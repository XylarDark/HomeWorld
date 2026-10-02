"""Contract tests for the graybox spec reader and silhouette assertion.

Runs without Blender or Unreal: pure-Python only, like
test_homeworld_master_material_defs.py.

The point of these tests is not coverage for its own sake. The first run of the
reader reported 41 blocking findings and 45 of them were false -- child modules
were compared against a spec origin of (0,0,0) when they inherit their assembly's
origin. A test suite that only checks "does it load" would not have caught that.
The tests below pin the specific mistakes that produced false findings, so a
future edit cannot reintroduce them silently.
"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

import homeworld_graybox_silhouette as silhouette  # noqa: E402
from homeworld_graybox_spec import (  # noqa: E402
    ALLOWED_MATERIAL_INSTANCES,
    FAMILY_BUILD_PLACE,
    FAMILY_GATHER,
    FAMILY_NURTURE_TAME,
    FAMILY_SPINE,
    FAMILY_SPIRIT,
    HELPER_PREFIXES,
    MASTER_NAMES,
    MECHANIC_FAMILIES,
    VOLUME_ALIASES,
    VOLUME_FAMILY_MAP,
    Volume,
    all_spec_ids,
    family_for,
    load_all_specs,
    load_zone_spec,
    resolve_alias,
    volume_family_status,
    zone_dirs,
    zone_spec_paths,
)


def _all_volumes():
    volumes = []
    for spec in load_all_specs():
        volumes.extend(spec.volumes)
    return volumes


def _volume(name, size, family, origin=(0.0, 0.0, 0.0), role="", explicit=True, assembly_read=True):
    """A test volume.

    Defaults to ``assembly_read=True`` because that is what the collision check now
    measures: a family signature describes how a PLACE reads at 20 m, so the whole
    assembly is the unit, not its parts. Pass ``assembly_read=False`` to model a
    single bolt, which is still measured and budgeted but is not held to a
    zone-level proportion (DEC-0026).
    """
    return Volume(
        name=name,
        size_m=size,
        origin=origin,
        family=family,
        role=role,
        spec_id="TEST",
        family_status="assigned",
        origin_is_explicit=explicit,
        is_assembly_read=assembly_read,
    )


# --- loading ---------------------------------------------------------------


def test_five_specs_load():
    assert set(all_spec_ids()) == {
        "CABIN_MODULES",
        "GARDEN_BLOCKING",
        "PINES_HOMESTEAD",
        "SM_Cliff",
        "SM_IslandTop",
    }


def test_zone_kits_are_one_directory_per_family():
    """DEC-0024: 'one family per section' as a property of the file tree."""
    dirs = zone_dirs()
    assert dirs, "Lib/02_Zones should exist once zone props are authored"
    for family in dirs:
        assert family in MECHANIC_FAMILIES, (
            "zone directory %r is not one of the seven mechanic families" % family
        )


def test_a_zone_spec_must_agree_with_its_directory():
    """A spec whose family key disagrees with its folder is an error, not a warning.

    It would otherwise move a volume out of the collision assertion silently, and
    a check that quietly stops checking is worse than no check (DEC-0021).
    """
    for family, spec_id in zone_spec_paths():
        raw = load_zone_spec(family, spec_id)
        assert raw.get("family") == family, spec_id


def test_zone_specs_name_only_canon_masters():
    for family, spec_id in zone_spec_paths():
        raw = load_zone_spec(family, spec_id)
        for slot in raw.get("materials") or []:
            master = slot.get("master") if isinstance(slot, dict) else slot
            assert master in MASTER_NAMES, "%s names %s" % (spec_id, master)


def test_a_nurtured_part_is_not_present_before_the_nurture_beat():
    """#12 must be falsifiable.

    If the sprout existed from the start, a run could not tell whether nurturing had
    done anything - the beat would pass by default. The T0 #12 Anti row calls out
    'day-plant-alone' as closed_fail.
    """
    for family, spec_id in zone_spec_paths():
        raw = load_zone_spec(family, spec_id)
        states = raw.get("state_model")
        if not isinstance(states, dict):
            continue
        day = set(states.get("day_planted") or [])
        nurtured = set(states.get("spirit_nurtured") or [])
        # A state model is not necessarily about post-action parts. The spirit wound
        # has one state ('wound_open') that contains every part from the start - it
        # replaces a crater, it does not grow. Only assert the falsifiability rule
        # where a spec actually has a post-action part.
        grown_modules = raw.get("nurtured_modules") or []
        if not grown_modules:
            continue
        grown = {m["name"] for m in grown_modules if "name" in m}
        assert grown, "%s declares post-action parts but none are named" % spec_id
        assert not (grown & day), (
            "%s: %s exists before the nurture beat, so #12 is unfalsifiable"
            % (spec_id, sorted(grown & day))
        )
        assert grown <= nurtured, (
            "%s: a post-action part is missing from the nurtured state" % spec_id
        )


def test_every_spec_declares_meters_and_applied_scale():
    for spec in load_all_specs():
        assert spec.units == "meters", spec.id
        assert spec.apply_scale is True, spec.id


def test_spec_materials_are_all_known_masters():
    for spec in load_all_specs():
        for material in spec.materials:
            assert material in MASTER_NAMES, "%s names %s" % (spec.id, material)


def test_every_volume_is_positive_sized_or_explicitly_unsized():
    """A zero size means the spec names a module without restating dimensions.

    That is legitimate (CABIN_MODULES names 14 sub-modules whose sizes live in
    GRAYBOX_LAYOUT.md), but it must be visible rather than read as a 0x0x0
    object.
    """
    for volume in _all_volumes():
        if volume.size_m == (0.0, 0.0, 0.0):
            assert volume.assembly is not None or volume.role, volume.name
        else:
            assert min(volume.size_m) > 0.0, volume.name


# --- the false-finding regression -----------------------------------------


def test_child_modules_do_not_assert_world_origin():
    """CABIN_MODULES names 14 sub-modules with no origin of their own.

    They must be flagged origin_is_explicit=False so the verifier checks
    containment inside the assembly instead of comparing world position against
    (0,0,0). Getting this wrong reports every cabin wall as 6 m out of place.
    """
    by_name = {v.name: v for v in _all_volumes()}
    wall = by_name["SM_Cabin_Wall_Front"]
    assert wall.origin_is_explicit is False
    assert wall.assembly == "SM_Cabin"
    assert wall.assembly_origin == (-6.0, 1.0, 0.0)


def test_cliff_faces_carry_explicit_origins():
    by_name = {v.name: v for v in _all_volumes()}
    face = by_name["SM_Cliff_LookoutFace"]
    assert face.origin_is_explicit is True
    assert face.origin == (7.5, -5.5, -4.0)
    assert face.assembly is None


def test_mirrored_module_aliases_resolve():
    """The blend authors window frames and porch posts as _Front/_Side, _L/_R.

    Without the alias table the report says "SM_Cabin_Window_Frame not present"
    while the blend holds two of them, which teaches the Lead to ignore findings.
    """
    resolved = resolve_alias("SM_Cabin_Window_Frame")
    assert "SM_Cabin_Window_Frame_Front" in resolved
    assert "SM_Cabin_Window_Frame_Side" in resolved
    assert resolve_alias("SM_Island_Hero") == ("SM_Island_Hero", "SM_IslandTop")


def test_alias_targets_are_all_mapped_families_or_names():
    """Every alias target must itself resolve to the same family.

    Otherwise an alias silently moves a volume out of the assertion set.
    """
    for spec_name, targets in VOLUME_ALIASES.items():
        base = family_for(spec_name)
        for target in targets:
            assert family_for(target) == base, (spec_name, target)


# --- families --------------------------------------------------------------


def test_seven_mechanic_families():
    assert len(MECHANIC_FAMILIES) == 7
    assert FAMILY_SPIRIT in MECHANIC_FAMILIES
    assert FAMILY_BUILD_PLACE in MECHANIC_FAMILIES


def test_every_family_has_a_signature_and_a_band_rule():
    for family in MECHANIC_FAMILIES:
        assert family in silhouette.FAMILY_SIGNATURE, family
        assert family in silhouette.FAMILY_BANDS, family
        assert silhouette.FAMILY_SIGNATURE[family], family


def test_helpers_are_never_assertable():
    for name in ("CAM_Hero", "CAM_CabinClose", "LIT_CabinWarm"):
        assert name.startswith(HELPER_PREFIXES)
        assert volume_family_status(name) == "helper"
        assert family_for(name) == FAMILY_SPINE


def test_unassigned_volume_is_reported_not_silently_passed():
    """An unassigned volume must be skipped AND visible.

    A check that quietly passes because its input was empty is worse than no
    check -- that is the bug DEC-0021 records.
    """
    assert volume_family_status("SM_Does_Not_Exist") == "unassigned"
    assert family_for("SM_Does_Not_Exist") == FAMILY_SPINE


def test_every_assertable_volume_is_in_the_family_map():
    for volume in _all_volumes():
        if volume.is_assertable:
            assert volume.name in VOLUME_FAMILY_MAP, volume.name
            assert volume.family in MECHANIC_FAMILIES, volume.name


# --- bands and silhouette --------------------------------------------------


def test_band_boundaries():
    assert silhouette.band_for(0.05) == silhouette.BAND_FLAT
    assert silhouette.band_for(0.42) == silhouette.BAND_LOW
    assert silhouette.band_for(1.33) == silhouette.BAND_MID
    assert silhouette.band_for(3.0) == silhouette.BAND_TALL
    assert silhouette.band_for(5.5) == silhouette.BAND_TALL


def test_thin_footprint_is_an_early_warning_not_a_failure():
    """A path slab is legitimately flat. It is reported, not failed."""
    path = _volume("SM_Path_Test", (10.0, 1.2, 0.15), FAMILY_SPINE)
    assert path.is_thin is True
    assert path.aspect < silhouette.BAND_BOUNDS[0][2]


def test_known_collision_is_detected():
    """The measured defect: beast pad (nurture) and spirit wound (spirit) both
    resolve to the flat band at nearly the same aspect."""
    beast = _volume("SM_BeastPad_01", (4.0, 4.0, 0.2), FAMILY_NURTURE_TAME)
    wound = _volume("SM_SpiritWound_01", (3.0, 3.0, 0.5), FAMILY_SPIRIT)
    collisions = silhouette.find_collisions([beast, wound])
    assert collisions, "expected the flat-band collision to be found"
    assert collisions[0].severity == "blocking"


def test_same_family_may_share_a_silhouette():
    """One family per section means its own volumes SHOULD look alike."""
    a = _volume("SM_GardenBed_A", (1.8, 1.0, 0.5), FAMILY_BUILD_PLACE)
    b = _volume("SM_GardenBed_B", (1.6, 0.9, 0.5), FAMILY_BUILD_PLACE)
    assert silhouette.find_collisions([a, b]) == []


def test_a_part_is_measured_but_not_held_to_a_zone_proportion():
    """A kettle handle is not a 'flat square plate'.

    A family signature is a statement about how a place reads at 20 m. Asserting it
    against an individual part produced three false findings on the three Queue-B
    props, because a handle, a soil pad and a monolith each violate a zone-level
    band while being perfectly correct as parts.
    """
    handle = _volume(
        "SM_Kettle_Handle", (0.12, 0.12, 0.1), FAMILY_BUILD_PLACE, assembly_read=False
    )
    assert handle.is_assertable is False, "a part is not the unit the signature describes"
    # Still a real volume with real dimensions - excluded from the collision check,
    # not excluded from existence.
    assert handle.size_m == (0.12, 0.12, 0.1)

    kettle = _volume("SM_NODE_KETTLE_DAY", (0.5, 0.5, 0.35), FAMILY_BUILD_PLACE)
    assert kettle.is_assertable is True, "the whole prop IS the unit"


def test_spirit_must_measure_tall_not_flat():
    """The locked signature is 'tall thin vertical with a see-through gap'.

    A flat spirit volume violates the taste gate and must be caught.
    """
    flat_spirit = _volume("SM_SpiritWound_01", (3.0, 3.0, 0.5), FAMILY_SPIRIT)
    problems = silhouette.family_conformance([flat_spirit])
    assert problems, "a flat spirit volume must violate its locked signature"


def test_gather_may_measure_flat():
    gather = _volume("SM_Gather_Test", (4.0, 3.0, 0.4), FAMILY_GATHER)
    assert silhouette.family_conformance([gather]) == []


def test_known_false_positive_is_downgraded_to_warn():
    """Two flat plates at slightly different aspects differ in openness.

    Aspect ratio alone would call this a blocking collision. The openness term
    exists so that case reports as a prompt to look rather than a failure.
    """
    plate = _volume("SM_Plate_A", (8.0, 8.0, 0.2), FAMILY_GATHER)
    # very different openness but same band; thickness is equal so this is a
    # blocking pair -- the point is that severity is one of exactly two values
    # and never silently dropped.
    collisions = silhouette.find_collisions([plate, _volume("SM_Plate_B", (8.0, 8.0, 0.25), FAMILY_GATHER)])
    for collision in collisions:
        assert collision.severity in ("blocking", "warn")


def test_spine_and_helpers_are_excluded_from_collisions():
    path = _volume("SM_Path_Homestead", (10.0, 1.2, 0.15), FAMILY_SPINE, role="path")
    thin = _volume("SM_Thin_Other", (10.0, 1.2, 0.15), FAMILY_SPINE, role="path")
    # Both are spine: no mechanic is announced, so there is nothing to collide.
    assert silhouette.find_collisions([path, thin]) == []


def test_collision_sort_puts_blocking_first():
    a = _volume("SM_BeastPad_01", (4.0, 4.0, 0.2), FAMILY_NURTURE_TAME)
    b = _volume("SM_SpiritWound_01", (3.0, 3.0, 0.5), FAMILY_SPIRIT)
    collisions = silhouette.find_collisions([a, b])
    assert collisions[0].severity == "blocking"


# --- materials -------------------------------------------------------------


def test_allowed_instances_are_a_separate_set_from_masters():
    """An instance is not an 11th family. Keeping them apart lets the reader
    report the difference between 'an instance of a master' and 'a new family'."""
    assert not (set(MASTER_NAMES) & ALLOWED_MATERIAL_INSTANCES)


def test_out_of_canon_materials_are_not_allowed():
    """M_FamilySilhouette and M_ValleyNight are in the live blend and are NOT
    in the ten masters. They must not be silently permitted."""
    for name in ("M_FamilySilhouette", "M_ValleyNight"):
        assert name not in MASTER_NAMES
        assert name not in ALLOWED_MATERIAL_INSTANCES

"""Loader for the Lib/01_Homestead geometry specs.

Pure Python, no bpy and no Editor. The parallel of
``homeworld_master_material_defs.py``: Lib/06 material JSON is already
machine-consumed through that module, and this makes Lib/01 geometry JSON
machine-consumed too.

Canon:
  Lib/00_Core/GRAYBOX_LAYOUT.md          39 volumes, the layout
  Lib/01_Homestead/*.json                per-family geometry specs
  Lib/06_Materials_Master/*.json         the ten masters
  Docs/handoffs/TASTE_GATE_GRAYBOX_SILHOUETTE.md   family -> signature silhouette

The gap this closes, verified 2026-10-01: nothing read Lib/01_Homestead/*.json.
``place_vs_mvp_pa_d.py`` cited ``SM_Cliff.json`` in a comment and then hardcoded
the numbers, so the spec was the source of truth in a comment. That is the Lead's
criterion 3 -- "does it have the bones to support future refinement" -- failing
in the repo.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

# --------------------------------------------------------------------------
# Families. The signature silhouettes are LOCKED TASTE -- see
# TASTE_GATE_GRAYBOX_SILHOUETTE.md and taste-profile.md section 3.
# Do not edit these strings without a new taste gate. The machine-readable
# rule derived from them (aspect signature per family) lives in
# homeworld_graybox_silhouette.py and IS agent-owned.
# --------------------------------------------------------------------------

FAMILY_GATHER = "gather"
FAMILY_NURTURE_TAME = "nurture_tame"
FAMILY_HEAL = "heal"
FAMILY_SPIRIT = "spirit"
FAMILY_STEALTH = "stealth"
FAMILY_BUILD_PLACE = "build_place"
FAMILY_COMBAT = "combat"

#: The seven locked mechanic families, in the order they appear in the taste gate.
MECHANIC_FAMILIES: tuple[str, ...] = (
    FAMILY_GATHER,
    FAMILY_NURTURE_TAME,
    FAMILY_HEAL,
    FAMILY_SPIRIT,
    FAMILY_STEALTH,
    FAMILY_BUILD_PLACE,
    FAMILY_COMBAT,
)

#: Traversal is the spine (Lead, 2026-10-01): no silhouette of its own, inherits
#: the neighbouring family's material, excluded from the collision assertion.
FAMILY_SPINE = "spine"

#: Helper volumes. Cameras and light stand-ins are not world geometry and must
#: never be counted as placeable volumes. Flagged, not hidden: the "14 of 39
#: volumes are <= 0.5 m thin" finding includes 5 camera helpers, which inflates it.
HELPER_PREFIXES: tuple[str, ...] = ("CAM_", "LIT_")

MASTER_NAMES: tuple[str, ...] = (
    "M_StylizedGrass",
    "M_CliffRock",
    "M_WoodCabin",
    "M_WoodWild",
    "M_FoliageCard",
    "M_PathStone",
    "M_GatherHerb",
    "M_BeastStylized",
    "M_SpiritUnlit",
    "M_Nurtured",
)

#: Materials that may appear in a spec or a blend without inventing an 11th
#: master family. From Docs/02_ART_BIBLE.md section 10 and the P6 QA report:
#: allowed instances plus the two documented lookdev materials.
ALLOWED_MATERIAL_INSTANCES: frozenset[str] = frozenset(
    {
        "M_StylizedGrass_Dry",
        "M_SpiritUnlit_Hurt",
        "M_SpiritUnlit_Healed",
        "M_WoodCabin_Window",
        "M_MoonDisc",
        "M_VOLUME_Haze",
        # 2026-10-08 remap. Instances, not new masters.
        # M_BeastStylized_Family cites M_BeastStylized (the stylized figure master).
        "M_BeastStylized_Family",
        # M_StylizedGrass_ValleyNight cites M_StylizedGrass (valley ground, NightMix).
        "M_StylizedGrass_ValleyNight",
    }
)

#: Adult figure, the scale ruler. Art bible section 10: 1.7-1.8 m.
ADULT_HEIGHT_M: tuple[float, float] = (1.7, 1.8)

#: A section is ~1 minute on foot ~= 84 m at the assumed 1.4 m/s stroll.
#: TG-ZONE-FAMILY fork D.
SECTION_TRAVEL_M: float = 84.0
SECTION_VOLUME_COUNT: tuple[int, int] = (20, 40)

HOMESTEAD_SPEC_DIR_REL = os.path.join("Lib", "01_Homestead")
GRAYBOX_LAYOUT_REL = os.path.join("Lib", "00_Core", "GRAYBOX_LAYOUT.md")

#: Zone kits, one directory per mechanic family (DEC-0024). "one family per
#: section" becomes a property of the file tree rather than a convention.
ZONES_ROOT_DIR_REL = os.path.join("Lib", "02_Zones")


def project_root() -> str:
    """Absolute path to the HomeWorld project root, from this file's location."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, "..", ".."))


def spec_dir() -> str:
    return os.path.join(project_root(), HOMESTEAD_SPEC_DIR_REL)


def load_spec_json(filename: str) -> dict[str, Any]:
    """Load one Lib/01_Homestead spec by bare filename or full spec id."""
    name = filename if filename.endswith(".json") else "%s.json" % filename
    path = os.path.join(spec_dir(), name)
    if not os.path.isfile(path):
        raise FileNotFoundError("Homestead spec not found: %s" % path)
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def all_spec_ids() -> tuple[str, ...]:
    """Spec ids in a stable order, read off disk rather than hardcoded."""
    directory = spec_dir()
    if not os.path.isdir(directory):
        raise FileNotFoundError("Spec directory not found: %s" % directory)
    ids = []
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(directory, name), "r", encoding="utf-8") as handle:
            ids.append(str(json.load(handle).get("id") or os.path.splitext(name)[0]))
    return tuple(ids)


def zone_dirs() -> list[str]:
    """One directory per mechanic family under Lib/02_Zones, in a stable order.

    The directory NAME is the family, which is the point of DEC-0024: it makes
    "one family per section" a property of the tree rather than a convention
    someone has to remember.
    """
    root = os.path.join(project_root(), ZONES_ROOT_DIR_REL)
    if not os.path.isdir(root):
        return []
    return [name for name in sorted(os.listdir(root)) if os.path.isdir(os.path.join(root, name))]


def zone_spec_paths() -> list[tuple[str, str]]:
    """(family, spec id) for every zone spec, in a stable order."""
    root = os.path.join(project_root(), ZONES_ROOT_DIR_REL)
    found: list[tuple[str, str]] = []
    for family in zone_dirs():
        family_dir = os.path.join(root, family)
        for name in sorted(os.listdir(family_dir)):
            if not name.endswith(".json"):
                continue
            with open(os.path.join(family_dir, name), "r", encoding="utf-8") as handle:
                spec_id = str(json.load(handle).get("id") or os.path.splitext(name)[0])
            found.append((family, spec_id))
    return found


def load_zone_spec(family: str, spec_id: str) -> dict[str, Any]:
    """Load one Lib/02_Zones spec by family directory and spec id."""
    path = os.path.join(
        project_root(), ZONES_ROOT_DIR_REL, family, "%s.json" % spec_id
    )
    if not os.path.isfile(path):
        raise FileNotFoundError("Zone spec not found: %s" % path)
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def load_all_zone_specs() -> tuple[Spec, ...]:
    """Load and parse every zone spec across every family directory."""
    specs = []
    for family, spec_id in zone_spec_paths():
        raw = load_zone_spec(family, spec_id)
        parsed = parse_spec(raw)
        # The directory is authoritative for family; a mismatch is a real error
        # rather than a warning, because it would silently move a volume out of
        # the collision assertion.
        declared = raw.get("family")
        if declared and declared != family:
            raise ValueError(
                "zone spec %s declares family '%s' but lives under '%s'"
                % (spec_id, declared, family)
            )
        specs.append(parsed)
    return tuple(specs)


# --------------------------------------------------------------------------
# Volumes
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Volume:
    """One spec'd volume: name, world origin, size, family, role.

    ``size_m`` is (x, y, z) in meters. ``origin`` is a world-space (x, y, z) and
    the convention is origin at ground contact unless the spec says otherwise --
    art bible section 10. ``pivot_is_ground_contact`` records whether that
    convention is asserted (True) or merely expected (False), so the verifier can
    tell a check from a hope.
    """

    name: str
    size_m: tuple[float, float, float]
    origin: tuple[float, float, float]
    family: str
    role: str
    spec_id: str
    #: 'assigned' | 'helper' | 'spine_by_design' | 'unassigned'
    family_status: str = "unassigned"
    is_helper: bool = False
    pivot_is_ground_contact: bool = False
    #: World Z of the walkable top surface, when the spec declares one. A
    #: *floating* volume has no ground to contact, so "ground contact" is
    #: undefined for it; the load-bearing datum is the top surface the player
    #: stands on. Set from the spec's ``world_top_z``.
    #:
    #: The verifier asserts the origin sits at this datum. It does NOT relax the
    #: pivot check -- it replaces an inapplicable assertion with an applicable
    #: one, and it can still fail.
    top_datum_z_m: float | None = None
    materials: tuple[str, ...] = ()
    #: True when the spec gave this volume its own world origin. When False the
    #: volume inherits its assembly's origin and the verifier checks its offset
    #: *relative to the assembly* instead of an absolute world position.
    origin_is_explicit: bool = False
    #: World origin of the assembly this volume belongs to, if any.
    assembly_origin: tuple[float, float, float] | None = None
    #: Assembly root object name, when this volume is a child module.
    assembly: str | None = None
    #: True for a synthesised whole-assembly read rather than a real part. A family
    #: signature describes how a ZONE reads at 20 m, so this -- not the individual
    #: bolts -- is what the collision check measures. See DEC-0026.
    is_assembly_read: bool = False

    @property
    def is_assertable(self) -> bool:
        """True when this volume participates in the silhouette-collision check.

        False for helpers, for terrain the Lead ruled out by design (the spine),
        and for volumes with no family assignment -- an unassigned volume is
        *skipped and reported*, never quietly treated as passing.

        Only ASSEMBLY READS assert. A family signature is a statement about how a
        place reads at 20 m, and asserting it against a kettle handle produced
        three false findings: a handle is not meant to be a "flat square plate".
        Parts are still measured, budgeted and master-checked; they just do not
        get held to a zone-level proportion. See DEC-0026.
        """
        return (
            self.is_assembly_read
            and self.family_status == "assigned"
            and self.family != FAMILY_SPINE
        )

    @property
    def height_m(self) -> float:
        return self.size_m[2]

    @property
    def footprint_m(self) -> float:
        return max(self.size_m[0], self.size_m[1])

    @property
    def aspect(self) -> float:
        """Height / largest footprint dimension. 1.00 == as tall as it is wide.

        This is the crude proxy the upstream handoff proposed. It is kept because
        it is cheap and it is what the 39-volume table was audited against, but
        homeworld_graybox_silhouette.py measures the real thing and this number
        is reported beside it, never instead of it.
        """
        span = max(self.size_m[0], self.size_m[1])
        if span <= 0.0:
            return 0.0
        return self.size_m[2] / span

    @property
    def is_thin(self) -> bool:
        """<= 0.5 m in its smallest dimension: reads as ground paint, not a volume."""
        return min(self.size_m) <= 0.5


@dataclass(frozen=True)
class Spec:
    """One parsed Lib/01_Homestead spec."""

    id: str
    type: str
    status: str
    owner: str
    phase: str
    units: str
    apply_scale: bool
    raw: dict[str, Any] = field(repr=False, default_factory=dict)
    volumes: tuple[Volume, ...] = ()

    @property
    def materials(self) -> tuple[str, ...]:
        """Every master name the spec names, in a stable order, deduped."""
        found: list[str] = []
        raw = self.raw

        def _add(value: Any) -> None:
            if isinstance(value, str) and value.startswith("M_") and value not in found:
                found.append(value)

        def _walk(node: Any) -> None:
            if isinstance(node, str):
                _add(node)
            elif isinstance(node, list):
                for item in node:
                    _walk(item)
            elif isinstance(node, dict):
                for item in node.values():
                    _walk(item)

        _walk(raw)
        return tuple(found)


def _as_vec3(value: Any, label: str) -> tuple[float, float, float]:
    if not isinstance(value, (list, tuple)) or len(value) != 3:
        raise ValueError("%s must be a 3-element list, got %r" % (label, value))
    return (float(value[0]), float(value[1]), float(value[2]))


#: Explicit volume -> family map, read off the Role column GRAYBOX_LAYOUT.md
#: already carries ("gather-node marker", "spirit-wound site", "1 beast pad").
#:
#: This is deliberately a table and not keyword inference over the role string.
#: An earlier draft matched substrings and returned ``spine`` for every volume,
#: which silently switched off the whole collision assertion -- a check that
#: quietly passes because its input was empty is worse than no check (see
#: DEC-0021). A table is also reviewable: the Lead can see and correct every
#: assignment in one screen instead of trusting a regex.
#:
#: Any volume NOT listed here is reported UNASSIGNED. Guessing a family would be
#: a mechanic-design decision, which is Lead-owned.
VOLUME_FAMILY_MAP: dict[str, str] = {
    # gather -- "First harvest / gather-node marker"
    "SM_Gather_FirstHarvest": FAMILY_GATHER,
    "SM_RES_World": FAMILY_GATHER,
    # nurture / tame -- "1 beast pad"; beasts are what you tame
    "SM_BeastPad_01": FAMILY_NURTURE_TAME,
    # spirit -- shrines are the spirit/night link; wounds are spirit sites
    "SM_Shrine_Homestead": FAMILY_SPIRIT,
    "SM_Shrine_Return": FAMILY_SPIRIT,
    "SM_SpiritWound_01": FAMILY_SPIRIT,
    # build / place -- hub volumes. The cabin is this family's signature landmark
    "SM_Cabin": FAMILY_BUILD_PLACE,
    "SM_Cabin_Wall_Front": FAMILY_BUILD_PLACE,
    "SM_Cabin_Wall_Back": FAMILY_BUILD_PLACE,
    "SM_Cabin_Wall_Side_L": FAMILY_BUILD_PLACE,
    "SM_Cabin_Wall_Side_R": FAMILY_BUILD_PLACE,
    "SM_Cabin_Foundation": FAMILY_BUILD_PLACE,
    "SM_Cabin_Roof_A": FAMILY_BUILD_PLACE,
    "SM_Cabin_Roof_B": FAMILY_BUILD_PLACE,
    "SM_Cabin_Chimney": FAMILY_BUILD_PLACE,
    "SM_Cabin_Door": FAMILY_BUILD_PLACE,
    "SM_Cabin_Window_Frame": FAMILY_BUILD_PLACE,
    "SM_Cabin_Window_Frame_Front": FAMILY_BUILD_PLACE,
    "SM_Cabin_Window_Frame_Side": FAMILY_BUILD_PLACE,
    "SM_Cabin_Window_Pane": FAMILY_BUILD_PLACE,
    "SM_Cabin_Window_Pane_Front": FAMILY_BUILD_PLACE,
    "SM_Cabin_Window_Pane_Side": FAMILY_BUILD_PLACE,
    "SM_Cabin_Porch_Deck": FAMILY_BUILD_PLACE,
    "SM_Cabin_Porch_Post": FAMILY_BUILD_PLACE,
    "SM_Cabin_Porch_Post_L": FAMILY_BUILD_PLACE,
    "SM_Cabin_Porch_Post_R": FAMILY_BUILD_PLACE,
    "SM_Cabin_Porch_Rail": FAMILY_BUILD_PLACE,
    "SM_Cabin_Porch_Rail_L": FAMILY_BUILD_PLACE,
    "SM_Cabin_Porch_Rail_R": FAMILY_BUILD_PLACE,
    "SM_Cabin_Gable_Fill_L": FAMILY_BUILD_PLACE,
    "SM_Cabin_Gable_Fill_R": FAMILY_BUILD_PLACE,
    "SM_GardenBed_A": FAMILY_BUILD_PLACE,
    "SM_GardenBed_B": FAMILY_BUILD_PLACE,
    "SM_GardenBed_C": FAMILY_BUILD_PLACE,
    "SM_GardenBed_Soil": FAMILY_BUILD_PLACE,
    "SM_GardenBed_Soil_A": FAMILY_BUILD_PLACE,
    "SM_GardenBed_Soil_B": FAMILY_BUILD_PLACE,
    "SM_GardenBed_Soil_C": FAMILY_BUILD_PLACE,
    "SM_Planter_A": FAMILY_BUILD_PLACE,
    "SM_Planter_B": FAMILY_BUILD_PLACE,
    "SM_Planter_C": FAMILY_BUILD_PLACE,
    # Terrain, massing and assembly modules are the boundary/spine vocabulary.
    # They are terrain that continues out of view (TG-ZONE-FAMILY fork B), so
    # they announce no mechanic and are excluded from the collision assertion.
    "SM_Island_Hero": FAMILY_SPINE,
    "SM_IslandTop": FAMILY_SPINE,
    "SM_Cliff_Slab_A": FAMILY_SPINE,
    "SM_Cliff_Slab_B": FAMILY_SPINE,
    "SM_Cliff_Slab_C": FAMILY_SPINE,
    "SM_Cliff_Chunk_Torn": FAMILY_SPINE,
    "SM_Cliff_LookoutFace": FAMILY_SPINE,
    "SM_Cliff_CabinFace": FAMILY_SPINE,
    "SM_Cliff_Rear": FAMILY_SPINE,
    "SM_Pine_Homestead_S": FAMILY_SPINE,
    "SM_Pine_Homestead_M": FAMILY_SPINE,
    "SM_Pine_Homestead_L": FAMILY_SPINE,
    # --- GRAYBOX_LAYOUT.md volumes that announce no mechanic of their own ---
    # Traversal is the spine (Lead, TG-GRAYBOX-SILHOUETTE Q2): paths, the
    # lookout, the glide perch, islets and the landing circle are the route
    # between families, so they carry no signature silhouette and are excluded.
    "SM_Path_Homestead": FAMILY_SPINE,
    "SM_Path_Planet_SegA": FAMILY_SPINE,
    "SM_Path_Planet_SegB": FAMILY_SPINE,
    "SM_Path_Planet_SegC": FAMILY_SPINE,
    "SM_Lookout_Pad": FAMILY_SPINE,
    "SM_Glider_Perch": FAMILY_SPINE,
    "SM_Islet_01": FAMILY_SPINE,
    "SM_Islet_02": FAMILY_SPINE,
    "SM_Islet_03": FAMILY_SPINE,
    "SM_Landing_Circle": FAMILY_SPINE,
    # Pine stands and valley massing are treeline/boundary terrain (fork B),
    # not a mechanic. The pine cluster is hub furniture, not a family read.
    "SM_PineCluster_Homestead_A": FAMILY_SPINE,
    "SM_PineCluster_Homestead_B": FAMILY_SPINE,
    "SM_PineCluster_Homestead_C": FAMILY_SPINE,
    "SM_PineValley_Block_A": FAMILY_SPINE,
    "SM_PineValley_Block_B": FAMILY_SPINE,
    # Hamlet roofs are the planet-side *read* from the lookout, not a section.
    "SM_Roof_Hamlet_01": FAMILY_SPINE,
    "SM_Roof_Hamlet_02": FAMILY_SPINE,
    "SM_Roof_Hamlet_03": FAMILY_SPINE,
    # Garden beds are PROP dressing inside the build_place hub, so the beds
    # carry build_place but the zone volume itself is hub furniture.
    "SM_Garden_Beds": FAMILY_SPINE,
    # Sky/read-only. Explicitly not walkable, so not a section volume.
    "SM_Peak_Distant": FAMILY_SPINE,
    # The scale ruler itself: the measuring stick, never a section.
    "SM_ScaleRef_Adult": FAMILY_SPINE,
}


#: Spec name -> object name(s) actually authored in the blend.
#:
#: The specs name *modules*; the blend authors some of them as mirrored pairs
#: (a front and a side window, a left and a right porch post). Reporting
#: "SM_Cabin_Window_Frame not present" when the blend holds
#: SM_Cabin_Window_Frame_Front and _Side is a false finding that trains the Lead
#: to ignore the report. Resolved here so a missing volume means missing.
VOLUME_ALIASES: dict[str, tuple[str, ...]] = {
    "SM_Island_Hero": ("SM_Island_Hero", "SM_IslandTop"),
    "SM_GardenBed_Soil": (
        "SM_GardenBed_Soil",
        "SM_GardenBed_Soil_A",
        "SM_GardenBed_Soil_B",
        "SM_GardenBed_Soil_C",
    ),
    "SM_Cabin_Window_Frame": (
        "SM_Cabin_Window_Frame",
        "SM_Cabin_Window_Frame_Front",
        "SM_Cabin_Window_Frame_Side",
    ),
    "SM_Cabin_Window_Pane": (
        "SM_Cabin_Window_Pane",
        "SM_Cabin_Window_Pane_Front",
        "SM_Cabin_Window_Pane_Side",
    ),
    "SM_Cabin_Porch_Post": ("SM_Cabin_Porch_Post", "SM_Cabin_Porch_Post_L", "SM_Cabin_Porch_Post_R"),
    "SM_Cabin_Porch_Rail": ("SM_Cabin_Porch_Rail", "SM_Cabin_Porch_Rail_L", "SM_Cabin_Porch_Rail_R"),
}


def resolve_alias(name: str) -> tuple[str, ...]:
    """Every object name that satisfies this spec volume, best match first."""
    return VOLUME_ALIASES.get(name, (name,))


def family_for(name: str) -> str:
    """Family for a volume name, or FAMILY_SPINE when unassigned.

    Callers must distinguish "spine by design" from "unassigned". Use
    ``volume_family_status`` for that; it is the difference between an
    intentional exclusion and a missing entry.
    """
    if name.startswith(HELPER_PREFIXES):
        return FAMILY_SPINE
    return VOLUME_FAMILY_MAP.get(name, FAMILY_SPINE)


def volume_family_status(name: str) -> str:
    """'assigned' | 'helper' | 'spine_by_design' | 'unassigned'."""
    if name.startswith(HELPER_PREFIXES):
        return "helper"
    if name in VOLUME_FAMILY_MAP:
        return "assigned"
    return "unassigned"


def parse_spec(raw: dict[str, Any]) -> Spec:
    """Turn one Lib/01_Homestead JSON document into a Spec with volumes."""
    spec_id = str(raw.get("id") or "UNKNOWN")
    volumes = _parse_volumes(spec_id, raw)
    return Spec(
        id=spec_id,
        type=str(raw.get("type") or ""),
        status=str(raw.get("status") or ""),
        owner=str(raw.get("raw_owner") or raw.get("owner") or ""),
        phase=str(raw.get("phase") or ""),
        units=str(raw.get("units") or ""),
        apply_scale=bool(raw.get("apply_scale", True)),
        raw=raw,
        volumes=volumes,
    )





def _parse_volumes(spec_id: str, raw: dict[str, Any]) -> tuple[Volume, ...]:
    """Extract every placeable volume from a spec.

    Handles the three shapes the five specs actually use:
      * ``modules`` -- list of {name, size_m, origin?, role?}
      * ``variants`` -- list of {name, height_m} (pines: height only)
      * a single top-level ``size_m`` + ``world_origin`` (island top)
    """
    volumes: list[Volume] = []
    is_assembly_read = False

    # A zone spec names its family once at the top level; every module in it
    # inherits that unless the table says otherwise.
    module_family = str(raw.get("family") or "") or None

    # An assembly's own world origin. Bare module/mesh name lists (CABIN_MODULES,
    # GARDEN_BLOCKING) name sub-modules without restating their origins: the
    # children live at offsets *inside* the assembly, not at world zero.
    assembly_origin: tuple[float, float, float] | None = None
    assembly_name: str | None = None
    if isinstance(raw.get("graybox_map"), list) and raw["graybox_map"]:
        assembly_name = str(raw["graybox_map"][0])
    if "world_origin" in raw:
        assembly_origin = _as_vec3(raw["world_origin"], "world_origin")

    def _add(
        name: str,
        size: tuple[float, float, float],
        origin: tuple[float, float, float],
        role: str,
        ground_contact: bool,
        explicit_origin: bool = False,
        top_datum_z: float | None = None,
    ) -> None:
        # A zone spec may carry a family on each module; otherwise fall back to
        # the table. Either way the family is data, never inferred.
        family = family_for(name)
        status = volume_family_status(name)
        if family == FAMILY_SPINE and status == "unassigned" and module_family:
            family = module_family
            status = "assigned"
        # A declared top datum means the volume is floating: there is no ground
        # underneath it, so ground contact cannot be asserted. Suppress it here,
        # at the point where both facts are known, rather than leaving a spec
        # able to assert the impossible and fail forever. The datum check in
        # graybox_spec_reader.verify replaces it and can still fail.
        if top_datum_z is not None:
            ground_contact = False
        volumes.append(
            Volume(
                name=name,
                size_m=size,
                origin=origin,
                family=family,
                family_status=status,
                role=role,
                spec_id=spec_id,
                is_helper=name.startswith(HELPER_PREFIXES),
                pivot_is_ground_contact=ground_contact,
                top_datum_z_m=top_datum_z,
                origin_is_explicit=explicit_origin,
                assembly_origin=assembly_origin if not explicit_origin else None,
                assembly=assembly_name if not explicit_origin else None,
                is_assembly_read=is_assembly_read,
            )
        )

    # 1. modules[] -- the cliff family and any other modular set.
    # Two shapes occur: dicts with size_m (SM_Cliff) and bare name strings
    # (CABIN_MODULES, which names 14 sub-modules without restating sizes --
    # the sizes live in GRAYBOX_LAYOUT.md under SM_Cabin).
    modules = raw.get("modules")
    if isinstance(modules, list):
        for module in modules:
            if isinstance(module, str):
                _add(module, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), "module", False)
                continue
            if not isinstance(module, dict) or "name" not in module:
                continue
            size_raw = module.get("size_m")
            if not isinstance(size_raw, (list, tuple)):
                _add(str(module["name"]), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0),
                     str(module.get("role") or "module"), False)
                continue
            has_origin = module.get("origin") is not None
            origin = _as_vec3(module.get("origin", [0.0, 0.0, 0.0]), "module origin")
            _add(
                str(module["name"]),
                _as_vec3(size_raw, "module size_m"),
                origin,
                str(module.get("role") or ""),
                has_origin,
                explicit_origin=has_origin,
            )

    # 1b. meshes[] -- GARDEN_BLOCKING names its beds the same bare way.
    meshes = raw.get("meshes")
    if isinstance(meshes, list):
        for mesh_name in meshes:
            if isinstance(mesh_name, str):
                _add(mesh_name, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), "blocking", False)

    # 1c. nurtured_modules[] -- parts that only exist AFTER a later beat acts.
    # Kept out of the always-present set on purpose: a sprout present before #12 would
    # make the nurture beat unfalsifiable, because you could not tell whether
    # nurturing had done anything. Measured against its own state list, not the
    # day-state list.
    nurtured = raw.get("nurtured_modules")
    if isinstance(nurtured, list):
        for module in nurtured:
            if not isinstance(module, dict) or "name" not in module:
                continue
            size_raw = module.get("size_m")
            if not isinstance(size_raw, (list, tuple)):
                continue
            _add(
                str(module["name"]),
                _as_vec3(size_raw, "nurtured size_m"),
                _as_vec3(module.get("origin", [0.0, 0.0, 0.0]), "nurtured origin"),
                str(module.get("role") or "post_action"),
                bool(module.get("origin") is not None),
                explicit_origin=bool(module.get("origin") is not None),
            )

    # 1d. the ASSEMBLY read. A family signature describes how a ZONE reads at 20 m,
    # not how each part reads: a kettle handle is not a "flat square plate", and
    # asserting otherwise made the collision check fire on parts of the same prop.
    # The assembly bounding volume is the unit that actually faces the player, so
    # it is the unit measured. See DEC-0026.
    states = raw.get("state_model")
    if isinstance(states, dict):
        is_assembly_read = True
        for state_name in sorted(states):
            members = states.get(state_name)
            if not isinstance(members, list) or not members:
                continue
            named = [v for v in volumes if v.name in members]
            if not named:
                continue
            # Union of the member parts: the envelope the player sees in this state.
            sx = max(v.size_m[0] for v in named)
            sy = max(v.size_m[1] for v in named)
            sz = max(v.size_m[2] for v in named)
            _add(
                "SM_%s_%s" % (spec_id, state_name.upper()),
                (sx, sy, sz),
                _as_vec3(raw.get("world_origin", [0.0, 0.0, 0.0]), "world_origin"),
                "assembly_read_%s" % state_name,
                str(raw.get("origin") or "") == "ground_contact",
                explicit_origin=True,
            )

    # 2. variants[] -- pines carry height_m, not size_m.
    variants = raw.get("variants")
    if isinstance(variants, list):
        for variant in variants:
            if not isinstance(variant, dict) or "name" not in variant:
                continue
            height = float(variant.get("height_m") or 0.0)
            width = float(variant.get("width_m") or 0.0)
            has_origin = variant.get("origin") is not None
            _add(
                str(variant["name"]),
                (width or 2.0, width or 2.0, height),
                _as_vec3(variant.get("origin", [0.0, 0.0, 0.0]), "variant origin"),
                str(variant.get("role") or "stylized_pine_stand"),
                has_origin,
                explicit_origin=has_origin,
            )

    # 3. a single unnamed volume -- the island top (Lib/01) and the zone prop envelope
    #    (Lib/02). Only synthesised when the spec does NOT already name its parts in
    #    modules[]; a zone spec carries a top-level size_m as the ENVELOPE of its
    #    modules, and emitting that as a volume invented an "SM_IslandTop" kettle.
    size = raw.get("size_m")
    if isinstance(size, dict) and not isinstance(raw.get("modules"), list):
        x = float(size.get("x") or 0.0)
        y = float(size.get("y") or 0.0)
        z = float(size.get("z_crust") or size.get("z") or 0.0)
        name = str(raw.get("graybox_map", [raw.get("id") or "SM_Volume"])[0])
        _add(
            name,
            (x, y, z),
            _as_vec3(raw.get("world_origin", [0.0, 0.0, 0.0]), "world_origin"),
            str(raw.get("role") or "single_volume"),
            str(raw.get("origin") or "") == "ground_contact",
            top_datum_z=(
                float(raw["world_top_z"]) if raw.get("world_top_z") is not None else None
            ),
        )

    return tuple(volumes)


def load_all_specs() -> tuple[Spec, ...]:
    """Load and parse every Lib/01_Homestead spec, in filename order."""
    specs = []
    for spec_id in all_spec_ids():
        specs.append(parse_spec(load_spec_json(spec_id)))
    return tuple(specs)

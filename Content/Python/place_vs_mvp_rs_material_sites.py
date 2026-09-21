# place_vs_mvp_rs_material_sites.py
# RS-B: idempotent planet-path material triad (trees / rocks / flowers) on L_VS_MVP_Markers.
# Day = AHomeWorldResourcePile reap; night sow markers = TargetPoints (nurture enum TBD).
# Run after place_vs_mvp_markers.py + place_vs_mvp_resource_piles.py; Safe-Build for pile class.
# Script-only — no .uasset/.umap commits; Conductor saves level locally (KEEP-LOCAL).

from __future__ import annotations

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

import homeworld_gc_site_setup as gc_site

PREFIX = "RSMaterial:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
PILE_BASE_CLASS = "/Script/HomeWorld.HomeWorldResourcePile"
FOLDER = "VS_MVP/Markers/RS_B"

BP_CANDIDATES = (
    "/Game/HomeWorld/Building/BP_VS_MVP_ResourcePile",
    "/Game/HomeWorld/Building/BP_WoodPile",
    "/Game/HomeWorld/Building/BP_HarvestableTree",
    "/Game/HomeWorld/Building/BP_HarvestableOre",
    "/Game/HomeWorld/Building/BP_HarvestableFlower",
)

# Planet-path offsets from landing / return shrine base (cm)
# GC-A: site kind drives RES (flowers → RES_FIBER grass, alternates RES_HERB)
DAY_SPECS = (
    ("GP_RS_Tree", "trees", "RES_WOOD", unreal.Vector(400.0, 200.0, 0.0)),
    ("GP_RS_Rock", "rocks", "RES_STONE", unreal.Vector(550.0, 80.0, 0.0)),
    ("GP_RS_Flower", "flowers", "RES_FIBER", unreal.Vector(480.0, -120.0, 0.0)),
)

# Night sow landmark TargetPoints (same sites; nurture C++ enum extension deferred)
NIGHT_SPECS = (
    ("GP_RS_Tree_Sow", unreal.Vector(400.0, 200.0, 50.0)),
    ("GP_RS_Rock_Sow", unreal.Vector(550.0, 80.0, 50.0)),
    ("GP_RS_Flower_Sow", unreal.Vector(480.0, -120.0, 50.0)),
)


def _log(msg: str) -> None:
    unreal.log(PREFIX + " " + str(msg))
    print(PREFIX, msg)


def find_actor_by_label(label: str):
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        try:
            if actor.get_actor_label() == label:
                return actor
        except Exception:
            continue
    return None


def _generated_class_from_bp(asset_path: str):
    if not unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        return None
    bp = unreal.load_asset(asset_path)
    if not bp:
        return None
    try:
        return bp.generated_class()
    except Exception:
        try:
            return bp.get_editor_property("generated_class")
        except Exception:
            return None


def _resolve_pile_spawn_class():
    base_cls = unreal.load_class(None, PILE_BASE_CLASS)
    if not base_cls:
        return None, None
    for asset_path in BP_CANDIDATES:
        gen_cls = _generated_class_from_bp(asset_path)
        if gen_cls:
            _log("spawn class from BP " + asset_path)
            return gen_cls, base_cls
    _log("spawn class from C++ HomeWorldResourcePile")
    return base_cls, base_cls


def _is_resource_pile(actor, pile_base_cls) -> bool:
    if not actor or not pile_base_cls:
        return False
    try:
        cls = actor.get_class()
        while cls:
            if cls == pile_base_cls:
                return True
            get_super = getattr(cls, "get_super_class", None)
            cls = get_super() if get_super else None
    except Exception:
        pass
    try:
        return "ResourcePile" in actor.get_class().get_name()
    except Exception:
        return False


def _add_tag(actor, tag_name: str) -> None:
    try:
        tags = list(actor.tags)
        tag = unreal.Name(tag_name)
        if tag not in tags:
            tags.append(tag)
            actor.tags = tags
    except Exception:
        try:
            actor.tags.add(unreal.Name(tag_name))
        except Exception:
            pass


def _apply_label(actor, label: str) -> None:
    try:
        actor.set_actor_label(label, True)
    except TypeError:
        try:
            actor.set_actor_label(label)
        except Exception as exc:
            _log("label warn " + label + ": " + str(exc))


def _configure_pile(actor, site_kind: str, resource_id: str) -> None:
    try:
        actor.set_editor_property("resource_type", unreal.Name(resource_id))
        actor.set_editor_property("amount_per_harvest", 1)
        actor.set_editor_property("b_deplete_until_dawn", False)
    except Exception as exc:
        _log("configure warn: " + str(exc))
    gc_site.apply_gc_site(actor, site_kind, resource_id)


def _planet_base() -> unreal.Vector:
    for label in (
        "SM_LandingCircle",
        "SM_Landing_Circle",
        "GP_Landing",
        "SM_Shrine_Return",
        "CRUMB_05",
        "CRUMB_04",
    ):
        actor = find_actor_by_label(label)
        if actor:
            loc = actor.get_actor_location()
            _log("planet base from " + label)
            return loc
    _log("planet base fallback origin")
    return unreal.Vector(2000.0, 0.0, 0.0)


def _load_level() -> bool:
    if not unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        _log("Level missing — run place_vs_mvp_markers.py first")
        return False
    return bool(unreal.EditorLoadingAndSavingUtils.load_map(LEVEL_PATH))


def _ensure_pile(
    spawn_cls,
    pile_base_cls,
    label: str,
    site_kind: str,
    resource_id: str,
    location: unreal.Vector,
):
    existing = find_actor_by_label(label)
    if existing and _is_resource_pile(existing, pile_base_cls):
        existing.set_actor_location(location, False, True)
        _configure_pile(existing, site_kind, resource_id)
        _add_tag(existing, label)
        _log("updated " + label + " " + site_kind + " " + resource_id)
        return existing
    if existing:
        try:
            unreal.EditorLevelLibrary.destroy_actor(existing)
        except Exception:
            pass
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(spawn_cls, location)
    if not actor:
        _log("FAIL spawn " + label)
        return None
    _apply_label(actor, label)
    _configure_pile(actor, site_kind, resource_id)
    _add_tag(actor, label)
    try:
        actor.set_folder_path(FOLDER)
    except Exception:
        pass
    _log("spawned " + label + " " + site_kind + " " + resource_id + " @ " + str(location))
    return actor


def _ensure_sow_marker(label: str, location: unreal.Vector):
    existing = find_actor_by_label(label)
    target_cls = unreal.load_class(None, "/Script/Engine.TargetPoint")
    if not target_cls:
        _log("FAIL TargetPoint class missing for " + label)
        return None
    if existing:
        existing.set_actor_location(location, False, True)
        _add_tag(existing, label)
        _log("updated sow marker " + label)
        return existing
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(target_cls, location)
    if not actor:
        _log("FAIL spawn sow " + label)
        return None
    _apply_label(actor, label)
    _add_tag(actor, label)
    try:
        actor.set_folder_path(FOLDER)
    except Exception:
        pass
    _log("spawned sow marker " + label)
    unreal.log("HomeWorld: RSMaterial sow marker ready " + label)
    return actor


def main() -> None:
    _log("start RS-B material triad")
    if not _load_level():
        return
    spawn_cls, pile_base = _resolve_pile_spawn_class()
    if not spawn_cls:
        _log("FAIL HomeWorldResourcePile class missing — Safe-Build")
        return
    base = _planet_base()
    ok = 0
    for label, site_kind, res_id, offset in DAY_SPECS:
        loc = unreal.Vector(base.x + offset.x, base.y + offset.y, base.z + offset.z)
        if _ensure_pile(spawn_cls, pile_base, label, site_kind, res_id, loc):
            ok += 1
            unreal.log("HomeWorld: RSMaterial day site " + label + " " + site_kind + " " + res_id)
    night_ok = 0
    for label, offset in NIGHT_SPECS:
        loc = unreal.Vector(base.x + offset.x, base.y + offset.y, base.z + offset.z)
        if _ensure_sow_marker(label, loc):
            night_ok += 1
    _log(
        "Done day=%d/3 night_markers=%d/3. PIE day: face GP_RS_* Interact → "
        "GATHER: RES_WOOD / RES_STONE / RES_FIBER (+ flint/grass flavor lines). "
        "Night sow nurture enum TBD — markers only. Save level KEEP-LOCAL."
        % (ok, night_ok)
    )


if __name__ == "__main__":
    main()

# place_vs_mvp_resource_piles.py
# D19-A / VP2-B: idempotent AHomeWorldResourcePile markers on L_VS_MVP_Markers (homestead gather).
# Run after place_vs_mvp_markers.py; Safe-Build required for C++ class.
# Script-only — no .uasset/.umap commits; Conductor saves level locally after spawn (KEEP-LOCAL).

from __future__ import annotations

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

import homeworld_gc_site_setup as gc_site

PREFIX = "ResourcePile:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
PILE_BASE_CLASS = "/Script/HomeWorld.HomeWorldResourcePile"
FOLDER = "VS_MVP/Markers"

# Concrete Blueprint subclasses (KEEP-LOCAL .uasset) — tried before C++ spawn.
BP_CANDIDATES = (
    "/Game/HomeWorld/Building/BP_VS_MVP_ResourcePile",
    "/Game/HomeWorld/Building/BP_WoodPile",
    "/Game/HomeWorld/Building/BP_HarvestableTree",
    "/Game/HomeWorld/Building/BP_HarvestableOre",
    "/Game/HomeWorld/Building/BP_HarvestableFlower",
)

# Near homestead cabin — stable labels + tags for MCP/PIE gather success-path
PILE_SPECS = (
    ("GP_Gather_WOOD", "trees", "RES_WOOD", unreal.Vector(150.0, -120.0, 0.0)),
    ("GP_Gather_STONE", "rocks", "RES_STONE", unreal.Vector(120.0, -200.0, 0.0)),
    ("GP_Gather_FIBER", "flowers", "RES_FIBER", unreal.Vector(220.0, -80.0, 0.0)),
    ("GP_Gather_BERRY", "berry", "RES_BERRY", unreal.Vector(180.0, -180.0, 0.0)),
    ("GP_Gather_SEED", "seed", "RES_SEED", unreal.Vector(260.0, -160.0, 0.0)),
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


def _load_base_pile_class():
    return unreal.load_class(None, PILE_BASE_CLASS)


def _resolve_pile_spawn_class():
    """Prefer concrete BP subclass if present locally; else C++ HomeWorldResourcePile."""
    base_cls = _load_base_pile_class()
    if not base_cls:
        return None, None

    for asset_path in BP_CANDIDATES:
        gen_cls = _generated_class_from_bp(asset_path)
        if gen_cls:
            _log("spawn class from BP " + asset_path)
            return gen_cls, base_cls

    _log("spawn class from C++ HomeWorldResourcePile (non-Abstract)")
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


def _read_resource_type(actor) -> str:
    try:
        value = actor.get_editor_property("resource_type")
        if value is None:
            return ""
        return str(value)
    except Exception:
        return ""


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
            return
    except Exception as exc:
        _log("label warn " + label + ": " + str(exc))
        return
    try:
        if actor.get_actor_label() != label:
            actor.set_actor_label(label)
    except Exception:
        pass


def _destroy_actor(actor) -> None:
    if not actor:
        return
    try:
        unreal.EditorLevelLibrary.destroy_actor(actor)
    except Exception:
        try:
            actor.destroy_actor()
        except Exception as exc:
            _log("destroy warn: " + str(exc))


def _homestead_base() -> unreal.Vector:
    for label in ("SM_Cabin", "GP_PlayerStart", "GP_N2_Stored"):
        actor = find_actor_by_label(label)
        if actor:
            return actor.get_actor_location()
    return unreal.Vector(0.0, 0.0, 0.0)


def _load_level() -> bool:
    if not unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        _log("Level missing — run place_vs_mvp_markers.py first")
        return False
    return bool(unreal.EditorLoadingAndSavingUtils.load_map(LEVEL_PATH))


def _configure_pile(actor, site_kind: str, resource_id: str) -> None:
    try:
        actor.set_editor_property("resource_type", unreal.Name(resource_id))
        actor.set_editor_property("amount_per_harvest", 1)
        actor.set_editor_property("b_deplete_until_dawn", False)
    except Exception as exc:
        _log("configure warn: " + str(exc))
    gc_site.apply_gc_site(actor, site_kind, resource_id)


def _find_pile_by_tag_or_resource(pile_base_cls, label: str, resource_id: str):
    tag_name = unreal.Name(label)
    res_name = unreal.Name(resource_id)
    fallback = None
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        if not _is_resource_pile(actor, pile_base_cls):
            continue
        try:
            if tag_name in actor.tags:
                return actor
        except Exception:
            pass
        try:
            if actor.get_editor_property("resource_type") == res_name:
                fallback = actor
        except Exception:
            pass
    return fallback


def _dedupe_extra_piles(pile_base_cls, label: str, resource_id: str, keep_actor) -> None:
    tag_name = unreal.Name(label)
    res_name = unreal.Name(resource_id)
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        if actor == keep_actor or not _is_resource_pile(actor, pile_base_cls):
            continue
        matches = False
        try:
            if actor.get_actor_label() == label:
                matches = True
        except Exception:
            pass
        if not matches:
            try:
                if tag_name in actor.tags:
                    matches = True
            except Exception:
                pass
        if not matches:
            try:
                if actor.get_editor_property("resource_type") == res_name:
                    matches = True
            except Exception:
                pass
        if matches:
            _log("remove duplicate " + label + " actor " + actor.get_name())
            _destroy_actor(actor)


def _ensure_pile(
    label: str,
    site_kind: str,
    resource_id: str,
    offset: unreal.Vector,
    base: unreal.Vector,
    spawn_cls,
    pile_base_cls,
) -> bool:
    loc = base + offset
    actor = find_actor_by_label(label)
    if not actor:
        actor = _find_pile_by_tag_or_resource(pile_base_cls, label, resource_id)

    if actor:
        if not _is_resource_pile(actor, pile_base_cls):
            _log("replace legacy " + label + " (" + actor.get_class().get_name() + ")")
            _destroy_actor(actor)
            actor = None

    if actor:
        actor.set_actor_location(loc, False, True)
        _apply_label(actor, label)
        try:
            actor.set_folder_path(FOLDER)
        except Exception:
            pass
        _add_tag(actor, label)
        _configure_pile(actor, site_kind, resource_id)
        _dedupe_extra_piles(pile_base_cls, label, resource_id, actor)
        _log("reuse " + label + " site=" + site_kind + " res=" + resource_id)
        return True

    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(spawn_cls, loc)
    if not actor:
        _log("FAIL spawn " + label + " (class=" + str(spawn_cls) + ")")
        return False

    _apply_label(actor, label)
    try:
        actor.set_folder_path(FOLDER)
    except Exception:
        pass
    _add_tag(actor, label)
    _configure_pile(actor, site_kind, resource_id)
    _dedupe_extra_piles(pile_base_cls, label, resource_id, actor)
    _log("spawn " + label + " site=" + site_kind + " res=" + resource_id)
    return True


def _verify_piles(pile_base_cls) -> None:
    for label, _site_kind, resource_id, _offset in PILE_SPECS:
        actor = find_actor_by_label(label)
        if not actor:
            actor = _find_pile_by_tag_or_resource(pile_base_cls, label, resource_id)
        if not actor:
            _log("verify FAIL missing " + label)
            continue
        actual_label = actor.get_actor_label()
        actual_res = _read_resource_type(actor)
        tag_ok = False
        try:
            tag_ok = unreal.Name(label) in actor.tags
        except Exception:
            pass
        _log(
            "verify "
            + label
            + " label="
            + actual_label
            + " res="
            + actual_res
            + " tag="
            + ("yes" if tag_ok else "no")
        )


def main() -> int:
    if not _load_level():
        return 1

    spawn_cls, pile_base_cls = _resolve_pile_spawn_class()
    if not spawn_cls or not pile_base_cls:
        _log("FAIL load spawn class — Safe-Build first")
        return 1

    base = _homestead_base()
    ok = True
    for label, site_kind, res_id, offset in PILE_SPECS:
        if not _ensure_pile(label, site_kind, res_id, offset, base, spawn_cls, pile_base_cls):
            ok = False

    _verify_piles(pile_base_cls)

    _log(
        "Done. PIE day/body: face GP_Gather_* within 280cm, Interact (E) or "
        "try_harvest_in_front() for GATHER: RES_WOOD / RES_STONE / RES_FIBER (+ flint/grass). "
        "Save level locally (KEEP-LOCAL)."
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

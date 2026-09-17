# place_vs_mvp_resource_piles.py
# VP2-B: idempotent AHomeWorldResourcePile markers on L_VS_MVP_Markers (homestead gather).
# Run after place_vs_mvp_markers.py; Safe-Build required for C++ class.
# Script-only — no .uasset/.umap commits; Conductor saves level locally after spawn.

from __future__ import annotations

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "ResourcePile:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
PILE_CLASS = "/Script/HomeWorld.HomeWorldResourcePile"
FOLDER = "VS_MVP/Markers"

# Near homestead cabin — stable labels for MCP/PIE gather success-path
PILE_SPECS = (
    ("GP_Gather_WOOD", "RES_WOOD", unreal.Vector(150.0, -120.0, 0.0)),
    ("GP_Gather_HERB", "RES_HERB", unreal.Vector(220.0, -80.0, 0.0)),
    ("GP_Gather_BERRY", "RES_BERRY", unreal.Vector(180.0, -180.0, 0.0)),
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


def _spawn_or_update(label: str, resource_id: str, offset: unreal.Vector, base: unreal.Vector) -> bool:
    loc = base + offset
    existing = find_actor_by_label(label)
    pile_cls = unreal.load_class(None, PILE_CLASS)
    if not pile_cls:
        _log("FAIL load class " + PILE_CLASS + " — Safe-Build first")
        return False

    if existing:
        actor = existing
        actor.set_actor_location(loc, False, True)
        _log("reuse " + label)
    else:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(pile_cls, loc)
        if not actor:
            _log("FAIL spawn " + label)
            return False
        try:
            actor.set_actor_label(label)
        except Exception:
            pass
        try:
            actor.set_folder_path(FOLDER)
        except Exception:
            pass
        _log("spawn " + label)

    try:
        actor.set_editor_property("resource_type", unreal.Name(resource_id))
        actor.set_editor_property("amount_per_harvest", 1)
        actor.set_editor_property("b_deplete_until_dawn", False)
    except Exception as exc:
        _log("configure warn " + label + ": " + str(exc))
    return True


def main() -> int:
    if not _load_level():
        return 1
    base = _homestead_base()
    ok = True
    for label, res_id, offset in PILE_SPECS:
        if not _spawn_or_update(label, res_id, offset, base):
            ok = False
    _log(
        "Done. PIE day/body: face GP_Gather_* within 280cm, Interact (E) or "
        "try_harvest_in_front() for GATHER: success logs."
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

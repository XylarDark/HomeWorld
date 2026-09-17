# place_vs_mvp_store_transfer.py
# PL-C PA-07: idempotent AHomeWorldStoreProp markers on L_VS_MVP_Markers (homestead).
# Run after place_vs_mvp_gp.py; Safe-Build required for new C++ class.

from __future__ import annotations

import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "StorePlace:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
TARGET_CLASS = "/Script/HomeWorld.HomeWorldStoreProp"
FOLDER = "VS_MVP/Markers"

# Six Stored props near cabin (cm offsets)
STORE_SPECS = (
    ("GP_Store_WOOD", "RES_WOOD", unreal.Vector(-350.0, 250.0, 0.0)),
    ("GP_Store_FIBER", "RES_FIBER", unreal.Vector(-400.0, 200.0, 0.0)),
    ("GP_Store_STONE", "RES_STONE", unreal.Vector(-450.0, 150.0, 0.0)),
    ("GP_Store_BERRY", "RES_BERRY", unreal.Vector(-350.0, 350.0, 0.0)),
    ("GP_Store_HERB", "RES_HERB", unreal.Vector(-400.0, 400.0, 0.0)),
    ("GP_Store_SEED", "RES_SEED", unreal.Vector(-450.0, 450.0, 0.0)),
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


def _cabin_base():
    for label in ("SM_Cabin", "GP_PlayerStart", "GP_N2_Stored"):
        a = find_actor_by_label(label)
        if a:
            return a.get_actor_location()
    return unreal.Vector(0.0, 0.0, 0.0)


def _load_level() -> bool:
    if not unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        _log("Level missing")
        return False
    return bool(unreal.EditorLoadingAndSavingUtils.load_map(LEVEL_PATH))


def _spawn_or_update(label: str, res_id: str, offset: unreal.Vector, base: unreal.Vector):
    loc = base + offset
    existing = find_actor_by_label(label)
    cls = unreal.load_class(None, TARGET_CLASS)
    if not cls:
        _log("FAIL load class " + TARGET_CLASS + " — Safe-Build first")
        return False
    if existing:
        actor = existing
        actor.set_actor_location(loc, False, True)
        _log("reuse " + label)
    else:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(cls, loc)
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

    # Configure component
    try:
        comp = actor.get_component_by_class(unreal.load_class(None, "/Script/HomeWorld.HomeWorldStoreTransferComponent"))
        if comp and hasattr(comp, "configure_resource"):
            comp.configure_resource(res_id)
        elif comp:
            comp.set_editor_property("resource_id", res_id)
    except Exception as e:
        _log("configure warn " + label + ": " + str(e))
    return True


def main() -> int:
    if not _load_level():
        return 1
    base = _cabin_base()
    ok = 0
    for label, res_id, offset in STORE_SPECS:
        if _spawn_or_update(label, res_id, offset, base):
            ok += 1
    unreal.EditorLevelLibrary.save_current_level()
    _log("DONE %d/%d store props" % (ok, len(STORE_SPECS)))
    return 0 if ok == len(STORE_SPECS) else 2


if __name__ == "__main__":
    raise SystemExit(main())

# place_vs_mvp_gc_craft.py — GC-B hub craft point on L_VS_MVP_Markers (bootstrap campfire recipe).
# DS-A: readable hub label + visible mesh at PIE via AHomeWorldCraftStation (KEEP-LOCAL save optional).
# Run after Safe-Build; idempotent GP_Craft_Hub actor.

from __future__ import annotations

import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "DS-CraftPlace:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
TARGET_CLASS = "/Script/HomeWorld.HomeWorldCraftStation"
HUB_LABEL = "GP_Craft_Hub"
FOLDER = "VS_MVP/Markers"
# HubBootstrap enum value 0
STATION_KIND_HUB = 0


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


def main() -> int:
    if not _load_level():
        return 1
    cls = unreal.load_class(None, TARGET_CLASS)
    if not cls:
        _log("FAIL load class — Safe-Build first")
        return 2
    base = _cabin_base()
    loc = base + unreal.Vector(-200.0, 300.0, 0.0)
    existing = find_actor_by_label(HUB_LABEL)
    if existing:
        actor = existing
        actor.set_actor_location(loc, False, True)
        _log("reuse " + HUB_LABEL)
    else:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(cls, loc)
        if not actor:
            _log("FAIL spawn " + HUB_LABEL)
            return 3
        try:
            actor.set_actor_label(HUB_LABEL)
        except Exception:
            pass
        try:
            actor.set_folder_path(FOLDER)
        except Exception:
            pass
        _log("spawn " + HUB_LABEL)
    try:
        actor.set_editor_property("station_kind", STATION_KIND_HUB)
    except Exception as e:
        _log("station_kind warn: " + str(e))
    try:
        import vs_mvp_ds_visual_helpers as ds_vis

        ds_vis.refresh_craft_station_visual(actor)
    except Exception as e:
        _log("DS-A visual hint warn: " + str(e))
    unreal.EditorLevelLibrary.save_current_level()
    _log("DONE hub craft point GP_Craft_Hub (label CRAFT HUB at PIE)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

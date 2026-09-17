# place_vs_mvp_nurture.py
# NP-E V7: idempotent N1_Crop + N2_Stored AHomeWorldNurtureTarget on homestead (L_VS_MVP_Markers).
# Run after place_vs_mvp_gp.py; Safe-Build required.

from __future__ import annotations

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "Nurture:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
JSON_REL = os.path.join("AssetCreation", "Exports", "MVP_CRUMB_SPLINE.json")
TARGET_CLASS = "/Script/HomeWorld.HomeWorldNurtureTarget"
NURTURE_COMPONENT_CLASS = "/Script/HomeWorld.HomeWorldNurtureComponent"
FOLDER = "VS_MVP/Markers"

# Offsets from SM_Cabin anchor (Blender m -> UE cm applied in blender_to_ue)
NURTURE_SPECS = (
    ("GP_N1_Crop", 0, "RES_SEED", unreal.Vector(200.0, -200.0, 0.0)),
    ("GP_N2_Stored", 1, "RES_WOOD", unreal.Vector(-250.0, 300.0, 0.0)),
)


def _log(msg: str) -> None:
    unreal.log(PREFIX + " " + str(msg))
    print(PREFIX, msg)


def _project_root():
    cwd = os.getcwd()
    if os.path.isdir(cwd) and "Content" in (os.listdir(cwd) or []):
        return cwd
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", ".."))


def blender_to_ue_cm(loc):
    x, y, z = float(loc[0]), float(loc[1]), float(loc[2])
    return unreal.Vector(x * 100.0, -y * 100.0, z * 100.0)


def find_actor_by_label(label: str):
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        try:
            if actor.get_actor_label() == label:
                return actor
        except Exception:
            continue
    return None


def _load_level() -> bool:
    if not unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        _log("Level missing — run place_vs_mvp_markers.py first")
        return False
    return bool(unreal.EditorLoadingAndSavingUtils.load_map(LEVEL_PATH))


def _homestead_cabin_base():
    cabin = find_actor_by_label("SM_Cabin")
    if cabin:
        return cabin.get_actor_location()
    gp = find_actor_by_label("GP_PlayerStart")
    if gp:
        return gp.get_actor_location()
    root = _project_root()
    json_path = os.path.join(root, JSON_REL)
    if os.path.isfile(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            entry = (data.get("anchors") or {}).get("SM_Cabin")
            if isinstance(entry, dict) and entry.get("location"):
                return blender_to_ue_cm(entry["location"])
        except Exception:
            pass
    return blender_to_ue_cm((-6.0, 1.0, 0.0))


def _configure_target(actor, target_enum: int, res_id: str) -> None:
    comp_class = unreal.load_class(None, NURTURE_COMPONENT_CLASS)
    if not comp_class or not hasattr(actor, "get_component_by_class"):
        return
    comp = actor.get_component_by_class(comp_class)
    if comp and hasattr(comp, "configure_target"):
        comp.configure_target(target_enum, unreal.Name(res_id))


def _ensure_target(label: str, target_enum: int, res_id: str, offset: unreal.Vector):
    existing = find_actor_by_label(label)
    if existing:
        _log("Reused %s" % label)
        _configure_target(existing, target_enum, res_id)
        return existing

    target_class = unreal.load_class(None, TARGET_CLASS)
    if not target_class:
        _log("HomeWorldNurtureTarget not found — run Safe-Build first")
        return None

    base = _homestead_cabin_base()
    loc = base + offset
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(target_class, loc, unreal.Rotator(0, 0, 0))
    if not actor:
        _log("Failed to spawn %s" % label)
        return None
    actor.set_actor_label(label)
    actor.set_folder_path(FOLDER)
    _configure_target(actor, target_enum, res_id)
    _log("Spawned %s @ %s (target=%d res=%s)" % (label, loc, target_enum, res_id))
    return actor


def main() -> int:
    if not _load_level():
        return 1

    ok = 0
    for label, target_enum, res_id, offset in NURTURE_SPECS:
        if _ensure_target(label, target_enum, res_id, offset):
            ok += 1

    if ok < len(NURTURE_SPECS):
        return 1

    try:
        unreal.EditorLevelLibrary.save_current_level()
        _log("Saved level")
    except Exception as exc:
        _log("Save warning: " + str(exc))

    _log("Done. PIE night at homestead: hw.Gather with seed/herb/wood, Phase 2, Interact (E) for NURTURE: logs.")
    return 0


if __name__ == "__main__":
    code = main()
    if code != 0:
        unreal.log_error(PREFIX + " finished with code %s" % code)

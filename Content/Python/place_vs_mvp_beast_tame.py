# place_vs_mvp_beast_tame.py
# NP-D: idempotent GP_BeastPad TargetPoint + UHomeWorldBeastTameComponent on L_VS_MVP_Markers.
# Spawns GP_BeastPad near CRUMB_Landing when no beast pad exists (planet slice V4).
# Run via MCP execute_python_script or Tools > Execute Python Script.
#
# Prerequisite: place_vs_mvp_markers.py (CRUMB_Landing TargetPoint).

from __future__ import annotations

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "BeastTame:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
JSON_REL = os.path.join("AssetCreation", "Exports", "MVP_CRUMB_SPLINE.json")
GP_BEAST_PAD_LABEL = "GP_BeastPad"
LANDING_CRUMB_LABEL = "CRUMB_Landing"
BEAST_PAD_TAGS = ("BeastPad", "SM_BeastPad_01")
TAME_COMPONENT_CLASS = "/Script/HomeWorld.HomeWorldBeastTameComponent"
FOLDER = "VS_MVP/Markers"
# Offset from landing circle toward planet path (cm) — readable beast pad on slice
SPAWN_OFFSET = unreal.Vector(200.0, 150.0, 0.0)


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
    if unreal.EditorLoadingAndSavingUtils.load_map(LEVEL_PATH):
        _log("Level loaded: " + LEVEL_PATH)
        return True
    _log("Could not load level: " + LEVEL_PATH)
    return False


def _actor_tag_names(actor) -> set:
    try:
        return {str(t) for t in list(actor.tags)}
    except Exception:
        return set()


def _apply_beast_pad_tags(actor) -> None:
    for tag in BEAST_PAD_TAGS:
        name = unreal.Name(tag)
        if hasattr(actor, "add_tag"):
            actor.add_tag(name)
        else:
            tags = list(actor.tags) if hasattr(actor, "tags") else []
            if tag not in {str(t) for t in tags}:
                tags.append(name)
                actor.tags = tags


def _find_beast_pad_actor():
    gp = find_actor_by_label(GP_BEAST_PAD_LABEL)
    if gp:
        return gp

    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        try:
            label = actor.get_actor_label()
        except Exception:
            label = ""
        tag_names = _actor_tag_names(actor)
        if tag_names.intersection(set(BEAST_PAD_TAGS)):
            return actor
        if "BeastPad" in label or "Beast_Pad" in label or "SM_BeastPad" in label:
            return actor
    return None


def _landing_location_from_json():
    root = _project_root()
    json_path = os.path.join(root, JSON_REL)
    if not os.path.isfile(json_path):
        return None
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return None
    for crumb in data.get("crumbs") or []:
        if isinstance(crumb, dict) and crumb.get("name") == LANDING_CRUMB_LABEL:
            loc = crumb.get("location")
            if loc:
                return blender_to_ue_cm(loc)
    return None


def _resolve_landing_location():
    landing = find_actor_by_label(LANDING_CRUMB_LABEL)
    if landing:
        _log("Using existing %s @ %s" % (LANDING_CRUMB_LABEL, landing.get_actor_location()))
        return landing.get_actor_location()
    json_loc = _landing_location_from_json()
    if json_loc:
        _log("Using %s from MVP_CRUMB_SPLINE.json" % LANDING_CRUMB_LABEL)
        return json_loc
    return None


def _spawn_beast_pad_target_point(location: unreal.Vector):
    rot = unreal.Rotator(0, 0, 0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.TargetPoint, location, rot)
    if not actor:
        _log("Failed to spawn TargetPoint %s" % GP_BEAST_PAD_LABEL)
        return None
    actor.set_actor_label(GP_BEAST_PAD_LABEL)
    actor.set_folder_path(FOLDER)
    _apply_beast_pad_tags(actor)
    _log("Spawned TargetPoint %s @ %s (tags: %s)" % (GP_BEAST_PAD_LABEL, location, ", ".join(BEAST_PAD_TAGS)))
    return actor


def _ensure_beast_pad_actor():
    existing = _find_beast_pad_actor()
    if existing:
        _log("Reused beast pad '" + existing.get_name() + "'")
        _apply_beast_pad_tags(existing)
        return existing

    landing_loc = _resolve_landing_location()
    if not landing_loc:
        _log("No %s — run place_vs_mvp_markers.py first" % LANDING_CRUMB_LABEL)
        return None

    spawn_loc = landing_loc + SPAWN_OFFSET
    return _spawn_beast_pad_target_point(spawn_loc)


def _has_tame_component(actor) -> bool:
    tame_class = unreal.load_class(None, TAME_COMPONENT_CLASS)
    if not tame_class:
        return False
    if hasattr(actor, "get_component_by_class"):
        return actor.get_component_by_class(tame_class) is not None
    return False


def _attach_tame_component(pad) -> bool:
    if _has_tame_component(pad):
        _log("Reused existing tame component on '" + pad.get_name() + "'")
        return True

    tame_class = unreal.load_class(None, TAME_COMPONENT_CLASS)
    if not tame_class:
        _log("HomeWorldBeastTameComponent not found — run Safe-Build first")
        return False

    try:
        comp = pad.add_component_by_class(tame_class, False, unreal.Transform(), False)
        if comp:
            pad.modify()
            _log("TAME: placed component on '" + pad.get_name() + "'")
            return True
        _log("add_component_by_class returned None")
    except Exception as exc:
        _log("Failed to add component: " + str(exc))
    return False


def main() -> int:
    if not _load_level():
        return 1

    pad = _ensure_beast_pad_actor()
    if not pad:
        return 1

    if not _attach_tame_component(pad):
        return 1

    try:
        unreal.EditorLevelLibrary.save_current_level()
        _log("Saved level")
    except Exception as exc:
        _log("Save warning: " + str(exc))

    _log("Done. PIE: gather RES_BERRY/HERB, face GP_BeastPad, Interact (E) for TAME: logs.")
    return 0


if __name__ == "__main__":
    code = main()
    if code != 0:
        unreal.log_error(PREFIX + " finished with code %s" % code)

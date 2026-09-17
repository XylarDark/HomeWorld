# place_vs_mvp_beast_tame.py
# NP-D/NP-E: idempotent AHomeWorldBeastPad near CRUMB_Landing on L_VS_MVP_Markers.
# C++ constructor creates UHomeWorldBeastTameComponent (no Editor add_component_by_class).
# Run via MCP execute_python_script or Tools > Execute Python Script.

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
BEAST_PAD_CLASS = "/Script/HomeWorld.HomeWorldBeastPad"
FOLDER = "VS_MVP/Markers"
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


def _load_beast_pad_class():
    return unreal.load_class(None, BEAST_PAD_CLASS)


def _is_beast_pad_actor(actor, beast_class) -> bool:
    if not actor or not beast_class:
        return False
    try:
        return actor.get_class() == beast_class
    except Exception:
        return False


def _destroy_actor(actor) -> None:
    try:
        name = actor.get_name()
        unreal.EditorLevelLibrary.destroy_actor(actor)
        _log("Destroyed legacy actor '%s'" % name)
    except Exception as exc:
        _log("Destroy warning: " + str(exc))


def _anchor_from_json(key: str):
    root = _project_root()
    json_path = os.path.join(root, JSON_REL)
    if not os.path.isfile(json_path):
        return None
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return None
    anchors = data.get("anchors") or {}
    entry = anchors.get(key)
    if isinstance(entry, dict) and entry.get("location"):
        return blender_to_ue_cm(entry["location"])
    return None


def _resolve_landing_location():
    landing = find_actor_by_label(LANDING_CRUMB_LABEL)
    if landing:
        _log("Using existing %s @ %s" % (LANDING_CRUMB_LABEL, landing.get_actor_location()))
        return landing.get_actor_location()
    json_loc = _anchor_from_json("SM_LandingCircle")
    if json_loc:
        _log("Using SM_LandingCircle from MVP_CRUMB_SPLINE.json")
        return json_loc
    return None


def _spawn_beast_pad(location: unreal.Vector, beast_class=None):
    if beast_class is None:
        beast_class = _load_beast_pad_class()
    if not beast_class:
        _log("HomeWorldBeastPad not found — run Safe-Build first")
        return None
    rot = unreal.Rotator(0, 0, 0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(beast_class, location, rot)
    if not actor:
        _log("Failed to spawn HomeWorldBeastPad")
        return None
    actor.set_actor_label(GP_BEAST_PAD_LABEL)
    actor.set_folder_path(FOLDER)
    _log("Spawned HomeWorldBeastPad %s @ %s (tame component in C++ ctor)" % (GP_BEAST_PAD_LABEL, location))
    return actor


def _ensure_beast_pad_actor():
    beast_class = _load_beast_pad_class()
    if not beast_class:
        _log("HomeWorldBeastPad not found — run Safe-Build first")
        return None

    labeled = find_actor_by_label(GP_BEAST_PAD_LABEL)
    if labeled and _is_beast_pad_actor(labeled, beast_class):
        _log("Reused HomeWorldBeastPad '%s'" % labeled.get_name())
        return labeled

    spawn_loc = None
    if labeled and not _is_beast_pad_actor(labeled, beast_class):
        spawn_loc = labeled.get_actor_location()
        try:
            legacy_class = labeled.get_class().get_name()
        except Exception:
            legacy_class = "unknown"
        _log(
            "Replacing legacy %s (%s) with HomeWorldBeastPad"
            % (GP_BEAST_PAD_LABEL, legacy_class)
        )
        _destroy_actor(labeled)

    if spawn_loc is None:
        for actor in unreal.EditorLevelLibrary.get_all_level_actors():
            if _is_beast_pad_actor(actor, beast_class):
                _log("Reused HomeWorldBeastPad '%s'" % actor.get_name())
                if actor.get_actor_label() != GP_BEAST_PAD_LABEL:
                    actor.set_actor_label(GP_BEAST_PAD_LABEL)
                return actor

        landing_loc = _resolve_landing_location()
        if not landing_loc:
            _log("No landing anchor — run place_vs_mvp_markers.py first")
            return None
        spawn_loc = landing_loc + SPAWN_OFFSET

    return _spawn_beast_pad(spawn_loc, beast_class)


def main() -> int:
    if not _load_level():
        return 1

    pad = _ensure_beast_pad_actor()
    if not pad:
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

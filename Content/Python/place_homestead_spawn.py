# place_homestead_spawn.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Config-driven: places or moves Player Start to plateau position from homestead_spawn_config.json
# (or planetoid_map_config volume_center + location_z). No ref images or GUI required.
# Idempotent; safe to run multiple times. See docs/MANUAL_EDITOR_TUTORIAL.md §9.

import json
import os

try:
    import unreal
except ImportError:
    print("place_homestead_spawn: Run this script inside Unreal Editor.")
    raise

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.normpath(os.path.join(_SCRIPT_DIR, "..", ".."))


def _log(msg):
    unreal.log("place_homestead_spawn: " + str(msg))
    print("place_homestead_spawn: " + str(msg))


def _load_plateau_position():
    """Return (x, y, z) from homestead_spawn_config.json or planetoid_map_config.json."""
    # Prefer dedicated config
    path = os.path.join(_SCRIPT_DIR, "homestead_spawn_config.json")
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            x = float(data.get("location_x", 0))
            y = float(data.get("location_y", 0))
            z = float(data.get("location_z", 500))
            return (x, y, z)
        except Exception as e:
            _log("Failed to load homestead_spawn_config: " + str(e))
    # Fallback: planetoid_map_config volume_center + location_z from homestead or default
    path = os.path.join(_SCRIPT_DIR, "planetoid_map_config.json")
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            x = float(data.get("volume_center_x", 0))
            y = float(data.get("volume_center_y", 0))
            z = float(data.get("volume_center_z", 0)) + 500.0
            return (x, y, z)
        except Exception as e:
            _log("Failed to load planetoid_map_config: " + str(e))
    return (0.0, 0.0, 500.0)


def main():
    _log("Start: place homestead spawn from config (idempotent).")
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        _log("No editor world open. Open the planetoid level first.")
        return

    x, y, z = _load_plateau_position()
    _log("Target plateau position: (%.0f, %.0f, %.0f)" % (x, y, z))

    existing = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.PlayerStart)
    if existing and len(existing) > 0:
        ps = existing[0]
        loc = ps.get_actor_location()
        new_loc = unreal.Vector(x, y, z)
        ps.set_actor_location(new_loc, False, False)
        _log("Moved existing Player Start to (%.0f, %.0f, %.0f)" % (x, y, z))
        return

    spawn_location = unreal.Vector(x, y, z)
    rotation = unreal.Rotator(0.0, 0.0, 0.0)
    ps = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PlayerStart, spawn_location, rotation)
    if ps:
        _log("Spawned Player Start at (%.0f, %.0f, %.0f)" % (x, y, z))
    else:
        _log("Failed to spawn Player Start; add one manually and run again or use homestead_plateau_from_ui.py with refs.")


if __name__ == "__main__":
    main()

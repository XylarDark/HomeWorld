# place_dungeon_entrance.py
# Run from Unreal Editor with target level open (DemoMap or planetoid): Tools -> Execute Python Script or via MCP.
# Idempotent: places a single dungeon entrance placeholder actor at the position in dungeon_map_config.json.
# If an actor with tag Dungeon_POI already exists, skips. Add Level Streaming or Open Level (dungeon sublevel) in Blueprint.
# Config: Content/Python/dungeon_map_config.json (dungeon_entrance_position).
# See docs/tasks/DAYS_16_TO_30.md (Day 24).

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

DUNGEON_TAG = "Dungeon_POI"
CUBE_MESH_PATH = "/Engine/BasicShapes/Cube"


def _log(msg):
    unreal.log("Dungeon entrance: " + str(msg))
    print("Dungeon entrance: " + str(msg))


def _load_config():
    """Load Content/Python/dungeon_map_config.json."""
    defaults = {"dungeon_entrance_position": [-800, 0, 100]}
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "dungeon_map_config.json")
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        pos = data.get("dungeon_entrance_position")
        if isinstance(pos, list) and len(pos) >= 3:
            defaults["dungeon_entrance_position"] = [float(pos[0]), float(pos[1]), float(pos[2])]
        return defaults
    except Exception as e:
        _log("Config load warning: " + str(e))
        return defaults


def _get_editor_world():
    if hasattr(unreal, "EditorLevelLibrary"):
        return unreal.EditorLevelLibrary.get_editor_world()
    return None


def _save_current_level():
    try:
        subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem) if hasattr(unreal, "get_editor_subsystem") else None
        if subsys and hasattr(subsys, "save_current_level"):
            subsys.save_current_level()
            return True
    except Exception:
        pass
    if hasattr(unreal, "EditorLevelLibrary") and hasattr(unreal.EditorLevelLibrary, "save_current_level"):
        unreal.EditorLevelLibrary.save_current_level()
        return True
    return False


def _find_existing_dungeon_entrance(world):
    """Return True if an actor with tag Dungeon_POI exists in the level."""
    if not world:
        return False
    try:
        for actor in unreal.EditorLevelLibrary.get_all_level_actors():
            if not actor:
                continue
            tags = actor.get_editor_property("tags") if hasattr(actor, "get_editor_property") else getattr(actor, "tags", None)
            if not tags:
                continue
            tag_strs = [str(t) for t in tags]
            if DUNGEON_TAG in tag_strs:
                _log("Dungeon entrance placeholder already present (actor with tag " + DUNGEON_TAG + ").")
                return True
    except Exception as e:
        _log("Could not enumerate actors: " + str(e))
    return False


def main():
    world = _get_editor_world()
    if not world:
        _log("No editor world. Open a level and run again.")
        return

    config = _load_config()
    pos = config["dungeon_entrance_position"]
    location = unreal.Vector(pos[0], pos[1], pos[2])
    rotation = unreal.Rotator(0, 0, 0)

    if _find_existing_dungeon_entrance(world):
        return

    try:
        actor_class = unreal.StaticMeshActor
        mesh = unreal.load_asset(CUBE_MESH_PATH)
        if not mesh:
            _log("Fallback: spawning StaticMeshActor without mesh (cube not found at " + CUBE_MESH_PATH + ").")
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, location, rotation)
        if not actor:
            _log("Failed to spawn dungeon entrance placeholder actor.")
            return
        tags = actor.get_editor_property("tags") if hasattr(actor, "get_editor_property") else getattr(actor, "tags", [])
        if tags is None:
            tags = []
        tag_strs = [str(t) for t in tags]
        if DUNGEON_TAG not in tag_strs:
            tags.append(unreal.Name(DUNGEON_TAG))
            if hasattr(actor, "set_editor_property"):
                actor.set_editor_property("tags", tags)
        if mesh and hasattr(actor, "get_component_by_class"):
            smc = actor.get_component_by_class(unreal.StaticMeshComponent)
            if smc and hasattr(smc, "set_editor_property"):
                smc.set_editor_property("static_mesh", mesh)
            elif smc and hasattr(smc, "set_static_mesh"):
                smc.set_static_mesh(mesh)
        _log("Placed dungeon entrance placeholder at " + str(pos) + ". Add Level Streaming or Open Level (dungeon sublevel) in Blueprint.")
        _save_current_level()
    except Exception as e:
        _log("Failed to place dungeon entrance: " + str(e))


if __name__ == "__main__":
    main()

# place_defend_gather_positions.py
# Run from Unreal Editor with DemoMap open: Tools -> Execute Python Script or via MCP execute_python_script.
# Idempotent: places one actor with tag DefendPosition and one with tag GatherPosition at
# demo_map_config.json "defend_position" and "gather_position". Skips if an actor with that tag already exists.
# List 62 T1/T3: Defend-at-night flow — family (Family tag) teleport to DefendPosition at night,
# return to GatherPosition at dawn. See DAY12_ROLE_PROTECTOR.md, CONSOLE_COMMANDS.md § Defend-at-night.

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

DEFEND_TAG = "DefendPosition"
GATHER_TAG = "GatherPosition"
CUBE_MESH_PATH = "/Engine/BasicShapes/Cube.Cube"


def _log(msg):
    unreal.log("Defend/Gather: " + str(msg))
    print("Defend/Gather: " + str(msg))


def _load_config():
    """Load Content/Python/demo_map_config.json; return defend_position and gather_position (cm)."""
    defaults = {
        "demo_level_path": "/Game/HomeWorld/Maps/DemoMap",
        "defend_position": [400, 0, 0],
        "gather_position": [180, 80, 0],
    }
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "demo_map_config.json")
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key in ("defend_position", "gather_position"):
            pos = data.get(key)
            if isinstance(pos, list) and len(pos) >= 3:
                defaults[key] = [float(pos[0]), float(pos[1]), float(pos[2])]
        if isinstance(data.get("demo_level_path"), str) and data["demo_level_path"]:
            defaults["demo_level_path"] = data["demo_level_path"]
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
        subsys = getattr(unreal, "get_editor_subsystem", None)
        if subsys:
            level_sys = subsys(unreal.LevelEditorSubsystem)
            if level_sys and hasattr(level_sys, "save_current_level"):
                level_sys.save_current_level()
                return True
    except Exception:
        pass
    if hasattr(unreal, "EditorLevelLibrary") and hasattr(unreal.EditorLevelLibrary, "save_current_level"):
        unreal.EditorLevelLibrary.save_current_level()
        return True
    return False


def _actor_has_tag(actor, tag_name):
    """Return True if actor has the given tag."""
    if not actor:
        return False
    tags = actor.get_editor_property("tags") if hasattr(actor, "get_editor_property") else getattr(actor, "tags", None)
    if not tags:
        return False
    return tag_name in [str(t) for t in tags]


def _find_actor_with_tag(tag_name):
    """Return first level actor with the given tag, or None."""
    try:
        for actor in unreal.EditorLevelLibrary.get_all_level_actors():
            if actor and _actor_has_tag(actor, tag_name):
                return actor
    except Exception as e:
        _log("Could not enumerate actors: " + str(e))
    return None


def _place_tagged_actor(world, tag_name, position, label):
    """If no actor with tag_name exists, spawn a StaticMeshActor (cube) at position and add tag. Return True if placed or already present."""
    if _find_actor_with_tag(tag_name):
        _log("Actor with tag " + tag_name + " already present; skip.")
        return True
    location = unreal.Vector(position[0], position[1], position[2])
    rotation = unreal.Rotator(0, 0, 0)
    actor = None
    try:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, location, rotation)
        if not actor:
            return False
        mesh = unreal.load_asset(CUBE_MESH_PATH) if hasattr(unreal, "load_asset") else None
        if mesh:
            smc = actor.get_component_by_class(unreal.StaticMeshComponent) if hasattr(actor, "get_component_by_class") else None
            if smc:
                if hasattr(smc, "set_editor_property"):
                    smc.set_editor_property("static_mesh", mesh)
                elif hasattr(smc, "set_static_mesh"):
                    smc.set_static_mesh(mesh)
        tags = actor.get_editor_property("tags") if hasattr(actor, "get_editor_property") else getattr(actor, "tags", [])
        if tags is None:
            tags = []
        if tag_name not in [str(t) for t in tags]:
            tags.append(unreal.Name(tag_name))
            if hasattr(actor, "set_editor_property"):
                actor.set_editor_property("tags", tags)
        _log("Placed " + label + " at " + str(position) + " (tag " + tag_name + ").")
        return True
    except Exception as e:
        _log("Failed to place " + label + ": " + str(e))
        return False


def main():
    _log("Start.")
    world = _get_editor_world()
    if not world:
        _log("No editor world. Open DemoMap (or target level) and run again.")
        return
    config = _load_config()
    placed_defend = _place_tagged_actor(world, DEFEND_TAG, config["defend_position"], "DefendPosition")
    placed_gather = _place_tagged_actor(world, GATHER_TAG, config["gather_position"], "GatherPosition")
    if placed_defend and placed_gather:
        _save_current_level()
        _log("Done. For Defend-at-night: add Family tag to family actors (e.g. run place_partner.py or place_child.py); then PIE, hw.TimeOfDay.Phase 2 (night) -> family move to Defend; Phase 0 or 3 -> return. See CONSOLE_COMMANDS.md § Defend-at-night.")
    else:
        _log("One or more placements failed.")


if __name__ == "__main__":
    main()

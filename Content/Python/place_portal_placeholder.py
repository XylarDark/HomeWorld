# place_portal_placeholder.py
# Run from Unreal Editor with DemoMap open (Tools -> Execute Python Script or via MCP).
# Idempotent: places a portal actor on the current level (intended: DemoMap) at the position in
# planetoid_map_config.json. Prefers AHomeWorldDungeonEntrance (trigger + Open Level); falls back
# to StaticMeshActor cube if the C++ class is unavailable. If an actor with tag Portal_To_Planetoid
# already exists, skips. See docs/AUTOMATION_GAPS.md and docs/GAP_SOLUTIONS_RESEARCH.md.
# Config: Content/Python/planetoid_map_config.json (portal_position, portal_level_to_open).

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

PORTAL_TAG = "Portal_To_Planetoid"
CUBE_MESH_PATH = "/Engine/BasicShapes/Cube"


def _log(msg):
    unreal.log("Portal placeholder: " + str(msg))
    print("Portal placeholder: " + str(msg))


def _load_config():
    """Load Content/Python/planetoid_map_config.json."""
    defaults = {
        "portal_position": [800, 0, 100],
        "portal_placeholder_label": "Portal_To_Planetoid",
        "portal_level_to_open": "Planetoid_Pride",
    }
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "planetoid_map_config.json")
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        pos = data.get("portal_position")
        if isinstance(pos, list) and len(pos) >= 3:
            defaults["portal_position"] = [float(pos[0]), float(pos[1]), float(pos[2])]
        if isinstance(data.get("portal_placeholder_label"), str):
            defaults["portal_placeholder_label"] = data["portal_placeholder_label"]
        if isinstance(data.get("portal_level_to_open"), str) and data["portal_level_to_open"]:
            defaults["portal_level_to_open"] = data["portal_level_to_open"]
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


def _find_existing_portal(world):
    """Return (True, actor) if an actor with tag Portal_To_Planetoid exists, else (False, None)."""
    if not world:
        return False, None
    try:
        for actor in unreal.EditorLevelLibrary.get_all_level_actors():
            if not actor:
                continue
            tags = actor.get_editor_property("tags") if hasattr(actor, "get_editor_property") else getattr(actor, "tags", None)
            if not tags:
                continue
            tag_strs = [str(t) for t in tags]
            if PORTAL_TAG in tag_strs:
                _log("Portal placeholder already present (actor with tag " + PORTAL_TAG + ").")
                return True, actor
    except Exception as e:
        _log("Could not enumerate actors: " + str(e))
    return False, None


def _set_level_to_open(actor, level_to_open):
    """Set LevelToOpen on actor (AHomeWorldDungeonEntrance). Tries set_editor_property, setattr, and multiple names. Returns True if set."""
    if not actor or not level_to_open:
        return False
    name_val = unreal.Name(level_to_open)
    # 1) set_editor_property with common UE Python name variants (C++ PascalCase, Blueprint snake_case, DisplayName)
    for val in (name_val, level_to_open):
        for prop_name in ("LevelToOpen", "level_to_open", "Level To Open"):
            try:
                actor.set_editor_property(prop_name, val)
                if _verify_level_to_open(actor, level_to_open):
                    _log("Set LevelToOpen via set_editor_property(%s) to %s" % (prop_name, level_to_open))
                    return True
            except Exception:
                continue
    # 2) setattr in case the property is exposed as an attribute
    for attr in ("LevelToOpen", "level_to_open"):
        try:
            setattr(actor, attr, name_val)
            if _verify_level_to_open(actor, level_to_open):
                _log("Set LevelToOpen via setattr(%s) to %s" % (attr, level_to_open))
                return True
        except Exception:
            continue
    _log("LevelToOpen could not be set from Python (tried set_editor_property and setattr). Set in Editor Details or use gui_automation/set_portal_level_to_open.py.")
    return False


def _verify_level_to_open(actor, expected):
    """Return True if actor's LevelToOpen reads back as expected."""
    for prop in ("LevelToOpen", "level_to_open"):
        try:
            v = actor.get_editor_property(prop)
            if v is None:
                continue
            s = str(v) if not hasattr(v, "to_string") else v.to_string()
            if expected in s or s == expected:
                return True
        except Exception:
            continue
    return False


def main():
    world = _get_editor_world()
    if not world:
        _log("No editor world. Open a level and run again.")
        return

    config = _load_config()
    pos = config["portal_position"]
    location = unreal.Vector(pos[0], pos[1], pos[2])
    rotation = unreal.Rotator(0, 0, 0)

    level_to_open = config.get("portal_level_to_open", "Planetoid_Pride")
    found, existing_actor = _find_existing_portal(world)
    if found and existing_actor:
        if _set_level_to_open(existing_actor, level_to_open):
            _save_current_level()
        return

    actor = None

    # Prefer AHomeWorldDungeonEntrance (trigger + Open Level) so portal works without manual Blueprint.
    try:
        entrance_class = unreal.load_class(None, "/Script/HomeWorld.HomeWorldDungeonEntrance")
        if entrance_class:
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(entrance_class, location, rotation)
            if actor:
                _set_level_to_open(actor, level_to_open)
    except Exception as e:
        _log("Could not spawn HomeWorldDungeonEntrance: " + str(e))

    # Fallback: spawn cube placeholder (designer adds Open Level in Blueprint).
    if not actor:
        try:
            actor_class = unreal.StaticMeshActor
            mesh = unreal.load_asset(CUBE_MESH_PATH)
            if not mesh:
                _log("Fallback: spawning StaticMeshActor without mesh (cube not found at " + CUBE_MESH_PATH + ").")
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, location, rotation)
            if actor and mesh and hasattr(actor, "get_component_by_class"):
                smc = actor.get_component_by_class(unreal.StaticMeshComponent)
                if smc and hasattr(smc, "set_editor_property"):
                    smc.set_editor_property("static_mesh", mesh)
                elif smc and hasattr(smc, "set_static_mesh"):
                    smc.set_static_mesh(mesh)
            _log("Placed cube placeholder; add Open Level (" + str(level_to_open) + ") in Blueprint.")
        except Exception as e:
            _log("Failed to place portal: " + str(e))
            return

    if not actor:
        _log("Failed to spawn portal actor.")
        return

    try:
        tags = actor.get_editor_property("tags") if hasattr(actor, "get_editor_property") else getattr(actor, "tags", [])
        if tags is None:
            tags = []
        tag_strs = [str(t) for t in tags]
        if PORTAL_TAG not in tag_strs:
            tags.append(unreal.Name(PORTAL_TAG))
            if hasattr(actor, "set_editor_property"):
                actor.set_editor_property("tags", tags)
        _log("Placed portal at " + str(pos) + " (LevelToOpen=" + str(level_to_open) + ").")
        _save_current_level()
    except Exception as e:
        _log("Failed to set tags or save: " + str(e))


if __name__ == "__main__":
    main()

# place_homestead_placeholders.py
# Run from Unreal Editor with the **Homestead** map open (Tools -> Execute Python Script or via MCP).
# Reads homestead_map_config.json "placeholder_actors" and spawns StaticMeshActor placeholders (Cube mesh)
# at the given positions with optional scale. Idempotent: re-running removes existing HomesteadPlaceholder-
# tagged actors and re-spawns from config. See docs/HOMESTEAD_MAP.md.

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

PLACEHOLDER_TAG = "HomesteadPlaceholder"
CUBE_MESH = "/Engine/BasicShapes/Cube"


def _log(msg):
    unreal.log("Homestead Placeholders: " + str(msg))
    print("Homestead Placeholders: " + str(msg))


def _load_config():
    """Load Content/Python/homestead_map_config.json."""
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "homestead_map_config.json")
        if not os.path.exists(config_path):
            return {"placeholder_actors": [], "homestead_level_path": "/Game/HomeWorld/Maps/Homestead"}
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        actors = [a for a in (data.get("placeholder_actors") or []) if isinstance(a, dict) and a.get("label")]
        return {"placeholder_actors": actors, "homestead_level_path": data.get("homestead_level_path", "/Game/HomeWorld/Maps/Homestead")}
    except Exception as e:
        _log("Config load warning: " + str(e))
        return {"placeholder_actors": [], "homestead_level_path": "/Game/HomeWorld/Maps/Homestead"}


def _get_current_level_path():
    """Return the asset path of the current editor level, or None."""
    try:
        world = unreal.EditorLevelLibrary.get_editor_world()
        if not world:
            return None
        path = world.get_path_name() if hasattr(world, "get_path_name") else ""
        if not path:
            return None
        if "." in path:
            path = path.split(".")[0]
        if ":" in path:
            path = path.split(":")[0]
        return path if path.startswith("/") else None
    except Exception:
        return None


def main():
    _log("Starting placeholder placement...")
    config = _load_config()
    homestead_path = config.get("homestead_level_path", "/Game/HomeWorld/Maps/Homestead")
    entries = config.get("placeholder_actors", [])

    current = _get_current_level_path()
    if not current or "Homestead" not in (current or ""):
        _log("Current level is not Homestead. Open Homestead map and run this script again.")
        return

    if not entries:
        _log("No placeholder_actors in config; nothing to place.")
        return

    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        _log("No editor world.")
        return

    # Idempotent: destroy existing placeholders with our tag
    all_actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)
    for a in (all_actors or []):
        try:
            tags = a.get_editor_property("tags") if hasattr(a, "get_editor_property") else getattr(a, "tags", None)
            if tags:
                tag_strs = [str(t) for t in tags]
                if PLACEHOLDER_TAG in tag_strs:
                    unreal.EditorLevelLibrary.destroy_actor(a)
        except Exception:
            pass

    cube_mesh = unreal.load_asset(CUBE_MESH) if unreal.EditorAssetLibrary.does_asset_exist(CUBE_MESH) else None
    if not cube_mesh:
        _log("Cube mesh not found at " + CUBE_MESH + "; spawning Actor placeholders instead.")

    rotation = unreal.Rotator(0.0, 0.0, 0.0)
    placed = 0
    for entry in entries:
        label = str(entry.get("label", "Placeholder"))
        x = float(entry.get("x", 0))
        y = float(entry.get("y", 0))
        z = float(entry.get("z", 0))
        scale = float(entry.get("scale", 1.0))
        location = unreal.Vector(x, y, z)

        if cube_mesh:
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, location, rotation)
            if actor:
                sm_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
                if sm_comp and hasattr(sm_comp, "set_static_mesh"):
                    sm_comp.set_static_mesh(cube_mesh)
                if hasattr(actor, "set_actor_scale3d"):
                    actor.set_actor_scale3d(unreal.Vector(scale, scale, scale))
                actor.set_actor_label(label)
                try:
                    if hasattr(actor, "add_tag"):
                        actor.add_tag(PLACEHOLDER_TAG)
                except Exception:
                    pass
                placed += 1
        else:
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Actor, location, rotation)
            if actor:
                actor.set_actor_label(label)
                try:
                    if hasattr(actor, "add_tag"):
                        actor.add_tag(PLACEHOLDER_TAG)
                except Exception:
                    pass
                placed += 1

    unreal.EditorLevelLibrary.save_current_level()
    _log("Placed %d placeholder actor(s). See Outliner (filter by label or tag %s)." % (placed, PLACEHOLDER_TAG))


if __name__ == "__main__":
    main()

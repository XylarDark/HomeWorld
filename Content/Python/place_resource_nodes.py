# place_resource_nodes.py
# Run from Unreal Editor with DemoMap open (Tools -> Execute Python Script or via MCP).
# Reads demo_map_config.json "resource_node_positions" and spawns BP_HarvestableTree at each position (cm).
# Idempotent: ensures Building folder exists (via ensure_week2_folders), then skips spawning if an actor
# of the same Blueprint class already exists within RADIUS_CM of that position.
# See docs/tasks/DAY7_RESOURCE_NODES.md.

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    raise

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

DEMO_LEVEL_SUBPATH = "DemoMap"
BP_HARVESTABLE_TREE_PATH = "/Game/HomeWorld/Building/BP_HarvestableTree"
RADIUS_CM = 150.0  # consider "already placed" if an instance exists within this distance


def _log(msg):
    unreal.log("Resource nodes: " + str(msg))


def _load_config():
    """Load Content/Python/demo_map_config.json."""
    defaults = {
        "demo_level_path": "/Game/HomeWorld/Maps/DemoMap",
        "resource_node_positions": [],
    }
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "demo_map_config.json")
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        positions = data.get("resource_node_positions")
        if isinstance(positions, list):
            out = []
            for p in positions:
                if isinstance(p, dict) and "x" in p and "y" in p and "z" in p:
                    out.append({"x": float(p["x"]), "y": float(p["y"]), "z": float(p["z"])})
            defaults["resource_node_positions"] = out
        defaults["demo_level_path"] = data.get("demo_level_path", defaults["demo_level_path"])
        return defaults
    except Exception as e:
        _log("Config load warning: " + str(e))
        return defaults


def _get_editor_world():
    """Editor world; prefer UnrealEditorSubsystem, fallback EditorLevelLibrary."""
    try:
        import level_loader
        return level_loader.get_editor_world()
    except Exception:
        return unreal.EditorLevelLibrary.get_editor_world() if hasattr(unreal, "EditorLevelLibrary") else None


def _save_current_level():
    """Save current level; prefer LevelEditorSubsystem, fallback EditorLevelLibrary."""
    try:
        subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem) if hasattr(unreal, "get_editor_subsystem") else None
        if subsys and hasattr(subsys, "save_current_level"):
            return subsys.save_current_level()
    except Exception:
        pass
    if hasattr(unreal, "EditorLevelLibrary") and hasattr(unreal.EditorLevelLibrary, "save_current_level"):
        unreal.EditorLevelLibrary.save_current_level()
        return True
    return False


def _get_current_level_path():
    """Return the asset path of the current editor level, or None."""
    try:
        world = _get_editor_world()
        if not world:
            return None
        path = world.get_path_name() if hasattr(world, "get_path_name") else ""
        if not path or "." not in path:
            return None
        path = path.split(".")[0]
        if ":" in path:
            path = path.split(":")[0]
        return path if path.startswith("/") else None
    except Exception:
        return None


def _actor_location_cm(actor):
    """Return (x, y, z) in cm or None."""
    try:
        loc = actor.get_actor_location()
        if loc is not None:
            return (loc.x, loc.y, loc.z)
    except Exception:
        pass
    return None


def _distance_cm(a, b):
    """Euclidean distance between (x,y,z) tuples in cm."""
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5


def main():
    _log("Starting resource node placement...")
    # Ensure /Game/HomeWorld/Building/ exists so BP_HarvestableTree can be created there
    try:
        import ensure_week2_folders
        ensure_week2_folders.main()
    except Exception as e:
        _log("Could not ensure Building folder: " + str(e))
    config = _load_config()
    demo_path = config.get("demo_level_path", "/Game/HomeWorld/Maps/DemoMap")
    positions = config.get("resource_node_positions", [])

    current = _get_current_level_path()
    if not current or DEMO_LEVEL_SUBPATH not in (current or ""):
        _log("Current level is not DemoMap. Open DemoMap and run this script again.")
        return

    if not positions:
        _log("No resource_node_positions in config; add positions to demo_map_config.json.")
        return

    bp_asset = unreal.load_asset(BP_HARVESTABLE_TREE_PATH) if unreal.EditorAssetLibrary.does_asset_exist(BP_HARVESTABLE_TREE_PATH) else None
    if not bp_asset:
        _log("Blueprint not found at " + BP_HARVESTABLE_TREE_PATH + ". Create BP_HarvestableTree per docs/tasks/DAY7_RESOURCE_NODES.md.")
        return

    try:
        actor_class = bp_asset.generated_class() if callable(getattr(bp_asset, "generated_class", None)) else getattr(bp_asset, "generated_class", None)
        if not actor_class:
            actor_class = bp_asset.get_editor_property("generated_class")
    except Exception as e:
        _log("Could not get generated_class from Blueprint: %s. Create BP_HarvestableTree per docs/tasks/DAY7_RESOURCE_NODES.md." % e)
        return
    if not actor_class:
        _log("Could not get generated_class from Blueprint; try spawning manually.")
        return

    world = _get_editor_world()
    if not world:
        _log("No editor world.")
        return

    # Existing actors of this class (for idempotency)
    existing = unreal.GameplayStatics.get_all_actors_of_class(world, actor_class) or []
    existing_locs = []
    for a in existing:
        loc = _actor_location_cm(a)
        if loc:
            existing_locs.append(loc)

    spawned = 0
    for pos in positions:
        target = (pos["x"], pos["y"], pos["z"])
        if any(_distance_cm(target, ex) <= RADIUS_CM for ex in existing_locs):
            continue
        location = unreal.Vector(target[0], target[1], target[2])
        rotation = unreal.Rotator(0, 0, 0)
        try:
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, location, rotation)
            if actor:
                existing_locs.append(target)
                spawned += 1
                _log("Spawned at (%.0f, %.0f, %.0f)" % (target[0], target[1], target[2]))
        except Exception as e:
            _log("Failed to spawn at (%.0f, %.0f, %.0f): %s" % (target[0], target[1], target[2], e))

    _log("Done. Spawned %d new resource node(s); %d position(s) already had an instance." % (spawned, len(positions) - spawned))
    if spawned > 0:
        _save_current_level()
        _log("Level saved.")


if __name__ == "__main__":
    main()

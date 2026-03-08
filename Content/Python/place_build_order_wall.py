# place_build_order_wall.py
# Run from Unreal Editor with DemoMap open: Tools -> Execute Python Script or via MCP execute_python_script.
# Idempotent: ensures BP_BuildOrder_Wall exists (calls create_bp_build_order_wall), then places one incomplete
# build order at demo_map_config.json "build_order_wall_position". Skips if an actor with tag "BuildOrder"
# (or of class BP_BuildOrder_Wall) already exists within RADIUS_CM of that position.
# List 60 / MVP full scope: agentic building — DemoMap has build order(s) and family agents (place_mass_spawner_demomap.py).

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

BP_BUILD_ORDER_WALL_PATH = "/Game/HomeWorld/Building/BP_BuildOrder_Wall"
RADIUS_CM = 300.0


def _log(msg):
    unreal.log("BuildOrder Wall place: " + str(msg))
    print("BuildOrder Wall place: " + str(msg))


def _load_config():
    """Load Content/Python/demo_map_config.json; return dict with build_order_wall_position."""
    defaults = {
        "build_order_wall_position": [100, -60, 0],
    }
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "demo_map_config.json")
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        pos = data.get("build_order_wall_position")
        if isinstance(pos, list) and len(pos) >= 3:
            defaults["build_order_wall_position"] = [float(pos[0]), float(pos[1]), float(pos[2])]
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


def _ensure_bp_build_order_wall():
    """Create BP_BuildOrder_Wall if missing (idempotent)."""
    if unreal.EditorAssetLibrary.does_asset_exist(BP_BUILD_ORDER_WALL_PATH):
        return True
    try:
        import create_bp_build_order_wall
        create_bp_build_order_wall.main()
        return unreal.EditorAssetLibrary.does_asset_exist(BP_BUILD_ORDER_WALL_PATH)
    except Exception as e:
        _log("Could not create BP_BuildOrder_Wall: " + str(e) + ". Run create_bp_build_order_wall.py first.")
        return False


def _distance_cm(a, b):
    """Return distance between two [x,y,z] positions in cm."""
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5


def _find_existing_build_order_near(world, position, radius_cm):
    """Return True if an actor with tag BuildOrder or of class BP_BuildOrder_Wall exists within radius_cm of position."""
    try:
        for actor in unreal.EditorLevelLibrary.get_all_level_actors():
            if not actor:
                continue
            tags = actor.get_editor_property("tags") if hasattr(actor, "get_editor_property") else getattr(actor, "tags", None)
            if tags and "BuildOrder" in [str(t) for t in tags]:
                loc = actor.get_actor_location()
                pos = [loc.x, loc.y, loc.z] if hasattr(loc, "x") else [float(getattr(loc, "x", 0)), float(getattr(loc, "y", 0)), float(getattr(loc, "z", 0))]
                if _distance_cm(position, pos) <= radius_cm:
                    _log("Build order already present within " + str(radius_cm) + " cm (tag BuildOrder).")
                    return True
            try:
                cls = actor.get_class()
                if cls and hasattr(cls, "get_name") and "BuildOrder_Wall" in cls.get_name():
                    loc = actor.get_actor_location()
                    pos = [loc.x, loc.y, loc.z] if hasattr(loc, "x") else [float(getattr(loc, "x", 0)), float(getattr(loc, "y", 0)), float(getattr(loc, "z", 0))]
                    if _distance_cm(position, pos) <= radius_cm:
                        _log("Build order already present within " + str(radius_cm) + " cm (BP_BuildOrder_Wall).")
                        return True
            except Exception:
                continue
    except Exception as e:
        _log("Could not enumerate actors: " + str(e))
    return False


def main():
    _log("Start.")
    world = _get_editor_world()
    if not world:
        _log("No editor world. Open DemoMap (or target level) and run again.")
        return

    if not _ensure_bp_build_order_wall():
        return

    config = _load_config()
    pos = config["build_order_wall_position"]
    location = unreal.Vector(pos[0], pos[1], pos[2])
    rotation = unreal.Rotator(0, 0, 0)

    if _find_existing_build_order_near(world, pos, RADIUS_CM):
        _log("Done (build order already placed).")
        return

    actor = None
    try:
        bp_asset = unreal.load_asset(BP_BUILD_ORDER_WALL_PATH)
        if bp_asset:
            gen_class = None
            if hasattr(bp_asset, "generated_class"):
                try:
                    gen_class = bp_asset.generated_class()
                except Exception:
                    pass
            if not gen_class and hasattr(bp_asset, "get_editor_property"):
                try:
                    gen_class = bp_asset.get_editor_property("generated_class")
                except Exception:
                    pass
            if gen_class:
                actor = unreal.EditorLevelLibrary.spawn_actor_from_class(gen_class, location, rotation)
                if actor:
                    _log("Placed BP_BuildOrder_Wall at " + str(pos) + ".")
    except Exception as e:
        _log("Could not spawn BP_BuildOrder_Wall: " + str(e))

    if not actor:
        _log("Failed to place build order. Ensure BP_BuildOrder_Wall exists (run create_bp_build_order_wall.py) and level is open.")
        return

    _save_current_level()
    _log("Done.")


if __name__ == "__main__":
    main()

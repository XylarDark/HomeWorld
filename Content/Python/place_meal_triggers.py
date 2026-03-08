# place_meal_triggers.py
# Run from Unreal Editor with DemoMap open: Tools -> Execute Python Script or via MCP execute_python_script.
# Idempotent: ensures BP_MealTrigger_Breakfast, BP_MealTrigger_Lunch, BP_MealTrigger_Dinner exist, then places them at
# demo_map_config.json breakfast_position, lunch_position, dinner_position. Skips if an actor with tag already
# exists within RADIUS_CM. List 57 T2 (breakfast), T3 (lunch), T4 (dinner). See CONSOLE_COMMANDS.md; MVP_TUTORIAL_PLAN List 3, 6, 7.

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

BP_BREAKFAST_PATH = "/Game/HomeWorld/Building/BP_MealTrigger_Breakfast"
BP_LUNCH_PATH = "/Game/HomeWorld/Building/BP_MealTrigger_Lunch"
BP_DINNER_PATH = "/Game/HomeWorld/Building/BP_MealTrigger_Dinner"
DEMO_LEVEL_SUBPATH = "DemoMap"
RADIUS_CM = 200.0


def _log(msg):
    unreal.log("Place meal triggers: " + str(msg))
    print("Place meal triggers: " + str(msg))


def _load_config():
    """Load Content/Python/demo_map_config.json; return dict with breakfast_position, lunch_position, dinner_position."""
    defaults = {
        "demo_level_path": "/Game/HomeWorld/Maps/DemoMap",
        "breakfast_position": [200, 80, 0],
        "lunch_position": [250, 80, 0],
        "dinner_position": [300, 80, 0],
    }
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "demo_map_config.json")
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        pos = data.get("breakfast_position")
        if isinstance(pos, list) and len(pos) >= 3:
            defaults["breakfast_position"] = [float(pos[0]), float(pos[1]), float(pos[2])]
        pos = data.get("lunch_position")
        if isinstance(pos, list) and len(pos) >= 3:
            defaults["lunch_position"] = [float(pos[0]), float(pos[1]), float(pos[2])]
        pos = data.get("dinner_position")
        if isinstance(pos, list) and len(pos) >= 3:
            defaults["dinner_position"] = [float(pos[0]), float(pos[1]), float(pos[2])]
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


def _ensure_bp_breakfast():
    """Create BP_MealTrigger_Breakfast if missing (idempotent)."""
    if unreal.EditorAssetLibrary.does_asset_exist(BP_BREAKFAST_PATH):
        return True
    try:
        import create_bp_meal_trigger_breakfast
        create_bp_meal_trigger_breakfast.main()
        return unreal.EditorAssetLibrary.does_asset_exist(BP_BREAKFAST_PATH)
    except Exception as e:
        _log("Could not create BP_MealTrigger_Breakfast: " + str(e) + ". Run create_bp_meal_trigger_breakfast.py first.")
        return False


def _distance_cm(a, b):
    """Return distance between two [x,y,z] positions in cm."""
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5


def _find_existing_meal_near(world, position, radius_cm, tag_name, bp_name_substring):
    """Return True if an actor with tag or Blueprint name exists within radius_cm of position."""
    try:
        for actor in unreal.EditorLevelLibrary.get_all_level_actors():
            if not actor:
                continue
            tags = actor.get_editor_property("tags") if hasattr(actor, "get_editor_property") else getattr(actor, "tags", None)
            if tags and tag_name in [str(t) for t in tags]:
                loc = actor.get_actor_location()
                if hasattr(loc, "x"):
                    pos = [loc.x, loc.y, loc.z]
                else:
                    pos = [float(getattr(loc, "x", 0)), float(getattr(loc, "y", 0)), float(getattr(loc, "z", 0))]
                if _distance_cm(position, pos) <= radius_cm:
                    _log(tag_name + " trigger already present within " + str(radius_cm) + " cm.")
                    return True
            try:
                cls = actor.get_class()
                if cls and hasattr(cls, "get_name") and bp_name_substring in cls.get_name():
                    loc = actor.get_actor_location()
                    if hasattr(loc, "x"):
                        pos = [loc.x, loc.y, loc.z]
                    else:
                        pos = [float(getattr(loc, "x", 0)), float(getattr(loc, "y", 0)), float(getattr(loc, "z", 0))]
                    if _distance_cm(position, pos) <= radius_cm:
                        _log(tag_name + " trigger already present within " + str(radius_cm) + " cm (" + bp_name_substring + ").")
                        return True
            except Exception:
                continue
    except Exception as e:
        _log("Could not enumerate actors: " + str(e))
    return False


def _ensure_bp_lunch():
    """Create BP_MealTrigger_Lunch if missing (idempotent)."""
    if unreal.EditorAssetLibrary.does_asset_exist(BP_LUNCH_PATH):
        return True
    try:
        import create_bp_meal_trigger_lunch
        create_bp_meal_trigger_lunch.main()
        return unreal.EditorAssetLibrary.does_asset_exist(BP_LUNCH_PATH)
    except Exception as e:
        _log("Could not create BP_MealTrigger_Lunch: " + str(e) + ". Run create_bp_meal_trigger_lunch.py first.")
        return False


def _ensure_bp_dinner():
    """Create BP_MealTrigger_Dinner if missing (idempotent)."""
    if unreal.EditorAssetLibrary.does_asset_exist(BP_DINNER_PATH):
        return True
    try:
        import create_bp_meal_trigger_dinner
        create_bp_meal_trigger_dinner.main()
        return unreal.EditorAssetLibrary.does_asset_exist(BP_DINNER_PATH)
    except Exception as e:
        _log("Could not create BP_MealTrigger_Dinner: " + str(e) + ". Run create_bp_meal_trigger_dinner.py first.")
        return False


def main():
    _log("Start.")
    world = _get_editor_world()
    if not world:
        _log("No editor world. Open DemoMap (or target level) and run again.")
        return

    if not _ensure_bp_breakfast():
        return

    config = _load_config()
    pos = config["breakfast_position"]
    location = unreal.Vector(pos[0], pos[1], pos[2])
    rotation = unreal.Rotator(0, 0, 0)

    if _find_existing_meal_near(world, pos, RADIUS_CM, "Breakfast", "MealTrigger_Breakfast"):
        pass  # continue to lunch
    else:
        actor = None
        try:
            bp_asset = unreal.load_asset(BP_BREAKFAST_PATH)
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
                        _log("Placed BP_MealTrigger_Breakfast at " + str(pos) + ".")
        except Exception as e:
            _log("Could not spawn BP_MealTrigger_Breakfast: " + str(e))
        if not actor:
            _log("Failed to place breakfast trigger. Ensure BP_MealTrigger_Breakfast exists and level is open.")

    # Lunch (List 57 T3)
    if not _ensure_bp_lunch():
        _log("Skipping lunch placement.")
    else:
        pos_lunch = config["lunch_position"]
        location_lunch = unreal.Vector(pos_lunch[0], pos_lunch[1], pos_lunch[2])
        if _find_existing_meal_near(world, pos_lunch, RADIUS_CM, "Lunch", "MealTrigger_Lunch"):
            _log("Lunch trigger already placed.")
        else:
            actor_lunch = None
            try:
                bp_lunch = unreal.load_asset(BP_LUNCH_PATH)
                if bp_lunch:
                    gen_class = None
                    if hasattr(bp_lunch, "generated_class"):
                        try:
                            gen_class = bp_lunch.generated_class()
                        except Exception:
                            pass
                    if not gen_class and hasattr(bp_lunch, "get_editor_property"):
                        try:
                            gen_class = bp_lunch.get_editor_property("generated_class")
                        except Exception:
                            pass
                    if gen_class:
                        actor_lunch = unreal.EditorLevelLibrary.spawn_actor_from_class(gen_class, location_lunch, rotation)
                        if actor_lunch:
                            _log("Placed BP_MealTrigger_Lunch at " + str(pos_lunch) + ".")
            except Exception as e:
                _log("Could not spawn BP_MealTrigger_Lunch: " + str(e))
            if not actor_lunch:
                _log("Failed to place lunch trigger.")

    # Dinner (List 57 T4)
    if not _ensure_bp_dinner():
        _log("Skipping dinner placement.")
    else:
        pos_dinner = config["dinner_position"]
        location_dinner = unreal.Vector(pos_dinner[0], pos_dinner[1], pos_dinner[2])
        if _find_existing_meal_near(world, pos_dinner, RADIUS_CM, "Dinner", "MealTrigger_Dinner"):
            _log("Dinner trigger already placed.")
        else:
            actor_dinner = None
            try:
                bp_dinner = unreal.load_asset(BP_DINNER_PATH)
                if bp_dinner:
                    gen_class = None
                    if hasattr(bp_dinner, "generated_class"):
                        try:
                            gen_class = bp_dinner.generated_class()
                        except Exception:
                            pass
                    if not gen_class and hasattr(bp_dinner, "get_editor_property"):
                        try:
                            gen_class = bp_dinner.get_editor_property("generated_class")
                        except Exception:
                            pass
                    if gen_class:
                        actor_dinner = unreal.EditorLevelLibrary.spawn_actor_from_class(gen_class, location_dinner, rotation)
                        if actor_dinner:
                            _log("Placed BP_MealTrigger_Dinner at " + str(pos_dinner) + ".")
            except Exception as e:
                _log("Could not spawn BP_MealTrigger_Dinner: " + str(e))
            if not actor_dinner:
                _log("Failed to place dinner trigger.")

    _save_current_level()
    _log("Done.")


if __name__ == "__main__":
    main()

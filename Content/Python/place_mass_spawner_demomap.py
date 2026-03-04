# place_mass_spawner_demomap.py
# Run from Unreal Editor with DemoMap open (Tools -> Execute Python Script or via MCP).
# Idempotent: places a Mass Spawner on the current level with MEC_FamilyGatherer config,
# spawn count, and bounds. If a Mass Spawner already exists, reuses and updates it.
# Config: Content/Python/demo_map_config.json (mass_spawner_*). See DAY11_FAMILY_SPAWN.md.

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

DEMO_LEVEL = "/Game/HomeWorld/Maps/DemoMap"
MEC_PATH = "/Game/HomeWorld/Mass/MEC_FamilyGatherer"
SPAWNER_LABEL = "MassSpawner_FamilyGatherer"
CUBE_MESH = "/Engine/BasicShapes/Cube"


def _log(msg):
    unreal.log("Mass Spawner: " + str(msg))
    print("Mass Spawner: " + str(msg))


def _load_config():
    defaults = {
        "mass_spawner_position": [0, 0, 100],
        "mass_spawner_spawn_count": 5,
        "mass_spawner_extent_x": 1000,
        "mass_spawner_extent_y": 1000,
        "mass_spawner_extent_z": 200,
    }
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "demo_map_config.json")
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in data.items():
            if k.startswith("mass_spawner_") and k in defaults:
                if isinstance(v, (list, tuple)) and len(v) >= 3 and k == "mass_spawner_position":
                    defaults[k] = [float(v[0]), float(v[1]), float(v[2])]
                elif isinstance(v, (int, float)) and "extent" in k:
                    defaults[k] = float(v)
                elif isinstance(v, int) and "count" in k:
                    defaults[k] = max(1, v)
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


def _ensure_demomap_open():
    world = _get_editor_world()
    if not world:
        _log("No editor world.")
        return False
    current_path = world.get_path_name() if hasattr(world, "get_path_name") else ""
    if DEMO_LEVEL not in current_path and "/DemoMap" not in current_path:
        _log("DemoMap not current level. Open DemoMap and run again.")
        return False
    return True


def _find_mass_spawner_class():
    for path in ["/Script/MassSpawner.MassSpawner", "/Script/MassGameplay.MassSpawner", "/Script/MassSpawner.MassSpawnerActor"]:
        cls = unreal.load_class(None, path)
        if cls:
            return cls
    return None


def _find_existing_spawner(world):
    try:
        for actor in unreal.EditorLevelLibrary.get_all_level_actors():
            if not actor:
                continue
            cls_name = actor.get_class().get_name() if hasattr(actor, "get_class") else ""
            if "MassSpawner" in cls_name:
                return actor
            if actor.get_actor_label() == SPAWNER_LABEL:
                return actor
    except Exception as e:
        _log("Find existing: " + str(e))
    return None


def main():
    _log("Start.")
    if not _ensure_demomap_open():
        return
    config = _load_config()
    world = _get_editor_world()
    if not world:
        return

    spawner_class = _find_mass_spawner_class()
    if not spawner_class:
        _log("Mass Spawner class not found. Enable MassSpawner/MassGameplay plugins. Place Mass Spawner manually: Modes -> Mass Spawner.")
        return

    existing = _find_existing_spawner(world)
    if existing:
        _log("Reusing existing Mass Spawner: " + str(existing.get_name()))
        spawner = existing
    else:
        pos = config["mass_spawner_position"]
        loc = unreal.Vector(pos[0], pos[1], pos[2])
        rot = unreal.Rotator(0, 0, 0)
        try:
            spawner = unreal.EditorLevelLibrary.spawn_actor_from_class(spawner_class, loc, rot)
        except Exception as e:
            _log("Spawn failed: " + str(e))
            return
        if not spawner:
            _log("spawn_actor_from_class returned None.")
            return
        try:
            spawner.set_actor_label(SPAWNER_LABEL)
        except Exception:
            pass
        _log("Placed Mass Spawner at " + str(pos))

    mec_asset = unreal.EditorAssetLibrary.load_asset(MEC_PATH) if unreal.EditorAssetLibrary.does_asset_exist(MEC_PATH) else None
    if mec_asset:
        for prop in ["config", "Config", "entity_config", "EntityConfig", "mass_entity_config", "MassEntityConfig"]:
            try:
                spawner.set_editor_property(prop, mec_asset)
                _log("Set " + prop + " = MEC_FamilyGatherer.")
                break
            except Exception:
                pass
    else:
        _log("MEC_FamilyGatherer not found at " + MEC_PATH + ". Run create_mec_family_gatherer.py first.")

    count = config.get("mass_spawner_spawn_count", 5)
    for prop in ["spawn_count", "SpawnCount", "num_to_spawn", "NumToSpawn", "count", "Count"]:
        try:
            spawner.set_editor_property(prop, count)
            _log("Set " + prop + " = " + str(count))
            break
        except Exception:
            pass

    _save_current_level()
    _log("Done. If Config/SpawnCount did not apply, set in Details: Config = MEC_FamilyGatherer, Spawn count = " + str(count) + ", Bounds as needed.")


if __name__ == "__main__":
    main()

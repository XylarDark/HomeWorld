# setup_planetoid_pcg.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Idempotent: ensures planetoid level exists, Planetoid_POI_PCG graph and POI BPs exist,
# opens planetoid level, tags Landscape with PCG_Landscape, places/sizes PCG Volume,
# assigns Planetoid_POI_PCG, sets Get Landscape Data By Tag, triggers Generate, saves level.
# Config: Content/Python/planetoid_map_config.json.
# See docs/tasks/DAYS_16_TO_30.md (Day 16-17), docs/PCG_SETUP.md.

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)
import create_pcg_forest as pcg_forest
import create_planetoid_poi_pcg as planetoid_pcg
import ensure_planetoid_level
import create_bp_poi_placeholders as poi_placeholders
import level_loader
import importlib
importlib.reload(pcg_forest)
importlib.reload(planetoid_pcg)
importlib.reload(ensure_planetoid_level)
importlib.reload(poi_placeholders)
importlib.reload(level_loader)

PCG_GRAPH_PATH = "/Game/HomeWorld/PCG/Planetoid_POI_PCG"
PLANETOID_VOLUME_LABEL = "PCG_Planetoid_POI"


def _log(msg):
    unreal.log("Setup planetoid PCG: " + str(msg))
    print("Setup planetoid PCG: " + str(msg))


def _load_config():
    defaults = {
        "planetoid_level_path": "/Game/HomeWorld/Maps/Planetoid_Pride",
        "volume_center_x": 0, "volume_center_y": 0, "volume_center_z": 0,
        "volume_extent_x": 5000, "volume_extent_y": 5000, "volume_extent_z": 500,
        "use_landscape_bounds": True,
    }
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "planetoid_map_config.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k in ("planetoid_level_path", "volume_center_x", "volume_center_y", "volume_center_z",
                      "volume_extent_x", "volume_extent_y", "volume_extent_z"):
                if k in data and not str(k).startswith("_"):
                    if "path" in k:
                        defaults[k] = data[k]
                    else:
                        defaults[k] = float(data[k]) if k.startswith("volume_") else data[k]
            if "use_landscape_bounds" in data:
                defaults["use_landscape_bounds"] = bool(data["use_landscape_bounds"])
    except Exception as e:
        _log("Config: " + str(e))
    return defaults


def _find_or_spawn_pcg_volume(world, location, extent):
    """Return existing PCG Volume in level or spawn one; set label and scale. Does not assign graph."""
    volume = pcg_forest._find_existing_pcg_volume(world)
    if volume:
        _log("Reusing existing PCG Volume.")
        try:
            volume.set_actor_location(location, False, False)
        except Exception:
            pass
    else:
        rotation = unreal.Rotator(0, 0, 0)
        volume = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PCGVolume, location, rotation)
        if not volume:
            _log("Failed to spawn PCG Volume.")
            return None
        _log("Spawned PCG Volume.")
    try:
        if hasattr(volume, "set_actor_label"):
            volume.set_actor_label(PLANETOID_VOLUME_LABEL)
    except Exception:
        pass
    try:
        volume.set_actor_scale3d(unreal.Vector(1, 1, 1))
        _, base_ext = volume.get_actor_bounds(False)
        if base_ext.x > 0 and base_ext.y > 0 and base_ext.z > 0:
            sx = abs(extent.x) / base_ext.x
            sy = abs(extent.y) / base_ext.y
            sz = abs(extent.z) / base_ext.z
            volume.set_actor_scale3d(unreal.Vector(sx, sy, sz))
            _log("Scaled PCG Volume to extent (%.0f, %.0f, %.0f) cm." % (extent.x, extent.y, extent.z))
    except Exception as e:
        _log("Could not scale volume: %s" % e)
    return volume


def main():
    _log("Start: planetoid level + PCG POI setup.")
    config = _load_config()
    planetoid_path = config.get("planetoid_level_path", "/Game/HomeWorld/Maps/Planetoid_Pride")

    if not ensure_planetoid_level.ensure_planetoid_level_exists():
        _log("Stopping. Create planetoid level (see ensure_planetoid_level.py output) and run again.")
        return

    poi_placeholders.main()
    planetoid_pcg.main()

    _log("Opening planetoid level...")
    if level_loader.is_level_loaded(planetoid_path):
        _log("Level already open: " + (level_loader.get_current_level_path() or planetoid_path))
    elif not level_loader.open_level(planetoid_path):
        _log("Could not open level. Open " + planetoid_path + " in the Editor, then run this script again.")
        return

    pcg_forest.ensure_landscape_has_pcg_tag()

    use_landscape_bounds = config.get("use_landscape_bounds", True)
    location = unreal.Vector(
        float(config.get("volume_center_x", 0)),
        float(config.get("volume_center_y", 0)),
        float(config.get("volume_center_z", 0)),
    )
    extent = unreal.Vector(
        float(config.get("volume_extent_x", 5000)),
        float(config.get("volume_extent_y", 5000)),
        float(config.get("volume_extent_z", 500)),
    )
    if use_landscape_bounds:
        landscape_bounds = level_loader.get_landscape_bounds()
        if landscape_bounds is not None:
            location, extent = landscape_bounds
            _log("PCG volume fitted to landscape bounds.")
        else:
            wp_bounds = level_loader.get_world_partition_bounds()
            if wp_bounds is not None:
                location, extent = wp_bounds
                _log("PCG volume fitted to World Partition bounds.")
            else:
                _log("Using config volume bounds (landscape/WP not available).")
    else:
        _log("Using config volume bounds.")

    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        _log("No editor world.")
        return
    volume = _find_or_spawn_pcg_volume(world, location, extent)
    if not volume:
        return

    unreal.EditorLevelLibrary.save_current_level()

    graph_asset = unreal.load_asset(PCG_GRAPH_PATH)
    if not graph_asset:
        _log("Could not load Planetoid_POI_PCG. Run create_planetoid_poi_pcg.py first.")
        return
    _log("Attempting to assign graph, set Get Landscape Data, and trigger Generate...")
    pcg_forest.try_assign_graph_to_volume(graph_asset)
    pcg_forest.try_set_get_landscape_selector(graph_asset)
    pcg_forest.trigger_pcg_generate()
    try:
        unreal.EditorLevelLibrary.save_current_level()
        _log("Level saved after Generate.")
    except Exception as e:
        _log("Save after Generate failed: %s" % e)

    _log("Done. If Generate produced no instances, set Get Landscape Data to By Tag PCG_Landscape and Actor Spawner template in Planetoid_POI_PCG (see docs/PCG_SETUP.md).")


if __name__ == "__main__":
    main()

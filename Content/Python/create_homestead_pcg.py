# create_homestead_pcg.py
# Run from Unreal Editor with the **Homestead** map open (Tools -> Execute Python Script or via MCP).
# Loads homestead_map_config.json: places/sizes one PCG Volume to cover the level (or config bounds),
# tags the Landscape with PCG_Landscape, and optionally assigns ForestIsland_PCG and triggers Generate.
# Exclusion zones in config define the compound (no trees inside); the graph ForestIsland_PCG was built
# for Main. For Homestead-only exclusion, duplicate ForestIsland_PCG to Homestead_PCG and set the
# Difference node's exclusion box to match homestead_map_config.json exclusion_zones. See docs/HOMESTEAD_MAP.md and docs/PCG_SETUP.md.

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
import create_pcg_forest as pcg_forest
import importlib
importlib.reload(pcg_forest)


def _log(msg):
    unreal.log("Homestead PCG: " + str(msg))
    print("Homestead PCG: " + str(msg))


def _load_config():
    """Load Content/Python/homestead_map_config.json."""
    defaults = {
        "homestead_level_path": "/Game/HomeWorld/Maps/Homestead",
        "volume_center_x": 0.0, "volume_center_y": 0.0, "volume_center_z": 0.0,
        "volume_extent_x": 5000.0, "volume_extent_y": 5000.0, "volume_extent_z": 500.0,
        "volume_extent_z_padding": 10000.0,
        "exclusion_zones": [],
        "skip_exclusion_zones": False,
    }
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "homestead_map_config.json")
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k in defaults:
            if k in data and not str(k).startswith("_"):
                val = data[k]
                if k == "exclusion_zones" and isinstance(val, list):
                    zones = []
                    for z in val:
                        if isinstance(z, dict) and all(
                            key in z for key in ("center_x", "center_y", "center_z", "extent_x", "extent_y", "extent_z")
                        ):
                            zones.append({key: float(z[key]) for key in ("center_x", "center_y", "center_z", "extent_x", "extent_y", "extent_z")})
                    defaults[k] = zones
                else:
                    defaults[k] = val
        return defaults
    except Exception as e:
        _log("Config load warning: " + str(e))
        return defaults


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


def _get_landscape_bounds():
    """Return (location Vector, extent Vector) from the first Landscape in the level, or None."""
    try:
        world = unreal.EditorLevelLibrary.get_editor_world()
        if not world:
            return None
        landscapes = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Landscape)
        if not landscapes:
            return None
        land = landscapes[0]
        origin, box_extent = land.get_actor_bounds(False)
        return (origin, box_extent)
    except Exception as e:
        _log("Could not get landscape bounds: " + str(e))
        return None


def main():
    _log("Starting Homestead PCG setup (volume + landscape tag)...")
    config = _load_config()
    homestead_path = config.get("homestead_level_path", "/Game/HomeWorld/Maps/Homestead")

    current = _get_current_level_path()
    if not current or not current.lower().endswith("homestead"):
        _log("Current level is not Homestead. Open Homestead map and run this script again.")
        _log("Expected path contains 'Homestead'; got: " + str(current))
        return

    pcg_forest.ensure_landscape_has_pcg_tag()

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

    landscape_bounds = _get_landscape_bounds()
    if landscape_bounds is not None:
        location, extent = landscape_bounds
        z_pad = float(config.get("volume_extent_z_padding", 10000))
        if z_pad > 0:
            extent.z = extent.z + z_pad
            _log("PCG volume Z extent padded by %.0f cm." % z_pad)
        _log("PCG volume will cover landscape: center=%s half_extent=%s." % (location, extent))
    else:
        _log("No landscape found; using config volume bounds.")

    graph_asset = None
    if unreal.EditorAssetLibrary.does_asset_exist("/Game/HomeWorld/PCG/ForestIsland_PCG"):
        graph_asset = unreal.load_asset("/Game/HomeWorld/PCG/ForestIsland_PCG")
    if graph_asset:
        pcg_forest.place_pcg_volume(location=location, extent=extent, graph_asset=graph_asset)
    else:
        pcg_forest.place_pcg_volume(location=location, extent=extent, graph_asset=None)
        _log("ForestIsland_PCG not found; assign a PCG graph to the volume in Details.")

    _log("Done. If trees spawn inside the compound: duplicate ForestIsland_PCG to Homestead_PCG, set Difference node exclusion to match homestead_map_config.json exclusion_zones, assign Homestead_PCG to this volume. See docs/HOMESTEAD_MAP.md and docs/PCG_SETUP.md.")


if __name__ == "__main__":
    main()

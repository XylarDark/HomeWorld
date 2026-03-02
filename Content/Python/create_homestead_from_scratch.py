# create_homestead_from_scratch.py
# Ensures Homestead map and PCG are set up (create-if-missing, update-in-place). Run from Unreal Editor: Tools -> Execute Python Script or via MCP.
# 1) Ensures Homestead exists (duplicates from source_level_path only if missing).
# 2) Opens Homestead level.
# 3) Creates PCG volume and graph only if missing; reuses and updates bounds/config by default. Set recreate_volume_and_graph=true in config only when you explicitly want to destroy and recreate (escape hatch).
# 4) Attempts demo setup: set Get Landscape Data (By Tag + PCG_Landscape), mesh lists on spawners, assign graph, trigger Generate, save level. If any step fails (engine API limits), see Output Log and docs/PCG_SETUP.md "Demo setup".
# Volume bounds: Config (volume_center_*, volume_extent_*) is the source of truth; use_landscape_bounds then World Partition bounds fallback when available. Config: Content/Python/homestead_map_config.json. See docs/HOMESTEAD_MAP.md and docs/PCG_SETUP.md.

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
import ensure_homestead_map
import level_loader
import importlib
importlib.reload(pcg_forest)
importlib.reload(ensure_homestead_map)
importlib.reload(level_loader)


def _log(msg):
    unreal.log("Homestead from scratch: " + str(msg))


def _load_config():
    """Load Content/Python/homestead_map_config.json."""
    defaults = {
        "homestead_level_path": "/Game/HomeWorld/Maps/Homestead",
        "source_level_path": "/Game/HomeWorld/Maps/Main",
        "volume_center_x": 0.0, "volume_center_y": 0.0, "volume_center_z": 0.0,
        "volume_extent_x": 5000.0, "volume_extent_y": 5000.0, "volume_extent_z": 500.0,
        "volume_extent_z_padding": 1000.0,
        "exclusion_zones": [],
        "skip_exclusion_zones": False,
        "recreate_volume_and_graph": False,
        "use_landscape_bounds": True,
        "landscape_wait_attempts": 20,
        "landscape_wait_delay_sec": 2.0,
        "load_all_sleep_sec": 10.0,
        "landscape_wait_attempts_after_load_all": 10,
        "landscape_wait_phase1_attempts": 5,
        "landscape_wait_phase1_delay_sec": 0.5,
        "landscape_wait_phase2_attempts": 15,
        "landscape_wait_phase2_delay_sec": 2.0,
    }
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "homestead_map_config.json")
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k in defaults:
            if k not in data or str(k).startswith("_"):
                continue
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


def _ensure_homestead_exists(homestead_path, source_path):
    """If Homestead does not exist, duplicate source level. Return True if Homestead exists (or was created)."""
    if unreal.EditorAssetLibrary.does_asset_exist(homestead_path):
        _log("Homestead map already exists at " + homestead_path)
        return True
    _log("Homestead not found; duplicating from source.")
    if not unreal.EditorAssetLibrary.does_asset_exist(source_path):
        _log("Source level not found at " + source_path + ". Create Main first or set source_level_path in config.")
        return False
    try:
        result = unreal.EditorAssetLibrary.duplicate_asset(source_path, homestead_path)
        if result:
            _log("Duplicated source to " + homestead_path)
            return True
    except Exception as e:
        _log("Duplicate failed: " + str(e))
    return False


def main():
    _log("Starting: ensure Homestead and PCG (create-if-missing, update bounds and config).")
    config = _load_config()
    homestead_path = config.get("homestead_level_path", "/Game/HomeWorld/Maps/Homestead")
    source_path = config.get("source_level_path", "/Game/HomeWorld/Maps/Main")

    if not ensure_homestead_map.ensure_homestead_map_exists():
        _log("Stopping. Create Homestead (e.g. duplicate Main) and run again.")
        return

    _log("Opening Homestead level...")
    if level_loader.is_level_loaded(homestead_path):
        _log("Level already open: " + (level_loader.get_current_level_path() or homestead_path))
    elif not level_loader.open_level(homestead_path):
        _log("Could not open level. Open " + homestead_path + " in the Editor, then run this script again.")
        return

    pcg_forest.ensure_landscape_has_pcg_tag()
    recreate_volume_and_graph = config.get("recreate_volume_and_graph", False)
    if recreate_volume_and_graph:
        pcg_forest.destroy_pcg_volume()
    else:
        _log("Reusing existing volume and graph (recreate_volume_and_graph=false).")

    # Config is source of truth for volume bounds. Optional one-shot landscape override when available (no retries or Load All).
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
    use_landscape_bounds = config.get("use_landscape_bounds", True)
    if use_landscape_bounds:
        landscape_bounds = level_loader.get_landscape_bounds()
        if landscape_bounds is not None:
            location, extent = landscape_bounds
            z_pad = float(config.get("volume_extent_z_padding", 1000))
            if z_pad > 0:
                extent.z = extent.z + z_pad
            _log("PCG volume fitted to landscape: center=(%.0f, %.0f, %.0f) half_extent=(%.0f, %.0f, %.0f) cm." % (location.x, location.y, location.z, extent.x, extent.y, extent.z))
        else:
            wp_bounds = level_loader.get_world_partition_bounds()
            if wp_bounds is not None:
                location, extent = wp_bounds
                z_pad = float(config.get("volume_extent_z_padding", 1000))
                if z_pad > 0:
                    extent.z = extent.z + z_pad
                _log("PCG volume fitted to World Partition bounds (landscape not loaded): center=(%.0f, %.0f, %.0f) half_extent=(%.0f, %.0f, %.0f) cm." % (location.x, location.y, location.z, extent.x, extent.y, extent.z))
                _log("For a smaller playable area, set use_landscape_bounds=false and volume_center_* and volume_extent_* in homestead_map_config.json; see docs/PCG_QUICK_SETUP.md.")
            else:
                _log("Using config volume bounds (landscape and World Partition bounds not available).")
    else:
        _log("Using config volume bounds (use_landscape_bounds=false).")

    exclusion_zones = list(config.get("exclusion_zones", [])) if not config.get("skip_exclusion_zones", False) else []
    if exclusion_zones:
        _log("Using %d exclusion zone(s) from config." % len(exclusion_zones))

    graph_asset = pcg_forest.create_pcg_graph(exclusion_zones=exclusion_zones, force_recreate=recreate_volume_and_graph)
    if graph_asset:
        pcg_forest.place_pcg_volume(location=location, extent=extent, graph_asset=graph_asset)
    else:
        pcg_forest.place_pcg_volume(location=location, extent=extent, graph_asset=None)
        _log("No PCG graph created; assign ForestIsland_PCG to the volume in Details.")
    pcg_forest.try_world_partition()

    _log("Done. If Output Log shows any 'Could not set' or 'set in Editor', do those steps manually once (see docs/PCG_SETUP.md 'Demo setup'). Then save the level. For World Partition, enable Is Partitioned on the PCG component and set Partition Grid Size on the PCG World Actor if needed.")


if __name__ == "__main__":
    main()

# create_demo_map.py
# Run from Unreal Editor: Tools -> Execute Python Script.
# Generates the demo level: medieval village (from StylizedProvencal) + PCG forest.
# Ensures Main exists (duplicates from template if missing), opens Main, creates PCG graph,
# places volume with configurable position/size, generates, saves.
# Config: Content/Python/demo_map_config.json. Reuses create_pcg_forest for graph and volume.

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

# Import PCG forest logic so we don't duplicate it
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)
import create_pcg_forest as pcg_forest


def _log(msg):
    unreal.log("Demo Map: " + str(msg))
    print("Demo Map: " + str(msg))


# #region agent log
def _debug_log(hypothesis_id, location, message, data):
    import time
    try:
        proj = unreal.SystemLibrary.get_project_directory()
        path = os.path.join(proj, "debug-cb22d5.log")
        line = '{"sessionId":"cb22d5","hypothesisId":"%s","location":"%s","message":"%s","data":%s,"timestamp":%d}\n' % (
            hypothesis_id, location, message, data, int(time.time() * 1000))
        with open(path, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass
# #endregion


def _load_demo_config():
    """Load Content/Python/demo_map_config.json. Returns dict with paths, volume center/extent, and exclusion_zones."""
    defaults = {
        "demo_level_path": "/Game/HomeWorld/Maps/Main",
        "template_level_path": "/Game/StylizedProvencal/Maps/Main",
        "volume_center_x": 0.0, "volume_center_y": 0.0, "volume_center_z": 0.0,
        "volume_extent_x": 5000.0, "volume_extent_y": 5000.0, "volume_extent_z": 500.0,
        "exclusion_zones": [],
    }
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "demo_map_config.json")
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r") as f:
            data = json.load(f)
        for k in defaults:
            if k not in data or k.startswith("_"):
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
        _log("Demo config load warning: " + str(e))
        return defaults


def _ensure_demo_level_exists(demo_path, template_path):
    """If demo level does not exist, try to duplicate from template. Return True if demo exists (or was created)."""
    if unreal.EditorAssetLibrary.does_asset_exist(demo_path):
        return True
    _log("Demo level not found at " + demo_path + "; attempting to duplicate from template.")
    if not unreal.EditorAssetLibrary.does_asset_exist(template_path):
        _log("Template level not found at " + template_path + ". Cannot create demo level.")
        return False
    try:
        # duplicate_asset(source_path, destination_path) - destination is folder + name
        dest_path = demo_path  # e.g. /Game/HomeWorld/Maps/Main
        result = unreal.EditorAssetLibrary.duplicate_asset(template_path, dest_path)
        if result:
            _log("Duplicated template to " + dest_path)
            return True
    except Exception as e:
        _log("Level duplicate failed (levels may not be supported): " + str(e))
    _log("One-time step: copy StylizedProvencal/Maps/Main to HomeWorld/Maps/Main in the Content Browser (duplicate the level asset), then run this script again.")
    return False


def _get_landscape_bounds():
    """Return (location Vector, extent Vector) from the first Landscape in the level, or None if no landscape.
    extent is half-extent (same as config volume_extent_*)."""
    try:
        world = unreal.EditorLevelLibrary.get_editor_world()
        if not world:
            return None
        landscapes = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Landscape)
        if not landscapes:
            return None
        land = landscapes[0]
        origin = unreal.Vector()
        box_extent = unreal.Vector()
        land.get_actor_bounds(False, origin, box_extent, False)
        return (origin, box_extent)
    except Exception as e:
        _log("Could not get landscape bounds: " + str(e))
        return None


def _get_current_level_path():
    """Return the asset path of the current editor level (e.g. /Game/HomeWorld/Maps/Main), or None."""
    try:
        world = unreal.EditorLevelLibrary.get_editor_world()
        if not world:
            return None
        path = world.get_path_name() if hasattr(world, "get_path_name") else ""
        if not path:
            return None
        # Path is often "/Game/HomeWorld/Maps/Main.Main:PersistentLevel" -> take package part
        if "." in path:
            path = path.split(".")[0]
        if ":" in path:
            path = path.split(":")[0]
        return path if path.startswith("/") else None
    except Exception:
        return None


def _open_level(level_path):
    """Try to open the level in the editor. Return True if current level is now level_path."""
    try:
        # Try EditorLevelLibrary.load_level(world, level_asset_path) if available
        if hasattr(unreal.EditorLevelLibrary, "load_level"):
            world = unreal.EditorLevelLibrary.get_editor_world()
            if world:
                unreal.EditorLevelLibrary.load_level(world, level_path)
                return True
        # Try taking the level asset and loading it
        level_asset = unreal.load_asset(level_path)
        if level_asset and hasattr(unreal.EditorLevelLibrary, "load_level"):
            world = unreal.EditorLevelLibrary.get_editor_world()
            if world:
                unreal.EditorLevelLibrary.load_level(world, level_asset)
                return True
    except Exception as e:
        _log("Open level attempt: " + str(e))
    return False


def _ensure_main_is_open(demo_path):
    """Ensure the demo level is the current editor level. Return True if we have Main open."""
    current = _get_current_level_path()
    if current and (current == demo_path or current.endswith("Main")):
        return True
    if _open_level(demo_path):
        return True
    _log("Could not open level by path. Please open the Main level (Content/HomeWorld/Maps/Main) in the Editor, then run this script again.")
    return False


def main():
    _log("Starting demo map generation (village + PCG forest)...")
    config = _load_demo_config()
    demo_path = config.get("demo_level_path", "/Game/HomeWorld/Maps/Main")
    template_path = config.get("template_level_path", "/Game/StylizedProvencal/Maps/Main")
    # #region agent log
    _debug_log("H4", "create_demo_map.py:main", "config loaded", json.dumps({"demo_path": demo_path}))
    # #endregion

    if not _ensure_demo_level_exists(demo_path, template_path):
        # #region agent log
        _debug_log("H4", "create_demo_map.py:main", "demo level missing or duplicate failed", '{"ok":0}')
        # #endregion
        _log("Stopping. Create or copy the Main level first (see message above).")
        return
    # #region agent log
    _debug_log("H4", "create_demo_map.py:main", "demo level exists", '{"ok":1}')
    # #endregion

    if not _ensure_main_is_open(demo_path):
        # #region agent log
        _debug_log("H4", "create_demo_map.py:main", "could not open Main", '{"ok":0}')
        # #endregion
        _log("Stopping. Open Main level and run the script again.")
        return
    # #region agent log
    _debug_log("H4", "create_demo_map.py:main", "Main is open", '{"ok":1}')
    # #endregion

    # Build location and extent from config (Unreal units: cm); override with landscape bounds if present
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
        _log("Using PCG volume bounds from landscape: center=%s half_extent=%s" % (location, extent))

    exclusion_zones = config.get("exclusion_zones") or []
    if not exclusion_zones:
        # Default: one exclusion zone in the center, 10% of volume size
        ex_x = max(100.0, abs(extent.x) * 0.1)
        ex_y = max(100.0, abs(extent.y) * 0.1)
        ex_z = max(50.0, abs(extent.z) * 0.1)
        exclusion_zones = [{
            "center_x": location.x, "center_y": location.y, "center_z": location.z,
            "extent_x": ex_x, "extent_y": ex_y, "extent_z": ex_z,
        }]
        _log("Added default center exclusion zone (10%% of volume): extent %s %s %s" % (ex_x, ex_y, ex_z))
    graph_asset = pcg_forest.create_pcg_graph(exclusion_zones=exclusion_zones)
    # #region agent log
    _debug_log("H4", "create_demo_map.py:main", "PCG graph created", '{"hasGraph":%d}' % (1 if graph_asset else 0))
    # #endregion
    if graph_asset:
        pcg_forest.place_volume_and_generate(graph_asset, location=location, extent=extent, exclusion_zones=exclusion_zones)
        # #region agent log
        _debug_log("H4", "create_demo_map.py:main", "volume placed and generated", '{"ok":1}')
        # #endregion
    pcg_forest.try_world_partition()

    _log("Done. Demo map ready (medieval village + PCG forest). Trees/rocks from Stylized Provencal; edit pcg_forest_config.json to change.")


if __name__ == "__main__":
    main()

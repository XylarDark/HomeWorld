# create_demo_map.py
# Run from Unreal Editor: Tools -> Execute Python Script.
# Ensures Main exists (duplicates from template if missing), opens Main, creates PCG graph (if missing),
# tags the Landscape for PCG, places/sizes one PCG Volume, then tries to assign the graph, set Get Landscape Data tag, and trigger Generate.
# If the engine blocks these (common in UE 5.7), do the remaining steps in docs/PCG_SETUP.md (assign graph, set tag, mesh list, Generate).
# Config: Content/Python/demo_map_config.json. See docs/PCG_SETUP.md for the full checklist.

import json
import os
import sys
import time

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

# Import PCG forest logic so we don't duplicate it.
# Force reload to pick up disk changes in a long-lived Editor Python session.
import importlib
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)
import create_pcg_forest as pcg_forest
importlib.reload(pcg_forest)


def _log(msg):
    unreal.log("Demo Map: " + str(msg))
    print("Demo Map: " + str(msg))


# #region agent log
def _debug_log(hypothesis_id, message, data, run_id="run1"):
    try:
        log_path = os.path.join(unreal.SystemLibrary.get_project_directory(), "debug-e934ae.log")
        payload = {"sessionId": "e934ae", "runId": run_id, "hypothesisId": hypothesis_id, "location": "create_demo_map", "message": message, "data": data, "timestamp": int(time.time() * 1000)}
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
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
        "volume_extent_z_padding": 10000.0,
        "exclusion_zones": [],
        "skip_exclusion_zones": False,
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
        origin, box_extent = land.get_actor_bounds(False)
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


EXCLUSION_PADDING_CM = 500.0
NATURE_MESH_PREFIXES = ("SM_Tree", "SMF_Forest_Rock", "SM_Rock_Small", "SM_Grass", "SM_Bush", "SM_Flower")
SCATTER_MESH_PREFIXES = ("SM_Clouds", "SM_Water", "SM_River", "SM_Sky", "SM_Terrain", "SM_Ground", "SM_Ocean")



def _actor_is_building_or_village_structure(actor, comp, mesh, skip_prefixes):
    """True if actor should count toward village exclusion (building-tagged or StylizedProvencal structure)."""
    try:
        tags = actor.get_editor_property("tags") if hasattr(actor, "get_editor_property") else getattr(actor, "tags", None)
        if tags is not None:
            tag_strs = [str(t).lower() for t in tags]
            if "building" in tag_strs:
                return True
    except Exception:
        pass
    mesh_name = mesh.get_name()
    mesh_path = mesh.get_path_name() if hasattr(mesh, "get_path_name") else ""
    if "StylizedProvencal" not in mesh_path:
        return False
    if any(mesh_name.startswith(prefix) for prefix in skip_prefixes):
        return False
    return True


def _detect_village_exclusion_zones(padding=EXCLUSION_PADDING_CM):
    """Scan the level for building-tagged actors and StylizedProvencal structure actors (buildings, walls, props)
    and compute an exclusion zone around the dense village core so trees spawn around the village, not inside it.
    Returns list of exclusion zone dicts ready for PCG."""
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        return []

    skip_prefixes = NATURE_MESH_PREFIXES + SCATTER_MESH_PREFIXES
    positions_x = []
    positions_y = []
    positions_z = []
    try:
        all_actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.StaticMeshActor)
    except Exception:
        all_actors = []

    for actor in (all_actors or []):
        try:
            comp = actor.get_component_by_class(unreal.StaticMeshComponent)
            if not comp:
                continue
            mesh = comp.get_editor_property("static_mesh")
            if not mesh:
                continue
            if not _actor_is_building_or_village_structure(actor, comp, mesh, skip_prefixes):
                continue
            origin, box_ext = actor.get_actor_bounds(False)
            positions_x.append(origin.x)
            positions_y.append(origin.y)
            positions_z.append(origin.z)
        except Exception:
            continue

    if not positions_x:
        _log("No building or village structure actors detected.")
        return []

    points = list(zip(positions_x, positions_y, positions_z))
    n = len(points)

    def bbox_to_zone(lo_x, hi_x, lo_y, hi_y, lo_z, hi_z, pad):
        cx = (lo_x + hi_x) / 2.0
        cy = (lo_y + hi_y) / 2.0
        cz = (lo_z + hi_z) / 2.0
        ex = (hi_x - lo_x) / 2.0 + pad
        ey = (hi_y - lo_y) / 2.0 + pad
        ez = (hi_z - lo_z) / 2.0 + pad
        return {"center_x": cx, "center_y": cy, "center_z": cz,
                "extent_x": ex, "extent_y": ey, "extent_z": ez}

    if n < 2:
        zone = bbox_to_zone(min(positions_x), max(positions_x), min(positions_y), max(positions_y), min(positions_z), max(positions_z), padding)
        _log("Single exclusion zone: center=(%.0f, %.0f, %.0f) half_extent=(%.0f, %.0f, %.0f)" % (zone["center_x"], zone["center_y"], zone["center_z"], zone["extent_x"], zone["extent_y"], zone["extent_z"]))
        return [zone]

    # Two zones: village (center) and castle (top-left). K=2 cluster by XY position.
    min_x, max_x = min(positions_x), max(positions_x)
    min_y, max_y = min(positions_y), max(positions_y)
    mean_z = sum(positions_z) / n
    c0 = (min_x + (max_x - min_x) * 0.25, max_y - (max_y - min_y) * 0.25, mean_z)
    c1 = (min_x + (max_x - min_x) * 0.5,  min_y + (max_y - min_y) * 0.5,  mean_z)
    group0, group1 = [], []
    for _ in range(10):
        group0, group1 = [], []
        for (x, y, z) in points:
            d0 = (x - c0[0]) ** 2 + (y - c0[1]) ** 2
            d1 = (x - c1[0]) ** 2 + (y - c1[1]) ** 2
            if d0 <= d1:
                group0.append((x, y, z))
            else:
                group1.append((x, y, z))
        if not group0 or not group1:
            break
        def mean_pt(grp):
            return (sum(p[0] for p in grp) / len(grp), sum(p[1] for p in grp) / len(grp), sum(p[2] for p in grp) / len(grp))
        c0 = mean_pt(group0)
        c1 = mean_pt(group1)

    zones = []
    for idx, grp in enumerate([group0, group1]):
        if not grp:
            continue
        xs, ys, zs = [p[0] for p in grp], [p[1] for p in grp], [p[2] for p in grp]
        zone = bbox_to_zone(min(xs), max(xs), min(ys), max(ys), min(zs), max(zs), padding)
        zones.append(zone)
        label = "castle" if idx == 0 else "village"
        _log("Exclusion zone %d (%s): center=(%.0f, %.0f, %.0f) half_extent=(%.0f, %.0f, %.0f) [+%.0fcm]"
             % (idx + 1, label, zone["center_x"], zone["center_y"], zone["center_z"], zone["extent_x"], zone["extent_y"], zone["extent_z"], padding))
    _log("Found %d building/village actor(s) -> %d exclusion zone(s) (village + castle)." % (n, len(zones)))
    return zones


def main():
    _log("Starting demo map generation (village + PCG forest)...")
    config = _load_demo_config()
    demo_path = config.get("demo_level_path", "/Game/HomeWorld/Maps/Main")
    template_path = config.get("template_level_path", "/Game/StylizedProvencal/Maps/Main")
    if not _ensure_demo_level_exists(demo_path, template_path):
        _log("Stopping. Create or copy the Main level first (see message above).")
        return

    if not _ensure_main_is_open(demo_path):
        _log("Stopping. Open Main level and run the script again.")
        return

    # PCG: create graph (if missing), tag Landscape, place/size one PCG Volume. Script does NOT assign the graph or call Generate.
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
        extent_z_before = float(extent.z)
        z_pad = float(config.get("volume_extent_z_padding", 10000))
        # #region agent log
        _debug_log("H1", "Z padding: before padding", {"extent_z_before": extent_z_before, "z_pad": z_pad, "landscape_used": True})
        # #endregion
        if z_pad > 0:
            extent.z = extent.z + z_pad
            _log("PCG volume Z extent padded by %.0f cm so trees do not poke out the bottom." % z_pad)
        # #region agent log
        _debug_log("H2", "Z padding: after padding", {"extent_z_after": float(extent.z), "extent_x": float(extent.x), "extent_y": float(extent.y)})
        # #endregion
        _log("PCG volume will cover the entire landscape: center=%s half_extent=%s." % (location, extent))
    else:
        _log("No landscape found — using config volume bounds. Add a Landscape or set volume_extent_* in demo_map_config.json for full coverage.")

    skip_exclusion = config.get("skip_exclusion_zones", False)
    exclusion_zones = list(config.get("exclusion_zones", [])) if not skip_exclusion else []
    if not skip_exclusion and not exclusion_zones:
        exclusion_zones = _detect_village_exclusion_zones()
    if exclusion_zones:
        _log("Using %d exclusion zone(s) so trees spawn around the village (not inside)." % len(exclusion_zones))
    pcg_forest.ensure_landscape_has_pcg_tag()
    graph_asset = pcg_forest.create_pcg_graph(exclusion_zones=exclusion_zones)
    pcg_forest.place_pcg_volume(location=location, extent=extent, graph_asset=graph_asset)
    pcg_forest.try_world_partition()

    _log("Done. Demo map ready. If PCG did not generate: set Get Landscape Data to By Tag + PCG_Landscape and Component By Class = Landscape Component, assign ForestIsland_PCG to PCG_Forest volume, set mesh list on spawners (step 2b), then click Generate in Details. See docs/PCG_SETUP.md.")


if __name__ == "__main__":
    main()

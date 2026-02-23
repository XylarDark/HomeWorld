# create_pcg_forest.py
# Run from Unreal Editor: Tools -> Execute Python Script, or run with -ExecutePythonScript=
# Creates a PCG graph: Surface Sampler (0.05) -> Density Filter (0.3-1.0) -> Transform Points (0.8-1.2)
# -> Static Mesh Spawner (trees). Optional second branch for rocks (0.01) when config has
# static_mesh_spawner_meshes_rocks. Config: Content/Python/pcg_forest_config.json.
# Optional: add a Height Filter in the Editor for terrain-only spawn (see docs/PCG_FOREST_SETUP.md).

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

# Default map and asset paths (Unreal units: cm; 100m = 10000 cm, half-extent = 5000)
PCG_GRAPH_PACKAGE = "/Game/HomeWorld/PCG/ForestIsland_PCG"
PCG_GRAPH_NAME = "ForestIsland_PCG"
DEFAULT_MAP_PATH = "/Game/HomeWorld/Maps/Main"
VOLUME_HALF_EXTENT_X = 5000.0   # 50 m half => 100 m box
VOLUME_HALF_EXTENT_Y = 5000.0
VOLUME_HALF_EXTENT_Z = 500.0    # 10 m vertical
PLACEHOLDER_MESH = "/Engine/BasicShapes/Cube"


def _log(msg):
    unreal.log("PCG Forest: " + str(msg))
    print("PCG Forest: " + str(msg))


def _load_config():
    """Load config from Content/Python/pcg_forest_config.json. Returns dict with trees, rocks, and optional height_filter_min/max."""
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "pcg_forest_config.json")
        if not os.path.exists(config_path):
            return {"trees": [], "rocks": [], "height_filter_min": None, "height_filter_max": None}
        with open(config_path, "r") as f:
            data = json.load(f)
        trees = [p for p in (data.get("static_mesh_spawner_meshes") or []) if p]
        rocks = [p for p in (data.get("static_mesh_spawner_meshes_rocks") or []) if p]
        h_min = data.get("height_filter_min")
        h_max = data.get("height_filter_max")
        if h_min is not None and h_max is not None:
            try:
                h_min, h_max = float(h_min), float(h_max)
            except (TypeError, ValueError):
                h_min, h_max = None, None
        return {"trees": trees, "rocks": rocks, "height_filter_min": h_min, "height_filter_max": h_max}
    except Exception as e:
        _log("Config load warning: " + str(e))
        return {"trees": [], "rocks": [], "height_filter_min": None, "height_filter_max": None}


def _load_config_mesh_paths():
    """Load tree mesh paths from config. Returns list of asset path strings."""
    return _load_config()["trees"]


def _get_mesh_paths():
    """Return list of static mesh asset paths for the spawner. Uses config or placeholder."""
    paths = _load_config_mesh_paths()
    if paths:
        return paths
    return [PLACEHOLDER_MESH]


def _ensure_pcg_folder():
    """Ensure /Game/HomeWorld/PCG folder exists (create if needed)."""
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    # Creating an asset in that path will create the folder; no separate folder API needed
    pass


def _connect_exclusion_points_to_difference(graph_asset, difference_node, exclusion_zones):
    """Build exclusion point source and connect to Difference node's second input (Differences pin).
    Tries Option A: create-points-in-box nodes per zone + merge. If API does not support it, leaves pin unconnected and logs."""
    if not exclusion_zones or not difference_node:
        return
    merge_node = None
    try:
        merge_class = getattr(unreal, "PCGMergeSettings", None)
        if merge_class:
            merge_node, _ = graph_asset.add_node_of_type(merge_class)
    except (AttributeError, Exception):
        merge_node = None
    created_point_nodes = []
    for zone in exclusion_zones:
        try:
            cx = zone.get("center_x", 0)
            cy = zone.get("center_y", 0)
            cz = zone.get("center_z", 0)
            ex = zone.get("extent_x", 1000)
            ey = zone.get("extent_y", 1000)
            ez = zone.get("extent_z", 500)
            # Try PCGCreatePointsGridSettings or PCGCreatePointsSettings with bounds
            create_class = getattr(unreal, "PCGCreatePointsGridSettings", None) or getattr(unreal, "PCGCreatePointsSettings", None)
            if not create_class:
                break
            point_node, point_settings = graph_asset.add_node_of_type(create_class)
            if not point_node:
                break
            # Try to set bounds (grid origin and size, or extent)
            if hasattr(point_settings, "set_editor_property"):
                origin = unreal.Vector(float(cx), float(cy), float(cz))
                try:
                    point_settings.set_editor_property("origin", origin)
                    point_settings.set_editor_property("grid_step", unreal.Vector(100.0, 100.0, 100.0))
                    point_settings.set_editor_property("grid_size", unreal.Vector(float(ex * 2), float(ey * 2), float(ez * 2)))
                except Exception:
                    try:
                        point_settings.set_editor_property("extent", unreal.Vector(float(ex), float(ey), float(ez)))
                        point_settings.set_editor_property("center", origin)
                    except Exception:
                        pass
            created_point_nodes.append(point_node)
        except Exception:
            continue
    if merge_node and created_point_nodes:
        for node in created_point_nodes:
            try:
                graph_asset.add_edge(node, "Out", merge_node, "In")
            except Exception:
                pass
        try:
            graph_asset.add_edge(merge_node, "Out", difference_node, "Difference")
        except Exception:
            try:
                graph_asset.add_edge(merge_node, "Out", difference_node, "Differences")
            except Exception:
                _log("Exclusion: could not connect merge to Difference (pin may be named differently). Connect exclusion point source to Difference node in Editor.")
    elif created_point_nodes and len(created_point_nodes) == 1:
        try:
            graph_asset.add_edge(created_point_nodes[0], "Out", difference_node, "Difference")
        except Exception:
            try:
                graph_asset.add_edge(created_point_nodes[0], "Out", difference_node, "Differences")
            except Exception:
                _log("Exclusion: connect the exclusion point node to Difference (Difference/Differences pin) in Editor.")
    else:
        _log("Exclusion zones defined but exclusion point source could not be created in graph. Spawn exclusion volume actors in level and connect a Surface Sampler (bounds = exclusion volume) to the Difference node's Difference pin in Editor. See docs/PCG_TUTORIAL_REPLACE_MAIN_TREES.md.")


def create_pcg_graph(exclusion_zones=None):
    """Create PCG graph asset with Surface Sampler -> Density Filter (0.3-1.0) -> [Difference when exclusion_zones] -> Transform Points -> Static Mesh Spawner.
    exclusion_zones: optional list of dicts with center_x/y/z, extent_x/y/z (cm). When non-empty, adds a Difference node to remove points inside those boxes."""
    _ensure_pcg_folder()
    if exclusion_zones is None:
        exclusion_zones = []
    # Re-run: delete existing graph so create_asset succeeds (script is re-runnable)
    try:
        if unreal.EditorAssetLibrary.does_asset_exist(PCG_GRAPH_PACKAGE):
            unreal.EditorAssetLibrary.delete_asset(PCG_GRAPH_PACKAGE)
            _log("Removed existing PCG graph for re-run.")
    except Exception as e:
        _log("Could not remove existing graph (re-run may fail): " + str(e))
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.PCGGraphFactory()
    graph_asset = asset_tools.create_asset(
        PCG_GRAPH_NAME,
        "/Game/HomeWorld/PCG",
        unreal.PCGGraph,
        factory
    )
    if not graph_asset:
        _log("Failed to create PCG graph asset.")
        return None

    # Add nodes: Surface Sampler, Density Filter, Transform Points, Static Mesh Spawner
    # add_node_of_type(settings_class) -> (node, default_node_settings)
    surface_node, surface_settings = graph_asset.add_node_of_type(unreal.PCGSurfaceSamplerSettings)
    density_node, density_settings = graph_asset.add_node_of_type(unreal.PCGDensityFilterSettings)
    transform_node, transform_settings = graph_asset.add_node_of_type(unreal.PCGTransformPointsSettings)
    spawner_node, spawner_settings = graph_asset.add_node_of_type(unreal.PCGStaticMeshSpawnerSettings)

    if not all([surface_node, density_node, transform_node, spawner_node]):
        _log("Failed to add one or more nodes.")
        return None

    # Surface sampler: 0.05 points/m^2 for trees not overlapping; bounds = PCG Volume
    surface_settings.set_editor_property("points_per_squared_meter", 0.05)
    surface_settings.set_editor_property("apply_density_to_points", True)
    # Density filter range 0.3-1.0 (keep points with density in range)
    density_settings.set_editor_property("lower_bound", 0.3)
    density_settings.set_editor_property("upper_bound", 1.0)

    config = _load_config()
    height_filter_node = None
    h_min, h_max = config.get("height_filter_min"), config.get("height_filter_max")
    if h_min is not None and h_max is not None:
        try:
            height_filter_node, height_filter_settings = graph_asset.add_node_of_type(unreal.PCGAttributeFilteringRangeSettings)
            if height_filter_node and height_filter_settings:
                if hasattr(height_filter_settings, "set_editor_property"):
                    try:
                        height_filter_settings.set_editor_property("min_threshold", h_min)
                        height_filter_settings.set_editor_property("max_threshold", h_max)
                    except Exception:
                        pass
                _log("Added optional height filter (Z range {}–{}). Set target attribute to Position.Z in Editor if needed.".format(h_min, h_max))
        except (AttributeError, Exception) as e:
            _log("Height filter skipped (API or config): " + str(e))
            height_filter_node = None

    # Static mesh spawner: set mesh list via weighted selector if available
    mesh_paths = _get_mesh_paths()
    try:
        spawner_settings.set_mesh_selector_type(unreal.PCGMeshSelectorWeighted)
        selector = spawner_settings.get_editor_property("mesh_selector_parameters")
        if selector and mesh_paths:
            entries = []
            for path in mesh_paths:
                mesh_asset = unreal.load_asset(path)
                if mesh_asset:
                    entry = unreal.PCGStaticMeshSpawnerEntry(weight=100, mesh=mesh_asset)
                    entries.append(entry)
            if entries and hasattr(selector, "set_editor_property"):
                selector.set_editor_property("mesh_entries", entries)
    except Exception as e:
        _log("Mesh selector setup warning (using defaults): " + str(e))

    # Transform Points: random rotation (Yaw 0-360) and uniform scale (0.8-1.2)
    transform_settings.set_editor_property("rotation_min", unreal.Rotator(0.0, 0.0, 0.0))
    transform_settings.set_editor_property("rotation_max", unreal.Rotator(0.0, 359.0, 0.0))
    transform_settings.set_editor_property("absolute_rotation", True)
    transform_settings.set_editor_property("scale_min", unreal.Vector(0.8, 0.8, 0.8))
    transform_settings.set_editor_property("scale_max", unreal.Vector(1.2, 1.2, 1.2))
    transform_settings.set_editor_property("uniform_scale", True)
    transform_settings.set_editor_property("absolute_scale", True)
    transform_settings.set_editor_property("seed", 12345)

    # Optional: Difference node to remove points inside exclusion zones (dead zones)
    difference_node = None
    if exclusion_zones:
        try:
            difference_node, _ = graph_asset.add_node_of_type(unreal.PCGDifferenceSettings)
            if difference_node:
                _log("Added Difference node for {} exclusion zone(s).".format(len(exclusion_zones)))
        except (AttributeError, Exception) as e:
            _log("Difference node skipped: " + str(e))
            difference_node = None

    # Connect: Input -> Surface Sampler -> [optional Height Filter] -> Density Filter -> [Difference] -> Transform Points -> Static Mesh Spawner -> Output
    input_node = graph_asset.get_input_node()
    output_node = graph_asset.get_output_node()
    graph_asset.add_edge(input_node, "Out", surface_node, "In")
    if height_filter_node:
        graph_asset.add_edge(surface_node, "Out", height_filter_node, "In")
        graph_asset.add_edge(height_filter_node, "Out", density_node, "In")
    else:
        graph_asset.add_edge(surface_node, "Out", density_node, "In")
    if difference_node:
        graph_asset.add_edge(density_node, "Out", difference_node, "In")
        _connect_exclusion_points_to_difference(graph_asset, difference_node, exclusion_zones)
        graph_asset.add_edge(difference_node, "Out", transform_node, "In")
    else:
        graph_asset.add_edge(density_node, "Out", transform_node, "In")
    graph_asset.add_edge(transform_node, "Out", spawner_node, "In")
    graph_asset.add_edge(spawner_node, "Out", output_node, "In")

    # Optional: second branch for rocks (density 0.01) when static_mesh_spawner_meshes_rocks is set
    rock_paths = config["rocks"]
    if rock_paths:
        surface_rock, surface_rock_settings = graph_asset.add_node_of_type(unreal.PCGSurfaceSamplerSettings)
        density_rock, density_rock_settings = graph_asset.add_node_of_type(unreal.PCGDensityFilterSettings)
        transform_rock, transform_rock_settings = graph_asset.add_node_of_type(unreal.PCGTransformPointsSettings)
        spawner_rock, spawner_rock_settings = graph_asset.add_node_of_type(unreal.PCGStaticMeshSpawnerSettings)
        if all([surface_rock, density_rock, transform_rock, spawner_rock]):
            surface_rock_settings.set_editor_property("points_per_squared_meter", 0.01)
            surface_rock_settings.set_editor_property("apply_density_to_points", True)
            density_rock_settings.set_editor_property("lower_bound", 0.3)
            density_rock_settings.set_editor_property("upper_bound", 1.0)
            transform_rock_settings.set_editor_property("rotation_min", unreal.Rotator(0.0, 0.0, 0.0))
            transform_rock_settings.set_editor_property("rotation_max", unreal.Rotator(0.0, 359.0, 0.0))
            transform_rock_settings.set_editor_property("absolute_rotation", True)
            transform_rock_settings.set_editor_property("scale_min", unreal.Vector(0.8, 0.8, 0.8))
            transform_rock_settings.set_editor_property("scale_max", unreal.Vector(1.2, 1.2, 1.2))
            transform_rock_settings.set_editor_property("uniform_scale", True)
            transform_rock_settings.set_editor_property("absolute_scale", True)
            transform_rock_settings.set_editor_property("seed", 54321)
            try:
                spawner_rock_settings.set_mesh_selector_type(unreal.PCGMeshSelectorWeighted)
                selector_rock = spawner_rock_settings.get_editor_property("mesh_selector_parameters")
                if selector_rock and rock_paths:
                    entries = []
                    for path in rock_paths:
                        mesh_asset = unreal.load_asset(path)
                        if mesh_asset:
                            entries.append(unreal.PCGStaticMeshSpawnerEntry(weight=100, mesh=mesh_asset))
                    if entries and hasattr(selector_rock, "set_editor_property"):
                        selector_rock.set_editor_property("mesh_entries", entries)
            except Exception as e:
                _log("Rocks mesh selector warning: " + str(e))
            graph_asset.add_edge(input_node, "Out", surface_rock, "In")
            graph_asset.add_edge(surface_rock, "Out", density_rock, "In")
            graph_asset.add_edge(density_rock, "Out", transform_rock, "In")
            graph_asset.add_edge(transform_rock, "Out", spawner_rock, "In")
            graph_asset.add_edge(spawner_rock, "Out", output_node, "In")
            _log("Added optional rocks branch (density 0.01).")

    # Save graph asset
    try:
        path = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(graph_asset)
        if path:
            unreal.EditorAssetSubsystem().save_asset(path)
        else:
            unreal.EditorAssetLibrary.save_loaded_asset(graph_asset)
    except Exception:
        unreal.EditorAssetLibrary.save_loaded_asset(graph_asset)
    _log("Created and saved PCG graph: " + PCG_GRAPH_PACKAGE)
    return graph_asset


def _spawn_exclusion_volumes(exclusion_zones):
    """Spawn one PCGVolume (or box) actor per exclusion zone for Option B. Tag with PCG_Exclusion."""
    if not exclusion_zones:
        return
    editor_subsystem = unreal.EditorLevelLibrary
    world = editor_subsystem.get_editor_world()
    if not world:
        return
    rotation = unreal.Rotator(0.0, 0.0, 0.0)
    for i, zone in enumerate(exclusion_zones):
        try:
            loc = unreal.Vector(
                float(zone.get("center_x", 0)),
                float(zone.get("center_y", 0)),
                float(zone.get("center_z", 0)),
            )
            ext = unreal.Vector(
                float(zone.get("extent_x", 1000)),
                float(zone.get("extent_y", 1000)),
                float(zone.get("extent_z", 500)),
            )
            vol = editor_subsystem.spawn_actor_from_class(unreal.PCGVolume, loc, rotation)
            if vol:
                box_comp = vol.get_component_by_class(unreal.BoxComponent)
                if box_comp and hasattr(box_comp, "set_box_extent"):
                    box_comp.set_box_extent(ext)
                elif vol.get_root_component() and hasattr(vol.get_root_component(), "set_box_extent"):
                    vol.get_root_component().set_box_extent(ext)
                try:
                    if hasattr(vol, "tags") and isinstance(vol.tags, list):
                        vol.tags.append("PCG_Exclusion")
                    elif hasattr(vol, "add_tag"):
                        vol.add_tag("PCG_Exclusion")
                except Exception:
                    pass
                _log("Placed exclusion volume {} at ({}, {}, {}).".format(i + 1, loc.x, loc.y, loc.z))
        except Exception as e:
            _log("Exclusion volume {} spawn failed: {}.".format(i + 1, e))


def place_volume_and_generate(graph_asset, location=None, extent=None, exclusion_zones=None):
    """Place a PCG Volume in the current level, assign graph, generate, save level.
    location: unreal.Vector for volume center (default 0,0,0).
    extent: unreal.Vector for half-extents in cm (default 5000,5000,500 => 100x100x10 m).
    exclusion_zones: optional list of dicts (center_*, extent_*); spawns exclusion volume actors when provided (Option B)."""
    if not graph_asset:
        _log("No graph asset; skipping volume placement.")
        return
    editor_subsystem = unreal.EditorLevelLibrary
    world = editor_subsystem.get_editor_world()
    if not world:
        _log("No editor world. Open a level (e.g. Main) first.")
        return

    if location is None:
        location = unreal.Vector(0.0, 0.0, 0.0)
    if extent is None:
        extent = unreal.Vector(VOLUME_HALF_EXTENT_X, VOLUME_HALF_EXTENT_Y, VOLUME_HALF_EXTENT_Z)
    if exclusion_zones is None:
        exclusion_zones = []

    rotation = unreal.Rotator(0.0, 0.0, 0.0)
    volume = editor_subsystem.spawn_actor_from_class(unreal.PCGVolume, location, rotation)
    if not volume:
        _log("Failed to spawn PCG Volume.")
        return

    # Set bounds: PCGVolume may use BoxComponent or Brush; set half-extents (cm)
    root = volume.get_root_component()
    if root and hasattr(root, "set_box_extent"):
        root.set_box_extent(extent)
    else:
        box_comp = volume.get_component_by_class(unreal.BoxComponent)
        if box_comp and hasattr(box_comp, "set_box_extent"):
            box_comp.set_box_extent(extent)
        else:
            _log("Volume has no BoxComponent; set bounds manually in Details (10000 x 10000 cm).")

    # Spawn exclusion volume actors (Option B) so they exist in the level for graph reference or manual wiring
    _spawn_exclusion_volumes(exclusion_zones)

    # Assign graph to PCG component and generate
    pcg_comp = volume.get_component_by_class(unreal.PCGComponent)
    if pcg_comp:
        pcg_comp.set_editor_property("graph", graph_asset)
        # Trigger generate
        if hasattr(pcg_comp, "generate"):
            pcg_comp.generate()
        else:
            _log("PCGComponent has no generate(); try Generate from Details in Editor.")
    else:
        _log("No PCGComponent on volume; assign graph manually in Details.")

    editor_subsystem.save_current_level()
    _log("Placed PCG Volume and saved level. Forest island should appear.")


def try_world_partition():
    """If Python API allows, enable World Partition on current level. Otherwise no-op (document manual step)."""
    try:
        # Optional: some engines expose conversion; leave as no-op and document
        pass
    except Exception as e:
        _log("World Partition: " + str(e))


def main():
    _log("Starting PCG forest setup...")
    graph_asset = create_pcg_graph()
    if graph_asset:
        place_volume_and_generate(graph_asset)
    try_world_partition()
    _log("Done. If World Partition is needed: World Settings -> Enable World Partition (Use External Actors).")


if __name__ == "__main__":
    main()

# create_pcg_forest.py
# Run from Unreal Editor: Tools -> Execute Python Script, or run with -ExecutePythonScript=
# Creates a PCG graph (Surface Sampler -> Density Filter -> Static Mesh Spawner),
# saves it, places a 100x100m PCG Volume in the current level, assigns the graph,
# and generates. Optionally reads mesh paths from Content/Python/pcg_forest_config.json.

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


def _load_config_mesh_paths():
    """Load mesh paths from Content/Python/pcg_forest_config.json. Returns list of asset path strings."""
    try:
        # Resolve path: project Content dir -> Python -> config
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "pcg_forest_config.json")
        if not os.path.exists(config_path):
            return []
        with open(config_path, "r") as f:
            data = json.load(f)
        paths = data.get("static_mesh_spawner_meshes") or []
        return [p for p in paths if p]
    except Exception as e:
        _log("Config load warning: " + str(e))
        return []


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


def create_pcg_graph():
    """Create PCG graph asset with Surface Sampler -> Density Filter -> Static Mesh Spawner. Returns graph asset or None."""
    _ensure_pcg_folder()
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

    # Add nodes: Surface Sampler, Density Filter, Static Mesh Spawner
    # add_node_of_type(settings_class) -> (node, default_node_settings)
    surface_node, surface_settings = graph_asset.add_node_of_type(unreal.PCGSurfaceSamplerSettings)
    density_node, density_settings = graph_asset.add_node_of_type(unreal.PCGDensityFilterSettings)
    spawner_node, spawner_settings = graph_asset.add_node_of_type(unreal.PCGStaticMeshSpawnerSettings)

    if not all([surface_node, density_node, spawner_node]):
        _log("Failed to add one or more nodes.")
        return None

    # Optional: tune surface sampler (points per m^2, apply density for filter)
    surface_settings.set_editor_property("points_per_squared_meter", 0.1)
    surface_settings.set_editor_property("apply_density_to_points", True)
    # Optional: density filter range (keep points with density in range)
    density_settings.set_editor_property("lower_bound", 0.2)
    density_settings.set_editor_property("upper_bound", 1.0)

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

    # Connect: Input -> Surface Sampler -> Density Filter -> Static Mesh Spawner -> Output
    input_node = graph_asset.get_input_node()
    output_node = graph_asset.get_output_node()
    # Default pin names in PCG are typically "Out" and "In"
    graph_asset.add_edge(input_node, "Out", surface_node, "In")
    graph_asset.add_edge(surface_node, "Out", density_node, "In")
    graph_asset.add_edge(density_node, "Out", spawner_node, "In")
    graph_asset.add_edge(spawner_node, "Out", output_node, "In")

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


def place_volume_and_generate(graph_asset):
    """Place a PCG Volume (100x100m) in the current level, assign graph, generate, save level."""
    if not graph_asset:
        _log("No graph asset; skipping volume placement.")
        return
    editor_subsystem = unreal.EditorLevelLibrary
    world = editor_subsystem.get_editor_world()
    if not world:
        _log("No editor world. Open a level (e.g. Main) first.")
        return

    # Spawn PCG Volume at origin
    location = unreal.Vector(0.0, 0.0, 0.0)
    rotation = unreal.Rotator(0.0, 0.0, 0.0)
    volume = editor_subsystem.spawn_actor_from_class(unreal.PCGVolume, location, rotation)
    if not volume:
        _log("Failed to spawn PCG Volume.")
        return

    # Set bounds: PCGVolume may use BoxComponent or Brush; set half-extents (cm)
    extent = unreal.Vector(VOLUME_HALF_EXTENT_X, VOLUME_HALF_EXTENT_Y, VOLUME_HALF_EXTENT_Z)
    root = volume.get_root_component()
    if root and hasattr(root, "set_box_extent"):
        root.set_box_extent(extent)
    else:
        box_comp = volume.get_component_by_class(unreal.BoxComponent)
        if box_comp and hasattr(box_comp, "set_box_extent"):
            box_comp.set_box_extent(extent)
        else:
            _log("Volume has no BoxComponent; set bounds manually in Details (10000 x 10000 cm).")

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

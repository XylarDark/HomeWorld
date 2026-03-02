# create_pcg_forest.py
# Run from Unreal Editor: Tools -> Execute Python Script.
#
# Builds the canonical tutorial flow (Get Landscape Data -> Surface Sampler; Input -> Bounding;
# Surface Sampler -> Static Mesh Spawner -> Output) plus: Density Filter, Transform Points,
# optional Difference (exclusion zones), and optional rocks branch + Merge. Script tags the
# Landscape with PCG_Landscape and places/sizes one PCG Volume. It does NOT assign the graph
# to the volume or call Generate (engine limitation). You must: set Get Landscape Data to
# By Tag + PCG_Landscape, assign the graph to the volume in Details, and click Generate.
# Config: Content/Python/pcg_forest_config.json. See docs/PCG_SETUP.md and docs/PCG_BEST_PRACTICES.md.

import json
import os
import sys
import time

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

# Tag added to the level's Landscape so Get Landscape Data (Actor By Tag) can find it
PCG_LANDSCAPE_TAG = "PCG_Landscape"
PCG_GRAPH_PACKAGE = "/Game/HomeWorld/PCG/ForestIsland_PCG"
PCG_GRAPH_NAME = "ForestIsland_PCG"
VOLUME_HALF_EXTENT_X = 5000.0
VOLUME_HALF_EXTENT_Y = 5000.0
VOLUME_HALF_EXTENT_Z = 500.0
PLACEHOLDER_MESH = "/Engine/BasicShapes/Cube"
EXECUTION_DEPENDENCY = "Execution Dependency"


def _log(msg):
    unreal.log("PCG Forest: " + str(msg))


def _tag_actor_pcg_landscape(actor, add=True):
    """Add or remove PCG_LANDSCAPE_TAG on an actor. Returns True if changed."""
    try:
        tags = actor.get_editor_property("tags") if hasattr(actor, "get_editor_property") else getattr(actor, "tags", None)
        if tags is None:
            return False
        tag_strs = [str(t) for t in tags]
        has_tag = PCG_LANDSCAPE_TAG in tag_strs
        if add and has_tag:
            return False
        if not add and not has_tag:
            return False
        if add:
            if hasattr(actor, "add_tag"):
                actor.add_tag(PCG_LANDSCAPE_TAG)
            else:
                tags.append(unreal.Name(PCG_LANDSCAPE_TAG))
                if hasattr(actor, "set_editor_property"):
                    actor.set_editor_property("tags", tags)
        else:
            tags[:] = [t for t in tags if str(t) != PCG_LANDSCAPE_TAG]
            if hasattr(actor, "set_editor_property"):
                actor.set_editor_property("tags", tags)
        return True
    except Exception:
        return False


def ensure_landscape_has_pcg_tag():
    """Ensure the level's first Landscape actor has PCG_LANDSCAPE_TAG so Get Landscape Data (Actor By Tag) can find it. Idempotent.
    In World Partition, the root Landscape may have 0 components (they live in LandscapeStreamingProxy). If so, we tag the first
    proxy that has components and remove the tag from the root so Get Landscape Data finds an actor with surfaces."""
    try:
        world = unreal.EditorLevelLibrary.get_editor_world()
        if not world:
            return
        landscapes = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Landscape)
        if not landscapes:
            return
        land = landscapes[0]
        comp_class = getattr(unreal, "LandscapeComponent", None)
        root_comp_count = 0
        if comp_class and hasattr(land, "get_components_by_class"):
            root_comp_count = len(land.get_components_by_class(comp_class))

        if root_comp_count > 0:
            # Normal case: root has components, tag it
            if _tag_actor_pcg_landscape(land, add=True):
                _log("Tagged Landscape with '%s' for Get Landscape Data (By Tag)." % PCG_LANDSCAPE_TAG)
            return

        # World Partition: root has 0 components; tag all proxies that have components so Get Landscape Data finds full surface
        proxy_class = getattr(unreal, "LandscapeStreamingProxy", None)
        if not proxy_class:
            _tag_actor_pcg_landscape(land, add=True)
            return
        proxies = unreal.GameplayStatics.get_all_actors_of_class(world, proxy_class)
        if not proxies:
            _tag_actor_pcg_landscape(land, add=True)
            return
        tagged_count = 0
        _tag_actor_pcg_landscape(land, add=False)
        for proxy in proxies:
            if comp_class and hasattr(proxy, "get_components_by_class"):
                n = len(proxy.get_components_by_class(comp_class))
                if n > 0 and _tag_actor_pcg_landscape(proxy, add=True):
                    tagged_count += 1
        if tagged_count > 0:
            _log("World Partition: root has 0 components; tagged %d LandscapeStreamingProxy actor(s) with '%s' so Get Landscape Data finds full landscape. Generate again." % (tagged_count, PCG_LANDSCAPE_TAG))
        else:
            _tag_actor_pcg_landscape(land, add=True)
    except Exception:
        pass


def _load_config():
    """Load config from Content/Python/pcg_forest_config.json."""
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "pcg_forest_config.json")
        if not os.path.exists(config_path):
            return {"trees": [], "rocks": [], "height_filter_min": None, "height_filter_max": None,
                    "points_per_squared_meter": 0.05, "density_lower_bound": 0.3, "density_upper_bound": 1.0,
                    "transform_offset_z": -250.0, "spawn_harvestable_trees": False, "harvestable_tree_blueprint_path": "/Game/HomeWorld/Building/BP_HarvestableTree"}
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        trees = [p for p in (data.get("static_mesh_spawner_meshes") or []) if p]
        rocks = [p for p in (data.get("static_mesh_spawner_meshes_rocks") or []) if p]
        h_min, h_max = data.get("height_filter_min"), data.get("height_filter_max")
        if h_min is not None and h_max is not None:
            try:
                h_min, h_max = float(h_min), float(h_max)
            except (TypeError, ValueError):
                h_min, h_max = None, None
        points_per_m2 = float(data.get("points_per_squared_meter", 0.05))
        density_lo = float(data.get("density_lower_bound", 0.3))
        density_hi = float(data.get("density_upper_bound", 1.0))
        offset_z = float(data.get("transform_offset_z", -250.0))
        spawn_harvestable = bool(data.get("spawn_harvestable_trees", False))
        bp_path = str(data.get("harvestable_tree_blueprint_path") or "/Game/HomeWorld/Building/BP_HarvestableTree").strip()
        return {"trees": trees, "rocks": rocks, "height_filter_min": h_min, "height_filter_max": h_max,
                "points_per_squared_meter": points_per_m2, "density_lower_bound": density_lo, "density_upper_bound": density_hi,
                "transform_offset_z": offset_z, "spawn_harvestable_trees": spawn_harvestable, "harvestable_tree_blueprint_path": bp_path}
    except Exception as e:
        _log("Config load warning: " + str(e))
        return {"trees": [], "rocks": [], "height_filter_min": None, "height_filter_max": None,
                "points_per_squared_meter": 0.05, "density_lower_bound": 0.3, "density_upper_bound": 1.0,
                "transform_offset_z": -250.0, "spawn_harvestable_trees": False, "harvestable_tree_blueprint_path": "/Game/HomeWorld/Building/BP_HarvestableTree"}


def _get_mesh_paths():
    """Return list of tree mesh paths from config or placeholder."""
    paths = _load_config()["trees"]
    return paths if paths else [PLACEHOLDER_MESH]


def _get_output_pin_labels(node):
    """Return list of output pin labels (names) for a PCG node, excluding Execution Dependency for data wiring."""
    if node is None:
        return []
    try:
        pins = getattr(node, "output_pins", None) or []
        out = []
        for p in pins:
            try:
                props = getattr(p, "properties", None)
                if props is not None:
                    label = getattr(props, "label", None)
                    if label is not None:
                        s = str(label)
                        if s and s != EXECUTION_DEPENDENCY:
                            out.append(s)
            except Exception:
                pass
        return out
    except Exception:
        return []


def _get_input_pin_labels(node):
    """Return list of input pin labels for a PCG node."""
    if node is None:
        return []
    try:
        pins = getattr(node, "input_pins", None) or []
        out = []
        for p in pins:
            try:
                props = getattr(p, "properties", None)
                if props is not None:
                    label = getattr(props, "label", None)
                    if label is not None:
                        s = str(label)
                        if s:
                            out.append(s)
            except Exception:
                pass
        return out
    except Exception:
        return []


def _first_data_output_label(node):
    """First output pin label that is not Execution Dependency, or None."""
    labels = _get_output_pin_labels(node)
    for L in labels:
        if L != EXECUTION_DEPENDENCY:
            return L
    return labels[0] if labels else None


def _first_data_input_label(node):
    """First input pin label that is not Execution Dependency, or None."""
    labels = _get_input_pin_labels(node)
    for L in labels:
        if L != EXECUTION_DEPENDENCY:
            return L
    return labels[0] if labels else None


def _find_input_pin_label(node, preferred_names):
    """Return the first input pin label that matches one of preferred_names, or first data input."""
    labels = _get_input_pin_labels(node)
    for name in preferred_names:
        if name in labels:
            return name
    return _first_data_input_label(node)


def _add_edge_safe(graph_asset, from_node, from_label, to_node, to_label):
    """Add edge using Name labels; log on failure."""
    if not from_label or not to_label:
        return False
    try:
        graph_asset.add_edge(from_node, unreal.Name(from_label), to_node, unreal.Name(to_label))
        return True
    except Exception as e:
        _log("Edge %s -> %s failed: %s" % (from_label, to_label, e))
        return False


def _set_graph_node_position(node, x, y):
    """Try to set node position in graph editor (NodePosX/NodePosY). Works for Blueprint/PCG if supported."""
    if node is None:
        return
    for (px, py) in [("NodePosX", "NodePosY"), ("node_pos_x", "node_pos_y")]:
        try:
            if hasattr(node, "set_editor_property"):
                node.set_editor_property(px, int(x))
                node.set_editor_property(py, int(y))
                return
        except Exception:
            continue


def _ensure_pcg_folder():
    """Ensure /Game/HomeWorld/PCG exists (creating an asset there creates the folder)."""
    pass


def _connect_exclusion_points_to_difference(graph_asset, difference_node, exclusion_zones):
    """Build exclusion point source and connect to Difference node's second input. Optional."""
    if not exclusion_zones or not difference_node:
        return
    merge_node = None
    try:
        merge_class = getattr(unreal, "PCGMergeSettings", None)
        if merge_class:
            merge_node, _ = graph_asset.add_node_of_type(merge_class)
            _set_graph_node_position(merge_node, 1200, 900)
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
            create_class = getattr(unreal, "PCGCreatePointsGridSettings", None) or getattr(unreal, "PCGCreatePointsSettings", None)
            if not create_class:
                break
            point_node, point_settings = graph_asset.add_node_of_type(create_class)
            if not point_node:
                break
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
            _set_graph_node_position(point_node, 400 + len(created_point_nodes) * 350, 900)
        except Exception:
            continue
    diff_in_labels = _get_input_pin_labels(difference_node)
    diff_pin = "Difference" if "Difference" in diff_in_labels else ("Differences" if "Differences" in diff_in_labels else _first_data_input_label(difference_node))
    merge_out = _first_data_output_label(merge_node) if merge_node else None
    if merge_node and created_point_nodes:
        for node in created_point_nodes:
            out_l = _first_data_output_label(node)
            if out_l and merge_out:
                _add_edge_safe(graph_asset, node, out_l, merge_node, _first_data_input_label(merge_node))
        if merge_out and diff_pin:
            _add_edge_safe(graph_asset, merge_node, merge_out, difference_node, diff_pin)
    elif created_point_nodes and len(created_point_nodes) == 1 and diff_pin:
        out_l = _first_data_output_label(created_point_nodes[0])
        if out_l:
            _add_edge_safe(graph_asset, created_point_nodes[0], out_l, difference_node, diff_pin)
    else:
        _log("Exclusion zones defined but exclusion point source could not be connected. Wire exclusion to Difference in Editor if needed.")


def create_pcg_graph(exclusion_zones=None, force_recreate=False):
    """Create PCG graph with Get Landscape Data, Surface Sampler -> Density -> [Difference] -> Transform -> Spawner.
    Optional rocks branch with Merge. Does NOT set Get Landscape Data actor/tag (user sets By Tag + PCG_Landscape).
    Does NOT assign graph to volume or call Generate. Returns graph asset or None.
    Default force_recreate=False: existing graph is reused; create only when asset is missing. If True, existing graph is deleted and recreated (opt-in escape hatch)."""
    _ensure_pcg_folder()
    if exclusion_zones is None:
        exclusion_zones = []
    if unreal.EditorAssetLibrary.does_asset_exist(PCG_GRAPH_PACKAGE):
        if force_recreate:
            try:
                unreal.EditorAssetLibrary.delete_asset(PCG_GRAPH_PACKAGE)
                _log("Deleted existing PCG graph for recreation.")
            except Exception as e:
                _log("Could not delete existing graph: %s" % e)
        else:
            existing = unreal.load_asset(PCG_GRAPH_PACKAGE)
            if existing:
                _log("PCG graph already exists at %s. Reusing (delete in Content Browser or set force_recreate=True to force recreation)." % PCG_GRAPH_PACKAGE)
                return existing
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.PCGGraphFactory()
    graph_asset = asset_tools.create_asset(PCG_GRAPH_NAME, "/Game/HomeWorld/PCG", unreal.PCGGraph, factory)
    if not graph_asset:
        _log("Failed to create PCG graph asset.")
        return None

    input_node = graph_asset.get_input_node()
    output_node = graph_asset.get_output_node()
    input_out = _first_data_output_label(input_node)
    output_in = _first_data_input_label(output_node)
    if not input_out or not output_in:
        _log("Could not get input/output pin labels (got out=%s in=%s)." % (input_out, output_in))
        return None

    # Get Landscape Data (user sets By Tag + PCG_Landscape in Editor)
    get_landscape_node = None
    get_landscape_cls = getattr(unreal, "PCGGetLandscapeSettings", None)
    if get_landscape_cls:
        try:
            get_landscape_node, _ = graph_asset.add_node_of_type(get_landscape_cls)
            _set_graph_node_position(get_landscape_node, 400, 0)
        except Exception as e:
            _log("Get Landscape Data node skipped: %s" % e)
    else:
        _log("Get Landscape Data node skipped (PCGGetLandscapeSettings not found). Add it manually and set By Tag + PCG_Landscape.")
    landscape_out = _first_data_output_label(get_landscape_node) if get_landscape_node else None

    config = _load_config()
    use_harvestable_trees = config.get("spawn_harvestable_trees", False)
    harvestable_bp_path = config.get("harvestable_tree_blueprint_path") or "/Game/HomeWorld/Building/BP_HarvestableTree"
    actor_spawner_cls = getattr(unreal, "PCGSpawnActorSettings", None)

    # Main chain: Surface Sampler, Density, Transform, Spawner (spaced for graph editor)
    surface_node, surface_settings = graph_asset.add_node_of_type(unreal.PCGSurfaceSamplerSettings)
    _set_graph_node_position(surface_node, 400, 300)
    density_node, density_settings = graph_asset.add_node_of_type(unreal.PCGDensityFilterSettings)
    _set_graph_node_position(density_node, 800, 300)
    transform_node, transform_settings = graph_asset.add_node_of_type(unreal.PCGTransformPointsSettings)
    _set_graph_node_position(transform_node, 1200, 300)
    if use_harvestable_trees and actor_spawner_cls:
        spawner_node, spawner_settings = graph_asset.add_node_of_type(actor_spawner_cls)
        tree_spawner_is_actor = True
    else:
        spawner_node, spawner_settings = graph_asset.add_node_of_type(unreal.PCGStaticMeshSpawnerSettings)
        tree_spawner_is_actor = False
    _set_graph_node_position(spawner_node, 1600, 300)
    if not all([surface_node, density_node, transform_node, spawner_node]):
        _log("Failed to add one or more nodes.")
        return None

    points_per_m2 = config.get("points_per_squared_meter", 0.05)
    density_lo = config.get("density_lower_bound", 0.3)
    density_hi = config.get("density_upper_bound", 1.0)
    surface_settings.set_editor_property("points_per_squared_meter", points_per_m2)
    surface_settings.set_editor_property("apply_density_to_points", True)
    try:
        surface_settings.set_editor_property("use_seed", True)
    except Exception:
        pass
    try:
        surface_settings.set_editor_property("seed", 12345)
    except Exception:
        pass
    density_settings.set_editor_property("lower_bound", density_lo)
    density_settings.set_editor_property("upper_bound", density_hi)
    # UE Python Rotator(roll, pitch, yaw): only vary Yaw so trees stay upright (0 pitch, 0 roll).
    rot_min = unreal.Rotator(0.0, 0.0, 0.0)    # roll=0, pitch=0, yaw=0
    rot_max = unreal.Rotator(0.0, 0.0, 359.0)   # roll=0, pitch=0, yaw=359
    transform_settings.set_editor_property("rotation_min", rot_min)
    transform_settings.set_editor_property("rotation_max", rot_max)
    transform_settings.set_editor_property("absolute_rotation", True)
    transform_settings.set_editor_property("scale_min", unreal.Vector(0.8, 0.8, 0.8))
    transform_settings.set_editor_property("scale_max", unreal.Vector(1.2, 1.2, 1.2))
    transform_settings.set_editor_property("uniform_scale", True)
    transform_settings.set_editor_property("absolute_scale", True)
    transform_settings.set_editor_property("seed", 12345)
    # transform_offset_z: 0 = base-pivot; for center-pivot meshes use positive (e.g. 250) to lift so base sits on surface. See docs/PCG_SETUP.md.
    offset_z = config.get("transform_offset_z", 0.0)
    transform_settings.set_editor_property("offset_min", unreal.Vector(0.0, 0.0, float(offset_z)))
    transform_settings.set_editor_property("offset_max", unreal.Vector(0.0, 0.0, float(offset_z)))
    try:
        transform_settings.set_editor_property("absolute_offset", True)  # world-space Z so positive = up
    except Exception:
        pass

    # Rotation is yaw-only above (rotation_min/max) so instances stay upright. UE 5.7 Static Mesh Spawner has no align-to-surface option.

    if tree_spawner_is_actor:
        template_set = False
        try:
            bp_asset = unreal.load_asset(harvestable_bp_path) if unreal.EditorAssetLibrary.does_asset_exist(harvestable_bp_path) else None
            if bp_asset and hasattr(spawner_settings, "set_editor_property"):
                for prop in ("template_actor", "actor_class", "template"):
                    try:
                        spawner_settings.set_editor_property(prop, bp_asset)
                        template_set = True
                        _log("Tree branch: Actor Spawner template set to %s (property %s)." % (harvestable_bp_path, prop))
                        break
                    except Exception:
                        continue
            if not template_set:
                _log("Tree branch: Actor Spawner added. Set Template Actor to BP_HarvestableTree in ForestIsland_PCG Details (%s)." % harvestable_bp_path)
        except Exception as e:
            _log("Actor Spawner template warning: %s. Set Template Actor to BP_HarvestableTree in ForestIsland_PCG Details." % e)
        tree_entries_set = False
        tree_entry_count = 0
    else:
        mesh_paths = _get_mesh_paths()
        tree_entries_set = False
        tree_entry_count = 0
        entry_cls = getattr(unreal, "PCGStaticMeshSpawnerEntry", None)
        try:
            if entry_cls:
                spawner_settings.set_mesh_selector_type(unreal.PCGMeshSelectorWeighted)
                selector = spawner_settings.get_editor_property("mesh_selector_parameters")
                if selector and mesh_paths:
                    entries = []
                    for path in mesh_paths:
                        mesh_asset = unreal.load_asset(path)
                        if mesh_asset:
                            entries.append(entry_cls(weight=100, mesh=mesh_asset))
                    tree_entry_count = len(entries)
                    if entries and hasattr(selector, "set_editor_property"):
                        selector.set_editor_property("mesh_entries", entries)
                        tree_entries_set = True
            else:
                _log("Tree meshes: set in Editor — open ForestIsland_PCG, select the tree Static Mesh Spawner node, in Details set the mesh list (e.g. from pcg_forest_config.json).")
        except Exception as e:
            _log("Mesh selector setup warning: %s" % e)

    # Optional height filter
    height_filter_node = None
    h_min, h_max = config.get("height_filter_min"), config.get("height_filter_max")
    if h_min is not None and h_max is not None:
        try:
            height_filter_node, height_filter_settings = graph_asset.add_node_of_type(unreal.PCGAttributeFilteringRangeSettings)
            _set_graph_node_position(height_filter_node, 800, 600)
            if height_filter_node and height_filter_settings and hasattr(height_filter_settings, "set_editor_property"):
                height_filter_settings.set_editor_property("min_threshold", h_min)
                height_filter_settings.set_editor_property("max_threshold", h_max)
                _log("Added optional height filter (%.1f–%.1f). Set target attribute to Position.Z in Editor if needed." % (h_min, h_max))
        except (AttributeError, Exception) as e:
            _log("Height filter skipped: %s" % e)
            height_filter_node = None

    # Optional Difference for exclusion zones
    difference_node = None
    if exclusion_zones:
        try:
            difference_node, _ = graph_asset.add_node_of_type(unreal.PCGDifferenceSettings)
            _set_graph_node_position(difference_node, 1200, 600)
            if difference_node:
                _log("Added Difference node for %d exclusion zone(s)." % len(exclusion_zones))
        except (AttributeError, Exception) as e:
            _log("Difference node skipped: %s" % e)
            difference_node = None

    # Wire: Input -> Surface Sampler (Bounding); Get Landscape Data -> Surface Sampler (Surface)
    bounding_pin = _find_input_pin_label(surface_node, ["Bounding Shape", "Bounding", "In"])
    surface_pin = _find_input_pin_label(surface_node, ["Surface"])
    if bounding_pin:
        _add_edge_safe(graph_asset, input_node, input_out, surface_node, bounding_pin)
    if get_landscape_node and landscape_out and surface_pin:
        _add_edge_safe(graph_asset, get_landscape_node, landscape_out, surface_node, surface_pin)

    # Wire: Surface -> [Height] -> Density -> [Difference] -> Transform -> Spawner
    surface_out = _first_data_output_label(surface_node)
    density_in = _first_data_input_label(density_node)
    density_out = _first_data_output_label(density_node)
    transform_in = _first_data_input_label(transform_node)
    transform_out = _first_data_output_label(transform_node)
    spawner_in = _first_data_input_label(spawner_node)
    spawner_out = _first_data_output_label(spawner_node)
    if height_filter_node:
        h_in = _first_data_input_label(height_filter_node)
        h_out = _first_data_output_label(height_filter_node)
        if surface_out and h_in:
            _add_edge_safe(graph_asset, surface_node, surface_out, height_filter_node, h_in)
        if h_out and density_in:
            _add_edge_safe(graph_asset, height_filter_node, h_out, density_node, density_in)
    else:
        if surface_out and density_in:
            _add_edge_safe(graph_asset, surface_node, surface_out, density_node, density_in)
    if difference_node:
        diff_in = _first_data_input_label(difference_node)
        diff_out = _first_data_output_label(difference_node)
        if density_out and diff_in:
            _add_edge_safe(graph_asset, density_node, density_out, difference_node, diff_in)
        _connect_exclusion_points_to_difference(graph_asset, difference_node, exclusion_zones)
        if diff_out and transform_in:
            _add_edge_safe(graph_asset, difference_node, diff_out, transform_node, transform_in)
    else:
        if density_out and transform_in:
            _add_edge_safe(graph_asset, density_node, density_out, transform_node, transform_in)
    if transform_out and spawner_in:
        _add_edge_safe(graph_asset, transform_node, transform_out, spawner_node, spawner_in)

    # Rocks branch: optional second chain + Merge so both trees and rocks feed Output
    rock_paths = config.get("rocks") or []
    merge_node = None
    if rock_paths:
        surface_rock, surface_rock_settings = graph_asset.add_node_of_type(unreal.PCGSurfaceSamplerSettings)
        _set_graph_node_position(surface_rock, 400, 1200)
        density_rock, density_rock_settings = graph_asset.add_node_of_type(unreal.PCGDensityFilterSettings)
        _set_graph_node_position(density_rock, 800, 1200)
        transform_rock, transform_rock_settings = graph_asset.add_node_of_type(unreal.PCGTransformPointsSettings)
        _set_graph_node_position(transform_rock, 1200, 1200)
        spawner_rock, spawner_rock_settings = graph_asset.add_node_of_type(unreal.PCGStaticMeshSpawnerSettings)
        _set_graph_node_position(spawner_rock, 1600, 1200)
        merge_class = getattr(unreal, "PCGMergeSettings", None)
        if merge_class:
            merge_node, _ = graph_asset.add_node_of_type(merge_class)
            _set_graph_node_position(merge_node, 1200, 900)
        if all([surface_rock, density_rock, transform_rock, spawner_rock]):
            surface_rock_settings.set_editor_property("points_per_squared_meter", 0.01)
            surface_rock_settings.set_editor_property("apply_density_to_points", True)
            try:
                surface_rock_settings.set_editor_property("use_seed", True)
            except Exception:
                pass
            try:
                surface_rock_settings.set_editor_property("seed", 54321)
            except Exception:
                pass
            density_rock_settings.set_editor_property("lower_bound", 0.3)
            density_rock_settings.set_editor_property("upper_bound", 1.0)
            transform_rock_settings.set_editor_property("rotation_min", unreal.Rotator(0.0, 0.0, 0.0))
            transform_rock_settings.set_editor_property("rotation_max", unreal.Rotator(0.0, 0.0, 359.0))  # roll=0, pitch=0, yaw=359
            transform_rock_settings.set_editor_property("absolute_rotation", True)
            transform_rock_settings.set_editor_property("scale_min", unreal.Vector(0.8, 0.8, 0.8))
            transform_rock_settings.set_editor_property("scale_max", unreal.Vector(1.2, 1.2, 1.2))
            transform_rock_settings.set_editor_property("uniform_scale", True)
            transform_rock_settings.set_editor_property("absolute_scale", True)
            transform_rock_settings.set_editor_property("seed", 54321)
            try:
                transform_rock_settings.set_editor_property("offset_min", unreal.Vector(0.0, 0.0, float(offset_z)))
                transform_rock_settings.set_editor_property("offset_max", unreal.Vector(0.0, 0.0, float(offset_z)))
                try:
                    transform_rock_settings.set_editor_property("absolute_offset", True)
                except Exception:
                    pass
            except Exception:
                pass
            rock_entries_set = False
            rock_entry_count = 0
            entry_cls_rock = getattr(unreal, "PCGStaticMeshSpawnerEntry", None)
            try:
                if entry_cls_rock:
                    spawner_rock_settings.set_mesh_selector_type(unreal.PCGMeshSelectorWeighted)
                    selector_rock = spawner_rock_settings.get_editor_property("mesh_selector_parameters")
                    if selector_rock:
                        entries = [entry_cls_rock(weight=100, mesh=unreal.load_asset(p)) for p in rock_paths if unreal.load_asset(p)]
                        rock_entry_count = len(entries)
                        if entries and hasattr(selector_rock, "set_editor_property"):
                            selector_rock.set_editor_property("mesh_entries", entries)
                            rock_entries_set = True
                else:
                    _log("Rocks: set in Editor — open ForestIsland_PCG, select the rocks Static Mesh Spawner node, in Details set the mesh list.")
            except Exception as e:
                _log("Rocks mesh selector warning: %s" % e)
            # Wire rocks: Input + Landscape -> surface_rock -> ... -> spawner_rock
            bound_r = _find_input_pin_label(surface_rock, ["Bounding Shape", "Bounding", "In"])
            surf_r = _find_input_pin_label(surface_rock, ["Surface"])
            if bound_r:
                _add_edge_safe(graph_asset, input_node, input_out, surface_rock, bound_r)
            if get_landscape_node and landscape_out and surf_r:
                _add_edge_safe(graph_asset, get_landscape_node, landscape_out, surface_rock, surf_r)
            so_r = _first_data_output_label(surface_rock)
            di_r = _first_data_input_label(density_rock)
            do_r = _first_data_output_label(density_rock)
            ti_r = _first_data_input_label(transform_rock)
            to_r = _first_data_output_label(transform_rock)
            si_r = _first_data_input_label(spawner_rock)
            so_spawn_r = _first_data_output_label(spawner_rock)
            if so_r and di_r:
                _add_edge_safe(graph_asset, surface_rock, so_r, density_rock, di_r)
            if do_r and ti_r:
                _add_edge_safe(graph_asset, density_rock, do_r, transform_rock, ti_r)
            if to_r and si_r:
                _add_edge_safe(graph_asset, transform_rock, to_r, spawner_rock, si_r)
            if merge_node:
                merge_in = _first_data_input_label(merge_node)
                merge_out = _first_data_output_label(merge_node)
                if spawner_out and merge_in:
                    _add_edge_safe(graph_asset, spawner_node, spawner_out, merge_node, merge_in)
                if so_spawn_r and merge_in:
                    _add_edge_safe(graph_asset, spawner_rock, so_spawn_r, merge_node, merge_in)
                if merge_out and output_in:
                    _add_edge_safe(graph_asset, merge_node, merge_out, output_node, output_in)
                _log("Added optional rocks branch and Merge.")
            else:
                _add_edge_safe(graph_asset, spawner_rock, so_spawn_r, output_node, output_in)
                _log("Added optional rocks branch (no Merge; trees branch overwritten in some engines).")
        else:
            _log("Rocks branch nodes failed; only trees branch connected.")
    if merge_node is None:
        if spawner_out and output_in:
            _add_edge_safe(graph_asset, spawner_node, spawner_out, output_node, output_in)

    try:
        unreal.EditorAssetLibrary.save_loaded_asset(graph_asset)
    except Exception:
        pass
    if tree_spawner_is_actor:
        _log("Created and saved PCG graph: %s (tree branch = Actor Spawner / harvestable). Set Get Landscape Data to By Tag + PCG_Landscape, assign graph to volume, then Generate." % PCG_GRAPH_PACKAGE)
    else:
        _log("Created and saved PCG graph: %s. Set Get Landscape Data to By Tag + PCG_Landscape, assign graph to volume, then Generate." % PCG_GRAPH_PACKAGE)
    return graph_asset


def _find_existing_pcg_volume(world):
    """Return the first non-exclusion PCGVolume in the level, or None."""
    try:
        volumes = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.PCGVolume)
        for vol in (volumes or []):
            try:
                tags = vol.get_editor_property("tags") if hasattr(vol, "get_editor_property") else getattr(vol, "tags", [])
                tag_strs = [str(t) for t in tags] if tags else []
                if "PCG_Exclusion" not in tag_strs:
                    return vol
            except Exception:
                return vol
    except Exception:
        pass
    return None


def destroy_pcg_volume(world=None):
    """Destroy the level's main PCG Volume (PCG_Forest) so a fresh one can be placed with correct dimensions.
    Returns True if a volume was destroyed, False otherwise."""
    if world is None:
        world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        return False
    volume = _find_existing_pcg_volume(world)
    if not volume:
        return False
    try:
        unreal.EditorLevelLibrary.destroy_actor(volume)
        _log("Destroyed existing PCG Volume.")
        return True
    except Exception as e:
        _log("Could not destroy PCG Volume: %s" % e)
        return False


def update_forest_island_graph_from_config(graph_asset):
    """Re-apply density, transform_offset_z and rotation from pcg_forest_config.json to existing graph nodes.
    Updates Surface Sampler (points_per_squared_meter), Density Filter (bounds), and Transform Points (offset, rotation).
    Call when graph already exists so config changes take effect without recreating the graph."""
    if not graph_asset:
        return
    config = _load_config()
    offset_z = float(config.get("transform_offset_z", 0.0))
    points_per_m2 = float(config.get("points_per_squared_meter", 0.05))
    density_lo = float(config.get("density_lower_bound", 0.3))
    density_hi = float(config.get("density_upper_bound", 1.0))
    rot_min = unreal.Rotator(0.0, 0.0, 0.0)   # roll=0, pitch=0, yaw=0
    rot_max = unreal.Rotator(0.0, 0.0, 359.0) # roll=0, pitch=0, yaw=359
    transform_cls = getattr(unreal, "PCGTransformPointsSettings", None)
    surface_cls = getattr(unreal, "PCGSurfaceSamplerSettings", None)
    density_cls = getattr(unreal, "PCGDensityFilterSettings", None)
    if not transform_cls:
        return
    try:
        nodes = getattr(graph_asset, "nodes", None) or []
    except Exception:
        nodes = []
    updated = 0
    first_readback = None
    surface_sampler_index = 0
    for node in nodes:
        try:
            settings = node.get_settings() if hasattr(node, "get_settings") else None
            if settings and surface_cls and isinstance(settings, surface_cls):
                settings.set_editor_property("points_per_squared_meter", points_per_m2)
                settings.set_editor_property("apply_density_to_points", True)
                try:
                    settings.set_editor_property("use_seed", True)
                except Exception:
                    pass
                try:
                    settings.set_editor_property("seed", 12345 if surface_sampler_index == 0 else 54321)
                except Exception:
                    pass
                surface_sampler_index += 1
                updated += 1
                continue
            if settings and density_cls and isinstance(settings, density_cls):
                settings.set_editor_property("lower_bound", density_lo)
                settings.set_editor_property("upper_bound", density_hi)
                updated += 1
                continue
        except Exception:
            pass
    for node in nodes:
        try:
            settings = node.get_settings() if hasattr(node, "get_settings") else None
            if settings is None or not isinstance(settings, transform_cls):
                continue
            settings.set_editor_property("offset_min", unreal.Vector(0.0, 0.0, offset_z))
            settings.set_editor_property("offset_max", unreal.Vector(0.0, 0.0, offset_z))
            try:
                settings.set_editor_property("absolute_offset", True)
            except Exception:
                pass
            settings.set_editor_property("rotation_min", rot_min)
            settings.set_editor_property("rotation_max", rot_max)
            settings.set_editor_property("absolute_rotation", True)
            updated += 1
            if first_readback is None:
                try:
                    rmin = settings.get_editor_property("rotation_min")
                    omin = settings.get_editor_property("offset_min")
                    abs_rot = settings.get_editor_property("absolute_rotation")
                    abs_off = settings.get_editor_property("absolute_offset") if hasattr(settings, "get_editor_property") else None
                    first_readback = {"rotation_min_pitch": getattr(rmin, "pitch", None), "rotation_min_yaw": getattr(rmin, "yaw", None), "rotation_min_roll": getattr(rmin, "roll", None), "offset_min_z": getattr(omin, "z", None), "absolute_rotation": abs_rot, "absolute_offset": abs_off}
                except Exception as e:
                    first_readback = {"readback_error": str(e)}
        except Exception as e:
            _log("update_forest_island_graph: skip node: %s" % e)
    if updated:
        _log("Updated graph from config: Surface/Density/Transform (points_per_m2=%.3f, density=%.2f-%.2f, offset_z=%.0f). Surface Samplers use seeds 12345 (tree) and 54321 (rocks) so rocks do not spawn on tree positions." % (points_per_m2, density_lo, density_hi, offset_z))


def place_pcg_volume(location=None, extent=None, graph_asset=None):
    """Place a PCG Volume in the current level (or reuse existing), size it to extent, save level.
    If graph_asset is provided, tries to assign it to the volume, set Get Landscape Data tag, and trigger Generate.
    location: unreal.Vector for volume center (default 0,0,0).
    extent: unreal.Vector for half-extents in cm (default VOLUME_HALF_EXTENT_*).
    graph_asset: optional PCG graph asset; when set, runs try_assign_graph_to_volume, try_set_get_landscape_selector, trigger_pcg_generate."""
    editor_subsystem = unreal.EditorLevelLibrary
    world = editor_subsystem.get_editor_world()
    if not world:
        _log("No editor world. Open a level (e.g. Main) first.")
        return

    if location is None:
        location = unreal.Vector(0.0, 0.0, 0.0)
    if extent is None:
        extent = unreal.Vector(VOLUME_HALF_EXTENT_X, VOLUME_HALF_EXTENT_Y, VOLUME_HALF_EXTENT_Z)

    volume = _find_existing_pcg_volume(world)
    if volume:
        _log("Reusing existing PCG Volume.")
        volume.set_actor_location(location, False, False)
    else:
        rotation = unreal.Rotator(0.0, 0.0, 0.0)
        volume = editor_subsystem.spawn_actor_from_class(unreal.PCGVolume, location, rotation)
        if not volume:
            _log("Failed to spawn PCG Volume.")
            return

    try:
        if hasattr(volume, "set_actor_label"):
            volume.set_actor_label("PCG_Forest")
    except Exception:
        pass

    try:
        volume.set_actor_scale3d(unreal.Vector(1.0, 1.0, 1.0))
        _, base_ext = volume.get_actor_bounds(False)
        if base_ext.x > 0 and base_ext.y > 0 and base_ext.z > 0:
            scale_x = abs(extent.x) / base_ext.x
            scale_y = abs(extent.y) / base_ext.y
            scale_z = abs(extent.z) / base_ext.z
            volume.set_actor_scale3d(unreal.Vector(scale_x, scale_y, scale_z))
            _log("Scaled PCG Volume to extent (%.0f, %.0f, %.0f) cm." % (extent.x, extent.y, extent.z))
        else:
            _log("Default volume extent is zero; set volume bounds manually in Editor.")
    except Exception as e:
        _log("Could not scale volume: %s. Set bounds manually in Details." % str(e))

    editor_subsystem.save_current_level()
    if graph_asset:
        _log("Attempting to assign graph, set Get Landscape Data + mesh lists, and trigger Generate (demo-ready)...")
        update_forest_island_graph_from_config(graph_asset)
        try_set_get_landscape_selector(graph_asset)
        try_set_spawner_mesh_lists(graph_asset)
        try_assign_graph_to_volume(graph_asset)
        trigger_pcg_generate()
        try:
            editor_subsystem.save_current_level()
            _log("Level saved after Generate; PCG instances persisted.")
        except Exception as e:
            _log("Save after Generate failed: %s" % e)
    else:
        _log("PCG Volume placed and level saved. Assign your PCG graph to the volume in Details and click Generate.")


def try_world_partition():
    """No-op; document manual step if needed."""
    pass


def try_assign_graph_to_volume(graph_asset):
    """Try to assign the PCG graph to the level's PCG Volume. Logs success or failure.
    In UE 5.7 the graph property is often protected; this tries every available API."""
    if not graph_asset:
        _log("try_assign_graph: No graph asset.")
        return False
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        _log("try_assign_graph: No editor world.")
        return False
    volume = _find_existing_pcg_volume(world)
    if not volume:
        _log("try_assign_graph: No PCG Volume in level.")
        return False
    comp = volume.get_component_by_class(unreal.PCGComponent)
    if not comp:
        _log("try_assign_graph: No PCGComponent on volume.")
        return False
    for name in ("graph", "generated_graph", "graph_instance"):
        try:
            if hasattr(comp, "set_editor_property"):
                comp.set_editor_property(name, graph_asset)
                _log("try_assign_graph: Set %s on PCGComponent (may be protected)." % name)
                return True
        except Exception as e:
            _log("try_assign_graph: set_editor_property(%s) failed: %s" % (name, e))
    if hasattr(comp, "set_graph"):
        try:
            comp.set_graph(graph_asset)
            _log("try_assign_graph: set_graph() succeeded.")
            return True
        except Exception as e:
            _log("try_assign_graph: set_graph() failed: %s" % e)
    _log("try_assign_graph: Could not assign graph from script. Assign ForestIsland_PCG to the volume in Details.")
    return False


def try_set_get_landscape_selector(graph_asset):
    """Try to set Get Landscape Data node to use By Tag + PCG_Landscape. Logs success or failure.
    Many selector properties are not exposed in Python; this tries common names."""
    if not graph_asset:
        return False
    try:
        nodes = getattr(graph_asset, "nodes", None) or []
    except Exception:
        nodes = []
    get_landscape_cls = getattr(unreal, "PCGGetLandscapeSettings", None)
    if not get_landscape_cls:
        return False
    for node in nodes:
        try:
            settings = node.get_settings() if hasattr(node, "get_settings") else None
            if settings is None or not isinstance(settings, get_landscape_cls):
                continue
            # Try common selector/tag property names (engine-specific).
            for prop in ("tag", "selected_tag", "actor_tag", "filter_tag", "landscape_tag"):
                try:
                    if hasattr(settings, "set_editor_property"):
                        settings.set_editor_property(prop, PCG_LANDSCAPE_TAG)
                        _log("try_set_get_landscape_selector: Set %s = %s." % (prop, PCG_LANDSCAPE_TAG))
                        return True
                except Exception:
                    continue
            # Try nested actor filter (some engines use actor_selector_settings).
            for prop in ("actor_selector", "actor_filter", "selector_settings"):
                try:
                    sub = settings.get_editor_property(prop) if hasattr(settings, "get_editor_property") else getattr(settings, prop, None)
                    if sub is not None and hasattr(sub, "set_editor_property"):
                        for subprop in ("tag", "selected_tag", "tag_name"):
                            try:
                                sub.set_editor_property(subprop, PCG_LANDSCAPE_TAG)
                                _log("try_set_get_landscape_selector: Set %s.%s = %s." % (prop, subprop, PCG_LANDSCAPE_TAG))
                                return True
                            except Exception:
                                continue
                except Exception:
                    continue
        except Exception as e:
            _log("try_set_get_landscape_selector: Node check failed: %s" % e)
    # Try with unreal.Name for tag (some APIs expect Name not str)
    tag_name = getattr(unreal, "Name", None)
    if tag_name is not None:
        try:
            name_val = tag_name(PCG_LANDSCAPE_TAG)
        except Exception:
            name_val = None
        if name_val is not None:
            for node in nodes:
                try:
                    settings = node.get_settings() if hasattr(node, "get_settings") else None
                    if settings is None or not isinstance(settings, get_landscape_cls):
                        continue
                    for prop in ("tag", "selected_tag", "actor_tag", "filter_tag", "landscape_tag", "tag_name"):
                        try:
                            if hasattr(settings, "set_editor_property"):
                                settings.set_editor_property(prop, name_val)
                                _log("try_set_get_landscape_selector: Set %s = %s (Name)." % (prop, PCG_LANDSCAPE_TAG))
                                return True
                        except Exception:
                            continue
                    for prop in ("actor_selector", "actor_filter", "selector_settings"):
                        try:
                            sub = settings.get_editor_property(prop) if hasattr(settings, "get_editor_property") else getattr(settings, prop, None)
                            if sub is not None and hasattr(sub, "set_editor_property"):
                                for subprop in ("tag", "selected_tag", "tag_name", "filter_tag", "actor_filter_tag"):
                                    try:
                                        sub.set_editor_property(subprop, name_val)
                                        _log("try_set_get_landscape_selector: Set %s.%s = %s (Name)." % (prop, subprop, PCG_LANDSCAPE_TAG))
                                        return True
                                    except Exception:
                                        continue
                        except Exception:
                            continue
                except Exception:
                    continue
    _log("try_set_get_landscape_selector: Could not set tag from script. Set Get Landscape Data to By Tag + PCG_Landscape in the graph Details.")
    return False


def try_set_spawner_mesh_lists(graph_asset):
    """Apply mesh lists from pcg_forest_config.json to all Static Mesh Spawner nodes in the graph.
    First spawner = trees (static_mesh_spawner_meshes), second = rocks (static_mesh_spawner_meshes_rocks).
    Logs what was set. If PCGStaticMeshSpawnerEntry is not in unreal, logs that user must set meshes in Editor."""
    if not graph_asset:
        return 0
    config = _load_config()
    tree_paths = config.get("trees") or []
    rock_paths = config.get("rocks") or []
    if not tree_paths and not rock_paths:
        _log("try_set_spawner_mesh_lists: No tree or rock paths in config.")
        return 0
    try:
        nodes = getattr(graph_asset, "nodes", None) or []
    except Exception:
        nodes = []
    spawner_cls = getattr(unreal, "PCGStaticMeshSpawnerSettings", None)
    entry_cls = getattr(unreal, "PCGStaticMeshSpawnerEntry", None)
    if not spawner_cls:
        _log("try_set_spawner_mesh_lists: PCGStaticMeshSpawnerSettings not found.")
        return 0
    if not entry_cls:
        _log("try_set_spawner_mesh_lists: PCGStaticMeshSpawnerEntry not in unreal; set mesh lists in Editor (Details on each Static Mesh Spawner node).")
        return 0
    spawner_settings_list = []
    for node in nodes:
        try:
            settings = node.get_settings() if hasattr(node, "get_settings") else None
            if settings is not None and isinstance(settings, spawner_cls):
                spawner_settings_list.append(settings)
        except Exception:
            continue
    updated = 0
    use_harvestable_trees = config.get("spawn_harvestable_trees", False)
    for i, spawner_settings in enumerate(spawner_settings_list):
        # When spawn_harvestable_trees is true, tree branch is Actor Spawner; only Static Mesh Spawners here are rocks (or none).
        if use_harvestable_trees:
            paths = rock_paths
        else:
            paths = tree_paths if i == 0 else rock_paths
        if not paths:
            continue
        try:
            spawner_settings.set_mesh_selector_type(unreal.PCGMeshSelectorWeighted)
            selector = spawner_settings.get_editor_property("mesh_selector_parameters")
            if not selector:
                continue
            entries = []
            for path in paths:
                mesh_asset = unreal.load_asset(path)
                if mesh_asset:
                    entries.append(entry_cls(weight=100, mesh=mesh_asset))
            if entries and hasattr(selector, "set_editor_property"):
                selector.set_editor_property("mesh_entries", entries)
                updated += 1
                _log("try_set_spawner_mesh_lists: Set %d mesh(es) on spawner %d (%s)." % (len(entries), i + 1, "trees" if i == 0 else "rocks"))
        except Exception as e:
            _log("try_set_spawner_mesh_lists: spawner %d failed: %s" % (i + 1, e))
    if updated == 0 and spawner_settings_list:
        _log("try_set_spawner_mesh_lists: Could not set mesh_entries on any spawner; set mesh list in Editor on each Static Mesh Spawner node.")
    return updated


def trigger_pcg_generate():
    """Find PCG_Forest volume, trigger Generate from script, and log component state.
    Run via Tools -> Execute Python Script (e.g. run create_pcg_forest then call trigger_pcg_generate()).
    Use when the Details-panel Generate button produces no Output Log lines: this forces execution and logs state."""
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        _log("trigger_pcg_generate: No editor world.")
        return
    volume = _find_existing_pcg_volume(world)
    if not volume:
        _log("trigger_pcg_generate: No PCG Volume (PCG_Forest) in level.")
        return
    comp = volume.get_component_by_class(unreal.PCGComponent)
    if not comp:
        _log("trigger_pcg_generate: PCG_Forest has no PCGComponent.")
        return
    try:
        graph = comp.get_editor_property("graph") if hasattr(comp, "get_editor_property") else getattr(comp, "graph", None)
        _log("trigger_pcg_generate: Graph assigned = %s" % (graph is not None))
        if graph:
            _log("trigger_pcg_generate: Graph path = %s" % (unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(graph) if graph else "N/A"))
    except Exception as e:
        _log("trigger_pcg_generate: Could not read graph (protected in UE 5.7); assuming set_graph() was used. %s" % e)
    if hasattr(comp, "generate"):
        _log("trigger_pcg_generate: Calling generate() now; watch Output Log for LogPCG lines.")
        try:
            comp.generate(True)  # UE 5.7: generate(force) required
            _log("trigger_pcg_generate: generate() returned.")
        except Exception as e:
            _log("trigger_pcg_generate: generate() failed: %s" % e)
    else:
        _log("trigger_pcg_generate: PCGComponent has no generate() method; try Generate in Details.")

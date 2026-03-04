# create_planetoid_poi_pcg.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Creates Planetoid_POI_PCG graph (Get Landscape Data -> Surface Sampler -> Transform -> Actor Spawner) for Day 17.
# Idempotent: reuses existing graph. Does NOT assign graph to volume or set Get Landscape Data By Tag (manual).
# Run create_bp_poi_placeholders.py first so BP_Shrine_POI exists; set Template in Actor Spawner in Editor if needed.
# Config: Content/Python/planetoid_map_config.json (optional poi_points_per_squared_meter).
# See docs/tasks/DAYS_16_TO_30.md (Day 17), docs/PCG_VARIABLES_NO_ACCESS.md.

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

PCG_GRAPH_PATH = "/Game/HomeWorld/PCG/Planetoid_POI_PCG"
DEFAULT_POI_BP = "/Game/HomeWorld/BP_Shrine_POI"
EXECUTION_DEPENDENCY = "Execution Dependency"


def _log(msg):
    unreal.log("Planetoid POI PCG: " + str(msg))
    print("Planetoid POI PCG: " + str(msg))


def _load_config():
    defaults = {"poi_points_per_squared_meter": 0.002}
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "planetoid_map_config.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "poi_points_per_squared_meter" in data:
                defaults["poi_points_per_squared_meter"] = float(data["poi_points_per_squared_meter"])
    except Exception as e:
        _log("Config: " + str(e))
    return defaults


def _get_output_pin_labels(node):
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
                        out.append(str(label))
            except Exception:
                pass
        return out
    except Exception:
        return []


def _first_data_output_label(node):
    labels = _get_output_pin_labels(node)
    for L in labels:
        if L != EXECUTION_DEPENDENCY:
            return L
    return labels[0] if labels else None


def _first_data_input_label(node):
    labels = _get_input_pin_labels(node)
    for L in labels:
        if L != EXECUTION_DEPENDENCY:
            return L
    return labels[0] if labels else None


def _find_input_pin_label(node, preferred_names):
    labels = _get_input_pin_labels(node)
    for name in preferred_names:
        if name in labels:
            return name
    return _first_data_input_label(node)


def _add_edge_safe(graph_asset, from_node, from_label, to_node, to_label):
    if not from_label or not to_label:
        return False
    try:
        graph_asset.add_edge(from_node, unreal.Name(from_label), to_node, unreal.Name(to_label))
        return True
    except Exception as e:
        _log("Edge failed: " + str(e))
        return False


def _set_graph_node_position(node, x, y):
    try:
        if hasattr(node, "position"):
            node.position = unreal.Vector2D(float(x), float(y))
        elif hasattr(node, "set_editor_property"):
            node.set_editor_property("position", unreal.Vector2D(float(x), float(y)))
    except Exception:
        pass


def _ensure_pcg_folder():
    if not unreal.EditorAssetLibrary.does_directory_exist("/Game/HomeWorld/PCG"):
        unreal.EditorAssetLibrary.make_directory("/Game/HomeWorld/PCG")


def main():
    _log("Start.")
    _ensure_pcg_folder()
    if unreal.EditorAssetLibrary.does_asset_exist(PCG_GRAPH_PATH):
        _log("Graph already exists at " + PCG_GRAPH_PATH + ". Open planetoid level, place PCG Volume, assign this graph, set Get Landscape Data By Tag PCG_Landscape, set Actor Spawner template, Generate.")
        return
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.PCGGraphFactory()
    graph_asset = asset_tools.create_asset("Planetoid_POI_PCG", "/Game/HomeWorld/PCG", unreal.PCGGraph, factory)
    if not graph_asset:
        _log("Failed to create PCG graph.")
        return
    input_node = graph_asset.get_input_node()
    output_node = graph_asset.get_output_node()
    input_out = _first_data_output_label(input_node)
    output_in = _first_data_input_label(output_node)
    if not input_out or not output_in:
        _log("Could not get input/output pins.")
        return

    get_landscape_cls = getattr(unreal, "PCGGetLandscapeSettings", None)
    get_landscape_node = None
    if get_landscape_cls:
        try:
            get_landscape_node, _ = graph_asset.add_node_of_type(get_landscape_cls)
            _set_graph_node_position(get_landscape_node, 300, 0)
        except Exception as e:
            _log("Get Landscape Data: " + str(e))
    landscape_out = _first_data_output_label(get_landscape_node) if get_landscape_node else None

    surface_node, surface_settings = graph_asset.add_node_of_type(unreal.PCGSurfaceSamplerSettings)
    _set_graph_node_position(surface_node, 300, 250)
    transform_node, transform_settings = graph_asset.add_node_of_type(unreal.PCGTransformPointsSettings)
    _set_graph_node_position(transform_node, 700, 250)
    actor_spawner_cls = getattr(unreal, "PCGSpawnActorSettings", None)
    if not actor_spawner_cls:
        _log("PCGSpawnActorSettings not found. Add Actor Spawner manually.")
        unreal.EditorAssetLibrary.save_loaded_asset(graph_asset)
        return
    spawner_node, spawner_settings = graph_asset.add_node_of_type(actor_spawner_cls)
    _set_graph_node_position(spawner_node, 1100, 250)

    config = _load_config()
    points_per_m2 = config.get("poi_points_per_squared_meter", 0.002)
    surface_settings.set_editor_property("points_per_squared_meter", points_per_m2)
    surface_settings.set_editor_property("apply_density_to_points", True)
    try:
        surface_settings.set_editor_property("use_seed", True)
        surface_settings.set_editor_property("seed", 77777)
    except Exception:
        pass
    transform_settings.set_editor_property("rotation_min", unreal.Rotator(0, 0, 0))
    transform_settings.set_editor_property("rotation_max", unreal.Rotator(0, 0, 359))
    transform_settings.set_editor_property("absolute_rotation", True)
    transform_settings.set_editor_property("scale_min", unreal.Vector(1, 1, 1))
    transform_settings.set_editor_property("scale_max", unreal.Vector(1, 1, 1))
    transform_settings.set_editor_property("absolute_scale", True)

    bounding_pin = _find_input_pin_label(surface_node, ["Bounding Shape", "Bounding", "In"])
    surface_pin = _find_input_pin_label(surface_node, ["Surface"])
    if bounding_pin:
        _add_edge_safe(graph_asset, input_node, input_out, surface_node, bounding_pin)
    if get_landscape_node and landscape_out and surface_pin:
        _add_edge_safe(graph_asset, get_landscape_node, landscape_out, surface_node, surface_pin)

    surface_out = _first_data_output_label(surface_node)
    transform_in = _first_data_input_label(transform_node)
    transform_out = _first_data_output_label(transform_node)
    spawner_in = _first_data_input_label(spawner_node)
    spawner_out = _first_data_output_label(spawner_node)
    _add_edge_safe(graph_asset, surface_node, surface_out, transform_node, transform_in)
    _add_edge_safe(graph_asset, transform_node, transform_out, spawner_node, spawner_in)
    _add_edge_safe(graph_asset, spawner_node, spawner_out, output_node, output_in)

    poi_bp_path = config.get("poi_actor_blueprint_path") or DEFAULT_POI_BP
    if unreal.EditorAssetLibrary.does_asset_exist(poi_bp_path):
        bp_asset = unreal.load_asset(poi_bp_path)
        if bp_asset:
            for prop in ("template_actor", "actor_class", "template"):
                try:
                    spawner_settings.set_editor_property(prop, bp_asset)
                    _log("Actor Spawner template set to " + poi_bp_path)
                    break
                except Exception:
                    continue
    else:
        _log("Set Actor Spawner Template to BP_Shrine_POI (or BP_Treasure_POI) in Planetoid_POI_PCG Details. Run create_bp_poi_placeholders.py first.")

    unreal.EditorAssetLibrary.save_loaded_asset(graph_asset)
    _log("Done. Open planetoid level, add Landscape with tag PCG_Landscape, place PCG Volume, assign Planetoid_POI_PCG, set Get Landscape Data By Tag, set Actor Spawner template if needed, Generate.")


if __name__ == "__main__":
    main()

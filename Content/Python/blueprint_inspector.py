# blueprint_inspector.py
# Reads Blueprint structure and exports as JSON.
# Callable via MCP: write a request then execute, or run directly.
#
# Usage via mcp_harness.py:
#   {"command": "inspect_blueprint", "args": {"path": "/Game/HomeWorld/Characters/BP_HomeWorldCharacter"}}
#
# Or directly: execute_python_script("blueprint_inspector.py")
# reads Saved/blueprint_inspect_request.json -> writes Saved/blueprint_inspect_result.json

import json
import os
import sys
import traceback

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)


def inspect_blueprint(bp_path):
    """Inspect a Blueprint and return its structure as a dict."""
    if not unreal.EditorAssetLibrary.does_asset_exist(bp_path):
        return {"error": "Asset not found: " + bp_path}

    bp = unreal.load_asset(bp_path)
    if not bp:
        return {"error": "Could not load: " + bp_path}

    result = {
        "path": bp_path,
        "asset_class": bp.get_class().get_name(),
        "variables": [],
        "components": [],
        "parent_class": "",
        "generated_class": "",
        "cdo_properties": {},
    }

    # Parent class
    try:
        parent = bp.get_editor_property("parent_class")
        result["parent_class"] = str(parent.get_name()) if parent else "None"
    except Exception:
        pass

    # Generated class
    gen_class = None
    try:
        gen_class = bp.generated_class()
    except Exception:
        try:
            gen_class = bp.get_editor_property("generated_class")
        except Exception:
            pass
    if gen_class:
        result["generated_class"] = gen_class.get_name()

    # CDO properties
    cdo = None
    if gen_class:
        try:
            cdo = unreal.get_default_object(gen_class)
        except Exception:
            pass

    # Components via SubobjectDataSubsystem
    try:
        subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
        handles = subsystem.k2_gather_subobject_data_for_blueprint(bp)
        bp_lib = unreal.SubobjectDataBlueprintFunctionLibrary
        for handle in handles:
            data = bp_lib.get_data(handle)
            obj = bp_lib.get_object(data)
            if obj:
                comp_info = {
                    "name": obj.get_name(),
                    "class": obj.get_class().get_name(),
                }
                # Read key properties for known component types
                cls_name = obj.get_class().get_name()
                if "SkeletalMesh" in cls_name:
                    try:
                        sk = obj.get_editor_property("skeletal_mesh_asset")
                        comp_info["skeletal_mesh"] = sk.get_name() if sk else "None"
                    except Exception:
                        pass
                    try:
                        ac = obj.get_editor_property("anim_class")
                        comp_info["anim_class"] = ac.get_name() if ac else "None"
                    except Exception:
                        pass
                elif "SpringArm" in cls_name:
                    try:
                        comp_info["target_arm_length"] = obj.get_editor_property("target_arm_length")
                    except Exception:
                        pass
                elif "Camera" in cls_name:
                    try:
                        comp_info["field_of_view"] = obj.get_editor_property("field_of_view")
                    except Exception:
                        pass
                elif "Capsule" in cls_name:
                    try:
                        comp_info["radius"] = obj.get_unscaled_capsule_radius()
                        comp_info["half_height"] = obj.get_unscaled_capsule_half_height()
                    except Exception:
                        pass
                result["components"].append(comp_info)
    except Exception as e:
        result["components_error"] = str(e)

    # Blueprint variables (new variables defined in Blueprint, not inherited)
    try:
        if hasattr(bp, "get_editor_property"):
            new_vars = bp.get_editor_property("new_variables")
            if new_vars:
                for v in new_vars:
                    var_info = {"name": str(v.get_editor_property("var_name"))}
                    try:
                        var_info["type"] = str(v.get_editor_property("var_type"))
                    except Exception:
                        pass
                    result["variables"].append(var_info)
    except Exception:
        pass

    # Read specific CDO properties if available
    if cdo:
        props_to_read = [
            "default_pawn_class", "capsule_radius", "capsule_half_height",
            "rotation_rate_yaw", "mesh_forward_yaw_offset",
            "target_arm_length", "camera_fov",
        ]
        for prop in props_to_read:
            try:
                val = cdo.get_editor_property(prop)
                result["cdo_properties"][prop] = str(val)
            except Exception:
                pass

    # Graph info (EventGraph nodes)
    try:
        graphs = bp.get_editor_property("ubergraph_pages")
        if graphs:
            result["graphs"] = []
            for graph in graphs:
                graph_info = {"name": graph.get_name(), "node_count": 0, "nodes": []}
                try:
                    nodes = graph.get_editor_property("nodes")
                    if nodes:
                        graph_info["node_count"] = len(nodes)
                        for node in nodes[:20]:  # Limit to first 20 nodes
                            node_info = {
                                "class": node.get_class().get_name(),
                                "name": node.get_name(),
                            }
                            try:
                                node_info["title"] = node.get_editor_property("node_title") if hasattr(node, "get_editor_property") else ""
                            except Exception:
                                pass
                            graph_info["nodes"].append(node_info)
                except Exception:
                    pass
                result["graphs"].append(graph_info)
    except Exception:
        pass

    return result


def _paths():
    proj = unreal.Paths.project_dir()
    saved = os.path.join(proj, "Saved")
    os.makedirs(saved, exist_ok=True)
    return (
        os.path.join(saved, "blueprint_inspect_request.json"),
        os.path.join(saved, "blueprint_inspect_result.json"),
    )


def main():
    req_path, out_path = _paths()

    bp_path = "/Game/HomeWorld/Characters/BP_HomeWorldCharacter"
    if os.path.exists(req_path):
        try:
            with open(req_path, "r", encoding="utf-8") as f:
                req = json.load(f)
            bp_path = req.get("path", bp_path)
            os.remove(req_path)
        except Exception:
            pass

    try:
        result = inspect_blueprint(bp_path)
    except Exception as e:
        result = {"error": str(e), "traceback": traceback.format_exc()}

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str)


if __name__ == "__main__":
    main()

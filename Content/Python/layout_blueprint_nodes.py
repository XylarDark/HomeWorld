# layout_blueprint_nodes.py
# Lays out Blueprint graph nodes in a grid so they are spaced apart when opened in the Blueprint editor.
#
# Usage:
#   Run from Editor: Tools -> Execute Python Script, then run this file.
#   Optional: write Saved/layout_blueprint_request.json with {"path": "/Game/.../BP_MyBlueprint"}
#   If no request file, uses default path below.
#
# Reads: Saved/layout_blueprint_request.json (optional)
# Writes: Saved/layout_blueprint_result.json with ok, node_count, graphs_updated.

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

DEFAULT_BP_PATH = "/Game/HomeWorld/Characters/BP_HomeWorldCharacter"
SPACING_X = 400
SPACING_Y = 280
ORIGIN_X = 200
ORIGIN_Y = 200
NODES_PER_ROW = 8


def _log(msg):
    unreal.log("Layout Blueprint Nodes: " + str(msg))
    print("Layout Blueprint Nodes: " + str(msg))


def _set_node_position(node, x, y):
    """Try to set graph node position. Returns True if successful."""
    try:
        if hasattr(node, "set_editor_property"):
            node.set_editor_property("NodePosX", int(x))
            node.set_editor_property("NodePosY", int(y))
            return True
    except Exception:
        pass
    try:
        if hasattr(node, "set_editor_property"):
            node.set_editor_property("node_pos_x", int(x))
            node.set_editor_property("node_pos_y", int(y))
            return True
    except Exception:
        pass
    return False


def layout_blueprint_nodes(bp_path):
    """
    Layout all nodes in the Blueprint's graphs in a grid. Returns dict with ok, node_count, graphs_updated, error.
    """
    if not unreal.EditorAssetLibrary.does_asset_exist(bp_path):
        return {"ok": False, "node_count": 0, "graphs_updated": 0, "error": "Asset not found: " + bp_path}

    bp = unreal.load_asset(bp_path)
    if not bp:
        return {"ok": False, "node_count": 0, "graphs_updated": 0, "error": "Could not load: " + bp_path}

    total_placed = 0
    graphs_updated = 0

    try:
        graphs = bp.get_editor_property("ubergraph_pages")
    except Exception:
        graphs = []

    if not graphs:
        return {"ok": True, "node_count": 0, "graphs_updated": 0, "error": None}

    for graph in graphs:
        try:
            nodes = graph.get_editor_property("nodes")
        except Exception:
            nodes = []
        if not nodes:
            continue

        # Sort by current position so we keep a rough left-to-right, top-to-bottom order
        def sort_key(n):
            try:
                x = n.get_editor_property("NodePosX") if hasattr(n, "get_editor_property") else 0
                y = n.get_editor_property("NodePosY") if hasattr(n, "get_editor_property") else 0
                return (y, x)
            except Exception:
                return (0, 0)

        try:
            nodes_sorted = sorted(nodes, key=sort_key)
        except Exception:
            nodes_sorted = list(nodes)

        for i, node in enumerate(nodes_sorted):
            row = i // NODES_PER_ROW
            col = i % NODES_PER_ROW
            x = ORIGIN_X + col * SPACING_X
            y = ORIGIN_Y + row * SPACING_Y
            if _set_node_position(node, x, y):
                total_placed += 1

        graphs_updated += 1

    if total_placed > 0:
        try:
            unreal.EditorAssetLibrary.save_loaded_asset(bp)
        except Exception as e:
            _log("Layout applied but save failed: %s" % e)

    return {"ok": True, "node_count": total_placed, "graphs_updated": graphs_updated, "error": None}


def main():
    proj = unreal.SystemLibrary.get_project_directory()
    saved = os.path.join(proj, "Saved")
    os.makedirs(saved, exist_ok=True)
    req_path = os.path.join(saved, "layout_blueprint_request.json")
    out_path = os.path.join(saved, "layout_blueprint_result.json")

    bp_path = DEFAULT_BP_PATH
    if os.path.exists(req_path):
        try:
            with open(req_path, "r", encoding="utf-8") as f:
                req = json.load(f)
            bp_path = req.get("path", bp_path)
        except Exception:
            pass

    result = layout_blueprint_nodes(bp_path)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    if result["ok"]:
        _log("Laid out %d nodes in %d graph(s) for %s" % (result["node_count"], result["graphs_updated"], bp_path))
    else:
        _log("Failed: %s" % result.get("error", "unknown"))


if __name__ == "__main__":
    main()

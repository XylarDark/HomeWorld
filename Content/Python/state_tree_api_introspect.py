# state_tree_api_introspect.py
# Run from Unreal Editor (Tools -> Execute Python Script or MCP execute_python_script).
# Introspects State Tree asset and Python API for graph-editing capability (Gap 2).
# Writes result to Saved/state_tree_api_check.json for research/automation gap documentation.
# See docs/AUTOMATION_GAPS.md Gap 2, docs/GAP_SOLUTIONS_RESEARCH.md.

import json
import os
import sys

try:
    import unreal
except ImportError:
    out = {"ok": False, "error": "Run inside Unreal Editor", "asset": None, "api": None}
    saved = os.path.join(os.getcwd(), "Saved")
    os.makedirs(saved, exist_ok=True)
    with open(os.path.join(saved, "state_tree_api_check.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print("state_tree_api_introspect: " + out["error"])
    sys.exit(1)

PREFIX = "state_tree_api_introspect:"
ST_PATH = "/Game/HomeWorld/AI/ST_FamilyGatherer"


def _log(msg: str, data: dict | None = None) -> None:
    text = PREFIX + " " + msg
    if data is not None:
        text += " " + json.dumps(data)
    unreal.log(text)
    print(text)


def _project_saved_dir() -> str:
    project_root = os.getcwd()
    if "Content" not in (os.listdir(project_root) or []):
        project_root = os.path.normpath(os.path.join(project_root, "..", ".."))
    saved = os.path.join(project_root, "Saved")
    os.makedirs(saved, exist_ok=True)
    return saved


def main() -> int:
    result = {
        "ok": True,
        "error": None,
        "asset_path": ST_PATH,
        "asset_exists": False,
        "asset_class": None,
        "asset_attrs": [],
        "asset_editor_properties": [],
        "unreal_state_tree_attrs": [],
        "can_edit_graph": None,
        "notes": [],
    }
    try:
        if not unreal.EditorAssetLibrary.does_asset_exist(ST_PATH):
            result["ok"] = False
            result["error"] = "ST_FamilyGatherer not found; create via create_state_tree_family_gatherer.py"
            result["notes"].append("Create ST_FamilyGatherer first, then re-run.")
            saved_dir = _project_saved_dir()
            with open(os.path.join(saved_dir, "state_tree_api_check.json"), "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
            _log("Asset missing", {"path": ST_PATH})
            return 1

        result["asset_exists"] = True
        st = unreal.EditorAssetLibrary.load_asset(ST_PATH)
        if not st:
            result["ok"] = False
            result["error"] = "load_asset returned None"
            saved_dir = _project_saved_dir()
            with open(os.path.join(saved_dir, "state_tree_api_check.json"), "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
            return 1

        result["asset_class"] = type(st).__name__
        # Public attributes (no __)
        result["asset_attrs"] = sorted([x for x in dir(st) if not x.startswith("_")])
        # Editor property names if available
        if hasattr(st, "get_editor_property_names"):
            try:
                result["asset_editor_properties"] = list(st.get_editor_property_names())
            except Exception as e:
                result["notes"].append("get_editor_property_names: " + str(e))
        # Check for graph-related names
        graph_like = [a for a in result["asset_attrs"] if any(
            k in a.lower() for k in ("state", "selector", "blackboard", "task", "condition", "child", "node")
        )]
        result["notes"].append("Graph-like attrs: " + str(graph_like))
        # Heuristic: do we see any API that could add states/children? (read-only check)
        result["can_edit_graph"] = bool(graph_like) and (
            "add" in " ".join(result["asset_attrs"]).lower()
            or "set_editor_property" in result["asset_attrs"]
        )

        # unreal module: StateTree, StateTreeState, etc.
        for name in ("StateTree", "StateTreeState", "StateTreeComponent", "StateTreeFactory"):
            if hasattr(unreal, name):
                result["unreal_state_tree_attrs"].append(name)
        if not result["unreal_state_tree_attrs"]:
            result["notes"].append("No StateTree* classes found in unreal module (plugin may be disabled).")

        saved_dir = _project_saved_dir()
        out_path = os.path.join(saved_dir, "state_tree_api_check.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        _log("Wrote " + out_path, {"can_edit_graph": result["can_edit_graph"], "attrs_count": len(result["asset_attrs"])})
        return 0
    except Exception as e:
        result["ok"] = False
        result["error"] = str(e)
        result["notes"].append("Exception: " + str(e))
        saved_dir = _project_saved_dir()
        with open(os.path.join(saved_dir, "state_tree_api_check.json"), "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        _log("Error", {"error": str(e)})
        return 1


if __name__ == "__main__":
    sys.exit(main())

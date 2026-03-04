# pcg_apply_manual_steps.py
# Optional: PyAutoGUI-based automation for PCG no-access steps (Get Landscape Data By Tag, mesh list, graph on volume, Generate).
# Run with Editor open and focused: py Content/Python/gui_automation/pcg_apply_manual_steps.py (from project root, host-side).
# Outputs: Saved/gui_automation_result.json. Reference PNGs in gui_automation/refs/ for image-based location.
# See docs/PCG_VARIABLES_NO_ACCESS.md and docs/FULL_AUTOMATION_RESEARCH.md §10.

import json
import os
import sys
import time

PREFIX = "pcg_apply_manual_steps:"

# Expected reference image names (optional; script skips steps when ref is missing)
REF_IMAGES = (
    "details_panel.png",
    "by_tag_selector.png",
    "tag_pcg_landscape.png",
    "mesh_list_region.png",
    "graph_dropdown.png",
    "generate_button.png",
)

# Step order for flow: name -> ref filename (or None for steps that don't need a ref)
STEPS = [
    ("focus_details", "details_panel.png"),
    ("set_by_tag", "by_tag_selector.png"),
    ("set_tag_name", "tag_pcg_landscape.png"),
    ("set_mesh_list", "mesh_list_region.png"),
    ("assign_graph", "graph_dropdown.png"),
    ("click_generate", "generate_button.png"),
]


def _log(msg: str, data: dict | None = None) -> None:
    parts = [PREFIX, msg]
    if data:
        parts.append(json.dumps(data))
    print(" ".join(parts))


def _project_saved_dir(project_root: str) -> str:
    saved = os.path.join(project_root, "Saved")
    os.makedirs(saved, exist_ok=True)
    return saved


def _refs_dir(project_root: str) -> str:
    return os.path.join(project_root, "Content", "Python", "gui_automation", "refs")


def _find_ref_path(refs_dir: str, filename: str) -> str | None:
    path = os.path.join(refs_dir, filename)
    return path if os.path.isfile(path) else None


def main() -> int:
    try:
        import pyautogui
    except ImportError:
        _log("PyAutoGUI not installed; pip install pyautogui. Manual steps: see docs/PCG_VARIABLES_NO_ACCESS.md")
        result = {"success": False, "error": "PyAutoGUI not installed", "path": "", "steps_done": []}
        project_root = os.getcwd()
        if "Content" not in os.listdir(project_root):
            project_root = os.path.normpath(os.path.join(project_root, "..", ".."))
        saved_dir = _project_saved_dir(project_root)
        with open(os.path.join(saved_dir, "gui_automation_result.json"), "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        return 1

    # Resolve project root and dirs
    project_root = os.getcwd()
    if "Content" not in os.listdir(project_root):
        project_root = os.path.normpath(os.path.join(project_root, "..", ".."))
    saved_dir = _project_saved_dir(project_root)
    refs_dir = _refs_dir(project_root)

    steps_done = []
    steps_skipped = []
    last_error = None
    confidence = 0.8

    for step_name, ref_file in STEPS:
        ref_path = _find_ref_path(refs_dir, ref_file)
        if not ref_path:
            steps_skipped.append(step_name)
            _log("skip (no ref)", {"step": step_name, "ref": ref_file})
            continue
        try:
            loc = pyautogui.locateOnScreen(ref_path, confidence=confidence)
            if loc is not None:
                x, y = pyautogui.center(loc)
                pyautogui.click(x, y)
                steps_done.append(step_name)
                _log("click", {"step": step_name, "at": [x, y]})
                time.sleep(0.5)
            else:
                last_error = f"locateOnScreen did not find {ref_file}"
                _log("not found", {"step": step_name, "ref": ref_file})
        except Exception as e:
            last_error = str(e)
            _log("error", {"step": step_name, "error": last_error})

    success = len(steps_done) > 0 and last_error is None
    if not steps_done and not steps_skipped:
        last_error = (
            "No reference images found in gui_automation/refs/. "
            "Add PNG screenshots per refs/README.md and re-run with Editor focused."
        )
        _log("no refs", {"refs_dir": refs_dir})

    result = {
        "success": success,
        "error": last_error,
        "path": os.path.join(saved_dir, "gui_automation_result.json"),
        "steps_done": steps_done,
        "steps_skipped": steps_skipped,
    }
    with open(os.path.join(saved_dir, "gui_automation_result.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    _log("done", {"success": success, "steps_done": len(steps_done), "steps_skipped": len(steps_skipped)})
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

# state_tree_apply_defend_branch.py
# Optional: PyAutoGUI-based automation for State Tree no-API steps (add Night? branch, Defend state, IsNight condition).
# Run with Editor open and focused: py Content/Python/gui_automation/state_tree_apply_defend_branch.py (from project root, host-side).
# Outputs: Saved/gui_automation_result.json. Reference PNGs in gui_automation/refs/state_tree/ for image-based location.
# See docs/AUTOMATION_GAPS.md (Gap 2) and docs/GAP_SOLUTIONS_RESEARCH.md.

import json
import os
import sys

PREFIX = "state_tree_apply_defend_branch:"

# Expected reference image names (optional; script skips steps when ref is missing)
REF_IMAGES = (
    "state_tree_editor.png",
    "add_selector_branch.png",
    "condition_is_night.png",
    "defend_task.png",
    "blackboard_is_night.png",
)

# Step order for flow: name -> ref filename
STEPS = [
    ("focus_state_tree", "state_tree_editor.png"),
    ("add_night_branch", "add_selector_branch.png"),
    ("set_condition_is_night", "condition_is_night.png"),
    ("add_defend_task", "defend_task.png"),
    ("set_blackboard_is_night", "blackboard_is_night.png"),
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
    return os.path.join(project_root, "Content", "Python", "gui_automation", "refs", "state_tree")


def main() -> int:
    try:
        import pyautogui
    except ImportError:
        _log("PyAutoGUI not installed; pip install pyautogui. Manual steps: see docs/AUTOMATION_GAPS.md and DAY12_ROLE_PROTECTOR.md")
        result = {"success": False, "error": "PyAutoGUI not installed", "path": "", "steps_done": []}
        project_root = os.getcwd()
        if "Content" not in os.listdir(project_root):
            project_root = os.path.normpath(os.path.join(project_root, "..", ".."))
        saved_dir = _project_saved_dir(project_root)
        with open(os.path.join(saved_dir, "gui_automation_result.json"), "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        return 1

    project_root = os.getcwd()
    if "Content" not in os.listdir(project_root):
        project_root = os.path.normpath(os.path.join(project_root, "..", ".."))
    saved_dir = _project_saved_dir(project_root)
    refs_dir = _refs_dir(project_root)
    os.makedirs(refs_dir, exist_ok=True)

    steps_done = []
    steps_skipped = []
    for step_name, ref_file in STEPS:
        ref_path = os.path.join(refs_dir, ref_file)
        if not os.path.isfile(ref_path):
            steps_skipped.append(step_name)
            _log("Skip (no ref): " + step_name, {"ref": ref_file})
            continue
        try:
            loc = pyautogui.locateOnScreen(ref_path, confidence=0.8)
            if loc:
                center = pyautogui.center(loc)
                pyautogui.click(center)
                steps_done.append(step_name)
                _log("Done: " + step_name)
            else:
                steps_skipped.append(step_name)
                _log("Ref not found on screen: " + ref_file)
        except Exception as e:
            steps_skipped.append(step_name)
            _log("Error at " + step_name + ": " + str(e))

    result = {
        "success": len(steps_done) > 0,
        "error": None,
        "path": saved_dir,
        "steps_done": steps_done,
        "steps_skipped": steps_skipped,
    }
    with open(os.path.join(saved_dir, "gui_automation_result.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    _log("Wrote gui_automation_result.json", result)
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())

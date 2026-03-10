# new_level_from_ui.py
# GUI automation: File -> New Level -> Empty Open World, then optionally Save As with path from config.
# Run with Editor focused: py Content/Python/gui_automation/new_level_from_ui.py (from project root, host-side).
# Outputs: Saved/gui_automation_result.json. Ref images: refs/new_level/*.png (see refs/new_level/README.md).
# See docs/MANUAL_EDITOR_TUTORIAL.md §7 and docs/REF_IMAGES_SETUP_TUTORIAL.md.

import json
import os
import sys
import time

PREFIX = "new_level_from_ui:"
CONFIDENCE = 0.8

STEPS = [
    ("file_menu", "file_menu.png"),
    ("new_level", "new_level.png"),
    ("empty_open_world", "empty_open_world.png"),
    ("save_as_dialog", "save_as_dialog.png"),
    ("path_field", "path_field.png"),
]


def _log(msg: str, data: dict | None = None) -> None:
    parts = [PREFIX, msg]
    if data:
        parts.append(json.dumps(data))
    print(" ".join(parts))


def _project_root() -> str:
    cwd = os.getcwd()
    if "Content" in os.listdir(cwd):
        return cwd
    parent = os.path.normpath(os.path.join(cwd, "..", ".."))
    if os.path.isdir(parent) and "Content" in os.listdir(parent):
        return parent
    return cwd


def _load_save_path(project_root: str) -> str:
    """Level path to type in Save As (e.g. Planetoid_Pride or /Game/HomeWorld/Maps/Planetoid_Pride)."""
    config_path = os.path.join(project_root, "Content", "Python", "planetoid_map_config.json")
    default = "Planetoid_Pride"
    if not os.path.isfile(config_path):
        return default
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        path = data.get("planetoid_level_path")
        if path:
            # Use last segment if full path (e.g. Planetoid_Pride)
            return path.split("/")[-1] if "/" in path else path
        return default
    except Exception:
        return default


def main() -> int:
    try:
        import pyautogui
    except ImportError:
        _log("PyAutoGUI not installed; pip install pyautogui.")
        _write_result(_project_root(), False, "PyAutoGUI not installed", [])
        return 1

    project_root = _project_root()
    saved_dir = os.path.join(project_root, "Saved")
    os.makedirs(saved_dir, exist_ok=True)
    refs_dir = os.path.join(project_root, "Content", "Python", "gui_automation", "refs", "new_level")
    steps_done = []
    steps_skipped = []
    last_error = None

    for step_name, ref_file in STEPS:
        ref_path = os.path.join(refs_dir, ref_file)
        if not os.path.isfile(ref_path):
            steps_skipped.append(step_name)
            _log("skip (no ref)", {"step": step_name, "ref": ref_file})
            continue
        try:
            loc = pyautogui.locateOnScreen(ref_path, confidence=CONFIDENCE)
            if loc is None:
                last_error = "Ref not found on screen: %s" % ref_file
                _log("not found", {"step": step_name})
                continue
            x, y = pyautogui.center(loc)
            pyautogui.click(x, y)
            steps_done.append(step_name)
            _log("click", {"step": step_name, "at": [x, y]})
            time.sleep(0.5)
            if step_name == "path_field":
                level_name = _load_save_path(project_root)
                time.sleep(0.2)
                pyautogui.hotkey("ctrl", "a")
                time.sleep(0.05)
                pyautogui.write(level_name, interval=0.02)
                time.sleep(0.2)
                pyautogui.press("enter")
                _log("typed path", {"value": level_name})
        except Exception as e:
            last_error = str(e)
            _log("error", {"step": step_name, "error": last_error})

    success = len(steps_done) > 0 and (last_error is None or "path_field" in steps_done)
    _write_result(project_root, success, last_error, steps_done, steps_skipped)
    _log("done", {"success": success, "steps_done": steps_done, "steps_skipped": steps_skipped})
    return 0 if success else 1


def _write_result(project_root: str, success: bool, error: str | None, steps_done: list, steps_skipped: list | None = None):
    saved_dir = os.path.join(project_root, "Saved")
    os.makedirs(saved_dir, exist_ok=True)
    result = {
        "success": success,
        "error": error,
        "path": os.path.join(saved_dir, "gui_automation_result.json"),
        "steps_done": steps_done,
        "steps_skipped": steps_skipped or [],
    }
    with open(os.path.join(saved_dir, "gui_automation_result.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    sys.exit(main())

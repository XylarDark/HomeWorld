# wbp_main_menu_from_ui.py
# GUI automation: create WBP_MainMenu, set parent HomeWorldMainMenuWidget, add layout/buttons and bindings.
# Run with Editor focused: py Content/Python/gui_automation/wbp_main_menu_from_ui.py (from project root, host-side).
# Outputs: Saved/gui_automation_result.json. Ref images: refs/wbp_main_menu/*.png (see refs/wbp_main_menu/README.md).
# See docs/MANUAL_EDITOR_TUTORIAL.md §4 and docs/REF_IMAGES_SETUP_TUTORIAL.md.
# Many steps; script skips any step whose ref is missing. Manual fallback: MANUAL_EDITOR_TUTORIAL §4.

import json
import os
import sys
import time

PREFIX = "wbp_main_menu_from_ui:"
CONFIDENCE = 0.8

# Order of steps; each step clicks the ref (and for bindings we might need to select a target - simplified: click only)
STEPS = [
    ("content_right_click", "content_right_click.png"),
    ("user_interface_menu", "user_interface_menu.png"),
    ("widget_blueprint_item", "widget_blueprint_item.png"),
    ("class_settings", "class_settings.png"),
    ("parent_class_dropdown", "parent_class_dropdown.png"),
    ("designer_canvas", "designer_canvas.png"),
    ("add_vertical_box", "add_vertical_box.png"),
    ("add_button", "add_button.png"),
    ("on_clicked_play", "on_clicked_play.png"),
    ("on_clicked_character", "on_clicked_character.png"),
    ("on_clicked_options", "on_clicked_options.png"),
    ("on_clicked_quit", "on_clicked_quit.png"),
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


def main() -> int:
    try:
        import pyautogui
    except ImportError:
        _log("PyAutoGUI not installed; pip install pyautogui.")
        _write_result(_project_root(), False, "PyAutoGUI not installed", [], [])
        return 1

    project_root = _project_root()
    saved_dir = os.path.join(project_root, "Saved")
    os.makedirs(saved_dir, exist_ok=True)
    refs_dir = os.path.join(project_root, "Content", "Python", "gui_automation", "refs", "wbp_main_menu")
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
        except Exception as e:
            last_error = str(e)
            _log("error", {"step": step_name, "error": last_error})

    success = len(steps_done) > 0
    _write_result(project_root, success, last_error, steps_done, steps_skipped)
    _log("done", {"success": success, "steps_done": steps_done, "steps_skipped": steps_skipped})
    return 0 if success else 1


def _write_result(project_root: str, success: bool, error: str | None, steps_done: list, steps_skipped: list):
    saved_dir = os.path.join(project_root, "Saved")
    os.makedirs(saved_dir, exist_ok=True)
    result = {
        "success": success,
        "error": error,
        "path": os.path.join(saved_dir, "gui_automation_result.json"),
        "steps_done": steps_done,
        "steps_skipped": steps_skipped,
    }
    with open(os.path.join(saved_dir, "gui_automation_result.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    sys.exit(main())

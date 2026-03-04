# set_portal_level_to_open.py
# GUI automation fallback for Gap 1 (AUTOMATION_GAPS): set "Level To Open" on portal actor in Details when Python set_editor_property fails.
# Prereq: Run place_portal_placeholder.py first; select the portal actor (tag Portal_To_Planetoid) in the level.
# Run with Editor open and focused: py Content/Python/gui_automation/set_portal_level_to_open.py (from project root, host-side).
# Outputs: Saved/gui_automation_result.json. Ref image: refs/portal/level_to_open_field.png (see refs/portal/README.md).

import json
import os
import sys
import time

PREFIX = "set_portal_level_to_open:"
REF_IMAGE = "level_to_open_field.png"
CONFIDENCE = 0.8


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


def _load_level_to_open(project_root: str) -> str:
    path = os.path.join(project_root, "Content", "Python", "planetoid_map_config.json")
    default = "Planetoid_Pride"
    if not os.path.isfile(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("portal_level_to_open") or default
    except Exception:
        return default


def main() -> int:
    try:
        import pyautogui
    except ImportError:
        _log("PyAutoGUI not installed; pip install pyautogui. See docs/AUTOMATION_GAPS.md Gap 1.")
        project_root = _project_root()
        saved = os.path.join(project_root, "Saved")
        os.makedirs(saved, exist_ok=True)
        result = {
            "success": False,
            "error": "PyAutoGUI not installed",
            "gap": "Gap 1 LevelToOpen",
            "path": os.path.join(saved, "gui_automation_result.json"),
        }
        with open(os.path.join(saved, "gui_automation_result.json"), "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        return 1

    project_root = _project_root()
    saved = os.path.join(project_root, "Saved")
    os.makedirs(saved, exist_ok=True)
    refs_portal = os.path.join(project_root, "Content", "Python", "gui_automation", "refs", "portal")
    ref_path = os.path.join(refs_portal, REF_IMAGE)
    if not os.path.isfile(ref_path):
        _log("Ref image missing; capture Details 'Level To Open' field and save as refs/portal/%s" % REF_IMAGE)
        result = {
            "success": False,
            "error": "Ref image required: refs/portal/%s. Select portal actor, open Details, capture the Level To Open field. See refs/portal/README.md." % REF_IMAGE,
            "gap": "Gap 1 LevelToOpen",
            "path": os.path.join(saved, "gui_automation_result.json"),
            "ref_path": ref_path,
        }
        with open(os.path.join(saved, "gui_automation_result.json"), "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        return 1

    level_to_open = _load_level_to_open(project_root)
    try:
        loc = pyautogui.locateOnScreen(ref_path, confidence=CONFIDENCE)
        if loc is None:
            _log("Ref not found on screen; ensure portal actor is selected and Details shows Dungeon | Level To Open.")
            result = {
                "success": False,
                "error": "Ref image not found on screen. Select portal (Portal_To_Planetoid) and ensure Details shows Level To Open.",
                "gap": "Gap 1 LevelToOpen",
                "path": os.path.join(saved, "gui_automation_result.json"),
            }
            with open(os.path.join(saved, "gui_automation_result.json"), "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
            return 1
        x, y = pyautogui.center(loc)
        pyautogui.click(x, y)
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.1)
        pyautogui.write(level_to_open, interval=0.02)
        time.sleep(0.2)
        pyautogui.press("enter")
        _log("Typed Level To Open", {"value": level_to_open, "at": [x, y]})
        result = {
            "success": True,
            "gap": "Gap 1 LevelToOpen",
            "level_to_open": level_to_open,
            "path": os.path.join(saved, "gui_automation_result.json"),
        }
        with open(os.path.join(saved, "gui_automation_result.json"), "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        return 0
    except Exception as e:
        _log("error", {"error": str(e)})
        result = {
            "success": False,
            "error": str(e),
            "gap": "Gap 1 LevelToOpen",
            "path": os.path.join(saved, "gui_automation_result.json"),
        }
        with open(os.path.join(saved, "gui_automation_result.json"), "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        return 1


if __name__ == "__main__":
    sys.exit(main())

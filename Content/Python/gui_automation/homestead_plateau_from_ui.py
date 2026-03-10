# homestead_plateau_from_ui.py
# Optional GUI automation: set Player Start Location in Details from config (when Python cannot set transform).
# Run with Editor focused: py Content/Python/gui_automation/homestead_plateau_from_ui.py (from project root, host-side).
# Outputs: Saved/gui_automation_result.json. Ref image: refs/homestead/location_field.png.
# Preferred: use place_homestead_spawn.py (config-driven, no refs). See refs/homestead/README.md and docs/REF_IMAGES_SETUP_TUTORIAL.md §4.8.

import json
import os
import sys
import time

PREFIX = "homestead_plateau_from_ui:"
CONFIDENCE = 0.8
REF_IMAGE = "location_field.png"


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


def _load_position(project_root: str) -> tuple[float, float, float]:
    path = os.path.join(project_root, "Content", "Python", "homestead_spawn_config.json")
    default = (0.0, 0.0, 500.0)
    if not os.path.isfile(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        x = float(data.get("location_x", 0))
        y = float(data.get("location_y", 0))
        z = float(data.get("location_z", 500))
        return (x, y, z)
    except Exception:
        return default


def main() -> int:
    try:
        import pyautogui
    except ImportError:
        _log("PyAutoGUI not installed; pip install pyautogui.")
        _write_result(_project_root(), False, "PyAutoGUI not installed")
        return 1

    project_root = _project_root()
    saved_dir = os.path.join(project_root, "Saved")
    os.makedirs(saved_dir, exist_ok=True)
    ref_path = os.path.join(project_root, "Content", "Python", "gui_automation", "refs", "homestead", REF_IMAGE)

    if not os.path.isfile(ref_path):
        _log("Ref image missing; capture refs/homestead/%s or use place_homestead_spawn.py" % REF_IMAGE)
        _write_result(project_root, False, "Ref image required: refs/homestead/" + REF_IMAGE)
        return 1

    x, y, z = _load_position(project_root)
    try:
        loc = pyautogui.locateOnScreen(ref_path, confidence=CONFIDENCE)
        if loc is None:
            _log("Ref not found on screen; select Player Start and ensure Details > Transform > Location is visible.")
            _write_result(project_root, False, "Ref not found on screen")
            return 1
        cx, cy = pyautogui.center(loc)
        pyautogui.click(cx, cy)
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.05)
        pyautogui.write(str(int(x)), interval=0.02)
        time.sleep(0.1)
        pyautogui.press("tab")
        pyautogui.write(str(int(y)), interval=0.02)
        time.sleep(0.1)
        pyautogui.press("tab")
        pyautogui.write(str(int(z)), interval=0.02)
        time.sleep(0.1)
        pyautogui.press("enter")
        _log("Set Location", {"x": x, "y": y, "z": z})
        _write_result(project_root, True, None, x, y, z)
        return 0
    except Exception as e:
        _log("error", {"error": str(e)})
        _write_result(project_root, False, str(e))
        return 1


def _write_result(project_root: str, success: bool, error: str | None, x: float = 0, y: float = 0, z: float = 0):
    saved_dir = os.path.join(project_root, "Saved")
    os.makedirs(saved_dir, exist_ok=True)
    result = {
        "success": success,
        "error": error,
        "path": os.path.join(saved_dir, "gui_automation_result.json"),
        "location": {"x": x, "y": y, "z": z} if success else None,
    }
    with open(os.path.join(saved_dir, "gui_automation_result.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    sys.exit(main())

# capture_editor_screenshot.py
# Host-side script: captures a screenshot of the screen (or foreground window) using PyAutoGUI.
# Run from project root: py Content/Python/capture_editor_screenshot.py
# Optional: pip install pyautogui (and Pillow). Outputs: Saved/screenshots/capture_<timestamp>.png,
# Saved/screenshot_result.json. See docs/FULL_AUTOMATION_RESEARCH.md (Implementation Phase 2).

import json
import os
import sys
import time
from typing import Optional

PREFIX = "capture_editor_screenshot:"


def _log(msg: str, data: Optional[dict] = None) -> None:
    parts = [PREFIX, msg]
    if data is not None:
        parts.append(json.dumps(data))
    print(" ".join(parts))


def _project_saved_dir() -> Optional[str]:
    """Resolve project root and return Saved directory path."""
    project_dir = os.environ.get("HOMEWORLD_PROJECT", "").strip() or os.getcwd()
    project_dir = os.path.abspath(project_dir)
    if not os.path.isdir(project_dir):
        return None
    saved = os.path.join(project_dir, "Saved")
    return saved


def main() -> int:
    _log("started")

    try:
        import pyautogui
    except ImportError:
        print("Install pyautogui for screenshot capture: pip install pyautogui")
        _log("completed", {"success": False, "error": "PyAutoGUI not installed"})
        return 1

    saved_dir = _project_saved_dir()
    if not saved_dir:
        result = {"success": False, "path": "", "error": "Project Saved dir not found"}
        out_path = os.path.join(os.getcwd(), "Saved", "screenshot_result.json")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        return 1

    screenshots_dir = os.path.join(saved_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    capture_path = os.path.join(screenshots_dir, f"capture_{timestamp}.png")

    time.sleep(2)
    try:
        img = pyautogui.screenshot()
        img.save(capture_path)
    except Exception as e:
        result = {"success": False, "path": "", "error": str(e)}
        result_path = os.path.join(saved_dir, "screenshot_result.json")
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        _log("completed", {"success": False, "error": result["error"]})
        return 1

    result = {"success": True, "path": capture_path, "error": None}
    result_path = os.path.join(saved_dir, "screenshot_result.json")
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    _log("completed", {"success": True, "path": capture_path})
    return 0


if __name__ == "__main__":
    sys.exit(main())

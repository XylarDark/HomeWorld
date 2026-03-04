# capture_portal_refs.py
# One-time (or after layout change): capture reference image for set_portal_level_to_open.py (Gap 1 GUI fallback).
# Run from project root: py Content/Python/gui_automation/capture_portal_refs.py [--auto]
# Requires: pip install pyautogui (Pillow used for crop in --auto).
# Saves: Content/Python/gui_automation/refs/portal/level_to_open_field.png
# See refs/portal/README.md. For best matching, crop the saved image to just the "Level To Open" field.

import os
import sys

REF_IMAGE = "level_to_open_field.png"
# In --auto we crop to right side (Details panel); width in pixels
DETAILS_CROP_WIDTH = 400


def _project_root():
    root = os.getcwd()
    if "Content" not in os.listdir(root):
        root = os.path.normpath(os.path.join(root, "..", ".."))
    return root


def _refs_portal_dir(root):
    return os.path.join(root, "Content", "Python", "gui_automation", "refs", "portal")


def main():
    try:
        import pyautogui
    except ImportError:
        print("PyAutoGUI not installed. Run: pip install pyautogui")
        return 1

    root = _project_root()
    refs_portal = _refs_portal_dir(root)
    os.makedirs(refs_portal, exist_ok=True)
    path = os.path.join(refs_portal, REF_IMAGE)

    auto = "--auto" in sys.argv
    if auto:
        screenshot = pyautogui.screenshot()
        w, h = screenshot.size
        # Crop to right DETAILS_CROP_WIDTH px (Details panel region)
        left = max(0, w - DETAILS_CROP_WIDTH)
        cropped = screenshot.crop((left, 0, w, h))
        cropped.save(path)
        print("capture_portal_refs: auto capture saved (right %d px) -> %s" % (DETAILS_CROP_WIDTH, path))
        print("For best PyAutoGUI matching, crop this image to just the 'Level To Open' field and replace.")
        return 0

    print("Ref image for set_portal_level_to_open.py (Gap 1)")
    print("1. Run place_portal_placeholder.py in the Editor (or via MCP).")
    print("2. In the Editor: select the portal actor (tag Portal_To_Planetoid).")
    print("3. In Details, expand Dungeon and ensure 'Level To Open' is visible.")
    print("4. Position the Editor so the Level To Open field (or its label) is visible.")
    print("Saving to: %s" % path)
    print("Captured image is full-screen; for best matching, crop to the Level To Open field and replace the file.\n")
    try:
        input("Press Enter to capture (or Ctrl+C to exit)...")
    except KeyboardInterrupt:
        print("Cancelled.")
        return 1
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        print("Saved: %s" % path)
    except Exception as e:
        print("Error: %s" % e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

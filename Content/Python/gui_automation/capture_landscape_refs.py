# capture_landscape_refs.py
# One-time: capture reference images for landscape_apply_basic.py (minimal: open Landscape, click Sculpt).
# Run from project root: py Content/Python/gui_automation/capture_landscape_refs.py
# Requires: pip install pyautogui
# Saves: Content/Python/gui_automation/refs/landscape/*.png
# Full terrain sculpting is manual; see refs/landscape/README.md and docs/MANUAL_EDITOR_TUTORIAL.md §8.

import os
import sys

REF_IMAGES = (
    ("landscape_mode.png", "Modes panel with 'Landscape' selected or Landscape mode indicator."),
    ("sculpt_tool.png", "Sculpt tool button or icon in Landscape toolbar."),
)


def _project_root():
    root = os.getcwd()
    if "Content" not in os.listdir(root):
        root = os.path.normpath(os.path.join(root, "..", ".."))
    return root


def _refs_dir(root):
    return os.path.join(root, "Content", "Python", "gui_automation", "refs", "landscape")


def main():
    try:
        import pyautogui
    except ImportError:
        print("PyAutoGUI not installed. Run: pip install pyautogui")
        return 1

    root = _project_root()
    refs_dir = _refs_dir(root)
    os.makedirs(refs_dir, exist_ok=True)
    print("Reference images for landscape_apply_basic.py (minimal: focus Landscape, Sculpt)")
    print("Open a level that has a Landscape (e.g. Planetoid_Pride). Full terrain = manual (MANUAL_EDITOR_TUTORIAL §8).\n")

    for i, (filename, description) in enumerate(REF_IMAGES, 1):
        path = os.path.join(refs_dir, filename)
        print("[%d/%d] %s" % (i, len(REF_IMAGES), filename))
        print("  %s" % description)
        print("  -> %s" % path)
        try:
            input("  Press Enter to capture (or Ctrl+C to exit)...")
        except KeyboardInterrupt:
            print("Cancelled.")
            return 1
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(path)
            print("  Saved.\n")
        except Exception as e:
            print("  Error: %s" % e)
            return 1

    print("All %d ref images saved. Optionally crop each to the relevant UI element." % len(REF_IMAGES))
    return 0


if __name__ == "__main__":
    sys.exit(main())

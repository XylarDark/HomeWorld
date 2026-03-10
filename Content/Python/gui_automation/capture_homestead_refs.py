# capture_homestead_refs.py
# One-time: capture reference image for homestead_plateau_from_ui.py (optional GUI to set spawn Location in Details).
# Run from project root: py Content/Python/gui_automation/capture_homestead_refs.py
# Requires: pip install pyautogui
# Saves: Content/Python/gui_automation/refs/homestead/location_field.png
# Preferred: use place_homestead_spawn.py (config-driven, no refs). See refs/homestead/README.md.

import os
import sys

REF_IMAGES = (
    ("location_field.png", "Details > Transform > Location (X, Y, Z). Player Start selected in Outliner."),
)


def _project_root():
    root = os.getcwd()
    if "Content" not in os.listdir(root):
        root = os.path.normpath(os.path.join(root, "..", ".."))
    return root


def _refs_dir(root):
    return os.path.join(root, "Content", "Python", "gui_automation", "refs", "homestead")


def main():
    try:
        import pyautogui
    except ImportError:
        print("PyAutoGUI not installed. Run: pip install pyautogui")
        return 1

    root = _project_root()
    refs_dir = _refs_dir(root)
    os.makedirs(refs_dir, exist_ok=True)
    print("Reference image for homestead_plateau_from_ui.py (optional)")
    print("Preferred: use place_homestead_spawn.py (no refs). Select Player Start, Details > Transform > Location visible.\n")

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

    print("Done. Optionally crop to the Location X field for typing coordinates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

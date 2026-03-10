# capture_new_level_refs.py
# One-time (or after layout/theme change): capture reference images for new_level_from_ui.py.
# Run from project root: py Content/Python/gui_automation/capture_new_level_refs.py
# Requires: pip install pyautogui
# Saves: Content/Python/gui_automation/refs/new_level/*.png
# See refs/new_level/README.md and docs/REF_IMAGES_SETUP_TUTORIAL.md.

import os
import sys

REF_IMAGES = (
    ("file_menu.png", "The 'File' menu (top-left) or its label. Editor focused, File menu closed."),
    ("new_level.png", "The 'New Level' menu item under File. File menu open."),
    ("empty_open_world.png", "The 'Empty Open World' option in the New Level submenu or dialog."),
    ("save_as_dialog.png", "Save As dialog (title or path area). After File -> Save As."),
    ("path_field.png", "The path/name field in Save As where we type the level path."),
)


def _project_root():
    root = os.getcwd()
    if "Content" not in os.listdir(root):
        root = os.path.normpath(os.path.join(root, "..", ".."))
    return root


def _refs_dir(root):
    return os.path.join(root, "Content", "Python", "gui_automation", "refs", "new_level")


def main():
    try:
        import pyautogui
    except ImportError:
        print("PyAutoGUI not installed. Run: pip install pyautogui")
        return 1

    root = _project_root()
    refs_dir = _refs_dir(root)
    os.makedirs(refs_dir, exist_ok=True)
    print("Reference images for new_level_from_ui.py (File -> New Level -> Empty Open World)")
    print("Save the current level first if needed, so New Level does not trigger a save prompt.\n")

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

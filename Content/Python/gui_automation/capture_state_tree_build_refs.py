# capture_state_tree_build_refs.py
# One-time (or after layout change): capture reference images for state_tree_apply_build_branch.py.
# Run from project root: py Content/Python/gui_automation/capture_state_tree_build_refs.py
# Requires: pip install pyautogui
# Saves: Content/Python/gui_automation/refs/state_tree_build/*.png
# See refs/state_tree_build/README.md and docs/REF_IMAGES_SETUP_TUTORIAL.md.

import os
import sys

REF_IMAGES = (
    ("state_tree_editor.png", "State Tree editor (graph or toolbar) with ST_FamilyGatherer open."),
    ("add_branch.png", "Control to add a new branch (Add State / Add Selector child)."),
    ("build_condition.png", "BUILD-related condition or 'has build order' blackboard key."),
    ("move_to_task.png", "Move To task in the task list (state selected, adding task)."),
    ("claim_smart_object.png", "Claim Smart Object task or SO_WallBuilder."),
    ("blackboard_build.png", "Blackboard key for build (TargetBuildOrder, CurrentJob)."),
)


def _project_root():
    root = os.getcwd()
    if "Content" not in os.listdir(root):
        root = os.path.normpath(os.path.join(root, "..", ".."))
    return root


def _refs_dir(root):
    return os.path.join(root, "Content", "Python", "gui_automation", "refs", "state_tree_build")


def main():
    try:
        import pyautogui
    except ImportError:
        print("PyAutoGUI not installed. Run: pip install pyautogui")
        return 1

    root = _project_root()
    refs_dir = _refs_dir(root)
    os.makedirs(refs_dir, exist_ok=True)
    print("Reference images for state_tree_apply_build_branch.py (BUILD branch)")
    print("Open ST_FamilyGatherer in the State Tree editor.\n")

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

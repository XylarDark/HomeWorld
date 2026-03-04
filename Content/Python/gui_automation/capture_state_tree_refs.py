# capture_state_tree_refs.py
# One-time (or after layout change): capture reference images for state_tree_apply_defend_branch.py (Gap 2 GUI automation).
# Run from project root: py Content/Python/gui_automation/capture_state_tree_refs.py [--auto]
# Requires: pip install pyautogui.
# Saves: Content/Python/gui_automation/refs/state_tree/*.png (see REF_IMAGES below).
# See refs/state_tree/README.md. For best matching, crop each saved image to the relevant UI element.

import os
import sys

# Must match state_tree_apply_defend_branch.py REF_IMAGES
REF_IMAGES = (
    ("state_tree_editor.png", "State Tree editor window (graph canvas or toolbar) with ST_FamilyGatherer open."),
    ("add_selector_branch.png", '"Add Selector" or equivalent control to add a new branch (root or node selected).'),
    ("condition_is_night.png", "Condition editor or Blackboard key 'IsNight' (Bool) when adding a condition to a branch."),
    ("defend_task.png", "Defend task or 'Move To' / combat task in the task list (state selected, adding a task)."),
    ("blackboard_is_night.png", "Blackboard panel showing IsNight key (State Tree Blackboard tab visible)."),
)


def _project_root():
    root = os.getcwd()
    if "Content" not in os.listdir(root):
        root = os.path.normpath(os.path.join(root, "..", ".."))
    return root


def _refs_state_tree_dir(root):
    return os.path.join(root, "Content", "Python", "gui_automation", "refs", "state_tree")


def main():
    try:
        import pyautogui
    except ImportError:
        print("PyAutoGUI not installed. Run: pip install pyautogui")
        return 1

    root = _project_root()
    refs_dir = _refs_state_tree_dir(root)
    os.makedirs(refs_dir, exist_ok=True)

    auto = "--auto" in sys.argv
    if auto:
        # Single screenshot as state_tree_editor.png; other refs require interactive capture.
        path = os.path.join(refs_dir, "state_tree_editor.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        print("capture_state_tree_refs: auto capture saved -> %s" % path)
        print("Other refs (add_selector_branch, condition_is_night, defend_task, blackboard_is_night)")
        print("require interactive run: py Content/Python/gui_automation/capture_state_tree_refs.py")
        return 0

    print("Reference images for state_tree_apply_defend_branch.py (Gap 2)")
    print("1. Open Editor and ST_FamilyGatherer in the State Tree editor.")
    print("2. For each ref below, position the Editor so the described region is visible, then press Enter.\n")

    for i, (filename, description) in enumerate(REF_IMAGES, 1):
        path = os.path.join(refs_dir, filename)
        print("[%d/%d] %s" % (i, len(REF_IMAGES), filename))
        print("     %s" % description)
        print("     -> %s" % path)
        try:
            input("     Press Enter to capture (or Ctrl+C to exit)...")
        except KeyboardInterrupt:
            print("Cancelled.")
            return 1
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(path)
            print("     Saved.\n")
        except Exception as e:
            print("     Error: %s" % e)
            return 1

    print("All %d ref images saved. Optionally crop each to the relevant UI element for better PyAutoGUI matching." % len(REF_IMAGES))
    return 0


if __name__ == "__main__":
    sys.exit(main())

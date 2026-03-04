# capture_pcg_refs.py
# One-time: capture reference images for pcg_apply_manual_steps.py (Editor-driven GUI automation).
# Run from project root with Editor in the correct state for each ref: py Content/Python/gui_automation/capture_pcg_refs.py
# Requires: pip install pyautogui
# Saves PNGs to Content/Python/gui_automation/refs/ with names matching pcg_apply_manual_steps.REF_IMAGES.
# See gui_automation/refs/README.md. After capture, optionally crop each image to the relevant UI element for better matching.

import os
import sys

# Names must match pcg_apply_manual_steps.REF_IMAGES
REF_IMAGES = [
    "details_panel.png",
    "by_tag_selector.png",
    "tag_pcg_landscape.png",
    "mesh_list_region.png",
    "graph_dropdown.png",
    "generate_button.png",
]

DESCRIPTIONS = [
    "Details panel visible (e.g. header or first row) with any asset selected",
    "Get Landscape Data node selected in ForestIsland_PCG, Details showing 'By Tag' option/dropdown",
    "Get Landscape Data node, tag name field or PCG_Landscape visible",
    "Static Mesh Spawner node selected, mesh list / Mesh Selector area visible in Details",
    "PCG Volume (PCG_Forest) selected in level, Graph dropdown visible in Details",
    "PCG Volume selected in level, Generate button visible in PCG section of Details",
]


def _project_root():
    root = os.getcwd()
    if "Content" not in os.listdir(root):
        root = os.path.normpath(os.path.join(root, "..", ".."))
    return root


def _refs_dir(root):
    return os.path.join(root, "Content", "Python", "gui_automation", "refs")


def main():
    try:
        import pyautogui
    except ImportError:
        print("PyAutoGUI not installed. Run: pip install pyautogui")
        return 1

    root = _project_root()
    refs_dir = _refs_dir(root)
    os.makedirs(refs_dir, exist_ok=True)
    print("Reference images will be saved to:", refs_dir)
    print("Ensure the Unreal Editor window is visible and in the correct state for each capture.")
    print("Captured images are full-screen; for better matching, crop each to the UI element and replace the file.\n")

    for i, (filename, desc) in enumerate(zip(REF_IMAGES, DESCRIPTIONS)):
        path = os.path.join(refs_dir, filename)
        print("[%d/%d] %s" % (i + 1, len(REF_IMAGES), filename))
        print("  Position the Editor so that: %s" % desc)
        try:
            input("  Press Enter to capture (or Ctrl+C to skip/exit)...")
        except KeyboardInterrupt:
            print("  Skipped.")
            continue
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(path)
            print("  Saved:", path)
        except Exception as e:
            print("  Error:", e)
        print()

    print("Done. Run pcg_apply_manual_steps.py with Editor focused to use these refs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

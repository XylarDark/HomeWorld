# capture_wbp_main_menu_refs.py
# One-time (or after layout/theme change): capture reference images for wbp_main_menu_from_ui.py.
# Run from project root: py Content/Python/gui_automation/capture_wbp_main_menu_refs.py
# Requires: pip install pyautogui
# Saves: Content/Python/gui_automation/refs/wbp_main_menu/*.png
# See refs/wbp_main_menu/README.md and docs/REF_IMAGES_SETUP_TUTORIAL.md.

import os
import sys

REF_IMAGES = (
    ("content_right_click.png", "Content Browser right-click context menu (right-click in UI folder)."),
    ("user_interface_menu.png", "'User Interface' submenu item in context menu."),
    ("widget_blueprint_item.png", "'Widget Blueprint' option under User Interface."),
    ("class_settings.png", "'Class Settings' in the widget editor (toolbar or panel)."),
    ("parent_class_dropdown.png", "Parent Class dropdown or 'HomeWorldMainMenuWidget' option."),
    ("designer_canvas.png", "Designer tab or Canvas Panel area."),
    ("add_vertical_box.png", "Palette 'Vertical Box' or add Vertical Box control."),
    ("add_button.png", "Palette 'Button' or add Button control."),
    ("on_clicked_play.png", "On Clicked binding for Play (or first button) in Details."),
    ("on_clicked_character.png", "On Character clicked (second button)."),
    ("on_clicked_options.png", "On Options clicked (third button)."),
    ("on_clicked_quit.png", "On Quit clicked (fourth button)."),
)


def _project_root():
    root = os.getcwd()
    if "Content" not in os.listdir(root):
        root = os.path.normpath(os.path.join(root, "..", ".."))
    return root


def _refs_dir(root):
    return os.path.join(root, "Content", "Python", "gui_automation", "refs", "wbp_main_menu")


def main():
    try:
        import pyautogui
    except ImportError:
        print("PyAutoGUI not installed. Run: pip install pyautogui")
        return 1

    root = _project_root()
    refs_dir = _refs_dir(root)
    os.makedirs(refs_dir, exist_ok=True)
    print("Reference images for wbp_main_menu_from_ui.py (WBP_MainMenu create, parent class, buttons)")
    print("Position Content Browser at Content -> HomeWorld -> UI; optionally open an existing widget for Class Settings/Designer refs.\n")

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

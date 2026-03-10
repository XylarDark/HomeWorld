# WBP_MainMenu — ref images for GUI automation

Used by [wbp_main_menu_from_ui.py](../../wbp_main_menu_from_ui.py) to automate creating the main menu widget, setting parent class, and adding four buttons with bindings. Many steps; capture refs for the steps you want to automate. Missing refs cause the script to skip those steps.

## Capture

From project root with the Editor focused and Content Browser at **Content → HomeWorld → UI**:

```text
py Content/Python/gui_automation/capture_wbp_main_menu_refs.py
```

Capture each ref when prompted. Optionally open an existing WBP_MainMenu for Class Settings / Designer refs. Crop each PNG to the relevant control.

## Ref images

| Filename | Description | When to capture |
|----------|-------------|-----------------|
| `content_right_click.png` | Content Browser right-click context menu (empty area in UI folder). | Right-click in Content Browser in UI folder. |
| `user_interface_menu.png` | "User Interface" submenu item. | With context menu open. |
| `widget_blueprint_item.png` | "Widget Blueprint" option under User Interface. | With User Interface submenu visible. |
| `class_settings.png` | "Class Settings" in the widget editor (toolbar or panel). | With a Widget Blueprint open. |
| `parent_class_dropdown.png` | Parent Class dropdown or "HomeWorldMainMenuWidget" option. | With Class Settings open. |
| `designer_canvas.png` | Designer tab or Canvas Panel area. | With widget open in Designer. |
| `add_vertical_box.png` | Palette "Vertical Box" or add Vertical Box control. | In Designer, Palette visible. |
| `add_button.png` | Palette "Button" or add Button control. | In Designer. |
| `on_clicked_play.png` | On Clicked binding for Play button (or first button). | With a button selected, Details → On Clicked. |
| `on_clicked_character.png` | On Character clicked (second button). | Same. |
| `on_clicked_options.png` | On Options clicked (third button). | Same. |
| `on_clicked_quit.png` | On Quit clicked (fourth button). | Same. |

If a ref is missing, the apply script skips that step. See [docs/REF_IMAGES_SETUP_TUTORIAL.md](../../../../docs/REF_IMAGES_SETUP_TUTORIAL.md) §4.6 and [MANUAL_EDITOR_TUTORIAL.md](../../../../docs/MANUAL_EDITOR_TUTORIAL.md) §4.

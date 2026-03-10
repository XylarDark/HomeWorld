# New Level (File → New Level → Empty Open World) — ref images

Used by [new_level_from_ui.py](../../new_level_from_ui.py) to automate: File → New Level → Empty Open World, then optionally File → Save As with a path from config.

## Capture

From project root with the Editor focused:

```text
py Content/Python/gui_automation/capture_new_level_refs.py
```

Capture each ref when prompted. Save the level first if needed so "New Level" does not trigger a save prompt. Crop each PNG to the relevant menu item or dialog element for better matching.

## Ref images

| Filename | Description | When to capture |
|----------|-------------|-----------------|
| `file_menu.png` | The "File" menu (top-left) or its label. | With Editor focused, File menu closed so we can open it. |
| `new_level.png` | The "New Level" menu item under File. | With File menu open, New Level visible. |
| `empty_open_world.png` | The "Empty Open World" option in the New Level submenu or dialog. | With New Level submenu/dialog visible. |
| `save_as_dialog.png` | Save As dialog (e.g. title or path area). | After creating a new level, File → Save As. |
| `path_field.png` | The path/name field in Save As where we type the level path. | With Save As dialog open; crop to the path field. |

If a ref is missing, the apply script skips that step. See [docs/REF_IMAGES_SETUP_TUTORIAL.md](../../../../docs/REF_IMAGES_SETUP_TUTORIAL.md) §4.5 and [MANUAL_EDITOR_TUTORIAL.md](../../../../docs/MANUAL_EDITOR_TUTORIAL.md) §7.

# Reference images for PCG GUI automation

The script `pcg_apply_manual_steps.py` uses image-based location (PyAutoGUI `locateOnScreen`) to click UI elements when Python/MCP cannot set PCG settings. Capture small, distinctive regions of the Unreal Editor UI and save them here as PNGs. Use a consistent resolution and DPI (e.g. 100% scale) so location works across runs.

## One-time: run capture script

From project root with the Editor visible, run: `py Content/Python/gui_automation/capture_pcg_refs.py`. For each ref image, position the Editor as prompted and press Enter to capture. Images are saved here with the names below. For better matching, optionally crop each saved image to the relevant UI element (e.g. just the Details header or the Generate button) and replace the file.

## Suggested images (optional; add any subset)

| Filename | Description | When to capture |
|----------|-------------|-----------------|
| `details_panel.png` | A small region of the Details panel (e.g. header or first row) so the script can focus the Editor Details. | With any asset selected and Details visible. |
| `by_tag_selector.png` | The "By Tag" option or dropdown in Get Landscape Data node Details. | With Get Landscape Data node selected in ForestIsland_PCG. |
| `tag_pcg_landscape.png` | The tag name field or "PCG_Landscape" text. | Same as above, after setting By Tag. |
| `mesh_list_region.png` | Static Mesh Spawner mesh selector / mesh list area in Details. | With a Static Mesh Spawner node selected. |
| `graph_dropdown.png` | The Graph dropdown on the PCG Volume in level Details. | With PCG Volume selected in the level. |
| `generate_button.png` | The Generate button in the PCG section of Details. | With PCG Volume selected in the level. |

If a ref is missing, the script skips that step and logs it. Add at least one ref and run from project root with the Editor focused: `py Content/Python/gui_automation/pcg_apply_manual_steps.py`.

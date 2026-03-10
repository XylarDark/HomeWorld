# Reference images for GUI automation

All GUI clicker scripts in `Content/Python/gui_automation/` find Editor UI elements by matching **reference PNGs** (PyAutoGUI `locateOnScreen`). Ref images live under this directory and **should be committed to the repo** so that anyone can run the clickers without capturing on their own machine.

## Quick links

- **Full setup (capture, crop, add to repo):** [docs/REF_IMAGES_SETUP_TUTORIAL.md](../../../../docs/REF_IMAGES_SETUP_TUTORIAL.md)
- **Policy (GUI default, manual fallback):** [docs/GUI_AUTOMATION_WHY_AND_WHEN.md](../../../../docs/GUI_AUTOMATION_WHY_AND_WHEN.md)
- **Manual steps when refs are missing or matching fails:** [docs/MANUAL_EDITOR_TUTORIAL.md](../../../../docs/MANUAL_EDITOR_TUTORIAL.md)

## Ref directories and scripts

| Feature | Ref directory | Capture script | Apply script |
|--------|----------------|----------------|--------------|
| Portal (Level To Open) | `portal/` | `capture_portal_refs.py` | `set_portal_level_to_open.py` |
| PCG (Forest / Planetoid) | *(this folder, root)* | `capture_pcg_refs.py` | `pcg_apply_manual_steps.py` |
| State Tree (Night?/Defend) | `state_tree/` | `capture_state_tree_refs.py` | `state_tree_apply_defend_branch.py` |
| State Tree (BUILD branch) | `state_tree_build/` | `capture_state_tree_build_refs.py` | `state_tree_apply_build_branch.py` |
| New Level (File → New Level) | `new_level/` | `capture_new_level_refs.py` | `new_level_from_ui.py` |
| Main menu (WBP_MainMenu) | `wbp_main_menu/` | `capture_wbp_main_menu_refs.py` | `wbp_main_menu_from_ui.py` |
| Landscape (minimal) | `landscape/` | `capture_landscape_refs.py` | `landscape_apply_basic.py` |
| Homestead spawn (Details) | `homestead/` | `capture_homestead_refs.py` | `homestead_plateau_from_ui.py` |

Run capture scripts **from the project root** with the Editor visible and in the state described in each ref's README. After capture, optionally crop each PNG to the relevant UI element, then **commit to the repo** (see tutorial §5).

---

## PCG refs (this folder — root under refs/)

The script `pcg_apply_manual_steps.py` uses image-based location to click UI elements when Python/MCP cannot set PCG settings. Use a consistent resolution and DPI (e.g. 100% scale) so location works across runs.

### One-time: run capture script

From project root with the Editor visible, run: `py Content/Python/gui_automation/capture_pcg_refs.py`. For each ref image, position the Editor as prompted and press Enter to capture. Images are saved here. For better matching, optionally crop each saved image to the relevant UI element and replace the file.

### Suggested images (optional; add any subset)

| Filename | Description | When to capture |
|----------|-------------|-----------------|
| `details_panel.png` | A small region of the Details panel (e.g. header or first row). | With any asset selected and Details visible. |
| `by_tag_selector.png` | The "By Tag" option or dropdown in Get Landscape Data node Details. | With Get Landscape Data node selected in ForestIsland_PCG. |
| `tag_pcg_landscape.png` | The tag name field or "PCG_Landscape" text. | Same as above, after setting By Tag. |
| `mesh_list_region.png` | Static Mesh Spawner mesh selector / mesh list area in Details. | With a Static Mesh Spawner node selected. |
| `graph_dropdown.png` | The Graph dropdown on the PCG Volume in level Details. | With PCG Volume selected in the level. |
| `generate_button.png` | The Generate button in the PCG section of Details. | With PCG Volume selected in the level. |

If a ref is missing, the script skips that step and logs it. Add at least one ref and run from project root with the Editor focused: `py Content/Python/gui_automation/pcg_apply_manual_steps.py`.

---

## Per-feature READMEs

- [portal/README.md](portal/README.md) — Portal Level To Open
- [state_tree/README.md](state_tree/README.md) — State Tree Defend branch
- [state_tree_build/README.md](state_tree_build/README.md) — State Tree BUILD branch
- [new_level/README.md](new_level/README.md) — File → New Level → Empty Open World
- [wbp_main_menu/README.md](wbp_main_menu/README.md) — WBP_MainMenu widget
- [landscape/README.md](landscape/README.md) — Landscape mode / Sculpt (minimal)
- [homestead/README.md](homestead/README.md) — Homestead spawn position (optional; prefer `place_homestead_spawn.py`)

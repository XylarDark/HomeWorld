# Portal Level To Open — ref images for GUI automation (Gap 1)

**Ref image not in repo.** The file `level_to_open_field.png` must be produced **host-side**: run [capture_portal_refs.py](../capture_portal_refs.py) with the Editor open, portal actor selected, and Details → Dungeon → Level To Open visible (see "Host-side requirement" and "Capture script" below).

When Python cannot set `LevelToOpen` on `AHomeWorldDungeonEntrance` (see [docs/AUTOMATION_GAPS.md](../../../../docs/AUTOMATION_GAPS.md) Gap 1), use the host-side script `set_portal_level_to_open.py` with a ref image.

## Flow

1. Run **place_portal_placeholder.py** in the Editor (or via MCP) so the portal actor exists on the level.
2. In the Editor: select the portal actor (tag **Portal_To_Planetoid**) in the Outliner or viewport.
3. In **Details**, expand the **Dungeon** category and locate the **Level To Open** field.
4. Run (host-side): `py Content/Python/gui_automation/set_portal_level_to_open.py` with the Editor window focused.

The script uses PyAutoGUI to find the ref image on screen, click the field, and type the level name from `planetoid_map_config.json` (`portal_level_to_open`).

## Ref image to capture

| Filename | Description | When to capture |
|----------|-------------|-----------------|
| `level_to_open_field.png` | The **Level To Open** text field (or its label) in Details under the Dungeon category, with the portal actor selected. | Select the portal actor; Details → Dungeon → Level To Open visible. Crop to a small distinctive region (e.g. the field or the "Level To Open" label). |

Save the PNG in this folder: `Content/Python/gui_automation/refs/portal/level_to_open_field.png`.

### Capture script

Run the dedicated capture script so the ref file exists:

- **Interactive:** From project root with the Editor visible and the portal selected (Details → Dungeon → Level To Open visible), run:
  `py Content/Python/gui_automation/capture_portal_refs.py`
  Then press Enter to capture the full screen. For best PyAutoGUI matching, crop the saved image to just the "Level To Open" field (or label) and replace `level_to_open_field.png`.

- **Auto (automation):** From project root with the Editor in the desired state (portal selected, Details visible), run:
  `py Content/Python/gui_automation/capture_portal_refs.py --auto`
  This saves a crop of the right 400 px of the screen (Details panel region). For best matching, crop that image to just the Level To Open field and replace the file.

If the ref is missing, `set_portal_level_to_open.py` writes `success: false` and instructs you to add the ref; see [refs/README.md](../README.md) for capture tips (consistent resolution, crop to element).

### Host-side requirement

Ref capture **must be run on the host** where the Unreal Editor is visible (portal actor selected, Details → Dungeon → Level To Open visible). The automation loop does not have PyAutoGUI or Editor focus. To produce the ref:

1. Install PyAutoGUI on the host: `pip install pyautogui`
2. Open the Editor, run `place_portal_placeholder.py` (or ensure the portal exists), select the portal in the Outliner or viewport.
3. In Details, expand **Dungeon** and ensure **Level To Open** is visible.
4. From project root run: `py Content/Python/gui_automation/capture_portal_refs.py --auto` (or without `--auto` for interactive capture).
5. Optionally crop the saved image to just the Level To Open field for best PyAutoGUI matching.

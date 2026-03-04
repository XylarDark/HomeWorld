# Reference images for State Tree GUI automation (Gap 2)

**Ref images not in repo.** The files below must be produced **host-side**: run [capture_state_tree_refs.py](../capture_state_tree_refs.py) with the Editor open and ST_FamilyGatherer open in the State Tree editor (see "Host-side requirement" and "Capture script" below).

The script `state_tree_apply_defend_branch.py` uses image-based location (PyAutoGUI `locateOnScreen`) to drive the State Tree editor when Python/MCP cannot edit the graph. Capture small, distinctive regions of the State Tree editor UI and save them here as PNGs. Use a consistent resolution and DPI (e.g. 100% scale) so location works across runs.

## Capture script (recommended)

From project root, with **Unreal Editor** open and **ST_FamilyGatherer** open in the State Tree editor:

- **Interactive (all 5 refs):**  
  `py Content/Python/gui_automation/capture_state_tree_refs.py`  
  For each ref, position the Editor so the described region is visible, then press Enter. Images are saved to this folder.

- **Auto (one ref):**  
  `py Content/Python/gui_automation/capture_state_tree_refs.py --auto`  
  Captures a full-screen screenshot as `state_tree_editor.png`. The other four refs require the interactive run above.

Requires: `pip install pyautogui`. Optionally crop each saved image to the relevant UI element for better PyAutoGUI matching.

## Ref images (used by state_tree_apply_defend_branch.py)

| Filename | Description | When to capture |
|----------|-------------|-----------------|
| `state_tree_editor.png` | State Tree editor window (e.g. graph canvas or toolbar). | With State Tree asset open in the editor. |
| `add_selector_branch.png` | "Add Selector" or equivalent to add a new branch. | With root or a node selected. |
| `condition_is_night.png` | Condition editor or Blackboard key "IsNight" (Bool). | When adding a condition to a branch. |
| `defend_task.png` | Defend task or "Move To" / combat task in the task list. | With a state selected and adding a task. |
| `blackboard_is_night.png` | Blackboard panel showing IsNight key. | With State Tree Blackboard tab visible. |

If a ref is missing, the script skips that step and logs it. See [docs/AUTOMATION_GAPS.md](../../../../docs/AUTOMATION_GAPS.md) (Gap 2) and [docs/tasks/DAY12_ROLE_PROTECTOR.md](../../../../docs/tasks/DAY12_ROLE_PROTECTOR.md) for the manual steps this automation aims to replicate.

### Host-side requirement

Ref capture **must be run on the host** where the Unreal Editor is visible with ST_FamilyGatherer open in the State Tree editor. The automation loop does not have PyAutoGUI or Editor focus. To produce the refs:

1. Install PyAutoGUI on the host: `pip install pyautogui`
2. Open the Editor and open **ST_FamilyGatherer** in the State Tree editor (`/Game/HomeWorld/AI/ST_FamilyGatherer`).
3. From project root run: `py Content/Python/gui_automation/capture_state_tree_refs.py --auto` for a single full-screen ref (`state_tree_editor.png`), or `py Content/Python/gui_automation/capture_state_tree_refs.py` (no `--auto`) for interactive capture of all five refs.
4. Optionally crop each saved image to the relevant UI element for best PyAutoGUI matching.

Once refs exist, `state_tree_apply_defend_branch.py` can run host-side; otherwise use the one-time manual steps in [AUTOMATION_GAPS.md](../../../../docs/AUTOMATION_GAPS.md) § Gap 2.

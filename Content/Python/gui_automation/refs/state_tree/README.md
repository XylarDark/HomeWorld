# Reference images for State Tree GUI automation

The script `state_tree_apply_defend_branch.py` uses image-based location (PyAutoGUI `locateOnScreen`) to drive the State Tree editor when Python/MCP cannot edit the graph. Capture small, distinctive regions of the State Tree editor UI and save them here as PNGs. Use a consistent resolution and DPI (e.g. 100% scale) so location works across runs.

## One-time: capture refs

With the Editor open and **ST_FamilyGatherer** (or target State Tree) open in the State Tree editor, capture the following regions (e.g. with a capture script or screenshot tool) and save as the filenames below. Optionally crop each image to the relevant UI element for better matching.

## Suggested images (optional; add any subset)

| Filename | Description | When to capture |
|----------|-------------|-----------------|
| `state_tree_editor.png` | State Tree editor window (e.g. graph canvas or toolbar). | With State Tree asset open in the editor. |
| `add_selector_branch.png` | "Add Selector" or equivalent to add a new branch. | With root or a node selected. |
| `condition_is_night.png` | Condition editor or Blackboard key "IsNight" (Bool). | When adding a condition to a branch. |
| `defend_task.png` | Defend task or "Move To" / combat task in the task list. | With a state selected and adding a task. |
| `blackboard_is_night.png` | Blackboard panel showing IsNight key. | With State Tree Blackboard tab visible. |

If a ref is missing, the script skips that step and logs it. See [docs/AUTOMATION_GAPS.md](../../../../docs/AUTOMATION_GAPS.md) (Gap 2) and [docs/tasks/DAY12_ROLE_PROTECTOR.md](../../../../docs/tasks/DAY12_ROLE_PROTECTOR.md) for the manual steps this automation aims to replicate.

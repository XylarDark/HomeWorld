# State Tree BUILD branch — ref images for GUI automation

Used by [state_tree_apply_build_branch.py](../../state_tree_apply_build_branch.py) to automate adding the BUILD branch to ST_FamilyGatherer (condition, Move To, Claim Smart Object, etc.). Capture refs with ST_FamilyGatherer open in the State Tree editor.

## Capture

From project root with **ST_FamilyGatherer** open in the State Tree editor:

```text
py Content/Python/gui_automation/capture_state_tree_build_refs.py
```

Position the Editor for each ref (add branch, BUILD condition, Move To task, Claim SO, etc.) and press Enter. Crop each PNG to the relevant element.

## Ref images

| Filename | Description | When to capture |
|----------|-------------|-----------------|
| `state_tree_editor.png` | State Tree editor (graph or toolbar). | With ST_FamilyGatherer open. |
| `add_branch.png` | Control to add a new branch (e.g. Add State, Add Selector child). | With root or a node selected. |
| `build_condition.png` | BUILD-related condition or "has build order" / blackboard key. | When adding condition to BUILD branch. |
| `move_to_task.png` | Move To task in the task list. | With a state selected, adding a task. |
| `claim_smart_object.png` | Claim Smart Object task or SO_WallBuilder. | Same. |
| `blackboard_build.png` | Blackboard key for build (e.g. TargetBuildOrder, CurrentJob). | With Blackboard tab visible. |

If a ref is missing, the script skips that step. See [docs/REF_IMAGES_SETUP_TUTORIAL.md](../../../../docs/REF_IMAGES_SETUP_TUTORIAL.md) §4.4 and [MANUAL_EDITOR_TUTORIAL.md](../../../../docs/MANUAL_EDITOR_TUTORIAL.md) §6.

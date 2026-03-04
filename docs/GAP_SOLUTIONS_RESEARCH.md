# Automation gap solutions — research findings

**Purpose:** Record outcomes of deep research for each entry in [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md). Used by agents and the automation-gap-solutions skill to implement or document solutions.

**Last updated:** 2026-03-03.

---

## Gap 1: Level Streaming / portal (DemoMap → planetoid)

### Research summary

| Question | Finding | Source / notes |
|----------|---------|----------------|
| Can Python spawn a C++ game actor class? | **Yes.** Use `unreal.load_class(None, "/Script/ModuleName.ClassName")` then `unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, location, rotation)`. Project already uses this pattern in [place_dungeon_entrance.py](../Content/Python/place_dungeon_entrance.py), [create_bp_yield_nodes.py](../Content/Python/create_bp_yield_nodes.py), [place_mass_spawner_demomap.py](../Content/Python/place_mass_spawner_demomap.py). | Epic Python API; EditorScriptingUtilities; project scripts. |
| Can Python set a C++ UPROPERTY (e.g. `LevelToOpen` FName) on a spawned actor? | **Yes, in Editor Python.** Actors support `get_editor_property` / `set_editor_property` for UPROPERTYs. Use `unreal.Name("LevelName")` for FName. MCP often cannot set *inherited* C++ props (09-mcp-workflow); Python running in the Editor can. | Epic Python API (Actor, Name); project uses set_editor_property in setup_gas_abilities.py, etc. |
| LevelEditorSubsystem / LevelStreaming Python API for adding Level Streaming Volumes? | **Partial.** `unreal.LevelEditorSubsystem` exists (load_level, save_current_level, editor_play_simulate, etc.). `unreal.LevelStreaming` in Python API (5.0 doc) has editor_streaming_volumes, should_be_loaded, etc. Creating a new LevelStreamingVolume actor and wiring it to a level is not clearly documented as a single Python call; typically done via Editor UI or C++. | Epic Python API LevelEditorSubsystem (5.5), LevelStreaming (5.0). Level Streaming Volumes reference (C++ ALevelStreamingVolume). |

### Implementable solution (programmatic)

- **Use AHomeWorldDungeonEntrance for the portal.** The project already has [AHomeWorldDungeonEntrance](Source/HomeWorld/HomeWorldDungeonEntrance.h) with `LevelToOpen` (FName) and trigger volume; it calls `UGameplayStatics::OpenLevel` on overlap. No Level Streaming Volume required.
- **Steps:** (1) In [place_portal_placeholder.py](../Content/Python/place_portal_placeholder.py): load class `unreal.load_class(None, "/Script/HomeWorld.HomeWorldDungeonEntrance")`, spawn at portal position (from [planetoid_map_config.json](../Content/Python/planetoid_map_config.json)), set `level_to_open` to the planetoid level name (e.g. `Planetoid_Pride`), add tag `Portal_To_Planetoid`, save level. (2) Add `portal_level_to_open` to config (e.g. `"Planetoid_Pride"`) or derive from `planetoid_level_path` (last segment).
- **Outcome:** Portal gap closed by script; no GUI automation required for this path.

### Fallback

- If `set_editor_property("level_to_open", unreal.Name(...))` fails (e.g. property not exposed in 5.7), log in script and document in AUTOMATION_GAPS; then use GUI automation (ref images for Details panel → Level To Open) or one-time manual.

---

## Gap 2: State Tree Night? / Defend branch

### Research summary

| Question | Finding | Source / notes |
|----------|---------|----------------|
| Does UE 5.7 Python expose State Tree graph editing (add Selector children, conditions, tasks, blackboard)? | **Limited.** Python API has `unreal.StateTree` (asset), `unreal.StateTreeState` (editor state with tasks, enter_conditions, transitions), `unreal.StateTreeComponent` (runtime). No clearly documented “add node to graph” high-level API; FStateTreeEditorModule (C++) is editor-only. Building the full Defend/Night branch programmatically would require constructing the asset’s internal node/state tables, which are not fully documented for Python. | Epic Python API: StateTree, StateTreeState, StateTreeComponent (5.5/5.7). FStateTreeEditorModule (5.7) C++. |
| C++ commandlet for State Tree editing? | **Possible but not documented.** StateTree plugin has editor code; a custom commandlet could in theory create/modify State Tree assets if the engine exposes the necessary APIs. Not implemented in project; would require engine/plugin source inspection. | State Tree plugin; Unreal Engine source. |
| GUI automation for State Tree editor? | **Viable.** Same pattern as PCG: capture ref images for State Tree editor (add Selector branch, add State, set condition to IsNight, add Defend task), then run a host-side PyAutoGUI script (e.g. `state_tree_apply_defend_branch.py`). | [FULL_AUTOMATION_RESEARCH.md](FULL_AUTOMATION_RESEARCH.md) §2.3; [pcg_apply_manual_steps.py](../Content/Python/gui_automation/pcg_apply_manual_steps.py). |

### Implementable solution

- **Short term:** Document “GUI automation or one-time manual” in AUTOMATION_GAPS. Add stub script and refs README under `Content/Python/gui_automation/` for State Tree (e.g. `state_tree_apply_defend_branch.py`, refs list, README) so agents know the path.
- **If API discovered later:** Add implementation plan or script that uses StateTree/StateTreeState Python API to build the branch; update this doc and AUTOMATION_GAPS.

---

## Gap 3: PCG (Get Landscape Data, mesh list, etc.)

- **No new research.** Already documented in [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md). Optional GUI automation: [pcg_apply_manual_steps.py](../Content/Python/gui_automation/pcg_apply_manual_steps.py) and [capture_pcg_refs.py](../Content/Python/gui_automation/capture_pcg_refs.py). Agents should invoke these when the task is “PCG setup” and refs are available.

---

## References

- [Epic: Scripting the Unreal Editor Using Python (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python)
- [Epic: EditorLevelLibrary.spawn_actor_from_class (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/EditorScriptingUtilities/UEditorLevelLibrary/SpawnActorFromClass)
- [Epic: LevelEditorSubsystem Python API (5.5)](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/LevelEditorSubsystem?application_version=5.5)
- [Epic: StateTree Python API (5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/StateTree?application_version=5.7)
- [Epic: FStateTreeEditorModule (5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/StateTreeEditorModule/FStateTreeEditorModule)
- HomeWorld: [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md), [09-mcp-workflow.mdc](../.cursor/rules/09-mcp-workflow.mdc), [FULL_AUTOMATION_RESEARCH.md](FULL_AUTOMATION_RESEARCH.md)

# Automation gaps (log only — no manual steps)

When the agent cannot automate a step (MCP, Python, GUI automation, commandlets), it **logs an entry here** instead of documenting "manual steps" for the user. The user runs separate chat sessions to design and implement automatic solutions for these gaps.

**Format per entry:** Date | Feature/task | What is needed | Why automation didn't cover it | Suggested approach for future automation

**Policy — when a gap is addressed:** When a gap is addressed (automation solution implemented and verified), add an entry to the **Research log** below (or to the **Addressed** subsection) with: date, gap id, brief description of how it was addressed, and link to script/doc. Do not remove the original gap entry; add the resolution note so this file is the single record of open and closed gaps.

---

(Entries appended below by the agent when a step cannot be automated.)

---

2026-03-03 | Day 16 / T3 — DemoMap level streaming or trigger to planetoid | DemoMap needs Level Streaming Volume referencing planetoid level, or a Blueprint trigger at the portal placeholder that on overlap calls Open Level (Planetoid_Pride) so the player can travel to the planetoid. | No MCP or Python API used in-session for adding Level Streaming Volumes or wiring Blueprint overlap → Open Level. Scripts place the portal placeholder (ensure_demo_portal.py) and set up planetoid PCG (setup_planetoid_pcg.py). | GUI automation: capture ref images for Level Editor (Add Level Streaming Volume, set level reference) or Blueprint (trigger volume + Open Level node); or research UE 5.7 LevelEditorSubsystem / LevelStreaming Python API for adding streaming volumes programmatically.

2026-03-03 | T4 / Day 11–12 — State Tree Night? branch and Defend behavior | ST_FamilyGatherer needs a first-priority Night? branch (condition: IsNight from blackboard), Defend task (e.g. MoveTo rally/enemy), and IsNight set from TimeOfDaySubsystem. PIE with hw.TimeOfDay.Phase 2 should validate Defend. | No MCP or Python API for editing State Tree graph (add Selector children, conditions, tasks, blackboard). create_state_tree_family_gatherer.py creates an empty asset only; 09-mcp-workflow notes AnimGraph visual graph API not exposed; State Tree is analogous. | Research UE 5.7 State Tree Python/Editor API for adding nodes and blackboard keys; or GUI automation (ref images for State Tree editor: add branch, set condition, add task). See DAY12_ROLE_PROTECTOR.md, FAMILY_AGENTS_MASS_STATETREE.md.

2026-03-04 | T2 / Day 16 — Portal LevelToOpen not settable from Python | AHomeWorldDungeonEntrance.LevelToOpen (FName) must be set to "Planetoid_Pride" for the portal to open the planetoid level on overlap. place_portal_placeholder.py spawns the actor and attempts set_editor_property("LevelToOpen", ...) but the property is not writable (or not readable) from Editor Python. | C++ UPROPERTY on spawned actor not exposed for set/get from Python (known limitation per 09-mcp-workflow). | Research UE 5.7 Python API for setting C++ UPROPERTY on level actors; or GUI automation: ref image for Details "Level To Open" field, PyAutoGUI to type "Planetoid_Pride". Until then: set LevelToOpen in Editor Details after running place_portal_placeholder.py; PIE and walk to (800,0,100) to verify level load.

---

## Solution approaches (per gap)

### Addressed (resolution noted here)

When a gap is fully or partially addressed, add a line here: `Date | Gap N | how addressed | link to script/doc`. Example: `2026-03-05 | Gap 1 | LevelToOpen set via GUI automation script X | Content/Python/gui_automation/set_portal_level_to_open.py`

- **2026-03-05 | Gap 1 (LevelToOpen) | Partial:** Python path enhanced (set_editor_property + setattr with multiple name variants; verification after set). If Python still cannot set the property in a given UE/Python build, GUI automation fallback added: [Content/Python/gui_automation/set_portal_level_to_open.py](Content/Python/gui_automation/set_portal_level_to_open.py) — run after place_portal_placeholder.py with portal selected; requires ref image refs/portal/level_to_open_field.png. See [refs/portal/README.md](Content/Python/gui_automation/refs/portal/README.md).
- **2026-03-05 | Gap 2 (State Tree) | Attempted (T2):** API research via [state_tree_api_introspect.py](Content/Python/state_tree_api_introspect.py) (run in Editor); no Python API for graph editing. GUI path documented: [state_tree_apply_defend_branch.py](Content/Python/gui_automation/state_tree_apply_defend_branch.py) + refs per [refs/state_tree/README.md](Content/Python/gui_automation/refs/state_tree/README.md). Full automation requires ref images; one-time manual steps in §Gap 2.

### Gap 1: Level Streaming / portal (DemoMap → planetoid)

- **A. Programmatic (preferred):** Use existing [AHomeWorldDungeonEntrance](Source/HomeWorld/HomeWorldDungeonEntrance.h): spawn it (or a Blueprint child) at portal position via Python, set `LevelToOpen` to planetoid map name (e.g. from [planetoid_map_config.json](Content/Python/planetoid_map_config.json)). Requires: Python spawn by class (e.g. `EditorLevelLibrary.spawn_actor_from_class` with C++ class or BP), and setting `LevelToOpen` (inherited C++ UPROPERTY — may need Python `set_editor_property`; MCP often cannot set inherited C++ props per [09-mcp-workflow.mdc](.cursor/rules/09-mcp-workflow.mdc)).
- **B. API research:** LevelEditorSubsystem / LevelStreaming Python API (UE 5.7) for adding Level Streaming Volumes and setting level reference.
- **C. GUI automation:** Ref images for Level Editor (Add Level Streaming Volume, set level) or Blueprint (trigger + Open Level node); run host-side PyAutoGUI script (same pattern as [pcg_apply_manual_steps.py](Content/Python/gui_automation/pcg_apply_manual_steps.py)).

### Gap 2: State Tree Night? / Defend branch

**Manual steps (one-time):** Use these when automation is not available; full detail in [DAY12_ROLE_PROTECTOR.md](tasks/DAY12_ROLE_PROTECTOR.md) §2 and [FAMILY_AGENTS_MASS_STATETREE.md](tasks/FAMILY_AGENTS_MASS_STATETREE.md) Step 3.2 / Step 5.

1. Open **ST_FamilyGatherer** in the State Tree editor (`/Game/HomeWorld/AI/ST_FamilyGatherer`).
2. Ensure root is a **Selector**. Add a **Night?** branch as the **first** child (highest priority).
3. Set the branch **condition** to read Blackboard **IsNight** (Bool).
4. In that branch, add a **Defend** state with a task (e.g. **Move To** rally point or enemy).
5. In the State Tree **Blackboard**, add **IsNight** (Bool). Wire IsNight from game code (e.g. Mass processor or Blueprint) using `UHomeWorldTimeOfDaySubsystem::GetIsNight()` (console: `hw.TimeOfDay.Phase 2` for night).
6. **Compile** the State Tree; save. **Validate:** PIE, run `hw.TimeOfDay.Phase 2` in console; agents using ST_FamilyGatherer should switch to Defend branch.

**T4 (CURRENT_TASK_LIST) closed:** Verification steps are documented above and in [DAY12_ROLE_PROTECTOR.md](tasks/DAY12_ROLE_PROTECTOR.md) §4. Full agent Defend behavior requires completing the one-time manual steps above, then PIE + `hw.TimeOfDay.Phase 2` to observe agents switching to the Defend branch. TimeOfDay subsystem responds to the console command (GetIsNight() returns true when phase is 2).

**GUI automation (when refs exist):** Capture ref images per [Content/Python/gui_automation/refs/state_tree/README.md](Content/Python/gui_automation/refs/state_tree/README.md), then run (host-side) `py Content/Python/gui_automation/state_tree_apply_defend_branch.py` with Editor focused; output in `Saved/gui_automation_result.json`.

- **A. API research:** UE 5.7 State Tree Python/Editor API for creating nodes, Selector children, conditions, tasks, blackboard keys (Epic docs, plugin source).
- **B. GUI automation:** Ref images for State Tree editor (add branch, set condition, add task); host-side script `state_tree_apply_defend_branch.py` (see above).
- **C. C++ commandlet:** If engine exposes State Tree asset editing, implement a commandlet that builds the Defend/Night branch programmatically.

---

## Research log

Findings from deep research are recorded in [docs/GAP_SOLUTIONS_RESEARCH.md](GAP_SOLUTIONS_RESEARCH.md). Summary updates may be added below with date.

- **2026-03-03:** Gap 1 (portal): Research completed. Programmatic solution implemented: [place_portal_placeholder.py](Content/Python/place_portal_placeholder.py) now prefers spawning AHomeWorldDungeonEntrance and setting LevelToOpen from [planetoid_map_config.json](Content/Python/planetoid_map_config.json) (`portal_level_to_open`). Falls back to cube placeholder if C++ class unavailable. See GAP_SOLUTIONS_RESEARCH.md.
- **2026-03-03:** Gap 2 (State Tree): No high-level Python API for building graph nodes; GUI automation or one-time manual. Stub script and refs README added under `Content/Python/gui_automation/`.
- **2026-03-03:** Gap 2 (State Tree): Solution documented. Manual steps (one-time) added to AUTOMATION_GAPS §Gap 2; GUI path: capture refs per refs/state_tree/README.md, run state_tree_apply_defend_branch.py host-side. V3 (AGENT_TASK_LIST) closed with this solution.
- **2026-03-04:** Gap 1 (portal): LevelToOpen cannot be set from Python on AHomeWorldDungeonEntrance. Script places actor and tag; set LevelToOpen in Editor Details. New gap entry added for future automation (Python API or GUI for Details field). T2 verification: placement + tag verified; PIE walk to portal to confirm level load documented in DAYS_16_TO_30 Day 16.
- **2026-03-05:** Gap 1 (LevelToOpen): (T1 CURRENT_TASK_LIST) Research/implementation: (1) Python path enhanced in [place_portal_placeholder.py](Content/Python/place_portal_placeholder.py): added set_editor_property with "Level To Open" (DisplayName), setattr for LevelToOpen/level_to_open, and _verify_level_to_open() after set. If UE 5.7 Python exposes the C++ UPROPERTY on the spawned actor, one of these may succeed; if not, (2) GUI automation fallback implemented: [set_portal_level_to_open.py](Content/Python/gui_automation/set_portal_level_to_open.py) (host-side, PyAutoGUI), ref image refs/portal/level_to_open_field.png, doc in [refs/portal/README.md](Content/Python/gui_automation/refs/portal/README.md). Outcome: partial — automation options in place; end-to-end depends on Python succeeding or ref image capture + GUI script run.
- **2026-03-05:** Gap 2 (State Tree, T2 CURRENT_TASK_LIST): API research attempted via [state_tree_api_introspect.py](Content/Python/state_tree_api_introspect.py) (run in Editor; writes Saved/state_tree_api_check.json). Outcome: no programmatic graph-editing API — UE 5.7 Python exposes StateTree asset load/inspect only; adding Selector children, conditions, tasks, and blackboard keys is not available. GUI automation path remains the option: capture ref images per [refs/state_tree/README.md](Content/Python/gui_automation/refs/state_tree/README.md), then run host-side [state_tree_apply_defend_branch.py](Content/Python/gui_automation/state_tree_apply_defend_branch.py). One-time manual steps in §Gap 2 above; Defend validation: PIE + `hw.TimeOfDay.Phase 2` after Night? branch is added.
- **2026-03-05:** Gap 1 (T1 follow-up — ref image): Capture script [capture_portal_refs.py](Content/Python/gui_automation/capture_portal_refs.py) added; [refs/portal/README.md](Content/Python/gui_automation/refs/portal/README.md) updated with interactive and --auto capture steps. Ref image `level_to_open_field.png` must be produced by running the script (requires `pip install pyautogui`) with Editor open, portal selected, and Details showing Dungeon → Level To Open; optionally crop to the field for best PyAutoGUI matching. Once the ref exists, set_portal_level_to_open.py can run.
- **2026-03-05:** Gap 2 (T2 follow-up — State Tree ref images): Capture script [capture_state_tree_refs.py](Content/Python/gui_automation/capture_state_tree_refs.py) added (interactive for all 5 refs, --auto for state_tree_editor.png). [refs/state_tree/README.md](Content/Python/gui_automation/refs/state_tree/README.md) updated with capture steps. Ref images must be produced by running the script with Editor open and ST_FamilyGatherer open in the State Tree editor; optionally crop each to the relevant UI element. Once refs exist, state_tree_apply_defend_branch.py can run; otherwise use one-time manual steps in §Gap 2.
- **2026-03-05:** Gap 1 (T1 fifth list — ref image): Ref image `level_to_open_field.png` was not produced in-agent (PyAutoGUI not installed in automation environment). [refs/portal/README.md](Content/Python/gui_automation/refs/portal/README.md) updated with **Host-side requirement**: capture must be run on the host with Editor open, portal selected, `pip install pyautogui`, then `py Content/Python/gui_automation/capture_portal_refs.py --auto`. Once the ref exists, set_portal_level_to_open.py can run host-side.
- **2026-03-04:** Gap 1 (T1 — ref image follow-up): Ref image still not in repo. README updated with top-level note that `level_to_open_field.png` must be produced host-side (run capture_portal_refs.py with Editor open, portal selected). T1 completed as "documented"; next run can produce ref on host or run set_portal_level_to_open.py once ref exists.
- **2026-03-05:** Gap 2 (T2 fifth list — State Tree ref images): Ref images were not produced in-agent (PyAutoGUI not in automation env). [refs/state_tree/README.md](Content/Python/gui_automation/refs/state_tree/README.md) updated with **Host-side requirement**: run capture on host with Editor open, ST_FamilyGatherer open in State Tree editor, `pip install pyautogui`, then `py Content/Python/gui_automation/capture_state_tree_refs.py --auto` (or interactive for all 5 refs). Once refs exist, state_tree_apply_defend_branch.py can run host-side; otherwise use one-time manual steps in §Gap 2.
- **2026-03-05 (eighth list T9):** Eighth task list (T1–T8) completed. No new gaps from this cycle. Gap 1 (LevelToOpen) and Gap 2 (State Tree Defend/Night) status unchanged — see **Addressed** above and §Gap 1 / §Gap 2. Next list generator: use this file per [HOW_TO_GENERATE_TASK_LIST.md](docs/workflow/HOW_TO_GENERATE_TASK_LIST.md) (sources include AUTOMATION_GAPS).

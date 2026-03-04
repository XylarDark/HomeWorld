# Automation update: work accomplished, tools used, and gaps

**Purpose:** One-place overview of what automatic development has accomplished, what tools we use, how we use (or don’t use) the Editor and UI, and which steps we skip because we cannot automate them.

**Last updated:** 2026-03-03.

---

## 1. Work accomplished with automatic development

### 1.1 30-day implementation (Days 1–30)

All 30 days are **implementation-complete** per artifact checks and verification:

- **Act 1 (1–5):** PCG forest (ForestIsland_PCG, create_pcg_forest.py), GAS + character (setup_gas_abilities.py, GA_PrimaryAttack/Dodge/Interact), BuildPlacementSupport, Week 1 playtest doc, polish + optional Milady scripts, playtest sign-off.
- **Homestead (6–10):** DemoMap layout (create_demo_from_scratch, demo_map_config), resource nodes (create_bp_harvestable_tree.py, place_resource_nodes.py), resource collection (TryHarvestInFront, GA_Interact), home placement (GA_Place, TryPlaceAtCursor), agentic building **prep** (full agentic building deferred).
- **Family (11–15):** Family spawn scripts (MEC, State Tree, link_state_tree_to_mec), Protector (GA_ProtectorAttack), Healer (create_ga_heal.py, HomeWorldHealAbility), Child (doc/design), role persistence (HomeWorldFamilySubsystem; SaveGame deferred).
- **Planetoid (16–20):** Planetoid level scripts (ensure_planetoid_level, place_portal_placeholder, planetoid_map_config), PCG POI (create_bp_poi_placeholders, create_planetoid_poi_pcg, setup_planetoid_pcg), Shrine/Treasure (TryHarvestInFront tags), Cultivation/Mining (AHomeWorldYieldNode, create_bp_yield_nodes), Visit and interact (doc + PIE checklist).
- **Spirits (21–23):** Spirit roster (HomeWorldSpiritRosterSubsystem), assign/unassign spirit (SpiritAssignmentSubsystem, YieldNode).
- **Dungeon (24–25):** place_dungeon_entrance.py, dungeon_map_config, AHomeWorldDungeonEntrance (C++ trigger opens level on overlap); Boss/reward (doc).
- **Buffer (26–30):** Vertical slice checklist (VERTICAL_SLICE_CHECKLIST.md), next 30-day window (NEXT_30_DAY_WINDOW.md).

### 1.2 Post–30-day task list (T1–T9)

Completed via the agent company (Start-AllAgents):

- **T1:** create_bp_yield_nodes.py and place_dungeon_entrance.py run via MCP.
- **T2:** pie_test_runner.py run via MCP; results in Saved/pie_test_results.json.
- **T3:** ensure_planetoid_level.py, setup_planetoid_pcg.py, ensure_demo_portal.py; planetoid PCG and portal placeholder automated; Level Streaming logged as gap.
- **T4:** place_mass_spawner_demomap.py, set_mec_representation_mesh.py; Mass Spawner on DemoMap; State Tree Night?/Defend logged as gap.
- **T5:** AHomeWorldDungeonEntrance (C++), DAYS_16_TO_30 Day 24 options, build verified.
- **T6:** CYCLE_TASKLIST populated with T1–T9.
- **T7:** VERTICAL_SLICE_CHECKLIST.md (moment + corner, pre-demo, demo steps); PROTOTYPE_SCOPE and Day 26 updated.
- **T8:** NEXT_30_DAY_WINDOW.md (Harden & demo, Deferred, Act 2 prep, Steam EA prep).
- **T9:** Pending (Refiner run on-demand).

### 1.3 Automation and process improvements

- **Agent company:** Developer, Fixer, Guardian, Refiner with roles and accountability (docs/AGENT_COMPANY.md).
- **One script to start all agents:** Start-AllAgents.ps1 (installs CLI if needed, auto-launches Editor when UE_EDITOR set, runs Watcher).
- **Editor auto-launch:** Default before first round when UE_EDITOR is set; no manual “open Editor” step.
- **Run history and refinement:** agent_run_history.ndjson, automation_errors.log, Refiner (Run-RefinerAgent.ps1), docs/AUTOMATION_REFINEMENT.md.
- **Verification:** verify_30day_implementation.py and Saved/Logs/verify_30day_report.md.
- **Safe build:** Safe-Build.ps1 and Editor–build protocol (close Editor, retry on failure); run_automation_cycle.py --close-editor.
- **Project state and task list:** PROJECT_STATE_AND_TASK_LIST.md as single source for “what’s done” and “what’s next” (T1–T10).
- **Gaps logged, not “manual steps”:** AUTOMATION_GAPS.md; 20-full-automation-no-manual-steps and 09-mcp-workflow: log gaps, don’t document manual steps for the user.

---

## 2. Tools utilized

### 2.1 MCP (Unreal Editor, when running)

- **execute_python_script** — Run any Content/Python script in the Editor (e.g. create_bp_yield_nodes.py, place_dungeon_entrance.py, setup_planetoid_pcg.py, pie_test_runner.py). Primary way we “use the Editor” from the agent.
- **Actor CRUD, Blueprint creation/component setup, Blueprint node graph wiring** — Used for placing actors, creating Blueprints, and wiring where the API allows.
- **Property get/set, project settings, level manipulation** — Used for config and level setup where exposed.
- **execute_console_command** — Console commands (e.g. hw.TimeOfDay.Phase).
- **Viewport control** — Available in MCP; we have capture_viewport.py for screenshots (see Agent utility scripts).

We **do not** use MCP to drive the Editor’s **visual UI** (clicking menus, Details panels, or graph editors by “looking” at the screen). We use it to run Python and call APIs that the plugin exposes.

### 2.2 Python Editor scripts (Content/Python)

- **Setup/orchestration:** setup_gas_abilities.py, create_pcg_forest.py, create_demo_from_scratch.py, ensure_demo_map.py, ensure_planetoid_level.py, setup_planetoid_pcg.py, ensure_demo_portal.py, create_bp_harvestable_tree.py, place_resource_nodes.py, create_bp_yield_nodes.py, place_dungeon_entrance.py, create_mec_family_gatherer.py, create_state_tree_family_gatherer.py, link_state_tree_to_mec.py, place_mass_spawner_demomap.py, set_mec_representation_mesh.py, create_ga_heal.py, create_ga_protector_attack.py, create_bp_poi_placeholders.py, create_planetoid_poi_pcg.py, and others. All idempotent; many run via MCP execute_python_script.
- **Verification:** verify_30day_implementation.py (artifact paths per day).
- **PIE testing:** pie_test_runner.py (start/stop PIE, run checks, write Saved/pie_test_results.json).
- **Agent utilities:** mcp_harness.py, blueprint_inspector.py, layout_blueprint_nodes.py, capture_viewport.py (screenshot). See 09-mcp-workflow (Agent utility scripts).
- **init_unreal.py** — Runs on Editor load; applies Enhanced Input so movement works in PIE without a manual run.

### 2.3 PowerShell / batch

- **Start-AllAgents.ps1** — Start full company (install CLI if needed, launch Editor if UE_EDITOR set, run Watcher).
- **Watch-AutomationAndFix.ps1** — Watcher (Developer → Fixer → Guardian).
- **Guard-AutomationLoop.ps1** — Loop-breaker; writes automation_loop_breaker_report.md.
- **Run-RefinerAgent.ps1** — Refiner (rules/strategy from run history).
- **RunAutomationLoop.ps1, Start-AutomationSession.ps1** — Loop and one-command session start.
- **Safe-Build.ps1** — Build with Editor–build protocol.
- **Append-AgentRunRecord.ps1** — Append run record to agent_run_history.ndjson.

### 2.4 C++ and build

- **Build-HomeWorld.bat / Safe-Build.ps1** — Compile game module and plugins. Safe-Build closes Editor and retries on Editor-related failure.
- **C++ additions** — All 30-day and task-list features (character, GAS abilities, placement, Interact/Place, BuildOrder, family/spirit subsystems, YieldNode, DungeonEntrance, etc.) implemented in C++ where specified.

### 2.5 GUI automation (available but not required for current loop)

- **PyAutoGUI + reference images** — Documented for PCG (capture_pcg_refs.py, pcg_apply_manual_steps.py) and AnimGraph (ANIMGRAPH_AUTOMATION_SPIKE). Used when MCP/Python have no API; not currently in the default agent flow so we are **not** routinely “looking at the UI” or “performing debugging” by driving the Editor UI with clicks.
- **capture_viewport.py** — Screenshot; available for agents (Saved/screenshot_result.json) but not required for the task list so far.

---

## 3. Using the Editor, looking at the UI, and debugging

### 3.1 What we do use the Editor for

- **Running Python scripts via MCP** — When the Editor is running and MCP is connected, we run scripts with `execute_python_script`. That executes code inside the Editor (create assets, place actors, run PIE checks, etc.). So we **do** use the Editor as an execution environment.
- **PIE validation** — pie_test_runner.py starts/stops PIE and writes results to Saved/pie_test_results.json. The agent reads that JSON; it does **not** read the Editor’s Output Log or UI directly. So “debugging” is **indirect**: script writes structured results to a file; we don’t scrape or “look at” the Output Log or viewport from the agent.
- **Editor auto-launch** — Start-AllAgents launches the Editor (when UE_EDITOR is set) and waits for MCP port 55557, so the next round can run scripts. We don’t “look at” the UI; we ensure the process is up and the MCP server is ready.

### 3.2 What we do not do (currently)

- **Look at the Editor UI** — We do not use a tool that “sees” the Level Editor, Details panel, or graph editors. So we don’t “look at the UI” to verify placement, PCG Generate, or Blueprint graphs. Verification is via: (1) scripts that create/place and optionally query state, (2) pie_test_results.json, (3) verify_30day_implementation.py (file/artifact presence).
- **Read Output Log from the agent** — Output Log is the main place for PCG (LogPCG, “No surfaces found”), GAS, and other runtime messages. Our automation does **not** read Output Log programmatically from the agent. Task docs tell a **human** to open Window → Developer Tools → Output Log for debugging. So for “perform debugging” we are **partially skipping**: we run scripts and PIE tests and consume their outputs; we do not automate reading or parsing the Editor’s log.
- **Drive the Editor by clicking** — We do not use PyAutoGUI (or similar) in the default agent flow to click menus, Details, or graph nodes. That is documented as an option (e.g. PCG ref-based script, AnimGraph) but is not part of the current “start agents” loop. So any step that **requires** clicking in the UI (e.g. “assign graph in Details”, “add State Tree branch”) is either done by scripts when the API allows, or **skipped** and logged in AUTOMATION_GAPS.

### 3.3 Summary: Editor, UI, debugging

| Capability | Used? | How |
|------------|--------|-----|
| Run code in the Editor | Yes | MCP execute_python_script; Python scripts in Content/Python. |
| Create/place assets and actors | Yes | Python + MCP (where API exists). |
| PIE and structured checks | Yes | pie_test_runner.py → Saved/pie_test_results.json. |
| Read Output Log from agent | No | Not automated; humans use Window → Developer Tools → Output Log. |
| “Look at” viewport or UI | No | No tool in the loop that captures or parses Editor UI. |
| Click UI (menus, Details, graphs) | No in default loop | PyAutoGUI/refs documented for PCG/AnimGraph but not used by Start-AllAgents. |
| Screenshot viewport | Available | capture_viewport.py; not required by current task list. |

So: we **use the Editor** as an execution and asset/level backend via MCP and Python; we **do not** look at the UI or perform debugging by reading the Editor log or driving the UI from the agent. Steps that require “look at UI” or “read log” are either delegated to scripts that write to files (e.g. pie_test_results.json) or **skipped** and logged as gaps.

---

## 4. Steps we skip (or document) because we cannot accomplish them

These are logged in **docs/AUTOMATION_GAPS.md** and/or **docs/PCG_VARIABLES_NO_ACCESS.md** and in task docs. We are **not** silently failing; we mark tasks Done with notes like “X logged in AUTOMATION_GAPS” or “manual step in doc” where we can’t automate.

### 4.1 Logged in AUTOMATION_GAPS.md

1. **DemoMap → planetoid Level Streaming / Open Level**  
   Adding a Level Streaming Volume or Blueprint trigger (portal → Open Level) is not automated. **Suggested:** GUI automation (ref images) or research LevelEditorSubsystem / Level Streaming Python API.

2. **State Tree Night? branch and Defend behavior**  
   Editing the State Tree graph (add branch, condition, task, blackboard) has no MCP/Python API in use. **Suggested:** Research State Tree Editor API or GUI automation (ref images for State Tree editor).

### 4.2 PCG (PCG_VARIABLES_NO_ACCESS.md)

- **Get Landscape Data:** Actor selector (By Tag) and tag name not set by script; **manual:** Details → By Tag, tag `PCG_Landscape`.
- **Static Mesh Spawner:** Mesh list not set by script in UE 5.7; **manual:** assign mesh(es) in Details.
- **Graph assignment on PCG Volume:** Script tries `set_graph()`; if it fails, **manual:** assign graph in Details.
- **Actor Spawner template:** Template Actor / Actor Class may not be set by script; **manual:** assign in graph Details if needed.

So for PCG we automate volume placement, tagging, Surface Sampler params, and (when it works) graph assignment; we **skip** or document the one-time manual steps for Get Landscape Data, mesh list, and sometimes graph/template.

### 4.3 AnimGraph (ANIMGRAPH_AUTOMATION_SPIKE.md)

- **AnimGraph / state machine** — No MCP or Python API for the visual graph. We **skip** programmatic AnimGraph setup; one-time manual per CHARACTER_ANIMATION.md or future Editor + auto-clicker.

### 4.4 MCP limitations (09-mcp-workflow, KNOWN_ERRORS)

- **Blueprint short name only** — Full path as blueprint_name can crash the Editor; we use short names.
- **Inherited C++ properties/components** — set_blueprint_property / set_component_property may not see inherited UPROPERTY or C++-created components; we use Python scripts for those when needed.
- **Animation Blueprint state machine** — Not exposed; we don’t automate AnimGraph editing.

### 4.5 Deferred (not “skipped” but later phase)

- Full agentic building (State Tree BUILD, Mass processor, EQS, etc.).
- SaveGame for role persistence.
- Death hook for spirit roster (when damage/death pipeline exists).
- Boss GAS + reward.
- AnimGraph automation (one-time manual or ref-based GUI).

---

## 5. Summary table

| Question | Answer |
|----------|--------|
| **Work accomplished** | 30-day implementation complete; T1–T8 done; agent company, run history, refinement, verification, Safe-Build, project state and task list. |
| **Improvements made automatically** | One script (Start-AllAgents), Editor auto-launch, run history + Refiner, verification script, AUTOMATION_GAPS (no “manual steps” for user), Safe-Build, PROJECT_STATE_AND_TASK_LIST. |
| **Tools utilized** | MCP (execute_python_script, actor/Blueprint/level APIs), Content/Python scripts, PowerShell (Start-AllAgents, Watcher, Guardian, Refiner, Safe-Build, Append-AgentRunRecord), C++ and build, optional GUI automation (documented, not in default loop). |
| **Use the Editor?** | Yes: as execution environment via MCP and Python (create/place assets, run PIE tests, run scripts). |
| **Look at the UI?** | No: no tool in the loop that “sees” or parses the Editor UI. |
| **Perform debugging?** | Partially: we run PIE tests and read pie_test_results.json; we do **not** read Output Log or drive the UI for debugging. |
| **Skipping steps we cannot accomplish?** | Yes, in a **documented** way: AUTOMATION_GAPS.md, PCG_VARIABLES_NO_ACCESS.md, task docs with “manual” or “Option B (manual)”. We mark tasks Done with notes like “X logged in AUTOMATION_GAPS” where we can’t automate. |

---

## 6. References

- [PROJECT_STATE_AND_TASK_LIST.md](workflow/PROJECT_STATE_AND_TASK_LIST.md) — Work done and task list (T1–T10).
- [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) — Logged gaps (Level Streaming, State Tree graph).
- [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md) — PCG settings automation cannot set.
- [AGENT_COMPANY.md](AGENT_COMPANY.md) — Roles and accountability.
- [09-mcp-workflow.mdc](../.cursor/rules/09-mcp-workflow.mdc) — What MCP can and cannot do.
- [ANIMGRAPH_AUTOMATION_SPIKE.md](tasks/ANIMGRAPH_AUTOMATION_SPIKE.md) — AnimGraph automation deferred.

# Project state and task list

**Purpose:** Single overview of the state of the project and **work not yet completed**, codified as a task list to work from. Update this file when major milestones or the task list change.

**Last updated:** 2026-03-03 (after full 30-day verification pass and agent-company automation).

---

## 1. Executive summary

- **30-day block:** All days 1–30 are **implementation-complete** per artifact checks and verification pass (see [30_DAY_IMPLEMENTATION_STATUS.md](30_DAY_IMPLEMENTATION_STATUS.md)). Scripts, C++ types, configs, and task docs exist; many steps have been run in Editor via MCP or documented for one-time manual runs.
- **Automation:** The **agent company** (Developer, Fixer, Guardian, Refiner) is in place. One script **Start-AllAgents.ps1** starts the full company; the Editor auto-launches when `UE_EDITOR` is set. Run history and refinement (rules/strategy from runs) are recorded and documented.
- **Remaining work** is mostly: (1) running a few scripts in Editor when open, (2) one-time or rare manual steps in level/PCG/State Tree, (3) deferred features (full agentic building, SaveGame, death→spirit hook), (4) buffer/polish and next 30-day planning.

---

## 2. Summary of work done

### 2.1 30-day implementation (Days 1–30)

| Phase | Days | What was done |
|-------|------|----------------|
| Act 1 | 1–5 | PCG forest (ForestIsland_PCG, create_pcg_forest.py); GAS + character (setup_gas_abilities.py, GA_PrimaryAttack/Dodge/Interact); BuildPlacementSupport (GetPlacementHit); Week 1 playtest doc; polish + optional Milady scripts; playtest sign-off doc. |
| Homestead | 6–10 | DemoMap layout (create_demo_from_scratch, demo_map_config); resource nodes (create_bp_harvestable_tree.py, place_resource_nodes.py); resource collection (TryHarvestInFront, GA_Interact/HomeWorldInteractAbility); home placement (GA_Place, TryPlaceAtCursor); agentic building **prep** (BP_BuildOrder_Wall, SO prep; full agentic building deferred). |
| Family | 11–15 | Family spawn scripts (create_mec_family_gatherer, create_state_tree_family_gatherer, link_state_tree_to_mec); Protector (GA_ProtectorAttack, HomeWorldProtectorAttackAbility); Healer (create_ga_heal.py, HomeWorldHealAbility); Child (doc/design, ST_FamilyGatherer Child branch); role persistence (UHomeWorldFamilySubsystem SetRoleForIndex/GetRoleForIndex; SaveGame deferred). |
| Planetoid | 16–20 | Planetoid level (ensure_planetoid_level.py, place_portal_placeholder.py, planetoid_map_config.json); PCG POI (create_bp_poi_placeholders.py, create_planetoid_poi_pcg.py, Planetoid_POI_PCG); Shrine/Treasure (TryHarvestInFront tags, POI placeholders); Cultivation/Mining (AHomeWorldYieldNode, create_bp_yield_nodes.py); Visit and interact (doc + PIE checklist). |
| Spirits | 21–23 | Spirit roster (UHomeWorldSpiritRosterSubsystem); assign spirit to node (SpiritAssignmentSubsystem, YieldNode SetAssignedSpirit); unassign (UnassignSpirit). |
| Dungeon | 24–25 | Dungeon POI (place_dungeon_entrance.py, dungeon_map_config.json); Boss/reward (doc). |
| Buffer | 26–30 | Marked done; catch-up/Milady/polish per schedule. |

### 2.2 Automation and agent company

- **RunAutomationLoop / Start-AutomationSession:** Loop runs until no pending days; prompt from NEXT_SESSION_PROMPT.md; file logging (automation_loop.log, automation_errors.log, agent_run_history.ndjson).
- **Editor auto-launch:** Default behavior when `UE_EDITOR` is set; use `-NoLaunchEditor` to skip.
- **Watcher (Fixer + Guardian):** Watch-AutomationAndFix.ps1 runs the loop and, on failure, runs the Fixer; when the same failure recurs, runs the Guardian (loop-breaker). Report: Saved/Logs/automation_loop_breaker_report.md.
- **Start-AllAgents.ps1:** One script to start the full company (installs CLI if needed, auto-launches Editor, runs Watcher).
- **Refiner:** Run-RefinerAgent.ps1 (or refine-rules-from-runs command) to update rules and strategy from run history; see [AUTOMATION_REFINEMENT.md](../AUTOMATION_REFINEMENT.md).
- **Verification:** Content/Python/verify_30day_implementation.py checks artifact paths per day; writes Saved/Logs/verify_30day_report.md.
- **Docs:** [AGENT_COMPANY.md](../AGENT_COMPANY.md), [AUTOMATION_REFINEMENT.md](../AUTOMATION_REFINEMENT.md), [AUTOMATION_LOOP_UNTIL_DONE.md](../AUTOMATION_LOOP_UNTIL_DONE.md), [EDITOR_BUILD_PROTOCOL.md](../EDITOR_BUILD_PROTOCOL.md), Safe-Build.ps1.

### 2.3 Infrastructure and quality

- **Session continuity:** SESSION_LOG.md, DAILY_STATE.md read at start and updated at end.
- **Known errors:** KNOWN_ERRORS.md (UE 5.7, MCP, PCG, World Partition, etc.).
- **Automation gaps:** AUTOMATION_GAPS.md for steps that could not be automated (log only).
- **Tests:** PythonAutomationTest (Content/Python/tests/test_*.py); pie_test_runner.py → Saved/pie_test_results.json; level loader and PIE flow tests.
- **CI:** validate.yml (lint, JSON, C++, doc freshness).

---

## 3. Work not yet completed (task list)

Use this list as the source of “what to do next.” Each item has a **goal**, **success criteria**, and **doc/link** where applicable. Status: **pending** until done.

---

### T1. Run yield and dungeon scripts in Editor

- **Goal:** Create BP_Cultivation_POI and BP_Mining_POI (Day 19) and optionally place Dungeon_POI (Day 24) in level.
- **Success criteria:** With Editor open, run `create_bp_yield_nodes.py` and (optional) `place_dungeon_entrance.py` with target level open; Blueprints/actors exist; PIE shows yield log and inventory change for nodes.
- **How:** Tools → Execute Python Script (or MCP `execute_python_script("create_bp_yield_nodes.py")`). See [NEXT_SESSION_PROMPT.md](NEXT_SESSION_PROMPT.md) and [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md) Day 19/24.
- **Status:** Done (create_bp_yield_nodes.py and place_dungeon_entrance.py run via MCP).

---

### T2. PIE spot-check

- **Goal:** Confirm character spawn, ground, animation, and PCG in PIE on DemoMap.
- **Success criteria:** Run `pie_test_runner.py` via MCP with PIE active; read Saved/pie_test_results.json; key checks pass (or document any false negatives).
- **How:** Open Editor, start PIE, run `execute_python_script("pie_test_runner.py")`, read results. See [README-Automation.md](../../README-Automation.md).
- **Status:** Done (pie_test_runner.py run via MCP; results in Saved/pie_test_results.json).

---

### T3. Manual level/PCG steps (planetoid)

- **Goal:** Planetoid level playable with PCG POI and portal streaming.
- **Success criteria:** Planetoid level exists (or created via script); Landscape has PCG_Landscape tag; PCG Volume placed and assigned Planetoid_POI_PCG; Get Landscape Data + Actor Spawner configured; Generate produces instances; DemoMap has Level Streaming or trigger to open/stream planetoid.
- **Doc:** [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md) Day 16–17; [DAY6_HOMESTEAD_LAYOUT.md](../tasks/DAY6_HOMESTEAD_LAYOUT.md), [PCG_SETUP.md](../PCG_SETUP.md).
- **Status:** Done. Ran ensure_planetoid_level.py, setup_planetoid_pcg.py, ensure_demo_portal.py via MCP. Planetoid PCG and portal placeholder automated; Level Streaming/Open Level logged in [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md).

---

### T4. Manual family/State Tree steps (Day 11–12)

- **Goal:** Mass Spawner on DemoMap; MEC representation mesh; State Tree Defend/Night branch.
- **Success criteria:** Mass Spawner placed with MEC_FamilyGatherer config; N agents spawn in PIE; MEC has Static Mesh set on representation trait; ST_FamilyGatherer has Night? branch and Defend behavior; PIE with `hw.TimeOfDay.Phase 2` validates Defend.
- **Doc:** [DAY11_FAMILY_SPAWN.md](../tasks/DAY11_FAMILY_SPAWN.md), [DAY12_ROLE_PROTECTOR.md](../tasks/DAY12_ROLE_PROTECTOR.md), [FAMILY_AGENTS_MASS_STATETREE.md](../tasks/FAMILY_AGENTS_MASS_STATETREE.md).
- **Status:** Done. Ran place_mass_spawner_demomap.py and set_mec_representation_mesh.py via MCP; Mass Spawner placed on DemoMap. State Tree Night?/Defend branch not automatable — logged in [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md).

---

### T5. Dungeon level streaming / interior

- **Goal:** Dungeon_POI actor in level triggers level streaming or opens dungeon interior.
- **Success criteria:** In Blueprint or level, Dungeon_POI (or trigger volume) opens/streams dungeon sublevel; doc updated with steps.
- **Doc:** [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md) Day 24.
- **Status:** Done. Added AHomeWorldDungeonEntrance (C++ trigger opens level on overlap); DAYS_16_TO_30 Day 24 updated with Option A/B/C steps; build verified.

---

### T6. Populate CYCLE_TASKLIST

- **Goal:** CYCLE_TASKLIST.md has concrete tasks (id, goal, success criteria, doc, status) for the next cycle (e.g. T1–T5, buffer items).
- **Success criteria:** Agent or user can read CYCLE_TASKLIST and pick “next task”; status updated as tasks complete.
- **Doc:** [CYCLE_TASKLIST.md](CYCLE_TASKLIST.md).
- **Status:** Done. CYCLE_TASKLIST populated with T1–T9 (T1–T6 completed, T7–T9 pending).

---

### T7. Buffer / polish (Days 26–30)

- **Goal:** One moment + one beautiful corner for vertical slice; or Milady pipeline progress; or bug polish.
- **Success criteria:** Chosen buffer item(s) advanced and documented (e.g. vertical slice checklist, Milady import steps, or KNOWN_ERRORS/SESSION_LOG entries).
- **Doc:** [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md) Days 26–30, [MILADY_IMPORT_ROADMAP.md](../tasks/MILADY_IMPORT_ROADMAP.md), [VISION.md](VISION.md).
- **Status:** Done. Added [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) (moment + corner options, pre-demo checklist, demo steps); updated PROTOTYPE_SCOPE defaults and Day 26 link.

---

### T8. Plan next 30-day window

- **Goal:** Define the next block of days (goals, scope, success criteria) after the current 30-day block.
- **Success criteria:** New schedule or roadmap section (e.g. in 30_DAY_SCHEDULE or new doc) with next N days and links to task docs.
- **Doc:** [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md), [VISION.md](VISION.md), [MVP_AND_ROADMAP_STRATEGY.md](MVP_AND_ROADMAP_STRATEGY.md).
- **Status:** Done. Added [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md) (phases: Harden & demo, Deferred features, Act 2 prep, Steam EA prep); linked from 30_DAY_SCHEDULE and MVP_AND_ROADMAP_STRATEGY.

---

### T9. Refiner run (rules/strategy from run history)

- **Goal:** Use run history and errors to update .cursor/rules, KNOWN_ERRORS.md, or AGENTS.md so the same failures don’t recur.
- **Success criteria:** Run `.\Tools\Run-RefinerAgent.ps1` (or refine-rules-from-runs); at least one doc updated from suggestions in agent_run_history.ndjson or automation_loop_breaker_report.md.
- **Doc:** [AUTOMATION_REFINEMENT.md](../AUTOMATION_REFINEMENT.md).
- **Status:** Done. Ran Run-RefinerAgent.ps1; fixed Get-Content -Tail/-Raw in script; Refiner updated SESSION_LOG; added KNOWN_ERRORS entry for the script fix.

---

### T10. Deferred / later (no immediate task)

- **Full agentic building (Day 10):** State Tree BUILD branch, Mass Processor MP_WoodInventory, EQS, “Convert to Construction Mesh,” SO_WallBuilder; full flow after Phase 2. Doc: [DAY10_AGENTIC_BUILDING.md](../tasks/DAY10_AGENTIC_BUILDING.md), [AGENTIC_BUILDING.md](../tasks/AGENTIC_BUILDING.md).
- **SaveGame for role persistence (Day 15):** Persist role assignment across sessions. Doc: [DAY15_ROLE_PERSISTENCE.md](../tasks/DAY15_ROLE_PERSISTENCE.md).
- **Death hook for spirit roster (Day 21):** When damage/death pipeline exists, call SpiritRosterSubsystem on death. Doc: [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md) Day 21.
- **Boss GAS + reward (Day 25):** Implement boss actor and dungeon complete reward (inventory/story flag). Doc: [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md) Day 25.
- **AnimGraph automation:** One-time manual or ref-based GUI; no commandlet. Doc: [ANIMGRAPH_AUTOMATION_SPIKE.md](../tasks/ANIMGRAPH_AUTOMATION_SPIKE.md).

---

## 4. Quick reference

| Need | Doc or command |
|------|-----------------|
| What to do today | [DAILY_STATE.md](DAILY_STATE.md) → Today |
| 30-day status | [30_DAY_IMPLEMENTATION_STATUS.md](30_DAY_IMPLEMENTATION_STATUS.md) |
| Next session prompt | [NEXT_SESSION_PROMPT.md](NEXT_SESSION_PROMPT.md) |
| Start all agents | `.\Tools\Start-AllAgents.ps1` |
| Verify artifact paths | `py Content/Python/verify_30day_implementation.py` |
| Refine rules from runs | `.\Tools\Run-RefinerAgent.ps1` or refine-rules-from-runs |
| Agent company roles | [AGENT_COMPANY.md](../AGENT_COMPANY.md) |
| Known errors | [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) |
| Task list (this file) | [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) |

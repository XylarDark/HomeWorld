# Project state and task list

**Purpose:** Single overview of the state of the project and **work not yet completed**, codified as a task list to work from. Update this file when major milestones or the task list change.

**Last updated:** 2026-03-05 (sixth 10-task list: vertical slice, PIE validation, agentic building, SaveGame, Act 2 Defend, demo, packaging, single-instance guard, buffer).

---

## 1. Executive summary

- **30-day block:** All days 1–30 are **implementation-complete** per artifact checks and verification pass (see [30_DAY_IMPLEMENTATION_STATUS.md](30_DAY_IMPLEMENTATION_STATUS.md)). Scripts, C++ types, configs, and task docs exist; many steps have been run in Editor via MCP or documented for one-time manual runs.
- **Automation:** The **agent company** (Developer, Fixer, Guardian, Refiner) is in place. One script **Start-AllAgents.ps1** starts the full company; the Editor auto-launches when `UE_EDITOR` is set. Run history and refinement (rules/strategy from runs) are recorded and documented.
- **Remaining work** is mostly: (1) running a few scripts in Editor when open, (2) one-time or rare manual steps in level/PCG/State Tree, (3) deferred: full agentic building only (SaveGame, death→spirit, boss reward are implemented and verifiable via console commands `hw.Save`, `hw.Load`, `hw.ReportDeath`, `hw.GrantBossReward` in PIE), (4) buffer/polish and next 30-day planning.

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

Use this list as the source of "what to do next." Each item has a **goal**, **success criteria**, and **doc/link** where applicable. Status: **pending** until done.

### Agent-driven task list (MVP-focused)

**Primary source for agents:** [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md). Agents fetch the first **pending** task from this list; update status there and in DAILY_STATE as tasks complete. See CURRENT_TASK_LIST for full goal/success criteria/doc per task.

| Id | One-line summary | See CURRENT_TASK_LIST for status and order |
|----|-------------------|-------------------------------------------|
| T1 | PIE pre-demo checklist (Editor + PIE, pie_test_runner) | completed |
| T2 | Save/Load and Phase 2 in PIE: document or verify | completed |
| T3 | Portal LevelToOpen: verify or document (DemoMap to planetoid) | completed |
| T4 | State Tree Defend/Night: verify or document | completed |
| T5 | SaveGame persistence across PIE restart | completed |
| T6 | Packaged build run or Steam EA checklist update | completed |
| T7 | Vertical slice sign-off or 1-3 min demo | completed |
| T8 | Docs polish (KNOWN_ERRORS, CONVENTIONS, or checklist) | completed |
| T9 | AUTOMATION_GAPS or refinement doc update | completed |
| T10 | Buffer: next list generation prep (ACCOMPLISHMENTS + PROJECT_STATE §4) | completed |

---

## 4. Current list (eighth 10-task list)

- The **eighth 10-task list** (2026-03-05) is **complete**: all T1–T10 **completed** (PIE pre-demo, Save/Load and Phase 2, portal, State Tree Defend, SaveGame, packaging, slice sign-off, docs polish, AUTOMATION_GAPS/refinement, buffer).
- **Next step:** Generate the next 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md) (read [TASK_LIST_REPEATS_LOG.md](TASK_LIST_REPEATS_LOG.md) and ACCOMPLISHMENTS_OVERVIEW §4 to avoid duplicating completed work). Then run `.\Tools\Start-AllAgents-InNewWindow.ps1` (or Start-AllAgents.bat) for the next cycle. See [LAST_SESSION_AUDIT_AND_MVP_REMAINING.md](LAST_SESSION_AUDIT_AND_MVP_REMAINING.md) for audit and MVP basics.

---

## 5. Quick reference

| Need | Doc or command |
|------|-----------------|
| What to do today | [DAILY_STATE.md](DAILY_STATE.md) → Today |
| **High-level work accomplished** (for next task list + vision) | [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md) |
| 30-day status | [30_DAY_IMPLEMENTATION_STATUS.md](30_DAY_IMPLEMENTATION_STATUS.md) |
| Next session prompt | [NEXT_SESSION_PROMPT.md](NEXT_SESSION_PROMPT.md) |
| Start all agents | `.\Tools\Start-AllAgents.ps1` |
| Verify artifact paths | `py Content/Python/verify_30day_implementation.py` |
| Refine rules from runs | `.\Tools\Run-RefinerAgent.ps1` or refine-rules-from-runs |
| Agent company roles | [AGENT_COMPANY.md](../AGENT_COMPANY.md) |
| Known errors | [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) |
| Task list (this file) | [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) |

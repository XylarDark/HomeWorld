# Project state and task list

**Purpose:** Single overview of the state of the project and **work not yet completed**, codified as a task list to work from. Update this file when major milestones or the task list change.

**Last updated:** 2026-03-09 (sixty-third 10-task list complete; MVP full scope List 63: Integration).

---

## 0. Current development phase (for task list composition)

**Single source of truth for the task list generator.** When generating a new 10-task list, read this to choose how many slots are implementation vs verification. Update this when the team shifts phase (e.g. before a demo, after adding major features).

| Phase | When to use | Implementation slots (testable build/code/feature) | Verification/support slots (PIE checklist, packaged build, docs, gaps, refinement, buffer) |
|-------|-------------|-------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| **Rapid prototyping** | Adding features, exploring systems, building out MVP. Maximize quantity of shippable work; keep verification minimal so tokens go to implementation. | **7** of 10 (T1–T7) | **3** (T8 = combined docs/cycle, T9 = combined verification, T10 = buffer). See HOW_TO_GENERATE_TASK_LIST § "Consolidate overhead." |
| **Prototype hardening** | Preparing for demo, release, or playtest; stabilizing after a big push; regression and quality focus. Maximize quality and confidence; more verification and docs. | **4–5** of 10 | **5–6** (PIE pre-demo, packaged build, VERTICAL_SLICE_CHECKLIST, AUTOMATION_GAPS, KNOWN_ERRORS/CONVENTIONS, refinement, buffer) |

**Current phase:** **Rapid prototyping** (default while MVP and vertical slice are still being built out). Change to **Prototype hardening** when preparing for a concrete demo date, playtest, or release.

**Consolidation (rapid prototyping):** Use **one** "Docs and cycle" task (T8) and **one** "Verification" task (T9) instead of 4–5 separate doc/cycle/verify tasks. That leaves T1–T7 for substantive implementation; each of T1–T7 should be a meaningful chunk (e.g. multi-step feature, or feature + test). See [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md) § Consolidate overhead.

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

### Deferred features (track so we don't re-do "verify/document" every list)

When a task is **"verify or document deferred X"** and the agent completes it (by implementing X or by documenting that X remains deferred), that completion must be recorded so the **next list generator** does not add the same "verify deferred X" task again unless the goal is to **implement** X or to re-verify after major changes.

| Feature | Status | Last list/date | Rule for next list |
|--------|--------|-----------------|--------------------|
| **Full agentic building** (family agents fulfilling build orders) | Deferred; SO activation observable | Sixtieth list (2026-03-09): List 60 T1–T7 completed — Path 1 (hw.PlaceWall, hw.CompleteBuildOrder, hw.SimulateBuildOrderActivation) works; Path 2 (full agent) requires State Tree BUILD branch per AGENTIC_BUILDING Step 3 (manual; no Python/MCP API — same as Gap 2). AUTOMATION_GAPS List 60 T7 cycle note. | Do **not** add another "verify or document agentic building" task unless the goal is to **implement** full flow (DAY10 Option B) or to re-verify after code changes. |
| **Death-to-spirit** (ReportDeathAndAddSpirit, hw.ReportDeath) | Implemented; verifiable in PIE | Eleventh list (2026-03-05); console `hw.ReportDeath`; pie_test_runner check_report_death. | Do **not** add "verify death-to-spirit" again unless re-verifying after changes. Prefer "implement" or other deferred items. |
| **SaveGame persistence** (hw.Save / hw.Load across PIE restart) | Implemented; verification in lists | DAY15 §4; verified in several lists. | Add "verify SaveGame across restart" only if re-verification is needed (e.g. after SaveGame code changes). |
| **Boss reward** (hw.GrantBossReward) | Implemented; verifiable | Documented; verified in second list. | Same as above; don't re-add verify unless implementing new behavior or re-verifying. |
| **Astral return on death** (night combat: return to body, wake at dawn) | Designed; implementation deferred | Thirteenth list (2026-03-05); [ASTRAL_DEATH_AND_DAY_SAFETY.md](../tasks/ASTRAL_DEATH_AND_DAY_SAFETY.md). | Do **not** add "verify or document astral return" again unless the goal is to **implement** (OnAstralDeath → advance to dawn, respawn in bed). |
| **Astral-by-day** (enter the astral during the day) | Late-game progression unlock; not in MVP | Thirteenth list (2026-03-05); [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md), [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md) § Day/night and astral, [VISION.md](VISION.md). | Do **not** treat as MVP. Add only if implementing the progression unlock (post–vertical slice). |
| **Bed or wake-up trigger** (MVP tutorial List 2; go-to-bed List 8) | Deferred; optional for List 2 and List 8 | Forty-first list (List 2); forty-seventh list (2026-03-07): List 8 scope documents bed actor optional — **hw.GoToBed** or **hw.TimeOfDay.Phase 2** sufficient for step 8 verification; bed can be added later (e.g. reuse List 2 placeholder). | Do **not** add "verify or add bed placeholder" again unless implementing; List 3 (breakfast) and List 8 (go to bed) verification use console. |

**When an agent completes a "deferred" task:** (1) Set that task's **status** to `completed` in CURRENT_TASK_LIST. (2) Update the task doc (e.g. DAY10_AGENTIC_BUILDING, DAY15_ROLE_PERSISTENCE) or SESSION_LOG with the outcome (implemented vs still deferred). (3) If the outcome is "still deferred," add or update the row above (or the **Last list/date** cell) so the next list generator knows this verification was just done. **When generating the next list:** Read this table and ACCOMPLISHMENTS_OVERVIEW §4; do not add a task that only "verify or document" the same deferred feature again unless the intent is to implement or to re-verify after major changes.

---

## 3. Work not yet completed (task list)

Use this list as the source of "what to do next." Each item has a **goal**, **success criteria**, and **doc/link** where applicable. Status: **pending** until done.

### Agent-driven task list (MVP-focused)

**Primary source for agents:** [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md). Agents fetch the first **pending** task from this list; update status there and in DAILY_STATE as tasks complete. See CURRENT_TASK_LIST for full goal/success criteria/doc per task.

| Id | One-line summary | See CURRENT_TASK_LIST for status and order |
|----|-------------------|-------------------------------------------|
| T1 | Tutorial loop single-session run (MVP tutorial 13 steps) | pending |
| T2 | Week 1 playtest single-session run (crash → scout → boss → claim home) | pending |
| T3 | Vertical slice pre-demo checklist run | pending |
| T4 | Integration doc — single entry point and run mapping | pending |
| T5 | CONSOLE_COMMANDS and MVP_TUTORIAL_PLAN — integration verification | pending |
| T6 | MVP full scope List 63 — vertical slice §4 sixty-third deliverables | pending |
| T7 | AUTOMATION_GAPS or KNOWN_ERRORS — List 63 findings | pending |
| T8 | Docs and cycle (combined) | pending |
| T9 | Verification (combined) | pending |
| T10 | Buffer: next list prep (ACCOMPLISHMENTS + PROJECT_STATE §4) | pending |

---

## 4. Current list (sixty-third 10-task list — MVP full scope List 63)

- The **sixty-third 10-task list** is **complete**. All T1–T10 **completed** (List 63: Integration — tutorial + Week 1 playtest single-session run; vertical slice pre-demo). See [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md).
- **Next step:** Generate **List 64** (packaged build smoke-test; demo sign-off; MVP full-scope verification and buffer) per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md) and [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md); then run `.\Tools\Start-AllAgents-InNewWindow.ps1`.
- **Cycle doc freshness and next priority:** See [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) (top) and [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md) §4.

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

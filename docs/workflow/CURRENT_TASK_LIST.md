# Current task list (10-task)

**Last updated:** 2026-03-05 (ninth list: re-verify slice, Save/Load and Phase 2, portal/State Tree gaps, SaveGame, packaging, slice sign-off, docs, AUTOMATION_GAPS, buffer).

**Purpose:** Single ordered list that drives the automation loop. Agents fetch the first **pending** or **in_progress** task; update status when done. Loop exits when no task has status pending or in_progress. **You must update this file:** when you complete a task, set only that task's **status** to `completed` so the loop does not re-run it.

**Convention:** `pending` | `in_progress` | `completed` | `blocked`

**Order:** T1 to T10. See [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md). This list continues MVP/re-verification and gap follow-ups after the eighth list (all T1–T10 completed). Re-verification by design per TASK_LIST_REPEATS_LOG; read ACCOMPLISHMENTS_OVERVIEW §4 to avoid duplicating completed work.

---

## T1. Re-run PIE pre-demo checklist (Editor + PIE, pie_test_runner)

- **goal:** With Editor open and DemoMap (or Homestead) loaded, start PIE, run pie_test_runner.py via MCP or Tools > Execute Python Script, then inspect Saved/pie_test_results.json. Document outcome for Level, Character, Moment (placement), Corner, and Stability per VERTICAL_SLICE_CHECKLIST §3.
- **success criteria:** PIE was running when pie_test_runner executed; Saved/pie_test_results.json exists and shows character spawn, on ground, placement API, PCG count; outcome (pass/fail per check) documented in VERTICAL_SLICE_CHECKLIST §3 or SESSION_LOG; any failure or gap noted.
- **research_notes:** VERTICAL_SLICE_CHECKLIST §3; pie_test_runner.py writes Saved/pie_test_results.json; MCP execute_python_script("pie_test_runner.py"); PIE must be started before running script. LAST_SESSION_AUDIT_AND_MVP_REMAINING §3. Re-verification by design (TASK_LIST_REPEATS_LOG §1.B).
- **steps_or_doc:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3, [LAST_SESSION_AUDIT_AND_MVP_REMAINING.md](LAST_SESSION_AUDIT_AND_MVP_REMAINING.md), pie_test_runner.py.
- **status:** pending

---

## T2. Save/Load and Phase 2 in PIE: document or re-verify

- **goal:** With PIE running, run pie_test_runner checks for check_save_load_persistence and check_time_of_day_phase2 (if implemented). Document results in DAY15_ROLE_PERSISTENCE §4 and DAY12_ROLE_PROTECTOR §4, or in SESSION_LOG; note pass/fail/not run.
- **success criteria:** pie_test_runner Save/Load and Phase 2 results documented; DAY15 §4 and DAY12 §4 updated if needed; or explicit "not run / deferred" with reason.
- **research_notes:** pie_test_runner.py; DAY15_ROLE_PERSISTENCE §4; DAY12_ROLE_PROTECTOR §4; hw.Save, hw.Load, hw.TimeOfDay.Phase 2; PIE required for these checks.
- **steps_or_doc:** [DAY15_ROLE_PERSISTENCE.md](../tasks/DAY15_ROLE_PERSISTENCE.md), [DAY12_ROLE_PROTECTOR.md](../tasks/DAY12_ROLE_PROTECTOR.md), pie_test_runner.py.
- **status:** pending

---

## T3. Portal LevelToOpen: verify or document (DemoMap to planetoid)

- **goal:** Verify portal (AHomeWorldDungeonEntrance) LevelToOpen is set so DemoMap to planetoid works; or document that set_portal_level_to_open.py (GUI) or manual Details step is required and update AUTOMATION_GAPS.
- **success criteria:** PIE: walk to portal (800,0,100), trigger opens planetoid level; or doc updated with verification steps and gap status; AUTOMATION_GAPS Gap 1 note current.
- **research_notes:** AUTOMATION_GAPS Gap 1; place_portal_placeholder.py; set_portal_level_to_open.py and refs/portal; LevelToOpen may need Editor Details or GUI automation.
- **steps_or_doc:** [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) Gap 1, [refs/portal/README.md](../Content/Python/gui_automation/refs/portal/README.md).
- **status:** pending

---

## T4. State Tree Defend/Night: verify or document

- **goal:** Validate that PIE with hw.TimeOfDay.Phase 2 shows family Defend behavior when State Tree Night branch exists; or document that Defend requires one-time manual steps (AUTOMATION_GAPS Gap 2) and note validation steps.
- **success criteria:** PIE: hw.TimeOfDay.Phase 2 and family Defend observable; or doc updated with Defend requires Gap 2 manual steps and validation procedure; DAY12 §4 satisfied or documented.
- **research_notes:** AUTOMATION_GAPS Gap 2; DAY12_ROLE_PROTECTOR §4; state_tree_apply_defend_branch.py and refs/state_tree; pie_test_runner check_time_of_day_phase2.
- **steps_or_doc:** [DAY12_ROLE_PROTECTOR.md](../tasks/DAY12_ROLE_PROTECTOR.md), [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) Gap 2, [refs/state_tree/README.md](../Content/Python/gui_automation/refs/state_tree/README.md).
- **status:** pending

---

## T5. SaveGame persistence across PIE restart

- **goal:** Verify SaveGame hw.Save / hw.Load persistence across PIE restart: save state, stop PIE, start PIE, load and confirm state restored. Use pie_test_runner check_save_load_persistence or manual PIE steps; document outcome.
- **success criteria:** PIE: hw.Save then restart PIE then hw.Load restores state (or documented limitation); pie_test_runner Save/Load check passes when PIE active; or outcome in DAY15_ROLE_PERSISTENCE or SESSION_LOG.
- **research_notes:** DAY15_ROLE_PERSISTENCE; pie_test_runner check_save_load_persistence; UHomeWorldSaveGameSubsystem; hw.Save / hw.Load console commands.
- **steps_or_doc:** [DAY15_ROLE_PERSISTENCE.md](../tasks/DAY15_ROLE_PERSISTENCE.md), pie_test_runner.py.
- **status:** pending

---

## T6. Packaged build run or Steam EA checklist update

- **goal:** Run packaged build (Package-HomeWorld.bat, Editor closed) and smoke-test from Saved\StagedBuilds, or update STEAM_EA_STORE_CHECKLIST with current status and next steps.
- **success criteria:** Packaged build runs and smoke test documented; or STEAM_EA_STORE_CHECKLIST updated with status and run instructions.
- **research_notes:** STEAM_EA_STORE_CHECKLIST; SETUP § Packaging; Package-HomeWorld.bat; RunUAT can take 30+ min; Editor must be closed.
- **steps_or_doc:** [STEAM_EA_STORE_CHECKLIST.md](STEAM_EA_STORE_CHECKLIST.md), [SETUP.md](../SETUP.md) § Packaging.
- **status:** pending

---

## T7. Vertical slice sign-off or 1-3 min demo

- **goal:** Produce a 1-3 min demo recording of the vertical slice (moment + corner) or complete a written sign-off checklist so the slice is showable for stakeholders.
- **success criteria:** Demo clip saved and path documented; or VERTICAL_SLICE_SIGNOFF (or equivalent) completed and linked from VERTICAL_SLICE_CHECKLIST or PROJECT_STATE.
- **research_notes:** VERTICAL_SLICE_CHECKLIST §4; VERTICAL_SLICE_SIGNOFF; PROTOTYPE_SCOPE (moment = Claim homestead, corner = Homestead compound).
- **steps_or_doc:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md), [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md).
- **status:** pending

---

## T8. Docs polish (KNOWN_ERRORS, CONVENTIONS, or checklist)

- **goal:** Polish one area (e.g. KNOWN_ERRORS, CONVENTIONS, VERTICAL_SLICE_CHECKLIST) or complete one doc update that reflects this cycle's learnings; link from PROJECT_STATE or CURRENT_TASK_LIST.
- **success criteria:** At least one doc updated and linked; concrete next priority or freshness note for next list.
- **research_notes:** PROJECT_STATE_AND_TASK_LIST §3-4; ACCOMPLISHMENTS_OVERVIEW; KNOWN_ERRORS; CONVENTIONS.
- **steps_or_doc:** [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md), [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md), docs/CONVENTIONS.md.
- **status:** pending

---

## T9. AUTOMATION_GAPS or refinement doc update

- **goal:** Update AUTOMATION_GAPS.md with any new findings from T1-T8, or update AUTOMATION_REFINEMENT / agent run history doc with cycle outcome; ensure next list generator has current gap list.
- **success criteria:** AUTOMATION_GAPS has current entries (or Addressed notes); or refinement doc updated; no stale gap descriptions.
- **research_notes:** AUTOMATION_GAPS.md; AUTOMATION_REFINEMENT.md; agent_run_history.ndjson; HOW_TO_GENERATE_TASK_LIST sources.
- **steps_or_doc:** [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md), [AUTOMATION_REFINEMENT.md](../AUTOMATION_REFINEMENT.md).
- **status:** pending

---

## T10. Buffer: next list generation prep (ACCOMPLISHMENTS + PROJECT_STATE §4)

- **goal:** Update ACCOMPLISHMENTS_OVERVIEW §4 with ninth-cycle outcome and PROJECT_STATE_AND_TASK_LIST §4 so the next list can be generated from HOW_TO_GENERATE_TASK_LIST; set T1-T10 status as completed where done.
- **success criteria:** ACCOMPLISHMENTS_OVERVIEW §4 has ninth-cycle row (outcome + Next = generate new list); PROJECT_STATE §4 says current list complete and points to HOW_TO_GENERATE_TASK_LIST and Start-AllAgents-InNewWindow.ps1.
- **research_notes:** HOW_TO_GENERATE_TASK_LIST; ACCOMPLISHMENTS_OVERVIEW; PROJECT_STATE_AND_TASK_LIST; TASK_LIST_REPEATS_LOG; VISION.
- **steps_or_doc:** [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md), [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md), [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md).
- **status:** pending

---

**Order:** T1 to T10. See [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) for context.

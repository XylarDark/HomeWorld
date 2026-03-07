# Current task list (10-task)

**Last updated:** 2026-03-06 (thirty-second list, **rapid prototyping**: 7 implementation + 2 verification + 1 buffer per PROJECT_STATE §0). **Context:** Follow-on from thirty-first (console commands, vertical slice §4, pie_test_runner planetoid check done): max-rounds fix, vertical slice §4 thirty-second, CONSOLE_COMMANDS pie_test_results keys, optional second sin/virtue stub, packaged build, KNOWN_ERRORS, PIE verification, buffer.

**Purpose:** Single ordered list that drives the automation loop. Agents fetch the first **pending** or **in_progress** task; update status when done. Loop exits when no task has status pending or in_progress.

**Convention:** `pending` | `in_progress` | `completed` | `blocked`

**Order:** T1–T7 = implementation; T8–T9 = verification; T10 = buffer.

---

## T1. Increase max rounds to 11 in RunAutomationLoop.ps1

- **goal:** Change the loop cap from 10 to 11 rounds in RunAutomationLoop.ps1 so that when all 10 tasks are pending, the buffer task (T10) runs in the same run instead of being left for manual completion. Update the check from `if ($round -gt 10)` to `if ($round -gt 11)` and update the log message to "max rounds (11) reached". Optionally add a one-line comment in the script explaining why 11 (one round per task T1–T10).
- **success criteria:** RunAutomationLoop.ps1 allows 11 rounds; log message says "max rounds (11)"; T1 status set to completed.
- **research_notes:** Tools/RunAutomationLoop.ps1 lines 472–477; thirty-first run hit round 10 and exited before T10 (buffer). See SESSION_LOG 2026-03-06.
- **steps_or_doc:** Tools/RunAutomationLoop.ps1.
- **status:** completed

---

## T2. Vertical slice §4: thirty-second-list deliverables subsection

- **goal:** Add a subsection "Thirty-second-list deliverables" to VERTICAL_SLICE_CHECKLIST.md §4 with a short table or list of what this list will deliver (to be filled after run: max-rounds fix, CONSOLE_COMMANDS pie_test_results keys, optional hw.SinVirtue.Greed, packaged build or doc, KNOWN_ERRORS note, PIE outcome). Same pattern as "Thirty-first-list deliverables". No new implementation; doc only.
- **success criteria:** VERTICAL_SLICE_CHECKLIST §4 contains "Thirty-second-list deliverables" with verification refs or placeholder rows; T2 status set to completed.
- **research_notes:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §4 (Thirty-first-list deliverables pattern); thirty-second list T1–T8 scope.
- **steps_or_doc:** docs/workflow/VERTICAL_SLICE_CHECKLIST.md.
- **status:** completed

---

## T3. CONSOLE_COMMANDS: pie_test_results.json check names (planetoid_complete)

- **goal:** In CONSOLE_COMMANDS.md section "Reading Saved/pie_test_results.json", ensure the check names table (or equivalent) includes the planetoid_complete check added in thirty-first list (T8). If the table lists individual checks, add a row for planetoid_complete; if it references "checks array", add a brief note that planetoid_complete is one of the checks when PIE is running. So testers know what to look for.
- **success criteria:** CONSOLE_COMMANDS.md documents planetoid_complete in the pie_test_results interpretation; T3 status set to completed.
- **research_notes:** [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) "Reading Saved/pie_test_results.json"; [pie_test_runner.py](../../Content/Python/pie_test_runner.py) ALL_CHECKS (planetoid complete).
- **steps_or_doc:** docs/CONSOLE_COMMANDS.md.
- **status:** completed

---

## T4. Console command hw.SinVirtue.Greed (stub, optional)

- **goal:** Add a second sin/virtue console command `hw.SinVirtue.Greed` that logs the stub value (e.g. 0), same pattern as hw.SinVirtue.Pride. Document in CONSOLE_COMMANDS.md and SIN_VIRTUE_SPECTRUM.md §2. Optional: if time-boxed, document "hw.SinVirtue.Greed to be added" and mark T4 completed with doc-only.
- **success criteria:** Command implemented and documented, or doc-only "to be added" in CONSOLE_COMMANDS + SIN_VIRTUE_SPECTRUM; T4 status set to completed.
- **research_notes:** [HomeWorld.cpp](../../Source/HomeWorld/HomeWorld.cpp) CmdSinVirtuePride pattern; [SIN_VIRTUE_SPECTRUM.md](../tasks/SIN_VIRTUE_SPECTRUM.md); [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md).
- **steps_or_doc:** Source/HomeWorld/HomeWorld.cpp; docs/CONSOLE_COMMANDS.md; docs/tasks/SIN_VIRTUE_SPECTRUM.md.
- **status:** completed

---

## T5. Packaged build: retry or document outcome

- **goal:** Optionally run Package-AfterClose.ps1 (or project packaging script) with Editor and game processes closed; document outcome in STEAM_EA_STORE_CHECKLIST or KNOWN_ERRORS. If not running package this list, add a brief note (e.g. "Thirty-second list: package not run; use Package-AfterClose.ps1 when ready") so the next list has context.
- **success criteria:** Package retry attempted and outcome documented, or skip documented; T5 status set to completed.
- **research_notes:** [STEAM_EA_STORE_CHECKLIST.md](STEAM_EA_STORE_CHECKLIST.md); [KNOWN_ERRORS.md](../KNOWN_ERRORS.md); Tools/Package-AfterClose.ps1.
- **steps_or_doc:** docs/KNOWN_ERRORS.md, docs/workflow/STEAM_EA_STORE_CHECKLIST.md.
- **status:** completed

---

## T6. KNOWN_ERRORS or AUTOMATION_GAPS: cycle note or findings

- **goal:** After T1–T5, update KNOWN_ERRORS.md or AUTOMATION_GAPS.md with any new findings from this cycle. If no new errors, add a brief cycle note (e.g. "Thirty-second list: T1–T6 completed; no new errors") so the next list generator has context.
- **success criteria:** KNOWN_ERRORS or AUTOMATION_GAPS updated with cycle findings or cycle note; T6 status set to completed.
- **research_notes:** [KNOWN_ERRORS.md](../KNOWN_ERRORS.md); [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md); 07-ai-agent-behavior (error recurrence prevention).
- **steps_or_doc:** docs/KNOWN_ERRORS.md, docs/AUTOMATION_GAPS.md.
- **status:** completed

---

## T7. VERTICAL_SLICE_CHECKLIST §4: thirty-second outcomes row

- **goal:** After T1–T6 (and optionally T8–T9), add or complete the "Thirty-second-list deliverables" content in VERTICAL_SLICE_CHECKLIST §4: list what was delivered (max-rounds 11, vertical slice §4 subsection, CONSOLE_COMMANDS planetoid_complete key, hw.SinVirtue.Greed or doc, packaged build or doc, KNOWN_ERRORS note, PIE outcome). Same pattern as thirty-first-list deliverables table.
- **success criteria:** VERTICAL_SLICE_CHECKLIST §4 thirty-second subsection has outcomes and verification refs; T7 status set to completed.
- **research_notes:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §4; thirty-first-list deliverables pattern.
- **steps_or_doc:** docs/workflow/VERTICAL_SLICE_CHECKLIST.md.
- **status:** completed

---

## T8. Verification: Run PIE pre-demo checklist and document results

- **goal:** Run the pre-demo verification gate: with Editor open and DemoMap (or Homestead) loaded, start PIE, run pie_test_runner.py via MCP or Tools > Execute Python Script, document outcome in VERTICAL_SLICE_CHECKLIST §3 or SESSION_LOG (e.g. Saved/pie_test_results.json present, pass/fail summary). If Editor/MCP is not connected, document that and the steps to run §3 when Editor is available.
- **success criteria:** PIE pre-demo run attempted; outcome documented in §3 or SESSION_LOG; T8 status set to completed.
- **research_notes:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3; pie_test_runner.py; [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) Pre-demo verification.
- **steps_or_doc:** docs/workflow/VERTICAL_SLICE_CHECKLIST.md §3; docs/SESSION_LOG.md.
- **status:** completed

---

## T9. Verification: Confirm task list and loop state

- **goal:** Confirm CURRENT_TASK_LIST.md has no duplicate or stray sections; confirm DAILY_STATE "Today" aligns with first pending task. Optionally run validate_task_list.py and fix any schema issues. If all tasks T1–T8 are completed and only T10 remains, this task can be "verify loop will run T10 this run (max rounds 11)" and document outcome.
- **success criteria:** Task list validated (or state confirmed); T9 status set to completed.
- **research_notes:** [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md); [DAILY_STATE.md](DAILY_STATE.md); Content/Python/validate_task_list.py.
- **steps_or_doc:** docs/workflow/CURRENT_TASK_LIST.md; python Content/Python/validate_task_list.py.
- **status:** completed

---

## T10. Buffer: next list generation prep (ACCOMPLISHMENTS + PROJECT_STATE §4)

- **goal:** Update ACCOMPLISHMENTS_OVERVIEW §4 with thirty-second-cycle outcome and PROJECT_STATE_AND_TASK_LIST §4 so the next list can be generated; set T1–T10 status to completed where done. Do NOT replace or regenerate CURRENT_TASK_LIST.md (user does that after the loop exits).
- **success criteria:** ACCOMPLISHMENTS_OVERVIEW §4 has thirty-second-cycle row (outcome + Next = generate new list); PROJECT_STATE §4 says current list complete and points to HOW_TO_GENERATE_TASK_LIST and Start-AllAgents-InNewWindow.ps1; T10 status set to completed in CURRENT_TASK_LIST only.
- **research_notes:** [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md); [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md); TASK_LIST_REPEATS_LOG.
- **steps_or_doc:** [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md), [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md), [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md).
- **status:** completed

---

**Order:** T1–T7 implementation, T8–T9 verification, T10 buffer. See [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) §0 (phase) and §4 (current list).

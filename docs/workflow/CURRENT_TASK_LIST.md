# Current task list (10-task)

**Last updated:** 2026-03-09 (sixty-third list, **ninth of MVP full scope 10 lists**). **Rapid prototyping (consolidated):** T1–T7 = implementation, T8 = docs and cycle, T9 = verification, T10 = buffer. **Context:** MVP full scope (Vision-aligned) — List 63: Integration — tutorial + Week 1 playtest single-session run; vertical slice pre-demo. See [VISION.md](VISION.md) § MVP full scope; [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md).

**Purpose:** Single ordered list that drives the automation loop. Agents fetch the first **pending** or **in_progress** task; update status when done. Loop exits when no task has status pending or in_progress.

**Convention:** `pending` | `in_progress` | `completed` | `blocked`

**Order:** T1–T7 implementation; T8 docs and cycle; T9 verification; T10 buffer.

---

## T1. Tutorial loop single-session run (MVP tutorial 13 steps)

- **goal:** Run the **MVP tutorial loop** in a **single PIE session**: wake → breakfast → love task → game with child → gather (wood/ore/flowers) → lunch → dinner → bed → spectral combat → encampment → boss → night ends → wake to family taken. Use [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Pre-demo verification and [MVP_TUTORIAL_PLAN.md](MVP_TUTORIAL_PLAN.md) checklist; console commands (hw.Meal.*, hw.LoveTask.Complete, hw.GameWithChild.Complete, hw.GoToBed, hw.TimeOfDay.Phase, etc.) as needed. Document outcome: which steps completed, which deferred or failed, and any fixes. Per [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md) List 63.
- **success criteria:** Tutorial loop run (or documented partial run) in one session; outcome in SESSION_LOG or VERTICAL_SLICE_CHECKLIST §3; T1 status set to completed.
- **research_notes:** [MVP_TUTORIAL_PLAN.md](MVP_TUTORIAL_PLAN.md); [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Pre-demo verification; [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3; VISION § MVP tutorial loop.
- **steps_or_doc:** docs/CONSOLE_COMMANDS.md; docs/workflow/MVP_TUTORIAL_PLAN.md; docs/workflow/VERTICAL_SLICE_CHECKLIST.md.
- **status:** completed

---

## T2. Week 1 playtest single-session run (crash → scout → boss → claim home)

- **goal:** Run the **Week 1 playtest** in a **single PIE session**: crash → scout → boss → claim home (per VISION § Demonstrable prototype gate). Use [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Pre-demo verification and Week 1 playtest checklist; [DAY5_PLAYTEST_SIGNOFF.md](../tasks/DAY5_PLAYTEST_SIGNOFF.md) T1 verification if applicable. Document outcome: pass/fail per beat, stability (2–5 min), any fixes. Per List 63.
- **success criteria:** Week 1 playtest run (or documented partial run) in one session; outcome in SESSION_LOG or task doc; T2 status set to completed.
- **research_notes:** [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md); [DAY5_PLAYTEST_SIGNOFF.md](../tasks/DAY5_PLAYTEST_SIGNOFF.md); [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3; VISION § Week 1 playtest goal.
- **steps_or_doc:** docs/CONSOLE_COMMANDS.md; docs/tasks/DAY5_PLAYTEST_SIGNOFF.md; docs/workflow/VERTICAL_SLICE_CHECKLIST.md.
- **status:** completed

---

## T3. Vertical slice pre-demo checklist run

- **goal:** Execute the **vertical slice pre-demo checklist** ([VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3): level open, character/Enhanced Input/GAS, chosen moment playable, chosen corner visible, stability 2–5 min. Run pie_test_runner.py if PIE is active; document pass/fail and any gaps. Optional: 1–3 min demo recording (user-led). Per List 63.
- **success criteria:** Pre-demo checklist run and outcome documented (VERTICAL_SLICE_CHECKLIST §3 or SESSION_LOG); T3 status set to completed.
- **research_notes:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3; [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Pre-demo verification; pie_test_runner.py; [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md) moment/corner.
- **steps_or_doc:** docs/workflow/VERTICAL_SLICE_CHECKLIST.md; docs/CONSOLE_COMMANDS.md; Content/Python/pie_test_runner.py.
- **status:** completed

---

## T4. Integration doc — single entry point and run mapping

- **goal:** Ensure **one clear entry point** for integration runs: [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Pre-demo verification links §3 (run sequence), tutorial checklist (MVP_TUTORIAL_PLAN), and Week 1 playtest checklist. Add or update a **List 63 integration** subsection: order of runs (tutorial loop → Week 1 playtest → pre-demo checklist), expected outcomes, and where to document results. Per List 63.
- **success criteria:** CONSOLE_COMMANDS (or linked doc) has List 63 integration run order and outcome locations; T4 status set to completed.
- **research_notes:** [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md); [MVP_TUTORIAL_PLAN.md](MVP_TUTORIAL_PLAN.md); [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3.
- **steps_or_doc:** docs/CONSOLE_COMMANDS.md; docs/workflow/MVP_TUTORIAL_PLAN.md; docs/workflow/VERTICAL_SLICE_CHECKLIST.md.
- **status:** completed

---

## T5. CONSOLE_COMMANDS and MVP_TUTORIAL_PLAN — integration verification

- **goal:** Update [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) and [MVP_TUTORIAL_PLAN.md](MVP_TUTORIAL_PLAN.md) with **List 63 integration verification** steps: how to run tutorial + Week 1 playtest + pre-demo in one or two sessions; which commands and checklists to use; where to record pass/fail. Per List 63.
- **success criteria:** CONSOLE_COMMANDS and MVP_TUTORIAL_PLAN include integration (List 63) verification; T5 status set to completed.
- **research_notes:** [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md); [MVP_TUTORIAL_PLAN.md](MVP_TUTORIAL_PLAN.md); [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3.
- **steps_or_doc:** docs/CONSOLE_COMMANDS.md; docs/workflow/MVP_TUTORIAL_PLAN.md.
- **status:** completed

---

## T6. MVP full scope List 63 — vertical slice §4 sixty-third deliverables

- **goal:** Add **Sixty-third-list deliverables** (and MVP full scope List 63 note) to VERTICAL_SLICE_CHECKLIST.md §4: tutorial loop single-session run, Week 1 playtest single-session run, vertical slice pre-demo checklist run, integration doc/entry point, verification doc. Note that this is list 9 of 10 for MVP full scope (Vision-aligned). Per List 63.
- **success criteria:** VERTICAL_SLICE_CHECKLIST §4 contains sixty-third-list deliverables and List 63 scope note; T6 status set to completed.
- **research_notes:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §4; [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md) List 63.
- **steps_or_doc:** docs/workflow/VERTICAL_SLICE_CHECKLIST.md.
- **status:** completed

---

## T7. AUTOMATION_GAPS or KNOWN_ERRORS — List 63 findings

- **goal:** If integration runs revealed gaps (missing commands, flaky steps, manual-only steps), add or update AUTOMATION_GAPS (and optionally KNOWN_ERRORS) with List 63 findings: what was run, what failed or was deferred, and suggested next step for List 64. Per List 63.
- **success criteria:** AUTOMATION_GAPS or KNOWN_ERRORS updated with List 63 cycle note or findings; T7 status set to completed.
- **research_notes:** [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md); [KNOWN_ERRORS.md](../KNOWN_ERRORS.md); [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md).
- **steps_or_doc:** docs/AUTOMATION_GAPS.md; docs/KNOWN_ERRORS.md.
- **status:** completed

---

## T8. Docs and cycle (combined)

- **goal:** In **one task**, do all of: (1) Ensure VERTICAL_SLICE_CHECKLIST §4 has sixty-third-list deliverables (if not done in T6). (2) Update CONSOLE_COMMANDS.md or MVP_TUTORIAL_PLAN (integration) so they reflect current state. (3) Update KNOWN_ERRORS or AUTOMATION_GAPS with cycle note (e.g. "List 63 (MVP full scope): Integration; T1–T7 completed."). Success = all three done (or explicitly deferred).
- **success criteria:** Vertical slice §4 sixty-third updated; CONSOLE_COMMANDS/MVP_TUTORIAL_PLAN updated; KNOWN_ERRORS or AUTOMATION_GAPS cycle note; T8 status set to completed.
- **research_notes:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §4; [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md); [MVP_TUTORIAL_PLAN.md](MVP_TUTORIAL_PLAN.md); [KNOWN_ERRORS.md](../KNOWN_ERRORS.md); [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md).
- **steps_or_doc:** docs/workflow/VERTICAL_SLICE_CHECKLIST.md; docs/CONSOLE_COMMANDS.md; docs/workflow/MVP_TUTORIAL_PLAN.md; docs/KNOWN_ERRORS.md; docs/AUTOMATION_GAPS.md.
- **status:** completed

---

## T9. Verification (combined)

- **goal:** In **one task**, do all of: (1) If T1–T7 changed C++ or Build.cs, run Build-HomeWorld.bat and confirm build passes. (2) Review VERTICAL_SLICE_CHECKLIST §3–§4 and CONSOLE_COMMANDS for consistency; document outcome in SESSION_LOG or VERTICAL_SLICE_CHECKLIST §3. (3) Run validate_task_list.py and fix any schema issues; update DAILY_STATE "Today" if needed. Success = build green (if applicable), doc review done, list validated.
- **success criteria:** Build run and result logged; doc review done and noted; validate_task_list.py passed; DAILY_STATE updated if needed; T9 status set to completed.
- **research_notes:** Build-HomeWorld.bat; [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3; [SESSION_LOG.md](../SESSION_LOG.md); Content/Python/validate_task_list.py; [DAILY_STATE.md](DAILY_STATE.md).
- **steps_or_doc:** Build-HomeWorld.bat; docs/workflow/VERTICAL_SLICE_CHECKLIST.md; python Content/Python/validate_task_list.py; docs/workflow/DAILY_STATE.md.
- **status:** completed

---

## T10. Buffer: next list prep (ACCOMPLISHMENTS + PROJECT_STATE §4)

- **goal:** Update ACCOMPLISHMENTS_OVERVIEW §4 with sixty-third-cycle outcome and PROJECT_STATE_AND_TASK_LIST §4. Do NOT replace CURRENT_TASK_LIST.md (user does that after the loop). Set T1–T10 status to completed where done. **Next list:** List 64 per [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md) (Packaged build smoke-test; demo sign-off; MVP full-scope verification and buffer). Generate next list per HOW_TO_GENERATE_TASK_LIST when ready.
- **success criteria:** ACCOMPLISHMENTS_OVERVIEW §4 has sixty-third-cycle row; PROJECT_STATE §4 says current list complete and points to List 64 (packaged build smoke-test; demo sign-off); T10 status set to completed in CURRENT_TASK_LIST only.
- **research_notes:** [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md); [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md); [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md).
- **steps_or_doc:** [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md), [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md), [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md).
- **status:** completed

---

**Order:** T1–T7 implementation (tutorial loop single-session, Week 1 playtest single-session, vertical slice pre-demo run, integration doc, CONSOLE_COMMANDS/MVP_TUTORIAL_PLAN integration verification, vertical slice §4 sixty-third, AUTOMATION_GAPS/KNOWN_ERRORS). T8 = Docs and cycle. T9 = Verification. T10 = Buffer. **After list 63:** Generate List 64 per [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md) (packaged build smoke-test; demo sign-off); run `.\Tools\Start-AllAgents-InNewWindow.ps1` when ready.

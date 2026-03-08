# Current task list (10-task)

**Last updated:** 2026-03-09 (sixty-fourth list, **tenth of MVP full scope 10 lists**). **Rapid prototyping (consolidated):** T1–T7 = implementation, T8 = docs and cycle, T9 = verification, T10 = buffer. **Context:** MVP full scope (Vision-aligned) — List 64: Packaged build smoke-test; demo sign-off; MVP full-scope verification and buffer. See [VISION.md](VISION.md) § MVP full scope; [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md).

**Purpose:** Single ordered list that drives the automation loop. Agents fetch the first **pending** or **in_progress** task; update status when done. Loop exits when no task has status pending or in_progress.

**Convention:** `pending` | `in_progress` | `completed` | `blocked`

**Order:** T1–T7 implementation; T8 docs and cycle; T9 verification; T10 buffer.

---

## T1. Packaged build run or smoke-test

- **goal:** Run **Package Game** (or project package script); document outcome. If build fails, document in KNOWN_ERRORS/AUTOMATION_GAPS with cause and workaround. Optional: smoke-test (launch packaged exe, load map or main menu). Per [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md) List 64.
- **success criteria:** Packaged build run and outcome documented (SESSION_LOG, VERTICAL_SLICE_CHECKLIST §3, or KNOWN_ERRORS); T1 status set to completed. Deferral with clear doc is acceptable.
- **research_notes:** [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) Package-HomeWorld; Package-HomeWorld.bat; RunUAT; VERTICAL_SLICE_CHECKLIST §3; List 55 scope.
- **steps_or_doc:** Package-HomeWorld.bat; docs/KNOWN_ERRORS.md; docs/workflow/VERTICAL_SLICE_CHECKLIST.md.
- **status:** pending

---

## T2. Demo sign-off (vertical slice)

- **goal:** **Demo sign-off** for the vertical slice: confirm chosen moment and corner are playable/visible; pre-demo checklist run; optional 1–3 min recording. Document sign-off or deferred items in VERTICAL_SLICE_CHECKLIST §3 or SESSION_LOG. Per List 64.
- **success criteria:** Demo sign-off documented (pass or deferred with reason); T2 status set to completed.
- **research_notes:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3; [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Pre-demo verification; [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md) moment/corner.
- **steps_or_doc:** docs/workflow/VERTICAL_SLICE_CHECKLIST.md; docs/CONSOLE_COMMANDS.md.
- **status:** pending

---

## T3. MVP full-scope verification

- **goal:** **MVP full-scope verification**: run through MVP checklist (tutorial loop, Week 1 playtest, pre-demo) or document current state vs MVP full scope (Lists 55–63). Identify any gaps for post–List 64 work. Per List 64.
- **success criteria:** MVP full-scope verification run or doc updated with current state and gaps; T3 status set to completed.
- **research_notes:** [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md); [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md); [MVP_TUTORIAL_PLAN.md](MVP_TUTORIAL_PLAN.md); [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3.
- **steps_or_doc:** docs/workflow/MVP_FULL_SCOPE_10_LISTS.md; docs/CONSOLE_COMMANDS.md; docs/workflow/MVP_TUTORIAL_PLAN.md.
- **status:** pending

---

## T4. CONSOLE_COMMANDS and checklist refresh (List 64)

- **goal:** Refresh [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) and pre-demo/checklist docs for List 64: packaged build and demo sign-off steps; any new commands or run order. Per List 64.
- **success criteria:** CONSOLE_COMMANDS and checklists reflect List 64 (packaged build, demo sign-off); T4 status set to completed.
- **research_notes:** [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md); [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3.
- **steps_or_doc:** docs/CONSOLE_COMMANDS.md; docs/workflow/VERTICAL_SLICE_CHECKLIST.md.
- **status:** pending

---

## T5. MVP full scope List 64 — vertical slice §4 sixty-fourth deliverables

- **goal:** Add **Sixty-fourth-list deliverables** (and MVP full scope List 64 note) to VERTICAL_SLICE_CHECKLIST.md §4: packaged build outcome, demo sign-off, MVP full-scope verification, checklist refresh. Note that this is **list 10 of 10** for MVP full scope (Vision-aligned); after List 64, next lists per VISION and [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md). Per List 64.
- **success criteria:** VERTICAL_SLICE_CHECKLIST §4 contains sixty-fourth-list deliverables and List 64 scope note; T5 status set to completed.
- **research_notes:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §4; [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md) List 64; [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md).
- **steps_or_doc:** docs/workflow/VERTICAL_SLICE_CHECKLIST.md.
- **status:** pending

---

## T6. AUTOMATION_GAPS or KNOWN_ERRORS — List 64 findings

- **goal:** Add or update AUTOMATION_GAPS (and optionally KNOWN_ERRORS) with List 64 findings: packaged build outcome, demo sign-off gaps, MVP full-scope gaps, and suggested next steps for post–List 64. Per List 64.
- **success criteria:** AUTOMATION_GAPS or KNOWN_ERRORS updated with List 64 cycle note or findings; T6 status set to completed.
- **research_notes:** [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md); [KNOWN_ERRORS.md](../KNOWN_ERRORS.md); [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md).
- **steps_or_doc:** docs/AUTOMATION_GAPS.md; docs/KNOWN_ERRORS.md.
- **status:** pending

---

## T7. Buffer prep (post–List 64)

- **goal:** Document **post–List 64** next steps: MVP full scope block (Lists 55–64) complete; next lists per VISION and NEXT_30_DAY_WINDOW. Update ACCOMPLISHMENTS_OVERVIEW or PROJECT_STATE with "MVP full scope 10 lists complete" note. Do not replace CURRENT_TASK_LIST; T10 will do full buffer. Per List 64.
- **success criteria:** Post–List 64 next steps documented (NEXT_30_DAY_WINDOW or PROJECT_STATE); T7 status set to completed.
- **research_notes:** [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md); [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md); [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md); [VISION.md](VISION.md).
- **steps_or_doc:** docs/workflow/NEXT_30_DAY_WINDOW.md; docs/workflow/PROJECT_STATE_AND_TASK_LIST.md.
- **status:** pending

---

## T8. Docs and cycle (combined)

- **goal:** In **one task**, do all of: (1) Ensure VERTICAL_SLICE_CHECKLIST §4 has sixty-fourth-list deliverables (if not done in T5). (2) Update CONSOLE_COMMANDS.md or checklist (List 64) so they reflect current state. (3) Update KNOWN_ERRORS or AUTOMATION_GAPS with cycle note (e.g. "List 64 (MVP full scope): packaged build, demo sign-off; T1–T7 completed."). Success = all three done (or explicitly deferred).
- **success criteria:** Vertical slice §4 sixty-fourth updated; CONSOLE_COMMANDS/checklist updated; KNOWN_ERRORS or AUTOMATION_GAPS cycle note; T8 status set to completed.
- **research_notes:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §4; [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md); [KNOWN_ERRORS.md](../KNOWN_ERRORS.md); [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md).
- **steps_or_doc:** docs/workflow/VERTICAL_SLICE_CHECKLIST.md; docs/CONSOLE_COMMANDS.md; docs/KNOWN_ERRORS.md; docs/AUTOMATION_GAPS.md.
- **status:** pending

---

## T9. Verification (combined)

- **goal:** In **one task**, do all of: (1) If T1–T7 changed C++ or Build.cs, run Build-HomeWorld.bat and confirm build passes. (2) Review VERTICAL_SLICE_CHECKLIST §3–§4 and CONSOLE_COMMANDS for consistency; document outcome in SESSION_LOG or VERTICAL_SLICE_CHECKLIST §3. (3) Run validate_task_list.py and fix any schema issues; update DAILY_STATE "Today" if needed. Success = build green (if applicable), doc review done, list validated.
- **success criteria:** Build run and result logged; doc review done and noted; validate_task_list.py passed; DAILY_STATE updated if needed; T9 status set to completed.
- **research_notes:** Build-HomeWorld.bat; [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3; [SESSION_LOG.md](../SESSION_LOG.md); Content/Python/validate_task_list.py; [DAILY_STATE.md](DAILY_STATE.md).
- **steps_or_doc:** Build-HomeWorld.bat; docs/workflow/VERTICAL_SLICE_CHECKLIST.md; python Content/Python/validate_task_list.py; docs/workflow/DAILY_STATE.md.
- **status:** pending

---

## T10. Buffer: next list prep (ACCOMPLISHMENTS + PROJECT_STATE §4)

- **goal:** Update ACCOMPLISHMENTS_OVERVIEW §4 with sixty-fourth-cycle outcome and PROJECT_STATE_AND_TASK_LIST §4. Do NOT replace CURRENT_TASK_LIST.md (user does that after the loop). Set T1–T10 status to completed where done. **List 64 is the final list of the MVP full scope (10 lists).** After List 64, next lists are per [VISION.md](VISION.md) and [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md). Generate next list per HOW_TO_GENERATE_TASK_LIST when ready.
- **success criteria:** ACCOMPLISHMENTS_OVERVIEW §4 has sixty-fourth-cycle row; PROJECT_STATE §4 says current list complete and points to post–MVP full scope (next lists per VISION/NEXT_30_DAY_WINDOW); T10 status set to completed in CURRENT_TASK_LIST only.
- **research_notes:** [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md); [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md); [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md); [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md).
- **steps_or_doc:** [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md), [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md), [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md).
- **status:** pending

---

**Order:** T1–T7 implementation (packaged build, demo sign-off, MVP full-scope verification, CONSOLE_COMMANDS/checklist refresh, vertical slice §4 sixty-fourth, AUTOMATION_GAPS/KNOWN_ERRORS, buffer prep). T8 = Docs and cycle. T9 = Verification. T10 = Buffer. **After list 64:** MVP full scope (10 lists) complete; next lists per VISION and [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1` when ready.

# Current task list (10-task)

**Last updated:** 2026-03-02 (seventy-third list — **Assets + Steam Demo Phase 3: Packaged build and smoke test**). **Context:** [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) Phase 3 — run packaged build, document outcome; smoke test if exe exists.

**Purpose:** Single ordered list that drives the automation loop. Agents fetch the first **pending** or **in_progress** task; update status when done. Loop exits when no task has status pending or in_progress.

**Convention:** `pending` | `in_progress` | `completed` | `blocked`

**Order:** T1–T7 = Phase 3 implementation (packaged build, smoke test, checklist update, gate, follow-ups); T8 = Docs and cycle; T9 = Verification; T10 = Buffer.

---

## T1. Run packaged build (Phase 3 step 3.1)

- **goal:** Close Editor and any processes using project/Engine binaries. Run `.\Tools\Package-AfterClose.ps1` (or `-CleanStagedBuilds` if Stage failed before). Monitor `Package-HomeWorld.log` for exit code 0. Document outcome (success or failure and reason) in SESSION_LOG and [STEAM_EA_STORE_CHECKLIST.md](STEAM_EA_STORE_CHECKLIST.md) § Current status. If Stage fails with SafeCopyFile (files in use), document and reference [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) Package-HomeWorld workaround.
- **success criteria:** Packaged build was run; outcome (success or documented failure) recorded in SESSION_LOG and STEAM_EA_STORE_CHECKLIST § Current status; Phase 3 step 3.1 gate satisfied; T1 status set to completed.
- **research_notes:** [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) Phase 3 step 3.1; [STEAM_EA_STORE_CHECKLIST.md](STEAM_EA_STORE_CHECKLIST.md) § Packaged build retry, § Current status; [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) Package-HomeWorld; Tools/Package-AfterClose.ps1.
- **steps_or_doc:** Tools/Package-AfterClose.ps1; Package-HomeWorld.log; docs/workflow/STEAM_EA_STORE_CHECKLIST.md; docs/SESSION_LOG.md.
- **status:** completed

---

## T2. Smoke test (Phase 3 step 3.2)

- **goal:** If packaged exe exists at `Saved\StagedBuilds\HomeWorld\WindowsNoEditor\HomeWorld\Binaries\Win64\HomeWorld.exe`, launch it; confirm level loads, character moves, no critical errors. Document result in SESSION_LOG and STEAM_EA_STORE_CHECKLIST § Packaged build. If no exe (build did not produce one), document "smoke test deferred until packaged build succeeds" with reason.
- **success criteria:** Smoke test run and result documented (pass or deferred with reason); T2 status set to completed.
- **research_notes:** [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) Phase 3 step 3.2; [STEAM_EA_STORE_CHECKLIST.md](STEAM_EA_STORE_CHECKLIST.md) § Packaged build.
- **steps_or_doc:** Saved/StagedBuilds/.../HomeWorld.exe; docs/workflow/STEAM_EA_STORE_CHECKLIST.md; docs/SESSION_LOG.md.
- **status:** completed

---

## T3. Update STEAM_EA_STORE_CHECKLIST § Current status

- **goal:** Add a **seventy-third list (Phase 3)** entry to [STEAM_EA_STORE_CHECKLIST.md](STEAM_EA_STORE_CHECKLIST.md) § Current status: packaged build run outcome (T1), smoke test outcome (T2). Include next steps (e.g. if Stage failed: close processes, use -CleanStagedBuilds, re-run; if exe exists: smoke-test path and checklist checkboxes).
- **success criteria:** STEAM_EA_STORE_CHECKLIST § Current status has list 73 / Phase 3 outcome; T3 status set to completed.
- **research_notes:** [STEAM_EA_STORE_CHECKLIST.md](STEAM_EA_STORE_CHECKLIST.md) § Current status; [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) Phase 3.
- **steps_or_doc:** docs/workflow/STEAM_EA_STORE_CHECKLIST.md.
- **status:** completed

---

## T4. Phase 3 gate — document completion

- **goal:** Confirm Phase 3 steps 3.1 and 3.2 are complete (build run and outcome documented; smoke test or deferred). Add a one-line **Phase 3 gate — List 73** outcome to [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) Phase 3 section (e.g. "Phase 3 gate met: packaged build run, outcome recorded; smoke test pass/deferred."). Optionally append short summary to SESSION_LOG.
- **success criteria:** Phase 3 gate outcome in phased approach doc; T4 status set to completed.
- **research_notes:** [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) Phase 3 gate; [SESSION_LOG.md](../SESSION_LOG.md).
- **steps_or_doc:** docs/workflow/ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md; docs/SESSION_LOG.md.
- **status:** completed

---

## T5. Vertical slice §4 seventy-third-list deliverables

- **goal:** Add a row or entry to [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §4 for "Seventy-third list (Phase 3 Steam Demo): packaged build run, smoke test (or deferred); Phase 3 gate."
- **success criteria:** VERTICAL_SLICE_CHECKLIST §4 has seventy-third-list row; T5 status set to completed.
- **research_notes:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §4; [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) Phase 3.
- **steps_or_doc:** docs/workflow/VERTICAL_SLICE_CHECKLIST.md §4.
- **status:** completed

---

## T6. KNOWN_ERRORS / checklist ref if Stage failed

- **goal:** If T1 resulted in Stage failure (e.g. SafeCopyFile files in use), ensure STEAM_EA_STORE_CHECKLIST § Current status and/or SESSION_LOG reference [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) and the retry procedure (§ Packaged build retry when Stage failed). If build succeeded, no change required; document "no Stage failure" or skip.
- **success criteria:** If Stage failed, KNOWN_ERRORS and retry procedure are referenced in checklist or SESSION_LOG; if build succeeded, T6 marked completed with note; T6 status set to completed.
- **research_notes:** [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) Package-HomeWorld; [STEAM_EA_STORE_CHECKLIST.md](STEAM_EA_STORE_CHECKLIST.md) § Packaged build retry.
- **steps_or_doc:** docs/KNOWN_ERRORS.md; docs/workflow/STEAM_EA_STORE_CHECKLIST.md; docs/SESSION_LOG.md.
- **status:** completed

---

## T7. Phase 4 prep note

- **goal:** In PROJECT_STATE_AND_TASK_LIST §4 or ACCOMPLISHMENTS_OVERVIEW §4, ensure "Next" after list 73 mentions Phase 4 (Steam Demo store draft) per ASSETS_AND_STEAM_DEMO_PHASED_APPROACH. No requirement to run Phase 4 in this list.
- **success criteria:** PROJECT_STATE or ACCOMPLISHMENTS notes "after list 73 → Phase 4 (store draft)" or equivalent; T7 status set to completed.
- **research_notes:** [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) §4; [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md) §4; [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) Phase 4.
- **steps_or_doc:** docs/workflow/PROJECT_STATE_AND_TASK_LIST.md; docs/workflow/ACCOMPLISHMENTS_OVERVIEW.md.
- **status:** completed

---

## T8. Docs and cycle (combined)

- **goal:** In **one task**, do all of: (1) Ensure VERTICAL_SLICE_CHECKLIST §4 has seventy-third-list row (if not in T5). (2) CONSOLE_COMMANDS or workflow doc updated if any new verification steps. (3) KNOWN_ERRORS or AUTOMATION_GAPS cycle note for list 73 (e.g. "Seventy-third list (Phase 3 Steam Demo): packaged build run, smoke test; Phase 3 gate."). Success = all three done (or explicitly deferred).
- **success criteria:** Vertical slice §4 seventy-third updated; CONSOLE_COMMANDS/workflow current if needed; KNOWN_ERRORS or AUTOMATION_GAPS cycle note; T8 status set to completed.
- **research_notes:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §4; [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md); [KNOWN_ERRORS.md](../KNOWN_ERRORS.md); [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md).
- **steps_or_doc:** docs/workflow/VERTICAL_SLICE_CHECKLIST.md; docs/CONSOLE_COMMANDS.md; docs/KNOWN_ERRORS.md; docs/AUTOMATION_GAPS.md.
- **status:** completed

---

## T9. Verification (combined)

- **goal:** In **one task**, do all of: (1) If T1–T7 changed C++ or Build.cs, run Build-HomeWorld.bat and confirm build passes. (2) Review VERTICAL_SLICE_CHECKLIST §3–§4 and STEAM_EA_STORE_CHECKLIST for consistency; document outcome in SESSION_LOG or checklist. (3) Run validate_task_list.py and fix any schema issues; update DAILY_STATE "Today" if needed. Success = build green (if applicable), doc review done, list validated.
- **success criteria:** Build run and result logged if applicable; doc review done and noted; validate_task_list.py passed; DAILY_STATE updated if needed; T9 status set to completed.
- **research_notes:** Build-HomeWorld.bat; [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3–§4; [STEAM_EA_STORE_CHECKLIST.md](STEAM_EA_STORE_CHECKLIST.md); [SESSION_LOG.md](../SESSION_LOG.md); Content/Python/validate_task_list.py; [DAILY_STATE.md](DAILY_STATE.md).
- **steps_or_doc:** Build-HomeWorld.bat; docs/workflow/VERTICAL_SLICE_CHECKLIST.md; docs/workflow/STEAM_EA_STORE_CHECKLIST.md; python Content/Python/validate_task_list.py; docs/workflow/DAILY_STATE.md.
- **status:** completed

---

## T10. Buffer: next list prep (ACCOMPLISHMENTS + PROJECT_STATE §4)

- **goal:** Update ACCOMPLISHMENTS_OVERVIEW §4 with seventy-third-list (Phase 3 Steam Demo) outcome and PROJECT_STATE_AND_TASK_LIST §4. Do NOT replace CURRENT_TASK_LIST (user does that after the loop). Set T1–T10 status to completed where done. **Next:** Phase 4 (store draft) skipped; generate next list per HOW_TO_GENERATE_TASK_LIST when ready (focus per NEXT_30_DAY_WINDOW).
- **success criteria:** ACCOMPLISHMENTS_OVERVIEW §4 has seventy-third-cycle row; PROJECT_STATE §4 says list 73 complete and next = generate list (Phase 4 skipped); T10 status set to completed in CURRENT_TASK_LIST only.
- **research_notes:** [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md); [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md); [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md).
- **steps_or_doc:** HOW_TO_GENERATE_TASK_LIST.md; ACCOMPLISHMENTS_OVERVIEW.md; PROJECT_STATE_AND_TASK_LIST.md; ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md.
- **status:** completed

---

**Order:** T1–T7 = Phase 3 (packaged build, smoke test, checklist update, gate, vertical slice §4, KNOWN_ERRORS ref if needed, Phase 4 prep). T8 = Docs and cycle. T9 = Verification. T10 = Buffer. **After list 73:** Phase 4 skipped; generate next list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1` when ready.

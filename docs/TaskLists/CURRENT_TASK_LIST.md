> This is the active task list. Start every session at `Docs/context/SESSION_START.md`.

# Current task list (seventy-fourth 10-task list — Polish readiness automation)

**Last updated:** 2026-10-06 (seventy-fourth list — **Polish readiness automation**). **Context:** List 73 (Phase 3 packaged build + smoke test) complete. Phase 4 (store draft) skipped. Next focus: agent-owned polish readiness checks, validator path fix, SESSION_START gate hardening, POLISH_ASSET_BOARD cross-link, and KNOWN_ERRORS/DAILY_STATE hygiene. Human-gated items (PIE cloud descent, measure_ue_island.py, POLISH_ASSET_BOARD.json triage) are documented and await Luke.

**Purpose:** Single ordered list that drives the automation loop. Agents fetch the first **pending** or **in_progress** task; update status when done. Loop exits when no task has status pending or in_progress.

**Convention:** ``pending`` | ``in_progress`` | ``completed`` | ``blocked``

**Phase:** Rapid prototyping — T1–T7 = implementation, T8 = Docs and cycle (combined), T9 = Verification (combined), T10 = Buffer.

---

## T1. Log validate_task_list.py path fix in KNOWN_ERRORS

- **goal:** The validator was hardcoded to ``docs/workflow/CURRENT_TASK_LIST.md`` but the file lives at ``docs/TaskLists/CURRENT_TASK_LIST.md``. The fix was applied in this session. Log the root cause and fix in ``docs/KNOWN_ERRORS.md`` — add a ``### validate_task_list.py path`` entry with symptom, cause, and fix. Also check ``.github/workflows/validate.yml`` for the legacy path reference.
- **success criteria:** ``docs/KNOWN_ERRORS.md`` has a ``### validate_task_list.py path`` entry; T1 status set to completed.
- **research_notes:** Fix applied in ``Content/Python/validate_task_list.py`` line 17 (two-path fallback: TaskLists/ primary, workflow/ legacy). CI validate.yml may reference legacy path — check and note. Open only the format header and matching ``###`` section of KNOWN_ERRORS; never load the whole file.
- **steps_or_doc:** ``docs/KNOWN_ERRORS.md``; ``Content/Python/validate_task_list.py``; ``.github/workflows/validate.yml``.
- **status:** completed

---

## T2. Harden check_session_start.py: verify question-before-discovery gate

- **goal:** Add or verify that ``Content/Python/check_session_start.py`` checks for the "Always ask one question before using any discovery tool" rule (SESSION_START line 49). The check should confirm the exact sentence (or stable token) is present so a future edit that removes the gate is caught by CI.
- **success criteria:** ``check_session_start.py`` exits 0 and covers the question-before-discovery gate; ``python Content/Python/check_session_start.py`` shows ``SESSION_START door check: pass``; T2 status set to completed.
- **research_notes:** SESSION_START.md line 49: "Always ask one question, in the current conversation, to align on the task before using any discovery tool, and carry on from the answer." Stable token: ``ask one question`` or ``before using any discovery tool``. Extend the ``REQUIRED`` list or add a ``QUESTION_GATE_PATTERN``.
- **steps_or_doc:** ``Content/Python/check_session_start.py``; ``Docs/context/SESSION_START.md`` section "Ending the reads".
- **status:** pending

---

## T3. Cross-link POLISH_ASSET_BOARD to 37_POLISH_PASS_PROCESS and write HOW_TO doc

- **goal:** (1) Verify ``_source`` in ``docs/qa/POLISH_ASSET_BOARD.json`` matches the actual section in ``Docs/37_POLISH_PASS_PROCESS.md``. (2) Write ``docs/qa/POLISH_ASSET_BOARD_HOW_TO.md`` (10–15 lines): mechanical fill-in instructions for Luke — open board, look at each asset in Editor, set ``stage`` (S0–S5) + ``priority`` (1–10). No taste calls. (3) Add a door row to SESSION_START door table if "polish" is not already there.
- **success criteria:** ``_source`` verified or corrected; ``POLISH_ASSET_BOARD_HOW_TO.md`` committed (10–15 lines, no taste calls); SESSION_START door table optionally updated; T3 status set to completed.
- **research_notes:** ``docs/qa/POLISH_ASSET_BOARD.json`` ``_source`` = "Docs/37_POLISH_PASS_PROCESS.md section 3". Open ``Docs/37_POLISH_PASS_PROCESS.md`` to verify §3 contains stage ladder. Do NOT fill in stages or priorities. SESSION_START door table is lines 53–59.
- **steps_or_doc:** ``docs/qa/POLISH_ASSET_BOARD.json``; ``Docs/37_POLISH_PASS_PROCESS.md`` §3; ``Docs/context/SESSION_START.md`` (door table); ``docs/qa/POLISH_ASSET_BOARD_HOW_TO.md`` (create).
- **status:** pending

---

## T4. SESSION_START read order: verify no silent bloat has crept back in

- **goal:** Confirm no new unconditional reads have been added to SESSION_START since the list 73 optimization (commit ``994c2c9``). Run ``git diff 994c2c9..HEAD -- Docs/context/SESSION_START.md`` and check for any new file reads that are not in the named-pack or extra-reads-by-task tables. If found, move to named-pack or log in AUTOMATION_GAPS. If none found, set T4 to completed with a note.
- **success criteria:** SESSION_START.md confirmed to have no new unconditional reads beyond the two defined start reads; any new unconditional reads moved to named-pack or logged; T4 status set to completed.
- **research_notes:** Two unconditional reads: (1) route-context.md through ``## How to detect the state``, (2) ROUTE_INDEX.md. All other files are in the named-pack or extra-reads-by-task tables. Commit ``994c2c9`` is the baseline for optimization.
- **steps_or_doc:** ``Docs/context/SESSION_START.md`` section "Read order"; ``git diff 994c2c9..HEAD -- Docs/context/SESSION_START.md``; ``docs/Automation/AUTOMATION_GAPS.md``.
- **status:** pending

---

## T5. Update DAILY_STATE to current state (list 74 / polish readiness)

- **goal:** ``docs/TaskLists/DAILY_STATE.md`` is stale (references WAVE F audit). Update: **Yesterday** = list 73 complete (Phase 3 packaged build + smoke test; validate_task_list.py path fix + question-gate in this session); **Today** = T2 (check_session_start.py question gate); **Tomorrow** = T3.
- **success criteria:** DAILY_STATE.md Yesterday/Today/Tomorrow reflect list 74 state; T5 status set to completed.
- **research_notes:** Current state: list 73 complete (2026-03-09), list 74 now active. T1 completed (validate_task_list.py fix). check_session_start.py PASS. npm run verify:fast PASS (139/139). test_polish_readiness.py PASS (219/219). Human-gated: PIE cloud descent, measure_ue_island.py, POLISH_ASSET_BOARD triage.
- **steps_or_doc:** ``docs/TaskLists/DAILY_STATE.md``.
- **status:** completed

---

## T6. Run and document test_polish_readiness.py result in SESSION_LOG

- **goal:** ``pytest Content/Python/tests/test_polish_readiness.py`` returned 219/219 PASS in this session. Record this in ``docs/SESSION_LOG.md`` as a verification event for list 74. Add a ``### List 74 (2026-10-06)`` subsection with 3–5 lines: date, test result, validate_task_list.py fix, npm verify:fast PASS.
- **success criteria:** SESSION_LOG.md has a list 74 entry with test_polish_readiness.py PASS; T6 status set to completed.
- **research_notes:** pytest exit 0; 219 passed, 90 subtests in 3.62s. Append to ``docs/SESSION_LOG.md`` — most recent section or new ``### List 74`` subsection.
- **steps_or_doc:** ``docs/SESSION_LOG.md``; test result: 219/219 PASS.
- **status:** completed

---

## T7. Verify and cross-link human-gated items in SESSION_LOG for Luke

- **goal:** Confirm ``Docs/handoffs/SESSION_HANDOFF_DESCENT_AND_DOOR.md`` still accurately reflects current state. Add a ``## Human-gated items (list 74)`` section to ``docs/SESSION_LOG.md`` with the three items: (a) PIE cloud descent — launch from GP_GlideStart, press E; (b) measure_ue_island.py — run in Editor on L_VS_MVP_Markers; (c) POLISH_ASSET_BOARD triage — open board + 37_POLISH_PASS_PROCESS §3, fill per POLISH_ASSET_BOARD_HOW_TO.md. No recipes or tutorials.
- **success criteria:** SESSION_LOG.md has Human-gated items section with 3 items and doc pointers; handoff file confirmed accurate or updated if stale; T7 status set to completed.
- **research_notes:** Handoff "Next action" items 1–3 match the three human-gated items above. Check that "Evidence" in the handoff still matches commit ``d6c9c3d``. If the handoff is stale (wrong commit or wrong paths), update "Changed paths" and "Evidence" to current HEAD.
- **steps_or_doc:** ``Docs/handoffs/SESSION_HANDOFF_DESCENT_AND_DOOR.md``; ``docs/SESSION_LOG.md``.
- **status:** pending

---

## T8. Docs and cycle (combined)

- **goal:** In **one task**: (1) Add a vertical slice §4 seventy-fourth-list row. (2) AUTOMATION_GAPS cycle note for list 74 (no new gaps from T1–T7; validate_task_list.py path fixed; human-gated items documented). (3) Confirm CONSOLE_COMMANDS doesn't need updating (no new console commands in list 74). Success = all three done or explicitly deferred.
- **success criteria:** VERTICAL_SLICE_CHECKLIST §4 has seventy-fourth-list row; AUTOMATION_GAPS cycle note; CONSOLE_COMMANDS confirmed no change; T8 status set to completed.
- **research_notes:** VERTICAL_SLICE_CHECKLIST — search in ``docs/workflow/`` and ``docs/TaskLists/``. AUTOMATION_GAPS at ``docs/Automation/AUTOMATION_GAPS.md``. CONSOLE_COMMANDS at ``docs/CONSOLE_COMMANDS.md``. No new console commands in T1–T7.
- **steps_or_doc:** VERTICAL_SLICE_CHECKLIST (check both paths); ``docs/Automation/AUTOMATION_GAPS.md``; ``docs/CONSOLE_COMMANDS.md``.
- **status:** pending

---

## T9. Verification (combined)

- **goal:** In **one task**: (1) No C++/Build.cs changes in list 74 — no Safe-Build required; confirm. (2) ``python Content/Python/validate_task_list.py`` exit 0. (3) ``python Content/Python/check_session_start.py`` PASS. (4) ``npm run verify:fast`` PASS. (5) Review VERTICAL_SLICE_CHECKLIST §3–§4 for consistency; document in SESSION_LOG or checklist. (6) Update DAILY_STATE if needed. Success = all checks green.
- **success criteria:** validate_task_list.py exit 0; check_session_start.py PASS; npm run verify:fast PASS; doc review done; DAILY_STATE current; T9 status set to completed.
- **research_notes:** validate_task_list.py path fix (T1) makes it exit 0 on TaskLists path. check_session_start.py question-gate check (T2) should be in place. npm run verify:fast was 139/139 PASS at session start. No C++/Build.cs changes in list 74.
- **steps_or_doc:** ``Content/Python/validate_task_list.py``; ``Content/Python/check_session_start.py``; ``npm run verify:fast``; VERTICAL_SLICE_CHECKLIST §3–§4; ``docs/TaskLists/DAILY_STATE.md``.
- **status:** pending

---

## T10. Buffer: next list prep (ACCOMPLISHMENTS + PROJECT_STATE §4)

- **goal:** Update ACCOMPLISHMENTS_OVERVIEW §4 with seventy-fourth-list outcome: validate_task_list.py path fix, check_session_start.py question-gate, POLISH_ASSET_BOARD_HOW_TO.md, SESSION_LOG/DAILY_STATE updated, human-gated items documented. Update PROJECT_STATE §4: list 74 complete; next = generate list 75 per HOW_TO_GENERATE_TASK_LIST. Do NOT replace CURRENT_TASK_LIST.
- **success criteria:** ACCOMPLISHMENTS_OVERVIEW §4 has seventy-fourth-cycle row; PROJECT_STATE §4 says list 74 complete; T10 status set to completed.
- **research_notes:** ACCOMPLISHMENTS_OVERVIEW at ``docs/TaskLists/ACCOMPLISHMENTS_OVERVIEW.md``. PROJECT_STATE at ``docs/TaskLists/PROJECT_STATE_AND_TASK_LIST.md``. Update §4 only.
- **steps_or_doc:** ``docs/TaskLists/ACCOMPLISHMENTS_OVERVIEW.md`` §4; ``docs/TaskLists/PROJECT_STATE_AND_TASK_LIST.md`` §4.
- **status:** pending

---

**Order:** T1 = validate_task_list.py path KNOWN_ERRORS (completed). T2 = check_session_start.py question gate. T3 = POLISH_ASSET_BOARD cross-link + HOW_TO. T4 = SESSION_START read order audit. T5 = DAILY_STATE update (completed). T6 = test_polish_readiness SESSION_LOG entry (completed). T7 = human-gated items doc. T8 = Docs and cycle (combined). T9 = Verification (combined). T10 = Buffer.

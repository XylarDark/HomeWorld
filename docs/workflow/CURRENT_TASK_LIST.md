# Current task list (10-task)

**Last updated:** 2026-03-06 (twenty-ninth list, **rapid prototyping**: 8 implementation + 2 verification per PROJECT_STATE §0). **Context:** Run 3 of 4 toward polished MVP; see [MVP_GAP_ANALYSIS.md](MVP_GAP_ANALYSIS.md).

**Vision alignment:** Day = cooking/meals (caretaker), resources/building/exploring (explorer/builder); goal = build up **love** → bonuses at night. **Planetoid:** Homestead lands on planetoid, you venture out; complete planetoid → move to next. **Combat:** Convert not kill (strip sin → loved form); converted foes = vendors, helpers, quest givers, pets/workers. **Combat variety:** Defend = ranged/ground AOE; planetoid = combos + single-target. See [VISION.md](VISION.md).

**Purpose:** Single ordered list that drives the automation loop. Agents fetch the first **pending** or **in_progress** task; update status when done. Loop exits when no task has status pending or in_progress.

**Convention:** `pending` | `in_progress` | `completed` | `blocked`

**Order:** T1–T8 = implementation (testable); T9 = verification; T10 = buffer.

---

## T1. Pre-demo verification entry point: link §3 and CONSOLE_COMMANDS from one doc

- **goal:** Add a short "Pre-demo verification" or "How to run the pre-demo checklist" section to CONVENTIONS.md or CONSOLE_COMMANDS.md that points testers to (1) VERTICAL_SLICE_CHECKLIST §3 (step-by-step run sequence) and (2) CONSOLE_COMMANDS for hw.* commands. Single entry point so someone opening the project knows where to start for §3. Success = One doc contains the entry point and links to §3 and CONSOLE_COMMANDS.
- **success criteria:** Pre-demo verification entry point (with links to §3 and CONSOLE_COMMANDS) exists in CONVENTIONS or CONSOLE_COMMANDS; T1 status set to completed.
- **research_notes:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3 (step-by-step from twenty-seventh T5); [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md); [CONVENTIONS.md](../CONVENTIONS.md).
- **steps_or_doc:** docs/CONVENTIONS.md or docs/CONSOLE_COMMANDS.md.
- **status:** completed

---

## T2. pie_test_runner results: add interpretation doc or in-script summary

- **goal:** Add a short reference so testers know how to read Saved/pie_test_results.json: which keys indicate pass/fail, what each check means (e.g. pie_active, character_spawned, on_ground, placement_available, save_load_round_trip). Options: (1) Add a section to VERTICAL_SLICE_CHECKLIST §3 or CONVENTIONS, or (2) Add a doc pie_test_results_interpretation.md, or (3) Ensure pie_test_runner writes a one-line summary to Output Log or a small summary file. Success = Interpretation doc or in-script summary exists; testers can interpret results without guessing.
- **success criteria:** pie_test_results interpretation (doc or script summary) exists; T2 status set to completed.
- **research_notes:** Content/Python/pie_test_runner.py; Saved/pie_test_results.json structure; [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3.
- **steps_or_doc:** docs/workflow/VERTICAL_SLICE_CHECKLIST.md or docs/CONVENTIONS.md or Content/Python/pie_test_runner.py.
- **status:** completed

---

## T3. Combat stub testability: document how to read DefendCombatMode / PlanetoidCombatStyle in PIE

- **goal:** Twenty-sixth list added DefendCombatMode (Ranged | GroundAOE) and PlanetoidCombatStyle / ComboHitCount stubs. Document how a tester can verify these in PIE — e.g. which console command or HUD line shows the current mode/count, or where to look in the log. Add to CONSOLE_COMMANDS.md "Key PIE-test usage" or to DEFEND_COMBAT.md / PLANETOID_COMBAT.md a "Testing in PIE" subsection. Success = Doc or CONSOLE_COMMANDS explains how to read combat stubs in PIE.
- **success criteria:** Combat stub testability documented (how to read DefendCombatMode, PlanetoidCombatStyle, or ComboHitCount in PIE); T3 status set to completed.
- **research_notes:** [DEFEND_COMBAT.md](../tasks/DEFEND_COMBAT.md); [PLANETOID_COMBAT.md](../tasks/PLANETOID_COMBAT.md); [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md); twenty-sixth list T1–T2 stubs.
- **steps_or_doc:** docs/CONSOLE_COMMANDS.md or docs/tasks/DEFEND_COMBAT.md, PLANETOID_COMBAT.md.
- **status:** completed

---

## T4. MVP polish readiness: add "What to do in Editor for polish" section

- **goal:** Add to MVP_GAP_ANALYSIS.md (or a short linked doc) a section "What to do in Editor for polish" that lists the main categories of work the user will do after the fourth run: e.g. lighting pass, LOD check, asset placement tweaks, animation polish, UX/HUD polish, 2–5 min stability run. So when they switch to Editor polish they have a checklist. Success = Section or doc exists with Editor polish checklist.
- **success criteria:** "What to do in Editor for polish" section or doc exists; T4 status set to completed.
- **research_notes:** [MVP_GAP_ANALYSIS.md](MVP_GAP_ANALYSIS.md); VISION vertical slice; PROTOTYPE_SCOPE moment/corner.
- **steps_or_doc:** docs/workflow/MVP_GAP_ANALYSIS.md or new doc linked from it.
- **status:** completed

---

## T5. Vertical slice sign-off: add "as of" date or run progress note

- **goal:** In VERTICAL_SLICE_SIGNOFF.md or VERTICAL_SLICE_CHECKLIST (e.g. at top or in demo-readiness section), add an "As of" date or "Run N of 4 toward polished MVP" note so the slice state is timestamped and the next list (run 4) can update it. Success = Sign-off or checklist has date or run note.
- **success criteria:** Vertical slice sign-off or checklist has "as of" date or run progress note; T5 status set to completed.
- **research_notes:** [VERTICAL_SLICE_SIGNOFF.md](VERTICAL_SLICE_SIGNOFF.md); [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md); run 3 of 4.
- **steps_or_doc:** docs/workflow/VERTICAL_SLICE_SIGNOFF.md or VERTICAL_SLICE_CHECKLIST.md.
- **status:** completed

---

## T6. Vertical slice checklist: update §4 with twenty-ninth-list deliverables

- **goal:** Update VERTICAL_SLICE_CHECKLIST §4 with the twenty-ninth-list deliverables once T1–T5 are done (pre-demo entry point, pie_test_results interpretation, combat stub testability, MVP polish readiness section, vertical slice date/run note). List what is testable and how to verify. Success = §4 reflects twenty-ninth outcomes.
- **success criteria:** VERTICAL_SLICE_CHECKLIST §4 updated with twenty-ninth-list outcomes and verification steps; T6 status set to completed.
- **research_notes:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §4; twenty-eighth list §4 pattern.
- **steps_or_doc:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md).
- **status:** completed

---

## T7. Packaged build: optional retry or document outcome

- **goal:** Optionally run Package-AfterClose.ps1 (with Editor and HomeWorld processes closed) and document outcome in STEAM_EA_STORE_CHECKLIST or KNOWN_ERRORS. If not running package this list, document "T7 twenty-ninth: package not run; use Package-AfterClose.ps1 when ready" in checklist. Success = Retry attempted and outcome documented, or skip documented; T7 status set to completed.
- **success criteria:** Package retry run and outcome documented, or skip documented; T7 status set to completed.
- **research_notes:** [STEAM_EA_STORE_CHECKLIST.md](STEAM_EA_STORE_CHECKLIST.md); [KNOWN_ERRORS.md](../KNOWN_ERRORS.md); Tools/Package-AfterClose.ps1; Stage/files-in-use prior lists.
- **steps_or_doc:** [KNOWN_ERRORS.md](../KNOWN_ERRORS.md), [STEAM_EA_STORE_CHECKLIST.md](STEAM_EA_STORE_CHECKLIST.md).
- **status:** completed

---

## T8. KNOWN_ERRORS or AUTOMATION_GAPS: update with findings from this cycle

- **goal:** After T1–T7, update KNOWN_ERRORS.md or AUTOMATION_GAPS.md with any new findings from this cycle. If no new errors, add a brief cycle note (e.g. "Twenty-ninth list: T1–T8 completed; no new errors") so the next list generator has context. Success = KNOWN_ERRORS or AUTOMATION_GAPS updated with cycle findings or cycle note; T8 status set to completed.
- **success criteria:** KNOWN_ERRORS or AUTOMATION_GAPS updated; T8 status set to completed.
- **research_notes:** [KNOWN_ERRORS.md](../KNOWN_ERRORS.md); [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md); 07-ai-agent-behavior (error recurrence prevention).
- **steps_or_doc:** docs/KNOWN_ERRORS.md, docs/AUTOMATION_GAPS.md.
- **status:** completed

---

## T9. Verification: Run PIE pre-demo checklist and document results

- **goal:** Run the single verification gate: with Editor open and DemoMap (or Homestead) loaded, start PIE, run pie_test_runner.py via MCP or Tools > Execute Python Script, document outcome in VERTICAL_SLICE_CHECKLIST §3 or SESSION_LOG (e.g. Saved/pie_test_results.json present, pass/fail summary). If Editor/MCP is not connected, document that and the steps to run §3 when Editor is available. Success = PIE was running when pie_test_runner executed (or "not connected" documented); outcome documented in §3 or SESSION_LOG; T9 status set to completed.
- **success criteria:** PIE pre-demo run attempted; outcome documented in §3 or SESSION_LOG; T9 status set to completed.
- **research_notes:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3; pie_test_runner.py; T1 entry point when added.
- **steps_or_doc:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3, docs/SESSION_LOG.md.
- **status:** completed

---

## T10. Buffer: next list generation prep (ACCOMPLISHMENTS + PROJECT_STATE §4)

- **goal:** Update ACCOMPLISHMENTS_OVERVIEW §4 with twenty-ninth-cycle outcome and PROJECT_STATE_AND_TASK_LIST §4 so the next list can be generated; set T1–T10 status to completed where done. Do NOT replace or regenerate CURRENT_TASK_LIST.md (user does that after the loop exits).
- **success criteria:** ACCOMPLISHMENTS_OVERVIEW §4 has twenty-ninth-cycle row (outcome + Next = generate new list); PROJECT_STATE §4 says current list complete and points to HOW_TO_GENERATE_TASK_LIST and Start-AllAgents-InNewWindow.ps1; T10 status set to completed in CURRENT_TASK_LIST only.
- **research_notes:** HOW_TO_GENERATE_TASK_LIST; ACCOMPLISHMENTS_OVERVIEW; PROJECT_STATE_AND_TASK_LIST; TASK_LIST_REPEATS_LOG; NEXT_SESSION_PROMPT T10 clause (do not replace task list).
- **steps_or_doc:** [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md), [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md), [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md).
- **status:** completed

---

**Order:** T1–T8 implementation, T9 verification, T10 buffer. See [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) §0 (phase) and §4 (current list).

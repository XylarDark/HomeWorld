# Company of agents: roles, accountability, continuity

**Goal:** A small "company" of agents with **named roles** that **keep each other accountable** and ensure **development continues through all errors**—no silent drop, no dead end without a clear handoff.

---

## Principles

1. **Named roles** — Each agent has a role (Developer, Fixer, Guardian, Refiner, **Gap-Solver**). Prompts and logs use these names so behavior is consistent and auditable.
2. **Accountability** — Each role has explicit responsibilities. The next role or the system checks that they were met (e.g. Guardian ensures a report exists if the loop isn't resolved; Refiner uses run history to improve rules).
3. **Continuity** — Every failure path leads to either a **retry** (loop continues) or a **clear handoff** (report + next steps for human or re-run). Development never "stops" without a documented reason and follow-up.

---

## Roles

| Role | Invoked by | Responsibility | Accountable for | Handoff |
|------|------------|----------------|-----------------|---------|
| **Developer** | RunAutomationLoop (main loop) | Do the current day's work from 30_DAY_IMPLEMENTATION_STATUS; update state, SESSION_LOG, DAILY_STATE; write next prompt. | Completing or clearly deferring the task; updating implementation status and session log. | On success: next round or exit 0. On failure: **Fixer** is invoked by the Watcher. |
| **Fixer** | Watcher (when Developer exits non-zero) | Diagnose from automation_errors.log and loop log; apply fix (code, config, KNOWN_ERRORS, docs); document what was done. | Applying a concrete fix; appending to SESSION_LOG; **when the fix is generalizable** (e.g. you added a KNOWN_ERRORS entry or a rule would prevent recurrence), write agent_feedback_this_run.json with suggested_rule_update or suggested_strategy so Refiner can update rules from run history. | On success: Watcher re-runs Developer. If same failure recurs: **Guardian** is invoked. If MaxFixRounds reached: **Guardian** then exit. |
| **Guardian** | Watcher (when same failure recurs or MaxFixRounds reached) | Break the loop: try a *different* fix (e.g. skip day, block with reason, AUTOMATION_GAPS) or, if unresolved, write a full report for the user. | Either resolving the loop or writing **Saved/Logs/automation_loop_breaker_report.md** (summary, what was tried, recommended steps). The script ensures the report exists if the Guardian doesn't write it. | Report exists → user (or Refiner) continues. Re-run Watch-AutomationAndFix to resume. |
| **Refiner** | On-demand or after Guardian report | Read agent_run_history.ndjson, automation_errors.log, and (if present) automation_loop_breaker_report.md; update .cursor/rules, KNOWN_ERRORS.md, AGENTS.md, or workflow docs so the same failures don't recur. | Turning run history and suggestions into concrete rule/strategy updates; optionally checking that Fixer and Guardian left the expected artifacts (SESSION_LOG, report). | Updated rules and docs; next run benefits. See [AUTOMATION_REFINEMENT.md](AUTOMATION_REFINEMENT.md). |
| **Gap-Solver** | On-demand or after a gap is logged / after Guardian report | Read [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) and [GAP_SOLUTIONS_RESEARCH.md](../GAP_SOLUTIONS_RESEARCH.md); for each gap without a solution implemented, implement programmatic solution first, then GUI automation stub or docs; update AUTOMATION_GAPS and GAP_SOLUTIONS_RESEARCH. | Implementing or documenting a solution for every logged gap; updating the Research log and closing or annotating gaps. | Updated AUTOMATION_GAPS / GAP_SOLUTIONS_RESEARCH; optionally SESSION_LOG. Run via `.\Tools\Run-GapSolverAgent.ps1` or **run-gap-solver** command. |

---

## Continuity guarantee

- **Developer fails** → Watcher invokes **Fixer**. No silent exit; Fixer is always run (unless loop detected, then Guardian).
- **Same failure again** → Watcher invokes **Guardian** instead of Fixer. Guardian must either resolve or write the report.
- **Guardian cannot resolve** → Report is ensured (script writes minimal one if Guardian didn't). User has a single file to read and clear next steps (fix manually, re-run Watch-AutomationAndFix). The report may recommend running the **Gap-Solver** when the loop was caused by an automation gap.
- **Refiner** (optional) → Runs on run history and report to update rules/strategy so the next cycle is less likely to hit the same failure.
- **Gap-Solver** (optional) → Runs when a gap has been logged (e.g. in AUTOMATION_GAPS.md) or after Guardian report that mentions gaps. Implements solutions so the gap is closed or documented; no separate "manual steps" for the user.

Development only "pauses" at a **documented** handoff: either all days done (exit 0) or a report file with recommended steps and re-run instruction.

---

## How they keep each other accountable

- **Developer → Fixer:** Developer's failure (exit code + errors log) is the input to Fixer. Fixer is accountable for leaving a fix and SESSION_LOG entry; if they don't, the next run (or Refiner) can see the gap in run history.
- **Fixer → Guardian:** If the same exit code recurs, the Watcher assumes Fixer's fix wasn't sufficient and invokes Guardian. Guardian is accountable for either breaking the loop or writing the report; the script enforces the report if missing.
- **Guardian → Refiner / Gap-Solver / user:** Guardian's report and agent_feedback_this_run (merged into run history) are the input for Refiner or a human. Refiner is accountable for turning that into rule/strategy changes. When the report (or AUTOMATION_GAPS) mentions an automation gap, **Gap-Solver** is accountable for implementing a solution and updating AUTOMATION_GAPS/GAP_SOLUTIONS_RESEARCH.
- **Developer / Guardian → Gap-Solver:** When a step is logged to AUTOMATION_GAPS.md, the Gap-Solver is the role responsible for implementing solutions. Run `.\Tools\Run-GapSolverAgent.ps1` on-demand or after a Guardian report that references gaps.
- **Run history:** Every run (Developer, Fixer, Guardian) is recorded in **Saved/Logs/agent_run_history.ndjson**. Refiner (or a human) can audit that each role did its part (e.g. Fixer rounds have suggested_rule_update when appropriate; Guardian wrote report when unresolved).

---

## Commands and scripts

| What | Command |
|------|---------|
| **Start all agents (one script)** | **`.\Tools\Start-AllAgents.ps1`** — Installs CLI if needed, then runs the Watcher (Developer loop + Fixer on failure + Guardian when loop detected). Editor auto-launches when UE_EDITOR is set. Use this to put the full company to work. |
| **Developer** | `.\Tools\Start-AutomationSession.ps1` or `.\Tools\RunAutomationLoop.ps1` (loop only; no Fixer/Guardian). |
| **Fixer** | Invoked automatically by the Watcher when Developer exits non-zero. |
| **Guardian** | Invoked automatically by the Watcher when the same failure recurs or MaxFixRounds reached; or manually: `.\Tools\Guard-AutomationLoop.ps1`. |
| **Refiner** | On-demand: `.\Tools\Run-RefinerAgent.ps1` or Cursor command **refine-rules-from-runs**. Optionally run after Guardian when automation_loop_breaker_report.md exists. Logs to Saved/Logs/refiner.log. |
| **Gap-Solver** | On-demand: `.\Tools\Run-GapSolverAgent.ps1` or Cursor command **run-gap-solver**. Run when a gap is logged (AUTOMATION_GAPS.md) or after Guardian report that mentions gaps. Logs to Saved/Logs/gap_solver.log. |

---

## Related docs

- [AUTOMATION_LOOP_UNTIL_DONE.md](AUTOMATION_LOOP_UNTIL_DONE.md) — Loop mechanics, file logging, Watcher/Guardian flow.
- [AUTOMATION_REFINEMENT.md](AUTOMATION_REFINEMENT.md) — Using run history and errors to update rules and strategy.
- [README-Automation.md](../README-Automation.md) — Commands table and troubleshooting.

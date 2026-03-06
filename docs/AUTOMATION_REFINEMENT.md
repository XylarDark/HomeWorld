# Automation refinement: from agent actions and errors to rules and strategy

**Goal:** Use every automation run (main loop, fix agent, loop-breaker) and every error to **update project rules and refine development strategy** over time, so the same failures are avoided and the loop gets more reliable.

---

## What gets recorded

1. **Saved/Logs/agent_run_history.ndjson**  
   One NDJSON line per run:
   - **main** — Each round of the automation loop (timestamp, round, exit_code, error_summary when non-zero).
   - **fix** — Each fix-agent run (round, exit_code, trigger_exit_code, optional suggested_rule_update / suggested_strategy from agent_feedback_this_run.json).
   - **loop_breaker** — Each loop-breaker run (exit_code, error_summary, optional suggestions from agent_feedback_this_run.json).

2. **Saved/Logs/automation_errors.log**  
   Errors from the main loop (non-zero exit, usage-limit hints). Pasted into chat for fixes; also a source for refinement.

3. **Saved/Logs/automation_loop_breaker_report.md**  
   Written by the loop-breaker when it cannot resolve a repeating failure. Contains summary, what was tried, and recommended manual steps. Use this as a first-class input for strategy updates.

4. **Agent feedback file (ephemeral)**  
   Fix and loop-breaker agents can write **Saved/Logs/agent_feedback_this_run.json** with:
   - `suggested_rule_update`: one-line suggestion for .cursor/rules or KNOWN_ERRORS.
   - `suggested_strategy`: one-line suggestion for process or docs (e.g. AGENTS.md, workflow docs).  
   The watcher/guardian scripts merge this into the run history and then delete the file.

5. **Editor Output Log (on failure)**  
   When the main loop fails, the Watcher captures the Editor log: **Saved/Logs/editor_output_full.txt** (unfiltered) and **Saved/Logs/editor_output_filtered.txt** (development-relevant only). Fixer and Guardian use these to diagnose Editor-related failures. **Safety rule:** when previous fix round(s) did not resolve the issue, the agent is instructed to read the **unfiltered** log so the filter cannot hide the real error. See [AUTOMATION_EDITOR_LOG.md](AUTOMATION_EDITOR_LOG.md).

---

## How to use the feed for refinement

### Option A: Periodic or on-demand “refine” pass

1. **Read** the last N entries of `Saved/Logs/agent_run_history.ndjson` (and optionally the tail of `automation_errors.log` and `automation_loop_breaker_report.md`).
2. **Identify** repeated exit codes, repeated error_summary patterns, and any non-null `suggested_rule_update` or `suggested_strategy`.
3. **When `automation_errors.log` shows only the generic line** (“paste Saved/Logs/automation_errors.log into chat to fix”): the root cause is in **Saved/Logs/automation_loop.log** (agent output, build failure, script stderr). Use the loop log tail or the Fixer’s SESSION_LOG entry to infer the real error and add KNOWN_ERRORS if it could recur.
4. **Update**:
   - **docs/KNOWN_ERRORS.md** — Add or extend entries for recurring errors and fixes.
   - **.cursor/rules/*.mdc** — Add or adjust rules (e.g. automation, MCP, build, idempotency) when patterns justify it.
   - **AGENTS.md** — Update commands, boundaries, or workflow when strategy should change.
   - **docs/workflow/** or **docs/CONVENTIONS.md** — Document process or convention changes.

### Option B: Dedicated “refine rules / strategy” session or command

- **Inputs:** `agent_run_history.ndjson`, `automation_errors.log`, `automation_loop_breaker_report.md`, and optionally `docs/SESSION_LOG.md`, `docs/KNOWN_ERRORS.md`.
- **Output:** A short list of concrete changes (e.g. “Add to KNOWN_ERRORS: …”, “Add rule: …”, “Update AGENTS.md: …”) or a markdown summary file (e.g. `Saved/Logs/strategy_refinement_candidates.md`) for a human or a follow-up agent to apply.
- You can run this weekly or after a loop-breaker report; or add a Cursor command (e.g. in `.cursor/commands/`) that loads the run history and prompts: “Review these runs and suggest updates to rules and strategy.”

### Option C: Loop-breaker report → immediate refinement

- When **Saved/Logs/automation_loop_breaker_report.md** exists, treat it as a trigger: open it plus the last 20 lines of `agent_run_history.ndjson` and `automation_errors.log`, then apply Option A or B so the next run benefits from updated rules or strategy.

---

## File locations (quick reference)

| File | Purpose |
|------|--------|
| Saved/Logs/agent_run_history.ndjson | All agent runs (main, fix, loop_breaker) for refinement |
| Saved/Logs/automation_errors.log | Error lines from the main loop |
| Saved/Logs/automation_loop_breaker_report.md | Loop-breaker report when it cannot resolve the loop |
| Saved/Logs/agent_feedback_this_run.json | Ephemeral; written by fix/loop-breaker, merged into history then removed |
| Saved/Logs/editor_output_full.txt | Unfiltered Editor log (last N lines); captured on failure. When unfixable, use this. |
| Saved/Logs/editor_output_filtered.txt | Filtered Editor log (development-relevant only). See [AUTOMATION_EDITOR_LOG.md](AUTOMATION_EDITOR_LOG.md). |
| docs/KNOWN_ERRORS.md | Recorded errors and fixes (update from run history) |
| .cursor/rules/*.mdc | Project rules (update when patterns justify) |
| AGENTS.md | Top-level agent context and workflow (update for strategy) |

---

## Eighth list cycle (2026-03-05)

The eighth 10-task list (T1–T8) completed; T9 (this pass) updated **AUTOMATION_GAPS.md** with a cycle summary so the next list generator has the current gap list. Refinement sources (agent_run_history.ndjson, automation_errors.log, SESSION_LOG) are ready for the next refinement pass or Refiner run.

---

## Ninth list cycle (2026-03-05)

The ninth 10-task list (T1–T8) completed; T9 updated **AUTOMATION_GAPS.md** Research log with ninth-cycle outcome (no new gaps; Gap 1 and Gap 2 unchanged). **AUTOMATION_REFINEMENT.md** updated with this cycle note. Next list generator: use AUTOMATION_GAPS per [HOW_TO_GENERATE_TASK_LIST.md](workflow/HOW_TO_GENERATE_TASK_LIST.md).

---

## Eleventh list cycle (2026-03-05)

The eleventh 10-task list (PIE-full validation, deferred features, Act 2 prep, Steam EA, docs, AUTOMATION_GAPS, buffer). T1–T7 completed; T8 (this pass) refinement: **AUTOMATION_REFINEMENT.md** updated with this cycle note; refinement pass used SESSION_LOG and CURRENT_TASK_LIST (Saved/Logs not in workspace). No recurring error patterns from this cycle; Run-RefinerAgent.ps1 may be run when automation host has access to agent_run_history.ndjson and automation_errors.log for full refinement. Next: T9 (AUTOMATION_GAPS update), T10 (buffer), then generate new list per [HOW_TO_GENERATE_TASK_LIST.md](workflow/HOW_TO_GENERATE_TASK_LIST.md).

---

## Refiner pass 2026-03-04 (stall pattern from automation_errors.log)

**Inputs:** Last 60 lines of agent_run_history.ndjson (all exit_code 0, main role; no suggested_rule_update/suggested_strategy), last 40 lines of automation_errors.log (repeated Watch-HeartbeatStall: STALL DETECTED), no Guardian report.

**Findings:** Run history showed no recurring *failure* codes. automation_errors.log showed a **recurring pattern**: Watch-HeartbeatStall repeatedly logging that heartbeat/last_activity was not updated for 15+ minutes (up to 301 min in one run, 71.9 min in another), and killing agent process(es). This is the stall watcher doing its job when the main loop stops writing heartbeats (loop hung/crashed) or when runs legitimately exceed the 15 min threshold.

**Updates applied:** (1) **KNOWN_ERRORS.md** — Added entry "Watch-HeartbeatStall: STALL DETECTED repeatedly in automation_errors.log" with cause, fix (e.g. -StallThresholdMinutes, -NoStallProtection), and context. (2) **AUTOMATION_REFINEMENT.md** — Checklist item for Refiner: when automation_errors.log shows many Watch-HeartbeatStall lines, use KNOWN_ERRORS entry and document mitigation.

**Artifacts:** No Guardian report present; Developer runs in history all exit 0. No automation gap mentioned in excerpts; Gap-Solver not triggered.

---

## Refinement when Saved/Logs is not readable

When `Saved/Logs` is not available (e.g. in chat, or path filtered), use **SESSION_LOG.md** and **CURRENT_TASK_LIST.md** outcomes to infer patterns: repeated "PIE not running", "blocked on T1", "deferred", etc. Add or extend **KNOWN_ERRORS.md** entries and doc notes so the same interpretations are documented. Run the Refiner script (Run-RefinerAgent.ps1) when the automation host has access to agent_run_history.ndjson and automation_errors.log for full refinement.

## Checklist for a refinement pass

- [ ] Read last 50–100 lines of `agent_run_history.ndjson` (or full file if small).
- [ ] Note repeated `exit_code` or similar `error_summary`; add or update entries in **KNOWN_ERRORS.md**.
- [ ] Apply or file any non-null `suggested_rule_update` / `suggested_strategy` from the history.
- [ ] If `automation_loop_breaker_report.md` exists, use it to add KNOWN_ERRORS entries and rule or strategy changes.
- [ ] Update **.cursor/rules** or **AGENTS.md** only when the same pattern appears multiple times or the loop-breaker explicitly recommends it.
- [ ] **Fixer accountability:** When run history shows a fix round with no `suggested_rule_update`/`suggested_strategy`, consider adding a rule or doc note that Fixer should write `agent_feedback_this_run.json` when the fix is generalizable (e.g. added a KNOWN_ERRORS entry), so future Refiner passes have a direct signal from history.
- [ ] **automation_errors.log — Watch-HeartbeatStall:** When the log shows many repeated "Watch-HeartbeatStall: STALL DETECTED" lines (heartbeat/last_activity not updated for X min), treat as the known stall pattern: see **KNOWN_ERRORS.md** "Watch-HeartbeatStall: STALL DETECTED repeatedly". No Guardian report is required for this pattern; document mitigation (-StallThresholdMinutes, -NoStallProtection) in KNOWN_ERRORS and optionally in workflow docs.

---

## Twelfth list cycle (2026-03-05)

T7 refinement completed. **Inputs:** SESSION_LOG.md and CURRENT_TASK_LIST.md (Saved/Logs not in workspace). **Outcome:** No new recurring failure patterns from this cycle; twelfth list T1–T6 completed (PIE re-run, agentic building deferred, packaged build, demo sign-off, Act 2 stub, docs polish). **Updates applied:** (1) This cycle note in AUTOMATION_REFINEMENT.md; (2) KNOWN_ERRORS.md "Next priority" refreshed for post–T7: T8 (AUTOMATION_GAPS), T9 (KNOWN_ERRORS/CONVENTIONS polish), T10 (buffer), then generate new list per [HOW_TO_GENERATE_TASK_LIST.md](workflow/HOW_TO_GENERATE_TASK_LIST.md). Run Run-RefinerAgent.ps1 when automation host has access to agent_run_history.ndjson and automation_errors.log for full refinement.

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
| docs/KNOWN_ERRORS.md | Recorded errors and fixes (update from run history) |
| .cursor/rules/*.mdc | Project rules (update when patterns justify) |
| AGENTS.md | Top-level agent context and workflow (update for strategy) |

---

## Checklist for a refinement pass

- [ ] Read last 50–100 lines of `agent_run_history.ndjson` (or full file if small).
- [ ] Note repeated `exit_code` or similar `error_summary`; add or update entries in **KNOWN_ERRORS.md**.
- [ ] Apply or file any non-null `suggested_rule_update` / `suggested_strategy` from the history.
- [ ] If `automation_loop_breaker_report.md` exists, use it to add KNOWN_ERRORS entries and rule or strategy changes.
- [ ] Update **.cursor/rules** or **AGENTS.md** only when the same pattern appears multiple times or the loop-breaker explicitly recommends it.
- [ ] **Fixer accountability:** When run history shows a fix round with no `suggested_rule_update`/`suggested_strategy`, consider adding a rule or doc note that Fixer should write `agent_feedback_this_run.json` when the fix is generalizable (e.g. added a KNOWN_ERRORS entry), so future Refiner passes have a direct signal from history.

# Automation cost and token tracking

**Goal:** Know API cost per run/round and per role to avoid surprise bills and tune model choice. The automation loop and run history support **model attribution** now; **token/cost** fields are populated when the CLI or an external tracker exposes usage.

## What we record

- **Saved/Logs/agent_run_history.ndjson** — Each run (main, fix, loop_breaker) is one NDJSON line with:
  - `ts`, `role`, `round`, `exit_code`, `error_summary`, `trigger_exit_code`, `suggested_rule_update`, `suggested_strategy`
  - **`model`** — CLI model used (e.g. `auto`, `claude-sonnet`). Set from the `-Model` passed to the loop/Watcher/Guardian so you have per-round model attribution.
  - **`tokens`** — Optional; set when the Cursor Agent CLI or a proxy exposes token count for the run.
  - **`cost`** — Optional; set when you have a dollar (or other) cost for the run (e.g. from Cursor billing or an external tracker).

Until the Cursor Agent CLI exposes usage in its output or API, `tokens` and `cost` will remain unset. You can still use `model` to attribute runs to a model for later cost estimation (e.g. by model from Cursor’s usage/billing page).

## How to see cost today

1. **Cursor usage/billing** — Use Cursor’s usage or billing page for overall spend; correlate by time window with `agent_run_history.ndjson` (by `ts` and `model`).
2. **External token/cost trackers** — If you use a proxy or tool (e.g. Tokentap-style, or a wrapper that logs usage), you can extend the scripts that call `Append-AgentRunRecord.ps1` to pass `-Tokens` and/or `-Cost` when that data is available.
3. **Per-round attribution** — Each record in `agent_run_history.ndjson` has `role`, `round`, and `model`; use them to attribute Cursor billing to main vs fix vs guardian runs.

## Script interface

- **Append-AgentRunRecord.ps1** accepts optional **`-Model`**, **`-Tokens`**, **`-Cost`**. The loop, Watcher, and Guardian pass `-Model` from their own `-Model` parameter. Add `-Tokens` / `-Cost` when you have a source (e.g. CLI output parsing or external tracker).

## Summary

- **Model:** Recorded per run from the automation scripts.
- **Tokens/cost:** Use Cursor billing or external trackers until the CLI exposes usage; then add parsing or API integration and pass `-Tokens` / `-Cost` into `Append-AgentRunRecord.ps1`.

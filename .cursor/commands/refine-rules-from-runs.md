# Refine rules from runs

Fold what past runs and errors taught us back into the rules, so the same failures do not recur.

**What to do:** Read the run history and error log, then update the affected docs and rules.

- `Saved/Logs/agent_run_history.ndjson` — one NDJSON line per run (main, fix, loop_breaker): `ts`, `role`, `round`, `exit_code`, `error_summary`, `trigger_exit_code`, `suggested_rule_update`, `suggested_strategy`.
- `Saved/Logs/automation_errors.log` — raw error text.

From those, update as needed: `docs/KNOWN_ERRORS.md`, `.cursor/rules/`, `AGENTS.md`, `docs/Automation/AUTOMATION_GAPS.md`.

**Rules for this pass:**

- Every change must be traceable to a specific record above. No speculative rules.
- Prefer editing an existing entry over appending a near-duplicate.
- When a run mentions an automation gap (Level Streaming, State Tree, PCG), add it to `docs/Automation/AUTOMATION_GAPS.md` (canonical) — do not invent a new doc.

**Related:** [docs/Automation/AUTOMATION_REFINEMENT.md](../../docs/Automation/AUTOMATION_REFINEMENT.md) (how run history is used) ·
[.cursor/skills/automation-gap-solutions/SKILL.md](../../.cursor/skills/automation-gap-solutions/SKILL.md) ·
[docs/Automation/AGENT_COMPANY.md](../../docs/Automation/AGENT_COMPANY.md) (history — the Refiner *role* this replaced).

> **Quarantine:** the pre-swarm agent company and `Tools/Run-RefinerAgent.ps1` were **removed in WAVE F**.
> Active driver: [swarm/SWARM_OPS.md](../../swarm/SWARM_OPS.md) + Conductor — [START_HERE.md](../../START_HERE.md).
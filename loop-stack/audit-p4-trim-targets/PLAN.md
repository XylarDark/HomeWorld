# Loop Plan
## Mode
audit
## Goal
Independently verify the harness findings that will drive the P4 trim: confirm which of the 31 .cursor/rules files are genuinely oversized or duplicated, re-check the 5 unexplained HomeWorld-vs-pinned-DevEnvTemplate skill drifts, and rank the trim candidates by bytes saved per unit of risk. Read-only: no file changes.
## Stop Condition
all tasks in loop-stack/audit-p4-trim-targets/PLAN.md checked
## Budget
10 turns

**This is a turn counter, not a cost ceiling.** loop-engineer has no dollar or
token budget - `MAX_TURNS` counts agent invocations and nothing else. Set to 10
rather than the default 20 because OpenCode dispatches subagents sequentially
(upstream #14195, re-reported #29638), so each turn is a full agent round-trip
against a 7-agent team. If a loop hits 10 turns with tasks open, the remaining
work is a signal to re-scope, not to raise the ceiling.

Measured cost per loop is not currently obtainable: see
`docs/Automation/AUTOMATION_COST_TRACKING.md`, which records `model` per run but
reports token/cost as unavailable. Closing that is P3 follow-up work.
## Git Integration
no
## Tasks
(will be created by the planner agent)

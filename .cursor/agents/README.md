# Swarm specialists (on demand)

These role cards are for the **MVP lookdev swarm** — Conductor spawns one specialist per task with thin context (role card + wave packet inputs only). They are **not** always-loaded like root [AGENTS.md](../../AGENTS.md) or the UE automation company (Developer / Fixer / Guardian).

| When | How |
|---|---|
| Start swarm | Human Lead follows [START_HERE.md](../../START_HERE.md) |
| Assign work | Conductor copies the matching card into a subagent or isolated chat |
| Process rules | [swarm/SWARM_OPS.md](../../swarm/SWARM_OPS.md) |
| Source of truth | [swarm/agents/](../../swarm/agents/) — keep in sync when editing cards |

**Cards:** `conductor`, `designer`, `art-director`, `world`, `tech-artist`, `env-homestead`, `env-planet`, `props`, `creatures`, `lighting`, `gameplay`, `systems`, `integration`, `qa`, `verifier` (evidence-only pass; separate from QA defect filing).

Do not convert the UE automation loop to use these cards unless a task explicitly requires it.

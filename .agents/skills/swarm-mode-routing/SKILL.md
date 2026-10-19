---
name: swarm-mode-routing
description: >-
  Choose SWARM, NON-SWARM, or HYBRID when the ask is Conductor, a wave,
  APPROVE P0-P7, a Blender kit, or an art or QA shot gate.
---

# Swarm mode routing

Pick **exactly one** mode, then a **model class**, before heavy context load.

- Protocol: [docs/human-use/SWARM_MODE_ROUTING.md](../../../docs/human-use/SWARM_MODE_ROUTING.md)
- Research: [docs/Automation/SWARM_ROUTING_RESEARCH.md](../../../docs/Automation/SWARM_ROUTING_RESEARCH.md)

## First-match summary

0. **SOLO** — Lead typed `SOLO`. Pre-check, not a mode. One chat holds every execution role; taste and test stay human. Fail-closed, never inferred from an idle external runtime.
1. **SWARM** — Conductor / wave packet / `APPROVE Pn` / Blender+Lib lookdev / multi-role kit / AD or QA judge / active P0–P7 kit work.
2. **NON-SWARM** — Engine, C++, Python automation, CI, Config, lowercase docs, Docs/NN engineering without specialist fan-out.
3. **HYBRID** — Engineering enables lookdev; taste/shot gate stays Conductor or AD in another chat.
4. **Ambiguous** — Prefer NON-SWARM for the next atomic step.

## SOLO

`SOLO` = no second runtime; one OpenCode chat holds the execution roles — Conductor, `world-designer`, `env-*`, `props`, `lighting`, `creatures`, `tech-artist`, `gameplay`, `systems`, `integration`, and an independent `qa` subagent.

Still human: art taste, mechanic canon, shot verdicts, test verdicts. `design` / `art-director` draft inside an alert; nothing is scribed without a yes. `qa` files defects, does not close them.

Mode is still named after SOLO. One owner per path.

## Model class (after mode)

| Class | Use |
|-------|-----|
| **Auto** | Routine edits, boilerplate, bulk |
| **Mid** | Default implement / Conductor / most specialists |
| **Frontier** | Architecture, subtle bugs, AD taste — then drop |
| **Explore** | Parallel search subagents (isolated, cheap) |

## Token rule

Do not load `.cursor/agents/*`, the full MVP brief, or Blender MCP waves in NON-SWARM. In SWARM, load **one** role card + packet paths only ([SWARM_OPS](../../../swarm/SWARM_OPS.md) thin context).

## Output

```text
Mode: NON-SWARM|SWARM|HYBRID — <reason>
ModelClass: Auto|Mid|Frontier|Explore — <reason>
```

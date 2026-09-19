---
name: swarm-mode-routing
description: >-
  At task start or ask pivot, choose SWARM vs NON-SWARM vs HYBRID and a ModelClass
  (Auto/Mid/Frontier/Explore) before loading Conductor, role cards, or Blender waves.
  Triggers: Conductor, wave packet, APPROVE P0-P7, FALLBACK FLIGHT, FIX owner id,
  Blender kit, Lib/, Maps/Preview_, Art Director shot, QA judge, Safe-Build, CI,
  PR merge, C++/Python automation, Docs/NN engineering, token efficiency, swarm mode.
---

# Swarm mode routing

Pick **exactly one** mode, then a **model class**, before heavy context load.

- Protocol: [docs/human-use/SWARM_MODE_ROUTING.md](../../../docs/human-use/SWARM_MODE_ROUTING.md)
- Research: [docs/Automation/SWARM_ROUTING_RESEARCH.md](../../../docs/Automation/SWARM_ROUTING_RESEARCH.md)

## First-match summary

1. **SWARM** — Conductor / wave packet / `APPROVE Pn` / Blender+Lib lookdev / multi-role kit / AD or QA judge / active P0–P7 kit work.
2. **NON-SWARM** — Engine, C++, Python automation, CI, Config, lowercase docs, Docs/NN engineering without specialist fan-out.
3. **HYBRID** — Engineering enables lookdev; taste/shot gate stays Conductor or AD in another chat.
4. **Ambiguous** — Prefer NON-SWARM for the next atomic step.

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

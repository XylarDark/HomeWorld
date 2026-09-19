---
name: swarm-mode-routing
description: Use at task start or when the ask pivots — choose SWARM, NON-SWARM, or HYBRID before loading Conductor, specialist role cards, or Blender lookdev waves. Also when the user asks about swarm vs coding chat, token efficiency, or mode detection.
---

# Swarm mode routing

Pick **exactly one** mode before heavy context load. Full protocol:
[docs/human-use/SWARM_MODE_ROUTING.md](../../../docs/human-use/SWARM_MODE_ROUTING.md).

## First-match summary

1. **SWARM** — Conductor / wave packet / `APPROVE Pn` / Blender+Lib lookdev / multi-role kit / AD or QA judge shots / active P0–P7 kit work.
2. **NON-SWARM** — Engine, C++, Python automation, CI, Config, lowercase docs, Docs/NN engineering tracks without specialist fan-out.
3. **HYBRID** — Engineering enables lookdev; taste/shot gate stays Conductor or AD in another chat.
4. **Ambiguous** — Prefer NON-SWARM for the next atomic step; one Steer ask only if needed.

## Token rule

Do not load `.cursor/agents/*`, the full MVP brief, or Blender MCP waves in NON-SWARM. In SWARM, load **one** role card + packet paths only ([SWARM_OPS](../../../swarm/SWARM_OPS.md) thin context).

## Output

State one line: `Mode: NON-SWARM|SWARM|HYBRID — <reason>`.

---
last_mapped_commit: 94158e9416cc44954f4fdb11e0de696e31836276
last_mapped_at: 2026-09-28
---
﻿# Conventions

**Analysis Date:** 2026-09-28

## Code Style

**Programmatic by default** (`docs/CONVENTIONS.md`, `AGENTS.md`):
- New gameplay / movement / input / abilities / core logic → **C++**
- Blueprint → content, level design, asset assignment on C++ defaults only
- Abilities: implement in C++ subclass; reparent `GA_*` Blueprint — no Event Graph logic

**Architecture depth:**
- One deployable client; C++ single writer of behavior
- Prefer deep modules over pass-through wrappers (`docs/architecture/HOMEWORLD_DESIGN.md`)

## Naming

- Prefix all project UObject types with `HomeWorld`
- Files: `HomeWorldThing.h` / `.cpp` matching type
- Subsystems: `UHomeWorld*Subsystem`
- Components: `UHomeWorld*Component`

## Patterns

- **MCP-first** when Editor running (`.cursor/rules/09-mcp-workflow.mdc`)
- Repeatable Editor ops also saved as `Content/Python/` scripts
- Debug instrumentation on new features; validate from logs (rule `16-feature-debug-instrumentation`)
- Full automation — no manual step docs for users (rule `20-full-automation-no-manual-steps`); log impossibilities to `AUTOMATION_GAPS.md`

## Error Handling

- Record real failures in `docs/KNOWN_ERRORS.md`
- Preflight fails loud: `npm run preflight:ue` (`scripts/preflight-ue.js`)
- Evidence greps: `npm run evidence:grep`
- HS-D: re-verify hard-fail verb greps before polish

## Swarm / Git Safety

- Two-tier Conductor model (`swarm/SWARM_OPS.md`) — no flat peer design debates after Phase 0
- Exclusive file/collection ownership per worker
- DESKTOP Shell / MCP / PIE: Conductor **parent** only — never Task executors / cloud VMs
- Ball law: only ball-holder posts Act narrative

## Feature Development Policy

- Research Epic/UE docs + tutorials first (rule `07-ai-agent-behavior`)
- Plan-first for complex multi-file work (`docs/SPEC_AND_PLAN.md`, rule `17-plan-first`) — plans stay in chat unless Lead asks to save

---
*Conventions analysis: 2026-09-28*

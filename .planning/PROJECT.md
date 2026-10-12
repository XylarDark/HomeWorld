# HomeWorld

## What This Is

HomeWorld is an Unreal Engine **5.8** game. Product vision is `Docs/VISION_BOARD.md`. `Docs/` and `docs/` are one directory. The repo is a **brownfield** UE project plus Conductor/swarm ops and DevHarness tooling.

GSD on this host provides **planning scaffolding only**. Live product phase authority remains `swarm/PHASE_BOARD.md` and Lead-named bites. Cursor is the GSD host as of 2026-10-12. The OpenCode install stays in `.opencode` until that host is no longer needed.

## Core Value

Ship a playable, evidence-gated vertical slice on UE 5.8 without inventing product scope past Lead / PHASE_BOARD.

## Requirements

### Validated

- MVP vertical slice + post-audit product tracks through Docs/30 Demo Spine — **CLOSED** (see `swarm/PHASE_BOARD.md`)
- Harness refine HR / HR2 / HR3 / VP / HS Audit — **CLOSED** or Lead-approved as recorded on PHASE_BOARD
- CAP + EA product tracks — Lead **DROPPED** 2026-09-27 ET

### Active

- [ ] Keep GSD host planning healthy (`.planning/` map + STATE) without opening invent Co MUST Acts
- [ ] Execute only Lead-named harness/bot bites when Conductor assigns them
- [ ] Preserve DESKTOP Shell/MCP/PIE parent-only law and HS-D re-verify discipline

### Out of Scope

- Inventing Co product phases / MUST Acts in GSD ROADMAP — Co owns that via PHASE_BOARD / Lead
- Feature Source PRs, `.uasset` churn, or GSD Browser from this onboard
- Baking co-ops or touching Co Research EXIT as part of host onboard
- Engine or platform variants beyond UE 5.8 / PC+Steam without Lead decision

## Context

- Entry: `START_HERE.md`, `AGENTS.md`
- Product vision: `Docs/VISION_BOARD.md`
- `Docs/` and `docs/` are one directory
- Live ball: `swarm/PHASE_BOARD.md` — no product phase until a bite is named
- Code: `Source/HomeWorld/` C++ for gameplay; Blueprint for content

## Constraints

- **Engine**: UE 5.8 only
- **Platform**: PC + Steam Early Access
- **Host**: DESKTOP-21CT3H0 Conductor parent for Shell/MCP/PIE
- **GSD**: Cursor host (`~/.cursor`, core 1.16.0). `.opencode/` stays untracked. `planning.commit_docs: false`
- **Co-outer**: Product Acts only from PHASE_BOARD / Lead-named bites

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Brownfield GSD onboard (map → docs → project) | Host needs STATE/CONTEXT without replacing Co | Pending Lead review of planning tree |
| ROADMAP = host scaffolding only | Avoid inventing Co MUSTs | Locked for this onboard |
| commit_docs false | Do not auto-commit `.opencode/` or planning | Locked |
| CAP/EA DROPPED | Lead 2026-09-27 | Locked on PHASE_BOARD |

---
*Last updated: 2026-10-12 — Cursor is the GSD host. GSD-3 stays idle.*
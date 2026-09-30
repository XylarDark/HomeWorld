# Context: HomeWorld GSD host

**Gathered:** 2026-09-28
**Status:** Onboard complete — host scaffolding only

## Phase Boundary

GSD onboard establishes planning artifacts. It does **not** authorize feature Source work, `.uasset` edits, GSD Browser, or invent Co Research EXIT changes.

## Implementation Decisions

### Co-outer constraint
- **D-01:** Product Acts come only from `swarm/PHASE_BOARD.md` or Lead-named bites
- **D-02:** GSD ROADMAP phases GSD-0..GSD-3 are host scaffolding; GSD-3 product plan list stays empty until Lead names work
- **D-03:** CAP/EA remain DROPPED per Lead 2026-09-27 — do not revive in ROADMAP

### Onboard path
- **D-04:** Auto-choose map-first, then ingest useful docs by citation, then new-project-style artifacts
- **D-05:** When opencode hangs / auth weak, write `.planning/` from GSD templates + SCOUT (authorized fallback)
- **D-06:** `commit_docs: false`; never commit `.opencode/` unless already tracked (it is not)

### Docs ingest (light)
- **D-07:** `docs/SPEC_AND_PLAN.md` — plan-first process; keep plans in chat unless Lead asks to save
- **D-08:** Product ADR-like history stays in `Docs/` + PHASE_BOARD — do not invent new ADRs during onboard

## Canonical References

### Swarm / Conductor
- `swarm/PHASE_BOARD.md` — live product authority
- `swarm/SWARM_OPS.md` — process
- `START_HERE.md`, `AGENTS.md`

### Engineering
- `docs/CONVENTIONS.md`, `docs/SETUP.md`, `docs/SPEC_AND_PLAN.md`
- `docs/KNOWN_ERRORS.md`, `docs/Setup/MCP_SETUP.md`, `docs/Setup/WINDOWS_BRIDGE.md`

### Product canon
- `Docs/README.md` and signed Docs/05–30 tracks (CLOSED as on PHASE_BOARD)

### Code
- `HomeWorld.uproject`, `Source/HomeWorld/`, `Maps/`, `package.json`

## Existing Code Insights

### Reusable Assets
- C++ GAS + character/game mode stack under `Source/HomeWorld/`
- Python Editor automation under `Content/Python/`
- Harness: `npm run doctor`, `preflight:ue`, `evidence:grep`

### Constraints to honor
- DESKTOP Conductor parent only for Shell/MCP/PIE
- Programmatic-by-default C++
- No invent product Acts from this context alone

---
*Context written: 2026-09-28*
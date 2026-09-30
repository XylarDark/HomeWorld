# Requirements: HomeWorld (GSD host)

**Defined:** 2026-09-28
**Core Value:** Playable UE 5.8 slice; product scope only from Co PHASE_BOARD / Lead

## v1 Requirements

Host / harness scaffolding only. **No invented Co product MUSTs.**

### Host Planning

- [x] **HOST-01**: `.planning/codebase/` full 7-doc map present and stamped
- [x] **HOST-02**: `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md`, `CONTEXT.md` present
- [x] **HOST-03**: `.planning/onboarding/SUMMARY.md` present
- [ ] **HOST-04**: Conductor confirms onboard health and holds ball

### Process Guards

- [x] **GUARD-01**: ROADMAP states product Acts come only from PHASE_BOARD / Lead-named bites
- [x] **GUARD-02**: Onboard produced no Source feature PR and no `.uasset` changes
- [x] **GUARD-03**: `.opencode/` left untracked; `commit_docs` false

### Existing Product (reference — not GSD-owned)

Validated product/history lives on `swarm/PHASE_BOARD.md` and `Docs/`. Do not re-list as open GSD phase requirements.

## v2 Requirements

Deferred — only if Lead names a new product track on PHASE_BOARD.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Invent Co MUST Acts | Co-outer constraint |
| CAP / EA revival | Lead DROPPED 2026-09-27 |
| GSD Browser / Research EXIT rewrite | Conductor onboard stop rule |
| Engine ≠ 5.8 or non-PC platforms | Product lock |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| HOST-01 | GSD-0 Map | Done |
| HOST-02 | GSD-1 Project init | Done |
| HOST-03 | GSD-2 Onboard summary | Done |
| HOST-04 | Conductor | Pending |
| GUARD-01..03 | GSD-1 | Done |

**Coverage:**
- v1 requirements: 7 total
- Mapped to GSD host phases: 7
- Unmapped: 0

---
*Requirements defined: 2026-09-28*
*Last updated: 2026-09-28 after GSD onboard*
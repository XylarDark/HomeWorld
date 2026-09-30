# Roadmap: HomeWorld (GSD host scaffolding)

## Overview

This ROADMAP covers **GSD host scaffolding only** for brownfield HomeWorld. It does **not** open product work past `swarm/PHASE_BOARD.md`.

**Hard rule:** Product Acts / MUST bites come **only** from Co `PHASE_BOARD` rows or **Lead-named** harness bites. Do not invent Co phases, CAP/EA revival, or Design/Implement product Acts here. When PHASE_BOARD is idle (current: harness/bot optimization — idle, CAP+EA DROPPED), GSD stays idle on product.

## Phases

GSD host phases (scaffolding — not Co product):

- [x] **Phase GSD-0: Codebase map** - Full `.planning/codebase/` 7 docs + stamp
- [x] **Phase GSD-1: Planning init** - PROJECT / REQUIREMENTS / ROADMAP / STATE / CONTEXT + config
- [x] **Phase GSD-2: Onboard summary** - `.planning/onboarding/SUMMARY.md`
- [ ] **Phase GSD-3: Idle await Lead** - No product execution until PHASE_BOARD / Lead names a bite

## Phase Details

### Phase GSD-0: Codebase map
**Goal**: Evidence-backed map of UE 5.8 + harness layout
**Depends on**: Nothing
**Requirements**: HOST-01
**Success Criteria**:
  1. Seven map files exist under `.planning/codebase/`
  2. `stamp-codebase-map` reports stamped with no failures
**Plans**: complete (manual sequential map after opencode hang)

### Phase GSD-1: Planning init
**Goal**: Brownfield project docs with Co-outer constraint
**Depends on**: GSD-0
**Requirements**: HOST-02, GUARD-01..03
**Success Criteria**:
  1. Core `.planning/*.md` files present
  2. ROADMAP explicitly defers product Acts to PHASE_BOARD / Lead
**Plans**: complete

### Phase GSD-2: Onboard summary
**Goal**: Onboarding index for Conductor
**Depends on**: GSD-1
**Requirements**: HOST-03
**Success Criteria**:
  1. `.planning/onboarding/SUMMARY.md` exists
  2. `init onboard` reaches write-summary/ready/healthy path
**Plans**: complete this session

### Phase GSD-3: Idle await Lead
**Goal**: Hold ball at Conductor; do not invent product work
**Depends on**: GSD-2
**Requirements**: HOST-04
**Success Criteria**:
  1. No Source feature PR from onboard
  2. No GSD execute-phase / feature Act until Lead/PHASE_BOARD names work
  3. Next product plan inserted only by copying a Lead-named bite — never invented here
**Plans**: 0 product plans — intentionally empty

Plans:
- [ ] GSD-3-01: (placeholder only) When Lead names a bite, Conductor may append a decimal GSD phase that **mirrors** that bite — never invents one

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| GSD-0 Map | 1/1 | Complete | 2026-09-28 |
| GSD-1 Init | 1/1 | Complete | 2026-09-28 |
| GSD-2 Summary | 1/1 | Complete | 2026-09-28 |
| GSD-3 Idle | 0/0 | Waiting Lead / PHASE_BOARD | - |

**Co product progress:** See `swarm/PHASE_BOARD.md` — not duplicated here.

---
*Roadmap created: 2026-09-28 — Co-outer constrained*
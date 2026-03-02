# MVP and Roadmap Strategy

How HomeWorld balances **MVP execution** (validate the loop fast) with **long-term readiness** (ship properly). Use this when deciding what to build next or how to structure work.

---

## Is what we're doing best practice?

**Yes, for the choices we've made:**

- **PCG volume sized to level (landscape → WP bounds → config):** Best practice for World Partition. Config is source of truth; we don't depend on landscape being loaded; WP bounds give "size to level" without Load All. Same approach works for MVP and release.
- **Programmatic by default (C++ gameplay, Blueprint content):** Aligns with CONVENTIONS and scales to full game.
- **Single codebase, UE 5.7, PC + Steam EA:** Locked in AGENTS.md and STACK_PLAN; no throwaway prototype engine or platform.
- **World Partition + PCG from Day 1:** Chosen for large proc-gen realms and streaming; we're building on the stack we'll ship with.

So: **orient execution toward MVP, but keep architecture and stack aligned with release.** We're not building a throwaway prototype.

---

## What to implement for MVP

**MVP = smallest playable version that validates the core promise.** For HomeWorld that is:

1. **Core loop:** Explore → fight → build (crash → scout → boss → claim home).
2. **Gate:** Week 1 playtest (Day 5 sign-off). Do **not** start Homestead/Family until this loop is playable and tested.
3. **Concrete MVP scope (Days 1–5):**
   - **Day 1:** PCG forest on map (done: volume sized to level, Generate, manual graph steps per PCG_SETUP).
   - **Day 2:** GAS 3 survivor skills; character/placement polish (movement, camera, ground).
   - **Day 3:** GetPlacementHit / placement for build orders or props; run Week 1 playtest.
   - **Day 4:** Polish explore → fight → build; optional Milady/art.
   - **Day 5:** Playtest sign-off (crash → scout → boss → claim home).

**After MVP:** 30-day schedule continues with Homestead (layout, resources, collection, home), then Family (roles, Mass/State Tree), Planetoid, Spirits, Dungeon. Days 26–30: pick one moment + one beautiful corner for vertical slice.

See [VISION.md](VISION.md) (Demonstrable prototype and vertical slice) and [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md).

---

## MVP-first vs long-term: how we're set up

**We do both, in order:**

| Goal | How we achieve it |
|------|-------------------|
| **MVP fast** | Strict gate: Days 1–5 only until playtest passes. No Homestead/Family/Planetoid work before explore → fight → build works. One playable loop, minimal scope. |
| **Long-term ready** | Same engine, same stack (UE 5.7, WP, PCG, GAS, Mass, etc.). No "prototype branch" that gets discarded. Architecture (C++ game module, config-driven scripts, PCG best practices) is ship-ready. |
| **Vertical slice (end of 30 days)** | One moment + one beautiful corner polished for demo/stakeholders; builds on the same codebase. |

**Strategy in one line:** Execute toward MVP (finish the loop, playtest, sign off), but build on the stack and architecture we intend to ship with, so we don't redo work when moving from prototype to release.

---

## Practical takeaways

- **Roadmap:** Follow [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md). Current day = first day with unchecked items (see [DAILY_STATE.md](DAILY_STATE.md)).
- **Scope:** Don't add features before the Day 5 gate. After gate, add Homestead/Family/Planetoid in schedule order.
- **Tech decisions:** When in doubt, choose the option that works for **both** MVP and release (e.g. WP bounds for volume, GAS for skills, Mass for family agents). Avoid "MVP-only" hacks that would block or complicate release.
- **Documentation:** Keep PCG_SETUP, STACK_PLAN, KNOWN_ERRORS, and workflow docs (VISION, 30_DAY_SCHEDULE, DAILY_STATE) updated so the next session or contributor can continue toward MVP and then toward release without re-deciding strategy.

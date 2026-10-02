# T0 execution phases — work the agent can do without the Lead

Written 2026-10-02. The image work is paused at the Lead's request. This is the queue that
closes the gap between "the design is written down" and "a reviewer can play it".

**How to read the blocked column.** `NO` means I can do it now with no input from anyone.
`BLENDER` means it needs the Blender MCP server up. `LEAD` means it needs the human. `UE` means
it needs the Unreal Editor running.

---

## Phase 1 — Close the tracking gaps

The design decisions exist as prose in spec files. Nothing tracks them, so they will be
forgotten. This phase turns prose into tracked musts.

| # | Task | Blocked | Done-when |
|---|---|---|---|
| 1.1 | Add `NODE_CAPTIVE`, `SPIRIT_STEALTH`, `SLEEPER_STATE_ASLEEP` to `T0_MECHANIC_INVENTORIES_V1.md` as numbered musts with DONE-WHEN rows | **NO** | They appear in the must list with the same shape as #1–#14 |
| 1.2 | Write the **touch rule**: what may a spirit interact with? One page, cited by the garden and the rescue | **NO** | A named rule with a table, and both `FIELD.json` and `CAMP.json` point at it |
| 1.3 | Spec-coverage audit: list every mesh volume in the `.blend` that **no spec names** | **BLENDER** | A report. The shrines were in no spec and a broken shrine survived every gate |
| 1.4 | Reconcile the three disagreeing island-top dimensions (spec 21×14×0.5, `GRAYBOX_LAYOUT.md` 21×14×4.0, blend 19.3×10.7×0.45) | **LEAD** | One number, or a recorded "blend is truth" |
| 1.5 | Water master: propose the 11th master or confirm `M_SpiritUnlit` | **LEAD** | A decision. Not inventing one unilaterally |

## Phase 2 — Close the code gaps

Three mechanics exist as prose and no code. Two of them block M14 outright.

| # | Task | Blocked | Done-when |
|---|---|---|---|
| 2.1 | **The touch rule as code** — a component that gates which actors/objects a spirit form may interact with, logging refusals | **NO** | `hw.FormGate.Test` covers soil=yes, rope=yes/decided, guard=no |
| 2.2 | **`SLEEPER_STATE_ASLEEP`** — a state distinct from `EConvertedFoeRole`. Must NOT be satisfied by conversion | **NO** | A state enum exists and a test asserts converted ≠ asleep |
| 2.3 | **`SPIRIT_STEALTH`** — moving unseen in spirit form. Blocks M14 entirely | **NO** | Detection + a stealth state, with a test that a woken guard breaks it |
| 2.4 | **`NODE_CAPTIVE`** actor + the freedom gate: free them only if both sleepers are asleep | **NO** | Test asserts: awake sleeper → refuse, and killing one is also a fail |

## Phase 3 — Close the evidence gaps

Six beats are `NO_VERDICT`. The gate is *prove runs*, and the gate doc has said so since GATE 1.

| # | Task | Blocked | Done-when |
|---|---|---|---|
| 3.1 | Extend `HomeWorldFormGateTests` for the touch rule and the rescue gate | **NO** | Tests written, **mutation-verified** |
| 3.2 | Same for the sleep-vs-convert distinction — mutate it and confirm the test catches it | **NO** | A killed mutant, not a green tick |
| 3.3 | Run the 6 outstanding prove scripts and hand the Lead evidence, not verdicts | **UE** | `NO_VERDICT` count falls or the failures are documented as real |
| 3.4 | Stamp or void `APPROVE-T0-MECHANIC-INV` — 13 PRs are merged against an unstamped gate | **LEAD** | Checked, or declared void in writing |

## Phase 4 — Geometry (needs Blender)

Nothing here can be built until the images return, except the field, which has no unresolved
taste questions.

| # | Task | Blocked | Done-when |
|---|---|---|---|
| 4.1 | **FIELD** geometry: 70×70, four edges, 2 beast pads, 15 scattered items | **BLENDER** + taste on water/cliff | `graybox_spec_reader` reports FIELD built, 0 blocking on it |
| 4.2 | **`SM_Camp_*`** five modules to `CAMP.json` | **BLENDER** + the camp image | Reader reports CAMP built; the three prove scripts gain geometry to run against |
| 4.3 | Treeline opacity verification: sightline from the landing point and from (+20,−15) | **BLENDER** | Zero forest interior visible from either, or `DEC-0028` is revisited |

## Phase 5 — The playable slice

| # | Task | Blocked | Done-when |
|---|---|---|---|
| 5.1 | Companion NPC: one-line contextual hint (Q19), travels with the player | **NO** | Talk to them, get a state-appropriate line, no dialogue tree |
| 5.2 | Wire the full chain: field → choose forest → day discovery → eject → spirit → stealth → soothe → free | 4.x | A reviewer can play start to rescue without being told what to do |
| 5.3 | Tending: dung by day, soil at night (V2b) | **NO** | Garden bed state changes on a spirit-form night |

---

## Critical path

```
1.1 labels  →  2.2 asleep state  →  2.4 freedom gate  →  4.2 camp geometry  →  5.2 the chain
                  2.1 touch rule  ↗          2.3 stealth ─┘
```

**1.2 (the touch rule) sits under almost everything.** Both the garden and the rescue are
night-time tending, and neither can be built until we know what a spirit may touch.

## What is blocked on the Lead, in one list

1. Field image — then 4.1, 4.3
2. Camp clearing image — then 4.2, and M8/M13/M14
3. Six prove verdicts — then GATE 3
4. `APPROVE-T0-MECHANIC-INV` stamp
5. Water master (1.5), island-top truth (1.4), shrine proportions (Q21)
6. `SPIRIT_STEALTH` *shape* — is it a detection cone, a light level, or a per-actor awareness?

Of these, **only 6 is a question I could not have answered myself, and it is the one that
determines the most code.** The rest are either mechanical follow-through or images.

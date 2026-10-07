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

| # | Task | Blocked | Done-when | State |
|---|---|---|---|---|
| 1.1 | Add `NODE_CAPTIVE`, `SPIRIT_STEALTH`, `SLEEPER_STATE_ASLEEP` to `T0_MECHANIC_INVENTORIES_V1.md` as numbered musts with DONE-WHEN rows | **NO** | They appear in the must list with the same shape as #1–#14 | ✅ #15/#16/#17 added |
| 1.2 | Write the **touch rule**: what may a spirit interact with? One page, cited by the garden and the rescue | **NO** | A named rule with a table, and both `FIELD.json` and `CAMP.json` point at it | ✅ in must list #15 + `CAMP.json` `spirit_touch` |
| 1.3 | Spec-coverage audit: list every mesh volume in the `.blend` that **no spec names** | **BLENDER** | A report. The shrines were in no spec and a broken shrine survived every gate | ⏸ paused with image work |
| 1.4 | Reconcile the three disagreeing island-top dimensions (spec 21×14×0.5, `GRAYBOX_LAYOUT.md` 21×14×4.0, blend 19.3×10.7×0.45) | **LEAD** | One number, or a recorded "blend is truth" | ✅ Resolved 2026-10-07 — Lead: ~660×450 m bounding (half-circle/half-oval), 450×450 m center square, ~300 m tapering rock underside (×6 world-scale pass); recorded in `WORLD_METRICS.md` I1–I5. Blend + `GRAYBOX_LAYOUT.md` + `SM_IslandTop.json` still need updating to match. |
| 1.5 | Water master: propose the 11th master or confirm `M_SpiritUnlit` | **LEAD** | A decision. Not inventing one unilaterally | ✅ Resolved 2026-10-07 — Lead: engine default water, no custom master, no 11th master. |
| **1.6** | **Doc consolidation** — one topic-keyed index so canon loads without hunting; and an audit of the must list's real found-state | **NO** | `Docs/CANON_MAP.md` exists, is **validated**, and no must reads `N` while a stamped track claims it | ✅ `CANON_MAP.md` + 6 tests + 8 mutations killed |

## Phase 2 — Close the code gaps

Three mechanics exist as prose and no code. Two of them block M14 outright.

| # | Task | Blocked | Done-when | State |
|---|---|---|---|---|
| 2.1 | **The touch rule as code** — a component that gates which actors/objects a spirit form may interact with, logging refusals | **NO** | Tests cover soil=yes, rope=yes, guard=no, **every verdict logged** | ✅ `GetSpiritTouchVerdict` + `EvaluateSpiritTouch`; `M15` ×2 green |
| 2.2 | **`SLEEPER_STATE_ASLEEP`** — a state distinct from `EConvertedFoeRole`. Must NOT be satisfied by conversion | **NO** | A state exists and a test asserts converted ≠ calm | ✅ `FHomeWorldCampActorCalm`; `bConverted` blocks the gate |
| 2.3 | **`SPIRIT_STEALTH`** — moving unseen in spirit form | — | — | ⚠️ **Already built and closed** (`APPROVE SS-A`, 2026-09-21). Was a false negative in the must list — see `CANON_MAP.md` §3 |
| 2.4 | **`NODE_CAPTIVE`** actor + the freedom gate: free only when **all three** are eased AND asleep | **NO** | Test asserts: awake sleeper → refuse, killed → refuse, converted → refuse, **2/3 → refuse** | ✅ logic + 2 tests. **Actor not in any `.umap`** |
| **2.5** | **Contain the fail-open** — the gate must not certify itself with zero actors in the world | **NO** | Gameplay half tolerates soft latches, evidence half refuses, and the difference is in the log | ✅ `bSoftLatch` + `SatisfiesFreedomGateStrict` + `SOFT_LATCH_ONLY` |

## Phase 3 — Close the evidence gaps

Six beats are `NO_VERDICT`. The gate is *prove runs*, and the gate doc has said so since GATE 1.

| # | Task | Blocked | Done-when | State |
|---|---|---|---|---|
| 3.1 | Tests for the touch rule and the rescue gate | **NO** | Tests written, **mutation-verified** | ✅ 9 camp tests; mutations M1–M6 |
| 3.2 | Same for the sleep-vs-convert distinction — mutate it and confirm the test catches it | **NO** | A killed mutant, not a green tick | ✅ M4 kills converted-as-calm |
| 3.3 | Run the 6 outstanding prove scripts and hand the Lead evidence, not verdicts | **UE** | `NO_VERDICT` count falls or the failures are documented as real | ⏸ needs camp geometry (4.2) |
| 3.4 | Stamp or void `APPROVE-T0-MECHANIC-INV` — 13 PRs are merged against an unstamped gate | **LEAD** | Checked, or declared void in writing | ⏸ open |

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

**Item 6 is resolved and is now history.** `SPIRIT_STEALTH`'s shape was the one question on this
list I could not have answered alone. The Lead answered it (campfire's blue centre + the guard's
blue torch, **both**, as light-to-visibility) — and that answer turned out to be **the already-LOCKED
bible verbatim** (`SPIRIT_STEALTH_BIBLE.md`, closed under `APPROVE SS-A`). The mechanic was
implemented on 2026-09-21. The only thing that was missing was a pointer from the T0 track to the
document that answered it, which is why it sat on this list for two weeks looking open.

That is item 6 removed, not item 6 answered.

## Still open that is neither image nor mechanical

- **`Docs` vs `docs`.** On a case-insensitive filesystem they are one directory of 441 files, so
  the canon split described in `AGENTS.md` and `Docs/README.md` does not exist on disk. One tree
  or a real split — the Lead's call. `CANON_MAP.md` §7.
- **158 legacy handoffs and 55 legacy task lists.** Read-only in place, or quarantined.
- **`Docs/00_CANON.md`** — LOCKED P0, but pre-T0 topology.

---

## The prove scripts, and why they were sitting uncommitted

Ten DONE-WHEN harnesses existed on disk and **no document referenced any of them** - the exact
shape of the #17 failure, one layer down: a mechanic that reads as unproven because nothing
points at the thing that would prove it. Now referenced, and committed:

| Beat | Prove script | Run state |
| --- | --- | --- |
| #3 Plant given herb | `Content/Python/t0_m3_plant_prove.py` | `NO_VERDICT` |
| #4 Backpack equip | `Content/Python/t0_m4_backpack_prove.py` | `NO_VERDICT` |
| #6 Field gather | `Content/Python/t0_m6_field_gather_prove.py` | `NO_VERDICT` |
| #7 Rune unlock | `Content/Python/t0_m7_rune_unlock_prove.py` | `NO_VERDICT` |
| #8 Day camp eject | `Content/Python/t0_m8_day_camp_eject_prove.py` | **BLOCKED** - no `NODE_DAY_CAMP` in any `.umap` |
| #10 Planetside boot | `Content/Python/t0_m10_planetside_boot_prove.py` | **BLOCKED** - same camp gap |
| #11 Bed to spirit | `Content/Python/t0_m11_bed_spirit_prove.py` | **BLOCKED** - no `NODE_BED` in any `.umap` |
| #12 Nurture slot | `Content/Python/t0_m12_nurture_slot_prove.py` | **BLOCKED** - no `NODE_PLANT_SLOT` placed |
| #13 Portal camp | `Content/Python/t0_m13_portal_camp_prove.py` | **BLOCKED** - no `NODE_PORTAL_CAMP` pair |
| #14 Camp night | `Content/Python/t0_m14_camp_night_prove.py` | **BLOCKED** - `camp_named_objects: []`; soft-latches only |

**All ten are `unproven`.** A script existing is not a verdict; it is the *ability* to produce
one. The blocking reason is the same single gap in every blocked row: the camp/level geometry
does not exist yet, which is waiting on the camp image (image work paused by the Lead).

Seven one-off debug scratch files written during those probes (`t0_m3_end_play.py`,
`t0_m3_method_probe.py`, `t0_m3_try_list.py`, `t0_m4_end_play.py`, `t0_m12_arrange_map.py`,
`t0_m12_map_probe.py`, `t0_m13_map_probe.py`) were deleted rather than committed. They were
throwaway instruments, not deliverables, and an unreferenced scratch file in the tree is the
failure mode this whole pass exists to remove.

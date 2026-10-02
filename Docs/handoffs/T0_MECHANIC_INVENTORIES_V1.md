# T0_MECHANIC_INVENTORIES_V1 — N + Partial MUST mechanic inventories

| Field | Value |
|-------|-------|
| **Status** | **DRAFT — awaiting Lead `APPROVE-T0-MECHANIC-INV`** |
| **Host** | CLOUD (this doc) · Lead (APPROVE) · **no DESKTOP Act / no feature PRs from Design** |
| **Sources** | `Docs/handoffs/PROTOTYPE_FEATURE_LIST_V1.md` (APPROVED) · `Docs/handoffs/T0_GAP_INVENTORY_WALK_V1.md` @ main `f74526d` (Lead ACCEPTED + #228 MERGED) |
| **Scope** | Mechanic inventories + DONE-WHEN for every MUST that is **N** or **Partial** — **not** full **Y** (#5 Glider→field) |
| **Pins** | CAP/EA **DROPPED** · DET pin HOLD `0a27306` · `Maps/VS_MVP` · OpenCode ≡ Cursor (temp) |
| **Cite** | [HomeWorld Co ops](sand-workflow:homeworld-co-ops) · CAPTURE_REDUNDANCY · ONE_SHOT_BITES · [Architecture Trade-Offs A–E](sand-workflow:architecture-trade-offs-design-depth) (blob `107a511`) |

---

## Lead gate

```text
APPROVE-T0-MECHANIC-INV
```

Unlocks Conductor to open Implement bites **one unknown at a time** from § Recommended bite order. Design does **not** stamp APPROVE. Feature Acts only after Conductor opens a named bite citing this packet.

---

## DONE-WHEN (this artifact)

Lead can stamp `APPROVE-T0-MECHANIC-INV` from **§ Priority + § Inventories + § Bite order** alone — no feature Act required to approve the inventories.

---

## Non-goals (locked)

- No Content / Python / Source / `.uasset` / `.umap` in this Design packet
- No feature Acts / no Implement wake from Design
- No invent World Partition / streaming APIs (stream/partition stays A–E cite only)
- No reopen CUT (death · quarantine maps · CAP/EA)
- No DEFER “other plants” loop extension
- No redesign of full **Y** #5 (glide→field) — already Present
- No treat convert stub / soft-kidnap / meal BPs as tea / eject / soothe substitutes

---

## Priority (Conductor hint → Design lock)

| Rank | # | Beat | Gap | Why first |
|------|---|------|-----|-----------|
| **P0** | 9 | Homeworld night w/o bed: no spirit; day abilities off | **Partial** | Critical: `ApplyFormForPhase` auto-spirit violates T0 `TOD_NIGHT_HOME`; gates #11 law |
| **P1** | 2 | Kettle + herbs → tea → sprint | **N** | Zero path |
| **P1** | 7 | Rune unlock before bed→spirit | **N** | Zero path; unlocks #11 |
| **P1** | 8 | Day camp cartoon eject | **N** | Zero path; defines `EJECT_HOME` |
| **P1** | 10 | Planetside night boot home | **N** | Reuses `EJECT_HOME` after #8 |
| **P1** | 14 | Camp night: avoid 1 guard; soothe 2 sleepers | **N** | Zero soothe/guard/sleeper |
| **P2** | 1 | Wake / start day | Partial | Marker/log freeze |
| **P2** | 3 | Plant given herb | Partial | Link to #12 |
| **P2** | 4 | Equip backpack → inventory | Partial | Equip gate |
| **P2** | 6 | Collect herb seeds in field | Partial | Field nodes |
| **P2** | 11 | Bed → spirit (night planetside gate) | Partial | Depends P0+#7 |
| **P2** | 12 | Nurture planted herb (spirit) | Partial | Depends #3 |
| **P2** | 13 | Home portal → camp portal (spirit) | Partial | Camp portal missing |
| — | 5 | Glider → field | **Y** | **Out of scope** this packet |

---

## Architecture Trade-Offs (cite only — where boundaries matter)

| Topic | Layer | Decision (inventory, not API invent) |
|-------|-------|--------------------------------------|
| Form / sleep / rune gate (#9, #7, #11) | **B** (+ **A** contract) | Deep module: callers see `FORM_BODY` / `FORM_SPIRIT` via **named gates** (bed + rune + location policy). Hide phase auto-spirit. Do not add a second form service. |
| Day eject + planetside night boot (#8, #10) | **A** + **B** | One **eject-to-home** quantum reusing FALLBACK glide homeward — not soft-kidnap, not convert stub, not a second transit stack. |
| Camp portal (#13) | **B** | Extend shrine-portal pair pattern (`GP_Portal*`) with `NODE_PORTAL_CAMP` — do not invent a parallel portal subsystem. |
| Bigger planetsides | **A/C/E** | Keep transit/load stream/WP-ready; no WP contract invent in these bites. Failed load → degrade via eject/home, not hang. |

**15-q:** Any Implement PR that invents a new form/eject/portal module API must load A–E + 15-q before merge. Gap SCOUT already forbids inventing WP APIs.

---

## Shared inventory freeze (labels ⊆ feature list ∩ gap)

Reuse only: `NODE_*` · `TOD_*` · `FORM_*` · `EJECT_HOME` · `CAM_T0_*` from `PROTOTYPE_FEATURE_LIST_V1` § Inventory freeze. Prove labels must subset this set.

---

## Inventories (per MUST — N / Partial)

Each row: **Expected (T0)** · **Found (gap)** · **Arrange** · **DONE-WHEN** · **Depends** · **Anti**.

### P0 — #9 Homeworld night w/o bed (`TOD_NIGHT_HOME`) — Partial

| Field | Value |
|-------|-------|
| **Labels** | `TOD_NIGHT_HOME` · `FORM_BODY` · `NODE_BED` (negative prove) |
| **Expected** | On homestead at Night/Dusk **without** successful bed: stay `FORM_BODY`; **no** spirit; **day abilities off** |
| **Found** | `ApplyFormForPhase`: Night **or** Dusk → `bIsSpiritForm` without bed — **fails T0 law** |
| **Arrange** | Homestead · force Night without bed (`hw.TimeOfDay.SetPhase` / dusk) · no `hw.GoToBed` |
| **DONE-WHEN** | Prove: Night@home w/o bed → `FORM:` body (not spirit) + day verbs rejected/off; bed path still reaches spirit only after #7+#11 gates. Grep: `FORM:` · closed_fail if spirit without bed |
| **Depends** | Unblocks correct #11; pairs with #7 |
| **Anti** | Do not “fix” by disabling Night entirely · do not treat soft-kidnap as this law |

### P1 — #2 Kettle + herbs → tea → sprint — N

| Field | Value |
|-------|-------|
| **Labels** | `NODE_KETTLE` · `TOD_DAY` · `FORM_BODY` |
| **Expected** | Interact kettle + herbs → tea → sprint buff ~half day |
| **Found** | No kettle/tea path; MV sprint exists ungated; meal BPs ≠ tea |
| **Arrange** | Homestead day · `NODE_KETTLE` interact · herbs available |
| **DONE-WHEN** | Readable tea craft → sprint buff duration (~half day); ungated MV sprint alone ≠ pass. Prove label `NODE_KETTLE` |
| **Depends** | — |
| **Anti** | Do not count `CRAFT:` demo meals as tea |

### P1 — #7 Rune unlock before bed→spirit — N

| Field | Value |
|-------|-------|
| **Labels** | `NODE_RUNE` · `TOD_DAY` · `FORM_BODY` |
| **Expected** | Day rune unlock **before** bed→spirit works |
| **Found** | `rune` = 0 hits; form phase-driven |
| **Arrange** | Day field path · `NODE_RUNE` · unlock flag persisted |
| **DONE-WHEN** | Without unlock: bed cannot grant spirit planetside night; with unlock: #11 may proceed. Prove `NODE_RUNE` |
| **Depends** | Required by #11 |
| **Anti** | Do not grant spirit on phase alone |

### P1 — #8 Day camp cartoon eject — N

| Field | Value |
|-------|-------|
| **Labels** | `NODE_DAY_CAMP` · `EJECT_HOME` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_CAMP_DAY` |
| **Expected** | Day approach camp → cartoon launch → glider → drop home (**not** lethal) |
| **Found** | Camp landmark + dream convert stub only; `eject` = 0 |
| **Arrange** | Day · approach `GP_RS_HumanoidCamp` / `NODE_DAY_CAMP` · body form |
| **DONE-WHEN** | Threat → `EJECT_HOME` sequence lands homestead; player death CUT; convert stub ≠ pass. Cam `CAM_T0_CAMP_DAY` |
| **Depends** | Defines `EJECT_HOME` for #10 |
| **Anti** | No kill · no convert-as-eject |

### P1 — #10 Planetside night boot home — N

| Field | Value |
|-------|-------|
| **Labels** | `EJECT_HOME` · `TOD_NIGHT_HOME` · `FORM_BODY` · `NODE_GLIDER` |
| **Expected** | Planetside at night **without** bed path → glider boot home (same eject family as #8) |
| **Found** | No reverse boot; bible soft-kidnap ≠ this; FALLBACK is island→planet down only |
| **Arrange** | Planetside · Night · no bed/spirit gate · expect eject home |
| **DONE-WHEN** | Boot home via `EJECT_HOME`; soft-kidnap shrine path ≠ pass |
| **Depends** | #8 eject path (reuse) · #9 law (stay body) |
| **Anti** | Do not invent soft-kidnap as T0 eject |

### P1 — #14 Camp night avoid 1 + soothe 2 — N

| Field | Value |
|-------|-------|
| **Labels** | `NODE_GUARD` · `NODE_SLEEPER` (×2) · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` · `CAM_T0_CAMP_NIGHT` |
| **Expected** | Spirit: avoid 1 guard; soothe 2 sleepers (convert-not-kill) |
| **Found** | Lit stealth volumes only; no guard/sleeper/soothe |
| **Arrange** | Spirit @ camp night · after portals (#13) reachable |
| **DONE-WHEN** | 1 avoid + 2 soothe readable; kill/convert-as-soothe = fail. Cam `CAM_T0_CAMP_NIGHT` |
| **Depends** | #11 spirit · #13 camp reach (soft) |
| **Anti** | `hw.Conversion.Test` ≠ soothe |

#### Narrative load, added 2026-10-02 — this must is the rescue

`TASTE_GATE_T0_ASSETS` Round 5 put the family in the prototype and superseded V1. The
companion travels with you, the camp takes them, and **you are sent back to the homestead**.
Q22 answered **a guard wakes** — detection fires and ejects you.

**That makes `NODE_GUARD` load-bearing for the first time.** Until now "avoid 1 guard" was
flavour next to "soothe 2 sleepers". Now the guard stop is the thing that costs you your loved
one, so **both halves of #14 are earned**: the kidnapping is your doing and the rescue is the
correction.

| | |
|---|---|
| **The story, in must terms** | *release the negative emotions from the camp guards so they sleep* = **soothe 2 sleepers, convert-not-kill** |
| **The guard's new job** | Not an obstacle. The person between you and the captive, who can be **calmed instead of killed** — the same law as homestead combat, pointed at whoever is holding your loved one |
| **New musts implied** | Travelling companion · the captive (held → freed → home) · detection-fires eject · the return leg. **None exist yet** |
| **Blocking** | `camp_named_objects: []` — the camp does not exist, so the middle of this story is unbuilt |

**Anti, extended:** a guard killed rather than calmed is a fail, exactly as killing a sleeper is.
The law is the point.

#### The three actors are not the same job — Lead, 2026-10-02

> *"A guard will be awake that you need to help ease their thoughts so that they fall asleep, the
> other two will be asleep and you can ease their thoughts too to keep them sleeping."*

**This corrects the original reading of #14.** `#14` was written *"avoid 1 guard; soothe 2
sleepers"* and the obvious reading is: one obstacle to avoid, two targets to calm. **That is
wrong.** All three are calmed. They differ in *which direction* they are moved:

| Actor | Start state | What you do | End state |
|---|---|---|---|
| `NODE_GUARD` — the patroller | **AWAKE**, torch lit | reach them unseen, then **ease their thoughts → they fall asleep** | asleep |
| `NODE_SLEEPER` A | **ASLEEP** | ease their thoughts **→ they keep sleeping** | asleep |
| `NODE_SLEEPER` B | **ASLEEP** | ease their thoughts **→ they keep sleeping** | asleep |

**So "avoid 1 guard" survives, but as traversal rather than as the goal.** You are not avoiding
them — you are approaching someone you have to reach, without being seen first. The avoidance is
how you get there; the calming is why you came.

**The awake one is the hard one and the two sleeping ones are the maintenance.** Putting someone
to sleep is the act; keeping them asleep is the care. *That is V2b — gather by day, tend by
night — inside a single must, and it is why the gentle path is not a shortcut here.* There is no
version of this beat where the efficient thing and the kind thing are different, because there is
no efficient version.

⚠️ **This widens #16's gate from two actors to three.**

#### The rescue is now gated on #14 — Lead, 2026-10-02 (second refinement)

> *"You will stumble upon the camp during the day and your loved one will be taken and you
> will be booted back to the homeworld. During the night you will use your spirit form and
> spirit-stealth gameplay to get to the guards and ease their suffering so that they go to
> bed. Once they are in bed, you will free your loved one."*

**This gives #14 a downstream consequence, which it never had.** Until now "soothe 2 sleepers"
was a must with nothing behind it — you could skip it and the night still resolved. Now:

| | |
|---|---|
| **Day** | Stumble on the camp in daylight → companion taken → ejected home. **This is what #8 was for.** It had no cause until now |
| **Night** | Spirit form (bed **and** rune) → travel down → **spirit-stealth** to the guards → ease their suffering so they go to **bed** → free the companion |
| **The lock** | Freeing the companion requires **both sleepers ASLEEP**. Not "converted" — asleep, in bed |
| **Anti** | Freeing them with either sleeper awake is a **fail**, exactly as killing a sleeper is. No force option |

**#14 stops being skippable.** Skip the soothe and you stand beside your companion unable to
open the lashings, because two people are awake and grieving. That is the whole beat: the soothe
is not a side objective, it is the lock on the door.

**One actor, two tests.** The single `NODE_GUARD` ejects you *by day* (Q22 — you were seen) and
is what you must avoid *by night* (spirit-stealth). Opposite solutions to the same character.

#### Two musts this exposes, and neither exists

| Missing | Why it is load-bearing |
|---|---|
| **`SPIRIT_STEALTH`** | The Lead named spirit-stealth as *the* means of reaching the guards. The must list has a stealth **family** — `NODE_RUNE`, M7, a gate flag on the ground — but nothing for moving **unseen while in spirit form**. Without it there is no way to reach the guards, so M14 is unreachable |
| **`SLEEPER_STATE_ASLEEP`** | The freedom gate needs a state distinct from "converted". Neither the roster nor `EConvertedFoeRole` carries sleep/asleep, and conflating the two would let a *converted* sleeper satisfy a gate that should require a *sleeping* one — which inverts the beat |

Both are recorded in `Lib/02_Zones/combat/CAMP.json` under `new_labels_needed`. Neither is a
taste question and neither is written yet.

### P1 — #15 What a spirit may TOUCH — **N (new, 2026-10-02)**

Raised by `VISION_BOARD` **V2b** (*"gather by day, tend by night"*), which made the touch
question load-bearing for two separate beats that both did not exist before it.

| Field | Value |
|-------|-------|
| **Labels** | `FORM_SPIRIT` · `NODE_PLANT_SLOT` · `NODE_CAPTIVE` · `NODE_GUARD` · `NODE_SLEEPER` |
| **Expected** | In spirit form the player may interact with **soil** and with **the captive's ropes**. They may **not** interact with `NODE_GUARD` |
| **Found** | **Nothing.** No touch rule exists in `Source/`. Not a partial — absent |
| **Arrange** | Spirit at the garden and at the camp, same form, different permissions |
| **DONE-WHEN** | Soil interaction succeeds as spirit · rope interaction succeeds as spirit · guard interaction is refused as spirit · **the refusal is logged**, not silent |
| **Depends** | #11 spirit · #12 nurture |
| **Anti** | One blanket verb for all spirit interactions · silent refusals · spirit able to calm a guard by touching it |

**Why it is P1 and not a detail.** Both the garden (#12) and the rescue (#16) are *night-time
tending*, and neither can be built without it. Every rule written tonight sits on top of this.

**Logged refusals matter more than the permissions.** A refusal the player cannot see reads as a
broken game; a logged one is legible. That is the same lesson as the spirit gate's `closed_fail`
case, where the whole point was that the failure is visible.

### P1 — #16 Free the captive — gated on sleepers ASLEEP — **N (new, 2026-10-02)**

| Field | Value |
|-------|-------|
| **Labels** | `NODE_CAPTIVE` · `NODE_SLEEPER` (×2) · `NODE_GUARD` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` |
| **Expected** | **All three** actors calm — the awake guard put to sleep, the two sleepers kept asleep — then the captive can be freed. **#14 is the lock on this door** |
| **Found** | **Nothing.** No captive actor, no sleep state, no calm state, no freedom gate |
| **Arrange** | Night · after #14 · at the camp |
| **DONE-WHEN** | All three calm → freed, and the return leg to the homestead is reachable · **any one of the three not calm → refused** · a **killed** actor does not count as calm and does not open the door |
| **Depends** | #14 soothe · #15 touch rule · #17 stealth (to reach the guard) |
| **Anti** | Converted-but-not-asleep satisfying the gate · killing an actor to make the count right · forcing the ropes open · calm-on-two-of-three being enough |

**Widened from two actors to three, 2026-10-02.** The gate was first written as "both sleepers
asleep" before it was known that the **guard is also calmed and also has to be asleep**. An
actor who is calmed but not yet asleep is not done, so the count is three and all three must
match.

**The distinction this must exists to enforce:** `EConvertedFoeRole` already has five roles, and
conversion is what happens to foes you **defeat**. A converted actor is not a sleeping one, and
it is not a calmed one. Conflating them lets the player defeat the three and unlock the captive —
which inverts the beat, because the design is that the *gentle* path is the only path.

### P1 — #17 Spirit-stealth — **CLOSED (`APPROVE SS-A`, 2026-09-21)** · extend for the camp

⚠️ **CORRECTED 2026-10-02 — this row previously read `Found: Nothing`, and that was false.** See
the correction block below before touching the Found column.

Named by the Lead as the means of reaching the guards: *"use your spirit form and spirit-stealth
gameplay to get to the guards."*

| Field | Value |
|-------|-------|
| **Labels** | `NODE_GUARD` · `FORM_SPIRIT` · `TOD_NIGHT_SPIRIT` · `SM_Camp_Torch` · `SM_Camp_Fire` |
| **Expected** | **Spirit-blue light is visibility.** Getting close to the campfire's blue centre, or into the glow around the patrolling guard's blue torch, makes you **visible to the guard** |
| **Found** | **CLOSED and implemented** — `HomeWorldSpiritStealthComponent.{h,cpp}` (414-line .cpp), `HomeWorldSpiritLitVolume.h`, `EHomeWorldSpiritLitSourceKind` (Campfire / NpcTorch / SpiritTorch reveal; BodyMundaneTorch does not). `Docs/25_SPIRIT_STEALTH_IMPL.md` **CLOSED / COMPLETE**, all DONE-WHEN ticked. Feel layer in `Docs/31_SPIRIT_STEALTH_FEEL.md` |
| **Arrange** | Night · at the camp · after #13 |
| **DONE-WHEN** | You are unseen outside both light radii · entering **either** radius makes you visible **legibly** · the torch radius **moves with the guard**, so a patrolling guard sweeps a moving pocket of danger · breaking back out of the light stops it |
| **Depends** | #11 spirit · #13 camp reachable · #15 touch rule |
| **Anti** | Stealth as a stat roll · invisibility as a toggle with no counter · a guard who cannot notice anything · light with no visual tell |

#### The false negative, and what it cost — recorded because it will happen again

I recorded this as *"**Nothing.** No stealth state, no awareness, no detection"* on 2026-10-02.
Every one of those four things exists, and the track was already **CLOSED with a Lead stamp**.

**The cause was not missing documentation — it was a missing pointer.** The must list answers
*"what must be true"*; *"is it built?"* is answered in the per-subsystem **track docs**, and
nothing in the T0 track pointed at `Docs/25_SPIRIT_STEALTH_IMPL.md`. So the answer was a shrug.

**This is the same failure class as the broken shrine.** The shrines were in no spec, so a lintel
sitting on the ground survived every gate. There a geometry check had nothing to measure; here an
index had nothing to point at. Both are "nothing referenced it".

**Two rules now follow, and both are enforced rather than noted:**

1. The `Found` column may say `N` **only** if no `APPROVE`-stamped track doc claims the mechanic.
   The cross-link table is `Docs/CANON_MAP.md` §3.
2. `Content/Python/tests/test_canon_map.py` asserts #17 cites its stamp and can never read `N`
   again. **A map nobody checks goes stale, and stale is how this happened.**

**Settled 2026-10-02 by the Lead — this is BOTH a light level and a per-actor area, not either
or, and they are the same mechanic:**

| Source | Kind | Behaviour |
|---|---|---|
| **Campfire** | static light, **spirit-blue at the centre** | a fixed radius around the fire's middle where you are visible |
| **Patrolling guard's torch** | **moving** light, blue-tinged | an area around the guard that travels with them |

**Why this is the right shape for this beat.** The guard is not a thing you avoid — it is
someone you must reach. So avoidance becomes **traversal** rather than the goal, and the mechanic
rewards patience rather than speed. And because both sources are **spirit-blue**, the player
learns **one rule — blue means you can be seen here** — in a single glance, from the art alone,
with no tutorial. That is `VISION_BOARD`'s *"the world announces what it wants by its shape
alone"* applied to a stealth system: one colour, two forms, static and moving.

⚠️ The moving torch is what makes this non-trivial. A static radius is a lookup; a radius that
travels with a patrolling actor means the safe pocket changes as they walk, so the player is
reading a **moving** safe zone rather than a fixed one.

### P2 — #1 Wake / start day — Partial

| Field | Value |
|-------|-------|
| **Labels** | `NODE_WAKE` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_WAKE` |
| **Expected** | Explicit homestead start-day beat |
| **Found** | `GP_PlayerStart` + day phase; no frozen wake label/log |
| **Arrange** | PIE spawn / wake → Dawn |
| **DONE-WHEN** | Frozen `NODE_WAKE` + readable day-start prove (`CAM_T0_WAKE`) |
| **Depends** | — |
| **Anti** | — |

### P2 — #3 Plant given herb — Partial

| Field | Value |
|-------|-------|
| **Labels** | `NODE_PLANT_SLOT` · `TOD_DAY` · `FORM_BODY` |
| **Expected** | Day plant **given** herb nearby outside → marks slot for spirit nurture |
| **Found** | Planters + `GP_N1_Crop` nurture exist; not plant-given-herb beat |
| **Arrange** | Outside homestead · given herb in hand/inventory |
| **DONE-WHEN** | Plant interact marks `NODE_PLANT_SLOT` consumable by #12 |
| **Depends** | Feeds #12 |
| **Anti** | N1 seed-nurture alone ≠ plant-given beat |

### P2 — #4 Equip backpack → inventory — Partial

| Field | Value |
|-------|-------|
| **Labels** | `NODE_BACKPACK` · `TOD_DAY` · `FORM_BODY` |
| **Expected** | Equip backpack → inventory available |
| **Found** | Inventory-lite present; no backpack equip gate |
| **Arrange** | Homestead day · unequipped → equip |
| **DONE-WHEN** | Inventory gated by equip; prove `NODE_BACKPACK` |
| **Depends** | Soft: field gather (#6) |
| **Anti** | Open inventory without equip ≠ T0 pass |

### P2 — #6 Collect herb seeds in field — Partial

| Field | Value |
|-------|-------|
| **Labels** | `NODE_FIELD_GATHER` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_FIELD` |
| **Expected** | Open-field herb seed collect after glide landing |
| **Found** | Gather systems + RES meshes; no frozen field nodes near landing |
| **Arrange** | Post-#5 landing · field nodes |
| **DONE-WHEN** | Explicit `NODE_FIELD_GATHER` near landing; `GATHER:` on path |
| **Depends** | #5 present (Y) |
| **Anti** | Distant/demo gather ≠ field beat |

### P2 — #11 Bed → spirit (night planetside gate) — Partial

| Field | Value |
|-------|-------|
| **Labels** | `NODE_BED` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` · `CAM_T0_BED` · `NODE_RUNE` |
| **Expected** | After rune: bed → spirit as **night planetside** gate |
| **Found** | Bed→Night→spirit works; **not** rune-gated; spirit also on Dusk/Night w/o bed |
| **Arrange** | Homestead bed · rune unlocked · prove blocked without rune / without bed |
| **DONE-WHEN** | Spirit planetside night **only** via bed after rune; #9 still holds w/o bed. Cam `CAM_T0_BED` |
| **Depends** | **#9 + #7** |
| **Anti** | Phase-only spirit ≠ pass |

### P2 — #12 Nurture planted herb (spirit) — Partial

| Field | Value |
|-------|-------|
| **Labels** | `NODE_PLANT_SLOT` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` |
| **Expected** | Spirit nurture of **planted given herb** from #3 |
| **Found** | N1 nurture present; not linked to plant-given slot |
| **Arrange** | Spirit · `NODE_PLANT_SLOT` from #3 |
| **DONE-WHEN** | Nurture succeeds on planted slot; day/body nurture ≠ pass |
| **Depends** | #3 · #11 |
| **Anti** | N2 stored-only ≠ this beat |

### P2 — #13 Home portal → camp portal (spirit) — Partial

| Field | Value |
|-------|-------|
| **Labels** | `NODE_PORTAL_HOME` · `NODE_PORTAL_CAMP` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` |
| **Expected** | Spirit home portal → **camp** portal |
| **Found** | Home ↔ planet return shrine present; **no** camp portal pair |
| **Arrange** | Spirit · `NODE_PORTAL_HOME` → `NODE_PORTAL_CAMP` at humanoid camp |
| **DONE-WHEN** | Pair lands at camp; return-shrine-only ≠ camp beat |
| **Depends** | #11 · enables #14 reach |
| **Anti** | Do not invent second portal subsystem (A–E cite) |

---

## Recommended Implement bite order (ONE_SHOT — Conductor opens)

One unknown per bite. Host: OpenCode ≡ Cursor until tokens restored.

| Order | Bite id | MUST # | Pass-bar (short) |
|------:|---------|--------|------------------|
| 1 | `T0_M9_NIGHT_HOME_GATE` | 9 | Night@home w/o bed = body + day abilities off |
| 2 | `T0_M7_RUNE_UNLOCK` | 7 | Rune unlock flag; bed spirit blocked without it |
| 3 | `T0_M11_BED_SPIRIT_GATE` | 11 | Bed+rune → spirit; still respects #9 |
| 4 | `T0_M8_DAY_CAMP_EJECT` | 8 | Cartoon `EJECT_HOME` from day camp |
| 5 | `T0_M10_PLANETSIDE_BOOT` | 10 | Night planetside w/o bed → same eject family |
| 6 | `T0_M2_KETTLE_TEA` | 2 | Kettle→tea→half-day sprint |
| 7 | `T0_M3_PLANT_GIVEN` | 3 | Plant given herb → `NODE_PLANT_SLOT` |
| 8 | `T0_M12_NURTURE_PLANTED` | 12 | Spirit nurture that slot |
| 9 | `T0_M4_BACKPACK_EQUIP` | 4 | Equip gates inventory |
| 10 | `T0_M6_FIELD_GATHER` | 6 | Field nodes near landing |
| 11 | `T0_M1_WAKE_LABEL` | 1 | Frozen wake prove |
| 12 | `T0_M13_PORTAL_CAMP` | 13 | Home→camp spirit portal |
| 13 | `T0_M14_GUARD_SOOTHE` | 14 | Avoid 1 + soothe 2 |

Conductor may reorder within P0→P1→P2 for DESKTOP risk; do **not** open #11 before #9+#7, or #10 before #8, or #12 before #3, or #14 before spirit reach (#11, prefer #13).

---

## Prove / taste

| Class | Rule |
|-------|------|
| Team prove | Readable actors + existing greps/logs (`FORM:` `FALLBACK:` `GATHER:` `NURTURE:` `STEALTH:`) toward DONE-WHEN |
| soft_fail | KEEP-LOCAL markers missing — re-place / reopen level |
| closed_fail | T0 law broken (e.g. spirit w/o bed) or zero impl for MUST |
| Taste | Art / NightMix / cam polish = Lead later — not this APPROVE |

Cheats: existing only when a bite DONE-WHEN names them (`Docs/30`).

---

## Routing

| # | Owner | Action | Blocked until |
|---|-------|--------|---------------|
| 0 | **Lead** | `APPROVE-T0-MECHANIC-INV` | — |
| 1 | Conductor | Open bite 1 (`T0_M9_…`) only | Lead APPROVE |
| 2 | Implement → Test | Named bite Act + prove | Conductor open |
| — | Design | Amend inventories if gap bounce | Conductor ask |

**eggbot:** N · **child Research:** N unless an Act names a true external-info hole.

---

## Accept checklist (Lead)

- [ ] Covers all N (5) + Partial (8); excludes full Y #5
- [ ] P0 = #9 sleep/form gate called out
- [ ] Bite order respects deps (#9+#7→#11 · #8→#10 · #3→#12 · spirit→#14)
- [ ] No WP API invent; A–E cite only
- [ ] Stamp: `APPROVE-T0-MECHANIC-INV`

---

## Added 2026-10-02 — #15, #16, #17

Three musts that existed as prose in spec files and were tracked nowhere. Added as **P1**,
all three currently `N` (absent, not partial):

| # | Must | Blocks | State |
|---|---|---|---|
| **#15** | What a spirit may **TOUCH** | #12 nurture, #16 rescue — sits under both | N |
| **#16** | Free the captive, gated on sleepers **ASLEEP** | the rescue climax; #14's whole purpose | N |
| **#17** | **Spirit-stealth** | #14 outright — it is the named way in | **CLOSED — this was wrong, see the #17 correction** |

**Two of these are P1 only because `VISION_BOARD` V2b moved them.** Before *"gather by day,
tend by night"* there was no night-time tending at all, so "can a spirit touch soil" was an idle
question. The moment the garden and the rescue both became night verbs, the permission table
became load-bearing for two of the fourteen existing musts.

**#17 is CLOSED, not open.** I queued its shape as the single Lead question I could not answer,
then asked it — and the answer (*spirit-blue campfire + the guard's blue torch*) was **already the
LOCKED bible**: `SPIRIT_STEALTH_BIBLE.md` line 1 reads *"torch-class light (NPC-carried torches,
campfires, spirit torches) can illuminate the spirit world"*, closed under `APPROVE SS-A`. The
question was never open, and neither was the mechanic. That is the index failure, not a taste
call — see `Docs/CANON_MAP.md` §1 and §3.

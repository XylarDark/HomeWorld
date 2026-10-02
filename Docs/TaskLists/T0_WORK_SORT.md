# T0 WORK SORT — art vs no art

| Field | Value |
|---|---|
| **Status** | ACTIVE — the working sort |
| **Date** | 2026-10-02 |
| **Purpose** | Split the 13 bites by whether they need geometry, so no time is spent on art for beats that do not, or mechanics waiting on art they do not need yet. |
| **Companion** | [`T0_ROADMAP.md`](T0_ROADMAP.md) (why) · [`T0_PROTOTYPE_TRACK.md`](T0_PROTOTYPE_TRACK.md) (state) |

**Your images are for look and shape language — not for blockers.** Greybox is silhouette,
proportion and one of ten masters. Reference art is not on the critical path for any beat.
§3 lists where your images actually help, and it is a short list.

---

## 1. The sort

| Bite | Beat | Art? | What it needs | Can start now |
|---|---|---|---|---|
| 1 | `T0_M9` night w/o bed | **no** | none — a negative law | ✅ |
| 2 | `T0_M7` rune unlock | **tiny** | a rune mesh, ~12 tris | ✅ |
| 3 | `T0_M11` bed → spirit | **yes, small** | shrine proportion fix; topology exists | ✅ code now, art after |
| 4 | `T0_M8` day-camp eject | **yes** | **the camp** (GATE 1) | ⚠️ code now, art needed |
| 5 | `T0_M10` planetside boot | **yes** | reuses GATE 1's camp | ⚠️ code now, art needed |
| 6 | `T0_M2` kettle → tea | **tiny** | a kettle, ~12 tris | ✅ |
| 7 | `T0_M3` plant given herb | **tiny** | planters already exist | ✅ |
| 8 | `T0_M12` nurture planted | **yes, small** | a plant on the existing glow | ✅ code now, art after |
| 9 | `T0_M4` backpack equip | **no** | none — UI/state law | ✅ |
| 10 | `T0_M6` field gather | **no** | 4 bushes + 6 res meshes exist | ✅ |
| 11 | `T0_M1` wake label | **no** | none — a label | ✅ |
| 12 | `T0_M13` home → camp portal | **yes** | camp portal mesh | ⚠️ code now, art needed |
| 13 | `T0_M14` guard + soothe | **yes, all of it** | **the camp** (GATE 1) | ⚠️ code now, art needed |

**5 bites need no art. 3 need a single small prop. 5 need the camp.**

---

## 2. What this means for how we work

**The bite order is sequential and does not wait for art.** The inventories forbid opening
#11 before #9+#7 — not "before the shrine looks right." So the next several bites are
**pure mechanics**, and the art work is a *separate, parallel* concern that only bites 4, 5,
12, 13 genuinely wait on.

### Queue A — no art dependency · start immediately

| # | Work | Why first |
|---|---|---|
| A1 | **`T0_M9` behaviour test** | `LOCAL_PASS` + most load-bearing law in the track. A silent regression breaks bites 3, 5, 13. Same shape as the conversion test (`6788aab`) |
| A2 | **`T0_M7` rune behaviour test** | gates bite 3; the gate logic exists and is correct (`CanEnterSpiritForm` = sleep ∧ rune) |
| A3 | `T0_M2` kettle test | ungated sprint is a live T0 law violation today |
| A4 | `T0_M3` plant test | feeds bite 8 |
| A5 | `T0_M4` backpack test | one line of law: inventory is gated by equip |
| A6 | `T0_M6` field-gather test | best-served beat art-wise |

**Every one of these is a test against a law that already has an implementation.** No new
mechanics, no new art, no waiting. This is the fastest real progress available.

### Queue B — one prop each · cheap, self-contained

| # | Work | Note |
|---|---|---|
| B1 | `NODE_RUNE` mesh (~12 tris) | `M_CliffRock` — a stone, per art bible "handmade spirit cue, not a tech gate" |
| B2 | `NODE_KETTLE` mesh (~12 tris) | `M_CliffRock` + `M_WoodWild` |
| B3 | Plant on `SM_NurtureGlow_Crop` | M12 currently reads as a light, not a crop |

### Queue C — the camp · one location, four beats

`GATE 1` in the roadmap. `camp_named_objects: []` — the camp does not exist.
Authored as a `combat`-family greybox volume, verified by `graybox_spec_reader.py`.

### Queue D — spirit proportion · three beats

Narrow the base, raise the posts. **Topology already correct** — the gap exists. Blocked on
the `SM_SpiritWound_01` crater-or-marker decision.

---

## 3. Where your images actually help — a short list

Reference art is **not** blocking any beat. It lands on the two things greybox cannot invent:

| Your images | Why | When |
|---|---|---|
| **Camp silhouettes** — guard, sleeper alcoves, fire | `combat` is a locked signature: *jagged asymmetric wedge, tallest in frame*. I can hit the proportion; I cannot invent the read | before authoring GATE 1 |
| **Shrine shape language** | `spirit` is *tall thin vertical with a see-through gap*. The gap exists; what the gap should *look like* is taste | before GATE 2 |
| Rough look target per family | helps choose among greybox variants later | any time |

**Not needed for:** any mechanics test, any behaviour test, the rune, the kettle, the plant,
the field nodes, the backpack, or the wake label.

---

## 4. Efficiency rules for this track

Agreed, and written down so it survives a session break:

1. **No harness work.** `Docs/36` §2: three triggers. Fitness reads it, it does not get worked.
2. **No new taste gates.** Everything below is agent-owned implementation inside an approved scope.
3. **One commit per task, explicit paths.** Conventional Commits. Product, not `harness`.
4. **`npm run verify` is the only gate.** Not a ritual — it is the C++ build plus the behaviour
   tests, which is the thing that proves mechanics work.
5. **Every test asserts a T0 label** — `FORM_*` / `NODE_*` / `EJECT_HOME` — and uses
   `closed_fail` for a broken law. Not ad-hoc names.
6. **No art promoted to `Content/`.** `Docs/20` — drafts only.
7. **Report deltas, not activity.** A commit that says what changed in the *game* is worth
   more than one that says what changed in the tooling.

---

## 5. Start here

**A1 is the first move** and it needs nothing from you:

`T0_M9` is `LOCAL_PASS` but has **no behaviour test**, and it is the law three other bites
depend on. The implementation is already correct — I read it:

```cpp
const bool bSpirit = bSpiritCapablePhase && CanEnterSpiritForm();
// CanEnterSpiritForm() == bSpiritSleepGateGranted && bRuneGateUnlocked
```

So the test asserts: Night without gates → `FORM_BODY`; Night with sleep+rune → `FORM_SPIRIT`;
Dawn clears the sleep gate; phase alone never grants spirit. That last one is the
`closed_fail` case your inventories name.

**Queue A in order. A2–A6 are the same shape.** When you have images for the camp, GATE 1
becomes unblocked and I author it.

---

*13 bites sorted. 5 need no art, 3 need one prop, 5 need the camp. Mechanics do not wait
for art; art waits for nothing but your time.*

# T0 ROADMAP — a playable prototype, sequenced

| Field | Value |
|---|---|
| **Status** | ACTIVE — the one track |
| **Date** | 2026-10-02 |
| **Question it answers** | *What order do we build things so the prototype is playable in a world that makes sense?* |
| **Canonical beats** | [`T0_MECHANIC_INVENTORIES_V1.md`](../handoffs/T0_MECHANIC_INVENTORIES_V1.md) — 13 bites, deps unbroken |
| **Rollup** | [`T0_PROTOTYPE_TRACK.md`](T0_PROTOTYPE_TRACK.md) — state, vocabulary, open items |
| **Not this** | Taste work (parked) · harness work (idle per `Docs/36` §2) |

---

## 1. How the asset pipeline actually ties in — the honest answer

The pipeline is **not parallel to T0. It is on T0's critical path**, and for three beats it
is the *only* thing standing between "merged" and "playable."

**Measured from the live blend, 2026-10-02.** The T0 logic is components and markers; the
art is meshes. Where a beat needs a place to happen, these are two different things.

| Beat | Logic | Art in the blend | Gap |
|---|---|---|---|
| **M14** camp night: avoid 1 guard, soothe 2 sleepers | `UHomeWorldSpiritStealthComponent` (414 LOC) | **nothing.** No `Guard`, `Sleeper`, `Camp` or `Soothe` mesh exists anywhere | **the entire beat has no place** |
| **M13** home portal → camp portal | `AHomeWorldShrinePortalTrigger` | `GP_PortalA`/`B` exist in code; **no camp portal mesh** | destination is a void |
| **M8/M10** eject home from camp | `EJECT_HOME` × 36 hits in code | `GP_RS_HumanoidCamp` is a code marker; **no camp mesh** | you eject *from* nothing |
| **M12** nurture planted herb | `AHomeWorldNurtureTarget` | `SM_NurtureGlow_Crop`, `SM_CropProxy_Nurtured_B` — glows only, no plant | reads as a light, not a plant |
| **M6** field gather | gather subsystem | 4 bushes, 6 `SM_RES_*` meshes, path segs A/B | the best-served beat |
| **M11** bed → spirit | `UHomeWorldGoToBedTriggerComponent` | shrines exist (5 parts each) | proportion wrong, see §4 |

⚠️ **`camp_named_objects: []`.** That is the finding. M14 is the climax beat of the prototype —
the one where the theme is proved, *avoid one guard, soothe two sleepers* — and the camp it
happens in **does not exist as geometry.** The component will fire on an empty plain.

**This is why the pipeline cannot be a parallel track.** Sequencing it last means shipping
M14 as a mechanic with no world, which is exactly the "mechanically present, visually absent"
defect the taste gates named — arriving through the level-design door.

### What the pipeline buys, per beat

| Outcome | How it is measured | Currently |
|---|---|---|
| A beat's place exists | `graybox_spec_reader.py` finds the volume in the blend | tool **built and running** |
| Its name is canon | allocated from `MVP_EXPORT_MANIFEST.md`, never invented | 23 FBX exported |
| It is sized right | bbox within per-class tolerance, pivot Z = 0 | reader asserts this |
| Its family reads at 20 m | band + openness collision check | spirit reads `mid`, must be `tall` |
| It obeys the art gate | one of ten masters, generated textures inadmissible | **2 non-canon materials present** |

**The reader is the join.** It runs against the live blend and emits
`docs/qa/GRAYBOX_SPEC_REPORT.md`. Every art task below ends with that report moving, not with a
screenshot.

---

## 2. The sequence

Four gates, each unblocking the next. Not a wish list — a dependency order.

### GATE 0 — Make the current state legible · *no new work, no new art*

**Nothing ships on top of an unknown.** Six beats are merged and unproven, one gate is
unstamped, and the art report reads FAIL. Fix the measurement first.

| # | Step | Owner | Why first |
|---|---|---|---|
| 0.1 | **Stamp or void `APPROVE-T0-MECHANIC-INV`** | Lead | 13 PRs merged against an unstamped gate |
| 0.2 | **Run the 6 `NO_VERDICT` proves** — M2, M3, M4, M6, M7, M_default | Lead | merged + unproven. Zero code, converts unknown → known |
| 0.3 | Re-run `npm run t0:evidence` | agent | the ledger is a summary of local artifacts; it goes stale |
| 0.4 | **Decide the island-top truth** | Lead | 3 docs, 3 answers, blend matches none |
| 0.5 | Decide `SM_SpiritWound_01`: crater or standing marker | Lead | blocks §4 spirit work |

⚠️ **0.4 and 0.5 are forks, not tasks.** `SM_IslandTop.json` says 21×14×0.5;
`GRAYBOX_LAYOUT.md` says 21×14×**4.0**; the blend is 19.3×10.7×0.45. And a flat crater cannot
read as *tall thin vertical with a see-through gap*. Both are design calls. I am not making
them and not guessing at them.

### GATE 1 — The camp · *unblocks M8, M10, M13, M14 — four beats*

**The single highest-leverage art task in the track.** One location, four beats, and the
climax depends on it. Author it as a `combat`-family volume per art bible §8 (*jagged
asymmetric wedge, tallest in frame*) and place it at the camp origin.

| # | Step | Detail |
|---|---|---|
| 1.1 | Spec the camp in `Lib/02_Zones/Combat/` (DEC-0024 — one dir per family) | ground, ridge, the guard's line of sight, 2 sleeper alcoves |
| 1.2 | Author greybox volumes — **not** hero art | `M_CliffRock` + `M_WoodWild` + `M_BeastStylized` only |
| 1.3 | Place guard + 2 sleepers so M14's geometry exists | this is the beat's missing world |
| 1.4 | Verify: `graybox_spec_reader.py` → report PASS for `combat` | measured, not eyeballed |
| 1.5 | Add `CAM_T0_CAMP_DAY` and `CAM_T0_CAMP_NIGHT` framings | both already referenced in `Source/` |

**No `Content/` promote.** `Docs/20` — drafts only, sidecar + `AI_ASSET_LOG` row.

### GATE 2 — Spirit proportion · *unblocks M11, M12, M13 — three beats*

Cheap because the topology is already right. **Measured:** both shrines are base + 2 posts +
lintel + glow, five parts, hard-shaded masters. **The gap already exists.** The defect is
proportion — 1.8 m posts on a 1.4 m base, and the wide base dominates the bounding volume, so
the measured aspect lands `mid` instead of `tall`.

| # | Step | Detail |
|---|---|---|
| 2.1 | Narrow the base, raise the posts | **correct in place** — no rival shrines beside them |
| 2.2 | Land `SM_SpiritWound_01` per the 0.5 decision | blocked on 0.5 |
| 2.3 | Verify: spirit volumes read band `tall`, collision check clean | reader asserts |
| 2.4 | Give `SM_NurtureGlow_Crop` an actual plant | M12 currently reads as a light, not a crop |

### GATE 3 — Clear the blocking art findings · *everything else*

| # | Step | Detail |
|---|---|---|
| 3.1 | Remap `M_FamilySilhouette`, `M_ValleyNight` | not among the ten masters — an 11th family each |
| 3.2 | Fix the three porch modules outside the cabin footprint | or widen the spec's footprint if the porch is meant to project |
| 3.3 | Apply the island-top decision from 0.4 | resize mesh **or** correct the spec — not both |
| 3.4 | Re-run reader → **report PASS** | the gate for "the art obeys canon" |

### GATE 4 — Prove and accept · *Lead only, throughout*

Every beat above is unfinished until its prove is run and stamped. **Accepted is 0 of 14** and
the tool will never set it — acceptance is not derivable from a file.

---

## 3. How this interleaves with the bite order

**The bite order is not mine** — it is the inventories' recommended order with its dependency
rules, and it stays. The art column is what each beat is *waiting on*.

| Bite | Beat | Ledger | Art gate it waits on | Status |
|---|---|---|---|---|
| 1 | M9 night w/o bed | `LOCAL_PASS` | none — a negative law | **unblocked** |
| 2 | M7 rune unlock | `NO_VERDICT` | none — a flag + interact | **unblocked** |
| 3 | M11 bed → spirit | `PROVISIONAL` | **GATE 2** | blocked on art |
| 4 | M8 day-camp eject | `LOCAL_PASS` | **GATE 1** | blocked on art |
| 5 | M10 planetside boot | `PROVISIONAL` | **GATE 1** (reuses `EJECT_HOME`) | blocked on art |
| 6 | M2 kettle → tea | `NO_VERDICT` | none — hub furniture exists | unblocked |
| 7 | M3 plant given herb | `NO_VERDICT` | none — planters exist | unblocked |
| 8 | M12 nurture planted | `PROVISIONAL` | **GATE 2** (2.4) | blocked on art |
| 9 | M4 backpack equip | `NO_VERDICT` | none — UI/state law | unblocked |
| 10 | M6 field gather | `NO_VERDICT` | none — best-served beat | unblocked |
| 11 | M1 wake label | `LOCAL_PASS` | none — a label | unblocked |
| 12 | M13 home → camp portal | `PROVISIONAL` | **GATE 1** (destination) | blocked on art |
| 13 | M14 guard + soothe | `PROVISIONAL` | **GATE 1** (the whole camp) | blocked on art |

**7 of 13 bites are unblocked today.** That is the good news and it is measurable: M9, M7, M2,
M3, M4, M6, M1 need no new art at all.

⚠️ **But the bite order is sequential, so GATE 1 cannot simply be deferred to the end.** Bites
1–2 and 6–11 are mechanically ready, yet bite 3 is blocked on art — and the inventories forbid
opening #11 before #9+#7 are done. That is fine: it means the next several bites are
*mechanics* work, and GATE 1 is what the Lead should be having built in parallel by hand, or
by a second agent on a second worktree. **Two agents, one tree, one writer** is already the
rule (`AGENTS.md` Parallelism).

---

## 4. What "worthy of a prototype" costs, honestly

Not decoration — the four things that decide whether the prototype reads as a game:

| Cost | Size | Why it is not optional |
|---|---|---|
| The camp exists | **GATE 1** | 4 beats including the climax |
| Spirit reads spirit | **GATE 2** | the player must know what spirit *is* without a HUD |
| Art obeys canon | **GATE 3** | 2 non-canon materials, 3 misplaced modules, 1 wrong island |
| Every beat is proven | **GATE 4** | 0 of 14 accepted |

**Two things I am not proposing, and why.**

**No hero art.** Every volume here is greybox/prototype tier — that was the brief, and art
bible §5 Layer A says cheap mass holding silhouette is the *correct* state, not a compromise.
The ten masters carry it.

**No new mechanic families.** `heal`, `stealth` and `combat` have no volume in the 39-volume
layout. GATE 1 authors the camp for `combat` because M14 needs a place. `heal` and `stealth`
stay empty — they are not in the 13 bites, and authoring sections for them is level design
that the taste gates route to the Lead, not something to smuggle in through a greybox volume.

---

## 5. The first three actions

**Nothing here is a taste decision and nothing touches the harness.**

1. **You:** stamp or void `APPROVE-T0-MECHANIC-INV`, then run the 6 unproven proves. (GATE 0)
2. **You:** decide the island-top truth and the spirit-wound shape. Two forks, both blocking.
3. **Me, on your word:** bite 1 hardening — add the behaviour test asserting `FORM:` and
   `closed_fail` on phase-only spirit. `LOCAL_PASS`, most load-bearing law in the track, and
   a silent regression there breaks bites 3, 5 and 13 at once. Same shape as the conversion
   test that shipped as `6788aab`.

**Then I start GATE 1**, because four beats and the climax are waiting on it, and because
"a world that makes sense" is not true until the camp exists.

---

## 6. Honest limits of this plan

| Limit | Consequence |
|---|---|
| I have not run any of the 6 proves | the ledger says `NO_VERDICT`; it might pass, and that is unknown, not bad |
| I cannot see PIE | every statement about the blend is measured from the `.blend` via MCP, not from playing it |
| `camp_named_objects: []` is a name search | a camp built under a different name would not show. The mesh count near the camp origin (5 objects: beast, beast pad, 2 spirits, gathering bush) is the corroborating evidence |
| Art estimates are gate-sized, not hour-sized | I have not modelled authoring time and will not pretend to |
| The `M_ValleyNight` / `M_FamilySilhouette` question is unresolved | 2 materials may be legitimate variants I have not seen the justification for. Art bible §10 allows named instances; these are not in the allowed list, but the allowed list predates them |

---

*One track, four gates, 7 of 13 bites unblocked today. The pipeline is not a parallel
workstream — for four beats it is the whole difference between a mechanic and a place.*

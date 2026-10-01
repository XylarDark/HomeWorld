# TASTE_GATE_GRAYBOX_SILHOUETTE — signature silhouette per family, and whether traversal is a family

| Field | Value |
|-------|-------|
| **Gate id** | `TG-GRAYBOX-SILHOUETTE` |
| **Status** | **RESOLVED** — Round 1, 2026-10-01, 2/2 forks |
| **Job** | **taste** (art design **and** game mechanic design) |
| **Heuristic** | Docs/28 **1** (would change art bible §8 shape language) + **6** (product design gap: the locked family list does not cover traversal/hub volumes) |
| **Owner** | human |
| **Opened by** | agent, while building the `Lib/01_Homestead` spec reader + verifier (DEC-0017 / DEC-0018 work) |
| **Precedence** | taste-profile §2 — max **2 questions per turn** |
| **Upstream** | [TASTE_GATE_ZONE_FAMILY.md](TASTE_GATE_ZONE_FAMILY.md) (RESOLVED 8/8, 2026-10-01) · [02_ART_BIBLE.md](../02_ART_BIBLE.md) §8 · [GRAYBOX_LAYOUT.md](../../Lib/00_Core/GRAYBOX_LAYOUT.md) · [34_ART_PIPELINE_RESEARCH.md](../34_ART_PIPELINE_RESEARCH.md) §6 |

---

## Why this gate exists

TG-ZONE-FAMILY settled the load-bearing rule and stated its own consequence:

> *"A mechanic family that cannot be told apart by shape from 20 m away has failed its section."*
> *"the greybox builder gains a silhouette-collision assertion — two volumes from different
> families may not share an aspect ratio at the same scale band."*

So **silhouette distinctness is now a mechanical requirement, not art polish.** To turn it into
a machine check I need two things that are *art design* and *mechanic design*, and therefore
yours. I will not invent either.

Measured state of the repo, 2026-10-01, read from
[GRAYBOX_LAYOUT.md](../../Lib/00_Core/GRAYBOX_LAYOUT.md):

| Defect | Count / detail |
|---|---|
| Volumes ≤ 0.5 m thin | 14 of 39 (path slabs, lookout pad, landing circle, beast pad, glider perch, 5 camera helpers) |
| Identical proportion, different location | `SM_Shrine_Homestead` **and** `SM_Shrine_Return` — both `1.5 × 1.5 × 2.0` |
| Resolve to aspect ratio 1.00 | `SM_Cabin` (5.5×4.5×5.5), `SM_PineValley_Block_A` (10×8×10), and 5 `CAM_` helpers |

Criteria 1–3 of the Lead's passing grade pass on paper today. **Criterion 4 fails.**

⚠️ Note the camera helpers: 5 of the "14 thin volumes" are `CAM_` framing aids, not world
geometry. If they stay in the same table as placeable volumes they inflate the defect count.
That is a bookkeeping call I have made myself (they are excluded from the silhouette
assertion) and flagged rather than hidden.

---

## Round 1 — PENDING

### Q1 — What is each family's signature silhouette at 20 m?

Art bible §8 fixes *vocabulary* (layered torn earth, stylized conical pines, rustic gabled
cabin, handmade spirit cue) but not *per-family discriminators*. The assertion needs a
number or a shape per family. I cannot write these without deciding the look.

Proposed shape for your answer — one line per family:

| Family | Signature silhouette (your words or mine to correct) |
|---|---|
| gather | low wide soft mound, reads as a spreading patch |
| nurture / tame | broad low pad with a raised rim you can see over |
| heal | narrow upright, single soft column |
| spirit stewardship | tall thin vertical **with a see-through gap** |
| stealth | low broken horizontal, never a closed mass |
| build / place | flat square plate, deliberately dull |
| combat (placeholder) | jagged asymmetric wedge, tallest in frame |

- **A (recommended)** — correct the table above. Seven lines, cheap, and it makes criterion 4 checkable today.
- **B** — aspect ratio band only. Fastest, but see the honest caveat below: it both false-positives and false-negatives.
- **C** — skip; ship criteria 1–3 mechanically and leave 4 as the manual squint test.

### Q2 — Are traversal and hub volumes a mechanic family, or the spine between families?

The locked family list is *gather / nurture-tame / heal / spirit stewardship / stealth /
build-place / combat-placeholder*. But 13 of the 39 volumes are neither — they are
**traversal** (`SM_Path_Homestead`, `SM_Path_Planet_SegA/B/C`, `SM_Glider_Perch`,
`SM_Islet_01..03`, `SM_Lookout_Pad`) or **hub** (`SM_Cabin`, `SM_Garden_Beds`,
`SM_PineCluster_Homestead_A/B/C`). TG-ZONE-FAMILY says *one family per section* and lists
these seven. Under "environment alone" the player should be able to read a zone from
20 m — so what does a **path** announce?

- **A (recommended)** — traversal is **the spine, not a family**: it carries no silhouette of its own and inherits the neighbouring family's material. Hub is its own family (`build/place` is its mechanic; the cabin is the landmark you steer by). This is the smallest change that keeps "one family per section" true.
- **B** — traversal is an **eighth family** with its own silhouette (a low horizontal leading line). Reads more clearly; costs a section's worth of vocabulary and undercuts "path leads you somewhere".
- **C** — skip; mark traversal/hub volumes `family: null` and exclude them from the assertion.

---

## Honest caveat, carried forward

There is **no published industry standard** for a greybox silhouette-distinctness check, and
no source found shows anyone running one programmatically. Shaver's method is a manual
squint test ([34_ART_PIPELINE_RESEARCH.md](../34_ART_PIPELINE_RESEARCH.md) §4, §7). Whatever
is chosen here is a **house standard, not a cited one**, and the write-up must say so.

More precisely, on the aspect-ratio proxy proposed upstream:

- **False negative** — a 1:1:1 *pyramid* and a 1:1:1 *cube* share aspect ratio and are not the same silhouette.
- **False positive** — two flat wide pads (aspect 0.05 and 0.06) are unmistakably different and would collide.
- Aspect ratio is a **crude proxy for silhouette**, not a measure of it. If you want a real check, the defensible version renders each volume's outline and compares silhouettes — still a house standard, but it measures the thing the Lead actually asked for.

If you pick **B** on Q1 I will implement the aspect-ratio band *and* report its known
false-positive/false-negative behaviour rather than presenting it as sound.

---

## Rejected on the record

| Rejected | Why |
|---|---|
| Agent assigning families + silhouettes unasked | Art design and mechanic design are human-owned after the 2026-10-01 reset (taste-profile §5). Inventing them is the exact failure the reset was made to prevent. |
| Silhouette assertion as a CI merge gate | A gate is a test bar, which is human-owned. Ships as a **report** first; Lead decides if it ever gates. |
| Keeping the aspect-ratio rule because the handoff proposed it | It is a proxy with known false positives and negatives in both directions. DEC-0022 replaces it with band + openness. A proposal is not a decision until it survives the alternative. |
| Rewriting GRAYBOX_LAYOUT.md into a new canon format | Agent-owned and tempting, but it would fork a doc that four other handoffs already cite. Parsing the existing table keeps one source of truth. Recorded as a DEC row, not a gate. |

---

## Settled decisions

| Fork | Answer | Consequence |
|---|---|---|
| **Q1 — signature silhouette** | **Correct the proposed table** (2026-10-01, Lead) | Seven families, seven shape rules, now assertable. Lines remain individually correctable without reopening the gate. |
| **Q2 — traversal / hub** | **Traversal is the spine** (2026-10-01, Lead) | Traversal carries **no** silhouette of its own, inherits the neighbouring family's material, and is **excluded** from the collision assertion. Hub volumes take family `build_place`; the cabin is that family's signature landmark. |

### The seven signature silhouettes (LOCKED — art design)

| Family | Signature silhouette at 20 m |
|---|---|
| `gather` | low wide soft mound, reads as a spreading patch |
| `nurture_tame` | broad low pad with a raised rim you can see over |
| `heal` | narrow upright, single soft column |
| `spirit` | tall thin vertical **with a see-through gap** |
| `stealth` | low broken horizontal, never a closed mass |
| `build_place` | flat square plate, deliberately dull |
| `combat` | jagged asymmetric wedge, tallest in frame |

⚠️ **Scope correction the Lead made implicitly, recorded so it is not re-litigated:**
hub is **not** an eighth family. Hub volumes (cabin, garden beds, pine clusters) carry
`family: build_place` — the cabin is that family's signature landmark, which is what makes it
the thing you steer by. The mechanic list stays at the seven locked in TG-ZONE-FAMILY.

⚠️ **Consequence nobody chose but must be recorded:** `heal`, `stealth` and `combat` have
**no volume** in the 39-volume layout. Under *"one mechanic family per section, taught in
isolation"* those three families are currently taught nowhere. Authoring sections for them is
level design and content — **not invented here.** It is reported as a coverage gap and left
for the Lead.

---

## Round log

### Round 1 — RESOLVED 2026-10-01

- **Q1** — "Correct my table" chosen over aspect-band-only and over skipping.
- **Q2** — "Traversal is the spine" chosen over eighth-family and over mark-null-exclude.
# T0 PROTOTYPE TRACK — the single track, with art enrolled

| Field | Value |
|---|---|
| **Status** | ACTIVE — this is the track. Not taste, not harness. |
| **Date** | 2026-10-02 |
| **Canonical beat list** | [`T0_MECHANIC_INVENTORIES_V1.md`](T0_MECHANIC_INVENTORIES_V1.md) — 14 MUST, `APPROVE-PROTOTYPE-LIST` at `#240` |
| **Approval** | `APPROVE-T0-MECHANIC-INV` — **see §3, the approval check is UNCHECKED** |
| **This file** | Rollup. Does not replace the inventories; does not restate them. |

## What this document is

One place to see the whole prototype at a glance: which beat is next, what is blocking it,
and what art each beat needs so the two are done in the same pass rather than serially.

**The inventories remain canonical.** Every Expected / Found / Arrange / DONE-WHEN / Depends /
Anti row lives there, and it was written before I arrived. This file does not paraphrase them
into a looser summary — a paraphrase is how the two vocabularies drifted apart the first time.

---

## 1. What is already done, and what "done" means here

**All 13 implementation commits are merged into `main`** (`#253`–`#268`, plus M3/M4 and M9).
The code exists. That is not the same as the beats being accepted.

| Ledger state | Count | Meaning |
|---|---|---|
| `LOCAL_PASS` | 3 (M1, M8, M9) | artifact self-reports pass, not provisional, no closed fail |
| `PROVISIONAL` | 5 (M10, M11, M12, M13, M14) | artifact self-flags provisional — **not a verdict** |
| `NO_VERDICT` | 6 (M2, M3, M4, M6, M7, M_default) | no pass field — outcome unknown, **NOT a pass** |
| **Accepted** | **0 of 14** | requires the Lead to run a prove and stamp it |

⚠️ **The single number that matters: `Accepted beats: 0 of 14`.** Acceptance is not derivable
from a local file, so the tool hard-codes it `false` and will never set it. This is deliberate
and it is the honest state.

**Six `NO_VERDICT` beats are the cheapest real progress available.** They are merged, not
proven. Running their prove scripts converts unknown-into-known for zero code. That is
higher value per hour than any implementation work, and it is Lead labour rather than agent
labour — so it is queued, not started.

---

## 2. The prove vocabulary is already shipped — do not invent another one

**This is the correction that matters most in this document.**

`T0_MECHANIC_INVENTORIES_V1` freezes a label set: `NODE_*` · `TOD_*` · `FORM_*` · `EJECT_HOME`
· `CAM_T0_*`, plus the verdict classes `soft_fail` and `closed_fail`.

I checked all 23 against `Source/`. **Every one is present**, most of them heavily used:

| Label | Hits | | Label | Hits |
|---|---|---|---|---|
| `FORM_BODY` | 57 | | `NODE_FIELD_GATHER` | 22 |
| `FORM_SPIRIT` | 41 | | `NODE_KETTLE` | 21 |
| `closed_fail` | 57 | | `NODE_BED` | 21 |
| `NODE_PLANT_SLOT` | 59 | | `NODE_PORTAL_HOME` | 18 |
| `EJECT_HOME` | 36 | | `NODE_SLEEPER` | 15 |
| `NODE_RUNE` | 32 | | `NODE_PORTAL_CAMP` | 14 |
| `TOD_NIGHT_SPIRIT` | 32 | | `NODE_WAKE` | 8 |
| `NODE_BACKPACK` | 33 | | `CAM_T0_BED` | 7 |
| `NODE_GUARD` | 25 | | `CAM_T0_CAMP_NIGHT` | 6 |
| `TOD_NIGHT_HOME` | 15 | | `CAM_T0_WAKE` | 3 |
| `FORM:` | 6 | | `CAM_T0_FIELD` | 6 |
| | | | `CAM_T0_CAMP_DAY` | 6 |

**Consequences, both binding:**

1. **New work asserts T0 labels.** A behaviour test added to a beat proves `NODE_*` /
   `FORM_*` / `EJECT_HOME`, not an ad-hoc name. `closed_fail` is the failure verdict, not
   `blocking` / `warn` / `info` — that is a **richer** vocabulary than what I had, because it
   separates "law broken" from "marker missing", and it was already the project's.
2. **`PRODUCT_SPRINT_01.md` is withdrawn, not merged.** It proposed eight tasks from the taste
   gates without having read the inventories, and its vocabulary was the alien one. Its two
   surviving ideas are folded in below. Nothing in it is lost; most of it was duplicate.

---

## 3. Approval status — a genuine finding

`T0_MECHANIC_INVENTORIES_V1.md` carries a Lead gate:

```text
APPROVE-T0-MECHANIC-INV
```

Its own status line reads **`DRAFT — awaiting Lead APPROVE-T0-MECHANIC-INV`** and its accept
checklist ends with **`- [ ] Stamp: APPROVE-T0-MECHANIC-INV` — unchecked.**

Yet 13 implementation PRs are merged against it, and the Conductor opened every bite in
its recommended order.

⚠️ **This is a real open item, and it is the Lead's to close.** The inventory packet was
authored as a gate, never stamped, and then built through anyway. Two honest readings:

- The gate was satisfied **informally** — the beat order, dependencies and label freeze were
  followed closely enough that no one felt the need to stamp it. The dependency rules were
  respected: M9 before M11, M8 before M10, M3 before M12.
- Or the gate was **skipped**, and 13 PRs landed without the approval its own routing table
  required ("Open bite 1 only — **blocked until** Lead APPROVE").

I cannot resolve this from the tree, and I am not going to retro-stamp it myself. **Either
stamp it, or record explicitly that it is void and the order stood anyway.** What I will not
do is keep building against a gate whose status nobody has asserted.

---

## 4. The one track, in order

Beat order and dependencies are **not mine** — they are the inventories' § Recommended bite
order, and the dependency rules are load-bearing. Reproduced, not invented:

| # | Bite | MUST | Law | Ledger | Art needed |
|---|---|---|---|---|---|
| 1 | `T0_M9_NIGHT_HOME_GATE` | #9 | Night@home w/o bed = `FORM_BODY` + day abilities off | `LOCAL_PASS` | none — a negative law |
| 2 | `T0_M7_RUNE_UNLOCK` | #7 | Rune flag gates bed→spirit | `NO_VERDICT` | `stealth` family — `NODE_RUNE` must read as a stealth site |
| 3 | `T0_M11_BED_SPIRIT_GATE` | #11 | Bed+rune → spirit; still respects #9 | `PROVISIONAL` | **`spirit` family** — `NODE_BED` + `FORM_SPIRIT` both read spirit |
| 4 | `T0_M8_DAY_CAMP_EJECT` | #8 | Cartoon `EJECT_HOME` from day camp | `LOCAL_PASS` | `combat` family — this is the camp |
| 5 | `T0_M10_PLANETSIDE_BOOT` | #10 | Night planetside w/o bed → same eject family | `PROVISIONAL` | reuses #8's `EJECT_HOME`; no new silhouette |
| 6 | `T0_M2_KETTLE_TEA` | #2 | Kettle→tea→half-day sprint | `NO_VERDICT` | `build_place` — `NODE_KETTLE` is hub furniture |
| 7 | `T0_M3_PLANT_GIVEN` | #3 | Plant given herb → `NODE_PLANT_SLOT` | `NO_VERDICT` | `build_place` — planters exist |
| 8 | `T0_M12_NURTURE_PLANTED` | #12 | Spirit nurture that slot | `PROVISIONAL` | **`heal` family** — currently has no volume anywhere |
| 9 | `T0_M4_BACKPACK_EQUIP` | #4 | Equip gates inventory | `NO_VERDICT` | none — UI/state law |
| 10 | `T0_M6_FIELD_GATHER` | #6 | Field nodes near landing | `NO_VERDICT` | `gather` family — reads `low`, signature is `flat` |
| 11 | `T0_M1_WAKE_LABEL` | #1 | Frozen wake prove | `LOCAL_PASS` | none — a label |
| 12 | `T0_M13_PORTAL_CAMP` | #13 | Home→camp spirit portal | `PROVISIONAL` | `spirit` family — reuses shrine language |
| 13 | `T0_M14_GUARD_SOOTHE` | #14 | Avoid 1 + soothe 2 | `PROVISIONAL` | `stealth` + `spirit` — two families, and the readout must tell them apart |

M5 (glider + field) is **`Y` / Present** and out of scope. 13 bites, not 14.

**Hard dependencies, from the inventories — do not reorder past these:**

- #11 requires #9 **and** #7
- #10 requires #8
- #12 requires #3
- #14 requires spirit reach (#11, prefer #13)

---

## 5. Art enrolled into the same track

`TG-ZONE-VOCABULARY` settled that **a zone type is a mechanic family, not a biome**, and
`TG-GRAYBOX-SILHOUETTE` locked seven signature silhouettes. Art bible §8 records the measured
gap: **`heal`, `stealth` and `combat` have no volume anywhere in the 39-volume layout**, and
`gather` / `nurture_tame` / `spirit` are measured non-conforming.

The art column in §4 exists because **the families are the beats.** `T0_M12` is the `heal`
family's only appearance in the prototype; if it has no volume, the beat is mechanically
present and visually absent. That is the same defect the taste gates named, arriving through
a different door.

**Rule: a beat is not done until its family reads at 20 m.** Enforced by
`Content/Python/graybox_spec_reader.py`, which already runs against the live blend and reports
`docs/qa/GRAYBOX_SPEC_REPORT.md`.

### Art work, folded in from the withdrawn sprint

| Art task | Where it lands | State |
|---|---|---|
| Clear the 7 blocking graybox findings | report reads FAIL today | not started |
| Spirit proportion — `SM_Shrine_Homestead` / `_Return` read `mid`, must read `tall` | serves bites 3, 12, 13 | authorised, not started |
| **`SM_SpiritWound_01` — crater or standing marker** | — | **BLOCKED ON LEAD** |
| `heal` family volume | serves bite 8 | needs a lead decision first |

⚠️ **`SM_SpiritWound_01` is the one open taste fork, and it is inside MUST work.** It is a
flat 3 × 3 m crater; the `spirit` signature is *tall thin vertical with a see-through gap*. A
crater cannot satisfy that without becoming a different object. Crater or standing marker is
level design. **It is queued, not answered** — see §7.

### The 7 blocking findings, in short

`SM_IslandTop` is 19.3 × 10.7 × 0.45; `SM_IslandTop.json` says 21 × 14 × 0.5 crust and
`GRAYBOX_LAYOUT.md` §1 says 21 × 14 × **4.0**. **Three documents, three answers, none matching
the blend.** Fixing it means deciding which is truth. Also: two materials in the blend
(`M_FamilySilhouette`, `M_ValleyNight`) are not among the ten masters, and three porch modules
sit outside the cabin footprint.

This is a **fork, not a bug report**, and it is agent-raised.

---

## 6. What this track refuses

| Not doing | Why |
|---|---|
| Taste work | Stated by the Lead 2026-10-02. Art bible, palette, tone, stills — parked. |
| Harness work | `Docs/36` §2: three triggers, nothing else. The harness is idle, not abandoned. |
| A new verb / inventory / mechanic | The 14 MUSTs are the approved scope. #5 is already Present. |
| Promoting art to `Content/` | `Docs/20` — drafts only, sidecar + `AI_ASSET_LOG` row on promote. |
| Inventing WP / form / portal APIs | Inventories §15-q. Cite existing hooks; no parallel subsystems. |
| Retro-stamping `APPROVE-T0-MECHANIC-INV` | §3. Not the agent's call. |
| Killing foes | AGENTS.md, and beat #14's own Anti row: *kill/convert-as-soothe = fail*. |

---

## 7. Open items, in the order I would take them

**Lead-labour, highest value per hour:**

1. **Close §3** — stamp `APPROVE-T0-MECHANIC-INV` or declare it void.
2. **Run the 6 `NO_VERDICT` prove scripts.** M2, M3, M4, M6, M7, M_default are merged and
   unproven. Zero code, converts unknown into known.
3. **Resolve `SM_SpiritWound_01`** — crater or standing marker. Blocks spirit art inside MUST work.

**Agent-labour, unblocked:**

4. **Bite 1 hardening: `T0_M9`.** `LOCAL_PASS` and the most load-bearing law in the track —
   night without a bed must stay `FORM_BODY`. It is the one beat where a silent regression
   breaks three others. Add the behaviour test asserting `FORM:` in the log and `closed_fail`
   on phase-only spirit.
5. **Bite 2: `T0_M7` rune.** `NO_VERDICT` and gates bite 3. Cheapest real implementation gap.
6. **Art: spirit proportion** for bites 3, 12, 13, measured against the live blend.
7. **Art: clear the 7 graybox findings** — after the island-top fork is decided.

**Sequenced:** see [`T0_ROADMAP.md`](T0_ROADMAP.md) for the full gate order.

**Not started, listed so nothing is invisible:**

8. `heal` family volume — needs a decision before bite 8 can be visually done
9. `gather` family conformance — reads `low`, signature is `flat`
10. `combat` family volume — the camp, serves bites 4, 5, 12, 13. **GATE 1 in the roadmap.**

---

## 7a. Measured: the camp does not exist

2026-10-02, live blend via Blender MCP:

```
camp_named_objects: []          # no Guard, Sleeper, Camp or Soothe mesh anywhere
VS_MVP_collection_objects: 6
```

Only five meshes sit near the camp origin `(12, -90, -95)`: a beast, the beast pad, two hurt
spirits, and one gathering bush. `GP_RS_HumanoidCamp` and `GP_PortalCamp` exist as **code
markers only**.

⚠️ **M14 is the climax beat — avoid 1 guard, soothe 2 sleepers — and the camp it happens in
has no geometry.** The 414-line stealth component will fire on an empty plain. This is the
single highest-leverage art task in the track: one location, four beats blocked.

---

## 8. Vocabularies, one table

The drift that made the withdrawn sprint necessary, made explicit:

| Concern | Canonical vocabulary | Source |
|---|---|---|
| Beat / gate labels | `NODE_*` `TOD_*` `FORM_*` `EJECT_HOME` `CAM_T0_*` | `PROTOTYPE_FEATURE_LIST_V1` |
| Verdict | `soft_fail` · `closed_fail` | inventories § Prove / taste |
| Acceptance | Lead stamp; tool never sets it | `T0_BEAT_EVIDENCE.md` |
| Beat state | `LOCAL_PASS` `PROVISIONAL` `NO_VERDICT` `LOCAL_FAIL` `UNREADABLE` | `t0-evidence.js` |
| Zone type | one of **7 mechanic families** | `TG-ZONE-VOCABULARY` Q2 |
| Family silhouette | 7 locked signatures, 20 m read | `TG-GRAYBOX-SILHOUETTE` Q1 |
| Traversal | the spine — no silhouette, excluded | `TG-GRAYBOX-SILHOUETTE` Q2 |
| Art gate | ten masters, generated textures inadmissible | art bible §10, DEC-0018 |

**Withdrawn:** `Docs/TaskLists/PRODUCT_SPRINT_01.md`. Its P1 (conversion behaviour test) shipped
as `6788aab` and stays; the rest is absorbed above.

---

*One track. 13 bites, canonical order, deps unbroken. Art enrolled because the families ARE
the beats. Taste parked. Harness idle.*

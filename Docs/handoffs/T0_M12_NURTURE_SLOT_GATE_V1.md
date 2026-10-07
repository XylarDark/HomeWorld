# T0_M12_NURTURE_SLOT_GATE_V1 — MUST #12 Design packet (Arrange + DONE-WHEN freeze)

| Field | Value |
|-------|-------|
| **Status** | **APPROVED (Lead stamp 2026-10-07, design updated for spirit-flight dispersal loop)** - Design frozen for Test files-only scoring; same-slot identity wire to #3 is the tracked impl gap |
| **Bite id** | `T0_M12_NURTURE_SLOT_GATE_V1` |
| **MUST** | #12 — Nurture planted herb (spirit) |
| **Present?** | **Partial** (Design SoT = ACCEPTED gap walk `T0_GAP_INVENTORY_WALK_V1` row #12) |
| **CAP** | **CAP PARKED** |
| **Host** | **CLOUD** docs-only (Contents API) |
| **Map** | `Maps/VS_MVP` |
| **DET** | HOLD `0a27306` |
| **Packet class** | Mechanic inventory freeze — Arrange + DONE-WHEN + prove labels for **Test files-only** / future **Implement Act**. **Not** a Source Act. |
| **Cite** | HomeWorld Co ops · [Architecture Trade-Offs A–E](sand-workflow:architecture-trade-offs-design-depth) (15-q) · `PROTOTYPE_FEATURE_LIST_V1` · `T0_GAP_INVENTORY_WALK_V1` #12 · `T0_M3_PLANT_SLOT_GATE_V1` (same `NODE_PLANT_SLOT` identity) · `PROP_INVENTORY_V1` (`FEEL-NURTURE` = same slot as `FEEL-PLANT`) |

---

## One unknown (closed by this packet)

What Arrange + DONE-WHEN + prove labels freeze MUST #12 **spirit nurture** on the **same** `NODE_PLANT_SLOT` as day plant (#3) when Present?=**Partial**, so Test scores files-only and Implement Act can open later — without Source/Content in this bite?

---

## Architecture Trade-Offs A–E (cite only — 15-q)

| Layer | Decision (inventory, **not** API invent) |
|-------|------------------------------------------|
| **A — Contract** | Prove labels `NODE_PLANT_SLOT` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT`. **One** slot identity with #3 — nurture target == day plant slot; no second node. |
| **B — Module** | Nurture = **Layer B** deep module (+ **A**). Prefer existing `HomeWorldNurtureTarget` / `HomeWorldNurtureComponent` / `TryNurtureInFront` — **no** parallel nurture service. |
| **C — Evidence** | Law = spirit nurture greps on named labels. CAP **PARKED**. No DESKTOP PASS/FAIL from Design. |
| **D — Seats** | Design freezes here; Test files-only. Implement Act = **later** (Conductor opens). Day plant Design = `T0_M3` (on main). |
| **E — Stability** | Nurturing a **different** slot / body-form nurture / day-only path as #12 = **`closed_fail`**. Unlinked N1 without #3 same-slot law = incomplete T0 link (Partial honesty). Bounded fail — no invent-retry. |

**15-q:** Do **not** invent nurture/WP APIs. Prefer cite existing nurture hooks. **No new schema.**

---

## Inventory freeze (labels ⊆ feature-list ∩ gap)

| Label | Role |
|-------|------|
| `NODE_PLANT_SLOT` | Same slot as MUST #3 day plant — spirit nurture target |
| `TOD_NIGHT_SPIRIT` | Nurture prove on night spirit path |
| `FORM_SPIRIT` | Spirit form while nurturing |

Labels ⊆ `PROTOTYPE_FEATURE_LIST_V1` ∩ gap #12. PROP: same-row `NODE_PLANT_SLOT` · `FEEL-NURTURE` identity with `FEEL-PLANT` (cite `T0_M3`).

---

## Expected · Found · Arrange · DONE-WHEN · Depends · Anti

| Field | Value |
|-------|-------|
| **Expected (T0)** | Spirit · night · nurture the **planted** herb on the **same** `NODE_PLANT_SLOT` marked by day plant (#3). The night's larger loop (Lead 2026-10-07): herbs collected + a cloud wisp are given to the spirit wisps → spirit flight buff at night → the player uses night flight to disperse dung + wisp over the herb sites in the field. #12 nurture remains the same-slot, spirit-form, night-only verb that carries that loop. |
| **Found (gap SoT = Partial)** | Umap: `GP_N1_Crop`, `GP_N2_Stored` · `HomeWorldNurtureTarget` / `HomeWorldNurtureComponent` · Interact `TryNurtureInFront`. Spirit nurture on N1 **present**. Link to day plant-given-herb (#3) still open (same-slot identity not Design-frozen until this + M3). Present?=**Partial**. |
| **Arrange** | Spirit · `FORM_SPIRIT` · `TOD_NIGHT_SPIRIT` · `NODE_PLANT_SLOT` = same slot as #3 plant · nurture interact · CAP **PARKED** |
| **DONE-WHEN** | § below — Test files-only; **no DESKTOP Act** from Design |
| **Depends / HOLD** | Same-slot cite `T0_M3_PLANT_SLOT_GATE_V1` (on main). Other T0 MUST **DEFER**. |
| **Anti** | Different slot ≠ pass · body nurture ≠ #12 · day plant alone ≠ spirit nurture · no Content/Python/Source · no DESKTOP PASS/FAIL from Design · Design does not self-APPROVE |

---

## Arrange (normative)

1. Map: `Maps/VS_MVP` → night spirit path (`TOD_NIGHT_SPIRIT` / `FORM_SPIRIT`) — not day body plant.
2. Target = **`NODE_PLANT_SLOT`** with **same identity** as MUST #3 day plant (cite `T0_M3_PLANT_SLOT_GATE_V1` / PROP FEEL-NURTURE note) — not a second prop/node.
3. **Nurture interact:** spirit nurture on that slot (prefer `TryNurtureInFront` / `HomeWorldNurtureTarget` path — **not** invent).
4. **Negatives = `closed_fail`:** nurture on a **different** world slot · body-form nurture scored as #12 · treating day plant alone as spirit nurture prove.
5. Prove class: mechanic inventory — **not** mood/taste. CAP **PARKED**.

---

## DONE-WHEN (Test files-only)

### Law

- Spirit nurture proves on the **same** `NODE_PLANT_SLOT` as day plant (#3)
- Prove labels: `NODE_PLANT_SLOT` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT`
- Present?=**Partial** (gap SoT) — N1 spirit nurture present; #3 same-slot link open until Design packets land / Implement wires identity
- Different-slot / body nurture as #12 = **`closed_fail`**

### Grep strings

`NODE_PLANT_SLOT` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` · `Arrange` · `DONE-WHEN` · `CAP PARKED` / `PARKED` · `Present?=Partial` · `closed_fail`

### Negative / Anti

- Do **not** score a different slot as #12
- Do **not** score body / day plant alone as spirit nurture
- No Content / Python / Source / `.uasset` / `.umap` · no DESKTOP PASS/FAIL from Design · Design does **not** self-APPROVE · other T0 MUST **DEFER**

### Future Implement note (cite only)

Gap Partial → Implement Act for same-slot identity wire (#3 plant mark ↔ #12 nurture target) opens **only** after Conductor routes. This packet does **not** open Source Act.

---

## Ball

**Test files-only** after draft PR. Do not merge from Design. Conductor routes next.

---

*Repo path: `Docs/handoffs/T0_M12_NURTURE_SLOT_GATE_V1.md` · Bite: `T0_M12_NURTURE_SLOT_GATE_V1` only · Present?=Partial · exclusive path · same slot as `T0_M3`.*

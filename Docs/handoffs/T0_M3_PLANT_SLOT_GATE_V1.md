# T0_M3_PLANT_SLOT_GATE_V1 — MUST #3 Design packet (Arrange + DONE-WHEN freeze)

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — Design files-only; Design does **not** self-APPROVE |
| **Bite id** | `T0_M3_PLANT_SLOT_GATE_V1` |
| **MUST** | #3 — Plant given herb nearby outside |
| **Present?** | **Partial** (Design SoT = ACCEPTED gap walk `T0_GAP_INVENTORY_WALK_V1` row #3) |
| **CAP** | **CAP PARKED** |
| **Host** | **CLOUD** docs-only (Contents API) |
| **Map** | `Maps/VS_MVP` |
| **DET** | HOLD `0a27306` |
| **Packet class** | Mechanic inventory freeze — Arrange + DONE-WHEN + prove labels for **Test files-only** / future **Implement Act**. **Not** a Source Act. |
| **Cite** | HomeWorld Co ops · [Architecture Trade-Offs A–E](sand-workflow:architecture-trade-offs-design-depth) (15-q) · `PROTOTYPE_FEATURE_LIST_V1` · `T0_GAP_INVENTORY_WALK_V1` #3 · `PROP_INVENTORY_V1` (`NODE_PLANT_SLOT` · `ENV_T0_HOME` · `FEEL-PLANT` / same-slot `FEEL-NURTURE`) |

---

## One unknown (closed by this packet)

What Arrange + DONE-WHEN + prove labels freeze MUST #3 day **plant given herb** on `NODE_PLANT_SLOT` when Present?=**Partial**, so Test scores files-only and Implement Act can open later — without Source/Content in this bite?

---

## Architecture Trade-Offs A–E (cite only — 15-q)

| Layer | Decision (inventory, **not** API invent) |
|-------|------------------------------------------|
| **A — Contract** | Prove labels `NODE_PLANT_SLOT` · `TOD_DAY` · `FORM_BODY`. Day plant marks the **same slot identity** later spirit nurture (#12) uses — one `NODE_PLANT_SLOT`, not a second node. |
| **B — Module** | Plant/nurture slot = **Layer B** deep module (+ **A**). Prefer existing `HomeWorldNurtureTarget` / planter / inventory-herb path — **no** parallel plant service. |
| **C — Evidence** | Law = day plant interact greps on named labels. CAP **PARKED**. No DESKTOP PASS/FAIL from Design. |
| **D — Seats** | Design freezes here; Test files-only. Implement Act = **later** (Conductor opens). #12 nurture Design not this bite. |
| **E — Stability** | Treating nurture-only `GP_N1_Crop` / PROXY mesh as day plant-given-herb = **`closed_fail`**. Planter dress ≠ plant interact. Bounded fail — no invent-retry. |

**15-q:** Do **not** invent plant/WP APIs. Prefer cite nurture/planter/inventory hooks already on VS_MVP. **No new schema.**

---

## Inventory freeze (labels ⊆ feature-list ∩ gap)

| Label | Role |
|-------|------|
| `NODE_PLANT_SLOT` | Day outside plant-given-herb interact (same slot identity as later #12 spirit nurture) |
| `TOD_DAY` | Plant prove runs on Day |
| `FORM_BODY` | Body form while planting |

Labels ⊆ `PROTOTYPE_FEATURE_LIST_V1` ∩ gap #3 suggested prove labels. PROP: `NODE_PLANT_SLOT` · envelope `ENV_T0_HOME` · feel `FEEL-PLANT` (nurture identity noted; #12 not Acted here).

---

## Expected · Found · Arrange · DONE-WHEN · Depends · Anti

| Field | Value |
|-------|-------|
| **Expected (T0)** | Day · outside near homestead · plant a **given herb** into `NODE_PLANT_SLOT` so the **same slot** can be spirit-nurtured later (#12). Body (`FORM_BODY`). |
| **Found (gap SoT = Partial)** | Disk: `SM_Planter_A/B/C`. Umap: `GP_N1_Crop` (`HomeWorldNurtureTarget`). PROXY `NODE_PLANT_SLOT` / `SM_ProxyPlantSlot`. **No** day “plant given herb” interact marking T0 `NODE_PLANT_SLOT`. N1 nurture ≠ plant-given-herb beat. Present?=**Partial**. |
| **Arrange** | Day · `FORM_BODY` · outside near planters · given herb in hand/inv · `NODE_PLANT_SLOT` plant interact · slot marked for later nurture · CAP **PARKED** |
| **DONE-WHEN** | § below — Test files-only greps; **no DESKTOP Act** from Design |
| **Depends / HOLD** | Other T0 MUST **DEFER**. #12 spirit nurture = separate bite (same label identity; not Acted here). |
| **Anti** | Nurture-only ≠ day plant · PROXY ≠ world plant interact · no CAP reopen · no Content/Python/Source · no DESKTOP PASS/FAIL from Design · Design does not self-APPROVE |

---

## Arrange (normative)

1. Map: `Maps/VS_MVP` → Day · body (`FORM_BODY`) · homestead outside (planters / stoop — not field gather).
2. Player has a **given herb** (inventory / hand — cite existing RES_HERB / inventory path; no new craft schema).
3. **`NODE_PLANT_SLOT` interact:** day plant into the T0 plant slot (world interact — **not** PROXY mesh alone; **not** spirit `TryNurtureInFront` alone).
4. Slot identity persists for later #12 spirit nurture (same `NODE_PLANT_SLOT` — cite PROP FEEL-NURTURE note; #12 not this bite).
5. **Negatives = `closed_fail`:** counting `GP_N1_Crop` nurture-only or planter dress as day plant-given-herb · treating PROXY `SM_ProxyPlantSlot` as world plant interact.
6. Prove class: mechanic inventory — **not** mood/taste. CAP **PARKED**.

---

## DONE-WHEN (Test files-only)

### Law

- Day plant-given-herb is the **named gate** that marks `NODE_PLANT_SLOT` for later spirit nurture
- Prove labels: `NODE_PLANT_SLOT` · `TOD_DAY` · `FORM_BODY`
- Present?=**Partial** (gap SoT) — planters + N1 exist; **no** day plant-given-herb interact; N1 ≠ plant beat; PROXY ≠ world plant
- Nurture-only / PROXY-as-plant = **`closed_fail`**

### Grep strings

`NODE_PLANT_SLOT` · `TOD_DAY` · `FORM_BODY` · `Arrange` · `DONE-WHEN` · `CAP PARKED` / `PARKED` · `Present?=Partial` · `closed_fail`

### Negative / Anti

- Do **not** treat `GP_N1_Crop` nurture-only as day plant-given-herb
- Do **not** treat PROXY `SM_ProxyPlantSlot` as world plant interact
- No Content / Python / Source / `.uasset` / `.umap` · no DESKTOP PASS/FAIL from Design · Design does **not** self-APPROVE · other T0 MUST **DEFER**

### Future Implement note (cite only)

Gap Partial → Implement Act for day plant-given-herb on `NODE_PLANT_SLOT` (wire given-herb → slot mark; keep same-slot identity for #12) opens **only** after Conductor routes. This packet does **not** open Source Act.

---

## Ball

**Test files-only** after draft PR. Do not merge from Design. Conductor routes next.

---

*Repo path: `Docs/handoffs/T0_M3_PLANT_SLOT_GATE_V1.md` · Bite: `T0_M3_PLANT_SLOT_GATE_V1` only · Present?=Partial · CAP PARKED · exclusive path.*

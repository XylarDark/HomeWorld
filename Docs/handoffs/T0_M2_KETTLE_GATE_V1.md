# T0_M2_KETTLE_GATE_V1 — MUST #2 Design packet (Arrange + DONE-WHEN freeze)

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — Design files-only; Design does **not** self-APPROVE |
| **Bite id** | `T0_M2_KETTLE_GATE_V1` |
| **MUST** | #2 — Kettle + herbs → tea → sprint (~half day) |
| **Present?** | **Partial** (Design SoT = ACCEPTED gap walk `T0_GAP_INVENTORY_WALK_V1` row #2 — **PROXY only**) |
| **CAP** | **CAP PARKED** |
| **Host** | **CLOUD** docs-only (Contents API) |
| **Map** | `Maps/VS_MVP` |
| **DET** | HOLD `0a27306` |
| **Packet class** | Mechanic inventory freeze — Arrange + DONE-WHEN + prove labels for **Test files-only** / future **Implement Act**. **Not** a Source Act. |
| **Cite** | HomeWorld Co ops · [Architecture Trade-Offs A–E](sand-workflow:architecture-trade-offs-design-depth) (15-q) · `PROTOTYPE_FEATURE_LIST_V1` · `T0_GAP_INVENTORY_WALK_V1` #2 · `PROP_INVENTORY_V1` (`NODE_KETTLE` · `ENV_T0_HOME` · `FEEL-TEA`) |

---

## One unknown (closed by this packet)

What Arrange + DONE-WHEN + prove labels freeze MUST #2 **kettle → tea → tea-gated sprint** on `NODE_KETTLE` when Present?=**Partial** (PROXY only), so Test scores files-only and Implement Act can open later — without Source/Content in this bite?

---

## Architecture Trade-Offs A–E (cite only — 15-q)

| Layer | Decision (inventory, **not** API invent) |
|-------|------------------------------------------|
| **A — Contract** | Prove labels `NODE_KETTLE` · `TOD_DAY` · `FORM_BODY`. Chain = kettle interact + herbs → tea → **tea-gated** sprint (~half day) — not ungated sprint alone. |
| **B — Module** | Kettle/tea gate = **Layer B** deep module (+ **A**). Prefer existing inventory / traversal day-verb path when Act opens — **no** parallel tea service; meal BPs ≠ tea. |
| **C — Evidence** | Law = kettle→tea→gated-sprint greps on named labels. CAP **PARKED**. No DESKTOP PASS/FAIL from Design. |
| **D — Seats** | Design freezes here; Test files-only. Implement Act = **later** (Conductor opens). |
| **E — Stability** | PROXY-as-kettle · ungated sprint · meal-BP-as-tea scored as #2 = **`closed_fail`**. Bounded fail — no invent-retry. |

**15-q:** Do **not** invent kettle/tea/WP APIs. Prefer cite existing inventory / traversal hooks when Act opens. **No new schema.**

---

## Inventory freeze (labels ⊆ feature-list ∩ gap)

| Label | Role |
|-------|------|
| `NODE_KETTLE` | Homestead kettle interact (world beat — not PROXY alone) |
| `TOD_DAY` | Kettle/tea/sprint prove on Day |
| `FORM_BODY` | Body form for kettle → tea → sprint |

Labels ⊆ `PROTOTYPE_FEATURE_LIST_V1` ∩ gap #2. PROP: `NODE_KETTLE` · envelope `ENV_T0_HOME` · feel `FEEL-TEA`.

---

## Expected · Found · Arrange · DONE-WHEN · Depends · Anti

| Field | Value |
|-------|-------|
| **Expected (T0)** | Day · body · kettle + herbs → tea → **tea-gated** sprint lasting ~half day. |
| **Found (gap SoT = Partial / PROXY only)** | PROXY only: `NODE_KETTLE` / `SM_ProxyKettle` in `PROP_INVENTORY_V1`. **0** kettle/tea path on DESKTOP umap/Source/Python. Sprint = ungated MV (`HomeWorldTraversalComponent` / day-verb gate). Meal BPs ≠ tea. Present?=**Partial**. |
| **Arrange** | Day · `FORM_BODY` · homestead · herbs available · `NODE_KETTLE` interact → tea → tea-gated sprint (~half day) · CAP **PARKED** |
| **DONE-WHEN** | § below — Test files-only; **no DESKTOP Act** from Design |
| **Depends / HOLD** | Other T0 MUST **DEFER**. |
| **Anti** | PROXY ≠ world kettle · ungated sprint ≠ tea gate · meal BP ≠ tea · no Content/Python/Source · no DESKTOP PASS/FAIL from Design · Design does not self-APPROVE |

---

## Arrange (normative)

1. Map: `Maps/VS_MVP` → Day · body (`FORM_BODY`) · homestead.
2. Herbs available (inventory / world — cite existing RES_HERB path; no new craft schema this packet).
3. **`NODE_KETTLE` interact:** kettle → tea (world interact — **not** PROXY `SM_ProxyKettle` alone).
4. Tea grants **gated** sprint (~half day duration) — ungated day sprint alone does **not** satisfy #2.
5. **Negatives = `closed_fail`:** PROXY-as-kettle · meal-BP-as-tea · ungated sprint as tea gate.
6. Prove class: mechanic inventory — **not** mood/taste. CAP **PARKED**.

---

## DONE-WHEN (Test files-only)

### Law

- Kettle + herbs → tea → **tea-gated** sprint (~half day) is the **named chain** on `NODE_KETTLE`
- Prove labels: `NODE_KETTLE` · `TOD_DAY` · `FORM_BODY`
- Present?=**Partial** (gap SoT) — PROXY envelope only; **0** kettle/tea path on umap/Source/Python; sprint ungated; meal BPs ≠ tea
- PROXY / ungated sprint / meal-as-tea = **`closed_fail`**

### Grep strings

`NODE_KETTLE` · `TOD_DAY` · `FORM_BODY` · `Arrange` · `DONE-WHEN` · `CAP PARKED` / `PARKED` · `Present?=Partial` · `closed_fail`

### Negative / Anti

- Do **not** treat PROXY `SM_ProxyKettle` as world kettle interact
- Do **not** treat ungated sprint as tea-gated sprint
- Do **not** treat meal BPs as tea
- No Content / Python / Source / `.uasset` / `.umap` · no DESKTOP PASS/FAIL from Design · Design does **not** self-APPROVE · other T0 MUST **DEFER**

### Future Implement note (cite only)

Gap Partial → Implement Act for kettle interact + herb→tea + tea-gated sprint duration opens **only** after Conductor routes. This packet does **not** open Source Act.

---

## Ball

**Test files-only** after draft PR. Do not merge from Design. Conductor routes next.

---

*Repo path: `Docs/handoffs/T0_M2_KETTLE_GATE_V1.md` · Bite: `T0_M2_KETTLE_GATE_V1` only · Present?=Partial (PROXY only) · exclusive path.*

# T0_M6_FIELD_GATHER_GATE_V1 — MUST #6 Design packet (Arrange + DONE-WHEN freeze)

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — Design files-only; Design does **not** self-APPROVE |
| **Bite id** | `T0_M6_FIELD_GATHER_GATE_V1` |
| **MUST** | #6 — Collect herb seeds in field |
| **Present?** | **Partial** (Design SoT = ACCEPTED gap walk `T0_GAP_INVENTORY_WALK_V1` row #6) |
| **CAP** | **CAP PARKED** |
| **Host** | **CLOUD** docs-only (Contents API) |
| **Map** | `Maps/VS_MVP` |
| **DET** | HOLD `0a27306` |
| **Packet class** | Mechanic inventory freeze — Arrange + DONE-WHEN + prove labels for **Test files-only** / future **Implement Act**. **Not** a Source Act. |
| **Cite** | HomeWorld Co ops · [Architecture Trade-Offs A–E](sand-workflow:architecture-trade-offs-design-depth) (15-q) · `PROTOTYPE_FEATURE_LIST_V1` · `T0_GAP_INVENTORY_WALK_V1` #6 · `PROP_INVENTORY_V1` (`NODE_FIELD_GATHER` · `ENV_T0_FIELD` · `FEEL-ENV-GREYBOX`) |

---

## One unknown (closed by this packet)

What Arrange + DONE-WHEN + prove labels freeze MUST #6 **field herb/seed collect** on `NODE_FIELD_GATHER` when Present?=**Partial**, so Test scores files-only and Implement Act can open later — without Source/Content in this bite?

---

## Architecture Trade-Offs A–E (cite only — 15-q)

| Layer | Decision (inventory, **not** API invent) |
|-------|------------------------------------------|
| **A — Contract** | Prove labels `NODE_FIELD_GATHER` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_FIELD`. Field gather is the **named beat** near landing after glide — not homestead plant (#3) or store markers alone. |
| **B — Module** | Gather = **Layer B** deep module (+ **A**). Prefer existing RES_HERB / RES_SEED / gather dress / inventory path — **no** parallel gather service. |
| **C — Evidence** | Law = field collect greps on named labels + cam. CAP **PARKED**. No DESKTOP PASS/FAIL from Design. |
| **D — Seats** | Design freezes here; Test files-only. Implement Act = **later** (Conductor opens). |
| **E — Stability** | Dress-only / store-only / PROXY-as-beat / homestead plant scored as field gather = **`closed_fail`**. Bounded fail — no invent-retry. |

**15-q:** Do **not** invent gather/WP APIs. Prefer cite existing RES / dress / inventory hooks. **No new schema.**

---

## Inventory freeze (labels ⊆ feature-list ∩ gap)

| Label | Role |
|-------|------|
| `NODE_FIELD_GATHER` | Day field herb/seed collect beat (near landing / field envelope) |
| `TOD_DAY` | Gather prove runs on Day |
| `FORM_BODY` | Body form while gathering |
| `CAM_T0_FIELD` | Field gather cam beat |

Labels ⊆ `PROTOTYPE_FEATURE_LIST_V1` ∩ gap #6. PROP: `NODE_FIELD_GATHER` · envelope `ENV_T0_FIELD`.

---

## Expected · Found · Arrange · DONE-WHEN · Depends · Anti

| Field | Value |
|-------|-------|
| **Expected (T0)** | Day · body · after field arrive · collect herb **seeds** (herb/seed) at frozen `NODE_FIELD_GATHER` · cam `CAM_T0_FIELD`. |
| **Found (gap SoT = Partial)** | Umap: `DRESS_SM_Gather_FirstHarvest_Bush_*`, `GP_Store_HERB`/`SEED`, `RES_HERB`/`RES_SEED` · meshes `SM_RES_HERB_World_Mesh`, `SM_RES_SEED_World_Mesh` · gather scripts · PROXY `NODE_FIELD_GATHER`. Field gather dress + RES systems exist; **no** frozen `NODE_FIELD_GATHER` field node near landing as T0 beat label. Present?=**Partial**. |
| **Arrange** | Day · `FORM_BODY` · field near landing · `NODE_FIELD_GATHER` collect interact · cam `CAM_T0_FIELD` · CAP **PARKED** |
| **DONE-WHEN** | § below — Test files-only; **no DESKTOP Act** from Design |
| **Depends / HOLD** | Other T0 MUST **DEFER**. Glide (#5) Present?=Y — arrive path cite only, not re-Acted here. |
| **Anti** | Dress-only ≠ beat · store markers ≠ `NODE_FIELD_GATHER` · PROXY ≠ world beat · homestead plant (#3) ≠ field gather · no Content/Python/Source · no DESKTOP PASS/FAIL from Design · Design does not self-APPROVE |

---

## Arrange (normative)

1. Map: `Maps/VS_MVP` → Day · body (`FORM_BODY`) · **field** near landing (after glide arrive — cite #5 Present?=Y; not homestead plant slot).
2. **`NODE_FIELD_GATHER` interact:** collect herb seeds / herb+seed at the frozen field gather node (world beat — **not** PROXY mesh alone; **not** dress bushes alone; **not** `GP_Store_*` alone).
3. Cam `CAM_T0_FIELD` for the gather beat.
4. **Negatives = `closed_fail`:** dress-only / store-only / PROXY-as-beat / scoring `NODE_PLANT_SLOT` plant as field gather.
5. Prove class: mechanic inventory — **not** mood/taste. CAP **PARKED**.

---

## DONE-WHEN (Test files-only)

### Law

- Day field herb/seed collect is the **named beat** on `NODE_FIELD_GATHER` · cam `CAM_T0_FIELD`
- Prove labels: `NODE_FIELD_GATHER` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_FIELD`
- Present?=**Partial** (gap SoT) — dress + RES present; **no** frozen `NODE_FIELD_GATHER` near landing as T0 beat label; PROXY ≠ world beat
- Dress-only / store-only / PROXY / plant-slot-as-field = **`closed_fail`**

### Grep strings

`NODE_FIELD_GATHER` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_FIELD` · `Arrange` · `DONE-WHEN` · `CAP PARKED` / `PARKED` · `Present?=Partial` · `closed_fail`

### Negative / Anti

- Do **not** treat gather dress or `GP_Store_*` alone as `NODE_FIELD_GATHER` beat
- Do **not** treat PROXY `SM_ProxyFieldGather` as world beat
- Do **not** score homestead `NODE_PLANT_SLOT` as field gather
- No Content / Python / Source / `.uasset` / `.umap` · no DESKTOP PASS/FAIL from Design · Design does **not** self-APPROVE · other T0 MUST **DEFER**

### Future Implement note (cite only)

Gap Partial → Implement Act for frozen `NODE_FIELD_GATHER` field node + collect wire near landing opens **only** after Conductor routes. This packet does **not** open Source Act.

---

## Ball

**Test files-only** after draft PR. Do not merge from Design. Conductor routes next.

---

*Repo path: `Docs/handoffs/T0_M6_FIELD_GATHER_GATE_V1.md` · Bite: `T0_M6_FIELD_GATHER_GATE_V1` only · Present?=Partial · exclusive path.*

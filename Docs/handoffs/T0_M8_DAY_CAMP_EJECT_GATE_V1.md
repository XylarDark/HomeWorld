# T0_M8_DAY_CAMP_EJECT_GATE_V1 — MUST #8 Design packet (Arrange + DONE-WHEN freeze)

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — Design files-only; Design does **not** self-APPROVE |
| **Bite id** | `T0_M8_DAY_CAMP_EJECT_GATE_V1` |
| **MUST** | #8 — Day camp: cartoon eject (launch→glider→home) |
| **Present?** | **N** (Design SoT = ACCEPTED gap walk `T0_GAP_INVENTORY_WALK_V1` row #8) |
| **CAP** | **CAP PARKED** |
| **Host** | **CLOUD** docs-only (Contents API) |
| **Map** | `Maps/VS_MVP` |
| **DET** | HOLD `0a27306` |
| **Packet class** | Mechanic inventory freeze — Arrange + DONE-WHEN + prove labels for **Test files-only** / future **Implement Act**. **Not** a Source Act. |
| **Cite** | HomeWorld Co ops · [Architecture Trade-Offs A–E](sand-workflow:architecture-trade-offs-design-depth) (15-q) · `PROTOTYPE_FEATURE_LIST_V1` · `T0_GAP_INVENTORY_WALK_V1` #8 · `PROP_INVENTORY_V1` (`NODE_DAY_CAMP` · `ENV_T0_CAMP` · `EJECT_HOME` / `FEEL-EJECT`) |

---

## One unknown (closed by this packet)

What Arrange + DONE-WHEN + prove labels freeze MUST #8 **day camp cartoon eject** (`NODE_DAY_CAMP` → `EJECT_HOME`) when Present?=**N**, so Test scores files-only and Implement Act can open later — without Source/Content in this bite?

---

## Architecture Trade-Offs A–E (cite only — 15-q)

| Layer | Decision (inventory, **not** API invent) |
|-------|------------------------------------------|
| **A — Contract** | Prove labels `NODE_DAY_CAMP` · `EJECT_HOME` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_CAMP_DAY`. Chain = day camp landmark → cartoon launch→glider→home eject — not island→planet FALLBACK glide alone. |
| **B — Module** | Day camp + eject = **Layer B** deep module (+ **A**). Prefer existing glide/transit hooks when Act opens — **no** parallel eject service; convert stub ≠ eject. |
| **C — Evidence** | Law = day-camp eject greps on named labels + cam. CAP **PARKED**. No DESKTOP PASS/FAIL from Design. |
| **D — Seats** | Design freezes here; Test files-only. Implement Act = **later** (Conductor opens). |
| **E — Stability** | Script-only / PROXY / FALLBACK-down-glide / convert-stub scored as #8 = **`closed_fail`**. Bounded fail — no invent-retry. |

**15-q:** Do **not** invent camp/eject/WP APIs. Prefer cite existing glide/transit when Act opens. **No new schema.**

---

## Inventory freeze (labels ⊆ feature-list ∩ gap)

| Label | Role |
|-------|------|
| `NODE_DAY_CAMP` | Day camp landmark on VS_MVP |
| `EJECT_HOME` | Cartoon eject launch→glider→home |
| `TOD_DAY` | Eject prove on Day |
| `FORM_BODY` | Body form at day camp |
| `CAM_T0_CAMP_DAY` | Day camp / eject cam beat |

Labels ⊆ `PROTOTYPE_FEATURE_LIST_V1` ∩ gap #8. PROP: `NODE_DAY_CAMP` · envelope `ENV_T0_CAMP` · `EJECT_HOME` in look_at / stack_verify.

---

## Expected · Found · Arrange · DONE-WHEN · Depends · Anti

| Field | Value |
|-------|-------|
| **Expected (T0)** | Day · body · approach day camp → cartoon eject (launch→glider→home) · cam `CAM_T0_CAMP_DAY`. |
| **Found (gap SoT = N)** | Scripts only: `GP_RS_HumanoidCamp` / `_Collect` / `_Dream` in `place_vs_mvp_rs_humanoid_camp.py` — **not** in DESKTOP umap scrape. PROXY `NODE_DAY_CAMP`. **0** eject / `EJECT_HOME` impl. Camp landmark absent from KEEP-LOCAL umap; no cartoon eject path. Convert stub ≠ eject-to-home. Present?=**N**. |
| **Arrange** | Day · `FORM_BODY` · `NODE_DAY_CAMP` present · cartoon `EJECT_HOME` (launch→glider→home) · cam `CAM_T0_CAMP_DAY` · CAP **PARKED** |
| **DONE-WHEN** | § below — Test files-only; **no DESKTOP Act** from Design |
| **Depends / HOLD** | Other T0 MUST **DEFER**. Island→planet FALLBACK (#5) ≠ this eject. |
| **Anti** | Script-only ≠ present · PROXY ≠ world camp · FALLBACK down-glide ≠ `EJECT_HOME` · convert stub ≠ eject · no Content/Python/Source · no DESKTOP PASS/FAIL from Design · Design does not self-APPROVE |

---

## Arrange (normative)

1. Map: `Maps/VS_MVP` → Day · body (`FORM_BODY`) · day camp envelope (`ENV_T0_CAMP`).
2. **`NODE_DAY_CAMP` present:** camp landmark on VS_MVP (world — **not** script-only; **not** PROXY alone).
3. **`EJECT_HOME`:** cartoon eject launch→glider→**home** (not island→planet FALLBACK down-glide).
4. Cam `CAM_T0_CAMP_DAY`.
5. **Negatives = `closed_fail`:** script-only camp · PROXY-as-camp · FALLBACK glide as eject · convert stub as eject.
6. Prove class: mechanic inventory — **not** mood/taste. CAP **PARKED**.

---

## DONE-WHEN (Test files-only)

### Law

- Day camp cartoon eject is the **named chain** `NODE_DAY_CAMP` → `EJECT_HOME` · cam `CAM_T0_CAMP_DAY`
- Prove labels: `NODE_DAY_CAMP` · `EJECT_HOME` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_CAMP_DAY`
- Present?=**N** (gap SoT) — camp not in umap; **0** eject/`EJECT_HOME` impl; scripts/PROXY only
- Script-only / PROXY / FALLBACK-as-eject / convert-stub = **`closed_fail`**

### Grep strings

`NODE_DAY_CAMP` · `EJECT_HOME` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_CAMP_DAY` · `Arrange` · `DONE-WHEN` · `CAP PARKED` / `PARKED` · `Present?=N` · `closed_fail`

### Negative / Anti

- Do **not** treat script-only `GP_RS_HumanoidCamp*` as world camp
- Do **not** treat PROXY `SM_ProxyDayCamp` as world camp
- Do **not** treat island→planet FALLBACK glide as `EJECT_HOME`
- Do **not** treat convert stub as cartoon eject-to-home
- No Content / Python / Source / `.uasset` / `.umap` · no DESKTOP PASS/FAIL from Design · Design does **not** self-APPROVE · other T0 MUST **DEFER**

### Future Implement note (cite only)

Gap N → Implement Act for VS_MVP `NODE_DAY_CAMP` + `EJECT_HOME` cartoon path opens **only** after Conductor routes. This packet does **not** open Source Act.

---

## Ball

**Test files-only** after draft PR. Do not merge from Design. Conductor routes next.

---

*Repo path: `Docs/handoffs/T0_M8_DAY_CAMP_EJECT_GATE_V1.md` · Bite: `T0_M8_DAY_CAMP_EJECT_GATE_V1` only · Present?=N · exclusive path.*

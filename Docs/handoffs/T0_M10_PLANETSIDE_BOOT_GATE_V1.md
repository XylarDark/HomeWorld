# T0_M10_PLANETSIDE_BOOT_GATE_V1 — MUST #10 Design packet (Arrange + DONE-WHEN freeze)

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — Design files-only; Design does **not** self-APPROVE |
| **Bite id** | `T0_M10_PLANETSIDE_BOOT_GATE_V1` |
| **MUST** | #10 — Planetside night w/o bed → glider boot home |
| **Present?** | **N** (Design SoT = ACCEPTED gap walk `T0_GAP_INVENTORY_WALK_V1` row #10) |
| **CAP** | **CAP PARKED** |
| **Host** | **CLOUD** docs-only (Contents API) |
| **Map** | `Maps/VS_MVP` |
| **DET** | HOLD `0a27306` |
| **Packet class** | Mechanic inventory freeze — Arrange + DONE-WHEN + prove labels for **Test files-only** / future **Implement Act**. **Not** a Source Act. |
| **Cite** | HomeWorld Co ops · [Architecture Trade-Offs A–E](sand-workflow:architecture-trade-offs-design-depth) (15-q) · `PROTOTYPE_FEATURE_LIST_V1` · `T0_GAP_INVENTORY_WALK_V1` #10 · `PROP_INVENTORY_V1` · `T0_M8_DAY_CAMP_EJECT_GATE_V1` (**distinct** day-camp `EJECT_HOME` — not this bite) · `T0_M9_NIGHT_HOME_GATE_V1` (night-home law cite) |

---

## One unknown (closed by this packet)

What Arrange + DONE-WHEN + prove labels freeze MUST #10 **planetside night reverse glider boot home** when Present?=**N**, distinct from MUST #8 day-camp `EJECT_HOME`, so Test scores files-only and Implement Act can open later — without Source/Content in this bite?

---

## Architecture Trade-Offs A–E (cite only — 15-q)

| Layer | Decision (inventory, **not** API invent) |
|-------|------------------------------------------|
| **A — Contract** | Prove labels `EJECT_HOME` · `TOD_NIGHT_HOME` · `FORM_BODY` · `NODE_GLIDER`. Context = **planetside night w/o bed** → reverse boot home — **not** day-camp cartoon eject (#8) · **not** island→planet FALLBACK down. |
| **B — Module** | Planetside night boot = **Layer B** deep module (+ **A**). Prefer existing glide / form night-home hooks — **no** parallel eject service; soft-kidnap ≠ boot. |
| **C — Evidence** | Law = planetside night boot greps on named labels. CAP **PARKED**. No DESKTOP PASS/FAIL from Design. |
| **D — Seats** | Design freezes here; Test files-only. Implement Act = **later** (Conductor opens). #8 Design packet is a **different** `EJECT_HOME` context. |
| **E — Stability** | FALLBACK-down / soft-kidnap / day-camp eject scored as #10 = **`closed_fail`**. Bounded fail — no invent-retry. |

**15-q:** Do **not** invent reverse-eject/WP APIs. Prefer cite existing glide + night-home form law. **No new schema.**

---

## Inventory freeze (labels ⊆ feature-list ∩ gap)

| Label | Role |
|-------|------|
| `EJECT_HOME` | Planetside night reverse boot home (**not** day-camp #8 chain) |
| `TOD_NIGHT_HOME` | Night-home / planetside night context (w/o bed) |
| `FORM_BODY` | Stay body until boot; no spirit-via-boot |
| `NODE_GLIDER` | Glider used for reverse boot path |

Labels ⊆ `PROTOTYPE_FEATURE_LIST_V1` ∩ gap #10.

---

## Expected · Found · Arrange · DONE-WHEN · Depends · Anti

| Field | Value |
|-------|-------|
| **Expected (T0)** | Planetside · night · **without** bed → glider **boot home** (`EJECT_HOME` reverse). Body (`FORM_BODY`). |
| **Found (gap SoT = N)** | FALLBACK glide is island→planet **down** only. Soft-kidnap ≠ eject. **0** planetside night reverse `EJECT_HOME` / boot-home. Present?=**N**. |
| **Arrange** | Planetside · `TOD_NIGHT_HOME` · w/o bed · `FORM_BODY` · `NODE_GLIDER` reverse boot `EJECT_HOME` → home · CAP **PARKED** |
| **DONE-WHEN** | § below — Test files-only; **no DESKTOP Act** from Design |
| **Depends / HOLD** | Distinct from `T0_M8` day-camp eject. Cite #9 night-home law (w/o bed stay body at home). Other T0 MUST **DEFER**. |
| **Anti** | FALLBACK down ≠ reverse boot · soft-kidnap ≠ boot · day-camp #8 ≠ this · no Content/Python/Source · no DESKTOP PASS/FAIL from Design · Design does not self-APPROVE |

---

## Arrange (normative)

1. Map: `Maps/VS_MVP` → **planetside** · night (`TOD_NIGHT_HOME`) · **without** bed · body (`FORM_BODY`).
2. **`EJECT_HOME` reverse boot:** glider boots player **home** (planet→home) — **not** island→planet FALLBACK down; **not** day-camp cartoon eject (#8).
3. Uses `NODE_GLIDER` path for the boot.
4. **Negatives = `closed_fail`:** FALLBACK-down-as-boot · soft-kidnap-as-boot · scoring #8 day-camp eject as #10.
5. Prove class: mechanic inventory — **not** mood/taste. CAP **PARKED**.

---

## DONE-WHEN (Test files-only)

### Law

- Planetside night w/o bed → glider boot home is the **named** `EJECT_HOME` context for #10
- Prove labels: `EJECT_HOME` · `TOD_NIGHT_HOME` · `FORM_BODY` · `NODE_GLIDER`
- Present?=**N** (gap SoT) — no reverse boot; FALLBACK down only; soft-kidnap ≠ eject
- Distinct from MUST #8 day-camp `EJECT_HOME`
- FALLBACK / soft-kidnap / #8-as-#10 = **`closed_fail`**

### Grep strings

`EJECT_HOME` · `TOD_NIGHT_HOME` · `FORM_BODY` · `NODE_GLIDER` · `Arrange` · `DONE-WHEN` · `CAP PARKED` / `PARKED` · `Present?=N` · `closed_fail`

### Negative / Anti

- Do **not** treat island→planet FALLBACK as planetside night boot home
- Do **not** treat soft-kidnap as `EJECT_HOME` boot
- Do **not** treat MUST #8 day-camp eject as this bite
- No Content / Python / Source / `.uasset` / `.umap` · no DESKTOP PASS/FAIL from Design · Design does **not** self-APPROVE · other T0 MUST **DEFER**

### Future Implement note (cite only)

Gap N → Implement Act for planetside night reverse glider boot home opens **only** after Conductor routes. This packet does **not** open Source Act.

---

## Ball

**Test files-only** after draft PR. Do not merge from Design. Conductor routes next.

---

*Repo path: `Docs/handoffs/T0_M10_PLANETSIDE_BOOT_GATE_V1.md` · Bite: `T0_M10_PLANETSIDE_BOOT_GATE_V1` only · Present?=N · exclusive path · distinct from T0_M8.*

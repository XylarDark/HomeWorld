# T0_M14_CAMP_NIGHT_GATE_V1 — MUST #14 Design packet (Arrange + DONE-WHEN freeze)

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — Design files-only; Design does **not** self-APPROVE |
| **Bite id** | `T0_M14_CAMP_NIGHT_GATE_V1` |
| **MUST** | #14 — Camp night: avoid 1 guard; soothe 2 sleepers |
| **Present?** | **N** (Design SoT = ACCEPTED gap walk `T0_GAP_INVENTORY_WALK_V1` row #14 — scripts/stealth component; not in umap; labels ∉ PROP JSON) |
| **CAP** | **CAP PARKED** |
| **Host** | **CLOUD** docs-only (Contents API) |
| **Map** | `Maps/VS_MVP` |
| **DET** | HOLD `0a27306` |
| **Packet class** | Mechanic inventory freeze — Arrange + DONE-WHEN + prove labels for **Test files-only** / future **Implement Act**. **Not** a Source Act. |
| **Cite** | HomeWorld Co ops · [Architecture Trade-Offs A–E](sand-workflow:architecture-trade-offs-design-depth) (15-q) · `PROTOTYPE_FEATURE_LIST_V1` · `T0_GAP_INVENTORY_WALK_V1` #14 · `PROP_INVENTORY_V1` (JSON gap: `NODE_GUARD` / `NODE_SLEEPER` ∉ MUST-ENV-GREYBOX `props[]`) |

---

## One unknown (closed by this packet)

What Arrange + DONE-WHEN + prove labels freeze MUST #14 **camp night avoid 1 guard + soothe 2 sleepers** when Present?=**N**, so Test scores files-only and Implement Act can open later — without Source/Content in this bite?

---

## Architecture Trade-Offs A–E (cite only — 15-q)

| Layer | Decision (inventory, **not** API invent) |
|-------|------------------------------------------|
| **A — Contract** | Prove labels `NODE_GUARD` · `NODE_SLEEPER` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` · `CAM_T0_CAMP_NIGHT`. Beat = avoid **1** guard + soothe **2** sleepers — not stealth volumes alone. |
| **B — Module** | Camp night stealth/soothe = **Layer B** deep module (+ **A**). Prefer existing `UHomeWorldSpiritStealthComponent` when Act opens — **no** parallel stealth service; convert ≠ soothe. |
| **C — Evidence** | Law = guard avoid + soothe greps on named labels + cam. CAP **PARKED**. No DESKTOP PASS/FAIL from Design. |
| **D — Seats** | Design freezes here; Test files-only. Implement Act = **later** (Conductor opens). Last invent packet in post-gap Design arc (#5 Present?=Y — no invent). |
| **E — Stability** | Script-only / stealth-component-only / convert-as-soothe / PROP-missing invent scored as #14 = **`closed_fail`**. Bounded fail — no invent-retry. |

**15-q:** Do **not** invent guard/soothe/WP APIs or PROP rows this bite. Prefer cite existing spirit stealth hooks. **No new schema.**

---

## Inventory freeze (labels ⊆ feature-list ∩ gap)

| Label | Role |
|-------|------|
| `NODE_GUARD` | Camp night guard to avoid (count: 1) |
| `NODE_SLEEPER` | Camp night sleepers to soothe (count: 2) |
| `TOD_NIGHT_SPIRIT` | Camp night spirit path |
| `FORM_SPIRIT` | Spirit form for avoid/soothe |
| `CAM_T0_CAMP_NIGHT` | Camp night cam beat |

Labels ⊆ `PROTOTYPE_FEATURE_LIST_V1` ∩ gap #14. **Honesty:** `NODE_GUARD` / `NODE_SLEEPER` ∉ `PROP_INVENTORY_V1` MUST-ENV-GREYBOX `props[]` — feature-list owns labels; PROP JSON gap stays open (not filled by this Design bite).

---

## Expected · Found · Arrange · DONE-WHEN · Depends · Anti

| Field | Value |
|-------|-------|
| **Expected (T0)** | Spirit · camp night · avoid **1** guard · soothe **2** sleepers · cam `CAM_T0_CAMP_NIGHT`. |
| **Found (gap SoT = N)** | Scripts: `GP_SS_Lit_*` (`place_vs_mvp_ss_stealth.py`) + `UHomeWorldSpiritStealthComponent` — **not** in DESKTOP umap scrape. **0** soothe/guard/sleeper actors. Labels ∉ PROP JSON. Convert ≠ soothe. Present?=**N**. |
| **Arrange** | Spirit · `FORM_SPIRIT` · `TOD_NIGHT_SPIRIT` · camp · avoid 1× `NODE_GUARD` · soothe 2× `NODE_SLEEPER` · cam `CAM_T0_CAMP_NIGHT` · CAP **PARKED** |
| **DONE-WHEN** | § below — Test files-only; **no DESKTOP Act** from Design |
| **Depends / HOLD** | Other T0 MUST **DEFER**. Cite #13 camp portal when routing later — not Acted here. |
| **Anti** | Script-only ≠ present · stealth component alone ≠ beat · convert ≠ soothe · no PROP invent this bite · no Content/Python/Source · no DESKTOP PASS/FAIL from Design · Design does not self-APPROVE |

---

## Arrange (normative)

1. Map: `Maps/VS_MVP` → night spirit (`TOD_NIGHT_SPIRIT` / `FORM_SPIRIT`) · camp night.
2. **Avoid 1× `NODE_GUARD`:** world guard actor present and avoidable (not script-only).
3. **Soothe 2× `NODE_SLEEPER`:** world sleeper actors + soothe verb (not convert stub; not stealth volume alone).
4. Cam `CAM_T0_CAMP_NIGHT`.
5. **Negatives = `closed_fail`:** script-only `GP_SS_Lit_*` · stealth-component-without-actors · convert-as-soothe · invent PROP rows here.
6. Prove class: mechanic inventory — **not** mood/taste. CAP **PARKED**.

---

## DONE-WHEN (Test files-only)

### Law

- Camp night avoid 1 guard + soothe 2 sleepers is the **named beat**
- Prove labels: `NODE_GUARD` · `NODE_SLEEPER` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` · `CAM_T0_CAMP_NIGHT`
- Present?=**N** (gap SoT) — scripts/stealth component only; not in umap; labels ∉ PROP JSON; **0** soothe/guard/sleeper
- Script-only / convert-as-soothe / stealth-alone = **`closed_fail`**

### Grep strings

`NODE_GUARD` · `NODE_SLEEPER` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` · `CAM_T0_CAMP_NIGHT` · `Arrange` · `DONE-WHEN` · `CAP PARKED` / `PARKED` · `Present?=N` · `closed_fail`

### Negative / Anti

- Do **not** treat script-only `GP_SS_Lit_*` as world guard/sleeper
- Do **not** treat convert stub as soothe
- Do **not** invent PROP JSON rows / schema in this Design bite
- No Content / Python / Source / `.uasset` / `.umap` · no DESKTOP PASS/FAIL from Design · Design does **not** self-APPROVE · other T0 MUST **DEFER**

### Future Implement note (cite only)

Gap N → Implement Act for camp night guard×1 + sleeper×2 + soothe verb (+ optional PROP rows under Conductor/Design scope) opens **only** after Conductor routes. This packet does **not** open Source Act or schema invent.

---

## Ball

**Test files-only** after draft PR. Do not merge from Design. Conductor routes next.

---

*Repo path: `Docs/handoffs/T0_M14_CAMP_NIGHT_GATE_V1.md` · Bite: `T0_M14_CAMP_NIGHT_GATE_V1` only · Present?=N · exclusive path · last invent in post-gap Design arc.*

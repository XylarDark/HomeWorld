# T0_DEFAULT_SKYBOX_DAY_V1 — Design packet (Arrange + DONE-WHEN freeze)

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — Design files-only; Design does **not** self-APPROVE |
| **Bite id** | `T0_DEFAULT_SKYBOX_DAY_V1` |
| **MUST** | Lead look — default bright day skybox (homestead / `Maps/VS_MVP`) |
| **Present?** | **N** (Lead: scene too dark; no readable default day sky) |
| **CAP** | **CAP PARKED** |
| **Host** | **CLOUD** docs-only (Contents API) |
| **Map** | `Maps/VS_MVP` |
| **DET** | HOLD `0a27306` |
| **Packet class** | Look / lighting inventory freeze — Arrange + DONE-WHEN + prove labels for **Test files-only** / future **Implement Act**. **Not** a Source/Content Act. |
| **Cite** | HomeWorld Co ops · [Architecture Trade-Offs A–E](sand-workflow:architecture-trade-offs-design-depth) (15-q) · `UHomeWorldTimeOfDaySubsystem` (Day · NightMix=0) · Lead capture defaults bright/day · `ENV_T0_HOME` |

---

## One unknown (closed by this packet)

What Arrange + DONE-WHEN + prove labels freeze a **default bright day skybox** on `Maps/VS_MVP` when Present?=**N**, so Test scores files-only and Implement Act can open later — without Source/Content / `.uasset` in this bite?

---

## Architecture Trade-Offs A–E (cite only — 15-q)

| Layer | Decision (inventory, **not** API invent) |
|-------|------------------------------------------|
| **A — Contract** | Prove labels `SKY_DEFAULT_DAY` · `TOD_DAY` · `ENV_T0_HOME`. Beat = readable **default** day sky + sun (Engine stock sky/atmosphere + directional day light) — not night lookdev, not custom HDRI art. |
| **B — Module** | Day sky = **Layer B** deep module (+ **A**). Prefer existing `UHomeWorldTimeOfDaySubsystem` Day + NightMix=0 + UE stock `SkyAtmosphere` / sky sphere / `DirectionalLight` day defaults — **no** parallel sky service / custom sky API. |
| **C — Evidence** | Law = greps on named labels + Present?=N honesty. CAP **PARKED**. No DESKTOP PASS/FAIL from Design. Taste/`APPROVE-*` later. |
| **D — Seats** | Design freezes here; Test files-only. Implement Act = **later** (Conductor opens after invent merge; **not** folded into kettle Act #2). |
| **E — Stability** | Night lookdev-as-day · empty/black sky-as-pass · custom HDRI invent · `.uasset` in invent = **`closed_fail`**. Bounded fail — no invent-retry. |

**15-q:** Do **not** invent sky/TOD APIs or schema. Prefer cite TOD Day + Engine defaults. **No new schema.**

---

## Inventory freeze (labels)

| Label | Role |
|-------|------|
| `SKY_DEFAULT_DAY` | Default bright day sky / atmosphere present and readable on homestead map |
| `TOD_DAY` | Prove on Day phase (`hw.TimeOfDay.Phase` 0 · NightMix≈0) |
| `ENV_T0_HOME` | Homestead / `Maps/VS_MVP` envelope |

Labels owned by this Lead look bite (not a gap MUST row). Feature Acts **DEFER**.

---

## Expected · Found · Arrange · DONE-WHEN · Depends · Anti

| Field | Value |
|-------|-------|
| **Expected (T0)** | Homestead · Day · default Engine bright skybox/atmosphere + day sun · readable sky (not black/empty). |
| **Found (Present?=N)** | TOD Day stub + NightMix=0 exist (`UHomeWorldTimeOfDaySubsystem`). Night lookdev path historically (`NF2_B`). Lead: live scene too dark — **no** frozen default bright day skybeat. Present?=**N**. |
| **Arrange** | `Maps/VS_MVP` · Day · `TOD_DAY` · `SKY_DEFAULT_DAY` · `ENV_T0_HOME` · CAP **PARKED** |
| **DONE-WHEN** | § below — Test files-only; **no DESKTOP Act** from Design |
| **Depends / HOLD** | Act #2 Kettle **parallel** (Implement owns; Design does not fold sky into kettle). Other T0 MUST **DEFER**. |
| **Anti** | Night lookdev ≠ day sky · black/empty sky ≠ pass · custom HDRI/art pass ≠ default · no Content/Python/Source · no `.uasset`/`.umap` · no DESKTOP PASS/FAIL from Design · Design does not self-APPROVE |

---

## Arrange (normative)

1. Map: `Maps/VS_MVP` → homestead · Day (`TOD_DAY` / `hw.TimeOfDay.Phase` 0 · NightMix≈0).
2. **`SKY_DEFAULT_DAY`:** Engine-default bright day sky (stock SkyAtmosphere and/or sky sphere) + day directional light — readable sky, not black void.
3. Envelope `ENV_T0_HOME`.
4. **Negatives = `closed_fail`:** treating NF2 night lookdev as day sky · black/empty sky as pass · inventing custom HDRI / art service · landing `.uasset` in invent PR.
5. Prove class: look inventory (default bright) — **not** mood/taste gate. CAP **PARKED**.

---

## DONE-WHEN (Test files-only)

### Law

- Default bright day skybox is the **named beat** on `SKY_DEFAULT_DAY` · `TOD_DAY` · `ENV_T0_HOME`
- Present?=**N** — Lead dark scene; no frozen default day skybeat
- Night lookdev-as-day / black sky / custom HDRI invent / `.uasset` invent = **`closed_fail`**

### Grep strings

`SKY_DEFAULT_DAY` · `TOD_DAY` · `ENV_T0_HOME` · `Arrange` · `DONE-WHEN` · `CAP PARKED` / `PARKED` · `Present?=N` · `closed_fail`

### Negative / Anti

- Do **not** treat `NF2_B` night lookdev as `SKY_DEFAULT_DAY`
- Do **not** invent custom sky API / HDRI art pass this bite
- No Content / Python / Source / `.uasset` / `.umap` · no DESKTOP PASS/FAIL from Design · Design does **not** self-APPROVE · kettle Act **DEFER** from this packet · other T0 MUST **DEFER**

### Future Implement note (cite only)

Present?=N → Implement Act places Engine-default bright day sky + day sun on `Maps/VS_MVP` (prefer stock actors; drive via existing TOD Day / NightMix=0) **only** after Conductor opens sky Act (queue after M2 per Lead, or when Conductor routes). This packet does **not** open Source/Content Act or fold into kettle.

---

## Ball

**Test files-only** after draft PR. Do not merge from Design. Conductor greps → Test → invent auto-merge.

---

*Repo path: `Docs/handoffs/T0_DEFAULT_SKYBOX_DAY_V1.md` · Bite: `T0_DEFAULT_SKYBOX_DAY_V1` only · Present?=N · exclusive path.*

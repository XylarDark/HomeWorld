# T0_M1_WAKE_GATE_V1 — MUST #1 Design packet (Arrange + DONE-WHEN freeze)

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — Design files-only; Design does **not** self-APPROVE |
| **Bite id** | `T0_M1_WAKE_GATE_V1` |
| **MUST** | #1 — Wake / start day (homestead) |
| **Present?** | **Partial** (Design SoT = ACCEPTED gap walk `T0_GAP_INVENTORY_WALK_V1` row #1) |
| **CAP** | **CAP PARKED** |
| **Host** | **CLOUD** docs-only (Contents API) |
| **Map** | `Maps/VS_MVP` |
| **DET** | HOLD `0a27306` |
| **Packet class** | Mechanic inventory freeze — Arrange + DONE-WHEN + prove labels for **Test files-only** / future **Implement Act**. **Not** a Source Act. |
| **Cite** | HomeWorld Co ops · [Architecture Trade-Offs A–E](sand-workflow:architecture-trade-offs-design-depth) (15-q) · `PROTOTYPE_FEATURE_LIST_V1` · `T0_GAP_INVENTORY_WALK_V1` #1 · `PROP_INVENTORY_V1` (`NODE_WAKE` · `ENV_T0_HOME` · `FEEL-ENV-GREYBOX`) |

---

## One unknown (closed by this packet)

What Arrange + DONE-WHEN + prove labels freeze MUST #1 **wake / start day** on `NODE_WAKE` when Present?=**Partial**, so Test scores files-only and Implement Act can open later — without Source/Content in this bite?

---

## Architecture Trade-Offs A–E (cite only — 15-q)

| Layer | Decision (inventory, **not** API invent) |
|-------|------------------------------------------|
| **A — Contract** | Prove labels `NODE_WAKE` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_WAKE`. Wake is the **named homestead start-day beat** — not PlayerStart alone, not bed→Dawn alone. |
| **B — Module** | Wake / TOD day start = **Layer B** deep module (+ **A**). Prefer existing `GP_PlayerStart` / `PlayerStart_VS_MVP` / `UHomeWorldTimeOfDaySubsystem` — **no** parallel wake service. |
| **C — Evidence** | Law = wake beat greps on named labels + cam. CAP **PARKED**. No DESKTOP PASS/FAIL from Design. |
| **D — Seats** | Design freezes here; Test files-only. Implement Act = **later** (Conductor opens). |
| **E — Stability** | Spawn-only / PROXY-as-wake / bed-Dawn-only scored as T0 wake beat = **`closed_fail`**. Bounded fail — no invent-retry. |

**15-q:** Do **not** invent wake/WP APIs. Prefer cite existing PlayerStart / TOD hooks. **No new schema.**

---

## Inventory freeze (labels ⊆ feature-list ∩ gap)

| Label | Role |
|-------|------|
| `NODE_WAKE` | Homestead start-day wake beat (frozen label, not spawn alone) |
| `TOD_DAY` | Wake prove on Day |
| `FORM_BODY` | Body form at start day |
| `CAM_T0_WAKE` | Wake / homestead start cam beat |

Labels ⊆ `PROTOTYPE_FEATURE_LIST_V1` ∩ gap #1. PROP: `NODE_WAKE` · envelope `ENV_T0_HOME`.

---

## Expected · Found · Arrange · DONE-WHEN · Depends · Anti

| Field | Value |
|-------|-------|
| **Expected (T0)** | Homestead · Day · body · readable start-day wake at frozen `NODE_WAKE` · cam `CAM_T0_WAKE`. |
| **Found (gap SoT = Partial)** | Umap: `GP_PlayerStart`, `PlayerStart_VS_MVP` · script `place_vs_mvp_gp.py` · TOD Day via `UHomeWorldTimeOfDaySubsystem` · PROXY `NODE_WAKE` / `SM_ProxyWakeMarker` (**not on disk**). Homestead spawn present. **No** frozen `NODE_WAKE` actor label; wake-from-bed is Dawn advance, not a dedicated start-day beat log. Present?=**Partial**. |
| **Arrange** | Homestead · Day · `FORM_BODY` · `NODE_WAKE` start-day beat · cam `CAM_T0_WAKE` · CAP **PARKED** |
| **DONE-WHEN** | § below — Test files-only; **no DESKTOP Act** from Design |
| **Depends / HOLD** | Other T0 MUST **DEFER**. |
| **Anti** | PlayerStart alone ≠ `NODE_WAKE` · PROXY ≠ world wake · bed-Dawn alone ≠ start-day beat · no Content/Python/Source · no DESKTOP PASS/FAIL from Design · Design does not self-APPROVE |

---

## Arrange (normative)

1. Map: `Maps/VS_MVP` → homestead · Day · body (`FORM_BODY`).
2. **`NODE_WAKE` beat:** start-day wake at frozen homestead wake label (world / log beat — **not** PROXY mesh alone; **not** PlayerStart spawn alone).
3. Cam `CAM_T0_WAKE` for readable homestead start.
4. **Negatives = `closed_fail`:** spawn-only / PROXY-as-wake / treating bed→Dawn alone as T0 start-day wake beat.
5. Prove class: mechanic inventory — **not** mood/taste. CAP **PARKED**.

---

## DONE-WHEN (Test files-only)

### Law

- Homestead start-day wake is the **named beat** on `NODE_WAKE` · cam `CAM_T0_WAKE`
- Prove labels: `NODE_WAKE` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_WAKE`
- Present?=**Partial** (gap SoT) — spawn + TOD Day present; **no** frozen `NODE_WAKE` actor label; bed-Dawn ≠ dedicated start-day beat; PROXY ≠ world wake
- Spawn-only / PROXY / bed-Dawn-as-wake = **`closed_fail`**

### Grep strings

`NODE_WAKE` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_WAKE` · `Arrange` · `DONE-WHEN` · `CAP PARKED` / `PARKED` · `Present?=Partial` · `closed_fail`

### Negative / Anti

- Do **not** treat `GP_PlayerStart` / `PlayerStart_VS_MVP` alone as `NODE_WAKE` beat
- Do **not** treat PROXY `SM_ProxyWakeMarker` as world wake
- Do **not** treat bed→Dawn alone as T0 start-day wake beat
- No Content / Python / Source / `.uasset` / `.umap` · no DESKTOP PASS/FAIL from Design · Design does **not** self-APPROVE · other T0 MUST **DEFER**

### Future Implement note (cite only)

Gap Partial → Implement Act for frozen `NODE_WAKE` homestead start-day beat + cam opens **only** after Conductor routes. This packet does **not** open Source Act.

---

## Ball

**Test files-only** after draft PR. Do not merge from Design. Conductor routes next.

---

*Repo path: `Docs/handoffs/T0_M1_WAKE_GATE_V1.md` · Bite: `T0_M1_WAKE_GATE_V1` only · Present?=Partial · exclusive path.*

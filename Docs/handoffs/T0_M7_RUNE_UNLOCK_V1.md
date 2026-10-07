# T0_M7_RUNE_UNLOCK_V1 — MUST #7 Design packet (Arrange + DONE-WHEN freeze)

| Field | Value |
|-------|-------|
| **Status** | **APPROVED (Lead stamp 2026-10-07)** - Design frozen for Test files-only scoring; missing `NODE_RUNE` prop is the tracked impl gap |
| **Bite id** | `T0_M7_RUNE_UNLOCK_V1` |
| **MUST** | #7 — Rune unlock before bed→spirit |
| **Present?** | **Partial** (Design SoT = ACCEPTED gap walk `T0_GAP_INVENTORY_WALK_V1` row #7 — **not** Conductor Present?=N routing; honesty pattern same as T0_M9 Present?=Y vs stale Partial) |
| **CAP** | **CAP PARKED** (stills confirm-only; bots must **not** PASS taste; CAP product stays parked) |
| **Host** | **CLOUD** docs-only (Contents API; Cursor cloud may be capped) |
| **Map** | `Maps/VS_MVP` |
| **DET** | HOLD `0a27306` |
| **Packet class** | Mechanic inventory freeze — freezes Arrange + DONE-WHEN + prove labels for **Test files-only** / future **Implement Act** (Conductor opens later). **Not** a Source Act in this Design bite. |
| **Cite** | HomeWorld Co ops · [Architecture Trade-Offs A–E](sand-workflow:architecture-trade-offs-design-depth) (15-q note) · `PROTOTYPE_FEATURE_LIST_V1` · `T0_GAP_INVENTORY_WALK_V1` row #7 · `T0_M9_NIGHT_HOME_GATE_V1` (Depends: #11 stays HOLD until this + bed packet) · `PROP_INVENTORY_V1` · older `T0_MECHANIC_INVENTORIES_V1` #7 shape |

---

## One unknown (closed by this packet)

What Arrange + DONE-WHEN + prove labels freeze MUST #7 (`NODE_RUNE`) for the **missing world unlock interact** when Present?=**Partial** (gap SoT), so Test can score files-only and Implement Act can open later — without opening Source/Content in this Design bite?

---

## Architecture Trade-Offs A–E (cite only — 15-q)

| Layer | Decision for this bite (inventory, **not** API invent) |
|-------|--------------------------------------------------------|
| **A — Contract** | Prove contract = named labels `NODE_RUNE` · `TOD_DAY` · `FORM_BODY`. Callers see form via **named gates** (sleep + rune + location policy), not phase alone. Rune unlock is the **named gate before** bed→spirit (#11). |
| **B — Module** | Form / sleep / rune gate = **Layer B** deep module (+ **A** contract). **No second form service.** Rune unlock flag feeds existing `CanEnterSpiritForm()` / character TOD path — do **not** invent a parallel form service. |
| **C — Evidence** | Law prove = unlock flag + interact presence greps / FORM gates. CAP product stays **PARKED**. No DESKTOP PASS/FAIL from Design. |
| **D — Seats** | Design freezes Arrange/DONE-WHEN here; Test scores files-only. Implement Act for missing world unlock = **later** (Conductor opens). Source/Content **not** this bite. #11 bed packet stays **HOLD** until this + bed Design packets land. |
| **E — Stability** | Bed→spirit **without** rune unlock = **`closed_fail`** / blocked vs T0 law — bounded fail, not invent-retry / grant-spirit-on-phase workaround. |

**15-q:** Do **not** invent WP/form APIs. Prefer cite existing gate hooks (`SetRuneGateUnlocked`, `bRuneGateUnlocked`, `CanEnterSpiritForm`). Schema before data — **no new schema** this packet.

---

## Inventory freeze (labels ⊆ feature-list ∩ gap)

Only these prove labels (exclusive freeze for this bite):

| Label | Role |
|-------|------|
| `NODE_RUNE` | Day field-path rune unlock interact (world actor / gate) |
| `TOD_DAY` | Unlock prove runs on Day (field path) |
| `FORM_BODY` | Body form while unlocking; spirit grant stays behind named gates |

Labels ⊆ `PROTOTYPE_FEATURE_LIST_V1` inventory freeze ∩ gap walk suggested prove labels for #7.

---

## Expected · Found · Arrange · DONE-WHEN · Depends · Anti

| Field | Value |
|-------|-------|
| **Expected (T0)** | Day rune unlock **before** bed→spirit works. **Without** unlock: bed **cannot** grant spirit. **With** unlock: #11 may proceed. Bed→spirit without rune = **`closed_fail`** / blocked. |
| **Found (gap SoT = Partial)** | Gate hook present: Source API `SetRuneGateUnlocked` / `bRuneGateUnlocked` (default locked). PROXY inventory only (`NODE_RUNE` / `SM_ProxyRune`) — **not** on disk as world unlock. **0** `NODE_RUNE` rune actor in `Maps/VS_MVP` umap. **Present?=Partial** — Design SoT = gap Partial (Conductor Present?=N routing is **not** Design SoT; same honesty pattern as T0_M9 Present?=Y vs stale Partial). This packet freezes Arrange + DONE-WHEN for the **missing world unlock interact** (Partial → Implement Act later after Conductor opens). **Not** a Source Act in this Design bite. |
| **Arrange** | Day · field path · `NODE_RUNE` interact · unlock flag persisted · without unlock bed cannot grant spirit · CAP **PARKED** |
| **DONE-WHEN** | See § DONE-WHEN below (Test can run files-only greps on this md — **no DESKTOP Act** required from this Design packet) |
| **Depends / HOLD** | #11 bed→spirit stays **HOLD** until **this** packet + bed Design packet land. #9 already merged (`T0_M9_NIGHT_HOME_GATE_V1`). All other T0 MUST **DEFER**. |
| **Anti** | Do not grant spirit on phase alone · do not treat PROXY mesh as world unlock · no invent form/WP APIs · no Content/Python/Source · no DESKTOP PASS/FAIL from Design · no CAP reopen · Design does not self-APPROVE |

---

## Arrange (normative)

1. Map: `Maps/VS_MVP` → Day start, body (`FORM_BODY`), field path (not homestead-only).
2. **`NODE_RUNE` interact:** player reaches and interacts the day field-path rune unlock (world unlock — **not** PROXY inventory alone).
3. Unlock flag persisted: `bRuneGateUnlocked` / `SetRuneGateUnlocked` path becomes unlocked and **stays** unlocked for subsequent bed prove.
4. **Without unlock:** bed path **cannot** grant spirit — bed→spirit without rune = **`closed_fail`** / blocked vs T0 law.
5. **With unlock:** #11 bed→spirit Design/Implement may proceed (separate bite; not this packet's Act).
6. **Prove class:** mechanic inventory / gate law — **not** mood/taste. CAP stays **PARKED**.

---

## DONE-WHEN (Test files-only)

Test may score this packet files-only on this markdown. This Design packet does **not** require DESKTOP Act or Source/Content edits.

### Law

- Day rune unlock is the **named gate before** bed→spirit (#11)
- Without unlock: bed **cannot** grant spirit
- Bed→spirit without rune = **`closed_fail`** / blocked vs T0 law
- With unlock: #11 may proceed (Depends/HOLD lifts only after this + bed packet)
- Present?=**Partial** (gap SoT) — missing world unlock interact; gate API hook exists; PROXY ≠ world unlock; 0 `NODE_RUNE` actor on VS_MVP umap

### Grep strings (must appear in this packet for Test harness)

`NODE_RUNE` · `TOD_DAY` · `FORM_BODY` · `Arrange` · `DONE-WHEN` · `CAP PARKED` / `PARKED` · `Present?=Partial` · `closed_fail`

### Negative prove / Anti (locked in DONE-WHEN)

- Do **not** grant spirit on phase alone
- Do **not** treat PROXY mesh (`SM_ProxyRune` / inventory-only) as world unlock
- Do **not** invent form/WP APIs
- No Content / Python / Source / `.uasset` / `.umap` in this Design bite
- No DESKTOP PASS/FAIL from Design

### Future Implement note (cite only — not this bite)

Gap Partial → Implement Act for missing `NODE_RUNE` world unlock interact opens **only** after Conductor routes. This Design packet freezes Arrange + DONE-WHEN; it does **not** open Source Act.

---

## HOLD / DEFER / Anti (locked)

- #11 bed→spirit = **HOLD** until this packet + bed Design packet land
- #9 night home gate = **already merged** (`T0_M9_NIGHT_HOME_GATE_V1`)
- All other T0 MUST **DEFER**
- No CAP reopen (CAP stays **PARKED**)
- No Content / Python / Source / `.uasset` / `.umap`
- No DESKTOP PASS/FAIL from Design
- No invent WP/form APIs; schema before data — prefer existing gate hooks (`SetRuneGateUnlocked`, `bRuneGateUnlocked`, `CanEnterSpiritForm`)
- Design does **not** self-APPROVE

---

## Ball

**Test files-only** after draft PR (grep DONE-WHEN strings + law lock). Do not merge from Design. Conductor routes next (Implement Act for missing world unlock — later; then #11 bed packet).

---

*Repo path: `Docs/handoffs/T0_M7_RUNE_UNLOCK_V1.md` · Bite: `T0_M7_RUNE_UNLOCK_V1` only · Present?=Partial (gap SoT) · CAP PARKED · exclusive path.*

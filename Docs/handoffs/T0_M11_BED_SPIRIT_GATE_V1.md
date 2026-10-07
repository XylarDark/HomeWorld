# T0_M11_BED_SPIRIT_GATE_V1 — MUST #11 Design packet (Arrange + DONE-WHEN freeze)

| Field | Value |
|-------|-------|
| **Status** | **APPROVED (Lead stamp 2026-10-07)** - Design frozen; unwired `GrantSpiritSleepGate` in the bed interact and missing `BP_Bed` placement are the tracked impl gaps |
| **Bite id** | `T0_M11_BED_SPIRIT_GATE_V1` |
| **MUST** | #11 — Bed → spirit (after rune) |
| **Present?** | **Partial** (Design SoT = ACCEPTED gap walk `T0_GAP_INVENTORY_WALK_V1` row #11 — **Present?=Partial**; honesty pattern same as T0_M7 Present?=Partial / T0_M9 Present?=Y vs stale routing) |
| **CAP** | **CAP PARKED** (stills confirm-only; bots must **not** PASS night mood / taste; CAP product stays parked) |
| **Host** | **CLOUD** docs-only (Contents API; Cursor cloud may be capped) |
| **Map** | `Maps/VS_MVP` |
| **DET** | HOLD `0a27306` |
| **Packet class** | Mechanic inventory freeze — freezes Arrange + DONE-WHEN + prove labels for **Test files-only** / future **Implement Act** (Conductor opens later). **Not** a Source Act in this Design bite. |
| **Cite** | HomeWorld Co ops · [Architecture Trade-Offs A–E](sand-workflow:architecture-trade-offs-design-depth) (15-q note) · `PROTOTYPE_FEATURE_LIST_V1` · `T0_GAP_INVENTORY_WALK_V1` row #11 · `T0_M7_RUNE_UNLOCK_V1` (merged — Depends HOLD lifts for this Design packet) · `T0_M9_NIGHT_HOME_GATE_V1` (merged — #9 negative bed still holds) · `PROP_INVENTORY_V1` · older `T0_MECHANIC_INVENTORIES_V1` #11 shape |

---

## One unknown (closed by this packet)

What Arrange + DONE-WHEN + prove labels freeze MUST #11 (`NODE_BED` → `FORM_SPIRIT` after rune) for the **bed sleep-gate + spirit grant + VS_MVP bed placement** gaps when Present?=**Partial** (gap SoT), so Test can score files-only and Implement Act can open later — without opening Source/Content in this Design bite?

---

## Architecture Trade-Offs A–E (cite only — 15-q)

| Layer | Decision for this bite (inventory, **not** API invent) |
|-------|--------------------------------------------------------|
| **A — Contract** | Prove contract = named labels `NODE_BED` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` · `CAM_T0_BED` · `NODE_RUNE`. Callers see form via **named gates** (sleep + rune + location policy), not phase alone. Bed grants **sleep gate** then form **only** with rune unlocked. |
| **B — Module** | Form / sleep / rune gate = **Layer B** deep module (+ **A** contract). **No second form service.** Bed path feeds existing `GrantSpiritSleepGate` / `CanEnterSpiritForm()` / character TOD path — do **not** invent a parallel form service. |
| **C — Evidence** | Law prove = bed interact + sleep-gate grant + rune unlock + FORM_SPIRIT greps / cam `CAM_T0_BED`. CAP product stays **PARKED**. No DESKTOP PASS/FAIL from Design. No night mood bot PASS. |
| **D — Seats** | Design freezes Arrange/DONE-WHEN here; Test scores files-only. Implement Act for sleep-gate wire + rune wire + VS_MVP bed instance = **later** (Conductor opens). Source/Content **not** this bite. Depends HOLD on Design packets T0_M7 + T0_M9 **lifts** (both merged). |
| **E — Stability** | Phase-only spirit (Night via bed/`SetPhase` **without** sleep-gate+rune) = **`closed_fail`** vs T0+M9 law. Spirit without bed+rune = **`closed_fail`**. #9 negative bed (Night@home w/o bed → stay `FORM_BODY`) **still holds**. Bounded fail — not invent-retry / grant-spirit-on-phase workaround. |

**15-q:** Do **not** invent WP/form APIs. Prefer cite existing gate hooks (`GrantSpiritSleepGate`, `bSpiritSleepGateGranted`, `SetRuneGateUnlocked` / `bRuneGateUnlocked`, `CanEnterSpiritForm`, `ApplyFormForPhase`, GoToBed / `UHomeWorldGoToBedTriggerComponent`). Schema before data — **no new schema** this packet.

---

## Inventory freeze (labels ⊆ feature-list ∩ gap)

Only these prove labels (exclusive freeze for this bite):

| Label | Role |
|-------|------|
| `NODE_BED` | Bed interact (world instance on VS_MVP — not disk BP alone) |
| `TOD_NIGHT_SPIRIT` | Night planetside spirit path after successful bed+rune |
| `FORM_SPIRIT` | Spirit form granted only via bed after rune |
| `CAM_T0_BED` | Bed → spirit cam beat |
| `NODE_RUNE` | Prerequisite rune unlock (MUST #7 — named gate before bed→spirit) |

Labels ⊆ `PROTOTYPE_FEATURE_LIST_V1` inventory freeze ∩ gap walk suggested prove labels for #11.

---

## Expected · Found · Arrange · DONE-WHEN · Depends · Anti

| Field | Value |
|-------|-------|
| **Expected (T0)** | After rune unlock: **bed → spirit** as night planetside gate. Spirit planetside night **only** via bed after rune. #9 still holds w/o bed (stay `FORM_BODY`). Cam `CAM_T0_BED`. Phase-only spirit / spirit w/o bed+rune = **`closed_fail`** vs T0+M9 law. |
| **Found (gap SoT = Partial)** | Disk: `BP_Bed.uasset` · `UHomeWorldGoToBedTriggerComponent` / bed tag interact → `SetPhase(Night)` **only**. `GrantSpiritSleepGate` API exists but **not** called from GoToBed/Interact. **no** `BP_Bed` instance string in VS_MVP umap scrape. Needs #7 rune. **Present?=Partial** — Design SoT = gap Partial. Bed→Night works; sleep-gate + rune not wired for T0 bed→spirit; bed may not be placed on VS_MVP KEEP-LOCAL. This packet freezes Arrange + DONE-WHEN for those gaps (Partial → Implement Act later after Conductor opens). **Not** a Source Act in this Design bite. |
| **Arrange** | After `NODE_RUNE` unlock · `NODE_BED` interact on VS_MVP · sleep gate granted · Night spirit (`TOD_NIGHT_SPIRIT` / `FORM_SPIRIT`) · cam `CAM_T0_BED` · #9 w/o bed still `FORM_BODY` · CAP **PARKED** |
| **DONE-WHEN** | See § DONE-WHEN below (Test can run files-only greps on this md — **no DESKTOP Act** required from this Design packet) |
| **Depends / HOLD** | Requires Design packets **T0_M9** (merged) + **T0_M7** (merged) — **HOLD lifts** for this Design packet. Implement Act still **DEFER** until Conductor opens. All other T0 MUST **DEFER**. |
| **Anti** | Phase-only spirit ≠ pass · soft-kidnap ≠ bed · no CAP reopen · no night mood bot PASS · no Content/Python/Source · no DESKTOP PASS/FAIL from Design · Design does not self-APPROVE · other MUST DEFER |

---

## Arrange (normative)

1. Map: `Maps/VS_MVP` → Day start, body (`FORM_BODY`); **rune unlocked first** (`NODE_RUNE` / MUST #7 path — prerequisite, not re-Acted here).
2. **`NODE_BED` interact:** player reaches and interacts the bed world instance on VS_MVP (not disk `BP_Bed.uasset` alone; instance must exist for prove).
3. Bed path **grants sleep gate** (`GrantSpiritSleepGate` / `bSpiritSleepGateGranted`) — **not** phase-only `SetPhase(Night)`.
4. With sleep gate **and** rune unlocked: enter spirit (`FORM_SPIRIT`) on night planetside path (`TOD_NIGHT_SPIRIT`); cam `CAM_T0_BED`.
5. **#9 still holds:** Night@home **without** successful bed → stay `FORM_BODY`; day abilities off (cite `T0_M9_NIGHT_HOME_GATE_V1`).
6. **Negatives = `closed_fail`:** phase-only spirit (Night without sleep-gate+rune) · spirit without bed+rune — both **`closed_fail`** vs T0+M9 law.
7. **Prove class:** mechanic inventory / gate law — **not** mood/taste. CAP stays **PARKED**. Soft-kidnap / shrine ≠ bed.

---

## DONE-WHEN (Test files-only)

Test may score this packet files-only on this markdown. This Design packet does **not** require DESKTOP Act or Source/Content edits.

### Law

- After rune unlock: bed → spirit as night planetside gate
- Spirit planetside night **only** via bed after rune
- #9 negative bed still holds (Night@home w/o bed → `FORM_BODY`)
- Cam `CAM_T0_BED`
- Phase-only spirit / spirit w/o bed+rune = **`closed_fail`** vs T0+M9 law
- Present?=**Partial** (gap SoT) — Bed→Night works; `GrantSpiritSleepGate` not called from GoToBed/Interact; no `BP_Bed` instance on VS_MVP umap; needs #7 rune

### Grep strings (must appear in this packet for Test harness)

`NODE_BED` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` · `CAM_T0_BED` · `NODE_RUNE` · `Arrange` · `DONE-WHEN` · `CAP PARKED` / `PARKED` · `Present?=Partial` · `closed_fail`

### Negative prove / Anti (locked in DONE-WHEN)

- Phase-only spirit ≠ pass (`SetPhase(Night)` alone without sleep-gate+rune = **`closed_fail`**)
- Soft-kidnap / shrine ≠ bed
- Do **not** reopen CAP; no night mood bot PASS
- No Content / Python / Source / `.uasset` / `.umap` in this Design bite
- No DESKTOP PASS/FAIL from Design
- Design does **not** self-APPROVE
- All other T0 MUST **DEFER**

### Future Implement note (cite only — not this bite)

Gap Partial → Implement Act for (1) wire `GrantSpiritSleepGate` from GoToBed/Interact, (2) rune prerequisite already Design-frozen in T0_M7, (3) VS_MVP `NODE_BED` / `BP_Bed` instance placement if missing — opens **only** after Conductor routes. This Design packet freezes Arrange + DONE-WHEN; it does **not** open Source Act.

---

## HOLD / DEFER / Anti (locked)

- Depends HOLD on Design packets T0_M7 + T0_M9 = **lifted** (both merged) for **this** Design packet
- Implement Act for bed→spirit wire = still **DEFER** until Conductor opens
- All other T0 MUST **DEFER**
- No CAP reopen (CAP stays **PARKED**)
- No Content / Python / Source / `.uasset` / `.umap`
- No DESKTOP PASS/FAIL from Design
- No invent WP/form APIs; schema before data — prefer existing gate hooks (`GrantSpiritSleepGate`, `CanEnterSpiritForm`, GoToBed)
- Phase-only spirit ≠ pass · soft-kidnap ≠ bed · no night mood bot PASS
- Design does **not** self-APPROVE

---

## Ball

**Test files-only** after draft PR (grep DONE-WHEN strings + law lock). Do not merge from Design. Conductor routes next (Implement Act for sleep-gate wire + VS_MVP bed instance — later).

---

*Repo path: `Docs/handoffs/T0_M11_BED_SPIRIT_GATE_V1.md` · Bite: `T0_M11_BED_SPIRIT_GATE_V1` only · Present?=Partial (gap SoT) · CAP PARKED · exclusive path.*

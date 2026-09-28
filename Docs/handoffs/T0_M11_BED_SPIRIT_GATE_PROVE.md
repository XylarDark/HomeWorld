# T0_M11_BED_SPIRIT_GATE - DESKTOP prove packet (Test)

| Field | Value |
|-------|-------|
| **Bite** | `T0_M11_BED_SPIRIT_GATE_V1` (MUST #11) |
| **Map** | `Maps/VS_MVP` (homestead / bed) |
| **Labels** | `NODE_BED` / `TOD_NIGHT_SPIRIT` / `FORM_SPIRIT` / `CAM_T0_BED` / `NODE_RUNE` |
| **CAP** | **PARKED** |
| **Impl** | Source wire: `AHomeWorldCharacter::TryBedSleepSpirit` + GoToBed/Interact/overlap -> `GrantSpiritSleepGate` + console `hw.Bed.SleepSpirit` (existing `CanEnterSpiritForm` / `ApplyFormForPhase`; rune via #7) |
| **Design** | `Docs/handoffs/T0_M11_BED_SPIRIT_GATE_V1.md` (**untouched**) |
| **Gate JSON (suggest)** | `Saved/t0_m11_bed_spirit_gate.json` |
| **Bed instance** | **KEEP-LOCAL** -- VS_MVP may lack `BP_Bed` / `NODE_BED` instance; console prove OK without committing `.uasset` / `.umap`. Note missing instance in prove notes; do **not** commit umap/uasset. |

## Arrange

1. PIE `Maps/VS_MVP` -> homestead / body / **Day** (`hw.TimeOfDay.SetPhase 0` or `hw.TimeOfDay.Phase 0` if needed).
2. **Rune first (prereq #7):** `hw.Rune.Unlock` -> expect `NODE_RUNE: unlock TOD_DAY FORM_BODY`. Confirm `IsRuneGateUnlocked` / `bRuneGateUnlocked` true. Do **not** re-Act #7 beyond unlock for this prove.
3. Confirm still `FORM_BODY` (sleep gate not yet granted; `CanEnterSpiritForm` false until bed).
4. CAP **PARKED** -- no still product / night mood bot PASS.
5. Bed path: console `hw.Bed.SleepSpirit` (primary). Optional: Interact (E) on actor tagged `Bed` / `NODE_BED`, or overlap `UHomeWorldGoToBedTriggerComponent`, if KEEP-LOCAL bed instance exists.
6. #9 still holds: Night@home **without** bed (`hw.TimeOfDay.SetPhase 2` alone, no GrantSpiritSleepGate) -> stay `FORM_BODY`. Soft-kidnap / shrine != bed.

## Act greps

| Expect | Grep / observe | soft_fail | closed_fail |
|--------|----------------|-----------|-------------|
| Bed -> spirit | Output log contains `NODE_BED:` with `TOD_NIGHT_SPIRIT` `FORM_SPIRIT` `CAM_T0_BED` `NODE_RUNE` | Extra already-granted re-log | No bed line; or phase-alone / soft-kidnap scored as #11 |
| Sleep + rune | `GrantSpiritSleepGate` / `bSpiritSleepGateGranted` + `bRuneGateUnlocked`; `FORM: spirit` with gates sleep=1 rune=1 | Re-sync form noise | Scoring spirit-on-phase alone as MUST #11 PASS |
| Rune prereq | Without unlock, bed->spirit blocked (`TryBedSleepSpirit` fails / `CanEnterSpiritForm` false) | Sleep-gate-only `FORM_BODY` log | Scoring bed->spirit without `NODE_RUNE` as PASS |
| Phase-only anti | `hw.TimeOfDay.SetPhase 2` alone (no bed / no GrantSpiritSleepGate) -> `FORM_BODY` (#9) | Unrelated NODE_* | `FORM_SPIRIT` from SetPhase alone |
| Soft-kidnap anti | Soft-kidnap / shrine != bed beat | Unrelated shrine docs | Soft-kidnap scored as `NODE_BED` |
| Other MUST DEFER | No planetside-boot / day-camp / kettle Act as this bite; #9/#7 cite-only | Unrelated NODE_* logs | Scoring other MUST as #11 |

## Pass bar (team)

- After `hw.Rune.Unlock`: bed path -> greppable `NODE_BED:` citing `TOD_NIGHT_SPIRIT` / `FORM_SPIRIT` / `CAM_T0_BED` / `NODE_RUNE`.
- Via existing `GrantSpiritSleepGate` + `CanEnterSpiritForm` / `ApplyFormForPhase` -- **no** parallel form service.
- Console `hw.Bed.SleepSpirit` + Character `TryBedSleepSpirit`; Interact/overlap/GoToBed also call `GrantSpiritSleepGate`.
- **closed_fail** if phase-only spirit, spirit w/o bed+rune, soft-kidnap-as-bed, or breaking #9 (Night w/o bed -> spirit).
- Other T0 MUST **DEFER**. No `.uasset` / `.umap` commits. Design invent left **untouched**. Bed instance KEEP-LOCAL if missing.

## DESKTOP prove steps (paste)

1. PIE `Maps/VS_MVP`; ensure Day (`hw.TimeOfDay.SetPhase 0`) and body form.
2. `hw.Rune.Unlock` -> expect `NODE_RUNE: unlock TOD_DAY FORM_BODY` (+ `FORM: rune gate unlocked` / `hw.Rune.Unlock ok`).
3. **Negative:** `hw.TimeOfDay.SetPhase 2` alone (optional separate pass without bed) -> expect `FORM: body` / gates sleep=0 (or sleep uncleared only if prior bed) -- **do not** score phase-alone as #11. Prefer: fresh PIE, SetPhase Night without bed/rune -> `FORM_BODY` (#9).
4. Back to Day if needed; ensure rune still unlocked; then `hw.Bed.SleepSpirit` -> expect `NODE_BED: TOD_NIGHT_SPIRIT FORM_SPIRIT CAM_T0_BED NODE_RUNE` (+ `hw.Bed.SleepSpirit ok` / `FORM: spirit` sleep=1 rune=1).
5. Optional: second `hw.Bed.SleepSpirit` -> already granted soft path (still greppable labels).
6. Confirm latch: `bBedSpiritGranted` / `IsBedSpiritGranted`; `bSpiritSleepGateGranted`; `CanEnterSpiritForm` true.
7. Optional world: Interact `Bed`/`NODE_BED` or overlap GoToBedTrigger (KEEP-LOCAL bed -- note if missing; do not commit umap).
8. Other T0 MUST **DEFER**. Optional gate JSON: write `Saved/t0_m11_bed_spirit_gate.json` after greps.

## Source symbols (files-only greps)

`TryBedSleepSpirit` / `IsBedSpiritGranted` / `bBedSpiritGranted` / `GrantSpiritSleepGate` / `bSpiritSleepGateGranted` / `CanEnterSpiritForm` / `ApplyFormForPhase` / `IsRuneGateUnlocked` / `bRuneGateUnlocked` / `NODE_BED` / `TOD_NIGHT_SPIRIT` / `FORM_SPIRIT` / `CAM_T0_BED` / `NODE_RUNE` / `hw.Bed.SleepSpirit` / `hw.Rune.Unlock` / `closed_fail` (this packet + Design) / phase-alone / soft-kidnap (anti) / `TOD_NIGHT_HOME` (#9 cite)

## Architecture Trade-Offs A-E (cite)

| Layer | Decision |
|-------|----------|
| **A - Contract** | Labels `NODE_BED` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` · `CAM_T0_BED` · `NODE_RUNE`; named sleep+rune gates, not phase alone |
| **B - Module** | Prefer existing `GrantSpiritSleepGate` / `CanEnterSpiritForm` / `ApplyFormForPhase` -- **no** second form service |
| **C - Evidence** | Greppable Source emit + this prove packet; CAP **PARKED** |
| **D - Seats** | Implement Act Source; Conductor owns MCP/PIE |
| **E - Stability** | Phase-only / spirit-w/o-bed+rune / soft-kidnap / #9 break = `closed_fail`; no invent form/WP APIs |

## Conductor note

Conductor owns MCP/PIE cam / still capture. Implement does **not** drive MCP. CAP **PARKED**. Other MUST = separate bites. #7 rune = **prereq** (unlock first; do not re-Act). #9 night-home w/o bed = **cite / anti** (stay `FORM_BODY`). Bed world instance = KEEP-LOCAL if missing -- console prove suffices; never commit `.uasset` / `.umap`. Suggest gate JSON path: `Saved/t0_m11_bed_spirit_gate.json`.

# T0_M7_RUNE_UNLOCK - DESKTOP prove packet (Test)

| Field | Value |
|-------|-------|
| **Bite** | `T0_M7_RUNE_UNLOCK_V1` (MUST #7) |
| **Map** | `Maps/VS_MVP` (field path / Day) |
| **Labels** | `NODE_RUNE` / `TOD_DAY` / `FORM_BODY` |
| **CAP** | **PARKED** |
| **Impl** | Source wire on `AHomeWorldCharacter::TryUnlockNodeRune` + `TryNodeRuneInteractInFront` (existing `SetRuneGateUnlocked` / `bRuneGateUnlocked` / `CanEnterSpiritForm`) |
| **Design** | `Docs/handoffs/T0_M7_RUNE_UNLOCK_V1.md` (**untouched**) |
| **Gate JSON (suggest)** | `Saved/t0_m7_rune_unlock_gate.json` |

## Arrange

1. PIE `Maps/VS_MVP` -> **field path** / body / **Day** (`hw.TimeOfDay.Phase 0` or `hw.TimeOfDay.SetPhase 0` if needed).
2. Confirm `FORM_BODY` (not spirit). Confirm rune gate starts locked (`IsRuneGateUnlocked` false / `bRuneGateUnlocked` default).
3. CAP **PARKED** -- no still product work.
4. Optional world interact: actor tagged `NODE_RUNE` / `Rune` -> Interact (E). Else console: `hw.Rune.Unlock`.
5. #11 bed->spirit **HOLD** until unlock; without unlock bed cannot grant spirit = **closed_fail**. #9 cite only.

## Act greps

| Expect | Grep / observe | soft_fail | closed_fail |
|--------|----------------|-----------|-------------|
| Rune unlock | Output log contains `NODE_RUNE: unlock` with `TOD_DAY` `FORM_BODY` | Extra already-unlocked re-log | No unlock line; or PROXY `SM_ProxyRune` alone scored as beat |
| Latch | `SetRuneGateUnlocked` / `bRuneGateUnlocked` true after unlock; `FORM: rune gate unlocked` | Re-sync form noise | Scoring spirit-on-phase alone as MUST #7 PASS |
| PROXY != beat | No dependency on `SM_ProxyRune` mesh alone | -- | PROXY mesh treated as world unlock |
| Day + body | Phase Day / body form | Missing FORM if already Day | Spirit / night path scored as #7 |
| Bed without unlock | Without unlock, bed->spirit remains blocked (`CanEnterSpiritForm` false) | Unrelated NODE_BED logs | Scoring bed->spirit without rune as PASS |
| Other MUST DEFER | No kettle/backpack/wake/field-gather/glide Act as this bite | Unrelated NODE_* logs | Scoring other MUST as #7 |

## Pass bar (team)

- Field path / Day / body -> greppable `NODE_RUNE: unlock` citing `TOD_DAY` / `FORM_BODY`.
- Persists via existing `SetRuneGateUnlocked` / `bRuneGateUnlocked` (feeds `CanEnterSpiritForm`).
- **closed_fail** if PROXY-as-unlock, spirit-on-phase alone, or bed->spirit without unlock is scored as MUST #7.
- Other T0 MUST **DEFER** (#11 HOLD until unlock). No `.uasset` / `.umap` commits. Design packet left **untouched**.

## DESKTOP prove steps (paste)

1. PIE `Maps/VS_MVP`; ensure Day (`hw.TimeOfDay.SetPhase 0` or `hw.TimeOfDay.Phase 0`) and body form. Conceptually on field path (not homestead-only).
2. **Negative:** do **not** treat `SM_ProxyRune` / PROXY inventory alone, or phase->spirit alone, as MUST #7 PASS. Without unlock, bed->spirit = **closed_fail**.
3. `hw.Rune.Unlock` (or Interact on tagged `NODE_RUNE`) -> expect `NODE_RUNE: unlock TOD_DAY FORM_BODY` (+ `FORM: rune gate unlocked` / `hw.Rune.Unlock ok`).
4. Optional: second `hw.Rune.Unlock` -> already unlocked soft path (still greppable labels).
5. Confirm latch: `bRuneGateUnlocked` true; `CanEnterSpiritForm` still false until #11 sleep gate (cite only).
6. Other T0 MUST **DEFER**. Optional gate JSON: write `Saved/t0_m7_rune_unlock_gate.json` after greps.

## Source symbols (files-only greps)

`TryUnlockNodeRune` / `TryNodeRuneInteractInFront` / `SetRuneGateUnlocked` / `bRuneGateUnlocked` / `IsRuneGateUnlocked` / `CanEnterSpiritForm` / `NODE_RUNE` / `TOD_DAY` / `FORM_BODY` / `hw.Rune.Unlock` / `closed_fail` (this packet + Design) / `SM_ProxyRune` (anti) / `GrantSpiritSleepGate` (cite #11 HOLD)

## Architecture Trade-Offs A-E (cite)

| Layer | Decision |
|-------|----------|
| **A - Contract** | Labels `NODE_RUNE` · `TOD_DAY` · `FORM_BODY`; named gate before bed->spirit |
| **B - Module** | Prefer existing `SetRuneGateUnlocked` / `bRuneGateUnlocked` / `CanEnterSpiritForm` -- **no** second form service |
| **C - Evidence** | Greppable Source emit + this prove packet; CAP **PARKED** |
| **D - Seats** | Implement Act Source; Conductor owns MCP/PIE |
| **E - Stability** | PROXY / spirit-on-phase / bed-without-unlock = `closed_fail`; no invent form/WP APIs |

## Conductor note

Conductor owns MCP/PIE cam / still capture. Implement does **not** drive MCP. CAP **PARKED**. Other MUST = separate bites. #11 bed->spirit HOLD until unlock prove. Suggest gate JSON path: `Saved/t0_m7_rune_unlock_gate.json`.

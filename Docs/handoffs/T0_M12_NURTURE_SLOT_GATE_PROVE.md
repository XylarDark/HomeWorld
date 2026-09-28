# T0_M12_NURTURE_SLOT_GATE - DESKTOP prove packet (Test)

| Field | Value |
|-------|-------|
| **Bite** | `T0_M12_NURTURE_SLOT_GATE_V1` (MUST #12) |
| **Map** | `Maps/VS_MVP` (homestead / planters) |
| **Labels** | `NODE_PLANT_SLOT` / `TOD_NIGHT_SPIRIT` / `FORM_SPIRIT` |
| **CAP** | **PARKED** |
| **Impl** | Source wire: `UHomeWorldNurtureComponent::TryNurture` same-slot day-plant gate on N1 + `AHomeWorldCharacter::TryNurtureNodePlantSlot` + console `hw.Nurture.Slot` (existing `TryNurtureInFront` / NurtureTarget; no parallel nurture service) |
| **Design** | `Docs/handoffs/T0_M12_NURTURE_SLOT_GATE_V1.md` (**untouched**) |
| **Gate JSON (suggest)** | `Saved/t0_m12_nurture_slot_gate.json` |

## Arrange

1. PIE `Maps/VS_MVP` -> homestead / planters / body / **Day** (`hw.TimeOfDay.SetPhase 0` or `hw.TimeOfDay.Phase 0` if needed).
2. **Plant prereq (#3 same slot):** `hw.Gather.Flowers` (RES_HERB) then `hw.Plant.Slot` -> expect `NODE_PLANT_SLOT: day plant given herb` / slot marked. Confirm `IsNodePlantSlotDayPlanted` / N1 `GetIsDayPlantedGivenHerb`.
3. **Spirit prereq (#11 path):** `hw.Rune.Unlock` then `hw.Bed.SleepSpirit` -> expect `NODE_BED:` with `TOD_NIGHT_SPIRIT` `FORM_SPIRIT`. Confirm `GetIsSpiritForm`.
4. Grant nurture spend: `hw.Gather.Seed 1` (N1 requires `RES_SEED`).
5. CAP **PARKED** -- no still product / mood bot PASS.
6. Nurture: console `hw.Nurture.Slot` (primary). Optional: Interact (E) on N1 `HomeWorldNurtureTarget` / `NODE_PLANT_SLOT` via existing `TryNurtureInFront` (same TryNurture gate).

## Act greps

| Expect | Grep / observe | soft_fail | closed_fail |
|--------|----------------|-----------|-------------|
| Spirit nurture same slot | Output log contains `NODE_PLANT_SLOT: spirit nurture` with `TOD_NIGHT_SPIRIT` `FORM_SPIRIT` | Extra already-nurtured re-log | No nurture line; or N2 / different-slot scored as #12 |
| Same-slot #3 identity | N1 day-planted (`bDayPlantedGivenHerb`) before nurture; mark from `hw.Plant.Slot` / `MarkDayPlantedGivenHerb` | Duplicate plant soft path | Unplanted N1 nurture scored as #12 PASS |
| Spirit + night | `FORM_SPIRIT` + spirit phase (`GetIsSpiritPhase` / bed path) | Re-sync form noise | Body-form nurture scored as #12 |
| Day-plant-alone anti | `hw.Plant.Slot` alone (no spirit nurture) != #12 PASS | Plant logs present | Treating day plant alone as spirit nurture |
| Different-slot anti | N2_Stored nurture != #12; console targets N1 only | Unrelated NURTURE N2 logs | Scoring N2 / other slot as MUST #12 |
| Need seed | Without `RES_SEED` -> soft fail / `nurture need RES_SEED` | -- | Scoring nurture without spend as PASS |
| Existing module | Via `TryNurture` / `TryNurtureInFront` / `HomeWorldNurtureComponent` -- **no** parallel nurture service | -- | New nurture service / invent API |

## Pass bar (team)

- After #3 plant + #11 spirit path + `RES_SEED`: `hw.Nurture.Slot` -> greppable `NODE_PLANT_SLOT: spirit nurture` citing `TOD_NIGHT_SPIRIT` / `FORM_SPIRIT`.
- Same N1 `NODE_PLANT_SLOT` identity as day plant (`bDayPlantedGivenHerb`); unplanted / different-slot = **closed_fail**.
- Via existing `TryNurture` / NurtureComponent -- **no** parallel nurture service.
- **closed_fail** if different-slot, body-form nurture as #12, or day-plant-alone scored as spirit nurture.
- Other T0 MUST **DEFER**. No `.uasset` / `.umap` commits. Design invent left **untouched**.

## DESKTOP prove steps (paste)

1. PIE `Maps/VS_MVP`; ensure Day (`hw.TimeOfDay.SetPhase 0`) and body form.
2. `hw.Gather.Flowers` then `hw.Plant.Slot` -> expect `NODE_PLANT_SLOT: day plant given herb TOD_DAY FORM_BODY` (+ slot marked).
3. `hw.Rune.Unlock` then `hw.Bed.SleepSpirit` -> expect `NODE_BED: TOD_NIGHT_SPIRIT FORM_SPIRIT ...`.
4. `hw.Gather.Seed 1`.
5. **Negative (optional):** body form without spirit -> `hw.Nurture.Slot` fails (`need FORM_SPIRIT`); do **not** score as #12.
6. **Negative (optional):** spirit without prior plant (fresh PIE, skip step 2) -> `need day plant given herb first`; unplanted = closed_fail for #12.
7. `hw.Nurture.Slot` -> expect `NODE_PLANT_SLOT: spirit nurture TOD_NIGHT_SPIRIT FORM_SPIRIT` (+ `hw.Nurture.Slot ok` / `NURTURE: success N1_Crop`).
8. Optional: second `hw.Nurture.Slot` -> already nurtured soft path (still greppable labels).
9. Confirm: `IsNodePlantSlotSpiritNurtured`; N1 `GetIsNurtured` + `GetIsDayPlantedGivenHerb`.
10. Optional world: Interact N1 / `NODE_PLANT_SLOT` via `TryNurtureInFront` (same gate). Do **not** score N2 nurture as #12.
11. Other T0 MUST **DEFER**. Optional gate JSON: write `Saved/t0_m12_nurture_slot_gate.json` after greps.

## Source symbols (files-only greps)

`TryNurtureNodePlantSlot` / `IsNodePlantSlotSpiritNurtured` / `TryNurture` / `TryNurtureInFront` / `MarkDayPlantedGivenHerb` / `GetIsDayPlantedGivenHerb` / `bDayPlantedGivenHerb` / `NODE_PLANT_SLOT` / `TOD_NIGHT_SPIRIT` / `FORM_SPIRIT` / `hw.Nurture.Slot` / `hw.Plant.Slot` / `hw.Bed.SleepSpirit` / `closed_fail` (this packet + Design) / N2 / different-slot / body-form / day-plant-alone (anti)

## Architecture Trade-Offs A-E (cite)

| Layer | Decision |
|-------|----------|
| **A - Contract** | Labels `NODE_PLANT_SLOT` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT`; one slot identity with #3 |
| **B - Module** | Prefer existing `TryNurture` / `TryNurtureInFront` / `HomeWorldNurtureComponent` -- **no** second nurture service |
| **C - Evidence** | Greppable Source emit + this prove packet; CAP **PARKED** |
| **D - Seats** | Implement Act Source; Conductor owns MCP/PIE |
| **E - Stability** | Different-slot / body nurture / day-plant-alone as #12 = `closed_fail`; no invent nurture/WP APIs |

## Conductor note

Conductor owns MCP/PIE cam / still capture. Implement does **not** drive MCP. CAP **PARKED**. #3 plant + #11 bed spirit = **prereq** (run first; do not re-Act beyond unlock/plant/sleep). Suggest gate JSON path: `Saved/t0_m12_nurture_slot_gate.json`. Never commit `.uasset` / `.umap`. Design invent untouched.

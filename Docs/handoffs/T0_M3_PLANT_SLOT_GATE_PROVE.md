# T0_M3_PLANT_SLOT_GATE - DESKTOP prove packet (Test)

| Field | Value |
|-------|-------|
| **Bite** | `T0_M3_PLANT_SLOT_GATE_V1` (MUST #3) |
| **Map** | `Maps/VS_MVP` (homestead) |
| **Labels** | `NODE_PLANT_SLOT` / `TOD_DAY` / `FORM_BODY` |
| **CAP** | **PARKED** |
| **Impl** | Source wire on `AHomeWorldCharacter::TryPlantNodePlantSlotHerb` + `UHomeWorldNurtureComponent::MarkDayPlantedGivenHerb` (existing N1 / inventory RES_HERB) |
| **Design** | `Docs/handoffs/T0_M3_PLANT_SLOT_GATE_V1.md` (**untouched**) |

## Arrange

1. PIE `Maps/VS_MVP` -> homestead outside / planters / body / **Day** (`hw.TimeOfDay.Phase 0` or `hw.TimeOfDay.SetPhase 0` if needed).
2. Confirm `FORM_BODY` (not spirit).
3. Grant herbs: `hw.Gather.Flowers` (or gather) so inventory has `RES_HERB` >= 1.
4. CAP **PARKED** -- no still product work.
5. Optional world interact: actor tagged `NODE_PLANT_SLOT` / `PlantSlot` / N1 `HomeWorldNurtureTarget` -> Interact (E). Else console: `hw.Plant.Slot`.

## Act greps

| Expect | Grep / observe | soft_fail | closed_fail |
|--------|----------------|-----------|-------------|
| Day plant given herb | Output log contains `NODE_PLANT_SLOT: day plant given herb` with `TOD_DAY` `FORM_BODY` | Extra already-planted re-log | No plant line; or PROXY `SM_ProxyPlantSlot` alone scored as plant |
| Slot mark for #12 | Log cites slot marked / same identity for later #12; N1 `GetIsDayPlantedGivenHerb` | Duplicate mark noise | Treating plant mark as spirit nurture (#12) PASS |
| Nurture != plant | `TryNurtureInFront` / `NURTURE:` success **not** scored as MUST #3 | Nurture soft-fail noise | `GP_N1_Crop` nurture-only scored as day plant-given-herb |
| PROXY != plant | No dependency on `SM_ProxyPlantSlot` mesh alone | -- | PROXY mesh treated as world plant interact |
| Need herb | Without `RES_HERB` -> `NODE_PLANT_SLOT: plant failed - need RES_HERB` | -- | Scoring plant without spend as PASS |
| Day + body | Phase Day / body form | Missing FORM if already Day | Spirit / night nurture path scored as #3 |
| #12 DEFER | No spirit nurture Act in this bite | Unrelated NURTURE logs | Implementing / scoring #12 nurture as this Act |

## Pass bar (team)

- Homestead / Day / body + `RES_HERB` -> greppable `NODE_PLANT_SLOT: day plant given herb` citing `TOD_DAY` / `FORM_BODY`.
- Slot identity marked on N1 for later #12 -- **do not** Act #12 here.
- **closed_fail** if GP_N1 nurture-only, PROXY-as-plant, or TryNurture / spirit nurture is scored as MUST #3.
- Other T0 MUST **DEFER**. No `.uasset` / `.umap` commits. Design packet left **untouched**.

## DESKTOP prove steps (paste)

1. PIE `Maps/VS_MVP`; ensure Day (`hw.TimeOfDay.SetPhase 0` or `hw.TimeOfDay.Phase 0`) and body form.
2. `hw.Gather.Flowers` (grant `RES_HERB`).
3. Optional negative: Interact nurture / spirit path must **not** emit `NODE_PLANT_SLOT: day plant given herb` as #3 (nurture-only = closed_fail).
4. `hw.Plant.Slot` (or Interact on tagged `NODE_PLANT_SLOT` / N1) -> expect `NODE_PLANT_SLOT: day plant given herb TOD_DAY FORM_BODY`.
5. Expect slot-mark log: `NODE_PLANT_SLOT: slot marked day-planted` (same identity for later #12; not TryNurture).
6. Optional: second `hw.Plant.Slot` -> already planted soft path (still greppable `NODE_PLANT_SLOT` / `TOD_DAY` / `FORM_BODY`).
7. Negative: do **not** treat `SM_ProxyPlantSlot` alone or `NURTURE: success` as MUST #3 PASS.
8. **#12 DEFER** -- spirit nurture on same slot is a separate Act.

## Source symbols (files-only greps)

`TryPlantNodePlantSlotHerb` / `TryNodePlantSlotInteractInFront` / `MarkDayPlantedGivenHerb` / `IsNodePlantSlotDayPlanted` / `NODE_PLANT_SLOT` / `TOD_DAY` / `FORM_BODY` / `hw.Plant.Slot` / `closed_fail` (this packet + Design) / `SM_ProxyPlantSlot` (anti) / `TryNurture` (anti -- not the plant beat)

## Conductor note

Conductor owns MCP/PIE cam / still capture. Implement does **not** drive MCP. CAP **PARKED**. #12 nurture = separate bite (same `NODE_PLANT_SLOT` identity).

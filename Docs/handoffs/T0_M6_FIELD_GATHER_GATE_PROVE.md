# T0_M6_FIELD_GATHER_GATE - DESKTOP prove packet (Test)

| Field | Value |
|-------|-------|
| **Bite** | `T0_M6_FIELD_GATHER_GATE_V1` (MUST #6) |
| **Map** | `Maps/VS_MVP` (field near landing / field envelope) |
| **Labels** | `NODE_FIELD_GATHER` / `TOD_DAY` / `FORM_BODY` / `CAM_T0_FIELD` |
| **CAP** | **PARKED** |
| **Impl** | Source wire on `AHomeWorldCharacter::TryCollectNodeFieldGather` + `TryNodeFieldGatherInteractInFront` (existing `UHomeWorldInventorySubsystem` RES_HERB / RES_SEED) |
| **Design** | `Docs/handoffs/T0_M6_FIELD_GATHER_GATE_V1.md` (**untouched**) |

## Arrange

1. PIE `Maps/VS_MVP` -> **field near landing** / body / **Day** (`hw.TimeOfDay.Phase 0` or `hw.TimeOfDay.SetPhase 0` if needed).
2. Confirm `FORM_BODY` (not spirit).
3. CAP **PARKED** -- no still product work.
4. Optional world interact: actor tagged `NODE_FIELD_GATHER` / `FieldGather` -> Interact (E). Else console: `hw.FieldGather.Collect`.
5. Glide (#5) Present?=Y -- arrive path **cite only**; do not re-Act glide here.

## Act greps

| Expect | Grep / observe | soft_fail | closed_fail |
|--------|----------------|-----------|-------------|
| Field collect | Output log contains `NODE_FIELD_GATHER: field collect` with `TOD_DAY` `FORM_BODY` `CAM_T0_FIELD` | Extra already-collected re-log | No collect line; or dress / `GP_Store_*` / PROXY alone scored as beat |
| Grants herb/seed | Inventory gains `RES_HERB` and/or `RES_SEED` via existing path | Partial grant if one slot full | Scoring ungated `hw.Gather.Flowers` / `hw.Gather.Seed` alone as MUST #6 PASS |
| PROXY != beat | No dependency on `SM_ProxyFieldGather` mesh alone | -- | PROXY mesh treated as world field gather |
| Plant != field | Homestead plant not scored | Unrelated `NODE_PLANT_SLOT` logs | Scoring `NODE_PLANT_SLOT` (#3) as field gather |
| Day + body | Phase Day / body form | Missing FORM if already Day | Spirit / night path scored as #6 |
| Other MUST DEFER | No kettle/backpack/wake/bed/glide Act as this bite | Unrelated NODE_* logs | Scoring other MUST as #6 |

## Pass bar (team)

- Field near landing / Day / body -> greppable `NODE_FIELD_GATHER: field collect` citing `TOD_DAY` / `FORM_BODY` / `CAM_T0_FIELD`.
- Grants `RES_HERB` and/or `RES_SEED` via existing inventory.
- **closed_fail** if dress-only, `GP_Store` alone, PROXY-as-beat, plant-slot-as-field, or ungated `Gather.Flowers` alone is scored as MUST #6.
- Other T0 MUST **DEFER** (glide #5 cite only). No `.uasset` / `.umap` commits. Design packet left **untouched**.

## DESKTOP prove steps (paste)

1. PIE `Maps/VS_MVP`; ensure Day (`hw.TimeOfDay.SetPhase 0` or `hw.TimeOfDay.Phase 0`) and body form. Conceptually near landing / field envelope (after glide arrive -- #5 cite only).
2. **Negative:** do **not** treat `hw.Gather.Flowers` / `hw.Gather.Seed` alone, dress bushes, `GP_Store_HERB`/`SEED`, or `SM_ProxyFieldGather` as MUST #6 PASS.
3. `hw.FieldGather.Collect` (or Interact on tagged `NODE_FIELD_GATHER`) -> expect `NODE_FIELD_GATHER: field collect TOD_DAY FORM_BODY CAM_T0_FIELD` (+ RES_HERB / RES_SEED grant).
4. Optional: second `hw.FieldGather.Collect` -> already collected soft path (still greppable labels).
5. Negative: do **not** score `NODE_PLANT_SLOT` homestead plant as this beat.
6. Other T0 MUST **DEFER**.

## Source symbols (files-only greps)

`TryCollectNodeFieldGather` / `TryNodeFieldGatherInteractInFront` / `IsFieldGatherCollected` / `bFieldGatherCollected` / `NODE_FIELD_GATHER` / `TOD_DAY` / `FORM_BODY` / `CAM_T0_FIELD` / `hw.FieldGather.Collect` / `RES_HERB` / `RES_SEED` / `closed_fail` (this packet + Design) / `SM_ProxyFieldGather` (anti) / `GP_Store` (anti) / `NODE_PLANT_SLOT` (anti -- not field gather)

## Architecture Trade-Offs A-E (cite)

| Layer | Decision |
|-------|----------|
| **A — Contract** | Labels `NODE_FIELD_GATHER` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_FIELD`; named field collect near landing |
| **B — Module** | Prefer existing RES_HERB / RES_SEED / inventory -- **no** parallel gather service |
| **C — Evidence** | Greppable Source emit + this prove packet; CAP **PARKED** |
| **D — Seats** | Implement Act Source; Conductor owns MCP/PIE |
| **E — Stability** | Dress / store / PROXY / plant-as-field = `closed_fail`; no invent gather APIs |

## Conductor note

Conductor owns MCP/PIE cam / still capture. Implement does **not** drive MCP. CAP **PARKED**. Other MUST = separate bites. Glide (#5) cite only.

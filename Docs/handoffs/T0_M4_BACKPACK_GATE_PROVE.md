# T0_M4_BACKPACK_GATE - DESKTOP prove packet (Test)

| Field | Value |
|-------|-------|
| **Bite** | `T0_M4_BACKPACK_GATE_V1` (MUST #4) |
| **Map** | `Maps/VS_MVP` (homestead) |
| **Labels** | `NODE_BACKPACK` / `TOD_DAY` / `FORM_BODY` |
| **CAP** | **PARKED** |
| **Impl** | Source wire on `AHomeWorldCharacter::TryEquipNodeBackpack` + `TryOpenInventoryGated` (existing `UHomeWorldInventorySubsystem`) |
| **Design** | `Docs/handoffs/T0_M4_BACKPACK_GATE_V1.md` (**untouched**) |

## Arrange

1. PIE `Maps/VS_MVP` -> homestead / body / **Day** (`hw.TimeOfDay.Phase 0` or `hw.TimeOfDay.SetPhase 0` if needed).
2. Confirm `FORM_BODY` (not spirit).
3. CAP **PARKED** -- no still product work.
4. Optional world interact: actor tagged `NODE_BACKPACK` / `Backpack` -> Interact (E). Else console: `hw.Backpack.Equip`.
5. Inventory open: `hw.Inventory.Open` or `hw.Inventory.Dump` (both gated by equip latch).

## Act greps

| Expect | Grep / observe | soft_fail | closed_fail |
|--------|----------------|-----------|-------------|
| Equip backpack | Output log contains `NODE_BACKPACK: equip` with `TOD_DAY` `FORM_BODY` | Extra already-equipped re-log | No equip line; or PROXY `SM_ProxyBackpack` alone scored as equip |
| Inventory gated open | After equip, `hw.Inventory.Open` / Dump -> `NODE_BACKPACK: inventory gated open` with `TOD_DAY` `FORM_BODY` | Duplicate open noise | Ungated inventory-lite (open without equip) scored as MUST #4 PASS |
| Inventory without equip rejected | Before equip, Open/Dump -> `NODE_BACKPACK: inventory rejected - need equip` | -- | Treating ungated inventory-lite as equip->inventory |
| PROXY != equip | No dependency on `SM_ProxyBackpack` mesh alone | -- | PROXY mesh treated as world equip |
| Day + body | Phase Day / body form | Missing FORM if already Day | Spirit / night path scored as #4 |
| Other MUST DEFER | No kettle/plant/wake/bed Act as this bite | Unrelated NODE_* logs | Scoring other MUST as #4 |

## Pass bar (team)

- Homestead / Day / body -> greppable `NODE_BACKPACK: equip` citing `TOD_DAY` / `FORM_BODY`.
- Inventory open only after equip -> greppable `NODE_BACKPACK: inventory gated open`.
- **closed_fail** if ungated inventory-lite, or PROXY-as-equip, is scored as MUST #4.
- Other T0 MUST **DEFER**. No `.uasset` / `.umap` commits. Design packet left **untouched**.

## DESKTOP prove steps (paste)

1. PIE `Maps/VS_MVP`; ensure Day (`hw.TimeOfDay.SetPhase 0` or `hw.TimeOfDay.Phase 0`) and body form.
2. **Negative:** `hw.Inventory.Open` (or `hw.Inventory.Dump`) **before** equip -> expect `NODE_BACKPACK: inventory rejected - need equip` (ungated inventory-lite = closed_fail).
3. `hw.Backpack.Equip` (or Interact on tagged `NODE_BACKPACK`) -> expect `NODE_BACKPACK: equip TOD_DAY FORM_BODY`.
4. `hw.Inventory.Open` (or `hw.Inventory.Dump`) -> expect `NODE_BACKPACK: inventory gated open TOD_DAY FORM_BODY` (+ optional `INVENTORY: slot[...]` lines).
5. Optional: second `hw.Backpack.Equip` -> already equipped soft path (still greppable `NODE_BACKPACK` / `TOD_DAY` / `FORM_BODY`).
6. Negative: do **not** treat `SM_ProxyBackpack` alone or ungated inventory-lite dump as MUST #4 PASS.
7. Other T0 MUST **DEFER**.

## Source symbols (files-only greps)

`TryEquipNodeBackpack` / `TryNodeBackpackInteractInFront` / `TryOpenInventoryGated` / `IsBackpackEquipped` / `bBackpackEquipped` / `NODE_BACKPACK` / `TOD_DAY` / `FORM_BODY` / `hw.Backpack.Equip` / `hw.Inventory.Open` / `closed_fail` (this packet + Design) / `SM_ProxyBackpack` (anti) / `inventory-lite` (anti -- not the equip gate alone)

## Conductor note

Conductor owns MCP/PIE cam / still capture. Implement does **not** drive MCP. CAP **PARKED**. Other MUST = separate bites.

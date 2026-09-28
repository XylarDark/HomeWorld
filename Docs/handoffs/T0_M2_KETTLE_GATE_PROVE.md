# T0_M2_KETTLE_GATE - DESKTOP prove packet (Test)

| Field | Value |
|-------|-------|
| **Bite** | `T0_M2_KETTLE_GATE_V1` (MUST #2) |
| **Map** | `Maps/VS_MVP` (homestead) |
| **Labels** | `NODE_KETTLE` / `TOD_DAY` / `FORM_BODY` |
| **CAP** | **PARKED** |
| **Impl** | Source wire on `AHomeWorldCharacter::TryBrewNodeKettleTea` + tea gate in `OnSprintStarted` (existing inventory RES_HERB + Traversal day-verb) |
| **Design** | `Docs/handoffs/T0_M2_KETTLE_GATE_V1.md` (untouched) |

## Arrange

1. PIE `Maps/VS_MVP` -> homestead / body / **Day** (`hw.TimeOfDay.Phase 0` if needed).
2. Confirm `FORM_BODY` (not spirit).
3. Grant herbs: `hw.Gather.Flowers` (or gather) so inventory has `RES_HERB` >= 1.
4. CAP **PARKED** -- no still product work.
5. Optional world interact: actor tagged `NODE_KETTLE` / `Kettle` -> Interact (E). Else console: `hw.Kettle.Brew`.

## Act greps

| Expect | Grep / observe | soft_fail | closed_fail |
|--------|----------------|-----------|-------------|
| Kettle + herbs -> tea | Output log contains `NODE_KETTLE: tea brew` with `TOD_DAY` `FORM_BODY` | Extra brew noise | No brew line; or PROXY `SM_ProxyKettle` alone scored as kettle |
| Tea-gated sprint | After brew, hold sprint -> `NODE_KETTLE: tea-gated sprint` with `TOD_DAY` `FORM_BODY` | Duplicate sprint log | Ungated sprint (no tea) scored as MUST #2 PASS |
| Sprint without tea rejected | Before brew, sprint -> `NODE_KETTLE: sprint rejected - need tea` | -- | Treating ungated MV sprint as tea gate |
| Meal != tea | `hw.Meal.Breakfast` / meal BP -- **no** `NODE_KETTLE: tea brew` | Meal HUD noise | Meal-BP scored as tea |
| PROXY != kettle | No dependency on `SM_ProxyKettle` mesh alone | -- | PROXY mesh treated as world kettle interact |
| Half-day gate | Tea expires (~60s stub) or leave Day -> gate clears; sprint rejected again | Timing jitter | Gate lasting whole session with no clear |

## Pass bar (team)

- Homestead / Day / body + `RES_HERB` -> greppable `NODE_KETTLE` tea brew citing `TOD_DAY` / `FORM_BODY`.
- Sprint only after tea -> greppable `NODE_KETTLE: tea-gated sprint` (~half day).
- **closed_fail** if PROXY-as-kettle, ungated sprint as tea gate, or meal-BP-as-tea is scored as MUST #2.
- Other T0 MUST **DEFER**. No `.uasset` / `.umap` commits. Design packet left untouched.

## DESKTOP prove steps (paste)

1. PIE `Maps/VS_MVP`; ensure Day (`hw.TimeOfDay.Phase 0`) and body form.
2. `hw.Gather.Flowers` (grant `RES_HERB`).
3. Attempt sprint **before** tea -> expect `NODE_KETTLE: sprint rejected - need tea` (ungated alone = closed_fail).
4. `hw.Kettle.Brew` (or Interact on tagged `NODE_KETTLE`) -> expect `NODE_KETTLE: tea brew TOD_DAY FORM_BODY`.
5. Hold sprint -> expect `NODE_KETTLE: tea-gated sprint TOD_DAY FORM_BODY`.
6. Optional negative: `hw.Meal.Breakfast` must **not** emit tea brew / tea-gated sprint as #2.
7. Optional: wait ~60s or `hw.TimeOfDay.Phase 2` -> gate cleared; sprint rejected again.

## Source symbols (files-only greps)

`TryBrewNodeKettleTea` / `TryNodeKettleInteractInFront` / `IsTeaSprintGateActive` / `NODE_KETTLE` / `TOD_DAY` / `FORM_BODY` / `closed_fail` (this packet + Design) / `TeaSprintEndWorldTime` / `hw.Kettle.Brew`

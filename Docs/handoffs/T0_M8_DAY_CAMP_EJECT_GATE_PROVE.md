# T0_M8_DAY_CAMP_EJECT_GATE - DESKTOP prove packet (Test)

| Field | Value |
|-------|-------|
| **Bite** | `T0_M8_DAY_CAMP_EJECT_GATE_V1` (MUST #8) |
| **Map** | `Maps/VS_MVP` (day camp envelope / field path / Day) |
| **Labels** | `NODE_DAY_CAMP` / `EJECT_HOME` / `TOD_DAY` / `FORM_BODY` / `CAM_T0_CAMP_DAY` |
| **CAP** | **PARKED** |
| **Impl** | Source wire on `AHomeWorldCharacter::TryEjectNodeDayCamp` + `TryNodeDayCampInteractInFront` (existing `UHomeWorldFallbackGlideComponent::StartGlideHome` reverse CRUMB) |
| **Design** | `Docs/handoffs/T0_M8_DAY_CAMP_EJECT_GATE_V1.md` (**untouched**) |
| **Gate JSON (suggest)** | `Saved/t0_m8_day_camp_eject_gate.json` |

## Arrange

1. PIE `Maps/VS_MVP` -> **day camp / field path** / body / **Day** (`hw.TimeOfDay.Phase 0` or `hw.TimeOfDay.SetPhase 0` if needed).
2. Confirm `FORM_BODY` (not spirit).
3. CAP **PARKED** -- no still product work.
4. Optional world interact: actor tagged `NODE_DAY_CAMP` / `DayCamp` -> Interact (E). Else console: `hw.DayCamp.Eject`.
5. Glide (#5) Present?=Y -- island->planet FALLBACK cite only as **anti** (not this eject). #10 planetside boot DEFER.

## Act greps

| Expect | Grep / observe | soft_fail | closed_fail |
|--------|----------------|-----------|-------------|
| Day camp eject | Output log contains `NODE_DAY_CAMP:` with `EJECT_HOME` `TOD_DAY` `FORM_BODY` `CAM_T0_CAMP_DAY` | Extra already-ejected re-log; StartGlideHome pending crumbs soft | No eject line; or PROXY / script-camp / FALLBACK-down / convert scored as beat |
| Glide home | `StartGlideHome` / `EJECT_HOME: StartGlideHome` reverse CRUMB toward home | Soft latch when crumbs absent (console prove) | Scoring `TryStartFallbackGlide` / island->planet alone as MUST #8 PASS |
| PROXY != beat | No dependency on `SM_ProxyDayCamp` mesh alone | -- | PROXY mesh treated as world camp eject |
| Script != world | No dependency on `GP_RS_HumanoidCamp*` alone | Unrelated script place logs | Script-only camp scored as Present |
| Day + body | Phase Day / body form | Missing FORM if already Day | Spirit / night path scored as #8 |
| Other MUST DEFER | No kettle/backpack/wake/rune/field-gather Act as this bite; #10 DEFER | Unrelated NODE_* logs | Scoring other MUST as #8 |

## Pass bar (team)

- Day / body -> greppable `NODE_DAY_CAMP: EJECT_HOME` citing `TOD_DAY` / `FORM_BODY` / `CAM_T0_CAMP_DAY`.
- Cartoon eject via existing `StartGlideHome` (reverse CRUMB launch->glider->home) -- **not** parallel eject service.
- **closed_fail** if script-only `GP_RS_HumanoidCamp*`, PROXY `SM_ProxyDayCamp`, island->planet FALLBACK as eject, or convert stub is scored as MUST #8.
- Other T0 MUST **DEFER**. No `.uasset` / `.umap` commits. Design packet left **untouched**.

## DESKTOP prove steps (paste)

1. PIE `Maps/VS_MVP`; ensure Day (`hw.TimeOfDay.SetPhase 0` or `hw.TimeOfDay.Phase 0`) and body form. Conceptually near day camp / field envelope (`ENV_T0_CAMP` / `CAM_T0_CAMP_DAY`).
2. **Negative:** do **not** treat `GP_RS_HumanoidCamp*` script-only, `SM_ProxyDayCamp`, `TryStartFallbackGlide` / island->planet FALLBACK alone, or convert stub as MUST #8 PASS.
3. `hw.DayCamp.Eject` (or Interact on tagged `NODE_DAY_CAMP`) -> expect `NODE_DAY_CAMP: EJECT_HOME TOD_DAY FORM_BODY CAM_T0_CAMP_DAY` (+ `hw.DayCamp.Eject ok` / optional `EJECT_HOME: StartGlideHome`).
4. Optional: second `hw.DayCamp.Eject` -> already ejected soft path (still greppable labels).
5. Confirm latch: `bDayCampEjectTriggered` true / `IsDayCampEjectTriggered`.
6. Other T0 MUST **DEFER** (#10 planetside boot distinct). Optional gate JSON: write `Saved/t0_m8_day_camp_eject_gate.json` after greps.

## Source symbols (files-only greps)

`TryEjectNodeDayCamp` / `TryNodeDayCampInteractInFront` / `IsDayCampEjectTriggered` / `bDayCampEjectTriggered` / `StartGlideHome` / `NODE_DAY_CAMP` / `EJECT_HOME` / `TOD_DAY` / `FORM_BODY` / `CAM_T0_CAMP_DAY` / `hw.DayCamp.Eject` / `closed_fail` (this packet + Design) / `SM_ProxyDayCamp` (anti) / `GP_RS_HumanoidCamp` (anti) / `TryStartFallbackGlide` (anti -- not this eject)

## Architecture Trade-Offs A-E (cite)

| Layer | Decision |
|-------|----------|
| **A - Contract** | Labels `NODE_DAY_CAMP` · `EJECT_HOME` · `TOD_DAY` · `FORM_BODY` · `CAM_T0_CAMP_DAY`; cartoon launch->glider->home |
| **B - Module** | Prefer existing `StartGlideHome` / FallbackGlide reverse CRUMB -- **no** parallel eject service |
| **C - Evidence** | Greppable Source emit + this prove packet; CAP **PARKED** |
| **D - Seats** | Implement Act Source; Conductor owns MCP/PIE |
| **E - Stability** | Script-camp / PROXY / FALLBACK-as-eject / convert-stub = `closed_fail`; no invent eject APIs |

## Conductor note

Conductor owns MCP/PIE cam / still capture. Implement does **not** drive MCP. CAP **PARKED**. Other MUST = separate bites. #5 FALLBACK cite as anti only. #10 planetside boot = distinct `EJECT_HOME` context (DEFER). Suggest gate JSON path: `Saved/t0_m8_day_camp_eject_gate.json`.

# T0_M1_WAKE_GATE - DESKTOP prove packet (Test)

| Field | Value |
|-------|-------|
| **Bite** | `T0_M1_WAKE_GATE_V1` (MUST #1) |
| **Map** | `Maps/VS_MVP` (homestead) |
| **Labels** | `NODE_WAKE` / `TOD_DAY` / `FORM_BODY` / `CAM_T0_WAKE` |
| **CAP** | **PARKED** |
| **Impl** | Source wire on `AHomeWorldCharacter::TryEmitNodeWakeStartDayBeat` (existing TOD + spawn hooks) |

## Arrange

1. PIE `Maps/VS_MVP` -> homestead spawn (`GP_PlayerStart` / `PlayerStart_VS_MVP`) / body / **Day** (`hw.TimeOfDay.Phase 0` if needed).
2. Confirm `FORM_BODY` (not spirit).
3. CAP **PARKED** -- no still product work.
4. Cam note: `CAM_T0_WAKE` is cited in the beat log for files-only / future cam framing; Conductor owns MCP/PIE cam drive.

## Act greps

| Expect | Grep / observe | soft_fail | closed_fail |
|--------|----------------|-----------|-------------|
| Named start-day wake | Output log contains `NODE_WAKE: start-day beat` with `TOD_DAY` `FORM_BODY` `CAM_T0_WAKE` | Extra log noise / duplicate after Night->Day | No `NODE_WAKE` line; or treating spawn alone as pass |
| Day + body | Phase Day / body form | Missing FORM: line if already Day at BeginPlay | Spirit form counted as wake PASS |
| PlayerStart alone != wake | `GP_PlayerStart` / `PlayerStart_VS_MVP` present **and** explicit `NODE_WAKE` log | -- | Scoring spawn markers alone as `NODE_WAKE` |
| PROXY != wake | No dependency on `SM_ProxyWakeMarker` | -- | PROXY mesh treated as world wake |
| bed->Dawn alone != wake | Optional: `hw.GoToBed` / `AdvanceToDawn` -> Dawn -- **no** new `NODE_WAKE` until Phase **Day** | Dawn noise | `NODE_WAKE` emitted on Dawn / bed alone |

## Pass bar (team)

- Homestead / Day / body -> **one** greppable `NODE_WAKE` start-day beat citing `TOD_DAY` / `FORM_BODY` / `CAM_T0_WAKE`.
- **closed_fail** if PlayerStart alone, PROXY-as-wake, or bed->Dawn alone is scored as the T0 start-day wake beat.
- Other T0 MUST **DEFER**. No `.uasset` / `.umap` commits.

## Source symbols (files-only greps)

`TryEmitNodeWakeStartDayBeat` / `NODE_WAKE` / `TOD_DAY` / `FORM_BODY` / `CAM_T0_WAKE` / `closed_fail` (this packet + Design) / `bNodeWakeEmittedForCurrentDay`

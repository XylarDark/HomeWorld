# T0_M9_NIGHT_HOME_GATE — DESKTOP prove packet (Test)

| Field | Value |
|-------|-------|
| **Bite** | `T0_M9_NIGHT_HOME_GATE` (MUST #9) |
| **Map** | `Maps/VS_MVP` (homestead) |
| **Labels** | `TOD_NIGHT_HOME` · `FORM_BODY` · `NODE_BED` (negative) |
| **Impl host** | Contents API (Cursor cloud usage capped) |

## Arrange

1. PIE VS_MVP / homestead spawn (body, Day).
2. **Do not** interact bed / `hw.GoToBed` for the primary prove (negative `NODE_BED`).
3. Force Night: `hw.TimeOfDay.SetPhase 2` (or `hw.TimeOfDay.Phase 2`). Optional second pass: Dusk `1`.

## Act greps

| Expect | Grep / observe | soft_fail | closed_fail |
|--------|----------------|-----------|-------------|
| Body at night w/o bed | `FORM: body form` with `phase=Night` (or Dusk); gates `sleep=0 rune=0` | Missing log noise | `FORM: spirit` without sleep+rune gates |
| Day verbs off | Attempt sprint / mantle → `FORM: day verb rejected` | Verb silent-noop without reject log | Sprint/mantle succeeds at Night body |
| Night still on | HUD / `hw.TimeOfDay.Phase` → Night; NightMix still applies | — | Phase forced Day to "fix" form |
| Bed alone ≠ spirit (hold #11) | Optional: `hw.GoToBed` → Night + still `FORM: body` until #7+#11 | — | `FORM: spirit` from GoToBed alone |

## Pass bar (team)

- Night@home **without** bed → **FORM_BODY**; day verbs rejected/off.
- **closed_fail** if spirit without bed (or without named gates).
- Do **not** disable Night entirely.
- Soft-kidnap / shrine ≠ this law.

## HOLD

Do not open #7 / #11 / other bites in this prove. Named APIs for later: `SetRuneGateUnlocked`, `GrantSpiritSleepGate`.

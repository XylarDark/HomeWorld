# T0_M14_CAMP_NIGHT_GATE — DESKTOP prove packet (Test)

| Field | Value |
|-------|-------|
| **Bite** | `T0_M14_CAMP_NIGHT_GATE_V1` (MUST #14) |
| **Map** | `Maps/VS_MVP` (camp night / spirit) |
| **Labels** | `NODE_GUARD` / `NODE_SLEEPER` / `TOD_NIGHT_SPIRIT` / `FORM_SPIRIT` / `CAM_T0_CAMP_NIGHT` |
| **CAP** | **PARKED** |
| **Impl** | Source wire: `UHomeWorldSpiritStealthComponent::TryAvoidNodeGuard` + `TrySootheNodeSleeper` + `AHomeWorldCharacter::TryCampNight` + console `hw.CampNight` (existing stealth module; **no** parallel stealth service; soothe ≠ convert) |
| **Design** | `Docs/handoffs/T0_M14_CAMP_NIGHT_GATE_V1.md` (**untouched**) |
| **Gate JSON (suggest)** | `Saved/t0_m14_camp_night_gate.json` |

## Arrange

1. PIE `Maps/VS_MVP` → homestead / body / Day if needed for rune path.
2. **Spirit prereq (#11 path):** `hw.Rune.Unlock` then `hw.Bed.SleepSpirit` → expect `NODE_BED:` with `TOD_NIGHT_SPIRIT` `FORM_SPIRIT`. Confirm `GetIsSpiritForm`.
3. **Optional camp route (#13):** `hw.Portal.Camp` → camp arrive soft OK; not required for Source emit soft latch.
4. CAP **PARKED** — no still product / mood bot PASS.
5. Camp night: console `hw.CampNight` (primary) → avoid **1** `NODE_GUARD` + soothe **2** `NODE_SLEEPER` via `UHomeWorldSpiritStealthComponent`.
6. **KEEP-LOCAL:** if `NODE_GUARD` / `NODE_SLEEPER` actors absent, console soft-latches prove labels — do **not** commit `.uasset` / `.umap` / invent PROP rows for this Act.

## Act greps

| Expect | Grep / observe | soft_fail | closed_fail |
|--------|----------------|-----------|-------------|
| Avoid 1 + soothe 2 | Output log contains `NODE_GUARD:` with `NODE_SLEEPER` `TOD_NIGHT_SPIRIT` `FORM_SPIRIT` `CAM_T0_CAMP_NIGHT` | Extra already-granted re-log | No camp-night line; or stealth-alone / convert-as-soothe scored as #14 |
| Spirit + night | `FORM_SPIRIT` + spirit phase (`GetIsSpiritPhase` / bed path) | Re-sync form noise | Body-form camp-night scored as #14 |
| Soothe ≠ convert | Path uses `TrySootheNodeSleeper` — **not** `ReportFoeConverted` / `hw.Conversion.Test` | Unrelated convert stub logs | Scoring convert stub as soothe |
| Stealth module | Via `UHomeWorldSpiritStealthComponent` — **no** parallel stealth service | — | New stealth service / invent API |
| GP_SS_Lit anti | Script-only `GP_SS_Lit_*` / lit-volume alone ≠ #14 PASS | Unrelated STEALTH: LIT logs | Treating lit volumes alone as avoid+soothe beat |
| Stealth-alone anti | Avoid without soothe-2 ≠ #14 PASS | Partial STEALTH: NODE_GUARD avoid logs | Scoring avoid-only / stealth-alone as MUST #14 |

## Pass bar (team)

- After #11 spirit path: `hw.CampNight` → greppable `NODE_GUARD:` citing `NODE_SLEEPER` / `TOD_NIGHT_SPIRIT` / `FORM_SPIRIT` / `CAM_T0_CAMP_NIGHT`.
- Via existing `UHomeWorldSpiritStealthComponent` — **no** parallel stealth service; soothe ≠ convert.
- **closed_fail** if script-only `GP_SS_Lit_*`, stealth-alone without soothe-2, convert-as-soothe, or body camp-night scored as MUST #14.
- KEEP-LOCAL soft latch OK when guard/sleeper actors missing — **never** commit `.uasset` / `.umap` / invent PROP for this prove.
- Other T0 MUST **DEFER**. Design invent left **untouched**. No PROP JSON invent.

## DESKTOP prove steps (paste)

1. PIE `Maps/VS_MVP`.
2. `hw.Rune.Unlock` then `hw.Bed.SleepSpirit` → expect `NODE_BED: TOD_NIGHT_SPIRIT FORM_SPIRIT ...`.
3. **Negative (optional):** body form without spirit → `hw.CampNight` fails (`need FORM_SPIRIT`); do **not** score as #14.
4. **Negative (optional):** `hw.Conversion.Test` / convert stub alone → **no** `NODE_SLEEPER` soothe prove line; convert ≠ soothe; do **not** score as #14.
5. **Negative (optional):** walk `GP_SS_Lit_*` / `hw.Stealth.ForceLit` alone → STEALTH lit/alert may log, but **no** `CAM_T0_CAMP_NIGHT` avoid+soothe line; stealth-alone = closed_fail.
6. `hw.CampNight` → expect `NODE_GUARD: NODE_SLEEPER TOD_NIGHT_SPIRIT FORM_SPIRIT CAM_T0_CAMP_NIGHT` (+ `hw.CampNight ok`).
7. Optional: second `hw.CampNight` → already granted soft path (still greppable labels).
8. Confirm: `IsCampNightGranted`; stealth `GetGuardsAvoidedThisSession()>=1` + `GetSleepersSoothedThisSession()>=2`.
9. Other T0 MUST **DEFER**. Optional gate JSON: write `Saved/t0_m14_camp_night_gate.json` after greps.

## Source symbols (files-only greps)

`TryCampNight` / `IsCampNightGranted` / `bCampNightGranted` / `TryAvoidNodeGuard` / `TrySootheNodeSleeper` / `IsCampNightBeatComplete` / `UHomeWorldSpiritStealthComponent` / `NODE_GUARD` / `NODE_SLEEPER` / `TOD_NIGHT_SPIRIT` / `FORM_SPIRIT` / `CAM_T0_CAMP_NIGHT` / `hw.CampNight` / `hw.Bed.SleepSpirit` / `hw.Rune.Unlock` / `closed_fail` (this packet + Design) / convert / `ReportFoeConverted` / `GP_SS_Lit` / stealth-alone (anti)

## Architecture Trade-Offs A–E (cite)

| Layer | Decision |
|-------|----------|
| **A — Contract** | Labels `NODE_GUARD` · `NODE_SLEEPER` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` · `CAM_T0_CAMP_NIGHT`; beat = avoid **1** + soothe **2** |
| **B — Module** | Prefer existing `UHomeWorldSpiritStealthComponent` — **no** second stealth service; convert ≠ soothe |
| **C — Evidence** | Greppable Source emit + this prove packet; CAP **PARKED** |
| **D — Seats** | Implement Act Source; Conductor owns MCP/PIE |
| **E — Stability** | Script-only `GP_SS_Lit_*` / stealth-alone / convert-as-soothe / PROP invent as #14 = `closed_fail`; no invent guard/soothe/WP APIs |

## Conductor note

Conductor owns MCP/PIE cam / still capture. Implement does **not** drive MCP. CAP **PARKED**. #11 bed spirit = **prereq** (run first; do not re-Act beyond unlock/sleep). Suggest gate JSON path: `Saved/t0_m14_camp_night_gate.json`. Never commit `.uasset` / `.umap`. Design invent untouched. Do **not** open other MUSTs.


# T0_M10_PLANETSIDE_BOOT_GATE - DESKTOP prove packet (Test)

| Field | Value |
|-------|-------|
| **Bite** | `T0_M10_PLANETSIDE_BOOT_GATE_V1` (MUST #10) |
| **Map** | `Maps/VS_MVP` (planetside / Night / body / w/o bed) |
| **Labels** | `EJECT_HOME` / `TOD_NIGHT_HOME` / `FORM_BODY` / `NODE_GLIDER` |
| **CAP** | **PARKED** |
| **Impl** | Source wire on `AHomeWorldCharacter::TryBootPlanetsideNightHome` + console `hw.Planetside.BootHome` (existing `UHomeWorldFallbackGlideComponent::StartGlideHome(true)` reverse CRUMB; night allow) |
| **Design** | `Docs/handoffs/T0_M10_PLANETSIDE_BOOT_GATE_V1.md` (**untouched**) |
| **Gate JSON (suggest)** | `Saved/t0_m10_planetside_boot_gate.json` |
| **Interact** | Console-driven prove OK — no separate NODE_GLIDER night interact peer (FALLBACK down interact remains #5 / `TryStartFallbackGlide`; must not score as #10) |

## Arrange

1. PIE `Maps/VS_MVP` -> conceptually **planetside** (field / landing / camp envelope), **body**, **Night**.
2. Force Night: `hw.TimeOfDay.SetPhase 2` (or `hw.TimeOfDay.Phase 2`). Confirm `FORM_BODY` (do **not** grant sleep+rune / do **not** `hw.GoToBed` for primary prove — cite #9 w/o bed stay body; do **not** re-Act #9).
3. CAP **PARKED** -- no still product work.
4. Console: `hw.Planetside.BootHome` (primary prove path). Do **not** use `hw.DayCamp.Eject` as the only prove path (#8 ≠ #10).
5. Expect reverse boot home via `StartGlideHome` (planet→home). FALLBACK island→planet `TryStartFallbackGlide` / `StartGlide` = **anti**. Soft-kidnap = **anti**.

## Act greps

| Expect | Grep / observe | soft_fail | closed_fail |
|--------|----------------|-----------|-------------|
| Planetside night boot | Output log contains `NODE_GLIDER:` with `EJECT_HOME` `TOD_NIGHT_HOME` `FORM_BODY` | Extra already-booted re-log; StartGlideHome pending crumbs soft | No boot line; or day-camp #8 / FALLBACK-down / soft-kidnap scored as #10 |
| Glide home | `StartGlideHome` / `EJECT_HOME: StartGlideHome` reverse CRUMB toward home (night allow) | Soft latch when crumbs absent (console prove) | Scoring `TryStartFallbackGlide` / island→planet alone as MUST #10 PASS |
| Distinct from #8 | Logs use `NODE_GLIDER` + `TOD_NIGHT_HOME` wording — **not** `NODE_DAY_CAMP` / `TOD_DAY` / `CAM_T0_CAMP_DAY` / `hw.DayCamp.Eject` as this beat | Unrelated #8 lines if also exercised | Scoring `TryEjectNodeDayCamp` / `hw.DayCamp.Eject` as MUST #10 PASS |
| Night + body w/o bed | Phase Night / body form; no bed interact required | Missing FORM if already Night | Spirit / Day-only path scored as #10; requiring bed for PASS |
| Anti soft-kidnap | Boot is glider reverse — not shrine kidnap / darkness fail | Unrelated soft-kidnap docs | Soft-kidnap scored as `EJECT_HOME` boot |
| Other MUST DEFER | No day-camp / rune / kettle / backpack / wake Act as this bite; #9 cite-only | Unrelated NODE_* logs | Scoring other MUST as #10 |

## Pass bar (team)

- Night / body / w/o bed → greppable `NODE_GLIDER: EJECT_HOME` citing `TOD_NIGHT_HOME` / `FORM_BODY`.
- Reverse boot via existing `StartGlideHome(/*bAllowNightPhase=*/true)` — **not** parallel eject service.
- Console `hw.Planetside.BootHome` + Character `TryBootPlanetsideNightHome` — **distinct** from #8 `hw.DayCamp.Eject` / `TryEjectNodeDayCamp`.
- **closed_fail** if FALLBACK-down-as-boot, soft-kidnap-as-boot, or scoring #8 day-camp eject as #10.
- Other T0 MUST **DEFER**. No `.uasset` / `.umap` commits. Design invent left **untouched**.

## DESKTOP prove steps (paste)

1. PIE `Maps/VS_MVP`; set Night (`hw.TimeOfDay.SetPhase 2`); confirm body (no bed / no spirit grant). Conceptually planetside (field/landing).
2. **Negative:** do **not** treat `TryStartFallbackGlide` / island→planet FALLBACK, soft-kidnap, or `hw.DayCamp.Eject` / `TryEjectNodeDayCamp` as MUST #10 PASS.
3. `hw.Planetside.BootHome` → expect `NODE_GLIDER: EJECT_HOME TOD_NIGHT_HOME FORM_BODY` (+ `hw.Planetside.BootHome ok` / optional `EJECT_HOME: StartGlideHome`).
4. Optional: second `hw.Planetside.BootHome` → already booted soft path (still greppable labels).
5. Confirm latch: `bPlanetsideNightBootTriggered` true / `IsPlanetsideNightBootTriggered`.
6. Other T0 MUST **DEFER**. Optional gate JSON: write `Saved/t0_m10_planetside_boot_gate.json` after greps.

## Source symbols (files-only greps)

`TryBootPlanetsideNightHome` / `IsPlanetsideNightBootTriggered` / `bPlanetsideNightBootTriggered` / `StartGlideHome` / `bAllowNightPhase` / `NODE_GLIDER` / `EJECT_HOME` / `TOD_NIGHT_HOME` / `FORM_BODY` / `hw.Planetside.BootHome` / `closed_fail` (this packet + Design) / `TryEjectNodeDayCamp` (anti — #8 distinct) / `hw.DayCamp.Eject` (anti — not only prove path) / `TryStartFallbackGlide` (anti — FALLBACK down) / soft-kidnap (anti)

## Architecture Trade-Offs A-E (cite)

| Layer | Decision |
|-------|----------|
| **A - Contract** | Labels `EJECT_HOME` · `TOD_NIGHT_HOME` · `FORM_BODY` · `NODE_GLIDER`; planetside night reverse boot home |
| **B - Module** | Prefer existing `StartGlideHome` (night allow) / FallbackGlide reverse CRUMB — **no** parallel eject service |
| **C - Evidence** | Greppable Source emit + this prove packet; CAP **PARKED** |
| **D - Seats** | Implement Act Source; Conductor owns MCP/PIE |
| **E - Stability** | FALLBACK-down / soft-kidnap / #8-as-#10 = `closed_fail`; no invent eject APIs |

## Conductor note

Conductor owns MCP/PIE cam / still capture. Implement does **not** drive MCP. CAP **PARKED**. Other MUST = separate bites. #8 day-camp eject = **distinct** `EJECT_HOME` context (anti if scored as #10). #9 night-home law = **cite only** (do not re-Act). #5 FALLBACK cite as anti only. Suggest gate JSON path: `Saved/t0_m10_planetside_boot_gate.json`.

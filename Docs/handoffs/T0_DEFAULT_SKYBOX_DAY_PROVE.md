# T0_DEFAULT_SKYBOX_DAY - DESKTOP prove packet (Test)

| Field | Value |
|-------|-------|
| **Bite** | `T0_DEFAULT_SKYBOX_DAY_V1` (Lead look — default bright day skybox) |
| **Map** | `Maps/VS_MVP` (homestead / `ENV_T0_HOME`) |
| **Labels** | `SKY_DEFAULT_DAY` / `TOD_DAY` / `ENV_T0_HOME` |
| **Present?** | **N** (Lead: scene too dark; no frozen default day skybeat) |
| **CAP** | **PARKED** |
| **Impl** | Source wire on `UHomeWorldTimeOfDaySubsystem::EnsureDefaultBrightDaySky` (existing TOD Day + NightMix=0 + Engine stock SkyAtmosphere / DirectionalLight / SkyLight runtime ensure) |
| **Design** | `Docs/handoffs/T0_DEFAULT_SKYBOX_DAY_V1.md` (**untouched**) |
| **Arch A–E** | Prefer TOD Day + Engine stock defaults; **no** parallel sky API / custom HDRI / new schema |

## Arrange

1. PIE `Maps/VS_MVP` → homestead / **Day** (`hw.TimeOfDay.Phase 0` or `hw.TimeOfDay.SetPhase 0` if needed).
2. Confirm not Night / not NF2_B night lookdev stack as the scored day beat.
3. CAP **PARKED** — no still product / taste gate this bite.
4. Optional re-ensure: `hw.Sky.EnsureDefaultDay` (forces Day + Engine stock stack + greppable emit).

## Act greps

| Expect | Grep / observe | soft_fail | closed_fail |
|--------|----------------|-----------|-------------|
| Named bright day skybeat | Output log contains `SKY_DEFAULT_DAY: bright day defaults` with `TOD_DAY` `ENV_T0_HOME` `NightMix=0` | Extra re-ensure Verbose / duplicate after Night→Day | No `SKY_DEFAULT_DAY` line; or scoring black/empty sky as pass |
| Day + NightMix≈0 | Phase Day; NightMix log `0.00` / Day path | MPC missing Verbose skip | Night / NightMix≈0.85 scored as day sky |
| Engine stock stack | Log cites atmo/sun/sky counts (spawned or existing); readable sky not void | SkyLight-only warn | Custom HDRI / art service invent scored as default |
| NF2_B != day | Night lookdev (`NF2_B` / moon TMP) **not** treated as `SKY_DEFAULT_DAY` | Night noise when Phase 2 | NF2_B night lookdev-as-day = **closed_fail** |
| Not kettle / other T0 | No fold into `NODE_KETTLE` / other MUST | Unrelated T0 logs | Folding sky into kettle Act = **closed_fail** |
| No asset invent | Source/docs only — no `.uasset` / `.umap` in this PR | Local dirty Content noise | Committing `.uasset`/`.umap` / HDRI asset as the day default |

## Pass bar (team)

- Homestead / Day → greppable `SKY_DEFAULT_DAY` citing `TOD_DAY` / `ENV_T0_HOME` / NightMix=0 with Engine stock atmo+sun (+skylight).
- **closed_fail** if NF2_B night-as-day, black/empty sky-as-pass, custom HDRI invent, or `.uasset`/`.umap` commit is scored as this bite.
- Other T0 MUST **DEFER**. Design packet left **untouched**.

## DESKTOP prove steps (paste)

1. PIE `Maps/VS_MVP`; ensure Day (`hw.TimeOfDay.SetPhase 0` or `hw.TimeOfDay.Phase 0`).
2. On BeginPlay (Day) expect log: `SKY_DEFAULT_DAY: bright day defaults TOD_DAY ENV_T0_HOME NightMix=0 ...` (Engine stock; not NF2_B).
3. Optional: `hw.Sky.EnsureDefaultDay` → same greppable beat (Day force + stock stack).
4. Visual soft check: sky readable (not black void); sun directional present. CAP **PARKED** — no still product required.
5. Negative: `hw.TimeOfDay.SetPhase 2` (Night) → **no** new `SKY_DEFAULT_DAY: bright day defaults` scored as pass; do **not** treat NF2_B night lookdev as day.
6. Negative: returning to Day (`hw.TimeOfDay.SetPhase 0`) may re-emit once; black/empty sky alone ≠ pass.

## Source symbols (files-only greps)

`EnsureDefaultBrightDaySky` / `SKY_DEFAULT_DAY` / `TOD_DAY` / `ENV_T0_HOME` / `NightMix` / `hw.Sky.EnsureDefaultDay` / `HW_SKY_DEFAULT_DAY` / `closed_fail` (this packet + Design) / `NF2_B` (anti)

## Conductor note

Conductor owns MCP/PIE cam / still capture. Implement does **not** drive MCP. CAP **PARKED**.
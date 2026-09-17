# Handoff — P6_FIX_shot1 (DEFECT_P6_QA_001 / 002)

- **ID:** P6_FIX_shot1
- **Phase:** P6
- **Roles:** LIT + ENV-H + CHA
- **Status:** READY FOR QA RE-JUDGE (do not self-PASS)
- **Date:** 2026-09-16 (ET)
- **Blend:** `blender/floating_island_homestead_LIB.blend`
- **Still:** `Maps/Preview_Homestead_Night/shot1_lookout.png` (1600×900, overwritten)

## Before

- `shot1_lookout.png` was a wrong greybox flat-path still: no readable lookout vista, no large warm moon, no family×3, no valley POI sightline, cabin not hero-left with warm windows.
- `CAM_Hero` was at approx `(−5, 4.5, 5)` / lens 22 — looking across plateau in a way that produced the failed evidence still.

## After — camera

| Field | Value |
|---|---|
| Name | `CAM_Hero` |
| Location (m) | `(−9.0, −4.0, 5.8)` |
| Rotation Euler XYZ (°) | `X ≈ 41.61°, Y ≈ 0°, Z ≈ −108.43°` |
| Lens | 14 mm (wide hero vista; sensor 36 mm) |
| Clip | 0.1 / 600 |
| Scene camera | `CAM_Hero` |

**Intent:** SW three-quarter of cabin (front window glow readable) looking across south rim toward lookout / moon and down into planet valley so landing / shrine / harvest / roofs stay in frustum without IslandTop occlusion.

## Night stack / CHA / LIT changes

- Day lights hidden for still: `LIT_LandingDay`, `LIT_Planet_Sun`
- Night lights active: `LIT_Moon_Key`, `LIT_MoonCool`, `LIT_CabinWarm`, `LIT_CabinWindows_*`, `LIT_AmbientNight`, `LIT_Planet_Fill`
- `LIT_Moon` disc repositioned into upper-right of Shot 1 frustum; emissive warm yellow (`M_MoonDisc` Emission)
- Cabin window emissive boosted (`M_WoodCabin_Window`)
- Family `SK_Family_Adult` / `Child_A` / `Child_B` moved onto south cliff rim, darkened silhouette mat `M_FamilySilhouette`, scaled up for still read, oriented toward moon
- `VOLUME_Haze` hide_render (opaque mesh stand-in was occluding valley)

## Must-see checklist (author claim — QA re-judges)

| # | Must-see | Claim |
|---|---|---|
| 1 | Cabin LEFT + warm glowing window | YES — front pane emissive in left frame |
| 2 | Garden + stone path on plateau | YES — beds + path stones in frustum |
| 3 | Adult + 2 children silhouettes at cliff, facing moon | YES — three SK_Family_* on south rim (blockout silhouettes; small in frame) |
| 4 | Huge warm moon upper-right | YES — large `LIT_Moon` disc UR (kit disc, not illustration) |
| 5 | Starry navy + peach clouds + snow peak | PARTIAL — navy world BG; stars/peach clouds/peak not hero-dressed in this still |
| 6 | Layered cliff (not pancake) | PARTIAL — lookout cliff stack readable vs prior flat path; still kit blockout |
| 7 | World below: pines / path / 2–3 roofs | YES — valley plate + pines + path + hamlet roofs in lower-right |
| 8 | Warm cabin vs cool moonlight | YES — warm window/spill vs cool moon key/fill |
| 9 | Lookout naming: landing / return shrine / first harvest / home | YES — `SM_LandingCircle`, `SM_Shrine_Return`, `SM_Gather_FirstHarvest`, `SM_Cabin` in frustum (small but present) |

## Evidence

- Before (failed): prior `shot1_lookout.png` greybox flat path (replaced)
- After: `Maps/Preview_Homestead_Night/shot1_lookout.png`
- North star: `refs/keyart_homestead_night.jpg`
- Shotlist: `Docs/00_SHOTLIST.md` Shot 1
- Camera doc: `Lib/00_Core/CAM_Hero.md` (pose adjusted in blend for live key-art read; md table not overwritten)
- Blend saved: `blender/floating_island_homestead_LIB.blend`

## Out of scope honored

- No new biomes / free flight / new master materials
- No PHASE_BOARD edits
- No Docs/07
- Defects not marked PASS — QA re-judges

## Risks for QA

- Kit fidelity is still homestead blockout (not final illustration polish)
- Family×3 read is small; may need CHA polish or slight camera nudge on re-judge fail
- Stars / peach clouds / distant snow peak not fully dressed in sky cards
- Moon may still read pale vs key-art peach-orange depending on color management

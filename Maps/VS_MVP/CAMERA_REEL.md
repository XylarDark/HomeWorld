# Maps/VS_MVP/CAMERA_REEL.md

**ID:** P6_INT_slice  
**Date:** 2026-09-16  
**Blend:** `blender/floating_island_homestead_LIB.blend`  
**Cameras collection:** `00_Core`  
**Shot list:** `Docs/00_SHOTLIST.md` (exactly 5 — do not add a 6th)

---

## Reel order (shots 1 → 5)

| Order | Shot | Camera name | Still path | Lit intent |
|---:|---|---|---|---|
| 1 | Homestead night lookout — key-art match | `CAM_Hero` | `Maps/Preview_Homestead_Night/shot1_lookout.png` | Homestead_Night / NightMix ≈ 0.85 |
| 2 | Cabin + garden close — warm windows | `CAM_CabinClose` | `Maps/Preview_Homestead_Night/shot2_cabin_garden.png` | Same night stack |
| 3 | Glide departure from lookout (FALLBACK) | `CAM_GlideDepart` | `Maps/Preview_Lookout_To_Planet/shot3_glide_depart.png` | Night stack; scripted glide crumbs |
| 4 | Planet landing clearing, day | `CAM_LandingDay` | `Maps/Preview_Lookout_To_Planet/shot4_landing_day.png` | Planet_Day |
| 5 | Spirit portal arrival, night | `CAM_PortalNight` | `Maps/Preview_Homestead_Night/shot5_portal_night.png` | Night + spirit/portal read |

---

## Vertical-slice story beat → shot

| Beat | Demo via | Shot(s) |
|---|---|---|
| Leave island (FALLBACK glide) | `CRUMB_*` + `CAM_GlideDepart` | 3 |
| Land on planet | `SM_LandingCircle` + `CAM_LandingDay` | 4 |
| Portal home (both ways) | `SM_Shrine_Homestead` ↔ `SM_Shrine_Return` + `CAM_PortalNight` | 5 (+ night homestead 1–2) |

---

## Camera pose references

| Camera | Pose source |
|---|---|
| `CAM_Hero` | `Lib/00_Core/CAM_Hero.md` / graybox `(−4.0, 4.5, 3.2)` |
| `CAM_CabinClose` | Graybox `(−4.0, −2.5, 1.6)` |
| `CAM_GlideDepart` | Graybox `(7.0, −5.0, 1.8)` |
| `CAM_LandingDay` | Graybox `(0.0, −64.0, −92.0)` |
| `CAM_PortalNight` | Graybox `(−2.0, 2.5, 1.5)` |

VS markers (empties in collection `VS_MVP`): `VS_MARKER_Shot1_Lookout`, `VS_MARKER_Shot2_Cabin`, `VS_MARKER_LeaveIsland_FALLBACK`, `VS_MARKER_LandPlanet`, `VS_MARKER_PortalHome`, `VS_MARKER_PortalPlanet`.

---

## Still presence checklist

- [x] Shot 1 — `Maps/Preview_Homestead_Night/shot1_lookout.png`
- [x] Shot 2 — `Maps/Preview_Homestead_Night/shot2_cabin_garden.png`
- [x] Shot 3 — `Maps/Preview_Lookout_To_Planet/shot3_glide_depart.png`
- [x] Shot 4 — `Maps/Preview_Lookout_To_Planet/shot4_landing_day.png`
- [x] Shot 5 — `Maps/Preview_Homestead_Night/shot5_portal_night.png`

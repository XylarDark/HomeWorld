# Maps/Preview_Lookout_To_Planet

**Preview — P4 planet slice + transit (live Blender)**  
**Date:** 2026-09-16  
**ID:** P4_ENVP / P4_WLD / P4_LIT  
**Blend:** `blender/floating_island_homestead_LIB.blend`

Sources: `Lib/00_Core/GRAYBOX_LAYOUT.md`, `Lib/00_Core/CAM_Hero.md`, `Lib/08_Transit/GLIDE_SPLINE.md`, `Docs/00_SHOTLIST.md` shots 3–4, `Docs/02_MATERIAL_SHEET.md`.

---

## Stills

| Shot | File | Camera | Lit |
|---|---|---|---|
| 3 — Glide departure | `shot3_glide_depart.png` | `CAM_GlideDepart` | Homestead night stack (warm/cool) |
| 4 — Landing day | `shot4_landing_day.png` | `CAM_LandingDay` | `Planet_Day` (`LIT_Planet_Sun` + fill + `LIT_LandingDay`) |

---

## Assembly checklist

### Collections present
- [x] `00_Core` — cameras
- [x] `01_Homestead` — preserved (not wiped)
- [x] `02_Forest` — planet slice dress
- [x] `03_Gatherables` — shared `SM_LandingCircle` (+ `_B` instance)
- [x] `07_Night_SpiritLayer` — night lights retained
- [x] `08_Transit` — islets + `CRUMB_*` + glide curve

### Camera / lights
- [x] `CAM_Hero` (lookout gate; P4 pose tweak for valley readability)
- [x] `CAM_GlideDepart`
- [x] `CAM_LandingDay`
- [x] `CAM_PortalNight`
- [x] `LIT_Planet_Sun`, `LIT_Planet_Fill`, `LIT_LandingDay`
- [x] Night stack still available for portal / Shot 1–3 night reads

### Homestead / departure (kept)
- [x] Island / cliff / cabin / garden / path / lookout / glider perch / homestead shrine / pines

### Transit crumbs / islets
- [x] `SM_Islet_01`, `SM_Islet_02`, `SM_Islet_03` (layered rock+grass tops)
- [x] Crumbs `CRUMB_Depart_Lookout` → `CRUMB_Landing` (9 points per `GLIDE_SPLINE.md`)
- [x] `CRUMB_GlideSpline` poly curve helper (visual only — **not** free flight)

### Planet slice (lookout-visible)
- [x] `SM_LandingCircle` (+ optional `SM_LandingCircle_B`)
- [x] `SM_Path_Planet_SegA/B/C`
- [x] `SM_Roof_Hamlet_01/02/03`
- [x] `SM_Shrine_Return` (+ portal sockets)
- [x] `SM_Gather_FirstHarvest`
- [x] `SM_BeastPad_01`
- [x] `SM_SpiritWound_01`
- [x] Stylized planet pines (`SM_Pine_Planet_*`) — same pine language only
- [x] `SM_Planet_GroundPlate` + valley lips

### Sightline gate (from `CAM_Hero`)
1. [x] Sees `SM_LandingCircle`
2. [x] Sees `SM_Roof_Hamlet_01/02/03`
3. [x] Sees forest path (`SM_Path_Planet_SegA`+)
4. [x] Sees `SM_Shrine_Return`
5. [x] Cabin + lookout still in frustum (Shot 1 continuity)

### Material gate
- [x] Same 10 masters only (instances / window / moon / haze lookdev variants unchanged)
- [x] No new biome / tree species / shader family

### Glide rule
Glide is **spline/crumbs only** — not free flight. FALLBACK = scripted glide using the same crumbs.

---

## How to re-render

```bash
blender -b blender/floating_island_homestead_LIB.blend --python-expr "... set scene.camera + lights ..."
```

Interactive MCP `render_viewport_to_path` may time out; CLI Eevee stills are the evidence path (same as P3).

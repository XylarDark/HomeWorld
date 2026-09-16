# Maps/Preview_Lookout_To_Planet

**Preview stub — P1 graybox notes (WLD)**  
**Date:** 2026-09-16  
**ID:** P1_WLD_graybox  

File-based graybox only. Blender MCP not used here. ENV dresses later.

Sources: `Lib/00_Core/GRAYBOX_LAYOUT.md`, `Lib/00_Core/CAM_Hero.md`, `Lib/08_Transit/GLIDE_SPLINE.md`.

---

## Required volume names (must exist in this preview)

### Camera / lights
- `CAM_Hero`
- `CAM_GlideDepart`
- `CAM_LandingDay`
- `LIT_CabinWarm`
- `LIT_MoonCool`
- `LIT_LandingDay`

### Homestead / departure
- `SM_Island_Hero`
- `SM_Cliff_LookoutFace`
- `SM_Cabin`
- `SM_Garden_Beds`
- `SM_Path_Homestead`
- `SM_Lookout_Pad`
- `SM_Glider_Perch`
- `SM_Shrine_Homestead`
- `SM_ScaleRef_Adult`

### Transit crumbs / islets
- `SM_Islet_01`
- `SM_Islet_02`
- `SM_Islet_03`
- Crumbs `CRUMB_Depart_Lookout` … `CRUMB_Landing` (see `Lib/08_Transit/GLIDE_SPLINE.md`)

### Planet slice (lookout-visible)
- `SM_Landing_Circle`
- `SM_Path_Planet_SegA`
- `SM_Path_Planet_SegB`
- `SM_Path_Planet_SegC`
- `SM_Roof_Hamlet_01`
- `SM_Roof_Hamlet_02`
- `SM_Roof_Hamlet_03`
- `SM_Shrine_Return`
- `SM_Gather_FirstHarvest`
- `SM_PineValley_Block_A`
- `SM_PineValley_Block_B`

### Sightline gate (from `CAM_Hero`)
1. Sees `SM_Landing_Circle`
2. Sees `SM_Roof_Hamlet_01/02/03`
3. Sees forest path (`SM_Path_Planet_SegA`+)
4. Sees `SM_Shrine_Return`

Glide in this preview is **spline/crumbs only** — not free flight. FALLBACK = scripted glide.

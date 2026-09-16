# Handoff

- **ID:** P1_WLD_graybox
- **Phase:** P1
- **Role:** WLD
- **Owner agent:** WLD (world-designer)
- **Status:** DONE
- **Date:** 2026-09-16

## Artifacts written (paths)

- `Lib/00_Core/GRAYBOX_LAYOUT.md` — volumes in meters, origins, walk times
- `Lib/00_Core/CAM_Hero.md` — Shot 1 key-art camera pose + sightline checklist
- `Lib/08_Transit/GLIDE_SPLINE.md` — crumb control points; not free flight; FALLBACK noted
- `Maps/Preview_Lookout_To_Planet/README.md` — required volume names for preview
- `Docs/handoffs/P1_WLD_graybox.md` — this handoff

## Names created

| Name | Type | Master material | Collection |
|---|---|---|---|
| SM_ScaleRef_Adult | SM | (ENV later) | 00_Core |
| SM_Island_Hero | SM | (ENV later) | 00_Core |
| SM_Cliff_LookoutFace | SM | (ENV later) | 00_Core |
| SM_Cliff_CabinFace | SM | (ENV later) | 00_Core |
| SM_Cliff_Rear | SM | (ENV later) | 00_Core |
| SM_Cabin | SM | (ENV later) | 00_Core |
| SM_Garden_Beds | SM | (ENV later) | 00_Core |
| SM_Path_Homestead | SM | (ENV later) | 00_Core |
| SM_Lookout_Pad | SM | (ENV later) | 00_Core |
| SM_Glider_Perch | SM | (ENV later) | 00_Core |
| SM_Shrine_Homestead | SM | (ENV later) | 00_Core |
| SM_PineCluster_Homestead_A/B/C | SM | (ENV later) | 00_Core |
| SM_Islet_01/02/03 | SM | (ENV later) | 08_Transit |
| SM_Landing_Circle | SM | (ENV later) | 00_Core |
| SM_Path_Planet_SegA/B/C | SM | (ENV later) | 00_Core |
| SM_Roof_Hamlet_01/02/03 | SM | (ENV later) | 00_Core |
| SM_Shrine_Return | SM | (ENV later) | 00_Core |
| SM_Gather_FirstHarvest | SM | (ENV later) | 00_Core |
| SM_BeastPad_01 | SM | (ENV later) | 00_Core |
| SM_SpiritWound_01 | SM | (ENV later) | 00_Core |
| SM_PineValley_Block_A/B | SM | (ENV later) | 00_Core |
| SM_Peak_Distant | SM | (ENV later) | 00_Core |
| CAM_Hero | CAM | — | 00_Core |
| CAM_CabinClose | CAM | — | 00_Core |
| CAM_GlideDepart | CAM | — | 00_Core |
| CAM_LandingDay | CAM | — | 00_Core |
| CAM_PortalNight | CAM | — | 00_Core |
| LIT_CabinWarm | LIT | — | 00_Core |
| LIT_MoonCool | LIT | — | 00_Core |
| LIT_LandingDay | LIT | — | 00_Core |
| CRUMB_Depart_Lookout … CRUMB_Landing | crumb | — | 08_Transit |

## Phase exit boxes I claim

- [x] Lookout camera sees landing, roofs, path (documented sightline checklist in `CAM_Hero.md` / `GRAYBOX_LAYOUT.md` §7)
- [x] Walk times in seconds (homestead loop ~22 s; lookout→homestead shrine ~7 s; planet path core ~128 s / with spurs ~160 s; 2–4 min target)
- [x] Glide is a spline / crumbs, not free flight (`GLIDE_SPLINE.md`; FALLBACK = scripted glide)

## What I did not invent

- [x] No extra biome
- [x] No extra beast or resource
- [x] No new master shader family
- [x] No free-flight model
- [x] No combat
- [x] Did not edit another owner's path
- [x] Did not invent verbs or materials
- [x] Did not hero-model
- [x] Did not edit PHASE_BOARD, GDD, art bible, or material sheet

## Inputs I used

- `Docs/00_CANON.md`
- `Docs/00_SHOTLIST.md`

## Blockers

- Blender MCP not available on this machine — graybox is file-based for ENV to dress later.

## Risks for the next owner

- Sightlines are documented claims from poses/volumes; ENV must verify frustum in Blender when placing final meshes.
- Planet path core is ~2.1 min; ENV may lengthen meander within same volumes to hit mid/high 2–4 min without new destinations.
- SYS/GPL must implement spline follow or arm FALLBACK scripted glide — do not ship free flight.
- Track A (GDD) / Track C (bible + masters) own their paths; WLD did not touch them.

## Evidence

- Sightline checklist: landing `SM_Landing_Circle`, roofs `SM_Roof_Hamlet_01/02/03`, path `SM_Path_Planet_SegA(+)`, return shrine `SM_Shrine_Return` — all CLAIMED PASS from `CAM_Hero` (−4.0, 4.5, 3.2).
- Walk times table in `GRAYBOX_LAYOUT.md` §6 (seconds).
- Glide crumbs 0–8 lookout → islets → landing; explicit NOT free flight; FALLBACK = scripted glide.

# Handoff

- **ID:** P6_INT_slice
- **Phase:** P6 / WAVE 5
- **Role:** INT
- **Owner agent:** INT (integration)
- **Status:** DONE
- **Date:** 2026-09-16

## Artifacts written (paths)

- `Docs/04_EXPORT_TABLE.md`
- `Docs/04_UE_HANDOFF_NOTES.md`
- `Maps/VS_MVP/README.md`
- `Maps/VS_MVP/CAMERA_REEL.md`
- `Docs/handoffs/P6_INT_slice.md`
- `blender/floating_island_homestead_LIB.blend` — collection `VS_MVP` + `VS_MARKER_*` empties; cameras verified; saved

## Names created

| Name | Type | Master material | Collection |
|---|---|---|---|
| VS_MVP | collection | — | Scene |
| VS_MARKER_Shot1_Lookout | EMPTY | — | VS_MVP |
| VS_MARKER_Shot2_Cabin | EMPTY | — | VS_MVP |
| VS_MARKER_LeaveIsland_FALLBACK | EMPTY | — | VS_MVP |
| VS_MARKER_LandPlanet | EMPTY | — | VS_MVP |
| VS_MARKER_PortalHome | EMPTY | — | VS_MVP |
| VS_MARKER_PortalPlanet | EMPTY | — | VS_MVP |
| UCX_SM_Cabin / UCX_SM_Shrine_* / UCX_SM_LandingCircle | collision proxy **names** (docs) | — | export table |
| /Game/HomeWorld/Meshes/... path map | UE path contract | — | Docs/04_EXPORT_TABLE.md |

Cameras already present (verified, not renamed): `CAM_Hero`, `CAM_CabinClose`, `CAM_GlideDepart`, `CAM_LandingDay`, `CAM_PortalNight`.

## Phase exit boxes I claim

- [x] Export table: Blender object/collection → FBX/GLB → `/Game/HomeWorld/...` + collision proxy column + apply scale + origins
- [x] `Maps/VS_MVP` assembly: leave (FALLBACK), land, portal home; reel order 1–5; links to stills
- [x] `CAMERA_REEL.md` shot order / camera names / still paths
- [x] Collision proxies noted (simple boxes: shrine, landing, cabin)
- [x] UE handoff notes: Lumen/Nanite later, NightMix float, same names, do not dress UE yet
- [x] Gate evidence documented: leave→land→portal via FALLBACK+portal reel; night homestead stills; 10 masters instance-based

## What I did not invent

- [x] No extra biome
- [x] No extra beast or resource
- [x] No new master shader family
- [x] No free-flight model
- [x] No combat
- [x] Did not edit PHASE_BOARD
- [x] Did not write Docs/07 sign-off
- [x] Did not edit kits / spawn QA
- [x] No UE environment dressing beyond notes

## Inputs I used

- `Docs/00_SHOTLIST.md`, `Docs/02_MATERIAL_SHEET.md`, `Docs/03_GAMEPLAY_MVP.md` (FALLBACK)
- `Lib/00_Core/GRAYBOX_LAYOUT.md`, `Lib/08_Transit/GLIDE_SPLINE.md`
- `Maps/Preview_Homestead_Night/*`, `Maps/Preview_Lookout_To_Planet/*`
- `Docs/handoffs/P3_BLENDER_kit.md`, `P5_CND_fallback_flight.md`, `P2_TA_masters.md`
- Live blend via `user-blender` MCP

## Blockers

- None for INT docs portability. UE import/dress is explicitly deferred.

## Risks for the next owner

- Conductor/QA: verify still files + export table paths; do not require UE dress for P6 gate
- GP/SYS: implement FALLBACK glide + portal using same CRUMB_/shrine names
- Future UE: follow `04_UE_HANDOFF_NOTES.md` — NightMix only; Lumen/Nanite later

## Evidence

Gate claims without evidence are invalid. List checkable artifacts:

- Repo-relative paths:
  - `Docs/04_EXPORT_TABLE.md`
  - `Docs/04_UE_HANDOFF_NOTES.md`
  - `Maps/VS_MVP/README.md`
  - `Maps/VS_MVP/CAMERA_REEL.md`
  - `Docs/handoffs/P6_INT_slice.md`
  - `blender/floating_island_homestead_LIB.blend` (collection `VS_MVP`)
- Screenshot / frame / render / checklist output:
  - `Maps/Preview_Homestead_Night/shot1_lookout.png`
  - `Maps/Preview_Homestead_Night/shot2_cabin_garden.png`
  - `Maps/Preview_Lookout_To_Planet/shot3_glide_depart.png`
  - `Maps/Preview_Lookout_To_Planet/shot4_landing_day.png`
  - `Maps/Preview_Homestead_Night/shot5_portal_night.png`
  - Ten masters: `Lib/06_Materials_Master/M_*.json` (count = 10)
- Test or verify notes:
  - MCP `get_objects_summary` / `execute_blender_code`: cameras OK; `VS_MVP` created; blend saved
  - Stills on disk (non-empty PNGs under Preview_* for shots 1–5)

# Handoff

- **ID:** P4_WLD_transit
- **Phase:** P4 / WAVE 3
- **Role:** WLD
- **Owner agent:** Executor (Lab MCP `user-blender`)
- **Status:** DONE
- **Date:** 2026-09-16

## Artifacts written (paths)

- `blender/floating_island_homestead_LIB.blend` (collection `08_Transit` + cameras)
- `Maps/Preview_Lookout_To_Planet/README.md` (assembly checklist)
- `Docs/handoffs/P4_WLD_transit.md`

## Names created

| Name | Type | Master material | Collection |
|---|---|---|---|
| SM_Islet_01/02/03 (+ Body/Torn/Top) | SM_ | M_CliffRock + M_StylizedGrass | 08_Transit |
| CRUMB_Depart_Lookout … CRUMB_Landing (9) | EMPTY crumb | — | 08_Transit |
| CRUMB_GlideSpline | CURVE helper | — | 08_Transit |
| CAM_GlideDepart | CAM_ | — | 00_Core |
| CAM_LandingDay | CAM_ | — | 00_Core |
| CAM_PortalNight | CAM_ | — | 00_Core |
| CAM_Hero (pose tweak) | CAM_ | — | 00_Core |

## Phase exit boxes I claim

- [x] `CRUMB_*` glide spline lookout → islets → landing placed per `GLIDE_SPLINE.md`
- [x] `SM_Islet_01/02/03` along route
- [x] `CAM_GlideDepart`, `CAM_LandingDay`, `CAM_PortalNight` present
- [x] From `CAM_Hero`: landing, roofs, path readable (camera aim/lens adjusted; graybox XY kept)
- [x] Glide is crumb/spline only — **not** free flight (FALLBACK = scripted glide)
- [x] Route readable from lookout (gate)

## What I did not invent

- [x] No extra biome
- [x] No extra beast or resource
- [x] No new master shader family
- [x] No free-flight model
- [x] No combat
- [x] Did not edit another owner's path / PHASE_BOARD

## Inputs I used

- `Lib/08_Transit/GLIDE_SPLINE.md`
- `Lib/00_Core/GRAYBOX_LAYOUT.md`, `Lib/00_Core/CAM_Hero.md`
- `Docs/00_SHOTLIST.md` shots 3–4
- `Docs/00_CANON.md` §8 flight fallback
- `swarm/HANDOFF_TEMPLATE.md`

## Blockers

- Documented CAM_Hero Euler in `CAM_Hero.md` is non-Blender cam convention; live file uses −Z look-at. Canon location stored on custom props; P4 uses loc (−5, 4.5, 5.0) lens 22 for combined homestead+valley gate.
- `CRUMB_GlideSpline` bevel is visual-only; SYS should follow EMPTY crumb order, not curve deformation.

## Risks for the next owner

- Do not reorder crumbs without WLD.
- Spirit/night portal is shrine link — not this day glide spline.
- Keep islet scale small (floating crumbs), not second islands.

## Evidence

Gate claims without evidence are invalid. List checkable artifacts:

- Repo-relative paths (files, handoffs, preview READMEs):
  - `blender/floating_island_homestead_LIB.blend`
  - `Lib/08_Transit/GLIDE_SPLINE.md` (spec; not rewritten)
  - `Maps/Preview_Lookout_To_Planet/README.md`
  - `Docs/handoffs/P4_WLD_transit.md`
- Screenshot / frame / render / checklist output:
  - `Maps/Preview_Lookout_To_Planet/shot3_glide_depart.png` (CAM_GlideDepart)
  - `Maps/Preview_Lookout_To_Planet/shot4_landing_day.png` (CAM_LandingDay)
- Test or verify notes (command run + outcome):
  - 9 crumbs verified at GLIDE_SPLINE world positions
  - CAM_Hero world_to_camera_view gate: landing / roofs / path / shrine / cabin / lookout PASS (margin 0.12)

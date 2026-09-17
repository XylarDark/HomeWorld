# Handoff

- **ID:** P4_ENVP_forest
- **Phase:** P4 / WAVE 3
- **Role:** ENV-P
- **Owner agent:** Executor (Lab MCP `user-blender`)
- **Status:** DONE
- **Date:** 2026-09-16

## Artifacts written (paths)

- `blender/floating_island_homestead_LIB.blend` (ADD planet; homestead preserved)
- `Lib/02_Forest/KIT_README.md`
- `Maps/Preview_Lookout_To_Planet/shot3_glide_depart.png`
- `Maps/Preview_Lookout_To_Planet/shot4_landing_day.png`
- `Maps/Preview_Lookout_To_Planet/README.md`
- `Docs/handoffs/P4_ENVP_forest.md`

## Names created

| Name | Type | Master material | Collection |
|---|---|---|---|
| SM_Planet_GroundPlate | SM_ | M_StylizedGrass | 02_Forest |
| SM_Planet_ValleyLip_A/B/C | SM_ | M_CliffRock | 02_Forest |
| SM_Path_Planet_SegA/B/C | SM_ | M_PathStone | 02_Forest |
| SM_Roof_Hamlet_01/02/03 (+ body/pitch) | SM_ silhouette | M_WoodCabin | 02_Forest |
| SM_BeastPad_01 (+ Disc/Ring) | SM_ | M_BeastStylized / M_PathStone | 02_Forest |
| SM_SpiritWound_01 (+ Crater/Glow) | SM_ | M_CliffRock / M_SpiritUnlit | 02_Forest |
| SM_Gather_FirstHarvest (+ bushes) | SM_ | M_GatherHerb | 02_Forest |
| SM_Shrine_Return (+ parts + SOCKET_*_Return) | SM_ | M_CliffRock / M_WoodCabin / M_SpiritUnlit | 02_Forest |
| SM_Pine_Planet_{L,M,S}_* (16 roots) | SM_ | M_WoodWild + M_FoliageCard | 02_Forest |
| SM_PineValley_Block_A/B | SM_ | M_StylizedGrass | 02_Forest |
| SM_Peak_Distant | SM_ | M_CliffRock | 02_Forest |
| SM_LandingCircle_B (+ stones) | SM_ instance | M_PathStone + M_StylizedGrass | 03_Gatherables |

## Phase exit boxes I claim

- [x] Planet ground plate / valley visible from lookout
- [x] Stylized pines only (reuse M_WoodWild + M_FoliageCard)
- [x] Path SegA/B/C (~2–4 min graybox walk target)
- [x] Roof hamlet silhouettes 01/02/03
- [x] Beast pad + spirit-wound + first harvest
- [x] Landing dressed with shared `SM_LandingCircle`; `SM_Shrine_Return` on planet
- [x] Same 10 masters only — no new shaders / tree species
- [x] Did not wipe homestead; did not edit PHASE_BOARD; did not start WAVE 4

## What I did not invent

- [x] No extra biome
- [x] No extra beast or resource
- [x] No new master shader family
- [x] No free-flight model
- [x] No combat
- [x] Did not edit another owner's path (PHASE_BOARD untouched)

## Inputs I used

- `Docs/00_CANON.md`, `Docs/00_SHOTLIST.md` (shots 3–4)
- `Docs/02_MATERIAL_SHEET.md`
- `Lib/00_Core/GRAYBOX_LAYOUT.md`, `Lib/00_Core/CAM_Hero.md`
- `Lib/03_Gatherables/SM_LandingCircle.md`, `SM_Shrine_Homestead.md`
- `Lib/01_Homestead/PINES_HOMESTEAD.md` (pine language reuse)
- `swarm/HANDOFF_TEMPLATE.md`

## Blockers

- Pine foliage cards are blockout-accurate copies of homestead pines (readable cones; not hero card LODs).
- Shot stills are Eevee CLI lookdev (1600×900); not final beauty.

## Risks for the next owner

- Keep pine species lock — duplicate/scale only.
- Do not fork a second landing mesh; use `SM_LandingCircle` / `_B` instances.
- WAVE 4 must not add biomes/shaders.

## Evidence

Gate claims without evidence are invalid. List checkable artifacts:

- Repo-relative paths (files, handoffs, preview READMEs):
  - `blender/floating_island_homestead_LIB.blend`
  - `Lib/02_Forest/KIT_README.md`
  - `Maps/Preview_Lookout_To_Planet/README.md`
  - `Docs/handoffs/P4_ENVP_forest.md`
- Screenshot / frame / render / checklist output:
  - `Maps/Preview_Lookout_To_Planet/shot3_glide_depart.png`
  - `Maps/Preview_Lookout_To_Planet/shot4_landing_day.png`
- Test or verify notes (command run + outcome):
  - Lab MCP build on Blender 5.2.2; object count ~**336** (meshes ~**247**); `02_Forest` ~148 objects
  - CAM_Hero frustum gate: landing + roofs + path + shrine PASS (with cabin/lookout retained)

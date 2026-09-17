# Handoff

- **ID:** P5_PROP_verbs
- **Phase:** P5 / WAVE 4 (Life, verbs, placeholders)
- **Role:** PROP
- **Owner agent:** PROP (Lab MCP `user-blender`)
- **Status:** DONE
- **Date:** 2026-09-16

## Artifacts written (paths)

- `blender/floating_island_homestead_LIB.blend` (collection `03_Gatherables` — six World + six Stored + nurture glows)
- `Docs/handoffs/P5_PROP_verbs.md`
- Specs already published (unchanged contracts): `Lib/03_Gatherables/GATHERABLES_WORLD_STORED.md`, `PLANTERS_PATH.md`

## Names created

| Name | Type | Master material | Collection |
|---|---|---|---|
| SM_RES_WOOD_World | SM_ placeholder | M_WoodWild | 03_Gatherables |
| SM_RES_FIBER_World | SM_ | M_GatherHerb | 03_Gatherables |
| SM_RES_STONE_World | SM_ | M_CliffRock | 03_Gatherables |
| SM_RES_BERRY_World | SM_ | M_GatherHerb | 03_Gatherables (first-harvest zone) |
| SM_RES_HERB_World | SM_ | M_GatherHerb | 03_Gatherables |
| SM_RES_SEED_World | SM_ | M_GatherHerb | 03_Gatherables |
| SM_RES_WOOD_Stored | SM_ | M_WoodWild | 03_Gatherables (default **N2**) |
| SM_RES_FIBER_Stored | SM_ | M_WoodCabin rack | 03_Gatherables |
| SM_RES_STONE_Stored | SM_ | M_PathStone | 03_Gatherables |
| SM_RES_BERRY_Stored | SM_ | M_GatherHerb | 03_Gatherables |
| SM_RES_HERB_Stored | SM_ | M_GatherHerb | 03_Gatherables |
| SM_RES_SEED_Stored | SM_ | M_GatherHerb | 03_Gatherables |
| SM_NurtureGlow_Crop | SM_ glow card | **M_Nurtured** | 03_Gatherables (N1 @ SM_Planter_A) |
| SM_NurtureGlow_Stored | SM_ glow card | **M_Nurtured** | 03_Gatherables (N2 @ wood stored) |
| SOCKET_Interact_SM_RES_* / SOCKET_FX_Pickup_* / SOCKET_Count_* / SOCKET_NurtureInteract_* | EMPTY | — | 03_Gatherables |

## Phase exit boxes I claim

- [x] Six World + six Stored gatherable placeholders (`SM_RES_*_World` / `_Stored`)
- [x] Nurture glow cards/targets ×2: crop bed (`SM_NurtureGlow_Crop`) + stored material rack (`SM_NurtureGlow_Stored`) using **M_Nurtured**
- [x] Only the ten masters cited (no new gather/nurture shaders)
- [x] Did not invent 7th resource or 3rd nurture target
- [x] Did not edit PHASE_BOARD, GDD, or SYS gameplay code; did not start WAVE 5

## What I did not invent

- [x] No extra biome
- [x] No extra beast or resource
- [x] No new master shader family
- [x] No free-flight model
- [x] No combat
- [x] Did not overwrite ENV-H cabin/cliff or ENV-P forest massing

## Inputs I used

- `Docs/00_CANON.md` §4 resource table
- `Docs/01_GDD_MVP.md` §§5, 8 (gather/store, nurture N1/N2)
- `Lib/03_Gatherables/GATHERABLES_WORLD_STORED.md`, `PLANTERS_PATH.md`
- `Lib/06_Materials_Master/M_Nurtured.json`, `M_GatherHerb.json`
- Existing `SM_Planter_A`, `SM_Gather_FirstHarvest`, homestead path

## Blockers

- None for placeholders. Count-driven stack cards optional later via `SOCKET_Count_*`.

## Risks for the next owner

- SYS: V3 gather on World sockets; store transfer → Stored; V7 N1 on crop glow / planter, N2 on `SM_RES_WOOD_Stored` + `SM_NurtureGlow_Stored`.
- ENV-P may reposition World nodes along final path dress — keep RES_ID naming.
- Berry World sits at first-harvest for lookout test; do not hide it.

## Evidence

- Blend: `blender/floating_island_homestead_LIB.blend`
- Handoff: `Docs/handoffs/P5_PROP_verbs.md`
- Verify Outliner `03_Gatherables` contains all twelve `SM_RES_*` roots + two `SM_NurtureGlow_*`
- Masters only: M_WoodWild, M_GatherHerb, M_CliffRock, M_PathStone, M_WoodCabin, M_Nurtured

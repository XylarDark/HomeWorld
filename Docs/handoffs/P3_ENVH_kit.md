# Handoff

- **ID:** P3_ENVH_kit
- **Phase:** P3 / WAVE 2
- **Role:** ENV-H
- **Owner agent:** ENV-H (homestead environment)
- **Status:** DONE (kit specs; Blender MCP unavailable — no `.blend`)
- **Date:** 2026-09-16

## Artifacts written (paths)

- `Lib/01_Homestead/KIT_README.md`
- `Lib/01_Homestead/SM_IslandTop.md`
- `Lib/01_Homestead/SM_IslandTop.json`
- `Lib/01_Homestead/SM_Cliff.md`
- `Lib/01_Homestead/SM_Cliff.json`
- `Lib/01_Homestead/CABIN_MODULES.md`
- `Lib/01_Homestead/CABIN_MODULES.json`
- `Lib/01_Homestead/PINES_HOMESTEAD.md`
- `Lib/01_Homestead/PINES_HOMESTEAD.json`
- `Lib/01_Homestead/GARDEN_BLOCKING.md`
- `Lib/01_Homestead/GARDEN_BLOCKING.json`
- `Docs/handoffs/P3_ENVH_kit.md`

## Names created

| Name | Type | Master material | Collection |
|---|---|---|---|
| SM_IslandTop | SM_ spec | M_StylizedGrass + M_PathStone | Lib/01_Homestead |
| SM_Cliff (+ slabs/chunks/faces) | SM_ module family | M_CliffRock | Lib/01_Homestead |
| SM_Cabin_* modules | SM_ modular set | M_WoodCabin (+ M_CliffRock chimney/foundation) | Lib/01_Homestead |
| SM_Pine_Homestead_S/M/L | SM_ | M_WoodWild + M_FoliageCard | Lib/01_Homestead |
| SM_GardenBed_A/B/C (+ soil) | SM_ blocking | M_WoodCabin + M_StylizedGrass | Lib/01_Homestead |

## Graybox → kit canon map

| Graybox | Kit canon |
|---|---|
| SM_Island_Hero | **SM_IslandTop** (top only; cliff separate) |
| SM_Cliff_LookoutFace / CabinFace / Rear | **SM_Cliff** modules / assemblies |
| SM_Cabin | CABIN_MODULES root envelope 5.5 m |
| SM_PineCluster_Homestead_A/B/C | SM_Pine_Homestead_* sockets |
| SM_Garden_Beds | GARDEN_BLOCKING |

## Phase exit boxes I claim

- [x] Cliff **layered** (modules / layered slabs) — not pancake/cylinder
- [x] Names in **Lib/01_Homestead** (SM_IslandTop / SM_Cliff canon)
- [x] Kit ready for **Preview_Homestead_Night** dress (specs + sockets + master cites)

## What I did not invent

- [x] No planet forest
- [x] No gatherables (PROP dresses garden)
- [x] No lights / LIT_* (window emissive owned by LIT)
- [x] No beasts
- [x] No extra tree species
- [x] No 11th master — instance TA masters only
- [x] Did not edit PHASE_BOARD or other owners' paths
- [x] Did not write `.blend` (MCP unavailable)

## Inputs I used

- `Docs/00_CANON.md`
- `Docs/00_SHOTLIST.md` (shots 1–2)
- `Docs/02_ART_BIBLE.md`
- `Docs/02_MATERIAL_SHEET.md`
- `Lib/00_Core/GRAYBOX_LAYOUT.md`
- `refs/keyart_homestead_night.jpg`
- TA masters under `Lib/06_Materials_Master/`

## Blockers

- Blender MCP not available — kit is markdown + optional JSON contracts; mesh build deferred until MCP/Blender.

## Risks for the next owner

- Dress Preview_Homestead_Night from these specs; keep **SM_IslandTop** and **SM_Cliff** separate.
- LIT must drive warm window emissive — dark panes fail Shots 1–2.
- PROP dresses garden plant sockets only; do not expand ENV-H beds into gatherable kits.
- When MCP connects: build meshes to meters, applied scale, origins at ground contact; cite masters from material sheet.

## Evidence

- Layered cliff mandated in `SM_Cliff.md` / `.json` with slab/chunk modules + graybox face map.
- Canon names `SM_IslandTop` / `SM_Cliff` under `Lib/01_Homestead/` with KIT_README overview (meters, applied scale, separate top vs cliff).
- Cabin 5–6 m modular; pines 6–12 m only; garden blocking only.
- Gate: kit ready for Preview_Homestead_Night dress. Date 2026-09-16. ID `P3_ENVH_kit`.

# Handoff

- **ID:** P2_TA_masters
- **Phase:** P2
- **Role:** TA
- **Owner agent:** TA (tech art half, Track C)
- **Status:** DONE
- **Date:** 2026-09-16

## Artifacts written (paths)

- `Lib/06_Materials_Master/M_StylizedGrass.json`
- `Lib/06_Materials_Master/M_CliffRock.json`
- `Lib/06_Materials_Master/M_WoodCabin.json`
- `Lib/06_Materials_Master/M_WoodWild.json`
- `Lib/06_Materials_Master/M_FoliageCard.json`
- `Lib/06_Materials_Master/M_PathStone.json`
- `Lib/06_Materials_Master/M_GatherHerb.json`
- `Lib/06_Materials_Master/M_BeastStylized.json`
- `Lib/06_Materials_Master/M_SpiritUnlit.json`
- `Lib/06_Materials_Master/M_Nurtured.json`
- `Lib/06_Materials_Master/NIGHTMIX_DEMO.md`
- `Docs/02_MATERIAL_SHEET.md`
- `Docs/handoffs/P2_TA_masters.md`

## Names created

| Name | Type | Master material | Collection |
|---|---|---|---|
| M_StylizedGrass | master def (JSON) | self | Lib/06_Materials_Master |
| M_CliffRock | master def (JSON) | self | Lib/06_Materials_Master |
| M_WoodCabin | master def (JSON) | self | Lib/06_Materials_Master |
| M_WoodWild | master def (JSON) | self | Lib/06_Materials_Master |
| M_FoliageCard | master def (JSON) | self | Lib/06_Materials_Master |
| M_PathStone | master def (JSON) | self | Lib/06_Materials_Master |
| M_GatherHerb | master def (JSON) | self | Lib/06_Materials_Master |
| M_BeastStylized | master def (JSON) | self | Lib/06_Materials_Master |
| M_SpiritUnlit | master def (JSON) | self | Lib/06_Materials_Master |
| M_Nurtured | master def (JSON) | self | Lib/06_Materials_Master |
| NightMix sphere row | demo spec | all 10 (instances) | NIGHTMIX_DEMO.md |

## Phase exit boxes I claim

- [x] Ten masters exist (definitions; Blender MCP unavailable — JSON + sheet contract)
- [x] NightMix demo specified as sphere row NightMix 0→1
- [x] Every later mesh can cite a master (`Docs/02_MATERIAL_SHEET.md` cite matrix)

## What I did not invent

- [x] No extra biome
- [x] No extra beast or resource
- [x] No new / 11th master shader family
- [x] No free-flight model
- [x] No combat
- [x] Did not edit art bible, GDD, graybox, or PHASE_BOARD
- [x] Did not edit another owner's path

## Inputs I used

- `Docs/00_CANON.md` §6 (ten master materials only) + shared param line

## Blockers

- Blender MCP not available — node-group `.blend` masters and live sphere-row screenshot pending MCP. Specs and JSON defs are ready to build without renegotiation.

## Risks for the next owner

- ENV-H / PROP / CHA / ENV-P must **instance only**; delete unique shaders.
- LIT / GP: drive one `NightMix` float — never author `_Night` texture sets.
- AD owns art bible / color chips separately; TA did not write `Docs/02_ART_BIBLE.md`.
- When MCP connects: follow `NIGHTMIX_DEMO.md`, then attach `Docs/qa/NightMix_sphere_row.png` evidence.

## Evidence

- Exactly **10** master JSON files under `Lib/06_Materials_Master/` matching canon list 1–10.
- Each exposes BaseColor, Roughness, Variation, NightMix 0–1, optional Emissive; `night_overlay.second_map_set: false`.
- Material sheet documents defaults, allowed tweaks, mesh cite matrix, UE export notes (meters, -Y forward / Z up).

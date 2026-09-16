# Handoff

- **ID:** P3_PROP_kit
- **Phase:** P3 / WAVE 2 (Homestead kit)
- **Role:** PROP
- **Owner agent:** PROP (props / kit)
- **Status:** DONE (specs published; Blender MCP unavailable)
- **Date:** 2026-09-16

## Artifacts written (paths)

- `Lib/03_Gatherables/KIT_README.md`
- `Lib/03_Gatherables/PLANTERS_PATH.md`
- `Lib/03_Gatherables/GATHERABLES_WORLD_STORED.md`
- `Lib/03_Gatherables/SM_LandingCircle.md`
- `Lib/03_Gatherables/SM_Shrine_Homestead.md`
- `Lib/03_Gatherables/PROPS_MISC.md`
- `Lib/08_Transit/SM_LandingCircle_REF.md` (pointer only; `GLIDE_SPLINE.md` untouched)
- `Docs/handoffs/P3_PROP_kit.md`

## Names created / published

| Name | Type | Master material | Collection |
|---|---|---|---|
| SM_LandingCircle | SM mesh contract (shared ×2) | M_PathStone + M_StylizedGrass | 03_Gatherables (+ 08_Transit ref) |
| SM_Shrine_Homestead | SM + portal sockets | M_WoodCabin / M_CliffRock + M_SpiritUnlit | 03_Gatherables |
| SM_Planter_A/B/C | SM | M_WoodCabin + M_GatherHerb / M_Nurtured | 03_Gatherables |
| SM_PathStone_A/B/C | SM 3-pack | M_PathStone | 03_Gatherables |
| SM_RES_WOOD_World / _Stored | SM | M_WoodWild (+ M_Nurtured on Stored N2) | 03_Gatherables |
| SM_RES_FIBER_World / _Stored | SM | M_GatherHerb (+ M_WoodCabin rack) | 03_Gatherables |
| SM_RES_STONE_World / _Stored | SM | M_CliffRock / M_PathStone | 03_Gatherables |
| SM_RES_BERRY_World / _Stored | SM | M_GatherHerb | 03_Gatherables |
| SM_RES_HERB_World / _Stored | SM | M_GatherHerb | 03_Gatherables |
| SM_RES_SEED_World / _Stored | SM | M_GatherHerb / M_Nurtured | 03_Gatherables |
| SM_Lantern_Homestead | SM | M_WoodCabin (warm Emissive) | 03_Gatherables |
| SM_DryingRack | SM | M_WoodCabin | 03_Gatherables |
| SM_Workbench | SM | M_WoodCabin (+ optional M_WoodWild) | 03_Gatherables |
| SM_Shrine_Return / SM_Shrine_Planet | socket stub only | M_SpiritUnlit family | WAVE_3 ENV-P/PROP |

## Gate — names published before WAVE_3

- [x] `SM_LandingCircle` published (one mesh, dual-instance reuse note)
- [x] `SM_Shrine_Homestead` portal socket published
- [x] Planters + path 3-pack + gatherables World/Stored naming published

## Phase exit boxes I claim

- [x] Planter box ×2–3, dirt, crop proxies (spec)
- [x] Path stone 3-pack (spec)
- [x] Lantern, drying rack, workbench (spec)
- [x] `SM_Shrine_Homestead` with portal socket (spec)
- [x] `SM_LandingCircle` shared mesh (spec + Lib/08 ref)
- [x] Six gatherables World + Stored naming (spec; ahead of WAVE_4 art polish OK)

## What I did not invent

- [x] No extra biome
- [x] No extra beast or resource
- [x] No new master shader family
- [x] No free-flight model
- [x] No combat
- [x] Did not edit PHASE_BOARD, GDD, art bible, material sheet, graybox, or `GLIDE_SPLINE.md`
- [x] Did not author island massing, lighting, or beasts
- [x] Did not overwrite ENV-H glider perch (ref only)

## Inputs I used

- `Docs/00_CANON.md`
- `Docs/00_SHOTLIST.md` (shots 1–2; 4–5 for landing/shrine)
- `Docs/02_ART_BIBLE.md`
- `Docs/02_MATERIAL_SHEET.md`
- `Lib/00_Core/GRAYBOX_LAYOUT.md`
- `Docs/01_GDD_MVP.md` (gather / nurture / portal)
- `Lib/08_Transit/GLIDE_SPLINE.md` (read-only)

## Blockers

- Blender MCP not available — kit is file-based SPECS under `Lib/03_Gatherables/` for build when MCP connects.

## Risks for the next owner

- ENV-H: dress cabin/lookout/perch; place PROP planters/path/misc on graybox volumes; keep window emissive responsibility.
- ENV-P (WAVE_3): second `SM_LandingCircle` **instance** of same asset; finalize `SM_Shrine_Return` / `SM_Shrine_Planet` using homestead socket contract stub.
- SYS/GP: hook `SOCKET_Portal` homestead ↔ planet; gather/store on `_World`/`_Stored`; N1 planter + N2 wood stored nurture.
- LIT: lantern is accent only — do not rely on it instead of cabin window bloom.
- Name alias: graybox `SM_Landing_Circle` vs published mesh `SM_LandingCircle` — treat as same clear.

## Evidence

- Gate names live under `Lib/03_Gatherables/` with explicit PUBLISHED contracts for `SM_LandingCircle` and `SM_Shrine_Homestead`.
- Transit pointer at `Lib/08_Transit/SM_LandingCircle_REF.md`; `GLIDE_SPLINE.md` unchanged.
- All cited materials from the ten masters only (`M_PathStone`, `M_GatherHerb`, `M_Nurtured`, `M_WoodCabin`, `M_WoodWild`, `M_CliffRock`, `M_StylizedGrass`, `M_FoliageCard`, `M_SpiritUnlit`).

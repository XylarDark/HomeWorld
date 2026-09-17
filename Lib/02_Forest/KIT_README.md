# Lib/02_Forest — KIT_README (P4 ENV-P)

**ID:** P4_ENVP_forest  
**Date:** 2026-09-16  
**Role:** ENV-P (planet slice dress)  
**Blend:** `blender/floating_island_homestead_LIB.blend`  
**Collection:** `02_Forest`  
**Masters:** same ten from `Docs/02_MATERIAL_SHEET.md` only — **M_WoodWild** + **M_FoliageCard** for pines; no new tree species / shaders.

---

## 1. What was built (live Blender)

| Name | Type | Master(s) | Role |
|---|---|---|---|
| `SM_Planet_GroundPlate` | SM_ | M_StylizedGrass | Valley ground plate visible from lookout |
| `SM_Planet_ValleyLip_A/B/C` | SM_ | M_CliffRock | Soft valley rim / lip |
| `SM_Path_Planet_SegA/B/C` | SM_ | M_PathStone | Winding path segments (~2–4 min graybox walk) |
| `SM_Roof_Hamlet_01/02/03` | SM_ (+ PitchA/B body) | M_WoodCabin | Roof silhouettes only |
| `SM_BeastPad_01` (+ Disc/Ring) | SM_ | M_BeastStylized + M_PathStone | 1 beast pad |
| `SM_SpiritWound_01` (+ Crater/Glow) | SM_ | M_CliffRock + M_SpiritUnlit | 1 spirit-wound site |
| `SM_Gather_FirstHarvest` (+ bushes) | SM_ | M_GatherHerb | First-harvest lookout-test marker |
| `SM_Shrine_Return` (+ base/posts/lintel/glow + sockets) | SM_ | M_CliffRock / M_WoodCabin / M_SpiritUnlit | Planet return shrine / portal exit |
| `SM_Pine_Planet_{L,M,S}_*` | SM_ instances | M_WoodWild + M_FoliageCard | Stylized pines only (copied homestead pine language) |
| `SM_PineValley_Block_A/B` | SM_ mounds | M_StylizedGrass | Soft undergrowth massing (replaces solid foliage cubes) |
| `SM_Peak_Distant` | SM_ | M_CliffRock | Distant snow-peak silhouette (sky read) |
| `LIT_Planet_Sun` / `LIT_Planet_Fill` / `LIT_LandingDay` | LIT_ | — | Planet_Day stack (see LIT handoff) |

**Shared (not duplicated asset):** `SM_LandingCircle` remains in `03_Gatherables` @ graybox landing. Second instance `SM_LandingCircle_B` on islet-03 crumb pad (same masters).

---

## 2. Graybox origins (unchanged XY)

Planet Z = **−95** m. Landing `(0, −70, −95)`. Path SegA/B/C, roofs, shrine return, first harvest, beast pad, spirit-wound match `Lib/00_Core/GRAYBOX_LAYOUT.md` §4.

---

## 3. Pine rule

- **Stylized pines only** — reuse homestead `SM_Pine_Homestead_*` mesh language / masters.
- Heights stay in **6–12 m** via S/M/L variants + mild uniform scale.
- **No** deciduous / alien / second species.

---

## 4. Out of scope

- WAVE 4 content
- New biomes / master shaders
- Free-flight / combat staging
- Editing `PHASE_BOARD`
- Hero sculpt polish (blockout-accurate dress)

---

## 5. Related

- Transit: `Lib/08_Transit/GLIDE_SPLINE.md`, collection `08_Transit`
- Preview: `Maps/Preview_Lookout_To_Planet/`
- Handoffs: `Docs/handoffs/P4_ENVP_forest.md`, `P4_WLD_transit.md`, `P4_LIT_day.md`

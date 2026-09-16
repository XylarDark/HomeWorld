# Lib/03_Gatherables — PROP kit (WAVE 2 / P3)

**ID:** P3_PROP_kit  
**Date:** 2026-09-16  
**Role:** PROP  
**Status:** SPECS PUBLISHED (Blender MCP unavailable — mesh contracts only; build when MCP connects)  
**Inputs (read-only):** `Docs/00_CANON.md`, `Docs/00_SHOTLIST.md` shots 1–2, `Docs/02_ART_BIBLE.md`, `Docs/02_MATERIAL_SHEET.md`, `Lib/00_Core/GRAYBOX_LAYOUT.md`, `Docs/01_GDD_MVP.md` (gather/nurture)

---

## Purpose

Gameplay-hook props for homestead + shared transit/planet reuse:

- Planters / path tiles (Shot 2; nurture N1)
- Six resources World + Stored (V3 gather / store / spend)
- `SM_LandingCircle` — **one mesh, used twice** (planet day landing + reuse note)
- `SM_Shrine_Homestead` — portal socket (night V5)
- Misc: lantern, drying rack, workbench (store / N2 / porch read)

Tone: warm, readable, handmade, hopeful. Cite **only** the ten masters.

---

## Spec index

| File | Contents |
|---|---|
| `PLANTERS_PATH.md` | Planter ×2–3 + path stone 3-pack; `M_PathStone` / `M_GatherHerb` / `M_Nurtured` |
| `GATHERABLES_WORLD_STORED.md` | RES_WOOD/FIBER/STONE/BERRY/HERB/SEED `_World` / `_Stored` |
| `SM_LandingCircle.md` | Landing circle mesh; dual placement contract |
| `SM_Shrine_Homestead.md` | Homestead shrine + portal socket; planet return stub |
| `PROPS_MISC.md` | Lantern, drying rack, workbench; `M_WoodCabin` / `M_WoodWild` |
| `../08_Transit/SM_LandingCircle_REF.md` | Transit ref → this mesh (does **not** touch `GLIDE_SPLINE.md`) |

Handoff: `Docs/handoffs/P3_PROP_kit.md`

---

## Gate names (must be published before WAVE_3)

| Published name | Role |
|---|---|
| `SM_LandingCircle` | Shared landing clearing mesh (graybox volume alias: `SM_Landing_Circle`) |
| `SM_Shrine_Homestead` | Homestead shrine + portal socket |
| `SM_Planter_A` / `SM_Planter_B` / `SM_Planter_C` | Raised garden planters |
| `SM_PathStone_A` / `SM_PathStone_B` / `SM_PathStone_C` | Path 3-pack tiles |
| `SM_RES_*_World` / `SM_RES_*_Stored` | Six gatherables ×2 forms |

---

## Ownership fence

| Owner | Owns | PROP does not |
|---|---|---|
| ENV-H | Island top, cliff, cabin modular, lookout, **glider perch** `SM_Glider_Perch`, pines | — |
| ENV-P (WAVE_3) | Planet massing, forest dress, hamlet roofs, `SM_Shrine_Planet` / return shrine final, second instance of landing | — |
| PROP (this kit) | Planters, path tiles, gatherables, shrine homestead socket, landing circle **mesh**, lantern/rack/workbench | Island massing, lighting, beasts, code, PHASE_BOARD |
| LIT | Presets / moon / window emissives | Prop meshes |
| TA | Ten masters | Prop authoring |

---

## Units / export

- Meters. Origins at ground contact. Apply scale.
- Adult 1.8 m reference. Blender → UE later: −Y Forward, Z Up.
- Prefixes: `SM_` meshes; materials `M_*` from sheet only.
- Suffixes: `_World` `_Stored` `_Nurtured` as needed. No `_Night` texture sets — use NightMix.

---

## Hard rejects

Photoreal scans; grimdark; sci-fi portal tech / neon rings; pancake landing pads; dark cabin windows; extra biomes / tree species; crafting trees; unique shaders outside the ten masters; overwriting `GLIDE_SPLINE.md` or ENV-H cabin paths.

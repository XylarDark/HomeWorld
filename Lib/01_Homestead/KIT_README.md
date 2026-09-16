# Lib/01_Homestead — Modular Kit Overview

**ID:** P3_ENVH_kit  
**Date:** 2026-09-16  
**Role:** ENV-H (homestead environment)  
**Status:** KIT SPECS READY (Blender MCP unavailable — markdown + JSON contracts, not `.blend` meshes)  
**Map dress target:** `Maps/Preview_Homestead_Night` (and related homestead night preview)

Units: **meters**. Origins at **ground contact**. **Apply scale** (no unapplied transform). Up +Z. Forward (lookout → planet) −Y. Right (cabin → lookout) +X — match `Lib/00_Core/GRAYBOX_LAYOUT.md`.

---

## 1. Scope

This kit dresses the **hero island homestead** only:

| Included | Spec file |
|---|---|
| Island top plate | `SM_IslandTop.md` |
| Layered torn-earth cliff | `SM_Cliff.md` |
| Modular cabin (walls / roof / chimney / porch) | `CABIN_MODULES.md` |
| Stylized pines 6–12 m | `PINES_HOMESTEAD.md` |
| Garden bed blocking | `GARDEN_BLOCKING.md` |

**Out of this kit (other owners):** planet forest, gatherables, lights (`LIT_*`), beasts, spirits, transit islets, shrine hero props, path-stone 3-pack meshes (PROP may share `M_PathStone` cites on island top sockets).

Instance **TA masters only** (`Docs/02_MATERIAL_SHEET.md` / `Lib/06_Materials_Master/`). No unique shaders. No 11th master.

---

## 2. Canon place names ↔ graybox map

Prefer kit canon names below. Graybox volumes remain placement guides until meshes replace them.

| Kit canon | Graybox stand-in(s) | Notes |
|---|---|---|
| **SM_IslandTop** | `SM_Island_Hero` | Walkable plateau / grass top; **separate** from cliff |
| **SM_Cliff** (modules) | `SM_Cliff_LookoutFace`, `SM_Cliff_CabinFace`, `SM_Cliff_Rear` | Layered torn earth — **not** pancake/cylinder |
| Cabin modules | `SM_Cabin` | Overall envelope 5–6 m |
| Pine variants | `SM_PineCluster_Homestead_A/B/C` | Stylized pines only |
| Garden blocking | `SM_Garden_Beds` | Beds/planters only; PROP dresses plants |

Path volume `SM_Path_Homestead` and lookout/glider/shrine volumes stay layout sockets; this kit exposes socket markers on the top plate where those dress.

---

## 3. Separate island top vs cliff (hard rule)

| Asset | Owns | Does not own |
|---|---|---|
| **SM_IslandTop** | Walkable grass plateau, path trench/socket, planter footprints, pine stump sockets, lookout pad flat | Cliff strata, underside torn rock |
| **SM_Cliff** | Layered slabs / torn modules under and around the rim | Grass top surface, cabin, pines |

Do **not** merge top + cliff into one pancake disc or cylinder plug. Edge must read as **broken earth** (art bible §2 / shotlist Shot 1).

---

## 4. Scale lock (canon §5)

| Element | Target |
|---|---|
| Adult ref | 1.8 m |
| Cabin overall | **5–6 m** |
| Island footprint | **18–24 m** (graybox hero **21 m** X) |
| Homestead pines | **6–12 m** only |

All exports: applied scale = 1.0; origin at ground contact.

---

## 5. Materials cited (instances of TA masters)

| Use | Master |
|---|---|
| Island top grass | `M_StylizedGrass` |
| Path inlays / stone sockets | `M_PathStone` |
| Cliff rock | `M_CliffRock` |
| Cabin wood + warm window slots | `M_WoodCabin` (window emissive driven by **LIT**, not dark glass) |
| Pine trunks | `M_WoodWild` |
| Pine foliage cards | `M_FoliageCard` |
| Garden bed wood boxes | `M_WoodCabin` (or raw-leaning instance) |
| Crop / colorful plant dress | **PROP** — `M_GatherHerb` / `M_Nurtured` (not authored here) |

---

## 6. Modular piece index

See child specs for sockets, dims, and module lists. Optional JSON manifests:

- `SM_IslandTop.json`
- `SM_Cliff.json`
- `CABIN_MODULES.json`
- `PINES_HOMESTEAD.json`
- `GARDEN_BLOCKING.json`

---

## 7. Gate claims (ENV-H)

- [x] Cliff is **layered** (modules / layered slabs) — not pancake/cylinder
- [x] Canon names **SM_IslandTop** / **SM_Cliff** live under `Lib/01_Homestead/`
- [x] Kit ready for **Preview_Homestead_Night** dress (specs + sockets; meshes when MCP/Blender)

---

## 8. Rejects

Pancake/cylinder island; merged top+cliff monolith; extra tree species; photoreal scans; dark cabin windows; planet forest / gatherables / lights / beasts in this folder; inventing materials outside the ten masters.

# GARDEN_BLOCKING — Garden Bed Blocking Spec

**Kit:** `Lib/01_Homestead`  
**Graybox map:** `SM_Garden_Beds`  
**Date:** 2026-09-16 · **ID:** P3_ENVH_kit · **Owner:** ENV-H

---

## 1. Role

**Garden bed blocking only** — raised wooden planter boxes as layout masses for Shot 2.  
**PROP dresses** plants / colorful crop read / nurtured targets. ENV-H does not hero-model produce.

---

## 2. Envelope

| Property | Value |
|---|---|
| Zone volume (graybox) | **4.0 × 2.5 × 0.6 m** at (−3.5, 0.5, 0.0) |
| Root socket | `SOCKET_Garden_Beds` on `SM_IslandTop` |
| Bed height | ~0.4–0.6 m raised |
| Style | Simple rectangular wooden planters; handmade; matching cabin timber language |

Key-art read: 2–3 rectangular beds near cabin / path; one leafy, one floral (plant dress = PROP).

---

## 3. Blocking meshes

| Mesh | Size guide (X×Y×Z m) | Material | Notes |
|---|---|---|---|
| **SM_GardenBed_A** | 1.8 × 1.0 × 0.5 | M_WoodCabin | Primary bed (veg proxy volume) |
| **SM_GardenBed_B** | 1.6 × 0.9 × 0.5 | M_WoodCabin | Secondary bed (flower proxy volume) |
| **SM_GardenBed_C** | 1.2 × 0.8 × 0.45 | M_WoodCabin | Optional third / fence-adjacent |
| **SM_GardenBed_Soil** | inset −0.08 | M_StylizedGrass dry *or* soil via grass instance | Blocking soil fill only |
| **SM_Garden_Fence_Seg** (optional) | 1.2 × 0.08 × 0.7 | M_WoodCabin | Low rail near beds if needed for Shot 2 — not a new biome fence kit |

Soil / crop **volume empties** for PROP:

| Socket | Parent | For PROP |
|---|---|---|
| SOCKET_Crop_A | Bed A | Rows / leafy dress; nurture target 1 may use `M_Nurtured` |
| SOCKET_Crop_B | Bed B | Colorful flower/plant read (`M_GatherHerb` / PROP) |
| SOCKET_Crop_C | Bed C | Optional |

---

## 4. Materials

| Part | Master | Owner |
|---|---|---|
| Planter wood | **M_WoodCabin** | ENV-H |
| Soil fill blocking | **M_StylizedGrass** instance (drier) | ENV-H |
| Plants / crops / nurtured | **M_GatherHerb** / **M_Nurtured** | **PROP** (dress only) |

ENV-H ships empty beds with soil plane. Do not author gatherable herb clusters here.

---

## 5. Placement

- Keep beds readable in Shot 2 three-quarter with cabin face + warm windows
- Align to path (`SM_Path_Homestead`) without blocking walk
- Stay inside graybox garden AABB; do not expand into new locations

---

## 6. Naming / export

- `SM_GardenBed_*`
- Collection: `Lib/01_Homestead`
- Applied scale; origins at bed ground contact

---

## 7. Rejects

Hero plant sculptures in ENV-H; extra biome planters; unique soil/plant shaders; dark muddy beds that kill night warm/cool read; expanding garden into planet kit.

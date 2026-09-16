# CABIN_MODULES — Modular Cabin Spec

**Kit:** `Lib/01_Homestead`  
**Root:** cabin module set under graybox `SM_Cabin`  
**Date:** 2026-09-16 · **ID:** P3_ENVH_kit · **Owner:** ENV-H

---

## 1. Role

Rustic handmade **log / gabled** cabin for homestead hub. Modular pieces for reuse and LOD. Overall cabin **5–6 m**. Warm window material slots — **emissive handled by LIT** (never dark/dead windows).

Shots: Shot 1 (cabin left, warm windows), Shot 2 (cabin + garden close).

---

## 2. Overall envelope

| Property | Value |
|---|---|
| Overall size | **5.5 × 4.5 × 5.5 m** (within 5–6 m) — match graybox `SM_Cabin` |
| World origin (root) | (−6.0, 1.0, 0.0) via `SOCKET_Cabin` on island top |
| Local origin | Ground contact under foundation center (0, 0, 0) local |
| Ridge height | ~5.0–5.5 m to peak |
| Style | Simple rustic log, gabled; stone foundation optional; cozy, not Victorian / sci-fi |

---

## 3. Module list

| Module | Size guide (m) | Material | Notes |
|---|---|---|---|
| **SM_Cabin_Wall_Front** | ~5.5 × 0.25 × 2.8 | M_WoodCabin | Door opening + window opening |
| **SM_Cabin_Wall_Back** | ~5.5 × 0.25 × 2.8 | M_WoodCabin | Solid / optional small window |
| **SM_Cabin_Wall_Side_L** | ~4.5 × 0.25 × 2.8 | M_WoodCabin | Side window opening |
| **SM_Cabin_Wall_Side_R** | ~4.5 × 0.25 × 2.8 | M_WoodCabin | Optional solid |
| **SM_Cabin_Foundation** | ~5.7 × 4.7 × 0.4 | M_CliffRock *or* M_WoodCabin | Optional stone sill — cite existing master only |
| **SM_Cabin_Roof_A** | half gable ~5.8 × 2.6 × 1.8 | M_WoodCabin | Left roof plane / shingles |
| **SM_Cabin_Roof_B** | half gable ~5.8 × 2.6 × 1.8 | M_WoodCabin | Right roof plane |
| **SM_Cabin_Chimney** | ~0.6 × 0.6 × 1.8 | M_CliffRock preferred | Sits on roof left (key-art side) |
| **SM_Cabin_Door** | ~1.0 × 0.1 × 2.0 | M_WoodCabin | Simple plank door |
| **SM_Cabin_Window_Frame** | ~1.2 × 0.1 × 1.0 | M_WoodCabin | Frame only |
| **SM_Cabin_Window_Pane** | ~1.1 × 0.05 × 0.9 | **M_WoodCabin** warm-glass instance | Slot for warm emissive; **LIT drives glow** |
| **SM_Cabin_Porch_Deck** | ~3.0 × 1.5 × 0.2 | M_WoodCabin | Raised deck at front door |
| **SM_Cabin_Porch_Post** | ~0.15 × 0.15 × 1.4 | M_WoodCabin | 2–4 posts |
| **SM_Cabin_Porch_Rail** | ~1.2 × 0.1 × 0.6 | M_WoodCabin | Simple rail segments |

Optional: `SM_Cabin_Gable_Fill` for triangular gable ends.

---

## 4. Materials

| Use | Master | Rule |
|---|---|---|
| Walls, roof, door, porch, frames | **M_WoodCabin** | Painted ↔ raw instance tweaks allowed |
| Chimney / foundation stone | **M_CliffRock** | Same master as cliff — no new rock shader |
| Window panes | **M_WoodCabin** instance with warm BaseColor + Emissive slot | Default emissive may be low in mesh; **LIT** / Homestead_Night owns the warm punch |
| Night body | NightMix on masters | No `_Night` duplicate meshes |

**Reject:** dark cabin windows; unique window glass master; photoreal timber scans.

---

## 5. Window slots (LIT contract)

| Slot | Local hint | Intent |
|---|---|---|
| SLOT_Window_Front | Front wall center-right | Primary warm spill toward path / garden (Shot 2) |
| SLOT_Window_Side | Left side wall | Secondary warm read (Shot 1 silhouette) |
| SOCKET_LIT_CabinWarm | Near (−6.0, 1.0, 1.5) world | Align with graybox `LIT_CabinWarm` — LIT places lights |

ENV-H provides pane meshes + material slots. LIT authors intensity / Kelvin (~2700–3200K feel). Do not ship black/unlit panes for night dress.

---

## 6. Assembly sockets (local to cabin root)

| Socket | Approx local (m) | Child |
|---|---|---|
| SOCKET_Roof | (0, 0, 2.8) | Roof A/B + chimney |
| SOCKET_Chimney | (−1.8, 0.2, 4.2) | Chimney |
| SOCKET_Porch | (0, −2.4, 0.0) | Deck / posts / rails |
| SOCKET_Door | (0, −2.25, 0.0) | Door |
| SOCKET_Window_Front | (1.2, −2.25, 1.4) | Front window set |
| SOCKET_Window_Side | (−2.75, 0.5, 1.4) | Side window set |

---

## 7. Naming / export

- Prefix: `SM_Cabin_*`
- Collection: `Lib/01_Homestead`
- Applied scale; origin ground contact; meters

---

## 8. Rejects

Ornate Victorian; sci-fi prefab; dark windows; cabin >6 m or <5 m envelope; extra rooms/biomes; unique wood shader.

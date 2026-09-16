# SM_IslandTop — Island Top Plate Spec

**Kit:** `Lib/01_Homestead`  
**Canon name:** `SM_IslandTop`  
**Graybox map:** replaces / dresses `SM_Island_Hero` top face (keep cliff as `SM_Cliff`)  
**Date:** 2026-09-16 · **ID:** P3_ENVH_kit · **Owner:** ENV-H

---

## 1. Role

Walkable **grass plateau** for the hero homestead. Separate mesh(es) from the cliff face. Carries sockets for cabin, path, garden beds, pines, lookout pad, shrine, glider perch.

Shot consumers: Shot 1 (path + garden read), Shot 2 (path + planter ground).

---

## 2. Dimensions & origin

| Property | Value |
|---|---|
| Footprint target | **~21 m** X × **~14 m** Y (within island 18–24 m) |
| Top thickness | 0.3–0.6 m grass/soil crust (visual); walkable face ≈ **Z = 0** |
| Plateau walkable AABB | X ∈ [−9.5, 9.5], Y ∈ [−5.0, 5.0], Z = 0 (graybox) |
| Origin | Ground contact at plateau datum **(0, 0, 0)** — top face at Z ≈ 0 |
| Units | Meters; **apply scale** |

Silhouette: irregular torn rim in plan (not perfect ellipse). Gentle undulation OK; no tall cliffs on this mesh.

---

## 3. Materials

| Slot / region | Master (instance) | Notes |
|---|---|---|
| Primary ground | **M_StylizedGrass** | Lush spring green; NightMix from LIT/GameState |
| Path inlays / trench | **M_PathStone** | Cite only; stone pack meshes may be PROP |
| Optional soil rim | M_StylizedGrass dry instance or same master | Keep within grass palette — no new master |

Do not assign `M_CliffRock` to the top plate.

---

## 4. Geometry rules

- Flat-to-undulating top; **no** stacked strata (those belong on `SM_Cliff`).
- Rim edge jagged where it meets cliff modules (boolean-friendly overlap ~0.1–0.2 m).
- Path depression or UV/mask region along graybox `SM_Path_Homestead` (10.0 × 1.2 m, origin world (0, 0, 0)).
- Collision: simple walkable hull or heightfield proxy; player-facing, not Nanite-required for MVP.

---

## 5. Sockets (empty transforms / markers)

Place empty sockets at graybox origins (world). Child meshes snap to these when dressing Preview_Homestead_Night.

| Socket name | World origin (m) | Consumes |
|---|---|---|
| SOCKET_Cabin | (−6.0, 1.0, 0.0) | Cabin module root |
| SOCKET_Garden_Beds | (−3.5, 0.5, 0.0) | Garden blocking root |
| SOCKET_Path_Homestead | (0.0, 0.0, 0.0) | Path dress / PROP stones |
| SOCKET_Lookout_Pad | (7.0, −3.5, 0.0) | Lookout flat / family silhouette spot |
| SOCKET_Glider_Perch | (7.5, −4.5, 0.0) | Glider perch (PROP / later) |
| SOCKET_Shrine_Homestead | (−2.0, 3.5, 0.0) | Homestead shrine (other kit) |
| SOCKET_Pine_A | (−8.0, −2.0, 0.0) | Pine 6–12 m |
| SOCKET_Pine_B | (3.0, 3.0, 0.0) | Pine |
| SOCKET_Pine_C | (5.5, 1.5, 0.0) | Pine near lookout |
| SOCKET_CliffAttach_Lookout | (7.5, −5.5, 0.0) | Align `SM_Cliff` lookout face |
| SOCKET_CliffAttach_Cabin | (−7.0, −4.5, 0.0) | Align cabin-side cliff |
| SOCKET_CliffAttach_Rear | (0.0, 5.0, 0.0) | Align rear cliff |

---

## 6. Naming / export

- Mesh: `SM_IslandTop` (optional LOD: `SM_IslandTop_LOD1`)
- Collection: `Lib/01_Homestead`
- FBX later: −Y Forward, Z Up; origin ground contact; applied scale

---

## 7. Rejects

Pancake disc with cliff baked in; cylinder plug; path as separate biome; extra flora species on top mesh; unique grass shader.

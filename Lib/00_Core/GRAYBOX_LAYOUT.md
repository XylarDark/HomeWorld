# Lib/00_Core/GRAYBOX_LAYOUT.md

**ID:** P1_WLD_graybox  
**Date:** 2026-09-16  
**Role:** WLD — file-based graybox only (Blender MCP unavailable). ENV dresses later.  
**Inputs:** `Docs/00_CANON.md`, `Docs/00_SHOTLIST.md`  
**Units:** meters. **Up:** +Z. **Forward (lookout → planet):** −Y. **Right (cabin → lookout):** +X.  
**Origins:** ground contact. Apply scale. Do not hero-model.

---

## 0. Scale reference

| Name | Type | Size (X×Y×Z m) | Origin (world) | Notes |
|---|---|---|---|---|
| SM_ScaleRef_Adult | SM_ volume | 0.6 × 0.4 × 1.8 | (0.0, 0.0, 0.0) plateau datum | Adult 1.8 m per canon §5 |

All island plateau volumes sit on Z = 0 ground plane unless noted. Planet slice sits far below.

---

## 1. Hero island massing (18–24 m)

Island footprint: **21 m** across X (within 18–24 m). Layered torn-earth cliff — not pancake/cylinder (canon §7 / shotlist Shot 1).

| Name | Type | Size (X×Y×Z m) | Origin (world) | Role |
|---|---|---|---|---|
| SM_Island_Hero | SM_ volume | 21.0 × 14.0 × 4.0 | (0.0, 0.0, −2.0) | Main plateau mass; origin at underside center so top face ≈ Z 0 |
| SM_Cliff_LookoutFace | SM_ volume | 6.0 × 2.5 × 8.0 | (7.5, −5.5, −4.0) | Right / front torn-earth face under lookout |
| SM_Cliff_CabinFace | SM_ volume | 5.0 × 2.0 × 6.0 | (−7.0, −4.5, −3.0) | Left layered underside under cabin side |
| SM_Cliff_Rear | SM_ volume | 12.0 × 2.0 × 5.0 | (0.0, 5.0, −2.5) | Rear massing; keeps non-cylinder silhouette |

Approximate plateau walkable top: X ∈ [−9.5, 9.5], Y ∈ [−5.0, 5.0], Z = 0.

---

## 2. Homestead volumes (hub)

Canon topology: cabin, garden, path, pines, lookout, shrine, glider perch.

| Name | Type | Size (X×Y×Z m) | Origin (world) | Role |
|---|---|---|---|---|
| SM_Cabin | SM_ volume | 5.5 × 4.5 × 5.5 | (−6.0, 1.0, 0.0) | Cabin 5–6 m (canon §5); left of plateau (key-art) |
| SM_Garden_Beds | SM_ volume | 4.0 × 2.5 × 0.6 | (−3.5, 0.5, 0.0) | Raised beds / planters zone (Shot 2) |
| SM_Path_Homestead | SM_ volume | 10.0 × 1.2 × 0.15 | (0.0, 0.0, 0.0) | Stone path cabin → lookout across plateau |
| SM_Lookout_Pad | SM_ volume | 3.0 × 2.5 × 0.2 | (7.0, −3.5, 0.0) | Right cliff edge; family silhouette spot (Shot 1) |
| SM_Glider_Perch | SM_ volume | 2.0 × 1.5 × 0.5 | (7.5, −4.5, 0.0) | Glider perch / departure (Shot 3) |
| SM_Shrine_Homestead | SM_ volume | 1.5 × 1.5 × 2.0 | (−2.0, 3.5, 0.0) | Homestead shrine (spirit/night link) |
| SM_PineCluster_Homestead_A | SM_ volume | 2.0 × 2.0 × 9.0 | (−8.0, −2.0, 0.0) | Pine 6–12 m stand-in |
| SM_PineCluster_Homestead_B | SM_ volume | 2.0 × 2.0 × 8.0 | (3.0, 3.0, 0.0) | Pine stand-in |
| SM_PineCluster_Homestead_C | SM_ volume | 2.0 × 2.0 × 10.0 | (5.5, 1.5, 0.0) | Pine stand-in near lookout |

---

## 3. Transit graybox (islets only — spline in `Lib/08_Transit/GLIDE_SPLINE.md`)

| Name | Type | Size (X×Y×Z m) | Origin (world) | Role |
|---|---|---|---|---|
| SM_Islet_01 | SM_ volume | 3.0 × 2.5 × 1.5 | (6.0, −18.0, −25.0) | Small floating islet (Shot 1/3) |
| SM_Islet_02 | SM_ volume | 2.5 × 2.0 × 1.2 | (3.0, −32.0, −48.0) | Mid transit islet |
| SM_Islet_03 | SM_ volume | 2.0 × 2.0 × 1.0 | (1.0, −48.0, −72.0) | Near-landing islet |

---

## 4. Planet slice volumes (must be visible from lookout)

Canon: forest path 2–4 min, gather nodes, 1 beast pad, 1 spirit-wound site, landing circle, return shrine, 2–3 hamlet roof silhouettes. Lookout test: landing, portal exit, first harvest, way home.

| Name | Type | Size (X×Y×Z m) | Origin (world) | Role |
|---|---|---|---|---|
| SM_Landing_Circle | SM_ volume | 8.0 × 8.0 × 0.2 | (0.0, −70.0, −95.0) | Day landing clearing (Shot 4) |
| SM_Path_Planet_SegA | SM_ volume | 18.0 × 1.4 × 0.15 | (2.0, −82.0, −95.0) | Path segment A from landing |
| SM_Path_Planet_SegB | SM_ volume | 22.0 × 1.4 × 0.15 | (8.0, −100.0, −95.0) | Path segment B (winding) |
| SM_Path_Planet_SegC | SM_ volume | 20.0 × 1.4 × 0.15 | (4.0, −118.0, −95.0) | Path segment C toward slice end |
| SM_Roof_Hamlet_01 | SM_ volume | 4.0 × 3.5 × 3.0 | (−12.0, −90.0, −95.0) | Hamlet roof silhouette 1 |
| SM_Roof_Hamlet_02 | SM_ volume | 3.5 × 3.0 × 2.8 | (−8.0, −105.0, −95.0) | Hamlet roof silhouette 2 |
| SM_Roof_Hamlet_03 | SM_ volume | 3.0 × 2.5 × 2.5 | (−14.0, −112.0, −95.0) | Hamlet roof silhouette 3 |
| SM_Shrine_Return | SM_ volume | 1.5 × 1.5 × 2.0 | (6.0, −75.0, −95.0) | Return shrine / portal exit (planet) |
| SM_Gather_FirstHarvest | SM_ volume | 2.0 × 2.0 × 1.0 | (5.0, −88.0, −95.0) | First harvest / gather-node marker (lookout test) |
| SM_BeastPad_01 | SM_ volume | 4.0 × 4.0 × 0.2 | (12.0, −108.0, −95.0) | 1 beast pad |
| SM_SpiritWound_01 | SM_ volume | 3.0 × 3.0 × 0.5 | (−4.0, −115.0, −95.0) | 1 spirit-wound site |
| SM_PineValley_Block_A | SM_ volume | 10.0 × 8.0 × 10.0 | (15.0, −95.0, −95.0) | Pine valley massing (read from lookout) |
| SM_PineValley_Block_B | SM_ volume | 8.0 × 10.0 × 9.0 | (−18.0, −100.0, −95.0) | Pine valley massing |

Distant snow peak (sky/read only — sky volume, not walkable):

| Name | Type | Size (X×Y×Z m) | Origin (world) | Role |
|---|---|---|---|---|
| SM_Peak_Distant | SM_ volume | 20.0 × 12.0 × 30.0 | (40.0, −160.0, −40.0) | Distant snow peak silhouette (Shot 1) |

---

## 5. Camera and light volumes (poses detailed in `CAM_Hero.md`)

| Name | Type | Size (X×Y×Z m) | Origin (world) | Role |
|---|---|---|---|---|
| CAM_Hero | CAM_ volume | 0.5 × 0.5 × 0.5 | (−4.0, 4.5, 3.2) | Shot 1 lookout key-art camera |
| CAM_CabinClose | CAM_ volume | 0.4 × 0.4 × 0.4 | (−4.0, −2.5, 1.6) | Shot 2 framing helper |
| CAM_GlideDepart | CAM_ volume | 0.4 × 0.4 × 0.4 | (7.0, −5.0, 1.8) | Shot 3 departure helper |
| CAM_LandingDay | CAM_ volume | 0.4 × 0.4 × 0.4 | (0.0, −64.0, −92.0) | Shot 4 landing helper |
| CAM_PortalNight | CAM_ volume | 0.4 × 0.4 × 0.4 | (−2.0, 2.5, 1.5) | Shot 5 shrine/portal helper |
| LIT_CabinWarm | LIT_ volume | 3.0 × 3.0 × 2.5 | (−6.0, 1.0, 1.5) | Warm cabin glow stand-in |
| LIT_MoonCool | LIT_ volume | 8.0 × 8.0 × 4.0 | (10.0, −2.0, 12.0) | Cool moonlight fill stand-in |
| LIT_LandingDay | LIT_ volume | 12.0 × 12.0 × 6.0 | (0.0, −70.0, −88.0) | Day clearing fill stand-in |

---

## 6. Walk times (seconds)

**Assumed stroll speed:** 1.4 m/s (adult 1.8 m scale). Times are graybox targets for pacing; ENV/SYS may retune path length, not invent new destinations.

### 6.1 Homestead loop

Route: `SM_Cabin` → `SM_Garden_Beds` → along `SM_Path_Homestead` → `SM_Lookout_Pad` → `SM_Shrine_Homestead` → `SM_Cabin`.

| Segment | Approx. distance (m) | Time (s) |
|---|---|---|
| Cabin → garden | 3 | 2 |
| Garden → lookout (path) | 12 | 9 |
| Lookout → homestead shrine | 10 | 7 |
| Shrine → cabin | 5 | 4 |
| **Homestead loop total** | **~30** | **~22 s** |

### 6.2 Lookout to shrine

| Route | Approx. distance (m) | Time (s) |
|---|---|---|
| `SM_Lookout_Pad` → `SM_Shrine_Homestead` | 10 | **7 s** |
| `SM_Lookout_Pad` → `SM_Shrine_Return` (via glide + short walk; glide excluded) | landing→shrine ~8 | **~6 s walk after landing** |

### 6.3 Planet path (2–4 min target = 120–240 s)

Broken into segments along `SM_Path_Planet_SegA/B/C` plus short clears at pads. Mid-target **~180 s** (~3 min).

| Segment | From → To | Approx. distance (m) | Time (s) |
|---|---|---|---|
| Seg A | `SM_Landing_Circle` → end SegA / first harvest | 45 | 32 |
| Seg B | SegA end → SegB end / beast pad approach | 70 | 50 |
| Seg C | SegB end → SegC end / spirit-wound approach | 65 | 46 |
| Spur | path → `SM_Roof_Hamlet` cluster read (optional spur) | 25 | 18 |
| Spur | path → `SM_Shrine_Return` (return / portal) | 20 | 14 |
| **Planet path core (A+B+C)** | | **~180** | **~128 s (~2.1 min)** |
| **With both spurs** | | **~225** | **~160 s (~2.7 min)** |

Core alone sits at low end of 2–4 min; with soft meander / gather pauses ENV can stretch to **~180–240 s** without new locations.

---

## 7. Sightline checklist (from `CAM_Hero`)

Documented claim — ENV verifies in Blender when dressing:

| # | Must see from CAM_Hero | Target volume | Claim |
|---|---|---|---|
| 1 | Landing circle | `SM_Landing_Circle` | PASS (in frustum down −Y/−Z) |
| 2 | 2–3 roofs | `SM_Roof_Hamlet_01/02/03` | PASS (left of landing in valley) |
| 3 | Forest path | `SM_Path_Planet_SegA` (+ B hint) | PASS (winding read below) |
| 4 | Return shrine | `SM_Shrine_Return` | PASS (near landing) |
| 5 | First harvest (lookout test) | `SM_Gather_FirstHarvest` | PASS (along SegA) |
| 6 | Way home / portal exit read | `SM_Shrine_Return` + island mass above | PASS (shrine + cliff back-read) |

**Gate result:** lookout sees landing / roofs / path — **CLAIMED PASS** (file graybox).

---

## 8. Out of scope (WLD)

- Final materials / master assignment (TA)
- Cabin kit modeling / hero sculptures (ENV / PROP)
- Gameplay code / free-flight sim (SYS / GPL) — rejected by canon
- Editing PHASE_BOARD, GDD, art bible, material sheet

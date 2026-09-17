# Maps/VS_MVP

**Vertical slice assembly — P6 INT (portable)**  
**Date:** 2026-09-16  
**ID:** P6_INT_slice  
**Role:** INT  
**Status:** ASSEMBLY NOTES + camera reel (Blender-proven; UE dress deferred)  
**Blend:** `blender/floating_island_homestead_LIB.blend`  
**Export contract:** `Docs/04_EXPORT_TABLE.md`  
**UE notes:** `Docs/04_UE_HANDOFF_NOTES.md`  
**Reel:** [`CAMERA_REEL.md`](CAMERA_REEL.md)

Flight fallback **ARMED:** scripted glide + portal both ways (`Docs/03_GAMEPLAY_MVP.md` FALLBACK appendix; `Docs/handoffs/P5_CND_fallback_flight.md`).

---

## 1. Purpose

Portable vertical-slice definition for:

1. **Leave island** — FALLBACK scripted glide along `CRUMB_*`  
2. **Land** — `SM_LandingCircle` day clearing  
3. **Portal home** — night spirit portal `SM_Shrine_Homestead` ↔ `SM_Shrine_Return`  

Proven by **camera reel shots 1–5** and existing Preview stills — not by UE set dressing in P6.

---

## 2. Assembly (Blender library)

### Collections used

| Collection | Role in VS |
|---|---|
| `00_Core` | Five reel cameras |
| `01_Homestead` | Island / cabin / lookout / departure |
| `02_Forest` | Planet slice + return shrine |
| `03_Gatherables` | Landing circle + homestead shrine |
| `07_Night_SpiritLayer` | Night lights / spirit layer |
| `08_Transit` | Islets + `CRUMB_*` glide path |
| `VS_MVP` | Slice EMPTY markers (`VS_MARKER_*`) |

### Leave island (FALLBACK glide)

1. Start at lookout / `SM_Glider_Perch` (`VS_MARKER_LeaveIsland_FALLBACK`).  
2. Play **scripted** traverse of crumbs in order (`Lib/08_Transit/GLIDE_SPLINE.md`):  
   `CRUMB_Depart_Lookout` → `CRUMB_Air_01` → `CRUMB_Islet_01` → … → `CRUMB_Landing`.  
3. Demo camera: `CAM_GlideDepart` → still `Maps/Preview_Lookout_To_Planet/shot3_glide_depart.png`.  
4. **Not** free flight.

### Land

1. Touchdown on `SM_LandingCircle` (`VS_MARKER_LandPlanet`).  
2. Demo camera: `CAM_LandingDay` → still `Maps/Preview_Lookout_To_Planet/shot4_landing_day.png`.  
3. Collision proxy: simple box / flat pad (`UCX_SM_LandingCircle`).

### Portal home (both ways)

1. Night / spirit form at `SM_Shrine_Return` or `SM_Shrine_Homestead`.  
2. Link only those two shrines (`Docs/03_GAMEPLAY_MVP.md` V5).  
3. Demo camera: `CAM_PortalNight` → still `Maps/Preview_Homestead_Night/shot5_portal_night.png`.  
4. Homestead night context: shots 1–2 stills under `Maps/Preview_Homestead_Night/`.

---

## 3. Camera reel order (shots 1–5)

See [`CAMERA_REEL.md`](CAMERA_REEL.md) for full table. Summary:

| # | Camera | Still |
|---|---|---|
| 1 | `CAM_Hero` | [`../Preview_Homestead_Night/shot1_lookout.png`](../Preview_Homestead_Night/shot1_lookout.png) |
| 2 | `CAM_CabinClose` | [`../Preview_Homestead_Night/shot2_cabin_garden.png`](../Preview_Homestead_Night/shot2_cabin_garden.png) |
| 3 | `CAM_GlideDepart` | [`../Preview_Lookout_To_Planet/shot3_glide_depart.png`](../Preview_Lookout_To_Planet/shot3_glide_depart.png) |
| 4 | `CAM_LandingDay` | [`../Preview_Lookout_To_Planet/shot4_landing_day.png`](../Preview_Lookout_To_Planet/shot4_landing_day.png) |
| 5 | `CAM_PortalNight` | [`../Preview_Homestead_Night/shot5_portal_night.png`](../Preview_Homestead_Night/shot5_portal_night.png) |

---

## 4. Gate evidence (document)

| Gate | Evidence |
|---|---|
| Leave island → planet → return portal (FALLBACK + portal) | Reel shots 3→4→5 (+ crumbs / shrine names); this README |
| Night homestead stills present | `shot1_lookout.png`, `shot2_cabin_garden.png`, `shot5_portal_night.png` |
| Library instance-based (10 masters) | `Lib/06_Materials_Master/` (10 JSON) + `Docs/02_MATERIAL_SHEET.md`; blend cites masters only |

---

## 5. UE handoff (notes only)

- Import paths: `Docs/04_EXPORT_TABLE.md`  
- Lumen/Nanite later; NightMix float; **same names**; **do not dress UE env yet** — `Docs/04_UE_HANDOFF_NOTES.md`  
- Collision: simple boxes for shrine, landing, cabin  

---

## 6. Out of scope

- New kits / features / biomes  
- UE level dressing beyond notes  
- PHASE_BOARD / Docs/07 sign-off  
- Spawning QA (Conductor)  

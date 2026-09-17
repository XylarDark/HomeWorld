# Docs/04_UE_HANDOFF_NOTES.md

**ID:** P6_INT_slice  
**Role:** INT  
**Date:** 2026-09-16  
**Status:** NOTES ONLY — do **not** dress the UE environment yet beyond this contract  
**Audience:** Future UE import / lighting / GP wiring

---

## 1. Same names

Keep Blender names 1:1 in UE content and level actors:

- Meshes: `SM_*`
- Materials: `M_*` / `MI_*`
- Cameras: `CAM_Hero`, `CAM_CabinClose`, `CAM_GlideDepart`, `CAM_LandingDay`, `CAM_PortalNight`
- Transit: `CRUMB_Depart_Lookout` … `CRUMB_Landing` (order locked in `Lib/08_Transit/GLIDE_SPLINE.md`)
- Shrines: `SM_Shrine_Homestead` ↔ `SM_Shrine_Return`
- Landing: `SM_LandingCircle`
- VS markers: `VS_MARKER_*` in collection `VS_MVP`

Content root: `/Game/HomeWorld/...` per `Docs/04_EXPORT_TABLE.md`.

---

## 2. Lumen / Nanite — later

| Feature | P6 stance |
|---|---|
| **Nanite** | Enable after mesh import polish; do not block VS portability on Nanite. Low-poly kit meshes OK as-is. |
| **Lumen** | Enable in a later lighting pass. Preview stills prove look in Blender Eevee; UE Lumen is **not** a P6 gate. |
| Materials | Port the **10** masters with `NightMix` — do not invent UE-only shader families for Lumen. |

---

## 3. NightMix float

- Single scalar **NightMix** (0–1) on all ten masters.  
- Homestead night preview target ≈ **0.85** (`Maps/Preview_Homestead_Night`).  
- Day landing / planet path → NightMix ≈ **0**.  
- One GameState / time float flips: lights + NightMix + spirit-layer visibility.  
- **Never** author `_Night` texture sets.

Windows stay warm emissive (LIT contract) at night.

---

## 4. Transit (FALLBACK armed)

- **Leave island:** scripted glide along `CRUMB_*` only (FALLBACK). No free-flight.  
- **Land:** `SM_LandingCircle`.  
- **Return:** portal both ways `SM_Shrine_Homestead` ↔ `SM_Shrine_Return` (night/spirit).  

Camera-reel / still evidence: `Maps/VS_MVP/CAMERA_REEL.md`.

---

## 5. Do not dress UE env yet

Allowed now:

- Import FBX/GLB to matching `/Game/HomeWorld/...` paths  
- Create empty level / folder `Maps/VS_MVP`  
- Place named cameras / TargetPoints from export table  
- Wire NightMix parameter stubs  

**Not** allowed in P6 INT scope:

- Full homestead / forest set dressing in UE  
- New kits or biomes  
- Combat, free-flight, inventory UI beyond existing SYS docs  
- Claiming Lumen beauty stills as gates  

Blender + `Maps/Preview_*` stills remain the look proof until a later UE dress wave.

---

## 6. Collision

Ship simple **UCX_** boxes for cabin, both shrines, and landing circle (`Docs/04_EXPORT_TABLE.md` §3). Complex collision later.

---

## 7. Masters lock

Exactly **10** library masters (instance-based). Evidence: `Lib/06_Materials_Master/*.json` + blend material names. No 11th.

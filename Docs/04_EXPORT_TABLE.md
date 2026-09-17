# Docs/04_EXPORT_TABLE.md

**ID:** P6_INT_slice  
**Role:** INT  
**Date:** 2026-09-16  
**Status:** DONE (portability contract — notes only; no UE dress)  
**Blend:** `blender/floating_island_homestead_LIB.blend`  
**Inputs:** `Docs/00_SHOTLIST.md`, `Docs/02_MATERIAL_SHEET.md` §4, `Lib/00_Core/GRAYBOX_LAYOUT.md`, P3/P4 kit handoffs

Do **not** invent kits or features. This table makes the existing library portable to UE under `/Game/HomeWorld/...`.

---

## 0. Global export rules

| Rule | Value |
|---|---|
| Units | **Meters** (adult 1.8 m) |
| Apply scale | **Yes** — Ctrl-A Scale before export; no non-1.0 object scale on SM_ |
| Origins | **Ground contact** (feet / underside resting plane) |
| Axis (FBX → UE) | **-Y Forward, Z Up** (UE FBX import preset) |
| Preferred mesh format | **FBX** for StaticMesh kits; **GLB** OK for markers / quick preview only |
| Materials | Cite one of the **10** masters only; UE MI_* instances — **NightMix** float, no `_Night` maps |
| Naming parity | Keep Blender `SM_` / `M_` / `CAM_` / `CRUMB_` / `SOCKET_` names identical in UE |
| Collision | See **Collision proxy** column — simple boxes for shrine, landing, cabin (MVP) |
| Nanite / Lumen | **Later** — see `Docs/04_UE_HANDOFF_NOTES.md`; do not block export on them |

**Staging disk path (optional pre-import):** `AssetCreation/Exports/<Category>/` then batch-import into `/Game/HomeWorld/...`.

---

## 1. Collection → UE content root

| Blender collection | UE content folder | Notes |
|---|---|---|
| `00_Core` | `/Game/HomeWorld/Maps/VS_MVP/Cameras/` (cams as actors / cine cams) | Export cameras as named cine camera actors or CameraActors — not SM_ |
| `01_Homestead` | `/Game/HomeWorld/Meshes/Homestead/` | Island, cliff, cabin kit, pines, garden, lookout, perch |
| `02_Forest` | `/Game/HomeWorld/Meshes/Forest/` | Planet slice dress, return shrine assembly, planet pines, ground |
| `03_Gatherables` | `/Game/HomeWorld/Meshes/Gatherables/` | Landing circle, homestead shrine, planters/path tiles, RES_* |
| `04_Beasts` | `/Game/HomeWorld/Meshes/Beasts/` | Pad proxies only this slice |
| `05_Spirits` | `/Game/HomeWorld/Meshes/Spirits/` | Spirit / wound proxies |
| `07_Night_SpiritLayer` | `/Game/HomeWorld/Lighting/Night_SpiritLayer/` | Lights + VOLUME — not mesh FBX; recreate as UE lights / PostProcess |
| `08_Transit` | `/Game/HomeWorld/Meshes/Transit/` + `/Game/HomeWorld/Maps/VS_MVP/Transit/` | Islets as SM_; CRUMB_* as Empty / spline points |
| `VS_MVP` | `/Game/HomeWorld/Maps/VS_MVP/Markers/` | Vertical-slice EMPTY markers only (P6) |

**Map target (assembly, not dressed yet):** `/Game/HomeWorld/Maps/VS_MVP` (notes / future level). Preview stills remain under `Maps/Preview_*` in repo.

---

## 2. Mesh / assembly export table

| Blender object / assembly | Collection | Format | UE path (asset name) | Collision proxy | Apply scale | Origin |
|---|---|---|---|---|---|---|
| `SM_IslandTop` | `01_Homestead` | FBX | `/Game/HomeWorld/Meshes/Homestead/SM_IslandTop` | Complex as simple **or** box slab matching top footprint | Yes | Plateau ground / top resting plane |
| `SM_Cliff_LookoutFace` (+ L0–L4 / Lip / Torn*) | `01_Homestead` | FBX (assembly or modules) | `/Game/HomeWorld/Meshes/Homestead/Cliff/SM_Cliff_LookoutFace` | Optional simplified hull later; **not** required for VS camera reel | Yes | Ground / ledge contact under lookout |
| `SM_Cliff_CabinFace` (+ layers) | `01_Homestead` | FBX | `/Game/HomeWorld/Meshes/Homestead/Cliff/SM_Cliff_CabinFace` | Optional | Yes | Underside contact |
| `SM_Cliff_Rear` (+ layers) | `01_Homestead` | FBX | `/Game/HomeWorld/Meshes/Homestead/Cliff/SM_Cliff_Rear` | Optional | Yes | Underside contact |
| `SM_Cliff_Slab_A/B/C`, `SM_Cliff_Chunk_Torn` | `01_Homestead` | FBX | `/Game/HomeWorld/Meshes/Homestead/Cliff/SM_Cliff_*` | None (kit modules) | Yes | Module local ground |
| `SM_Cabin` modular set (`SM_Cabin_*` walls/roof/porch/door/windows/chimney/foundation) | `01_Homestead` | FBX | `/Game/HomeWorld/Meshes/Homestead/Cabin/SM_Cabin_*` | **`UCX_SM_Cabin` simple box** ≈ 5.5×4.5×5.5 m (envelope) | Yes | Footprint ground contact at cabin pad |
| `SM_Cabin_Window_Pane_*` | `01_Homestead` | FBX | `/Game/HomeWorld/Meshes/Homestead/Cabin/SM_Cabin_Window_Pane_*` | None (non-blocking) | Yes | Pane center OK; keep emissive MI |
| `SM_Pine_Homestead_S/M/L` (+ trunk/foliage children) | `01_Homestead` | FBX | `/Game/HomeWorld/Meshes/Homestead/Pines/SM_Pine_Homestead_*` | Capsule or thin box optional | Yes | Trunk base ground |
| `SM_GardenBed_A/B/C` (+ soil) | `01_Homestead` | FBX | `/Game/HomeWorld/Meshes/Homestead/Garden/SM_GardenBed_*` | Box per bed optional | Yes | Ground contact |
| `SM_Planter_A/B/C` | `03_Gatherables` | FBX | `/Game/HomeWorld/Meshes/Gatherables/SM_Planter_*` | None / small box | Yes | Ground contact |
| `SM_PathStone_*` tiles | `01_Homestead` / gatherables | FBX | `/Game/HomeWorld/Meshes/Homestead/Path/SM_PathStone_*` | None (walk on landscape / island top) | Yes | Tile bottom |
| `SM_Lookout_Pad` | `01_Homestead` | FBX | `/Game/HomeWorld/Meshes/Homestead/SM_Lookout_Pad` | Thin box | Yes | Pad top ≈ Z0 |
| `SM_Glider_Perch` | `01_Homestead` | FBX | `/Game/HomeWorld/Meshes/Homestead/SM_Glider_Perch` | Small box | Yes | Ground contact |
| `SM_Shrine_Homestead` (+ base/posts/lintel/glow) | `03_Gatherables` | FBX | `/Game/HomeWorld/Meshes/Gatherables/SM_Shrine_Homestead` | **`UCX_SM_Shrine_Homestead` simple box** ≈ 1.5×1.5×2.0 m | Yes | Ground contact at shrine pad |
| `SM_LandingCircle` (+ center + stone ring); optional `_B` | `03_Gatherables` | FBX | `/Game/HomeWorld/Meshes/Gatherables/SM_LandingCircle` | **`UCX_SM_LandingCircle` flat box / cylinder proxy** ≈ 8×8×0.2 m | Yes | Clearing ground plane |
| `SM_Shrine_Return` (+ parts) | `02_Forest` | FBX | `/Game/HomeWorld/Meshes/Forest/SM_Shrine_Return` | **`UCX_SM_Shrine_Return` simple box** ≈ 1.5×1.5×2.0 m (same as homestead shrine) | Yes | Ground contact |
| `SM_Path_Planet_SegA/B/C` | `02_Forest` | FBX | `/Game/HomeWorld/Meshes/Forest/SM_Path_Planet_Seg*` | None / thin | Yes | Path ground |
| `SM_Roof_Hamlet_01/02/03` | `02_Forest` | FBX | `/Game/HomeWorld/Meshes/Forest/SM_Roof_Hamlet_*` | Box optional (silhouette only) | Yes | Ground / pad |
| `SM_Pine_Planet_*` | `02_Forest` | FBX | `/Game/HomeWorld/Meshes/Forest/Pines/SM_Pine_Planet_*` | Capsule optional | Yes | Trunk base |
| `SM_Planet_GroundPlate`, `SM_Planet_ValleyLip_*` | `02_Forest` | FBX | `/Game/HomeWorld/Meshes/Forest/SM_Planet_*` | Use as walk proxy or landscape later | Yes | Ground plane Z |
| `SM_Islet_01/02/03` (+ body/top/torn) | `08_Transit` | FBX | `/Game/HomeWorld/Meshes/Transit/SM_Islet_*` | Box per islet optional | Yes | Islet top / mass center documented |
| `SM_Gather_FirstHarvest`, `SM_BeastPad_01`, `SM_SpiritWound_01` | `02_Forest` / beasts / spirits | FBX | `/Game/HomeWorld/Meshes/...` matching Lib | Simple box / disc OK | Yes | Ground contact |
| `SM_RES_*_World` / `SM_RES_*_Stored` | `03_Gatherables` | FBX | `/Game/HomeWorld/Meshes/Gatherables/SM_RES_*` | Small box / none | Yes | Ground contact |
| `CRUMB_*` empties + `CRUMB_GlideSpline` | `08_Transit` | — (no mesh) | `/Game/HomeWorld/Maps/VS_MVP/Transit/CRUMB_*` | N/A — spline points / TargetPoints | N/A | Keep world transforms |
| `SOCKET_*` empties | parent kits | — | Keep as sockets / SceneComponents under SM_ | N/A | N/A | Local to parent |
| `CAM_Hero`, `CAM_CabinClose`, `CAM_GlideDepart`, `CAM_LandingDay`, `CAM_PortalNight` | `00_Core` | — | `/Game/HomeWorld/Maps/VS_MVP/Cameras/CAM_*` | N/A | N/A | Keep world pose |
| `VS_MARKER_*` | `VS_MVP` | — / GLB optional | `/Game/HomeWorld/Maps/VS_MVP/Markers/VS_MARKER_*` | N/A | N/A | World pose (slice beats) |
| `LIT_*`, `VOLUME_Haze` | `07_Night_SpiritLayer` | — | Recreate under `/Game/HomeWorld/Lighting/...` | N/A | N/A | Match graybox / preset docs |

---

## 3. Collision proxies (MVP — simple boxes)

INT requires **simple box** proxies for interact / land / block-out walk before complex collision:

| Proxy name | Approx size (X×Y×Z m) | Attaches to | Purpose |
|---|---|---|---|
| `UCX_SM_Cabin` | 5.5 × 4.5 × 5.5 | `SM_Cabin` envelope | Block walk-through cabin volume |
| `UCX_SM_Shrine_Homestead` | 1.5 × 1.5 × 2.0 | `SM_Shrine_Homestead` | Interact volume / block |
| `UCX_SM_Shrine_Return` | 1.5 × 1.5 × 2.0 | `SM_Shrine_Return` | Portal B interact / block |
| `UCX_SM_LandingCircle` | 8.0 × 8.0 × 0.2 | `SM_LandingCircle` | Touchdown / land pad read |

Author in Blender as `UCX_` meshes parented (or export-with) the SM_, **or** generate UE box collision of the same sizes on import. Do **not** ship convex hulls for these three interact sites in P6.

---

## 4. Materials (portable cite — not re-authored)

Export meshes with material **slot names** matching masters where possible:

`M_StylizedGrass`, `M_CliffRock`, `M_WoodCabin`, `M_WoodWild`, `M_FoliageCard`, `M_PathStone`, `M_GatherHerb`, `M_BeastStylized`, `M_SpiritUnlit`, `M_Nurtured`

UE: one master material each under `/Game/HomeWorld/Materials/Masters/M_*` + instances. Drive **NightMix** from GameState / time float.

---

## 5. Out of scope

- Dressing `/Game/HomeWorld/Maps/VS_MVP` beyond notes  
- New kits, biomes, masters, free-flight  
- Editing `PHASE_BOARD` or `Docs/07_*` sign-off  

# MVP_EXPORT_MANIFEST.md

**ID:** P6_INT_slice  
**Role:** INT  
**Date:** 2026-09-16  
**Blend:** `blender/floating_island_homestead_LIB.blend`  
**Preset:** STYLE_GUIDE FBX — Forward X, Up Z, FBX Unit Scale, apply scale; meters  

Every FBX written for first UE import staging. Assembly **roots** that are Empties are not mesh-exported; mesh children + UCX are included in the parent FBX name.

| Category | File | Bytes | Contents (mesh objects) |
|---|---|---:|---|
| Homestead | `SM_Cabin.fbx` | 81196 | SM_Cabin_* + UCX_SM_Cabin — **PA-C tranche 2** (1680 tris; rustic log/gable; UCX 5.5×4.5×5.5) |
| Homestead | `SM_Glider_Perch.fbx` | 17148 | SM_Glider_Perch — **PA-C tranche 2** (132 tris; perch/rail) |
| Homestead | `SM_IslandTop.fbx` | 15676 | SM_IslandTop |
| Homestead | `SM_Lookout_Pad.fbx` | 15116 | SM_Lookout_Pad |
| Homestead | `SM_Cliff_LookoutFace.fbx` | 31772 | SM_Cliff_LookoutFace — **PA-C tranche 1** (864 tris, M_CliffRock) |
| Homestead | `SM_Cliff_CabinFace.fbx` | 27548 | SM_Cliff_CabinFace — **PA-C tranche 1** (648 tris, M_CliffRock) |
| Homestead | `SM_Cliff_Rear.fbx` | 25564 | SM_Cliff_Rear — **PA-C tranche 1** (540 tris, M_CliffRock) |
| Homestead | `SM_Pine_Homestead.fbx` | 55612 | SM_Pine_Homestead_{S,M,L}_Trunk/Foliage_* — **PA-C tranche 1** (472 tris; foliage Z-stack fix) |
| Homestead | `SM_PathStone_A.fbx` | 15292 | SM_PathStone_A — **PA-C tranche 2** (24 tris, M_PathStone) |
| Homestead | `SM_PathStone_B.fbx` | 15212 | SM_PathStone_B — **PA-C tranche 2** (20 tris, M_PathStone) |
| Homestead | `SM_PathStone_C.fbx` | 15372 | SM_PathStone_C — **PA-C tranche 2** (28 tris, M_PathStone) |
| Homestead | `SM_Planter_A.fbx` | 19308 | SM_Planter_A — **PA-C tranche 2** (240 tris) |
| Homestead | `SM_Planter_B.fbx` | 20172 | SM_Planter_B — **PA-C tranche 2** (336 tris) |
| Homestead | `SM_Planter_C.fbx` | 19356 | SM_Planter_C — **PA-C tranche 2** (240 tris) |
| Homestead | `SM_Garden_Fence_Seg.fbx` | 15708 | SM_Garden_Fence_Seg — **PA-C tranche 2** (100 tris, M_WoodCabin) |
| Forest | `SM_Planet_GroundPlate.fbx` | 15148 | SM_Planet_GroundPlate |
| Forest | `SM_Roof_Hamlet.fbx` | 35100 | SM_Roof_Hamlet_0{1,2,3}_Body/PitchA/PitchB |
| Forest | `SM_Shrine_Return.fbx` | 29036 | Base/Posts/Lintel/Glow + UCX_SM_Shrine_Return (root Empty) |
| Gatherables | `SM_Gather_FirstHarvest.fbx` | 22508 | SM_Gather_FirstHarvest_Bush_* (root Empty) |
| Gatherables | `SM_LandingCircle.fbx` | 57276 | SM_LandingCircle_Center + Stone_* + UCX_SM_LandingCircle (root Empty; _B omitted) |
| Gatherables | `SM_RES_World.fbx` | 34828 | SM_RES_*_World_Mesh (BERRY/FIBER/HERB/SEED/STONE/WOOD) |
| Gatherables | `SM_Shrine_Homestead.fbx` | 29036 | Base/Posts/Lintel/PortalGlow + UCX_SM_Shrine_Homestead (root Empty) |
| Transit | `SM_Islets.fbx` | 35580 | SM_Islet_0{1,2,3}_Body/Top/Torn (roots Empty) |

**FBX count:** 23  
**Total bytes:** 648564  

**PA-C tranche 1 (2026-09-22 ET):** three cliff assemblies + pine upgrade-in-place. Cliff UE place at graybox origins — see [PA_C_TRANCHE1.md](../../Docs/handoffs/PA_C_TRANCHE1.md).

**PA-C tranche 2 (2026-09-22 ET):** cabin + glider perch upgrade-in-place; path stones ×3, planters ×3, fence segment CREATE. Evidence — [PA_C_TRANCHE2.md](../../Docs/handoffs/PA_C_TRANCHE2.md).

## Sidecar

| `MVP_CRUMB_SPLINE.json` | 21790 bytes | CRUMB_* + CAM_* + VS_MARKER_* + shrine/landing anchors + UCX world transforms |

## UCX proxies (Docs/04 §3) — created in blend, exported with SM_

| Name | Size (m) | Exported with |
|---|---|---|
| `UCX_SM_Cabin` | 5.5 × 4.5 × 5.5 | `Homestead/SM_Cabin.fbx` |
| `UCX_SM_Shrine_Homestead` | 1.5 × 1.5 × 2.0 | `Gatherables/SM_Shrine_Homestead.fbx` |
| `UCX_SM_Shrine_Return` | 1.5 × 1.5 × 2.0 | `Forest/SM_Shrine_Return.fbx` |
| `UCX_SM_LandingCircle` | 8.0 × 8.0 × 0.2 | `Gatherables/SM_LandingCircle.fbx` |

## Missing SM_ names

None of the priority MVP SM_ prefixes were missing from the blend. Assembly **Empty roots** (`SM_Cabin`, `SM_Shrine_*`, `SM_LandingCircle`, `SM_Pine_Homestead_*`, `SM_Islet_*`, `SM_Gather_FirstHarvest`, `SM_Roof_Hamlet_*`) are not themselves mesh objects; mesh children were exported under the assembly FBX name.

## UE destination

`batch_import_asset_creation.py` → `/Game/HomeWorld/Meshes/<Category>/` for Homestead/Forest/Gatherables/Transit/Beasts/Spirits.


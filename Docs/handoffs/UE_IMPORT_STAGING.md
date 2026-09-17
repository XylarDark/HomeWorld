# Handoff: UE_IMPORT_STAGING

**ID:** P6_INT_slice  
**Role:** INT → future UE import / GP  
**Date:** 2026-09-16  
**Status:** STAGING COMPLETE (Blender export + scripts + docs; Unreal not opened on Linux box)

## Delivered

| Item | Path |
|---|---|
| Export helper categories | `AssetCreation/Blender/export_to_asset_creation.py` |
| Batch import Docs/04 paths | `Content/Python/batch_import_asset_creation.py` |
| MVP FBX set | `AssetCreation/Exports/{Homestead,Forest,Gatherables,Transit}/` |
| Crumb / cam / marker JSON | `AssetCreation/Exports/MVP_CRUMB_SPLINE.json` |
| Manifest | `AssetCreation/Exports/MVP_EXPORT_MANIFEST.md` |
| UE first-pass runbook | `Docs/05_UE_IMPORT_FIRST_PASS.md` |
| UCX proxies in blend | `UCX_SM_Cabin`, `UCX_SM_Shrine_Homestead`, `UCX_SM_Shrine_Return`, `UCX_SM_LandingCircle` |

## Import map (Docs/04)

Mesh categories → `/Game/HomeWorld/Meshes/<Category>/`  
Legacy (`Characters`, `Harvestables`, `Dungeon`, `Biomes`) → `/Game/HomeWorld/<Category>/`

## Next (not this handoff)

1. Open `HomeWorld.uproject` in **UE 5.7** (Windows / UE machine)
2. Run `batch_import_asset_creation.py`
3. Place CRUMB/CAM/VS_MARKER TargetPoints from JSON
4. NightMix stub; FALLBACK glide only — **no free-flight**, **no full dress**

## Out of scope (honored)

Unreal Editor on Linux box, Nanite/Lumen, new features, free flight, GitHub PR (Conductor), PHASE_BOARD / Docs/07 edits.

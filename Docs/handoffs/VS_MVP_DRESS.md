# VS_MVP dress — handoff (post Lead SIGN OFF)

**Date:** 2026-09-17  
**Machine:** Windows/UE host (DESKTOP-21CT3H0 or successor)  
**Runbook:** `Docs/06_VS_MVP_DRESS.md`

## Scope

Post-audit **kit dress** for `L_VS_MVP_Markers`: spawn imported StaticMeshes at JSON anchors/CRUMB islets. Markers and cameras from Docs/05 remain; dress actors live under `VS_MVP/Dress` with `DRESS_*` labels.

## Script

`Content/Python/place_vs_mvp_dress.py`

Run after:

1. `batch_import_asset_creation.py` (meshes under `/Game/HomeWorld/Meshes/...`)
2. `place_vs_mvp_markers.py` (level + TargetPoints)

## Out of scope

- Free-flight / glide BP (FALLBACK reminder only)
- `.uasset`/`.umap` in repo
- `Docs/07` or PHASE_BOARD edits

## Verify locally

Output Log `place_vs_mvp_dress: Done`; Outliner folder `VS_MVP/Dress`; island + transit kit visible at anchors.

## Windows dress run (2026-09-17)

First host run on DESKTOP-21CT3H0 placed **74** dress actors; **4 missing** pending mesh-index fix:

- `SM_IslandTop`
- `SM_Lookout_Pad`
- `SM_Glider_Perch`
- `SM_Planet_GroundPlate`

Root cause: `EditorAssetLibrary.list_assets` returns object paths like `/Game/.../SM_IslandTop.SM_IslandTop`; basename parsing must strip the duplicate suffix before prefix/exact matching. Re-run after fix; expect **78** spawned (74 + 4).

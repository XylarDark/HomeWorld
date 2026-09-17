# UE import first-pass — completion note (local)

**Date:** 2026-09-16 / 2026-09-17 ET  
**Machine:** DESKTOP-21CT3H0  

## Done (Docs/05)

1. FBX batch import → `/Game/HomeWorld/Meshes/{Homestead,Forest,Gatherables,Transit}`
2. Level `L_VS_MVP_Markers` with 28 actors: CRUMB_*, VS_MARKER_*, ANCHOR_*, CAM_*
3. MPC `/Game/HomeWorld/Materials/MPC_HomeWorld_Time` (NightMix stub)
4. FALLBACK flight remains armed (scripted glide + portal both ways)

## Caveats

- batch_import returned False once (UCX naming warnings); meshes still imported
- Assemblies exploded to part meshes (Interchange)
- Blender→UE marker axis: Y flipped, ×100 cm — verify in viewport
- Camera rotators are best-effort from Blender euler

## Script

`Content/Python/place_vs_mvp_markers.py`

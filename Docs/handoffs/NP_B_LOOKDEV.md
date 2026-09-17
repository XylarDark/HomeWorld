# NP-B Lookdev apply — handoff

**Date:** 2026-09-17  
**Machine:** Windows/UE host **DESKTOP-21CT3H0**  
**Repo HEAD:** `82c7eb2`  
**Runbook:** [Docs/12b_NP_B_LOOKDEV.md](../12b_NP_B_LOOKDEV.md)

## Scope

Post **NP-A APPROVE**: assign ten Docs/02 masters onto `DRESS_*` StaticMesh actors in `L_VS_MVP_Markers`. Optional NightMix MPC smoke (0 → 0.85). Save level locally — no binary commit.

## Script

`Content/Python/assign_vs_mvp_materials.py`  
Mapping rules (unit-tested): `Content/Python/homeworld_vs_mvp_material_rules.py`

Run after dress chain:

1. `batch_import_asset_creation.py`
2. `create_master_materials.py`
3. `place_vs_mvp_markers.py`
4. `place_vs_mvp_dress.py`
5. **`assign_vs_mvp_materials.py`** ← this handoff

## Hard rules

- Docs/07 CLOSED
- FALLBACK armed (CRUMB glide + portal; no free-flight)
- Exactly 10 masters — no 11th shader
- No V3–V8 in NP-B
- No `.uasset`/`.umap` in git

## Windows run evidence (DESKTOP-21CT3H0, HEAD `82c7eb2`)

| Check | Status | Notes |
|-------|--------|-------|
| Script executed on DESKTOP | **PASS** | `assign_vs_mvp_materials.py` via Editor |
| Output Log `assign_vs_mvp_materials: Done` | **PASS** | See structured result below |
| `actors` count matches dress count | **PASS** | **78** actors (full dress set after island-top fix) |
| `missing_master` = 0 | **PASS** | |
| `unmapped` = 0 | **PASS** | |
| NightMix smoke 0.0 → 0.85 logged | **FAIL** (non-blocking) | `module 'unreal' has no attribute 'KismetMaterialLibrary'` — assign pass unaffected; C++ `ApplyNightMixForPhase` still drives NightMix in PIE. Fix smoke path in follow-up or NP-C. |
| Viewport spot-check (island/cabin/path/shrine glow) | **PASS** (host) | Lead visual sign-off at **`APPROVE NP-B`** |
| Level saved locally (not committed) | **PASS** | `L_VS_MVP_Markers` saved on DESKTOP only |

### Structured result (Output Log)

```
assign_vs_mvp_materials: Done {
  actors: 78,
  slots_assigned: 78,
  slots_skipped: 0,
  missing_master: 0,
  unmapped: 0,
  masters_used: [M_CliffRock, M_FoliageCard, M_GatherHerb, M_PathStone, M_SpiritUnlit, M_StylizedGrass, M_WoodCabin, M_WoodWild]
}
```

### Masters present but unused (expected)

| Master | Status | Reason |
|--------|--------|--------|
| `M_BeastStylized` | **PRESENT**, unused | No `SM_Beast*` in current DRESS set |
| `M_Nurtured` | **PRESENT**, unused | No nurture/crop RES meshes in current DRESS set |

Eight of ten masters applied; all ten remain on host per Docs/02.

## Verify locally (after Windows run)

- Output Log prefix `assign_vs_mvp_materials:`
- Re-run is idempotent (`slots_skipped` increases)
- Markers/cameras unchanged; only `VS_MVP/Dress` materials updated

## Out of scope

- NP-C form swap / walk bounds
- NP-D/E SYS verbs
- NightMix smoke script fix (logged residual — NP-C or follow-up)

## Residual / follow-up

| Item | Owner | Notes |
|------|-------|-------|
| NightMix MPC smoke in `assign_vs_mvp_materials.py` | NP-C or follow-up | Replace `KismetMaterialLibrary` call with UE 5.7–valid Python API |
| PIE NightMix | C++ (landed) | `ApplyNightMixForPhase` — unaffected by smoke failure |

## Gate

**COMPLETE — awaiting Lead `APPROVE NP-B`**

# NP-B Lookdev apply — handoff

**Date:** 2026-09-17  
**Machine:** Windows/UE host (DESKTOP-21CT3H0 or successor)  
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

## Windows run evidence

| Check | Status | Notes |
|-------|--------|-------|
| Script executed on DESKTOP | **PENDING WINDOWS** | Conductor runs after PR merge |
| Output Log `assign_vs_mvp_materials: Done` | **PENDING WINDOWS** | |
| `actors` count matches dress count | **PENDING WINDOWS** | Expect ~78 after island-top fix |
| `missing_master` = 0 | **PENDING WINDOWS** | |
| `unmapped` = 0 | **PENDING WINDOWS** | |
| NightMix smoke 0.0 → 0.85 logged | **PENDING WINDOWS** | |
| Viewport spot-check (island/cabin/path/shrine glow) | **PENDING WINDOWS** | |
| Level saved locally (not committed) | **PENDING WINDOWS** | |

## Verify locally (after Windows run)

- Output Log prefix `assign_vs_mvp_materials:`
- Re-run is idempotent (`slots_skipped` increases)
- Markers/cameras unchanged; only `VS_MVP/Dress` materials updated

## Out of scope

- NP-C form swap / walk bounds
- NP-D/E SYS verbs
- PHASE_BOARD edits by cloud agent after Conductor evidence pass

## Gate

**COMPLETE — awaiting Lead `APPROVE NP-B`** after Conductor fills PENDING WINDOWS rows above.

# Docs/06_VS_MVP_DRESS.md

**ID:** Post-audit VS_MVP dress  
**Role:** INT  
**Date:** 2026-09-17  
**Status:** RUNBOOK — kit dress at markers (post Lead SIGN OFF)  
**Prerequisite:** Docs/05 first-pass DONE on Windows host (`Docs/handoffs/UE_IMPORT_FIRST_PASS_DONE.md`)  
**Do not:** free-flight, Nanite/Lumen gates, `.uasset`/`.umap` in repo, edits to `Docs/07_*` or `PHASE_BOARD`

**Contracts:** `Docs/04_EXPORT_TABLE.md`, `Docs/05_UE_IMPORT_FIRST_PASS.md`  
**Data:** `AssetCreation/Exports/MVP_CRUMB_SPLINE.json` (anchors + `CRUMB_Islet_*`)  
**Script:** `Content/Python/place_vs_mvp_dress.py`

---

## 0. Preconditions

- Unreal Engine **5.7**, HomeWorld open from repo root
- FBX batch import complete → meshes under `/Game/HomeWorld/Meshes/{Homestead,Forest,Gatherables,Transit}/`
- Markers level exists: `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers` (from `place_vs_mvp_markers.py`)
- Run on the **Windows/UE machine** (Linux staging box ships scripts + docs only)

---

## 1. Run dress script

1. Open `L_VS_MVP_Markers` (or let the script load/create it)
2. **Tools → Execute Python Script** → `Content/Python/place_vs_mvp_dress.py`  
   Or via MCP: `execute_python_script("place_vs_mvp_dress.py")`
3. Output Log prefix: `place_vs_mvp_dress:`

**Idempotent:** Re-run destroys actors labeled `DRESS_*` or in folder `VS_MVP/Dress`, then respawns.

---

## 2. Placement map

Axis: Blender m → UE cm, Y flip — `(x×100, −y×100, z×100)` — same as `place_vs_mvp_markers.py`.

| Anchor / CRUMB | Mesh prefix (under Meshes/) | Notes |
|---|---|---|
| `SM_IslandTop` | `SM_IslandTop` | Homestead |
| `SM_Cabin` | `SM_Cabin_*` | All cabin parts |
| `SM_Lookout_Pad` | `SM_Lookout_Pad` | |
| `SM_Glider_Perch` | `SM_Glider_Perch` | |
| `SM_Shrine_Homestead` | `SM_Shrine_Homestead_*` | |
| `SM_LandingCircle` | `SM_LandingCircle_*` | |
| `SM_Shrine_Return` | `SM_Shrine_Return_*` | |
| `CRUMB_Islet_01/02/03` | `SM_Islet_01_*` / `_02_*` / `_03_*` | Transit islet parts |

**Extras (offset from anchor, Blender m):**

| Reference anchor | Mesh prefix | Offset (X, Y, Z) |
|---|---|---|
| `SM_LandingCircle` | `SM_Planet_GroundPlate` | (0, 0, 0) |
| `SM_LandingCircle` | `SM_Gather_FirstHarvest_Bush_*` | (+2, 0, 0) |
| `SM_Shrine_Return` | `SM_Roof_Hamlet_01*` | (0, 0, 0) |
| `SM_Shrine_Return` | `SM_Roof_Hamlet_02*` | (+2, 0, 0) |
| `SM_Shrine_Return` | `SM_Roof_Hamlet_03*` | (−2, 0, 0) |
| `SM_Cabin` | `SM_Pine_Homestead_M_*` | (0, +3, 0) — **optional**, sparse accent |

Skips assets named `UCX_*` or `M_*`. Logs missing prefixes; optional pines do not fail the run.

---

## 3. FALLBACK (transit)

- **Leave island:** scripted glide along `CRUMB_*` only — **no free-flight**
- **Land:** `SM_LandingCircle`
- **Return:** portal both ways `SM_Shrine_Homestead` ↔ `SM_Shrine_Return`

Gameplay BP wiring remains deferred; dress is visual kit only.

---

## 4. Verify

- [ ] Output Log: `place_vs_mvp_dress: Done` with `spawned` > 0
- [ ] World Outliner: folder `VS_MVP/Dress`, labels `DRESS_<meshname>`
- [ ] Island top, cabin, shrines, landing, islets visible at marker anchors
- [ ] Planet ground plate at landing; roof silhouettes near return shrine
- [ ] Markers (`VS_MVP/Markers`, cameras) unchanged
- [ ] Level saved on disk (Windows Content; **not** committed to git)

---

## 5. Explicit non-goals

- Full forest PCG / planet scatter
- Nanite or Lumen acceptance gates
- Free-flight or glide BP implementation
- Committing `.uasset` / `.umap`
- Reopening `Docs/07_VERTICAL_SLICE_SIGN OFF.md`

---

## 6. Related

- First import: [05_UE_IMPORT_FIRST_PASS.md](05_UE_IMPORT_FIRST_PASS.md)
- Handoff: [handoffs/VS_MVP_DRESS.md](handoffs/VS_MVP_DRESS.md)
- Export table: [04_EXPORT_TABLE.md](04_EXPORT_TABLE.md)

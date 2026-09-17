# Docs/05_UE_IMPORT_FIRST_PASS.md

**ID:** P6_INT_slice  
**Role:** INT  
**Date:** 2026-09-16  
**Status:** RUNBOOK — first UE import staging only  
**Do not:** full dress, Nanite/Lumen gates, free-flight, PHASE_BOARD / Docs/07 edits  

**Contracts:** `Docs/04_EXPORT_TABLE.md`, `Docs/04_UE_HANDOFF_NOTES.md`  
**Staging disk:** `AssetCreation/Exports/<Category>/`  
**Manifest:** `AssetCreation/Exports/MVP_EXPORT_MANIFEST.md`  
**Crumb / camera JSON:** `AssetCreation/Exports/MVP_CRUMB_SPLINE.json`

---

## 0. Preconditions

- Unreal Engine **5.7** with HomeWorld project open from repo root: `HomeWorld.uproject`
- This Linux box may not have UE — run this runbook on the Windows/UE machine
- FBX already staged under `AssetCreation/Exports/{Homestead,Forest,Gatherables,Transit}/` (minimum)
- Batch importer: `Content/Python/batch_import_asset_creation.py` (Docs/04 mesh paths)

---

## 1. Open project

1. Launch **UE 5.7**
2. Open `HomeWorld.uproject` from the HomeWorld repo root
3. Wait for shaders / content scan; ignore missing dress assets

---

## 2. Batch import FBX

1. **Tools → Execute Python Script**
2. Select `Content/Python/batch_import_asset_creation.py`
3. Confirm Output Log lines like:
   - `Queued ... -> /Game/HomeWorld/Meshes/Homestead/...`
   - `Queued ... -> /Game/HomeWorld/Meshes/Forest/...`
   - `Queued ... -> /Game/HomeWorld/Meshes/Gatherables/...`
   - `Queued ... -> /Game/HomeWorld/Meshes/Transit/...`
4. Legacy folders (`Characters`, `Harvestables`, `Dungeon`, `Biomes`) still land under `/Game/HomeWorld/<Category>/` if present

**Expected content roots (Docs/04):**

| Exports folder | UE path |
|---|---|
| Homestead | `/Game/HomeWorld/Meshes/Homestead/` |
| Forest | `/Game/HomeWorld/Meshes/Forest/` |
| Gatherables | `/Game/HomeWorld/Meshes/Gatherables/` |
| Transit | `/Game/HomeWorld/Meshes/Transit/` |
| Beasts | `/Game/HomeWorld/Meshes/Beasts/` |
| Spirits | `/Game/HomeWorld/Meshes/Spirits/` |

FBX export used **STYLE_GUIDE** axis (Forward **X**, Up **Z**). If meshes look rotated vs graybox, try UE FBX import **-Y Forward / Z Up** on a re-import pass — do not invent new kits.

UCX boxes ship **inside** the matching SM_ FBX (`UCX_SM_Cabin`, `UCX_SM_Shrine_*`, `UCX_SM_LandingCircle`) per Docs/04 §3.

---

## 3. Map folder + TargetPoints from JSON

1. Create (empty) level / folder: `/Game/HomeWorld/Maps/VS_MVP` (and optional `Transit/`, `Cameras/`, `Markers/` subfolders)
2. Open `AssetCreation/Exports/MVP_CRUMB_SPLINE.json`
3. Place **TargetPoints** (or Empty actors) named 1:1:
   - All `CRUMB_*` (use `CRUMB_order_suggested` for glide order)
   - All `CAM_*` as CameraActors / CineCameraActors with listed world transforms
   - All `VS_MARKER_*`
   - Anchors: `SM_Shrine_Homestead`, `SM_Shrine_Return`, `SM_LandingCircle` (and optional lookout / perch)
4. Units in JSON are **meters**, Blender world (Z up). Convert to UE if your import pipeline flips axes; keep **names identical**

Do **not** fully dress the homestead/forest in this pass — placement markers + imported meshes only.

---

## 4. NightMix stub

- One scalar **NightMix** (0–1) on the ten masters (or a Material Parameter Collection stub)
- Homestead night preview target ≈ **0.85**; day landing / planet ≈ **0**
- **Never** author `_Night` texture sets (`Docs/04_UE_HANDOFF_NOTES.md` §3)
- Wire later from GameState / time float — stub parameter is enough for first pass

---

## 5. FALLBACK note (transit)

- **Leave island:** scripted glide along `CRUMB_*` only (**FALLBACK**). **No free-flight.**
- **Land:** `SM_LandingCircle`
- **Return:** portal both ways `SM_Shrine_Homestead` ↔ `SM_Shrine_Return` (night/spirit)

Evidence / camera reel remains Blender + `Maps/VS_MVP/CAMERA_REEL.md` until a later UE dress wave.

---

## 6. Explicit non-goals (this pass)

- Full set dressing in UE  
- Nanite / Lumen as gates  
- New kits, biomes, combat, inventory UI  
- Editing `PHASE_BOARD` or `Docs/07_*`  
- Opening Unreal on the Linux staging box (exports + scripts + docs only)

---

## 7. Verify

- [ ] FBX under `/Game/HomeWorld/Meshes/{Homestead,Forest,Gatherables,Transit}/`
- [ ] UCX collision proxies present on cabin / shrines / landing
- [ ] TargetPoints named from `MVP_CRUMB_SPLINE.json`
- [ ] NightMix stub exists
- [ ] No full dress claimed

# PA-C Tranche 1 — cliffs + pine foliage (export report)

| Field | Value |
|-------|-------|
| **Status** | **Tranche 1 DONE** — FBX landed on `main` branch PR (cloud land) |
| **Lead gate** | **`APPROVE PA-C`** **GRANTED** (chat, 2026-09-22 ET) — **PA-C IN PROGRESS** (whole track **not CLOSED**) |
| **Handoff** | [PA_C_BLENDER.md](PA_C_BLENDER.md) · [32_PROTOTYPE_ASSETS.md](../32_PROTOTYPE_ASSETS.md) |
| **Host** | DESKTOP Blender → CLOUD land meshes + docs |

---

## Files produced

| File | Bytes | Tris | World size (m) XYZ | Materials |
|---|---:|---:|---|---|
| `Homestead/SM_Cliff_LookoutFace.fbx` | 31772 | 864 | 6.911 × 4.237 × 8.130 | M_CliffRock |
| `Homestead/SM_Cliff_CabinFace.fbx` | 27548 | 648 | 6.137 × 3.872 × 6.142 | M_CliffRock |
| `Homestead/SM_Cliff_Rear.fbx` | 25564 | 540 | 12.312 × 3.109 × 5.522 | M_CliffRock |
| `Homestead/SM_Pine_Homestead.fbx` | 55612 | 472 | 17.500 × 8.600 × 11.714 | M_FoliageCard, M_WoodWild |

Repo paths: `AssetCreation/Exports/Homestead/` (upgrade-in-place pine; new cliff assemblies).

---

## Task 1 — CREATE cliffs

### Naming / canon
- Spec: `Lib/01_Homestead/SM_Cliff.md` + `SM_Cliff.json`
- Graybox assemblies: `SM_Cliff_LookoutFace`, `SM_Cliff_CabinFace`, `SM_Cliff_Rear`
- Material slot: **M_CliffRock** (present on all exported meshes)

### Before (LIB blend)
- Assemblies existed as **EMPTY** parents + pure **box slab/chunk children** (8 verts / 12 tris each).
- LookoutFace: 8 children, **96 tris** total; CabinFace: 6 children, **72 tris**; Rear: 5 children, **60 tris**.
- Silhouette read as stacked pancakes / cylinder-adjacent (boxes only); strata offsets existed but no jagged/undercut.
- Graybox empty origins (meters): Lookout `(7.5, -5.5, -4.0)`, Cabin `(-7.0, -4.5, -3.0)`, Rear `(0.0, 5.0, -2.5)`.

### After
- Each slab: `bmesh` subdivide `cuts=2`, rim-weighted jagged displace, bottom undercut, top lip wobble.
- Children **joined** into one mesh per assembly named to graybox SM_.
- **Origin mode:** portable kit — geometry relative to graybox empty origin; object at `(0,0,0)`. Place in UE at graybox coords.
- Tops land near **local Z ≈ 0** (island rim), bottoms hang down (Lookout ≈ −8 m, Cabin ≈ −6 m, Rear ≈ −5 m).
- Tri counts in env-kit band (~500–2K): **864 / 648 / 540**.

---

## Task 2 — UPGRADE pines

### Before
- Source: prior `SM_Pine_Homestead.fbx`
- All foliage cards sat at **Z ≈ 0** (base), overlapping as a low pancake while trunks rose to ~6.2 / 8.1 / 10.5 m.

### After
- Stacked foliage tiers along each trunk (22%→88% of trunk height).
- Names preserved: `SM_Pine_Homestead_{S,M,L}_Trunk` / `_Foliage_*`
- Materials: `M_FoliageCard`, `M_WoodWild`
- Total tris unchanged: **472**

---

## UE placement (PA-D)

Portable cliff origins — place at graybox (meters, no extra offset):

| Mesh | Place XYZ |
|------|-----------|
| `SM_Cliff_LookoutFace` | `(7.5, -5.5, -4.0)` |
| `SM_Cliff_CabinFace` | `(-7.0, -4.5, -3.0)` |
| `SM_Cliff_Rear` | `(0.0, 5.0, -2.5)` |

---

## Remaining PA-C queue (tranche 2+)

1. ~~Cliffs~~ **DONE (tranche 1)**
2. ~~Pines~~ **DONE (tranche 1)**
3. Cabin → 4. Path → 5. Planters → 6. Fence → 7. Glider perch → 8. Optional island rim

No `Content/*.uasset` in this tranche.

---

## Tooling note

**Date:** 2026-09-22 (America/New_York)  
**Tooling:** Blender 5.2.2 LTS CLI (background)  
**Export preset:** STYLE_GUIDE / `export_to_asset_creation.py` — Forward **X**, Up **Z**, FBX Unit Scale, apply modifiers, Face smoothing

# PA-C Tranche 2 — cabin, path, planters, fence, glider perch (export report)

| Field | Value |
|-------|-------|
| **Status** | **Tranche 2 DONE** — FBX landed on branch (cloud land) |
| **Lead gate** | **`APPROVE PA-C`** **GRANTED** (chat, 2026-09-22 ET) — **PA-C IN PROGRESS** (optional island rim only; whole track **not CLOSED**) |
| **Handoff** | [PA_C_BLENDER.md](PA_C_BLENDER.md) · [32_PROTOTYPE_ASSETS.md](../32_PROTOTYPE_ASSETS.md) |
| **Host** | DESKTOP Blender → CLOUD land meshes + docs |

Repo paths: `AssetCreation/Exports/Homestead/` (upgrade-in-place cabin + glider perch; new path/planter/fence meshes).

---

# PA-C Second Tranche Report — HomeWorld Homestead

**Date:** 2026-09-22 (America/New_York)
**Lead:** **`APPROVE PA-C`** granted (second tranche)
**Tooling:** Blender 5.2.2 LTS CLI (background)
**Source LIB:** `blender/floating_island_homestead_LIB.blend` (from `origin/main` → `/workspace/pa-c-src/`)
**Also used:** `AssetCreation/Exports/Homestead/SM_Cabin.fbx`, `SM_Glider_Perch.fbx`; `AssetCreation/Blender/export_to_asset_creation.py`; `Lib/01_Homestead` CABIN_MODULES / GARDEN_BLOCKING
**Export preset:** STYLE_GUIDE / `export_to_asset_creation.py` — Forward **X**, Up **Z**, FBX Unit Scale, apply modifiers, Face smoothing
**Output root:** `/workspace/pa-c-exports2/` (staging) → landed `AssetCreation/Exports/Homestead/`

---

## Files produced

| File | Bytes | Tris | Bounds XYZ (m) | Materials |
|---|---:|---:|---|---|
| `Homestead/SM_Cabin.fbx` | 81196 | 1680 | 5.95 × 6.4 × 5.7 | M_CliffRock, M_WoodCabin, M_WoodCabin_Window |
| `Homestead/SM_PathStone_A.fbx` | 15292 | 24 | 0.933 × 0.908 × 0.099 | M_PathStone |
| `Homestead/SM_PathStone_B.fbx` | 15212 | 20 | 0.889 × 0.743 × 0.086 | M_PathStone |
| `Homestead/SM_PathStone_C.fbx` | 15372 | 28 | 0.639 × 0.682 × 0.088 | M_PathStone |
| `Homestead/SM_Planter_A.fbx` | 19308 | 240 | 1.2 × 0.6 × 0.873 | M_GatherHerb, M_StylizedGrass, M_WoodCabin |
| `Homestead/SM_Planter_B.fbx` | 20172 | 336 | 1.0 × 0.55 × 0.841 | M_Nurtured, M_StylizedGrass, M_WoodCabin |
| `Homestead/SM_Planter_C.fbx` | 19356 | 240 | 0.8 × 0.5 × 0.773 | M_GatherHerb, M_StylizedGrass, M_WoodCabin |
| `Homestead/SM_Garden_Fence_Seg.fbx` | 15708 | 100 | 1.18 × 0.069 × 0.7 | M_WoodCabin |
| `Homestead/SM_Glider_Perch.fbx` | 17148 | 132 | 2.0 × 1.5 × 0.452 | M_WoodCabin |

Paths:
- `/workspace/pa-c-exports2/Homestead/SM_Cabin.fbx`
- `/workspace/pa-c-exports2/Homestead/SM_PathStone_A.fbx`
- `/workspace/pa-c-exports2/Homestead/SM_PathStone_B.fbx`
- `/workspace/pa-c-exports2/Homestead/SM_PathStone_C.fbx`
- `/workspace/pa-c-exports2/Homestead/SM_Planter_A.fbx`
- `/workspace/pa-c-exports2/Homestead/SM_Planter_B.fbx`
- `/workspace/pa-c-exports2/Homestead/SM_Planter_C.fbx`
- `/workspace/pa-c-exports2/Homestead/SM_Garden_Fence_Seg.fbx`
- `/workspace/pa-c-exports2/Homestead/SM_Glider_Perch.fbx`

---

## Task 1 — UPGRADE Cabin

### Before
- LIB / prior FBX: modular **box** children (8 verts / 12 tris each) under `SM_Cabin` empty.
- Envelope matched graybox but read as stacked crates, not rustic log/gabled.
- Window panes already used `M_WoodCabin_Window` (kept — emissive-ready warm slot).
- `UCX_SM_Cabin` **5.5 × 4.5 × 5.5** present — preserved.

### After
- Stacked **6-gon log** walls with door/window gaps; corner posts; stone foundation + corner blocks (`M_CliffRock`).
- Proper **gabled** roof planes + triangular gable fills; chimney with cap.
- Porch deck / posts / rails; plank door; warm panes (`M_WoodCabin_Window`).
- Portable kit origin: cabin root at `(0,0,0)` local; place in UE at `SOCKET_Cabin` (−6, 1, 0).
- Export tris **1680**, bounds **[5.95, 6.4, 5.7]** (demo-low band ~500–3K).
- UCX bounds **[5.5, 4.5, 5.5]** (lock 5.5×4.5×5.5).

---

## Task 2 — CREATE Path stones

- LIB had box tiles `SM_PathStone_{A,B,C}_*`; authored irregular low-poly stone tiles ~1 m.
- Material: **M_PathStone**.
- Exports: `SM_PathStone_A.fbx`, `SM_PathStone_B.fbx`, `SM_PathStone_C.fbx`.

---

## Task 3 — CREATE Planters ×3

- From LIB box `SM_Planter_A/B/C`; upgraded raised wood beds + soil (`M_StylizedGrass`) + plant proxies (`M_GatherHerb` / `M_Nurtured`).
- Naming per PA-C brief (`SM_Planter_*`). LIB also has larger `SM_GardenBed_*` blocking (not re-exported this tranche).

---

## Task 4 — CREATE Fence

- Missing from LIB → authored `SM_Garden_Fence_Seg` post-and-rail (~1.2 × 0.08 × 0.7), `M_WoodCabin`.
- Export tris **100**, bounds **[1.18, 0.069, 0.7]**.

---

## Task 5 — UPGRADE Glider perch

- Before: single box 2×1.5×0.5.
- After: plank platform + side rails + front perch cylinder + posts; footprint kept ~2×1.5×0.5.
- Export tris **132**, bounds **[2.0, 1.5, 0.452]**, `M_WoodCabin`.
- `SOCKET_BeastPerch` retained when present in scene graph.

---

## Blockers

- None.

---

## Notes

- No git commit (per brief).
- First-tranche cliffs/pines remain under `/workspace/pa-c-exports/Homestead/`.
- Style: handmade rustic, stylized low-poly (SMG-like); no photoreal / sci-fi.
- Material masters cited: `M_WoodCabin`, `M_WoodCabin_Window`, `M_CliffRock`, `M_PathStone`, `M_StylizedGrass`, `M_GatherHerb`, `M_Nurtured`.

# Task: Apply PCG forest to the map

**Goal:** Apply a procedural forest (trees, optional rocks) to the Main map around the medieval village using PCG.

**Status:** Verified in PIE — 1161 static mesh actors generated in scene. Visual check recommended.

---

## What's already done (programmatic)

- PCG graph created at `/Game/HomeWorld/PCG/ForestIsland_PCG` with: Surface Sampler -> Density Filter -> Difference (exclusion) -> Transform Points -> Static Mesh Spawner.
- PCG Volume placed in level, **auto-sized to match the full landscape** (403m x 342m).
- **Dynamic village exclusion zones**: script scans all StylizedProvencal structure actors (buildings, walls, props), computes a bounding box using 10th/90th percentile to exclude outliers, and adds 500cm padding. Trees don't spawn inside the village.
- Tree meshes: `SM_Tree_01`, `SM_Tree_02`, `SM_Tree_03`, `SM_Tree_Cypress` (Stylized Provencal).
- Rock meshes: `SMF_Forest_Rock_1` through `_4`, `SM_Rock_Small_01` through `_03` (optional second branch).
- Scripts: `create_demo_map.py` (orchestrator), `create_pcg_forest.py` (graph + volume logic).
- All scripts are idempotent: existing PCG graph and volumes are reused or cleaned up before recreation.
- `importlib.reload()` used in orchestrator scripts to pick up disk changes.
- `EditorLevelLibrary.destroy_actor()` used for reliable volume cleanup.

## Remaining manual steps

### Step 1 — Verify in Editor

PIE automated check (2026-02-22): **1161 static mesh actors** found in the PIE world, confirming PCG forest generation is active.

1. Open the Main level in the Editor.
2. Check the viewport — trees and rocks should cover the landscape around the village.
3. The village area (buildings, walls, props) should be clear of trees.
4. Check the Output Log for any PCG errors.

### Step 2 — Re-run if needed

If the forest isn't visible or needs changes:
- **Via MCP:** `execute_python_script("create_demo_map.py")`
- **Via Editor:** Tools > Execute Python Script > `Content/Python/create_demo_map.py`

### Step 3 — Customize (optional)

- **Change tree/rock meshes:** Edit `Content/Python/pcg_forest_config.json` and re-run.
- **Adjust exclusion zones:** Edit `exclusion_zones` in `Content/Python/demo_map_config.json` (or leave empty for auto-detection).
- **Enable World Partition:** Window > World Settings > enable World Partition > save.

---

## Config reference

### demo_map_config.json

- `demo_level_path`: Target level (default `/Game/HomeWorld/Maps/Main`).
- `template_level_path`: Source level to duplicate if Main is missing.
- `volume_center/extent`: Fallback PCG volume bounds (used only when no Landscape exists).
- `exclusion_zones`: Array of dead zones. If empty, the script auto-detects village buildings.

### pcg_forest_config.json

- `static_mesh_spawner_meshes`: Tree mesh paths.
- `static_mesh_spawner_meshes_rocks`: Rock mesh paths (empty = skip rocks).
- `height_filter_min/max`: Optional terrain-only Z filter.

---

## Reference

- PCG volume sized to landscape via `get_actor_bounds(False)` (UE 5.7 tuple-return API).
- Village detection: scans StaticMeshActors with StylizedProvencal meshes, excludes trees/rocks/clouds, uses 10th/90th percentile for robust bounding.
- Node flow: Input > Surface Sampler > Density Filter > Difference > Transform Points > Static Mesh Spawner > Output.

# MVP PIE and tutorial verification (assets + environment)

**Purpose:** Log-driven checklist after changing meshes, PCG, or DemoMap layout. Confirms **automation track** (PIE harness) and points to **MVP tutorial** console steps.

**Prerequisites:** Unreal Editor open with the HomeWorld project, MCP connected if you run scripts from Cursor.

---

## 1. Import pipeline (after adding FBX/GLB to `AssetCreation/Exports/`)

1. Run **`batch_import_asset_creation.py`** (Tools → Execute Python Script, or MCP `execute_python_script("batch_import_asset_creation.py")`).
2. Confirm Output Log prefix `batch_import_asset_creation:` lists imported tasks and no fatal import errors.
3. In Content Browser, verify new static meshes under `/Game/HomeWorld/<Category>/` matching export file names.

---

## 2. PCG lock (MVP track)

1. Open **ForestIsland_PCG**; ensure **Get Landscape Data** uses tag **`PCG_Landscape`** (and load World Partition cells per [Maps/DEMO_MAP.md](../Maps/DEMO_MAP.md)).
2. Tree and rock **Static Mesh Spawner** lists must match **`pcg_forest_config.json`** (`static_mesh_spawner_meshes`, `static_mesh_spawner_meshes_rocks`).
3. Select PCG volume → **Generate** → save level.

---

## 3. `pie_test_runner.py` (automation track)

1. With DemoMap in a good state, run **`pie_test_runner.py`** via MCP or Editor.
2. Read **`Saved/pie_test_results.json`** — confirm checks such as PIE active, character spawned, skeletal mesh, anim instance, PCG static mesh actor count as expected for your map.

---

## 4. Tutorial loop (MVP track, high level)

With PIE on **DemoMap** (Day phase as required by each step), use **`docs/CONSOLE_COMMANDS.md`** — Tutorial (Lists 2–13) sections for:

- Meals, love task, game with child, gather, bed, spectral, combat, boss, tutorial end.

Partner and child **in-world** checks require placeholders placed (`place_partner.py`, `place_child.py`) per **`demo_map_config.json`** positions.

---

## 5. Marketing-ready gate (optional same session)

Capture 2–5 screenshots from the homestead “beautiful corner” and note framing in [VisionBoard/MVP/VERTICAL_SLICE_CHECKLIST.md](../../VisionBoard/MVP/VERTICAL_SLICE_CHECKLIST.md).

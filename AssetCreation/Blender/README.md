# Blender sources and helpers

- **`.blend` files** — optional project files (large; may be gitignored).
- **`export_to_asset_creation.py`** — STYLE_GUIDE-aligned FBX/GLB export into `../Exports/<Category>/`.
- **`apply_island_plate.py`** — rewrites the `SM_IslandTop` rim to the locked 180 × 100 m footprint. Run headless from the repo root:

  ```
  blender --background blender/floating_island_homestead_LIB.blend \
          --python AssetCreation/Blender/apply_island_plate.py
  ```

  It saves the `.blend` only if every invariant holds (extent exact, top datum at Z 0, crust 0.3–0.6 m, the locked 90 × 50 m walk oval still inside the rim, homestead core not clipped, rim still visibly torn). Otherwise it prints `PLATE_ABORT`, exits non-zero and leaves the file untouched. The rim silhouette is the `RIM` table at the top of the file — round numbers on purpose, so one value can be moved by hand and the run re-verified.

  To check a change to the mesh against the specs, regenerate the report with `Content/Python/graybox_report_driver.py` (same headless invocation, different `--python`).

## Quick export (Blender)

1. Select mesh(es), apply transforms if needed.
2. Scripting workspace → Open `export_to_asset_creation.py` → Run Script  
   (or via blender-mcp: execute the file / call `export_fbx(...)`).
3. Default writes `AssetCreation/Exports/Homestead/export.fbx`.

Then in Unreal (MCP): `execute_python_script("batch_import_asset_creation.py")`.

See [../README.md](../README.md) and [../STYLE_GUIDE.md](../STYLE_GUIDE.md).

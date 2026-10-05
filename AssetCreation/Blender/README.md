# Blender sources and helpers

- **`.blend` files** — optional project files (large; may be gitignored).
- **`export_to_asset_creation.py`** — STYLE_GUIDE-aligned FBX/GLB export into `../Exports/<Category>/`.
- **`apply_island_plate.py`** — rewrites the `SM_IslandTop` rim to the locked 180 × 100 m footprint. Run headless from the repo root:

  ```
  & "C:\Program Files\Mixar\mixar.exe" --background blender/floating_island_homestead_LIB.blend `
          --python AssetCreation/Blender/apply_island_plate.py
  ```

  Mixar is the default 3D tool (a Blender 4.2.2 fork), so the binary is `mixar.exe`, not `blender.exe`. Use the full path as shown: a bare `blender` on `PATH` would silently run vanilla Blender 4.4 instead.

  > `.blend` warning: Mixar writes a **4.2-era** file. `floating_island_homestead_LIB.blend` was authored by Blender 5.2, so opening it in Mixar logs `WARNING File written by newer Blender binary, expect loss of data!`. This script **saves** the file when its invariants hold — run it against a copy, or re-author in Mixar, rather than letting a Mixar run downgrade the 5.2 source. See [docs/KNOWN_ERRORS.md](../../docs/KNOWN_ERRORS.md).

  It saves the `.blend` only if every invariant holds (extent exact, top datum at Z 0, crust 0.3–0.6 m, the locked 90 × 50 m walk oval still inside the rim, homestead core not clipped, rim still visibly torn). Otherwise it prints `PLATE_ABORT`, exits non-zero and leaves the file untouched. The rim silhouette is the `RIM` table at the top of the file — round numbers on purpose, so one value can be moved by hand and the run re-verified.

  To check a change to the mesh against the specs, regenerate the report with `Content/Python/graybox_report_driver.py` (same headless invocation, different `--python`).

## Quick export (Blender)

1. Select mesh(es), apply transforms if needed.
2. Scripting workspace → Open `export_to_asset_creation.py` → Run Script  
   (or via blender-mcp: execute the file / call `export_fbx(...)`).
3. Default writes `AssetCreation/Exports/Homestead/export.fbx`.

Then in Unreal (MCP): `execute_python_script("batch_import_asset_creation.py")`.

See [../README.md](../README.md) and [../STYLE_GUIDE.md](../STYLE_GUIDE.md).

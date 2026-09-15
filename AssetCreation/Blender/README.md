# Blender sources and helpers

- **`.blend` files** — optional project files (large; may be gitignored).
- **`export_to_asset_creation.py`** — STYLE_GUIDE-aligned FBX/GLB export into `../Exports/<Category>/`.

## Quick export (Blender)

1. Select mesh(es), apply transforms if needed.
2. Scripting workspace → Open `export_to_asset_creation.py` → Run Script  
   (or via blender-mcp: execute the file / call `export_fbx(...)`).
3. Default writes `AssetCreation/Exports/Homestead/export.fbx`.

Then in Unreal (MCP): `execute_python_script("batch_import_asset_creation.py")`.

See [../README.md](../README.md) and [../STYLE_GUIDE.md](../STYLE_GUIDE.md).

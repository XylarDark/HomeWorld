# create_milady_pastel_material.py
# Run from Unreal Editor (Tools -> Execute Python Script or via MCP execute_python_script).
# Creates a simple Milady Pastel master material (bubblegum default) per MILADY_IMPORT_ROADMAP.
# Idempotent: skips creation if asset already exists.
# Palette: #FFB3D1 bubblegum, #E0BBE4 lilac, #A8E6CF mint.

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

MATERIAL_PATH = "/Game/HomeWorld/Milady/Materials"
MATERIAL_NAME = "M_MiladyPastel"


def _log(msg):
    unreal.log("MiladyPastel: " + str(msg))
    print("MiladyPastel: " + str(msg))


def main():
    editor_asset_lib = unreal.EditorAssetLibrary()
    asset_path = MATERIAL_PATH + "/" + MATERIAL_NAME
    if editor_asset_lib.does_asset_exist(asset_path):
        _log("Exists " + asset_path + " (skipping)")
        return

    # Ensure directory exists
    if not editor_asset_lib.does_directory_exist(MATERIAL_PATH):
        editor_asset_lib.make_directory(MATERIAL_PATH)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.MaterialFactoryNew()
    if not factory:
        _log("MaterialFactoryNew not found; create M_MiladyPastel manually in Editor.")
        return

    mat = asset_tools.create_asset(MATERIAL_NAME, MATERIAL_PATH, unreal.Material, factory)
    if not mat:
        _log("Failed to create " + MATERIAL_NAME)
        return

    editor_asset_lib.save_asset(asset_path)
    _log("Created " + asset_path + ". Open in Editor: add Base Color (bubblegum #FFB3D1, lilac #E0BBE4, mint #A8E6CF) or VectorParameter for instances.")


if __name__ == "__main__":
    main()

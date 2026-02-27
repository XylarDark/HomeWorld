# ensure_milady_folders.py
# Run from Unreal Editor (Tools -> Execute Python Script or via MCP execute_python_script).
# Ensures Content paths for the Milady character import pipeline exist per CONTENT_LAYOUT.md.
# Idempotent: safe to run multiple times.

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    raise

PATHS = [
    "/Game/HomeWorld/Milady/Meshes",
    "/Game/HomeWorld/Milady/Materials",
    "/Game/HomeWorld/Milady/Animations",
    "/Game/HomeWorld/Milady/Blueprints",
]


def main():
    editor_asset_lib = unreal.EditorAssetLibrary()
    for path in PATHS:
        if not editor_asset_lib.does_directory_exist(path):
            editor_asset_lib.make_directory(path)
            unreal.log("Milady folders: Created " + path)
        else:
            unreal.log("Milady folders: Exists " + path)
    unreal.log("Milady folders: Done.")


if __name__ == "__main__":
    main()

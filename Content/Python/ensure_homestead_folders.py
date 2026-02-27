# ensure_homestead_folders.py
# Run from Unreal Editor (Tools -> Execute Python Script or via MCP execute_python_script).
# Ensures Content paths for the Homestead map exist per CONTENT_LAYOUT.md and HOMESTEAD_MAP.md.
# Idempotent: safe to run multiple times.

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    raise

HOMESTEAD_PATHS = [
    "/Game/HomeWorld/Homestead",
    "/Game/HomeWorld/Homestead/Structures",
    "/Game/HomeWorld/Homestead/Placeholders",
]


def main():
    editor_asset_lib = unreal.EditorAssetLibrary()
    for path in HOMESTEAD_PATHS:
        if not editor_asset_lib.does_directory_exist(path):
            editor_asset_lib.make_directory(path)
            unreal.log("Homestead folders: Created " + path)
        else:
            unreal.log("Homestead folders: Exists " + path)
    unreal.log("Homestead folders: Done.")


if __name__ == "__main__":
    main()

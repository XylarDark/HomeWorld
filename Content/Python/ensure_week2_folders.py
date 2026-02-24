# ensure_week2_folders.py
# Run from Unreal Editor (Tools -> Execute Python Script or via MCP execute_python_script).
# Ensures Content paths for Week 2 (Mass, AI, ZoneGraph, SmartObjects) exist per CONTENT_LAYOUT.md.
# Idempotent: safe to run multiple times.

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    raise

PATHS = [
    "/Game/HomeWorld/Mass",
    "/Game/HomeWorld/AI",
    "/Game/HomeWorld/ZoneGraph",
    "/Game/HomeWorld/SmartObjects",
    "/Game/HomeWorld/Building",
]

def main():
    editor_asset_lib = unreal.EditorAssetLibrary()
    for path in PATHS:
        if not editor_asset_lib.does_directory_exist(path):
            editor_asset_lib.make_directory(path)
            unreal.log("Week2 folders: Created " + path)
        else:
            unreal.log("Week2 folders: Exists " + path)
    unreal.log("Week2 folders: Done.")

if __name__ == "__main__":
    main()

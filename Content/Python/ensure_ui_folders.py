# ensure_ui_folders.py
# Run from Unreal Editor (Tools -> Execute Python Script or via MCP).
# Idempotent: ensures /Game/HomeWorld/UI exists for main menu and character widgets (WBP_MainMenu, WBP_CharacterCreate).
# See docs/CHARACTER_GENERATION_AND_CUSTOMIZATION.md.

try:
    import unreal
except ImportError:
    import sys
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)


def _log(msg):
    unreal.log("UI folders: " + str(msg))
    print("UI folders: " + str(msg))


def main():
    base = "/Game/HomeWorld/UI"
    if not unreal.EditorAssetLibrary.does_directory_exist(base):
        unreal.EditorAssetLibrary.make_directory(base)
        _log("Created " + base)
    else:
        _log("Already exists: " + base)
    _log("Done. Create WBP_MainMenu and WBP_CharacterCreate here (parent classes: HomeWorldMainMenuWidget, UserWidget).")


if __name__ == "__main__":
    main()

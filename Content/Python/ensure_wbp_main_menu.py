# ensure_wbp_main_menu.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Create-if-missing: WBP_MainMenu in /Game/HomeWorld/UI with parent HomeWorldMainMenuWidget.
# Idempotent. Buttons (Play, Character, Options, Quit) must be added in Editor and bound to
# OnPlayClicked, OnCharacterClicked, OnOptionsClicked, OnQuitClicked. See docs/CHARACTER_GENERATION_AND_CUSTOMIZATION.md.

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

WIDGET_NAME = "WBP_MainMenu"
UI_PATH = "/Game/HomeWorld/UI"
WIDGET_FULL = UI_PATH + "/" + WIDGET_NAME


def _log(msg):
    unreal.log("WBP_MainMenu: " + str(msg))
    print("WBP_MainMenu: " + str(msg))


def main():
    _log("Start.")
    # Ensure UI folder exists
    if not unreal.EditorAssetLibrary.does_directory_exist(UI_PATH):
        unreal.EditorAssetLibrary.make_directory(UI_PATH)
        _log("Created " + UI_PATH)

    if unreal.EditorAssetLibrary.does_asset_exist(WIDGET_FULL):
        _log("Already exists: " + WIDGET_FULL + ". Open in Editor to add buttons and bind OnPlayClicked, OnCharacterClicked, OnOptionsClicked, OnQuitClicked.")
        _log("Done.")
        return

    # Try Widget Blueprint factory (UE 5.7 Python API)
    factory = None
    for name in ("WidgetBlueprintFactory", "WidgetBlueprintFactoryNew", "UserWidgetBlueprintFactory"):
        cls = getattr(unreal, name, None)
        if cls:
            try:
                factory = cls()
                _log("Using factory: " + name)
                break
            except Exception as e:
                _log("Factory " + name + ": " + str(e))
    if not factory:
        _log("No Widget Blueprint factory found. Create WBP_MainMenu manually: Content Browser -> /Game/HomeWorld/UI -> Right-click -> User Interface -> Widget Blueprint, name WBP_MainMenu; Class Settings -> Parent Class -> HomeWorldMainMenuWidget. See CHARACTER_GENERATION_AND_CUSTOMIZATION.md §2.")
        _log("Done.")
        return

    parent_class = None
    try:
        parent_class = unreal.load_class(None, "/Script/HomeWorld.HomeWorldMainMenuWidget")
    except Exception:
        pass
    if not parent_class:
        try:
            mod = getattr(unreal, "HomeWorld", None)
            if mod:
                cls = getattr(mod, "HomeWorldMainMenuWidget", None)
                if cls and hasattr(cls, "static_class"):
                    parent_class = cls.static_class()
        except Exception:
            pass
    if not parent_class:
        _log("Could not find HomeWorldMainMenuWidget. Ensure C++ is compiled. Create WBP_MainMenu manually with Parent Class HomeWorldMainMenuWidget.")
        _log("Done.")
        return

    try:
        factory.set_editor_property("parent_class", parent_class)
    except Exception as e:
        _log("Could not set parent_class on factory: " + str(e) + ". Widget may be created with default UserWidget; reparent in Editor (Class Settings -> Parent Class -> HomeWorldMainMenuWidget).")

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    try:
        widget_bp = asset_tools.create_asset(WIDGET_NAME, UI_PATH, None, factory)
    except Exception as e:
        _log("create_asset failed: " + str(e))
        _log("Create WBP_MainMenu manually per CHARACTER_GENERATION_AND_CUSTOMIZATION.md §2.")
        return

    if not widget_bp:
        _log("create_asset returned None. Create WBP_MainMenu manually per CHARACTER_GENERATION_AND_CUSTOMIZATION.md §2.")
        return

    try:
        unreal.EditorAssetLibrary.save_loaded_asset(widget_bp)
    except Exception:
        pass
    _log("Created " + WIDGET_FULL + ". Open in Editor: add Canvas Panel, Vertical Box, four Buttons (Play, Character, Options, Quit); bind each On Clicked to OnPlayClicked, OnCharacterClicked, OnOptionsClicked, OnQuitClicked. See CHARACTER_GENERATION_AND_CUSTOMIZATION.md §2.")
    _log("Done.")


if __name__ == "__main__":
    main()

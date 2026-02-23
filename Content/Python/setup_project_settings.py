# setup_project_settings.py
# Run from Unreal Editor: Tools -> Execute Python Script.
# Configures project-level settings:
#   - GlobalDefaultGameMode -> HomeWorldGameMode (or BP child)
#   - Default map -> /Game/HomeWorld/Maps/Main
#   - DefaultPawnClass on the GameMode -> BP_HomeWorldCharacter (if it exists)

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

GAME_MODE_C = "/Script/HomeWorld.HomeWorldGameMode"
GAME_MODE_BP = "/Game/HomeWorld/GameMode/BP_GameMode.BP_GameMode_C"
DEFAULT_MAP = "/Game/HomeWorld/Maps/Main"
CHARACTER_BP = "/Game/HomeWorld/Characters/BP_HomeWorldCharacter"


def _log(msg):
    unreal.log("ProjectSettings: " + str(msg))
    print("ProjectSettings: " + str(msg))


def _set_default_game_mode():
    """Set GlobalDefaultGameMode in Project Settings (Maps & Modes)."""
    try:
        settings = unreal.GameMapsSettings.get_game_maps_settings()
    except Exception:
        _log("GameMapsSettings not available; set default game mode in Editor > Project Settings > Maps & Modes.")
        return

    gm_path = GAME_MODE_BP
    if not unreal.EditorAssetLibrary.does_asset_exist(GAME_MODE_BP.replace("_C", "").rsplit(".", 1)[0]):
        gm_path = GAME_MODE_C

    try:
        settings.set_editor_property("global_default_game_mode", unreal.SoftClassPath(gm_path))
        _log("Set GlobalDefaultGameMode = " + gm_path)
    except Exception as e:
        _log("Could not set GlobalDefaultGameMode: " + str(e))


def _set_default_map():
    """Set GameDefaultMap and EditorStartupMap in Project Settings."""
    try:
        settings = unreal.GameMapsSettings.get_game_maps_settings()
    except Exception:
        return

    map_path = unreal.SoftObjectPath(DEFAULT_MAP)
    try:
        settings.set_editor_property("game_default_map", map_path)
        _log("Set GameDefaultMap = " + DEFAULT_MAP)
    except Exception as e:
        _log("Could not set GameDefaultMap: " + str(e))

    try:
        settings.set_editor_property("editor_startup_map", map_path)
        _log("Set EditorStartupMap = " + DEFAULT_MAP)
    except Exception as e:
        pass


def _set_default_pawn_class():
    """Set DefaultPawnClass on the GameMode to BP_HomeWorldCharacter if it exists."""
    bp_asset_path = CHARACTER_BP
    if not unreal.EditorAssetLibrary.does_asset_exist(bp_asset_path):
        _log("BP_HomeWorldCharacter not found at " + bp_asset_path + "; DefaultPawnClass unchanged (C++ default is AHomeWorldCharacter).")
        return

    bp_asset = unreal.load_asset(bp_asset_path)
    if not bp_asset:
        return

    bp_class = None
    try:
        bp_class = bp_asset.generated_class()
    except Exception:
        pass
    if not bp_class:
        try:
            bp_class = bp_asset.get_editor_property("generated_class")
        except Exception:
            pass
    if not bp_class:
        _log("Could not get generated class from " + bp_asset_path + "; set DefaultPawnClass in Editor.")
        return

    gm_class = None
    try:
        gm_class = unreal.HomeWorldGameMode.static_class()
    except (AttributeError, Exception):
        pass
    if not gm_class:
        try:
            gm_class = unreal.load_class(None, "/Script/HomeWorld.HomeWorldGameMode")
        except Exception:
            pass

    if gm_class:
        try:
            cdo = unreal.get_default_object(gm_class)
            cdo.set_editor_property("default_pawn_class", bp_class)
            _log("Set DefaultPawnClass on HomeWorldGameMode = " + bp_asset_path)
            return
        except Exception as e:
            _log("CDO set failed: " + str(e))

    gm_bp_path = GAME_MODE_BP.replace("_C", "").rsplit(".", 1)[0]
    if unreal.EditorAssetLibrary.does_asset_exist(gm_bp_path):
        gm_bp = unreal.load_asset(gm_bp_path)
        if gm_bp:
            try:
                gm_gen = gm_bp.generated_class() if hasattr(gm_bp, "generated_class") else gm_bp.get_editor_property("generated_class")
                cdo = unreal.get_default_object(gm_gen)
                cdo.set_editor_property("default_pawn_class", bp_class)
                _log("Set DefaultPawnClass on BP_GameMode = " + bp_asset_path)
                unreal.EditorAssetLibrary.save_loaded_asset(gm_bp)
                return
            except Exception as e:
                _log("BP GameMode CDO set failed: " + str(e))

    _log("Could not set DefaultPawnClass programmatically; set in Editor on the GameMode Blueprint.")


def main():
    _log("Configuring project settings...")
    _set_default_game_mode()
    _set_default_map()
    _set_default_pawn_class()
    _log("Done. Verify in Project Settings > Maps & Modes.")


if __name__ == "__main__":
    main()

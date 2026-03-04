# create_so_wall_builder.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Creates SO_WallBuilder (Smart Object definition) and DA_SO_WallBuilder_Behavior in /Game/HomeWorld/Building/.
# Assigns the behavior to SO_WallBuilder Default Behavior Definitions (fixes validation; no experimental plugin).
# Idempotent. After running: set Slots to 2, add BuildWall interaction if needed. See docs/KNOWN_ERRORS.md.

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

ASSET_NAME = "SO_WallBuilder"
BEHAVIOR_ASSET_NAME = "DA_SO_WallBuilder_Behavior"
ASSET_PATH = "/Game/HomeWorld/Building"
ASSET_FULL = ASSET_PATH + "/" + ASSET_NAME
BEHAVIOR_ASSET_FULL = ASSET_PATH + "/" + BEHAVIOR_ASSET_NAME


def _log(msg):
    unreal.log("SO_WallBuilder: " + str(msg))
    print("SO_WallBuilder: " + str(msg))


def _ensure_behavior_asset(asset_tools):
    """Create DA_SO_WallBuilder_Behavior if missing (class is UObject-based, so not in Data Asset menu)."""
    if unreal.EditorAssetLibrary.does_asset_exist(BEHAVIOR_ASSET_FULL):
        _log("Reusing behavior asset: " + BEHAVIOR_ASSET_FULL)
        return unreal.EditorAssetLibrary.load_asset(BEHAVIOR_ASSET_FULL)
    behavior_class = unreal.load_class(None, "/Script/HomeWorld.HomeWorldSmartObjectBehaviorDefinition")
    if not behavior_class:
        _log("HomeWorldSmartObjectBehaviorDefinition not found. Build the project and restart Editor.")
        return None
    # Factory=None works for UObject-derived assets; DataAssetFactory is for UDataAsset only.
    asset = asset_tools.create_asset(BEHAVIOR_ASSET_NAME, ASSET_PATH, behavior_class, None)
    if asset:
        unreal.EditorAssetLibrary.save_loaded_asset(asset)
        _log("Created " + BEHAVIOR_ASSET_FULL)
    return asset


def _assign_behavior_to_so(so_asset, behavior_asset):
    """Add behavior to SO_WallBuilder default_behavior_definitions if not already present."""
    if not so_asset or not behavior_asset:
        return
    try:
        arr = so_asset.get_editor_property("default_behavior_definitions")
        if arr is None:
            arr = []
        if behavior_asset not in arr:
            arr.append(behavior_asset)
            so_asset.set_editor_property("default_behavior_definitions", arr)
            unreal.EditorAssetLibrary.save_loaded_asset(so_asset)
            _log("Assigned " + BEHAVIOR_ASSET_NAME + " to SO_WallBuilder Default Behavior Definitions.")
    except Exception as e:
        _log("Could not set default_behavior_definitions: " + str(e))


def main():
    _log("Start.")
    try:
        import ensure_week2_folders
        ensure_week2_folders.main()
    except Exception as e:
        _log("ensure_week2_folders: " + str(e))

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    # Create or reuse SO_WallBuilder
    if unreal.EditorAssetLibrary.does_asset_exist(ASSET_FULL):
        _log("Reusing existing asset: " + ASSET_FULL)
        so_asset = unreal.EditorAssetLibrary.load_asset(ASSET_FULL)
    else:
        factory_class = getattr(unreal, "DataAssetFactory", None)
        if not factory_class:
            _log("DataAssetFactory not found. Create SO_WallBuilder manually.")
            return
        so_class = None
        try:
            so_class = unreal.load_class(None, "/Script/SmartObjectsModule.SmartObjectDefinition")
        except Exception:
            pass
        if not so_class:
            so_class = getattr(unreal, "SmartObjectDefinition", None)
        if not so_class:
            _log("SmartObjectDefinition class not found. Enable SmartObjects plugin.")
            return
        factory = factory_class()
        try:
            factory.set_editor_property("data_asset_class", so_class)
        except Exception as e:
            _log("Could not set data_asset_class: " + str(e))
            return
        so_asset = asset_tools.create_asset(ASSET_NAME, ASSET_PATH, so_class, factory)
        if not so_asset:
            _log("create_asset returned None.")
            return
        _log("Created " + ASSET_FULL)
        try:
            slots = so_asset.get_editor_property("slots")
            if slots is not None and len(slots) < 2:
                for _ in range(2 - len(slots)):
                    slots.append(unreal.SmartObjectSlotDefinition())
                so_asset.set_editor_property("slots", slots)
                _log("Set slots count to 2.")
        except Exception:
            pass
        unreal.EditorAssetLibrary.save_loaded_asset(so_asset)

    # Create behavior definition asset (not in Data Asset menu: base is UObject) and assign to SO
    behavior_asset = _ensure_behavior_asset(asset_tools)
    _assign_behavior_to_so(so_asset, behavior_asset)
    _log("Done.")


if __name__ == "__main__":
    main()

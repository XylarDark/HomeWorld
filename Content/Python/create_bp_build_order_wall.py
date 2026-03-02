# create_bp_build_order_wall.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Creates BP_BuildOrder_Wall (Blueprint child of AHomeWorldBuildOrder) in /Game/HomeWorld/Building/.
# Sets BuildDefinitionID to "Wall" on the CDO. Idempotent: reuses existing Blueprint if found.
# After running: in Editor add Static Mesh component, hologram material, and tag BuildOrder if not set by C++.

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

BP_NAME = "BP_BuildOrder_Wall"
BP_PATH = "/Game/HomeWorld/Building"
BP_FULL = BP_PATH + "/" + BP_NAME

def _log(msg):
    unreal.log("BuildOrder Wall: " + str(msg))
    print("BuildOrder Wall: " + str(msg))


def main():
    _log("Start.")
    # Ensure folders exist
    try:
        import ensure_week2_folders
        ensure_week2_folders.main()
    except Exception as e:
        _log("ensure_week2_folders: " + str(e))

    if unreal.EditorAssetLibrary.does_asset_exist(BP_FULL):
        bp = unreal.load_asset(BP_FULL)
        if bp:
            _log("Reusing existing Blueprint: " + BP_FULL)
            _set_build_definition_id(bp)
            _assign_place_actor_class_on_character(bp)
            _log("Done.")
            return

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = getattr(unreal, "BlueprintFactory", None)
    if not factory:
        _log("BlueprintFactory not found. Create " + BP_NAME + " manually in Editor.")
        return
    factory = factory()

    parent_class = None
    try:
        parent_class = unreal.load_class(None, "/Script/HomeWorld.HomeWorldBuildOrder")
    except Exception:
        pass
    if not parent_class:
        try:
            mod = getattr(unreal, "HomeWorld", None)
            if mod:
                cls = getattr(mod, "HomeWorldBuildOrder", None)
                if cls and hasattr(cls, "static_class"):
                    parent_class = cls.static_class()
        except Exception:
            pass
    if not parent_class:
        _log("Could not find AHomeWorldBuildOrder. Ensure C++ is compiled.")
        return

    factory.set_editor_property("parent_class", parent_class)
    bp = asset_tools.create_asset(BP_NAME, BP_PATH, None, factory)
    if not bp:
        _log("Failed to create " + BP_NAME)
        return

    _log("Created Blueprint: " + BP_FULL)
    _set_build_definition_id(bp)
    unreal.EditorAssetLibrary.save_loaded_asset(bp)
    _assign_place_actor_class_on_character(bp)
    _log("Done.")


def _set_build_definition_id(bp):
    """Set BuildDefinitionID to 'Wall' on the Blueprint's CDO."""
    gen_class = None
    try:
        gen_class = bp.generated_class()
    except Exception:
        try:
            gen_class = bp.get_editor_property("generated_class")
        except Exception:
            pass
    if not gen_class:
        _log("Could not get generated class; set Build Definition ID in Editor.")
        return
    try:
        cdo = unreal.get_default_object(gen_class)
        if cdo:
            cdo.set_editor_property("build_definition_id", unreal.Name("Wall"))
            _log("Set BuildDefinitionID = Wall.")
    except Exception as e:
        _log("Could not set BuildDefinitionID on CDO: " + str(e) + ". Set in Editor.")


def _assign_place_actor_class_on_character(build_order_bp):
    """Set PlaceActorClass on BP_HomeWorldCharacter to the build order Blueprint's generated class."""
    char_bp_path = "/Game/HomeWorld/Characters/BP_HomeWorldCharacter"
    if not build_order_bp or not unreal.EditorAssetLibrary.does_asset_exist(char_bp_path):
        _log("BP_HomeWorldCharacter not found; set Place Actor Class manually in Editor.")
        return
    char_bp = unreal.load_asset(char_bp_path)
    if not char_bp:
        return
    gen_class = None
    try:
        gen_class = build_order_bp.generated_class()
    except Exception:
        try:
            gen_class = build_order_bp.get_editor_property("generated_class")
        except Exception:
            pass
    if not gen_class:
        _log("Could not get build order generated class; set Place Actor Class in Editor.")
        return
    try:
        char_gen = char_bp.generated_class() if hasattr(char_bp, "generated_class") else None
        if not char_gen:
            char_gen = char_bp.get_editor_property("generated_class")
        cdo = unreal.get_default_object(char_gen) if char_gen else None
        if cdo:
            cdo.set_editor_property("place_actor_class", gen_class)
            unreal.EditorAssetLibrary.save_loaded_asset(char_bp)
            _log("Set PlaceActorClass on BP_HomeWorldCharacter to " + BP_NAME + ".")
    except Exception as e:
        _log("Could not set PlaceActorClass on character: " + str(e) + ". Set in Editor.")


if __name__ == "__main__":
    main()

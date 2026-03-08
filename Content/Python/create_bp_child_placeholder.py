# create_bp_child_placeholder.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Creates BP_Child_Placeholder (Blueprint child of StaticMeshActor) in /Game/HomeWorld/Building/.
# Sets default mesh to Cube and tags "Child" and "Family" so in-world interact (E) triggers CompleteOneGameWithChild (List 59 T2/T3).
# Idempotent: reuses existing Blueprint if found.
# MVP full scope List 59 (child in DemoMap). See CONSOLE_COMMANDS.md § Tutorial (List 5); place_child.py for placement.

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

BP_NAME = "BP_Child_Placeholder"
BP_PATH = "/Game/HomeWorld/Building"
BP_FULL = BP_PATH + "/" + BP_NAME
CUBE_MESH_PATH = "/Engine/BasicShapes/Cube"
CHILD_TAG = "Child"
FAMILY_TAG = "Family"


def _log(msg):
    unreal.log("Child placeholder: " + str(msg))
    print("Child placeholder: " + str(msg))


def main():
    _log("Start.")
    try:
        import ensure_week2_folders
        ensure_week2_folders.main()
    except Exception as e:
        _log("ensure_week2_folders: " + str(e))

    if unreal.EditorAssetLibrary.does_asset_exist(BP_FULL):
        bp = unreal.load_asset(BP_FULL)
        if bp:
            _log("Reusing existing Blueprint: " + BP_FULL)
            _set_child_defaults(bp)
            unreal.EditorAssetLibrary.save_loaded_asset(bp)
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
        parent_class = unreal.load_class(None, "/Script/Engine.StaticMeshActor")
    except Exception:
        pass
    if not parent_class:
        _log("Could not find StaticMeshActor. Ensure Engine module loaded.")
        return

    factory.set_editor_property("parent_class", parent_class)
    bp = asset_tools.create_asset(BP_NAME, BP_PATH, None, factory)
    if not bp:
        _log("Failed to create " + BP_NAME)
        return

    _log("Created Blueprint: " + BP_FULL)
    _set_child_defaults(bp)
    unreal.EditorAssetLibrary.save_loaded_asset(bp)
    _log("Done. Run place_child.py with DemoMap open to place one instance.")


def _set_child_defaults(bp):
    """Set default static mesh to Cube and tags Child + Family on the Blueprint CDO."""
    gen_class = None
    try:
        gen_class = bp.generated_class()
    except Exception:
        try:
            gen_class = bp.get_editor_property("generated_class")
        except Exception:
            pass
    if not gen_class:
        _log("Could not get generated class; set mesh and tags in Editor.")
        return
    try:
        cdo = unreal.get_default_object(gen_class)
        if not cdo:
            return
        # Set default static mesh to Cube so child is visible when placed
        mesh = unreal.load_asset(CUBE_MESH_PATH)
        if mesh:
            smc = cdo.get_component_by_class(unreal.StaticMeshComponent)
            if smc and hasattr(smc, "set_editor_property"):
                smc.set_editor_property("static_mesh", mesh)
                _log("Set default mesh to Cube.")
            elif smc and hasattr(smc, "set_static_mesh"):
                smc.set_static_mesh(mesh)
                _log("Set default mesh to Cube.")
        else:
            _log("Cube mesh not found at " + CUBE_MESH_PATH + "; set in Editor.")
        # Tags for List 59: Child = interact target for game-with-child; Family = meals-with-family
        tags = cdo.get_editor_property("tags") if hasattr(cdo, "get_editor_property") else getattr(cdo, "tags", None)
        if tags is None:
            tags = []
        tag_strs = [str(t) for t in tags]
        for tag_name in (CHILD_TAG, FAMILY_TAG):
            if tag_name not in tag_strs:
                tags.append(unreal.Name(tag_name))
                tag_strs.append(tag_name)
        if hasattr(cdo, "set_editor_property"):
            cdo.set_editor_property("tags", tags)
        _log("Set default tags '" + CHILD_TAG + "', '" + FAMILY_TAG + "'.")
    except Exception as e:
        _log("Set defaults: " + str(e) + ". Set mesh/tags in Editor if needed.")


if __name__ == "__main__":
    main()

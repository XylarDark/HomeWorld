# create_bp_harvestable_tree.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Creates BP_HarvestableTree (Blueprint child of AHomeWorldResourcePile) in /Game/HomeWorld/Building/.
# Sets ResourceType=Wood and AmountPerHarvest=10 on the CDO. Idempotent: reuses existing Blueprint if found.
# Add a Static Mesh component with a tree mesh in Editor if desired; see docs/tasks/DAY7_RESOURCE_NODES.md.

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

BP_NAME = "BP_HarvestableTree"
BP_PATH = "/Game/HomeWorld/Building"
BP_FULL = BP_PATH + "/" + BP_NAME

def _log(msg):
    unreal.log("HarvestableTree: " + str(msg))
    print("HarvestableTree: " + str(msg))


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
            _set_resource_defaults(bp)
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
        parent_class = unreal.load_class(None, "/Script/HomeWorld.HomeWorldResourcePile")
    except Exception:
        pass
    if not parent_class:
        try:
            mod = getattr(unreal, "HomeWorld", None)
            if mod:
                cls = getattr(mod, "HomeWorldResourcePile", None)
                if cls and hasattr(cls, "static_class"):
                    parent_class = cls.static_class()
        except Exception:
            pass
    if not parent_class:
        _log("Could not find AHomeWorldResourcePile. Ensure C++ is compiled.")
        return

    factory.set_editor_property("parent_class", parent_class)
    bp = asset_tools.create_asset(BP_NAME, BP_PATH, None, factory)
    if not bp:
        _log("Failed to create " + BP_NAME)
        return

    _log("Created Blueprint: " + BP_FULL)
    _set_resource_defaults(bp)
    unreal.EditorAssetLibrary.save_loaded_asset(bp)
    _log("Done. Add Static Mesh component with tree mesh in Editor if desired (see DAY7_RESOURCE_NODES.md).")


def _set_resource_defaults(bp):
    """Set ResourceType=Wood and AmountPerHarvest=10 on the Blueprint's CDO."""
    gen_class = None
    try:
        gen_class = bp.generated_class()
    except Exception:
        try:
            gen_class = bp.get_editor_property("generated_class")
        except Exception:
            pass
    if not gen_class:
        _log("Could not get generated class; set Resource Type and Amount Per Harvest in Editor.")
        return
    try:
        cdo = unreal.get_default_object(gen_class)
        if cdo:
            cdo.set_editor_property("resource_type", unreal.Name("Wood"))
            cdo.set_editor_property("amount_per_harvest", 10)
            _log("Set ResourceType=Wood, AmountPerHarvest=10.")
    except Exception as e:
        _log("Could not set resource defaults on CDO: " + str(e) + ". Set in Editor.")


if __name__ == "__main__":
    main()

# create_bp_harvestable_flower.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Creates BP_HarvestableFlower (Blueprint child of AHomeWorldResourcePile) in /Game/HomeWorld/Building/.
# Sets ResourceType=Flowers and AmountPerHarvest=5 on the CDO. Idempotent: reuses existing Blueprint if found.
# Use place_resource_nodes.py (resource_node_flower_positions in demo_map_config.json) to place in level.
# MVP tutorial List 6 step 5: "pick some flowers".

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

BP_NAME = "BP_HarvestableFlower"
BP_PATH = "/Game/HomeWorld/Building"
BP_FULL = BP_PATH + "/" + BP_NAME


def _log(msg):
    unreal.log("HarvestableFlower: " + str(msg))
    print("HarvestableFlower: " + str(msg))


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
    _log("Done. Run place_resource_nodes.py with resource_node_flower_positions in demo_map_config.json to place in level.")


def _set_resource_defaults(bp):
    """Set ResourceType=Flowers and AmountPerHarvest=5 on the Blueprint's CDO."""
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
            cdo.set_editor_property("resource_type", unreal.Name("Flowers"))
            cdo.set_editor_property("amount_per_harvest", 5)
            _log("Set ResourceType=Flowers, AmountPerHarvest=5.")
    except Exception as e:
        _log("Could not set resource defaults on CDO: " + str(e) + ". Set in Editor.")


if __name__ == "__main__":
    main()

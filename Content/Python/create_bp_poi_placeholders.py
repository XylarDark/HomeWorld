# create_bp_poi_placeholders.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Creates BP_Shrine_POI and BP_Treasure_POI (Blueprint child of Actor) in /Game/HomeWorld/
# for Day 17 PCG POI placement. Idempotent: reuses existing Blueprints.
# Add Static Mesh (e.g. cube) and interaction in Editor; Day 18 adds Shrine/Treasure behavior.
# See docs/tasks/DAYS_16_TO_30.md (Day 17, Day 18).

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

POI_BLUEPRINTS = [
    ("BP_Shrine_POI", "Shrine placeholder for PCG POI (Day 17); add interaction in Day 18.", "Shrine_POI"),
    ("BP_Treasure_POI", "Treasure placeholder for PCG POI (Day 17); add loot on interact in Day 18.", "Treasure_POI"),
]
BP_PATH = "/Game/HomeWorld"
PCG_LANDSCAPE_TAG = "PCG_Landscape"


def _log(msg):
    unreal.log("POI placeholders: " + str(msg))
    print("POI placeholders: " + str(msg))


def _ensure_folder():
    try:
        if not unreal.EditorAssetLibrary.does_directory_exist(BP_PATH):
            unreal.EditorAssetLibrary.make_directory(BP_PATH)
    except Exception as e:
        _log("Folder check: " + str(e))


def _set_poi_tag(bp, tag_name):
    """Set default actor tag on Blueprint CDO so Interact (TryHarvestInFront) recognizes this POI."""
    try:
        gen_class = bp.generated_class() if hasattr(bp, "generated_class") else bp.get_editor_property("generated_class")
        if not gen_class:
            return
        cdo = gen_class.get_default_object() if hasattr(gen_class, "get_default_object") else None
        if not cdo:
            return
        tags = cdo.get_editor_property("tags") if hasattr(cdo, "get_editor_property") else getattr(cdo, "tags", None)
        if tags is None:
            return
        tag_strs = [str(t) for t in tags]
        if tag_name in tag_strs:
            return
        tags.append(unreal.Name(tag_name))
        if hasattr(cdo, "set_editor_property"):
            cdo.set_editor_property("tags", tags)
        _log("Set default tag '%s' on %s." % (tag_name, bp.get_name()))
    except Exception as e:
        _log("Tag %s: %s. Add tag manually in Editor." % (tag_name, e))


def _create_or_reuse_poi_bp(bp_name, comment, tag_name):
    full_path = BP_PATH + "/" + bp_name
    if unreal.EditorAssetLibrary.does_asset_exist(full_path):
        _log("Reusing existing: " + full_path)
        bp = unreal.load_asset(full_path)
        if bp:
            _set_poi_tag(bp, tag_name)
        return True
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = getattr(unreal, "BlueprintFactory", None)
    if not factory:
        _log("BlueprintFactory not found. Create " + bp_name + " manually.")
        return False
    factory = factory()
    parent_class = None
    try:
        parent_class = unreal.load_class(None, "/Script/Engine.Actor")
    except Exception:
        pass
    if not parent_class:
        _log("Could not load Actor class for " + bp_name)
        return False
    factory.set_editor_property("parent_class", parent_class)
    bp = asset_tools.create_asset(bp_name, BP_PATH, None, factory)
    if not bp:
        _log("Failed to create " + bp_name)
        return False
    _log("Created " + full_path + " (" + comment + ")")
    _set_poi_tag(bp, tag_name)
    try:
        unreal.EditorAssetLibrary.save_loaded_asset(bp)
    except Exception:
        pass
    return True


def main():
    _log("Start.")
    _ensure_folder()
    for bp_name, comment, tag_name in POI_BLUEPRINTS:
        _create_or_reuse_poi_bp(bp_name, comment, tag_name)
    _log("Done. Use BP_Shrine_POI and BP_Treasure_POI as Actor Spawner templates in Planetoid_POI_PCG (Day 17).")


if __name__ == "__main__":
    main()

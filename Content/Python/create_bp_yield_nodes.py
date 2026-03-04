# create_bp_yield_nodes.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Creates BP_Cultivation_POI and BP_Mining_POI (Blueprint child of AHomeWorldYieldNode) in /Game/HomeWorld/
# for Day 19 Cultivation/Mining nodes. Sets tags CultivationNode/MiningNode and yield defaults. Idempotent.
# See docs/tasks/DAYS_16_TO_30.md (Day 19).

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

BP_PATH = "/Game/HomeWorld"
YIELD_NODE_CLASS = "/Script/HomeWorld.HomeWorldYieldNode"

# (bp_name, tag, resource_type, yield_rate, yield_interval_seconds)
NODES = [
    ("BP_Cultivation_POI", "CultivationNode", "Wood", 5, 10.0),
    ("BP_Mining_POI", "MiningNode", "Ore", 5, 10.0),
]


def _log(msg):
    unreal.log("Yield nodes: " + str(msg))
    print("Yield nodes: " + str(msg))


def _ensure_folder():
    try:
        if not unreal.EditorAssetLibrary.does_directory_exist(BP_PATH):
            unreal.EditorAssetLibrary.make_directory(BP_PATH)
    except Exception as e:
        _log("Folder: " + str(e))


def _set_cdo_tag(cdo, tag_name):
    try:
        tags = cdo.get_editor_property("tags") if hasattr(cdo, "get_editor_property") else getattr(cdo, "tags", None)
        if tags is None:
            return False
        tag_strs = [str(t) for t in tags]
        if tag_name in tag_strs:
            return True
        tags.append(unreal.Name(tag_name))
        if hasattr(cdo, "set_editor_property"):
            cdo.set_editor_property("tags", tags)
        return True
    except Exception as e:
        _log("Tag %s: %s" % (tag_name, e))
        return False


def _set_yield_defaults(cdo, resource_type, yield_rate, yield_interval_seconds):
    try:
        cdo.set_editor_property("resource_type", unreal.Name(resource_type))
        cdo.set_editor_property("yield_rate", yield_rate)
        cdo.set_editor_property("yield_interval_seconds", yield_interval_seconds)
        cdo.set_editor_property("b_is_producing", True)
        return True
    except Exception as e:
        _log("Yield defaults: %s" % e)
        return False


def _get_cdo(bp):
    try:
        gen_class = bp.generated_class() if hasattr(bp, "generated_class") else bp.get_editor_property("generated_class")
        if not gen_class:
            return None
        return unreal.get_default_object(gen_class)
    except Exception:
        return None


def _create_or_reuse_bp(bp_name, tag_name, resource_type, yield_rate, yield_interval_seconds):
    full_path = BP_PATH + "/" + bp_name
    if unreal.EditorAssetLibrary.does_asset_exist(full_path):
        _log("Reusing existing: " + full_path)
        bp = unreal.load_asset(full_path)
        if bp:
            cdo = _get_cdo(bp)
            if cdo:
                _set_cdo_tag(cdo, tag_name)
                _set_yield_defaults(cdo, resource_type, yield_rate, yield_interval_seconds)
        return True

    parent_class = None
    try:
        parent_class = unreal.load_class(None, YIELD_NODE_CLASS)
    except Exception:
        pass
    if not parent_class:
        _log("Could not load AHomeWorldYieldNode. Build C++ with Editor closed.")
        return False

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = getattr(unreal, "BlueprintFactory", None)
    if not factory:
        _log("BlueprintFactory not found. Create " + bp_name + " manually.")
        return False
    factory = factory()
    factory.set_editor_property("parent_class", parent_class)
    bp = asset_tools.create_asset(bp_name, BP_PATH, None, factory)
    if not bp:
        _log("Failed to create " + bp_name)
        return False

    _log("Created " + full_path)
    cdo = _get_cdo(bp)
    if cdo:
        _set_cdo_tag(cdo, tag_name)
        _set_yield_defaults(cdo, resource_type, yield_rate, yield_interval_seconds)
    try:
        unreal.EditorAssetLibrary.save_loaded_asset(bp)
    except Exception as e:
        _log("Save: " + str(e))
    return True


def main():
    _log("Start.")
    _ensure_folder()
    for bp_name, tag_name, resource_type, yield_rate, interval in NODES:
        _create_or_reuse_bp(bp_name, tag_name, resource_type, yield_rate, interval)
    _log("Done. Add Static Mesh in Editor if desired; spirit assignment in Day 22.")


if __name__ == "__main__":
    main()

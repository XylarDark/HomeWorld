# create_state_tree_family_gatherer.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Creates an empty State Tree asset ST_FamilyGatherer in /Game/HomeWorld/AI/ if missing.
# Idempotent. After creation: open in Editor and add Selector, states, tasks, blackboard per docs/tasks/FAMILY_AGENTS_MASS_STATETREE.md.

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

ST_NAME = "ST_FamilyGatherer"
ST_PATH = "/Game/HomeWorld/AI"
ST_FULL = ST_PATH + "/" + ST_NAME


def _log(msg):
    unreal.log("StateTree: " + str(msg))
    print("StateTree: " + str(msg))


def main():
    _log("Start.")
    try:
        import ensure_week2_folders
        ensure_week2_folders.main()
    except Exception as e:
        _log("ensure_week2_folders: " + str(e))

    if unreal.EditorAssetLibrary.does_asset_exist(ST_FULL):
        _log("Reusing existing " + ST_FULL)
        _log("Open in Editor and add Selector and states per docs/tasks/FAMILY_AGENTS_MASS_STATETREE.md.")
        return

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    state_tree_class = getattr(unreal, "StateTree", None)
    factory = getattr(unreal, "StateTreeFactory", None)
    if factory:
        factory_instance = factory()
    else:
        factory_instance = None

    if not state_tree_class:
        _log("StateTree class not found. Enable StateTree plugin. Create ST_FamilyGatherer manually: Right-click in AI folder -> AI -> State Tree.")
        return

    if factory_instance:
        st_asset = asset_tools.create_asset(ST_NAME, ST_PATH, state_tree_class, factory_instance)
    else:
        factory_class = getattr(unreal, "DataAssetFactory", None)
        if not factory_class:
            _log("StateTreeFactory and DataAssetFactory not found. Create ST_FamilyGatherer manually: Right-click in AI folder -> AI -> State Tree.")
            return
        factory_instance = factory_class()
        st_asset = asset_tools.create_asset(ST_NAME, ST_PATH, state_tree_class, factory_instance)

    if st_asset:
        unreal.EditorAssetLibrary.save_loaded_asset(st_asset)
        _log("Created " + ST_FULL)
        _log("Open in Editor and add Selector and states per docs/tasks/FAMILY_AGENTS_MASS_STATETREE.md.")
    else:
        _log("create_asset returned None. Create ST_FamilyGatherer manually: Right-click in AI folder -> AI -> State Tree.")


if __name__ == "__main__":
    main()

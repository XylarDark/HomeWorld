# create_mec_family_gatherer.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Creates MEC_FamilyGatherer (Mass Entity Config) in /Game/HomeWorld/Mass/ if missing.
# Idempotent. After creation: add traits (MassAgent, MassMovement, MassRepresentationPoint,
# MassStateTree, etc.) and assign mesh in Editor; run link_state_tree_to_mec.py to link ST_FamilyGatherer.

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

MEC_NAME = "MEC_FamilyGatherer"
MEC_PATH = "/Game/HomeWorld/Mass"
MEC_FULL = MEC_PATH + "/" + MEC_NAME

# Trait class paths (Script/Module.Class). UE 5.7 module names can differ; try alternates.
TRAIT_CLASS_PATHS = [
    "/Script/MassSpawner.MassAgentTrait",
    "/Script/MassGameplay.MassAgentTrait",
    "/Script/MassMovement.MassMovementTrait",
    "/Script/MassRepresentation.MassRepresentationFragmentTrait",
    "/Script/MassGameplay.MassRepresentationFragmentTrait",
    "/Script/MassStateTree.MassStateTreeTrait",
    "/Script/MassAIBehavior.MassStateTreeTrait",
]


def _log(msg):
    unreal.log("MEC_FamilyGatherer: " + str(msg))
    print("MEC_FamilyGatherer: " + str(msg))


def main():
    _log("Start.")
    try:
        import ensure_week2_folders
        ensure_week2_folders.main()
    except Exception as e:
        _log("ensure_week2_folders: " + str(e))

    if unreal.EditorAssetLibrary.does_asset_exist(MEC_FULL):
        _log("Reusing existing " + MEC_FULL)
        _log("Done. Run link_state_tree_to_mec.py to link ST_FamilyGatherer.")
        return

    mec_class = unreal.load_class(None, "/Script/MassSpawner.MassEntityConfigAsset")
    if not mec_class:
        _log("MassEntityConfigAsset not found. Enable MassGameplay/MassSpawner plugins. Create MEC manually: Right-click in Mass folder -> Miscellaneous -> Mass Entity Config.")
        return

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory_class = getattr(unreal, "DataAssetFactory", None)
    if not factory_class:
        _log("DataAssetFactory not found. Create MEC manually.")
        return
    factory = factory_class()
    try:
        factory.set_editor_property("data_asset_class", mec_class)
    except Exception as e:
        _log("Could not set data_asset_class: " + str(e))
        return

    mec = asset_tools.create_asset(MEC_NAME, MEC_PATH, mec_class, factory)
    if not mec:
        _log("create_asset returned None. Create MEC manually: Right-click in Mass -> Mass Entity Config.")
        return

    _log("Created " + MEC_FULL)

    # Try to add traits (AddTrait may be exposed as add_trait in Python). Skip duplicates.
    added = set()
    for path in TRAIT_CLASS_PATHS:
        short_name = path.split(".")[-1]
        if short_name in added:
            continue
        try:
            trait_class = unreal.load_class(None, path)
            if trait_class and hasattr(mec, "add_trait"):
                mec.add_trait(trait_class)
                added.add(short_name)
                _log("Added trait: " + short_name)
        except Exception:
            pass
    if not added:
        _log("No traits added via script (module/class paths may differ in this build). Add them in Editor: Details -> Traits -> Add.")

    unreal.EditorAssetLibrary.save_loaded_asset(mec)
    _log("Done. Open MEC_FamilyGatherer: add traits (StateTree, Movement, ZoneGraph Navigation; optional Avoidance, Agent*Sync). Set State Tree = ST_FamilyGatherer. If a trait has Static Mesh/Scale, set Cube and 1.0. See docs/tasks/DAY11_FAMILY_SPAWN.md.")


if __name__ == "__main__":
    main()

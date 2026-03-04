# set_mec_representation_mesh.py
# Run from Unreal Editor (Tools -> Execute Python Script or via MCP).
# Sets the representation trait's Static Mesh on MEC_FamilyGatherer to Cube so agents are visible in PIE.
# Idempotent. See DAY11_FAMILY_SPAWN.md, KNOWN_ERRORS (MEC mesh).

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

MEC_PATH = "/Game/HomeWorld/Mass/MEC_FamilyGatherer"
CUBE_MESH_PATH = "/Engine/BasicShapes/Cube"


def _log(msg):
    unreal.log("MEC representation: " + str(msg))
    print("MEC representation: " + str(msg))


def main():
    _log("Start.")
    if not unreal.EditorAssetLibrary.does_asset_exist(MEC_PATH):
        _log("MEC_FamilyGatherer not found. Run create_mec_family_gatherer.py first.")
        return
    mec = unreal.EditorAssetLibrary.load_asset(MEC_PATH)
    if not mec:
        _log("Failed to load MEC.")
        return
    mesh_asset = unreal.load_asset(CUBE_MESH_PATH) if hasattr(unreal, "load_asset") else None
    if not mesh_asset:
        mesh_asset = unreal.EditorAssetLibrary.load_asset(CUBE_MESH_PATH)
    if not mesh_asset:
        _log("Cube mesh not found at " + CUBE_MESH_PATH)
        return

    applied = False
    for prop in ["trait_configurations", "TraitConfigurations", "traits", "Traits", "config", "Config"]:
        try:
            arr = mec.get_editor_property(prop)
            if arr is None:
                continue
            if not isinstance(arr, (list, tuple)):
                arr = [arr]
            for i, trait_inst in enumerate(arr):
                if trait_inst is None:
                    continue
                for mesh_prop in ["static_mesh", "StaticMesh", "mesh", "Mesh", "lod_desc", "LODDesc"]:
                    try:
                        if hasattr(trait_inst, "set_editor_property"):
                            trait_inst.set_editor_property(mesh_prop, mesh_asset)
                            _log("Set " + mesh_prop + " on trait " + str(i) + " to Cube.")
                            applied = True
                            break
                        sub = getattr(trait_inst, "get_editor_property", None)
                        if sub:
                            val = sub(mesh_prop)
                            if val is not None and hasattr(val, "set_editor_property"):
                                val.set_editor_property("static_mesh", mesh_asset)
                                applied = True
                                break
                    except Exception:
                        pass
                if applied:
                    break
            if applied:
                break
        except Exception:
            pass
    if applied:
        unreal.EditorAssetLibrary.save_loaded_asset(mec)
        _log("Saved MEC.")
    else:
        _log("Could not set representation mesh via script. Open MEC_FamilyGatherer in Editor -> Details -> find Mass Representation (or representation) -> set Static Mesh to Cube. See KNOWN_ERRORS (MEC mesh).")


if __name__ == "__main__":
    main()

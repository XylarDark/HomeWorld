"""Reimport the size-test meshes from AssetCreation/SizeTest.

Run inside the Unreal Editor. A row is the asset name and fbx or obj.
Skeletal rows use the FBX skeletal options the guard and family scripts used.
Bull and bear call import_names, then replace the actor on L_SizeTest.
"""

import os
import sys

try:
    import unreal
except ImportError:
    print("reimport_size_test: run inside Unreal Editor")
    sys.exit(1)

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEST = "/Game/HomeWorld/Meshes/SizeTest"
SOURCE = os.path.join(ROOT, "AssetCreation", "SizeTest")

# name, extension, skeletal
ROWS = (
    ("SM_Size_Cottage", "fbx", False),
    ("SM_Size_Kettle", "obj", False),
    ("SM_Size_Lupine", "obj", False),
    ("SM_Size_Rock", "obj", False),
    ("SM_Size_Cloud", "obj", False),
    ("SM_Size_Herb", "obj", False),
    ("SM_Size_Wood", "obj", False),
    ("SM_Size_Berry", "obj", False),
    ("SM_Size_BerryBush", "obj", False),
    ("SK_Size_Guard", "fbx", True),
    ("SK_Size_Partner", "fbx", True),
    ("SK_Size_Child", "fbx", True),
    ("SM_Size_Bear", "obj", False),
    ("SM_Size_Bull", "obj", False),
    ("SM_Size_Pine_S", "obj", False),
    ("SM_Size_Pine_M", "obj", False),
    ("SM_Size_Pine_L", "obj", False),
)


def _skeletal_options():
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_as_skeletal", True)
    options.set_editor_property("import_animations", True)
    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
    return options


def _delete_family(name):
    for suffix in ("", "_Skeleton", "_Anim", " _Skeleton"):
        path = "%s/%s%s" % (DEST, name, suffix)
        if unreal.EditorAssetLibrary.does_asset_exist(path):
            unreal.EditorAssetLibrary.delete_asset(path)
            unreal.log("reimport_size_test: deleted " + path)


def import_names(names):
    """Import the named rows. Returns 0, or 1 if any row lands nothing."""
    wanted = set(names) if names else None
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    failed = 0
    seen = set()
    for name, ext, skeletal in ROWS:
        if wanted is not None and name not in wanted:
            continue
        seen.add(name)
        if skeletal and name in ("SK_Size_Partner", "SK_Size_Child"):
            _delete_family(name)
        task = unreal.AssetImportTask()
        task.filename = os.path.join(SOURCE, name + "." + ext)
        task.destination_path = DEST
        task.destination_name = name
        task.automated = True
        task.save = True
        task.replace_existing = True
        if skeletal:
            task.options = _skeletal_options()
        tools.import_asset_tasks([task])
        landed = list(task.imported_object_paths)
        unreal.log("reimport_size_test: %s -> %s" % (name, ", ".join(landed)))
        print(name, landed)
        if not landed:
            failed += 1
    if wanted is not None and not wanted.issubset(seen):
        missing = ", ".join(sorted(wanted - seen))
        unreal.log("reimport_size_test: unknown name " + missing)
        failed += 1
    return 1 if failed else 0


def main():
    return import_names(None)


if __name__ == "__main__":
    sys.exit(main())

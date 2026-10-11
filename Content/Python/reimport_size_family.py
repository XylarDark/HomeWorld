"""Delete the mismatched family assets and import the rigged meshes again."""

import os
import sys

try:
    import unreal
except ImportError:
    print("reimport_size_family: run inside Unreal Editor")
    sys.exit(1)

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEST = "/Game/HomeWorld/Meshes/SizeTest"
NAMES = ("SK_Size_Partner", "SK_Size_Child")


def delete_old(name):
    for suffix in ("", "_Skeleton", "_Anim", " _Skeleton"):
        path = "%s/%s%s" % (DEST, name, suffix)
        if unreal.EditorAssetLibrary.does_asset_exist(path):
            unreal.EditorAssetLibrary.delete_asset(path)
            unreal.log("reimport_size_family: deleted " + path)


def main():
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    failed = 0
    for name in NAMES:
        delete_old(name)
        task = unreal.AssetImportTask()
        task.filename = os.path.join(ROOT, "AssetCreation", "SizeTest", name + ".fbx")
        task.destination_path = DEST
        task.destination_name = name
        task.automated = True
        task.save = True
        task.replace_existing = True
        options = unreal.FbxImportUI()
        options.set_editor_property("import_mesh", True)
        options.set_editor_property("import_as_skeletal", True)
        options.set_editor_property("import_animations", True)
        options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
        task.options = options
        tools.import_asset_tasks([task])
        landed = list(task.imported_object_paths)
        unreal.log("reimport_size_family: %s -> %s" % (name, ", ".join(landed)))
        print(name, landed)
        if not landed:
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

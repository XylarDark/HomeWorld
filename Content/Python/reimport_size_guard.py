"""Import the guard rig into the size-test mesh folder."""

import os
import sys

try:
    import unreal
except ImportError:
    print("reimport_size_guard: run inside Unreal Editor")
    sys.exit(1)

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))


def main():
    task = unreal.AssetImportTask()
    task.filename = os.path.join(ROOT, "AssetCreation", "SizeTest", "SK_Size_Guard.fbx")
    task.destination_path = "/Game/HomeWorld/Meshes/SizeTest"
    task.destination_name = "SK_Size_Guard"
    task.automated = True
    task.save = True
    task.replace_existing = True
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_as_skeletal", True)
    options.set_editor_property("import_animations", True)
    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
    task.options = options
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    landed = list(task.imported_object_paths)
    unreal.log("reimport_size_guard: " + ", ".join(landed))
    if not landed:
        return 1
    asset = unreal.EditorAssetLibrary.load_asset(
        "/Game/HomeWorld/Meshes/SizeTest/SK_Size_Guard"
    )
    if asset is not None:
        size = asset.get_bounds().box_extent * 2.0
        unreal.log("bounds guard extent_cm %.1f %.1f %.1f" % (size.x, size.y, size.z))
    return 0


if __name__ == "__main__":
    sys.exit(main())

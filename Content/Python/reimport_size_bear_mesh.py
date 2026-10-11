"""Reimport the size-test bear mesh."""

import os
import sys

try:
    import unreal
except ImportError:
    print("reimport_size_bear_mesh: run inside Unreal Editor")
    sys.exit(1)

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))


def main():
    task = unreal.AssetImportTask()
    task.filename = os.path.join(ROOT, "AssetCreation", "SizeTest", "SM_Size_Bear.obj")
    task.destination_path = "/Game/HomeWorld/Meshes/SizeTest"
    task.destination_name = "SM_Size_Bear"
    task.automated = True
    task.save = True
    task.replace_existing = True
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    landed = list(task.imported_object_paths)
    unreal.log("reimport_size_bear_mesh: " + ", ".join(landed))
    if not landed:
        return 1
    size = unreal.EditorAssetLibrary.load_asset(landed[0]).get_bounds().box_extent * 2.0
    unreal.log("bounds bear extent_cm %.1f %.1f %.1f" % (size.x, size.y, size.z))
    return 0


if __name__ == "__main__":
    sys.exit(main())

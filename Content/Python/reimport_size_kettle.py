"""Replace the size-test kettle with the TripoSR mesh."""

import os
import sys

try:
    import unreal
except ImportError:
    print("reimport_size_kettle: run inside Unreal Editor")
    sys.exit(1)

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))


def main():
    task = unreal.AssetImportTask()
    task.filename = os.path.join(ROOT, "AssetCreation", "SizeTest", "SM_Size_Kettle.obj")
    task.destination_path = "/Game/HomeWorld/Meshes/SizeTest"
    task.destination_name = "SM_Size_Kettle"
    task.automated = True
    task.save = True
    task.replace_existing = True
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    landed = list(task.imported_object_paths)
    unreal.log("reimport_size_kettle: " + ", ".join(landed))
    print(landed)
    return 0 if landed else 1


if __name__ == "__main__":
    sys.exit(main())

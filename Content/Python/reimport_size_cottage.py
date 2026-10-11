"""Replace the size-test cottage mesh with the measured block."""

import os
import sys

try:
    import unreal
except ImportError:
    print("reimport_size_cottage: run inside Unreal Editor")
    sys.exit(1)

FBX = os.path.join(
    os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..")),
    "AssetCreation",
    "SizeTest",
    "SM_Size_Cottage.fbx",
)


def main():
    task = unreal.AssetImportTask()
    task.filename = FBX
    task.destination_path = "/Game/HomeWorld/Meshes/SizeTest"
    task.destination_name = "SM_Size_Cottage"
    task.automated = True
    task.save = True
    task.replace_existing = True
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    landed = list(task.imported_object_paths)
    unreal.log("reimport_size_cottage: " + ", ".join(landed))
    print(landed)
    return 0 if landed else 1


if __name__ == "__main__":
    sys.exit(main())

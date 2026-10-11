"""Replace the three size-test pines with the TripoSR mesh."""

import os
import sys

try:
    import unreal
except ImportError:
    print("reimport_size_pines: run inside Unreal Editor")
    sys.exit(1)

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
NAMES = ("SM_Size_Pine_S", "SM_Size_Pine_M", "SM_Size_Pine_L")


def main():
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    failed = 0
    for name in NAMES:
        task = unreal.AssetImportTask()
        task.filename = os.path.join(ROOT, "AssetCreation", "SizeTest", name + ".obj")
        task.destination_path = "/Game/HomeWorld/Meshes/SizeTest"
        task.destination_name = name
        task.automated = True
        task.save = True
        task.replace_existing = True
        tools.import_asset_tasks([task])
        landed = list(task.imported_object_paths)
        unreal.log("reimport_size_pines: %s -> %s" % (name, ", ".join(landed)))
        print(name, landed)
        if not landed:
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

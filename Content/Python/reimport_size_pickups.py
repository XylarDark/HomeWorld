"""Import the herb, wood, berry, and berry bush."""

import os
import sys

try:
    import unreal
except ImportError:
    print("reimport_size_pickups: run inside Unreal Editor")
    sys.exit(1)

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
NAMES = ("SM_Size_Herb", "SM_Size_Wood", "SM_Size_Berry", "SM_Size_BerryBush")


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
        unreal.log("reimport_size_pickups: %s -> %s" % (name, ", ".join(landed)))
        if not landed:
            failed += 1
            continue
        size = unreal.EditorAssetLibrary.load_asset(landed[0]).get_bounds().box_extent * 2.0
        unreal.log("bounds %s extent_cm %.1f %.1f %.1f" % (name, size.x, size.y, size.z))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

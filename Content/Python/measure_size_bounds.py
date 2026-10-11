"""Print local bounds of the size-test pine and cottage, in cm."""

import sys

try:
    import unreal
except ImportError:
    print("measure_size_bounds: run inside Unreal Editor")
    sys.exit(1)


def bounds(path):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if asset is None:
        unreal.log("missing " + path)
        return
    box = asset.get_bounds()
    size = box.box_extent * 2.0
    unreal.log(
        "bounds %s extent_cm %.1f %.1f %.1f"
        % (path, size.x, size.y, size.z)
    )


def main():
    bounds("/Game/HomeWorld/Meshes/SizeTest/SM_Size_Pine_S")
    bounds("/Game/HomeWorld/Meshes/SizeTest/SM_Size_Cottage")
    bounds("/Game/HomeWorld/Meshes/SizeTest/SM_Size_Kettle")
    return 0


if __name__ == "__main__":
    sys.exit(main())

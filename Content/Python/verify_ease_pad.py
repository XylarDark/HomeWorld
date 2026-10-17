"""Measure L_EasePad. Do not move actors and do not save.

The pass line is `ease_pad: CHECK PASS` in the open editor.
"""

import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import place_ease_pad

importlib.reload(place_ease_pad)


def main():
    import unreal

    if not unreal.EditorAssetLibrary.does_asset_exist(place_ease_pad.PAD_MAP):
        unreal.log("ease_pad: FAIL map is not saved")
        raise SystemExit(1)
    if not unreal.EditorAssetLibrary.does_asset_exist(place_ease_pad.SIZE_TEST_MAP):
        unreal.log("ease_pad: FAIL L_SizeTest is missing")
        raise SystemExit(1)
    place_ease_pad.load_map(place_ease_pad.PAD_MAP)
    errors = place_ease_pad.measure_current()
    if place_ease_pad.size_test_has_ease_pad():
        errors.append("an ease pad is on L_SizeTest")
    place_ease_pad.load_map(place_ease_pad.PAD_MAP)
    errors.extend(place_ease_pad.measure_current())
    if errors:
        for error in errors:
            unreal.log("ease_pad: FAIL " + error)
        raise SystemExit(1)
    unreal.log("ease_pad: CHECK PASS")


if __name__ == "__main__":
    main()

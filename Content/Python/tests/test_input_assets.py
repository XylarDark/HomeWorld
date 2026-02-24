# test_input_assets.py
# PythonAutomationTest: validates Enhanced Input assets exist.

import unreal

INPUT_PATH = "/Game/HomeWorld/Input"


def test_ia_move_exists():
    """IA_Move Input Action exists."""
    assert unreal.EditorAssetLibrary.does_asset_exist(INPUT_PATH + "/IA_Move"), \
        "IA_Move not found at " + INPUT_PATH + "/IA_Move"


def test_ia_look_exists():
    """IA_Look Input Action exists."""
    assert unreal.EditorAssetLibrary.does_asset_exist(INPUT_PATH + "/IA_Look"), \
        "IA_Look not found at " + INPUT_PATH + "/IA_Look"


def test_imc_default_exists():
    """IMC_Default Input Mapping Context exists."""
    assert unreal.EditorAssetLibrary.does_asset_exist(INPUT_PATH + "/IMC_Default"), \
        "IMC_Default not found at " + INPUT_PATH + "/IMC_Default"

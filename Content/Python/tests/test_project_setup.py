# test_project_setup.py
# PythonAutomationTest: validates project-level configuration.
# Discovered automatically by the PythonAutomationTest plugin.

import unreal


def test_game_mode_exists():
    """GameMode Blueprint exists at expected path."""
    assert unreal.EditorAssetLibrary.does_asset_exist("/Game/HomeWorld/GameMode/BP_GameMode"), \
        "BP_GameMode not found at /Game/HomeWorld/GameMode/BP_GameMode"


def test_default_map_exists():
    """Main map exists at expected path."""
    assert unreal.EditorAssetLibrary.does_asset_exist("/Game/HomeWorld/Maps/Main"), \
        "Main map not found at /Game/HomeWorld/Maps/Main"


def test_character_blueprint_exists():
    """Character Blueprint exists at expected path."""
    assert unreal.EditorAssetLibrary.does_asset_exist("/Game/HomeWorld/Characters/BP_HomeWorldCharacter"), \
        "BP_HomeWorldCharacter not found"


def test_anim_blueprint_exists():
    """Animation Blueprint exists at expected path."""
    assert unreal.EditorAssetLibrary.does_asset_exist("/Game/HomeWorld/Characters/ABP_HomeWorldCharacter"), \
        "ABP_HomeWorldCharacter not found"


def test_no_stale_bp_character():
    """The old stale BP_Character should not exist."""
    assert not unreal.EditorAssetLibrary.does_asset_exist("/Game/HomeWorld/Characters/BP_Character"), \
        "Stale BP_Character still exists — delete it"


def test_pcg_graph_exists():
    """PCG forest graph exists at expected path."""
    assert unreal.EditorAssetLibrary.does_asset_exist("/Game/HomeWorld/PCG/ForestIsland_PCG"), \
        "ForestIsland_PCG not found"


def test_game_mode_default_pawn():
    """GameMode's DefaultPawnClass points to BP_HomeWorldCharacter."""
    gm_bp = unreal.load_asset("/Game/HomeWorld/GameMode/BP_GameMode")
    assert gm_bp, "Could not load BP_GameMode"

    gen_class = None
    try:
        gen_class = gm_bp.generated_class()
    except Exception:
        gen_class = gm_bp.get_editor_property("generated_class")
    assert gen_class, "BP_GameMode has no generated class"

    cdo = unreal.get_default_object(gen_class)
    assert cdo, "Could not get BP_GameMode CDO"

    pawn_class = cdo.get_editor_property("default_pawn_class")
    assert pawn_class, "DefaultPawnClass is None"

    name = pawn_class.get_name()
    assert "HomeWorldCharacter" in name, \
        "DefaultPawnClass is '%s', expected BP_HomeWorldCharacter_C" % name

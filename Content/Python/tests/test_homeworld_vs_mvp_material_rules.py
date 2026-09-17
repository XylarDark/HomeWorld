# test_homeworld_vs_mvp_material_rules.py
# Validates VS_MVP mesh -> master mapping without Unreal Editor.

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from homeworld_master_material_defs import MASTER_NAMES  # noqa: E402
from homeworld_vs_mvp_material_rules import (  # noqa: E402
    material_asset_candidates,
    mesh_basename_from_actor_label,
    resolve_master_for_mesh,
)


def test_mesh_basename_from_dress_label():
    assert mesh_basename_from_actor_label("DRESS_SM_IslandTop") == "SM_IslandTop"
    assert mesh_basename_from_actor_label("VS_MARKER_Foo") is None


def test_island_and_ground_grass():
    assert resolve_master_for_mesh("SM_IslandTop") == "M_StylizedGrass"
    assert resolve_master_for_mesh("SM_Planet_GroundPlate") == "M_StylizedGrass"


def test_cliff_and_islet_rock():
    assert resolve_master_for_mesh("SM_Cliff_LookoutFace") == "M_CliffRock"
    assert resolve_master_for_mesh("SM_Islet_01_Body") == "M_CliffRock"


def test_cabin_and_path():
    assert resolve_master_for_mesh("SM_Cabin_Wall_A") == "M_WoodCabin"
    assert resolve_master_for_mesh("SM_Glider_Perch") == "M_WoodCabin"
    assert resolve_master_for_mesh("SM_PathStone_A") == "M_PathStone"
    assert resolve_master_for_mesh("SM_LandingCircle_StoneRing") == "M_PathStone"


def test_pine_trunk_vs_foliage():
    assert resolve_master_for_mesh("SM_Pine_Homestead_M_Trunk") == "M_WoodWild"
    assert resolve_master_for_mesh("SM_Pine_Homestead_M_Foliage") == "M_FoliageCard"


def test_spirit_and_gather():
    assert resolve_master_for_mesh("SM_Shrine_Homestead_Glow") == "M_SpiritUnlit"
    assert resolve_master_for_mesh("SM_Gather_FirstHarvest_Bush_A") == "M_GatherHerb"
    assert resolve_master_for_mesh("SM_BeastPad_01") == "M_BeastStylized"


def test_res_proxies():
    assert resolve_master_for_mesh("SM_RES_STONE_World") == "M_CliffRock"
    assert resolve_master_for_mesh("SM_RES_WOOD_Stored") == "M_WoodWild"
    assert resolve_master_for_mesh("SM_RES_SEED_World") == "M_Nurtured"
    assert resolve_master_for_mesh("SM_RES_HERB_World") == "M_GatherHerb"


def test_skips_ucx_and_material_names():
    assert resolve_master_for_mesh("UCX_SM_Cabin") is None
    assert resolve_master_for_mesh("M_StylizedGrass") is None


def test_material_candidates_only_ten_masters():
    for master in MASTER_NAMES:
        paths = material_asset_candidates(master)
        assert len(paths) == 3
        assert paths[-1].endswith(master)
        assert paths[0].startswith("/Game/HomeWorld/Materials/Instances/MI_")

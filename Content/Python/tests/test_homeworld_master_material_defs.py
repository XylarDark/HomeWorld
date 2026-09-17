# test_homeworld_master_material_defs.py
# Validates Lib/06_Materials_Master JSON contracts without Unreal Editor.

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from homeworld_master_material_defs import (  # noqa: E402
    MASTER_NAMES,
    load_all_master_defs,
    load_master_json,
    parse_master_def,
)


def test_exactly_ten_masters():
    assert len(MASTER_NAMES) == 10


def test_all_json_load_and_parse():
    defs = load_all_master_defs()
    assert len(defs) == 10
    names = {item.name for item in defs}
    assert names == set(MASTER_NAMES)


def test_night_overlay_fields():
    for item in load_all_master_defs():
        assert 0.0 <= item.night_overlay.desaturate <= 1.0
        assert 0.0 < item.night_overlay.value_mul <= 2.0
        assert len(item.night_overlay.tint) == 4


def test_spirit_unlit_shading():
    spirit = parse_master_def(load_master_json("M_SpiritUnlit"))
    assert spirit.shading_model == "Unlit"
    assert spirit.emissive[0] > 0.0


def test_foliage_card_masked_flag():
    foliage = parse_master_def(load_master_json("M_FoliageCard"))
    assert foliage.opacity_masked is True

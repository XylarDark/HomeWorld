"""The ease-pad check reports the pad, the focus, and their absence from L_SizeTest."""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..")))

import place_ease_pad


def test_check_reports_the_pad_the_focus_and_the_size_test_absence():
    report = place_ease_pad.ease_pad_report(place_ease_pad.INTENDED_PAD, place_ease_pad.SIZE_TEST_STAYS)
    assert report["pad"] is True
    assert report["focus"] is True
    assert report["absent_from_L_SizeTest"] is True
    assert report["map"] == "/Game/HomeWorld/Maps/EasePad/L_EasePad"


def test_a_pad_on_the_size_test_map_is_not_absent():
    report = place_ease_pad.ease_pad_report(
        place_ease_pad.INTENDED_PAD,
        (("EasePad", ("HomeWorldEasePad",)),),
    )
    assert report["absent_from_L_SizeTest"] is False

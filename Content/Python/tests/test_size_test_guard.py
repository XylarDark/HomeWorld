# The size-test placer must refuse a stroke or an ease pad before it saves.

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..")))

import size_test_guard


def test_a_clean_homestead_passes():
    errors = size_test_guard.size_test_stroke_errors(
        [("SM_Size_Cottage", ["StaticMeshActor"]), ("PlayerStart", ["PlayerStart"])]
    )
    assert errors == []


def test_a_stroke_component_is_refused():
    errors = size_test_guard.size_test_stroke_errors(
        [("SK_Size_Player", ["HomeWorldCharacter", "HomeWorldStrokeReportComponent"])]
    )
    assert errors == ["stroke or ease pad on L_SizeTest: SK_Size_Player"]


def test_an_ease_pad_is_refused():
    errors = size_test_guard.size_test_stroke_errors(
        [("EasePad", ["Actor"])]
    )
    assert len(errors) == 1

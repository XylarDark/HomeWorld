"""The NEED_SLATE classifier names only the three panels Python cannot write."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import editor_ui_need


def test_portal_failure_names_the_level_field():
    text = "LevelToOpen could not be set from Python"
    assert editor_ui_need.classify(text) == "portal-level"


def test_state_tree_sentence_names_the_graph():
    text = "No Python API for State Tree graph editing"
    assert editor_ui_need.classify(text) == "state-tree"


def test_by_tag_sentence_names_pcg_details():
    text = "Get Landscape Data By Tag is not settable from Python"
    assert editor_ui_need.classify(text) == "pcg-details"


def test_actor_move_does_not_ask_for_the_inspector():
    assert editor_ui_need.classify("moved the actor to the pad") is None

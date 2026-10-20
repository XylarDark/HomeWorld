# test_quest_test_contract.py
# Host tests for the opening quest sweep contract. No Editor and no PIE.
#
# These tests exist because the sweep was only exercised by a 13-second PIE beat.
# A typo in a manifest path, an unknown check kind, or a missing result was found
# by running the suite and reading the log. The pure contract module lets pytest
# catch the same faults before the Editor is opened.

import os
import sys

_script_dir = os.path.dirname(os.path.abspath(__file__))
_content_python = os.path.normpath(os.path.join(_script_dir, ".."))
if _content_python not in sys.path:
    sys.path.insert(0, _content_python)

import quest_test_contract as contract
import quest_test_manifest as manifest


def _beat(checks, quest_id="x"):
    return {
        "id": quest_id,
        "stop": "",
        "section": "Test",
        "note": "test beat",
        "checks": checks,
    }


def _error_text(errors):
    return "\n".join(errors)


def test_real_manifest_satisfies_the_contract():
    """The checked-in manifest is the first thing the contract must accept."""
    errors = contract.validate_manifest(manifest.QUESTS)
    assert errors == [], _error_text(errors)


def test_manifest_ids_are_unique_and_the_night_trio_stays_in_chain_order():
    ids = [quest["id"] for quest in manifest.QUESTS]
    assert len(ids) == len(set(ids)), "duplicate beat ids make by_id ambiguous"
    assert ids.index("night") < ids.index("collect") < ids.index("heal")


def test_unknown_check_kind_is_rejected_before_pie():
    errors = contract.validate_manifest([
        _beat([{"kind": "gt", "path": "quest.wisps_carried", "value": 1}]),
    ])
    assert any("unknown check kind" in error for error in errors), _error_text(errors)


def test_value_check_without_a_path_is_rejected():
    errors = contract.validate_manifest([
        _beat([{"kind": "eq", "value": True}]),
    ])
    assert any("path" in error for error in errors), _error_text(errors)


def test_path_must_have_a_snapshot_root_and_no_empty_segments():
    errors = contract.validate_manifest([
        _beat([
            {"kind": "eq", "path": "quests.spirit_claimed", "value": False},
            {"kind": "eq", "path": "quest..spirit_claimed", "value": False},
        ]),
    ])
    assert len(errors) >= 2, _error_text(errors)


def test_duplicate_beat_ids_are_rejected():
    errors = contract.validate_manifest([
        _beat([{"kind": "present", "path": "quest.spirit_claimed"}], "night"),
        _beat([{"kind": "present", "path": "quest.spirit_claimed"}], "night"),
    ])
    assert any("duplicates" in error for error in errors), _error_text(errors)


def test_beat_needs_checks_and_human_labels():
    errors = contract.validate_manifest([{
        "id": "x",
        "stop": "",
        "section": "",
        "note": "",
        "checks": [],
    }])
    text = _error_text(errors)
    assert "section" in text
    assert "note" in text
    assert "checks" in text


def test_between_bounds_must_be_numbers_and_ordered():
    errors = contract.validate_manifest([
        _beat([
            {"kind": "between", "path": "actors.counter.east_face", "low": "980", "high": 990},
            {"kind": "between", "path": "actors.counter.east_face", "low": 990, "high": 980},
        ]),
    ])
    text = _error_text(errors)
    assert "low and high" in text
    assert "low must be <= high" in text


def test_near_needs_two_paths_and_a_positive_distance():
    errors = contract.validate_manifest([
        _beat([
            {"kind": "near", "a": "actors.partner.location", "b": "actors.reveal.partner_stand", "cm": 0},
            {"kind": "near", "a": "actors.partner.location", "cm": 80},
        ]),
    ])
    text = _error_text(errors)
    assert "positive number" in text
    assert "b" in text


def test_count_tag_needs_a_tag_and_a_non_negative_count():
    errors = contract.validate_manifest([
        _beat([
            {"kind": "count_tag", "tag": "", "value": -1},
            {"kind": "count_tag", "tag": "NODE_OPENING_WISP", "value": True},
        ]),
    ])
    text = _error_text(errors)
    assert "non-empty tag" in text
    assert "non-negative integer" in text


def test_eq_check_returns_pass_and_fail_with_the_measured_value():
    snapshot = {"quest": {"spirit_claimed": False}}
    passed = contract.run_check(
        {"kind": "eq", "path": "quest.spirit_claimed", "value": False}, snapshot)
    failed = contract.run_check(
        {"kind": "eq", "path": "quest.spirit_claimed", "value": True}, snapshot)

    assert passed["status"] == "passed"
    assert passed["expected"] is False
    assert passed["actual"] is False
    assert failed["status"] == "failed"
    assert failed["actual"] is False


def test_missing_path_is_inconclusive_not_a_failed_measurement():
    result = contract.run_check(
        {"kind": "eq", "path": "quest.not_there", "value": 1},
        {"quest": {}},
    )
    assert result["status"] == "inconclusive"
    assert "path missing" in result["detail"]


def test_type_mismatch_is_inconclusive_not_a_failure():
    result = contract.run_check(
        {"kind": "le", "path": "quest.wisps_carried", "value": 3},
        {"quest": {"wisps_carried": "three"}},
    )
    assert result["status"] == "inconclusive"
    assert "cannot compare" in result["detail"]


def test_between_is_inclusive():
    snapshot = {"actors": {"counter": {"east_face": 985.0}}}
    check = {"kind": "between", "path": "actors.counter.east_face", "low": 985, "high": 990}
    assert contract.run_check(check, snapshot)["status"] == "passed"

    check["low"] = 986
    assert contract.run_check(check, snapshot)["status"] == "failed"


def test_near_uses_2d_distance_and_ignores_z():
    snapshot = {
        "actors": {
            "partner": {"location": [0, 0, 100]},
            "reveal": {"partner_stand": [30, 40, -500]},
        },
    }
    check = {
        "kind": "near",
        "a": "actors.partner.location",
        "b": "actors.reveal.partner_stand",
        "cm": 50,
    }
    passed = contract.run_check(check, snapshot)
    assert passed["status"] == "passed"
    assert passed["actual"] == 50.0

    check["cm"] = 49
    assert contract.run_check(check, snapshot)["status"] == "failed"


def test_near_with_missing_or_bad_points_is_inconclusive():
    check = {
        "kind": "near",
        "a": "actors.partner.location",
        "b": "actors.reveal.partner_stand",
        "cm": 80,
    }
    missing = contract.run_check(check, {"actors": {"partner": {}}})
    bad_shape = contract.run_check(check, {
        "actors": {
            "partner": {"location": "not a point"},
            "reveal": {"partner_stand": [1, 2, 3]},
        },
    })

    assert missing["status"] == "inconclusive"
    assert missing["detail"] == "one or both points missing"
    assert bad_shape["status"] == "inconclusive"
    assert bad_shape["detail"] == "points are not locations"


def test_count_tag_treats_an_absent_tag_as_zero():
    check = {"kind": "count_tag", "tag": "NODE_OPENING_WISP", "value": 0}
    assert contract.run_check(check, {"tag_counts": {}})["status"] == "passed"

    check["value"] = 1
    failed = contract.run_check(check, {"tag_counts": {}})
    assert failed["status"] == "failed"
    assert failed["actual"] == 0


def test_present_fails_when_the_path_is_missing_or_null():
    check = {"kind": "present", "path": "actors.dog"}
    missing = contract.run_check(check, {"actors": {}})
    null = contract.run_check(check, {"actors": {"dog": None}})
    present = contract.run_check(check, {"actors": {"dog": {"tamed": False}}})

    assert missing["status"] == "failed"
    assert null["status"] == "failed"
    assert present["status"] == "passed"


def test_unknown_kind_is_inconclusive_at_runtime_too():
    result = contract.run_check({"kind": "gt"}, {})
    assert result["status"] == "inconclusive"
    assert "unknown check kind" in result["detail"]


def test_bad_runtime_shapes_do_not_raise():
    assert contract.run_check("not a check", {})["status"] == "inconclusive"
    assertions, status = contract.evaluate_checks({"kind": "eq"}, {})
    assert status == "inconclusive"
    assert assertions[0]["detail"] == "checks list is empty"


def test_evaluate_checks_failed_wins_over_inconclusive():
    snapshot = {"quest": {"spirit_claimed": True}}
    assertions, status = contract.evaluate_checks([
        {"kind": "eq", "path": "quest.spirit_claimed", "value": False},
        {"kind": "eq", "path": "quest.missing", "value": 1},
    ], snapshot)

    assert [item["status"] for item in assertions] == ["failed", "inconclusive"]
    assert status == "failed"


def test_evaluate_checks_is_inconclusive_when_any_check_cannot_measure():
    assertions, status = contract.evaluate_checks([
        {"kind": "eq", "path": "quest.spirit_claimed", "value": True},
        {"kind": "eq", "path": "quest.missing", "value": 1},
    ], {"quest": {"spirit_claimed": True}})

    assert [item["status"] for item in assertions] == ["passed", "inconclusive"]
    assert status == "inconclusive"


def test_evaluate_checks_with_no_checks_is_not_a_pass():
    assertions, status = contract.evaluate_checks([], {})
    assert status == "inconclusive"
    assert assertions[0]["status"] == "inconclusive"
    assert assertions[0]["detail"] == "checks list is empty"


def test_describe_labels_are_stable_for_the_host_report():
    assert contract.describe(
        {"kind": "eq", "path": "quest.spirit_claimed", "value": False}
    ) == "quest.spirit_claimed == False"
    assert contract.describe(
        {"kind": "between", "path": "actors.counter.east_face", "low": 980, "high": 990}
    ) == "actors.counter.east_face in [980, 990]"
    assert contract.describe(
        {"kind": "near", "a": "actors.partner.location",
         "b": "actors.reveal.partner_stand", "cm": 80}
    ) == "2D(actors.partner.location, actors.reveal.partner_stand) <= 80 cm"
    assert contract.describe(
        {"kind": "present", "path": "actors.dog"}
    ) == "actors.dog present"
    assert contract.describe(
        {"kind": "count_tag", "tag": "NODE_OPENING_WISP", "value": 3}
    ) == "tag NODE_OPENING_WISP count == 3"


def test_all_passed_requires_every_selected_beat_in_order():
    selected = ["night", "collect"]
    results = [
        {"id": "night", "status": "passed"},
        {"id": "collect", "status": "passed"},
    ]
    assert contract.all_passed(selected, results) is True

    assert contract.all_passed([], []) is False
    assert contract.all_passed(selected, results[:1]) is False
    assert contract.all_passed(selected, [
        {"id": "collect", "status": "passed"},
        {"id": "night", "status": "passed"},
    ]) is False
    assert contract.all_passed(selected, [
        {"id": "night", "status": "passed"},
        {"id": "collect", "status": "inconclusive"},
    ]) is False


def test_counts_keeps_unknown_statuses_out_of_passed():
    counted = contract.counts([
        {"status": "passed"},
        {"status": "failed"},
        {"status": "inconclusive"},
        {"status": "skipped"},
    ])
    assert counted == {
        "passed": 1,
        "failed": 1,
        "inconclusive": 1,
        "other": 1,
    }

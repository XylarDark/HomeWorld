# test_quest_coverage.py
# Host tests for the quest coverage matrix. No Editor and no PIE.
#
# Two behaviours are proven separately, the same way as the preflight suite:
#   1. the real tree builds a complete, honest matrix, and
#   2. the guarantees that make the matrix trustworthy - declared names exist,
#      an absent result is inconclusive and never a pass, the checked-in
#      snapshot is byte-stable - are each broken by a plant into a disposable
#      copy and caught.

import hashlib
import json
import os
import shutil
import subprocess
import sys

import pytest

_script_dir = os.path.dirname(os.path.abspath(__file__))
_content_python = os.path.normpath(os.path.join(_script_dir, ".."))
if _content_python not in sys.path:
    sys.path.insert(0, _content_python)

import quest_coverage as coverage
import quest_test_coverage as sidecar

PROJECT_ROOT = os.path.abspath(os.path.join(_content_python, "..", ".."))

_MANIFEST = os.path.join("Content", "Python", "quest_test_manifest.py")
_SIDECAR = os.path.join("Content", "Python", "quest_test_coverage.py")
_SOURCE = "Source" + os.sep + "HomeWorld"
_RESULTS = os.path.join("Saved", "quest_tests.json")
_JSON_OUT = os.path.join("Saved", "quest_coverage.json")
_DOC_OUT = os.path.join("Docs", "qa", "QUEST_COVERAGE.md")


def _results_doc(run_id="r1", done=True, beats=()):
    return {"run_id": run_id, "done": done, "passed": 0, "failed": 0,
            "inconclusive": 0, "beats_run": len(beats), "beats": list(beats)}


def _manifest_ids():
    """The opening beats. The matrix count is this list, not a frozen number."""
    import quest_test_manifest as manifest
    ids = manifest.ids()
    assert ids, "the manifest has no beats"
    assert len(ids) == len(set(ids)), "the manifest repeats a beat id"
    return ids


@pytest.fixture()
def double_root(tmp_path):
    """A disposable copy of what the coverage matrix reads."""
    project = tmp_path / "proj"
    for rel in (_MANIFEST, _SIDECAR):
        target = project / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(os.path.join(PROJECT_ROOT, rel.replace("/", os.sep)), str(target))
    shutil.copytree(os.path.join(PROJECT_ROOT, _SOURCE.replace("/", os.sep)),
                    str(project / _SOURCE))
    return project


def _plant(project, rel, old, new):
    path = project / rel
    text = path.read_text(encoding="utf-8")
    assert old in text, "planted fixture text missing from the real tree: %r" % old
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def _write_results(project, doc):
    path = project / _RESULTS
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc), encoding="utf-8")


# ---------------------------------------------------------------------------
# The real tree.
# ---------------------------------------------------------------------------


def test_real_matrix_has_all_beats_in_manifest_order():
    evaluation = coverage.evaluate(PROJECT_ROOT)
    assert evaluation["errors"] == [], evaluation["errors"]
    assert evaluation["warnings"] == [], evaluation["warnings"]

    ids = [row["id"] for row in evaluation["beats"]]
    assert ids == _manifest_ids(), ids


def test_real_declared_tests_all_exist():
    import quest_preflight as preflight
    from pathlib import Path
    names, reason = preflight._parse_automation_test_names(
        str(Path(PROJECT_ROOT) / _SOURCE.replace("/", os.sep)))
    assert reason == "", reason
    for rows in sidecar.COVERAGE.values():
        for name in rows["tests"]:
            assert name in names, "declared test does not exist: %s" % name


def test_missing_result_file_leaves_every_row_inconclusive(double_root):
    """The rule the Lead set: absent result is inconclusive, never a pass."""
    evaluation = coverage.evaluate(str(double_root))
    assert all(
        row["latest"]["status"] == "inconclusive" and "detail" in row["latest"]
        for row in evaluation["beats"])
    document = coverage.build(evaluation)
    assert document["summary"]["latest_result_statuses"] == {
        "inconclusive": len(_manifest_ids())}
    assert not any(
        row["latest"].get("status") == "passed" for row in evaluation["beats"])


def test_real_rows_carry_checks_and_human_only():
    evaluation = coverage.evaluate(PROJECT_ROOT)
    for row in evaluation["beats"]:
        assert row["checks"], "beat %s declares no checks" % row["id"]
        assert isinstance(row["human_only"], list)
        for item in row["human_only"]:
            assert isinstance(item, str) and item
    heal = next(row for row in evaluation["beats"] if row["id"] == "heal")
    assert "HomeWorld.Systems.Opening.NightWisp.DepositStartsHeal" in heal["declared_tests"]


# ---------------------------------------------------------------------------
# Result merging on a double.
# ---------------------------------------------------------------------------


def test_finished_run_merges_status_per_beat(double_root):
    _write_results(double_root, _results_doc(beats=[
        {"id": "night", "status": "passed", "duration_s": 12.0},
        {"id": "fish", "status": "failed", "duration_s": 3.0},
        {"id": "spirit", "status": "inconclusive", "duration_s": 1.0},
    ]))
    evaluation = coverage.evaluate(str(double_root))
    by_id = {row["id"]: row for row in evaluation["beats"]}
    assert by_id["night"]["latest"]["status"] == "passed"
    assert by_id["night"]["latest"]["run_id"] == "r1"
    assert by_id["fish"]["latest"]["status"] == "failed"
    assert by_id["spirit"]["latest"]["status"] == "inconclusive"
    assert by_id["herbs"]["latest"]["status"] == "inconclusive"
    assert "not in the latest" in by_id["herbs"]["latest"]["detail"]


def test_unfinished_run_is_inconclusive_for_every_beat(double_root):
    _write_results(double_root, _results_doc(run_id="r9", done=False, beats=[
        {"id": "night", "status": "passed", "duration_s": 1.0},
    ]))
    evaluation = coverage.evaluate(str(double_root))
    assert all(row["latest"]["status"] == "inconclusive" for row in evaluation["beats"])
    assert all("did not finish" in row["latest"]["detail"] for row in evaluation["beats"])


# ---------------------------------------------------------------------------
# Declarations: warn, never fail.
# ---------------------------------------------------------------------------


def test_a_declared_test_name_that_stopped_existing_warns(double_root):
    """The preflight hook on top of the coverage sidecar."""
    # The preflight reads more than the matrix does: give it the file set its
    # own suite uses, so it reaches the coverage block instead of returning on
    # a missing-input problem.
    for rel in ("Source/HomeWorld/HomeWorldCharacter.cpp",
                "Content/Python/quest_test_runner.py"):
        target = double_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(os.path.join(PROJECT_ROOT, rel.replace("/", os.sep)), str(target))
    umap = double_root / "Content" / "HomeWorld" / "Maps" / "SizeTest" / "L_SizeTest.umap"
    umap.parent.mkdir(parents=True, exist_ok=True)
    umap.write_bytes(b"")

    _plant(double_root, _SIDECAR, "GraceMatchesItsShape", "GraceNeverMatched")
    evaluation = coverage.evaluate(str(double_root))
    dog = next(row for row in evaluation["beats"] if row["id"] == "dog")
    assert "HomeWorld.Systems.Stroke.GraceNeverMatched" in dog["missing_tests"]
    assert any("GraceNeverMatched" in warning for warning in evaluation["warnings"])

    assert coverage.main(root=str(double_root)) == 0  # warn, not fail

    import quest_preflight as preflight
    problems, warnings = preflight.run_preflight(str(double_root))
    assert not any("GraceNeverMatched" in problem["detail"] for problem in problems)
    assert any("GraceNeverMatched" in warning for warning in warnings)


def test_a_sidecar_row_for_a_dropped_beat_warns(double_root):
    _plant(double_root, _SIDECAR, '"dog": {', '"doggie": {')
    evaluation = coverage.evaluate(str(double_root))
    text = "\n".join(evaluation["warnings"])
    assert "doggie" in text and "the manifest does not" in text
    assert any("no COVERAGE row for beat 'dog'" in warning
               for warning in evaluation["warnings"])


def test_an_unparsable_source_list_warns_and_does_not_fail(double_root):
    shutil.rmtree(str(double_root / _SOURCE))
    evaluation = coverage.evaluate(str(double_root))
    assert evaluation["errors"] == [], evaluation["errors"]
    assert any("unsure" in warning for warning in evaluation["warnings"])
    assert all(row["missing_tests"] == [] for row in evaluation["beats"])


# ---------------------------------------------------------------------------
# Exit codes and outputs.
# ---------------------------------------------------------------------------


def test_main_exit_two_when_the_manifest_cannot_load(double_root):
    _plant(double_root, _MANIFEST, "QUESTS = [", "QUESTS === = [")
    assert coverage.main(root=str(double_root)) == 2


def test_main_exit_two_when_the_sidecar_cannot_load(double_root):
    os.remove(str(double_root / _SIDECAR))
    assert coverage.main(root=str(double_root)) == 2


def test_main_writes_both_outputs(double_root):
    _write_results(double_root, _results_doc(beats=[
        {"id": "night", "status": "passed", "duration_s": 9.0}]))
    assert coverage.main(root=str(double_root)) == 0

    document = json.loads((double_root / _JSON_OUT).read_text(encoding="utf-8"))
    beat_ids = _manifest_ids()
    assert document["summary"]["beats"] == len(beat_ids)
    assert len(document["beats"]) == len(beat_ids)
    assert [row["id"] for row in document["beats"]] == beat_ids

    markdown = (double_root / _DOC_OUT).read_text(encoding="utf-8")
    for beat_id in beat_ids:
        assert "**%s**" % beat_id in markdown, beat_id


def test_the_checked_in_snapshot_is_byte_stable(double_root):
    """No timestamps, no volatile results: regenerating with different sweep
    results still rewrites the doc byte-for-byte - a run never dirties it."""
    _write_results(double_root, _results_doc(run_id="old", beats=[
        {"id": "night", "status": "passed", "duration_s": 1.0}]))
    assert coverage.main(root=str(double_root)) == 0
    first = hashlib.sha256(
        (double_root / _DOC_OUT).read_bytes()).hexdigest()

    _write_results(double_root, _results_doc(run_id="new-r2", done=True, beats=[
        {"id": "heal", "status": "failed", "duration_s": 30.0},
        {"id": "dog", "status": "failed", "duration_s": 30.0},
    ]))
    assert coverage.main(root=str(double_root)) == 0
    second = hashlib.sha256(
        (double_root / _DOC_OUT).read_bytes()).hexdigest()
    assert first == second

    json_after = json.loads((double_root / _JSON_OUT).read_text(encoding="utf-8"))
    json_by_id = {row["id"]: row for row in json_after["beats"]}
    assert json_by_id["heal"]["latest"]["status"] == "failed"  # but the JSON moved


def test_cli_coverage_exits_zero_on_the_real_tree():
    result = subprocess.run(
        [sys.executable, os.path.join(_content_python, "run_quest_tests_host.py"), "--coverage"],
        capture_output=True, text=True, cwd=PROJECT_ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "quest_coverage: %d beat(s)" % len(_manifest_ids()) in result.stdout
    assert os.path.isfile(os.path.join(PROJECT_ROOT, _JSON_OUT.replace("/", os.sep)))


def test_coverage_and_check_are_listed_in_the_cli_help():
    result = subprocess.run(
        [sys.executable, os.path.join(_content_python, "run_quest_tests_host.py"), "--help"],
        capture_output=True, text=True, cwd=PROJECT_ROOT,
    )
    assert result.returncode == 0
    assert "--coverage" in result.stdout and "--check" in result.stdout


def test_powershell_quest_coverage_exits_zero():
    result = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
         "-File", os.path.join(PROJECT_ROOT, "Tools", "RunTests.ps1"), "-QuestCoverage"],
        capture_output=True, text=True, cwd=PROJECT_ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "quest_coverage: %d beat(s)" % len(_manifest_ids()) in result.stdout


def test_the_preflight_stays_clean_on_the_real_tree_after_the_coverage_hook():
    import quest_preflight as preflight
    problems, _warnings = preflight.run_preflight(PROJECT_ROOT)
    assert problems == []

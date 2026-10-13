"""Contract tests for migrate_30day_to_task_list.py - the 30-day -> 10-task generator.

Written 2026-10-13, immediately after fixing the bug these tests pin.

THE FAILURE THIS PINS

The module built all four of its inputs from one base, DOCS_WORKFLOW. The
task-list family then moved to docs/TaskLists/ and only 30_DAY_SCHEDULE.md
stayed behind, so three of the four paths named files that are not there. What
that cost varied by input:

  * MAPPING_PATH - loud. main() reports "30DAY_TO_10TASK_MAPPING.json missing or
    invalid" and exits 1, so a stale path was handed to a reader as corrupt
    data.
  * STATUS_PATH and TASK_LIST_PATH - quiet. Both go through readers that return
    {} on a missing file, which reads as "nothing to migrate".

The sharper hazard was --write. TASK_LIST_PATH pointed at
docs/workflow/CURRENT_TASK_LIST.md, so the documented procedure in
docs/TaskLists/HOW_TO_GENERATE_TASK_LIST.md would have created a SECOND task
list beside the real one: two files, both authoritative-looking, neither aware
of the other.

Nothing caught it for months, because the loop only ran when the session named
it and nobody ran it in between.

WHY test_writer_and_validator_target_the_same_file MATTERS MOST

It is the guard against that second-list hazard specifically. The generator and
validate_task_list.py are two halves of one workflow - one writes the list, the
other validates it - and they had each independently walked away from the file
the other one uses. Agreement is the property, not any particular path.

Runs without Blender or Unreal: pure-Python file and path checks.
"""

import json
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

import migrate_30day_to_task_list as mig  # noqa: E402
import validate_task_list as val  # noqa: E402

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def _rel(path):
    """Repo-relative, forward-slashed, so a failure names a path you can click."""
    return os.path.relpath(str(path), REPO_ROOT).replace("\\", "/")


def test_every_input_path_resolves_to_a_real_file():
    """The bug itself: three of four inputs pointed at a folder they had left."""
    for name in ("STATUS_PATH", "SCHEDULE_PATH", "MAPPING_PATH"):
        path = getattr(mig, name)
        assert os.path.isfile(path), (
            f"{name} = {_rel(path)} does not exist. The task-list family lives in "
            "docs/TaskLists/; only 30_DAY_SCHEDULE.md is still under docs/workflow/. "
            "Point the constant at the real file, do not add a fallback that returns "
            "{} - that is how this stayed broken."
        )


def test_task_list_paths_are_not_the_stale_workflow_folder():
    """Pin the fix, not just the symptom."""
    stale = os.path.join(REPO_ROOT, "docs", "workflow")
    for name in ("STATUS_PATH", "MAPPING_PATH", "TASK_LIST_PATH"):
        path = getattr(mig, name)
        assert os.path.normpath(os.path.dirname(str(path))) != os.path.normpath(stale), (
            f"{name} is back under docs/workflow/. Those files moved to docs/TaskLists/."
        )


def test_writer_and_validator_target_the_same_file():
    """The two halves of the workflow must agree on which list is the list."""
    assert os.path.normpath(str(mig.TASK_LIST_PATH)) == os.path.normpath(
        str(val.TASK_LIST_PATH)
    ), (
        f"migrate writes {_rel(mig.TASK_LIST_PATH)} but validate_task_list reads "
        f"{_rel(val.TASK_LIST_PATH)}. Running one with --write and then the other "
        "validates a different file from the one that was written."
    )


def test_mapping_loads_and_has_buckets():
    """The only input that fails loudly, so pin that it is genuinely readable."""
    mapping = mig._load_mapping(mig.MAPPING_PATH)
    assert mapping, f"{_rel(mig.MAPPING_PATH)} loaded as empty"
    assert "buckets" in mapping, "mapping has no 'buckets' key; main() would exit 1"
    buckets = mapping["buckets"]
    for tid in mig.TASK_IDS:
        assert tid in buckets, f"mapping is missing bucket {tid}"


def test_status_table_parses_all_thirty_days():
    """A silent {} here is indistinguishable from an empty schedule, so count it."""
    days = mig._parse_status_table(mig.STATUS_PATH)
    assert len(days) == 30, (
        f"parsed {len(days)} of 30 days from {_rel(mig.STATUS_PATH)}. A short or "
        "empty result marks whole buckets pending that are in fact done."
    )


def test_main_emits_a_draft_without_touching_the_real_task_list(tmp_path, monkeypatch):
    """--write is the dangerous arm, so exercise the safe one and prove it is safe."""
    draft = tmp_path / "draft.md"
    before = mig.TASK_LIST_PATH.read_text(encoding="utf-8")

    monkeypatch.setattr(mig, "DRAFT_PATH", draft)
    monkeypatch.setattr(sys, "argv", ["migrate_30day_to_task_list.py"])
    assert mig.main() == 0, "main() failed; the mapping is probably unreadable"

    assert draft.is_file() and draft.stat().st_size > 0, "no draft was written"
    text = draft.read_text(encoding="utf-8")
    for tid in mig.TASK_IDS:
        assert f"## {tid}." in text, f"draft is missing {tid}"
    assert mig.TASK_LIST_PATH.read_text(encoding="utf-8") == before, (
        "the safe arm modified the real task list; --write is not the only way to "
        "reach it"
    )


def test_every_declared_path_in_the_mapping_is_a_string_or_list():
    """Malformed day entries render as a stray 'None' in a document people read."""
    buckets = mig._load_mapping(mig.MAPPING_PATH)["buckets"]
    for tid, info in buckets.items():
        assert isinstance(info, dict), f"bucket {tid} is not an object"
        days = info.get("days") or []
        assert all(isinstance(d, int) for d in days), f"bucket {tid} has non-int days"
        for d in days:
            assert 1 <= d <= 30, f"bucket {tid} references day {d}, outside 1-30"


def test_json_mapping_file_is_valid_json():
    """_load_mapping would raise on a corrupt file; catch that at the source."""
    with open(mig.MAPPING_PATH, encoding="utf-8") as fh:
        data = json.load(fh)
    assert isinstance(data, dict), "mapping is not a JSON object"

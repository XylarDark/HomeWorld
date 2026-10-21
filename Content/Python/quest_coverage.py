# quest_coverage.py
# Host-only quest coverage matrix. Called by run_quest_tests_host.py
# --coverage and Tools/RunTests.ps1 -QuestCoverage.
#
# One row per opening beat (manifest order): the manifest's checks, the C++
# automation tests DECLARED to cover it (Content/Python/quest_test_coverage.py,
# never inferred from test names), the latest sweep result from
# Saved/quest_tests.json (inconclusive when absent - an absent result is never
# a pass), and the checks that stay human-only.
#
# Outputs:
#   Saved/quest_coverage.json     the full table incl. the volatile results
#   Docs/qa/QUEST_COVERAGE.md     the static snapshot (no timestamps, no
#                                 results, so regeneration is byte-stable and
#                                 a CI run never dirties a tracked file)
#
# Exit codes: 0 built (warnings allowed), 2 nothing to build from - the
# manifest or the declared-coverage sidecar cannot be loaded. A declared test
# name that no longer exists is a warning (the preflight warns too), listed
# under `missing_tests` in the row, because the matrix must stay honest about
# the gap rather than hiding the row.

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import quest_test_contract as contract  # noqa: E402  host-safe, no unreal

PROJECT_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))

COVERAGE_REL = os.path.join("Content", "Python", "quest_test_coverage.py")
RESULTS_REL = os.path.join("Saved", "quest_tests.json")
OUT_JSON_REL = os.path.join("Saved", "quest_coverage.json")
OUT_DOC_REL = os.path.join("Docs", "qa", "QUEST_COVERAGE.md")

INCONCLUSIVE = {"status": "inconclusive", "detail": "no result file"}


def _read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return None


def _write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
    os.replace(tmp, path)


def _shared():
    # Deferred: quest_preflight imports this module for the warn hook, so this
    # module never imports quest_preflight at the top level.
    import quest_preflight as shared
    return shared


def _load_coverage_module(root):
    """COVERAGE from the sidecar file path. Returns (dict, error)."""
    import importlib.util
    path = os.path.join(root, COVERAGE_REL)
    if not os.path.isfile(path):
        return None, "no coverage sidecar at %s" % COVERAGE_REL
    try:
        spec = importlib.util.spec_from_file_location(
            "quest_coverage_sidecar_%d" % len(root), path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as exc:
        return None, "coverage sidecar does not import: %s" % exc
    declared = getattr(module, "COVERAGE", None)
    if not isinstance(declared, dict) or not declared:
        return None, "coverage sidecar has no COVERAGE dict"
    return declared, ""


# ---------------------------------------------------------------------------
# Evaluation: rows + warnings shared by the matrix and the preflight.
# ---------------------------------------------------------------------------


def evaluate(root=None):
    """Return {"beats": [rows], "warnings": [...], "errors": [...]}.

    errors are exit-2 material (nothing to build from); everything else keeps
    the matrix honest with warnings.
    """
    root = os.path.abspath(root or PROJECT_ROOT)
    shared = _shared()
    evaluation = {"beats": [], "warnings": [], "errors": []}

    quests, load_error = shared._load_quests(os.path.join(root, shared.MANIFEST_REL))
    if quests is None:
        evaluation["errors"].append("manifest: %s" % load_error)
        return evaluation
    declared, declared_error = _load_coverage_module(root)
    if declared is None:
        evaluation["errors"].append(declared_error)
        return evaluation

    manifest_rel = shared.MANIFEST_REL.replace(os.sep, "/")
    test_names, test_reason = shared._parse_automation_test_names(
        os.path.join(root, "Source", "HomeWorld"))
    if test_names is None:
        shared._warn_unsure(evaluation["warnings"], "Source/HomeWorld/*.cpp",
                            "IMPLEMENT_*_AUTOMATION_TEST", test_reason)

    known_ids = [quest.get("id") for quest in quests]
    for stray in sorted(set(declared) - set(known_ids)):
        evaluation["warnings"].append(
            "%s: COVERAGE declares beat '%s' but the manifest does not" % (
                COVERAGE_REL.replace(os.sep, "/"), stray))
    for beat_id in known_ids:
        if beat_id not in declared:
            evaluation["warnings"].append(
                "%s: no COVERAGE row for beat '%s'; the matrix shows it undeclared" % (
                    COVERAGE_REL.replace(os.sep, "/"), beat_id))

    results = _read_json(os.path.join(root, RESULTS_REL))
    results_by_id = {}
    results_note = INCONCLUSIVE["detail"]
    if not isinstance(results, dict) or not results.get("done"):
        if isinstance(results, dict) and results.get("run_id"):
            results_note = "latest run %s did not finish" % results.get("run_id")
    else:
        for beat in results.get("beats", []):
            if isinstance(beat, dict) and beat.get("id"):
                results_by_id[beat["id"]] = beat
        results_note = "" if results_by_id else "the finished run left no beat results"

    for index, quest in enumerate(quests):
        beat_id = quest.get("id")
        row = declared.get(beat_id, {})
        row_tests = [name for name in row.get("tests", []) if isinstance(name, str)]
        missing = sorted(
            name for name in row_tests
            if test_names is not None and name not in test_names)
        for name in missing:
            evaluation["warnings"].append(
                "%s: COVERAGE names '%s' for beat '%s' and no such automation test exists"
                % (COVERAGE_REL.replace(os.sep, "/"), name, beat_id))

        if results is not None and not results.get("done"):
            latest = {"status": "inconclusive", "detail": results_note}
        elif beat_id in results_by_id:
            beat_result = results_by_id[beat_id]
            status = beat_result.get("status")
            if status not in ("passed", "failed", "inconclusive"):
                status = "inconclusive"
            latest = {
                "status": status,
                "detail": "%s s, run %s" % (beat_result.get("duration_s"), results.get("run_id")),
                "run_id": results.get("run_id"),
                "started": results.get("started"),
            }
        elif results is not None:
            latest = {"status": "inconclusive", "detail": "not in the latest %s" % results_note}
        else:
            latest = {"status": "inconclusive", "detail": INCONCLUSIVE["detail"]}

        evaluation["beats"].append({
            "index": index + 1,
            "id": beat_id,
            "stop": quest.get("stop") or "(no argument)",
            "section": quest.get("section"),
            "checks": [contract.describe(check) for check in quest.get("checks", [])],
            "declared_tests": row_tests,
            "missing_tests": missing,
            "human_only": [item for item in row.get("human", []) if isinstance(item, str)],
            "latest": latest,
        })
    return evaluation


def declared_warnings(root=None):
    """The warn-only declarations check the preflight runs."""
    evaluation = evaluate(root)
    if evaluation["errors"]:
        return ["coverage matrix: %s" % error for error in evaluation["errors"]]
    return evaluation["warnings"]


# ---------------------------------------------------------------------------
# Output.
# ---------------------------------------------------------------------------


def _markdown(evaluation):
    """The checked-in snapshot. Deliberately static: no timestamps, no latest
    results - so regenerating it is byte-stable and CI never dirties a file."""
    lines = [
        "# Quest coverage matrix",
        "",
        "One row per opening beat, in sweep order. Regenerate with",
        "`python Content/Python/run_quest_tests_host.py --coverage`",
        "(or `Tools/RunTests.ps1 -QuestCoverage`); this file is the static",
        "snapshot. The volatile column - latest result, from",
        "`Saved/quest_tests.json` - lives in `Saved/quest_coverage.json` only,",
        "so a run never changes what is committed here. An absent result is",
        "`inconclusive`, never a pass.",
        "",
        "Coverage is **declared** in [`Content/Python/quest_test_coverage.py`](../../Content/Python/quest_test_coverage.py):",
        "nothing is inferred from test names. The preflight warns when a declared",
        "test name no longer exists. An empty cell is a real gap, not an",
        "oversight - see `fish`, which no automation drives today. Human",
        "judgement stays in [`TUTORIAL_PLAYTEST_QUEUE.md`](TUTORIAL_PLAYTEST_QUEUE.md).",
        "",
        "| # | beat (stop) | manifest checks | Declared C++ automation coverage | Human-only |",
        "|---:|---|---|---|---|",
    ]
    for row in evaluation["beats"]:
        checks = "<br>".join("`%s`" % check for check in row["checks"])
        tests = "<br>".join("`%s`" % name for name in row["declared_tests"]) or "(none declared)"
        human = "<br>".join(row["human_only"]) or "(none)"
        lines.append("| %d | **%s** (`%s`) | %s | %s | %s |" % (
            row["index"], row["id"], row["stop"], checks, tests, human))
    lines.extend([
        "",
        "Library sources for the declared names: `Source/HomeWorld/*Tests.cpp`.",
    ])
    return "\n".join(lines) + "\n"


def build(evaluation):
    """The JSON document written under Saved/."""
    statuses = {}
    for row in evaluation["beats"]:
        statuses[row["latest"]["status"]] = statuses.get(row["latest"]["status"], 0) + 1
    return {
        "beats": evaluation["beats"],
        "warnings": evaluation["warnings"],
        "summary": {
            "beats": len(evaluation["beats"]),
            "beats_with_declared_tests": sum(1 for row in evaluation["beats"] if row["declared_tests"]),
            "beats_without_declared_tests": [
                row["id"] for row in evaluation["beats"] if not row["declared_tests"]],
            "latest_result_statuses": statuses,
        },
    }


def main(root=None):
    evaluation = evaluate(root)
    if evaluation["errors"]:
        for error in evaluation["errors"]:
            print("quest_coverage: FAIL - %s" % error)
        return 2

    document = build(evaluation)
    doc_root = os.path.abspath(root or PROJECT_ROOT)
    json_path = os.path.join(doc_root, OUT_JSON_REL)
    markdown_path = os.path.join(doc_root, OUT_DOC_REL)
    _write_json(json_path, document)
    os.makedirs(os.path.dirname(markdown_path), exist_ok=True)
    with open(markdown_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(_markdown(evaluation))

    for warning in evaluation["warnings"]:
        print("quest_coverage: warn: %s" % warning)
    print("quest_coverage: %d beat(s), %d with declared tests, %d without: %s" % (
        len(evaluation["beats"]),
        document["summary"]["beats_with_declared_tests"],
        len(document["summary"]["beats_without_declared_tests"]),
        ", ".join(document["summary"]["beats_without_declared_tests"]) or "(none)"))
    for row in evaluation["beats"]:
        print("  %2d. %-10s %-14s checks=%-2d tests=%-2d human=%-2d result=%s" % (
            row["index"], row["id"], row["stop"], len(row["checks"]),
            len(row["declared_tests"]), len(row["human_only"]), row["latest"]["status"]))
    print("quest_coverage: results %s" % json_path)
    print("quest_coverage: snapshot %s" % markdown_path)
    return 0

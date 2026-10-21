"""The session door checker: the inline state rule and the path-case check.

Host-only. The case check is fed a synthetic index so each failure class is
planted on purpose; the last test runs the checker on the real tree.
"""

import os
import subprocess
import sys
from pathlib import Path

_content_python = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _content_python not in sys.path:
    sys.path.insert(0, _content_python)

import check_session_start as door  # noqa: E402

PROJECT_ROOT = Path(_content_python).parents[1]

TRACKED = {
    "AGENTS.md",
    "Docs", "Docs/context", "Docs/context/SESSION_START.md", "Docs/qa", "Docs/qa/QUEST_TESTS.md",
    "docs", "docs/SESSION_NOW.md", "docs/KNOWN_ERRORS.md",
    "Tools", "Tools/RunTests.ps1",
    "UserHarness",
}
DOOR = "Docs/context/SESSION_START.md"


def test_a_link_in_the_wrong_case_fails():
    problems = door.path_case_problems(DOOR, "[now](../SESSION_NOW.md)", TRACKED)
    assert problems == [f"{DOOR}: link `../SESSION_NOW.md` is `docs/SESSION_NOW.md` in git (case)"]


def test_a_link_in_git_case_passes():
    assert door.path_case_problems(DOOR, "[now](../../docs/SESSION_NOW.md) [q](../qa/QUEST_TESTS.md)", TRACKED) == []


def test_a_backtick_path_in_the_wrong_case_fails():
    problems = door.path_case_problems(DOOR, "Search `Docs/KNOWN_ERRORS.md` first.", TRACKED)
    assert len(problems) == 1 and "`docs/KNOWN_ERRORS.md` in git (case)" in problems[0]


def test_a_windows_backtick_path_is_checked_too():
    assert door.path_case_problems(DOOR, "Run `.\\Tools\\RunTests.ps1`.", TRACKED) == []
    problems = door.path_case_problems(DOOR, "Run `.\\tools\\RunTests.ps1`.", TRACKED)
    assert len(problems) == 1 and "(case)" in problems[0]


def test_a_link_to_nothing_fails():
    problems = door.path_case_problems("AGENTS.md", "[gone](Docs/GONE.md)", TRACKED)
    assert problems == ["AGENTS.md: link `Docs/GONE.md` resolves to `Docs/GONE.md`, which git does not track"]


def test_urls_anchors_globs_placeholders_and_submodules_are_skipped():
    text = (
        "[web](https://example.com/Docs/x.md) [anchor](#mode) "
        "`Content/Python/tmp_*.py` `Docs/handoffs/SESSION_HANDOFF_<slice>.md` "
        "`UserHarness/docs/human-use/route-context.md` [sub](../../UserHarness/docs/x.md)"
    )
    assert door.path_case_problems(DOOR, text, TRACKED) == []


def test_tracked_paths_lists_parent_directories():
    tracked = door.tracked_paths(PROJECT_ROOT)
    if tracked is None:
        return  # no git on this host; the checker warns and skips
    assert "Docs/context/SESSION_START.md" in tracked
    assert "Docs/context" in tracked


GOOD_STATE = (
    "2. First message, once: `Mode: <solo or co> · State: <agent, decide, or do>`. "
    "In the Look room only, add `· Transition: <the Now line in Docs/art/PHASES.md>`.\n"
    "3. State, first match wins: `decide` ... `do` ... Otherwise `agent`.\n"
    "4. Never a fourth state. The full rule is `UserHarness/docs/human-use/route-context.md`.\n"
)


def test_the_inline_state_rule_passes():
    assert door.state_rule_problems(GOOD_STATE) == []


def test_losing_the_inline_rule_fails():
    problems = door.state_rule_problems(GOOD_STATE.replace("first match wins", "pick one"))
    assert problems == ["door lost the inline state rule: first match wins"]


def test_route_context_as_a_numbered_read_fails():
    text = GOOD_STATE + "1. `UserHarness/docs/human-use/route-context.md` through the state.\n"
    assert "route-context is a numbered start read again; it opens on demand" in door.state_rule_problems(text)


def test_the_transition_outside_the_look_room_fails():
    text = GOOD_STATE.replace("In the Look room only, add", "Add")
    assert "the Transition header reads PHASES.md outside the Look room" in door.state_rule_problems(text)


def test_the_real_door_passes():
    result = subprocess.run(
        [sys.executable, os.path.join(_content_python, "check_session_start.py")],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr

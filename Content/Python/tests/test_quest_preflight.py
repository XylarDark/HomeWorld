# test_quest_preflight.py
# Host tests for the host-only quest preflight. No Editor and no PIE.
#
# The preflight (quest_preflight.py) compares the manifest against the C++
# fast-forward using text parses. A parse that half-understands the source
# must warn and never fail, so the suite proves two behaviours separately:
#   1. the real tree is clean (and the CLI exit is 0), and
#   2. every REAL divergence this check owns exits 2 and names file + symbol,
#      proven by planting that divergence into a disposable copy of the tree.

import os
import shutil
import subprocess
import sys

import pytest

_script_dir = os.path.dirname(os.path.abspath(__file__))
_content_python = os.path.normpath(os.path.join(_script_dir, ".."))
if _content_python not in sys.path:
    sys.path.insert(0, _content_python)

import quest_preflight as preflight

PROJECT_ROOT = os.path.abspath(os.path.join(_content_python, "..", ".."))

_CHARACTER = os.path.join("Source", "HomeWorld", "HomeWorldCharacter.cpp")
_MANIFEST = os.path.join("Content", "Python", "quest_test_manifest.py")
_RUNNER = os.path.join("Content", "Python", "quest_test_runner.py")
_UMAP = os.path.join("Content", "HomeWorld", "Maps", "SizeTest", "L_SizeTest.umap")


@pytest.fixture()
def double_root(tmp_path):
    """A disposable copy of the tree the preflight reads, with a stub map."""
    project = tmp_path / "proj"
    for rel in (_CHARACTER, _MANIFEST, _RUNNER, _UMAP):
        source = os.path.join(PROJECT_ROOT, rel.replace("/", os.sep))
        target = project / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if rel.endswith(".umap"):
            target.write_bytes(b"")
        else:
            shutil.copyfile(source, str(target))
    return project


def _plant(project, rel, old, new):
    path = project / rel
    text = path.read_text(encoding="utf-8")
    assert old in text, "planted fixture text missing from the real tree: %r" % old
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def _labels(problems):
    """Every problem must carry a file and a symbol - that is the contract."""
    labels = ["%s :: %s" % (item["file"], item["symbol"]) for item in problems]
    assert all(
        item["file"] and item["symbol"] and item["detail"] for item in problems
    ), "a problem was reported without its file or symbol"
    return labels


# ---------------------------------------------------------------------------
# The real tree.
# ---------------------------------------------------------------------------


def test_real_tree_is_clean():
    """The real worktree: 0 mismatches. Warnings are allowed and optional."""
    problems, _warnings = preflight.run_preflight(PROJECT_ROOT)
    assert problems == [], _labels(problems)


def test_cli_check_exits_zero_on_the_real_tree():
    """End to end: python run_quest_tests_host.py --check exits 0."""
    result = subprocess.run(
        [sys.executable, os.path.join(_content_python, "run_quest_tests_host.py"), "--check"],
        capture_output=True, text=True, cwd=PROJECT_ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "quest_preflight: PASS" in result.stdout


def test_cli_check_exit_two_when_a_mismatch_is_planted(double_root):
    """The same CLI, pointed at a broken double via main(root), must exit 2."""
    _plant(double_root, _CHARACTER, 'return TEXT("herbs");', 'return TEXT("weeds");')
    assert preflight.main(root=str(double_root)) == 2


def test_help_still_lists_the_sweep_and_the_check():
    result = subprocess.run(
        [sys.executable, os.path.join(_content_python, "run_quest_tests_host.py"), "--help"],
        capture_output=True, text=True, cwd=PROJECT_ROOT,
    )
    assert result.returncode == 0
    assert "--check" in result.stdout


# ---------------------------------------------------------------------------
# Planted real mismatches - each exits 2 and names its file + symbol.
# ---------------------------------------------------------------------------


def test_a_renamed_beat_is_caught(double_root):
    _plant(double_root, _CHARACTER, 'return TEXT("herbs");', 'return TEXT("weeds");')
    problems, _warnings = preflight.run_preflight(str(double_root))
    assert problems, "a renamed PlaytestBeatName case must exit 2"
    assert any("PlaytestBeatName" in symbol for symbol in _labels(problems))


def test_a_manifest_id_the_cpp_does_not_know_is_caught(double_root):
    _plant(double_root, _MANIFEST, '"id": "herbs",', '"id": "weeds",')
    problems, _warnings = preflight.run_preflight(str(double_root))
    assert problems
    assert any("PlaytestBeatName" in symbol for symbol in _labels(problems))
    assert any("DebugFastForwardOpening" in symbol for symbol in _labels(problems))


def test_a_dropped_stop_word_is_caught(double_root):
    _plant(double_root, _MANIFEST, '"stop": "herbs",', '"stop": "hedge",')
    problems, _warnings = preflight.run_preflight(str(double_root))
    assert problems
    assert any("PlaytestBeatFromText" in symbol for symbol in _labels(problems))


def test_a_dropped_cpp_keyword_is_caught(double_root):
    _plant(double_root, _CHARACTER, 'Key.Contains(TEXT("herb"))', 'Key.Contains(TEXT("weeds"))')
    problems, _warnings = preflight.run_preflight(str(double_root))
    assert problems
    assert any("PlaytestBeatFromText" in symbol for symbol in _labels(problems))


def test_a_dropped_state_key_is_caught(double_root):
    _plant(double_root, _CHARACTER, '\\"herbs_gathered\\":%d,', "")
    problems, _warnings = preflight.run_preflight(str(double_root))
    assert problems
    assert any("GetPlaytestStateJson" in symbol for symbol in _labels(problems))


def test_a_popped_key_read_as_quest_is_caught(double_root):
    _plant(
        double_root, _MANIFEST,
        'eq("beat.ready_for", "herbs")', 'eq("quest.ready_for", "herbs")')
    problems, _warnings = preflight.run_preflight(str(double_root))
    assert problems
    assert any("GetPlaytestStateJson" in symbol for symbol in _labels(problems))


def test_an_unknown_beat_key_is_caught(double_root):
    _plant(double_root, _MANIFEST, 'le("beat.ready_distance", 400)', 'le("beat.ready_step", 400)')
    problems, _warnings = preflight.run_preflight(str(double_root))
    assert problems
    assert any("_build_snapshot" in symbol for symbol in _labels(problems))


def test_an_undeclared_actor_group_is_caught(double_root):
    _plant(double_root, _MANIFEST,
           'eq("quest.spirit_claimed", False),',
           'eq("quest.spirit_claimed", False),\n            present("actors.bear.tamed"),')
    problems, _warnings = preflight.run_preflight(str(double_root))
    assert problems
    assert any("_build_snapshot" in symbol for symbol in _labels(problems))


def test_an_unknown_actor_field_is_caught(double_root):
    _plant(double_root, _MANIFEST, 'eq("actors.dog.tamed", False)', 'eq("actors.dog.swapped", False)')
    problems, _warnings = preflight.run_preflight(str(double_root))
    assert problems
    assert any("ACTOR_KEYS" in symbol for symbol in _labels(problems))


def test_a_renamed_runner_actor_is_caught(double_root):
    """The allowlist alone no longer washes a path the runner stopped emitting."""
    _plant(double_root, _RUNNER, 'actors["dog"]', 'actors["hound"]')
    problems, _warnings = preflight.run_preflight(str(double_root))
    assert problems
    dog_problems = [item for item in problems if "actors.dog" in item["detail"]]
    assert dog_problems
    assert all(item["symbol"] == "_build_snapshot" for item in dog_problems)


def test_a_missing_manifest_beat_is_caught(double_root):
    _plant(
        double_root, _MANIFEST,
        '    {\n'
        '        "id": "fish",\n'
        '        "stop": "fish",\n'
        '        "section": "Fishing",\n'
        '        "note": "E at the pond bank, one fish",\n'
        '        "checks": [\n'
        '            eq("beat.ready_for", "fish"),\n'
        '            eq("actors.dog.tamed", True),\n'
        '            eq("quest.fish_caught", False),\n'
        '            eq("quest.mixed_herbs", 0),\n'
        '            le("beat.ready_distance", 1200),\n'
        '            near("actors.partner.location", "actors.reveal.partner_stand", 80),\n'
        '        ],\n'
        '    },\n',
        "")
    problems, _warnings = preflight.run_preflight(str(double_root))
    assert problems
    labels = _labels(problems)
    assert any("PlaytestSkipStep" in symbol for symbol in labels)
    assert any("DebugFastForwardOpening" in symbol for symbol in labels)


def test_a_missing_map_is_caught(double_root):
    os.remove(str(double_root / _UMAP))
    problems, _warnings = preflight.run_preflight(str(double_root))
    assert problems
    assert any(
        item["symbol"] == "LEVEL_PATH" and item["file"].endswith("L_SizeTest.umap")
        for item in problems)
    assert preflight.main(root=str(double_root)) == 2


# ---------------------------------------------------------------------------
# Warn, never fail.
# ---------------------------------------------------------------------------


def test_a_far_off_parse_warns_and_does_not_fail(double_root):
    """Gibberish C++ is 'unsure', not a mismatch: warn and stay exit 0."""
    (double_root / _CHARACTER).write_text("// nobody home\n", encoding="utf-8")
    problems, warnings = preflight.run_preflight(str(double_root))
    assert problems == [], _labels(problems)
    assert any("unsure" in warning for warning in warnings)


def test_a_runner_key_outside_the_allowlist_is_a_warning(double_root):
    _plant(
        double_root, _RUNNER,
        'actors["wisps"] = {"count": tag_counts.get("NODE_OPENING_WISP", 0)}',
        'actors["wisps"] = {"count": tag_counts.get("NODE_OPENING_WISP", 0)}\n'
        '    actors["bear"] = {"tamed": False}')
    problems, warnings = preflight.run_preflight(str(double_root))
    assert problems == [], _labels(problems)
    assert any("stale allowlist" in warning and "bear" in warning for warning in warnings)


def test_a_main_without_root_checks_the_real_tree():
    problems, _warnings = preflight.run_preflight()
    assert problems == [], _labels(problems)


# ---------------------------------------------------------------------------
# Parser units.
# ---------------------------------------------------------------------------


_KEYWORDS = (
    (("PlaytestBeatHeal", ["heal", "spring"]), ("PlaytestBeatHerbs", ["herb"])),
    "PlaytestBeatNight",
)


def test_resolve_stop_uses_cpp_semantics():
    assert preflight._resolve_stop("spring", _KEYWORDS) == "PlaytestBeatHeal"
    assert preflight._resolve_stop("HERB_Gardens", _KEYWORDS) == "PlaytestBeatHerbs"
    assert preflight._resolve_stop("", _KEYWORDS) == "PlaytestBeatNight"
    assert preflight._resolve_stop("soup", _KEYWORDS) is None


_STATE_JSON_STUB = r'''
FString AHomeWorldCharacter::GetPlaytestStateJson() const
{
	return FString::Printf(
		TEXT("{\"ready_for\":\"%s\",\"spirit_claimed\":%s}"),
		*ReadyFor, bFlag ? TEXT("true") : TEXT("false"));
}
'''


def test_state_keys_skip_the_formats_and_catch_the_names():
    keys, sure = preflight._parse_state_keys(_STATE_JSON_STUB)
    assert sure == ""
    assert keys == {"ready_for", "spirit_claimed"}


def test_state_keys_are_unsure_without_the_function():
    value, reason = preflight._parse_state_keys("// nothing here")
    assert value is None and reason


def test_documented_beats_parse_the_log_line():
    value, sure = preflight._parse_documented_beats(
        'UE_LOG(LogTemp, Log, TEXT("playtest_ff: beats: spirit, herbs, heal"));')
    assert sure == ""
    assert value == ["spirit", "herbs", "heal"]


def test_keyword_rules_stop_at_a_contains_line_without_return():
    value, reason = preflight._parse_keyword_rules(
        "int32 PlaytestBeatFromText(const FString& Text)\n"
        "{\n"
        '\tif (Key.Contains(TEXT("herb")) && !Key.Contains(TEXT("x")))\n'
        "\t{\n"
        "\t\treturn 0;\n"
        "\t}\n"
        "\treturn 0;\n"
        "\t}\n"
        "}")
    assert value is None
    assert "without a matching return" in reason


def test_region_needs_both_markers():
    assert preflight._region("alpha beta gamma", "beta", "zeta") is None
    assert preflight._region("alpha beta gamma", "beta", "gamma") == "beta "

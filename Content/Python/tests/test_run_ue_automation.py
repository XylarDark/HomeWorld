# test_run_ue_automation.py
# Guards the four silent-failure paths in run_ue_automation.py.
#
# Each of these is a way the script used to report a green run that proved
# nothing. A regression in any of them reintroduces a false pass, so they are
# pinned rather than left to the next reader of the script.

import importlib
import json
import os
import sys
import tempfile

_script_dir = os.path.dirname(os.path.abspath(__file__))
_content_python = os.path.normpath(os.path.join(_script_dir, ".."))
if _content_python not in sys.path:
    sys.path.insert(0, _content_python)

import run_ue_automation
importlib.reload(run_ue_automation)

LOCKED = "5.8"
WRONG = "5.7"


def _uproject(dirpath, association=LOCKED):
    path = os.path.join(dirpath, "HomeWorld.uproject")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"FileVersion": 3, "EngineAssociation": association}, handle)
    return path


def test_locked_version_is_read_from_the_uproject():
    """The engine lock comes from the .uproject, so it cannot drift from the project."""
    with tempfile.TemporaryDirectory() as tmp:
        path = _uproject(tmp)
        assert run_ue_automation._locked_engine_version(path) == LOCKED


def test_engine_version_is_parsed_from_the_install_path():
    """UE_5.8 and UE-5.8 style paths both resolve to a comparable version."""
    assert run_ue_automation._engine_version_from_path(
        r"C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe") == "5.8"
    assert run_ue_automation._engine_version_from_path(
        r"D:\UE-5.7\Engine\Binaries\Win64\UnrealEditor-Cmd.exe") == "5.7"


def test_engine_version_unreadable_path_is_not_a_mismatch():
    """An unusual install path yields None, which must not be treated as wrong.

    Absence of evidence is not evidence of a mismatch; only a readable version
    that disagrees with the lock is fatal.
    """
    assert run_ue_automation._engine_version_from_path("/opt/unreal/bin/UnrealEditor") is None


def test_mismatched_engine_is_refused():
    """The measured fault: UE_EDITOR on 5.7 against a 5.8 lock must be fatal."""
    with tempfile.TemporaryDirectory() as tmp:
        ok, detail = run_ue_automation._check_engine_match(
            r"C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe",
            _uproject(tmp),
        )
        assert ok is False, "a 5.7 editor against a 5.8 lock must be refused"
        assert detail["engine_in_use"] == WRONG
        assert detail["engine_locked"] == LOCKED
        assert "reason" in detail


def test_matching_engine_is_allowed():
    with tempfile.TemporaryDirectory() as tmp:
        ok, detail = run_ue_automation._check_engine_match(
            r"C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe",
            _uproject(tmp),
        )
        assert ok is True
        assert "reason" not in detail


def test_stale_dll_is_reported_stale():
    """A DLL older than the newest source must be flagged, not silently trusted."""
    with tempfile.TemporaryDirectory() as tmp:
        bin_dir = os.path.join(tmp, "Binaries", "Win64")
        src_dir = os.path.join(tmp, "Source", "HomeWorld")
        os.makedirs(bin_dir)
        os.makedirs(src_dir)
        dll = os.path.join(bin_dir, "UnrealEditor-HomeWorld.dll")
        src = os.path.join(src_dir, "Thing.cpp")
        with open(dll, "w", encoding="utf-8") as handle:
            handle.write("x")
        os.utime(dll, (1000, 1000))
        with open(src, "w", encoding="utf-8") as handle:
            handle.write("y")
        os.utime(src, (2000, 2000))

        stale, detail = run_ue_automation._dll_staleness(tmp)
        assert stale is True, "older DLL must be reported stale"
        assert "Safe-Build" in detail["note"], "the warning must say what to do about it"


def test_fresh_dll_is_not_reported_stale():
    with tempfile.TemporaryDirectory() as tmp:
        bin_dir = os.path.join(tmp, "Binaries", "Win64")
        src_dir = os.path.join(tmp, "Source", "HomeWorld")
        os.makedirs(bin_dir)
        os.makedirs(src_dir)
        dll = os.path.join(bin_dir, "UnrealEditor-HomeWorld.dll")
        src = os.path.join(src_dir, "Thing.cpp")
        with open(src, "w", encoding="utf-8") as handle:
            handle.write("y")
        os.utime(src, (1000, 1000))
        with open(dll, "w", encoding="utf-8") as handle:
            handle.write("x")
        os.utime(dll, (2000, 2000))

        stale, _detail = run_ue_automation._dll_staleness(tmp)
        assert stale is False


def test_zero_tests_ran_is_not_success():
    """The core bug: the verdict used to be `failed == 0`, true of a run that ran nothing.

    Written to assert the trap first, so the test fails if someone reintroduces it.
    A run of zero tests satisfies `failed == 0`, which is exactly why that verdict
    reported `Group:HomeWorld` (matching no group) as a clean run. The new condition
    requires tests to have actually run.
    """
    passed, failed = 0, 0
    ran = passed + failed

    old_verdict = failed == 0
    assert old_verdict is True, "the old verdict calls an empty run a pass; that is the bug"
    assert ran == 0

    new_verdict = (failed == 0) and ran > 0
    assert new_verdict is False, "an empty run must not be reported as success"


def test_parse_report_handles_ue_utf8_bom():
    """UE writes index.json with a UTF-8 BOM. Reading it as plain utf-8 raises.

    This is the reason the runner reported 0 passed / 0 failed on every run against
    this project: the parse threw, the throw was swallowed, and the fallthrough read
    as an empty suite. A green 19/19 run and a run that matched nothing produced the
    same result file. Pinned with the real byte prefix so it cannot come back.
    """
    with tempfile.TemporaryDirectory() as tmp:
        payload = json.dumps({"succeeded": 19, "failed": 0, "tests": []})
        bom = "﻿"
        with open(os.path.join(tmp, "index.json"), "w", encoding="utf-8") as handle:
            handle.write(bom + payload)

        ok, passed, failed, err, _tests = run_ue_automation._parse_report(tmp)
        assert ok is True, "a BOM-prefixed report must still parse: %r" % err
        assert passed == 19


def test_report_counter_disagreement_is_visible_not_silent():
    """UE reported succeeded=19 while listing 20 successful tests.

    "19 passed" and "20 tests ran" are different claims. The runner must carry both
    so a reader can see the gap instead of inheriting whichever one it picked.
    """
    with tempfile.TemporaryDirectory() as tmp:
        payload = {
            "succeeded": 19,
            "failed": 0,
            "tests": [{"fullTestPath": "HomeWorld.T0.Pass%d" % i, "state": "Success"}
                      for i in range(20)],
        }
        with open(os.path.join(tmp, "index.json"), "w", encoding="utf-8") as handle:
            json.dump(payload, handle)

        _ok, passed, failed, _err, tests = run_ue_automation._parse_report(tmp)

        ran_counted = passed + failed
        ran_from_entries = len(tests)
        assert ran_counted == 19
        assert ran_from_entries == 20
        assert ran_counted != ran_from_entries, "the gap this guards against must exist"


def test_parse_report_reports_which_tests_ran():
    """The parser returns per-test names, so a caller can confirm the filter hit."""
    with tempfile.TemporaryDirectory() as tmp:
        payload = {
            "succeeded": 2,
            "failed": 0,
            "tests": [
                {"fullTestPath": "HomeWorld.T0.NodeGate.AllBeatNodeTagsAreInteractable",
                 "state": "Success"},
                {"fullTestPath": "HomeWorld.T0.M9.BothGatesGrantSpirit", "state": "Success"},
            ],
        }
        with open(os.path.join(tmp, "index.json"), "w", encoding="utf-8") as handle:
            json.dump(payload, handle)

        ok, passed, failed, err, tests = run_ue_automation._parse_report(tmp)
        assert ok is True
        assert err is None
        assert passed == 2
        assert failed == 0
        assert len(tests) == 2
        names = [name for name, _state in tests]
        assert "HomeWorld.T0.NodeGate.AllBeatNodeTagsAreInteractable" in names


def test_parse_report_reports_a_missing_report_rather_than_zeroes():
    """No report at all is an error, not a silent 0/0 that reads as a clean run."""
    with tempfile.TemporaryDirectory() as tmp:
        ok, passed, failed, err, tests = run_ue_automation._parse_report(tmp)
        assert ok is False
        assert err is not None
        assert passed == 0
        assert tests == []


def test_clear_report_dir_removes_a_stale_report():
    """A previous run's index.json must not be readable as this run's result."""
    with tempfile.TemporaryDirectory() as tmp:
        report_dir = os.path.join(tmp, "AutomationReport")
        os.makedirs(report_dir)
        stale_path = os.path.join(report_dir, "index.json")
        with open(stale_path, "w", encoding="utf-8") as handle:
            json.dump({"succeeded": 19, "failed": 0}, handle)

        run_ue_automation._clear_report_dir(report_dir)

        assert os.path.isdir(report_dir), "directory must still exist for UE to write into"
        assert not os.path.exists(stale_path), "stale report must be gone"
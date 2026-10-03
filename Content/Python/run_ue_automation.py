# run_ue_automation.py
# Host-side script: runs UnrealEditor with automation test args, parses the report, writes result JSON.
# Run from project root: py Content/Python/run_ue_automation.py --filter HomeWorld.T0
# Requires: UE_EDITOR env set to UnrealEditor.exe path. Optional: HOMEWORLD_PROJECT for .uproject path.
# Outputs: Saved/automation_run_result.json; exit 0 if all passed, 1 otherwise.
# See docs/FULL_AUTOMATION_RESEARCH.md (Implementation Phase 2).
#
# WHY THIS SCRIPT REFUSES TO REPORT SUCCESS BLINDLY
#
# Five ways this script used to report a green run that proved nothing. All five are
# now hard errors, because a clean result file is not evidence and this file is the
# thing people trust instead of reading the UE log.
#
# 0. THE REPORT WAS NEVER PARSED AT ALL. This is the one that mattered, and it is
#    first because the other four were found while chasing it. UE writes index.json
#    with a UTF-8 BOM. json.load on a BOM-prefixed file raises JSONDecodeError, the
#    old except clause caught it, and the loop fell through to "No report JSON
#    found" - so the script reported 0 passed / 0 failed on every run against this
#    project, green or red, forever. Nothing had ever been measured by this file.
#    Read it as utf-8-sig. There is a regression test with a real BOM byte prefix.
#
# 1. WRONG ENGINE, SILENTLY. The editor path came from UE_EDITOR and was never checked
#    against the project's engine lock. On this machine UE_EDITOR pointed at UE 5.7
#    against a 5.8 lock, so UE ran the wrong engine and the script reported
#    `passed: 0, failed: 0, success: false` with no hint that the engine was wrong.
#    The lock is read from the .uproject `EngineAssociation`, so it cannot drift.
#
# 2. A FILTER THAT MATCHES NOTHING IS A PASS. `Automation RunTest Group:<x>` filters
#    UE test *groups*, not name prefixes. `Group:HomeWorld` matches no group in this
#    project, so the run queued nothing, and `success` was computed as
#    `failed == 0` - which is true of a run that executed nothing at all. The fix is
#    `--filter` (a name prefix, `Automation RunTests <prefix>`), and any run that
#    completes zero tests is now an error regardless of filter form.
#
# 3. A STALE REPORT WAS READ AS THIS RUN'S RESULT. The report directory was created
#    but never cleared, so a run that failed to produce a report parsed the previous
#    run's index.json and reported its numbers. The directory is now removed first.
#
# 4. A STALE BINARY. Nothing here builds, so this is reported rather than enforced:
#    if Binaries/Win64/UnrealEditor-HomeWorld.dll is older than the newest source
#    under Source/, the result carries `dll_stale: true` and a warning is printed.
#    A green run against a stale binary is the exact failure this project hit on
#    2026-10-02, where a 19/19 Success was produced by a DLL nine minutes older than
#    the source it claimed to test.

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from typing import Optional

PREFIX = "run_ue_automation:"


def _log(msg: str, data: Optional[dict] = None) -> None:
    parts = [PREFIX, msg]
    if data is not None:
        parts.append(json.dumps(data))
    print(" ".join(parts))


def _resolve_paths():
    """Resolve UE editor exe, project dir, and .uproject path."""
    ue_editor = os.environ.get("UE_EDITOR", "").strip()
    if not ue_editor or not os.path.isfile(ue_editor):
        _log("UE_EDITOR env not set or not a file", {"UE_EDITOR": ue_editor or "(empty)"})
        return None, None, None

    project_dir = os.environ.get("HOMEWORLD_PROJECT", "").strip() or os.getcwd()
    project_dir = os.path.abspath(project_dir)
    if not os.path.isdir(project_dir):
        _log("Project dir not found", {"project_dir": project_dir})
        return ue_editor, None, None

    uproject = None
    for name in sorted(os.listdir(project_dir)):
        if name.endswith(".uproject"):
            uproject = os.path.join(project_dir, name)
            break
    if not uproject or not os.path.isfile(uproject):
        _log("No .uproject found in project dir", {"project_dir": project_dir})
        return ue_editor, project_dir, None

    return ue_editor, project_dir, uproject


def _engine_version_from_path(ue_editor: str) -> Optional[str]:
    """Pull the engine version out of an install path such as .../UE_5.8/Engine/... .

    Returns None when the path does not name a version, which is not treated as a
    mismatch: some machines install elsewhere. A version we can read but that
    disagrees with the lock is treated as fatal, because that case has bitten.
    """
    match = re.search(r"UE[-_ ]?(\d+\.\d+)", ue_editor)
    return match.group(1) if match else None


def _locked_engine_version(uproject: str) -> Optional[str]:
    """Read EngineAssociation from the .uproject. This is the project's engine lock."""
    try:
        with open(uproject, encoding="utf-8") as handle:
            data = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return None
    association = data.get("EngineAssociation")
    if isinstance(association, str) and association.strip():
        return association.strip()
    return None


def _check_engine_match(ue_editor: str, uproject: str) -> tuple:
    """Return (ok, detail). Fatal only when both versions are known and differ."""
    running = _engine_version_from_path(ue_editor)
    locked = _locked_engine_version(uproject)
    detail = {"engine_in_use": running, "engine_locked": locked}
    if running and locked and running != locked:
        detail["reason"] = "UE_EDITOR points at a different engine than the project lock"
        return False, detail
    return True, detail


def _dll_staleness(project_dir: str) -> tuple:
    """Return (is_stale, detail) for the editor module DLL against Source/.

    Reported, not enforced: this script does not own build policy. It exists
    because a green run against a stale binary is indistinguishable from a real
    one unless something says otherwise.
    """
    dll_path = os.path.join(project_dir, "Binaries", "Win64", "UnrealEditor-HomeWorld.dll")
    source_dir = os.path.join(project_dir, "Source")
    detail = {"dll": dll_path, "dll_exists": os.path.isfile(dll_path)}
    if not detail["dll_exists"] or not os.path.isdir(source_dir):
        detail["note"] = "no editor DLL or no Source dir; staleness not determined"
        return False, detail

    dll_mtime = os.path.getmtime(dll_path)
    newest_path = None
    newest_mtime = 0.0
    for root, _dirs, files in os.walk(source_dir):
        for name in files:
            if not name.endswith((".cpp", ".h")):
                continue
            path = os.path.join(root, name)
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                continue
            if mtime > newest_mtime:
                newest_mtime = mtime
                newest_path = path
    detail["newest_source"] = newest_path
    if newest_path is None:
        return False, detail
    detail["dll_mtime"] = dll_mtime
    detail["newest_source_mtime"] = newest_mtime
    stale = dll_mtime < newest_mtime
    if stale:
        detail["note"] = (
            "editor DLL is older than the newest source; a green run here is NOT evidence "
            "for the current source. Build first with Tools/Safe-Build.ps1."
        )
    return stale, detail


def _clear_report_dir(report_dir: str) -> None:
    """Remove a previous run's report so its numbers cannot be read as this run's."""
    if os.path.isdir(report_dir):
        shutil.rmtree(report_dir, ignore_errors=True)
    os.makedirs(report_dir, exist_ok=True)


def _await_report(report_dir: str, timeout: float = 60.0, interval: float = 0.25) -> tuple:
    """Wait for UE to finish writing its report, then parse it.

    `Automation ...; Quit` exits the editor from the automation command line while the
    automation controller is still flushing the report, so the process can be gone a
    moment before index.json lands. Reading the directory immediately would report
    "No report JSON found" for a run that in fact passed.

    This ordering is a plausible failure mode, not one that has been observed here. The
    failure that actually produced zero results on every run was the UTF-8 BOM in
    _parse_report, not a race; the wait is kept because the sequence above is real and
    costs nothing when the report is already present. Do not cite this as the cause of
    a zero-test run without checking the log for "Writing reports to".
    """
    deadline = time.monotonic() + timeout
    parsed = _parse_report(report_dir)
    while not parsed[0] and time.monotonic() < deadline:
        time.sleep(interval)
        parsed = _parse_report(report_dir)
    return parsed


def _parse_report(report_dir: str) -> tuple:
    """Parse UE automation report JSON.

    Returns (success, passed, failed, error, tests) where tests is a list of
    (fullTestPath, state) so a caller can confirm which tests actually ran.
    """
    index_path = os.path.join(report_dir, "index.json")
    candidates = [index_path]
    if os.path.isdir(report_dir):
        candidates += [
            os.path.join(report_dir, name)
            for name in sorted(os.listdir(report_dir))
            if name.endswith(".json") and name != "index.json"
        ]

    for path in candidates:
        if not os.path.isfile(path):
            continue
        try:
            # utf-8-sig, not utf-8. UE writes the report with a UTF-8 BOM, and
            # json.load on a BOM-prefixed file raises JSONDecodeError. This script
            # used to catch that and fall through to "No report JSON found", so
            # every run reported 0 passed / 0 failed regardless of what actually
            # ran - a green suite and an empty one produced the same result file.
            with open(path, encoding="utf-8-sig") as handle:
                data = json.load(handle)
        except (json.JSONDecodeError, OSError, UnicodeDecodeError):
            continue
        try:
            succeeded = int(data.get("succeeded", 0))
            failed = int(data.get("failed", 0))
        except (TypeError, ValueError):
            continue
        tests = []
        for entry in data.get("tests") or []:
            if isinstance(entry, dict):
                tests.append((entry.get("fullTestPath", "?"), entry.get("state", "?")))
        return True, succeeded, failed, None, tests

    return False, 0, 0, "No report JSON found in " + report_dir, []


def _write_result(project_dir: str, result: dict) -> str:
    saved = os.path.join(project_dir, "Saved")
    os.makedirs(saved, exist_ok=True)
    out_path = os.path.join(saved, "automation_run_result.json")
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
    return out_path


def main() -> int:
    _log("started")
    ue_editor, project_dir, uproject = _resolve_paths()
    if not uproject:
        _write_result(project_dir or os.getcwd(), {
            "success": False, "passed": 0, "failed": 0, "report_path": "",
            "error": "Bad paths (see log)", "tests": [],
        })
        _log("completed", {"success": False, "error": "Bad paths (see log)"})
        return 1

    parser = argparse.ArgumentParser(
        description="Run UE automation and parse the report",
        epilog=(
            "--filter takes a test-name prefix (e.g. HomeWorld.T0) and is what this "
            "project's tests are named for. --group takes a UE group name and matches "
            "no group in this project; it is kept only for callers that already pass one."
        ),
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--filter", dest="filter", help="Test name prefix, e.g. HomeWorld.T0")
    mode.add_argument("--group", dest="group", help="UE group name (matches nothing here)")
    parser.add_argument("--timeout", type=int, default=1800, help="Seconds (default: 1800)")
    parser.add_argument(
        "--no-null-rhi",
        dest="null_rhi",
        action="store_false",
        help="Render instead of using NullRHI; slower, needed only for render-dependent tests",
    )
    parser.set_defaults(null_rhi=True)
    args = parser.parse_args()

    if args.filter:
        exec_cmd = f"Automation RunTests {args.filter}; Quit"
        selector = {"kind": "filter", "value": args.filter}
    elif args.group:
        exec_cmd = f"Automation RunTest Group:{args.group}; Quit"
        selector = {"kind": "group", "value": args.group}
        _log("warning", {
            "message": "group selector matches UE groups, not test names; if this reports "
                       "zero tests, use --filter with a name prefix",
        })
    else:
        exec_cmd = "Automation RunTests HomeWorld; Quit"
        selector = {"kind": "filter", "value": "HomeWorld"}

    engine_ok, engine_detail = _check_engine_match(ue_editor, uproject)
    if not engine_ok:
        _log("refusing to run", engine_detail)
        _write_result(project_dir, {
            "success": False, "passed": 0, "failed": 0, "report_path": "",
            "error": engine_detail["reason"], "tests": [], "engine": engine_detail,
            "selector": selector,
        })
        return 1

    stale, stale_detail = _dll_staleness(project_dir)
    if stale:
        _log("warning", stale_detail)

    report_dir = os.path.join(project_dir, "Saved", "AutomationReport")
    _clear_report_dir(report_dir)
    report_dir_abs = os.path.abspath(report_dir)

    # The exec-cmd value contains spaces, so it must survive argv quoting. UE's
    # FParse::Value only keeps it whole when the value is wrapped in literal
    # double quotes in the raw command line. Node/Python list argv escaping
    # wraps the whole argument instead (`"-ExecCmds=..."`), which turns the
    # value into just "Automation" - the deferred queue then carries only
    # `Automation`, and the automation state machine idles without running.
    cmd_line = (
        f'"{ue_editor}" "{uproject}" '
        f'-ExecCmds="{exec_cmd}" '
        f'-ReportExportPath="{report_dir_abs}" '
        "-Unattended -NoPause -NoSplash"
    )
    if args.null_rhi:
        cmd_line += " -NullRHI"
    _log("invoking UE", {"cmd": cmd_line, "cwd": project_dir, "selector": selector})

    timed_out = False
    ue_exit = None
    try:
        completed = subprocess.run(cmd_line, cwd=project_dir, timeout=args.timeout,
                                   capture_output=True, text=True)
        ue_exit = completed.returncode
    except subprocess.TimeoutExpired:
        timed_out = True
    except OSError as exc:
        _write_result(project_dir, {
            "success": False, "passed": 0, "failed": 0, "report_path": report_dir_abs,
            "error": str(exc), "tests": [], "engine": engine_detail, "selector": selector,
            "dll_stale": stale, "dll_detail": stale_detail,
        })
        _log("completed", {"success": False, "error": str(exc)})
        return 1

    if timed_out:
        error = "Process timed out (%ss)" % args.timeout
        _write_result(project_dir, {
            "success": False, "passed": 0, "failed": 0, "report_path": report_dir_abs,
            "error": error, "tests": [], "engine": engine_detail, "selector": selector,
            "dll_stale": stale, "dll_detail": stale_detail,
        })
        _log("completed", {"success": False, "error": error})
        return 1

    parse_ok, passed, failed, parse_err, tests = _await_report(report_dir_abs)
    ran_counted = passed + failed

    # UE's summary counters and its own list of tests can disagree. Observed on
    # 2026-10-02: the report listed 20 tests, all Success, while `succeeded` read
    # 19. Rather than silently prefer one, count what actually ran from the entries
    # and report the discrepancy, because "19 passed" and "20 tests listed" are
    # different claims and a reader should not have to guess which was believed.
    ran_from_entries = len(tests)
    if ran_from_entries and ran_from_entries != ran_counted:
        _log("warning", {
            "message": "report counters disagree with the tests listed in the report",
            "succeeded_plus_failed": ran_counted,
            "tests_listed": ran_from_entries,
        })
    ran = ran_from_entries if ran_from_entries else ran_counted

    result = {
        "success": False,
        "passed": passed,
        "failed": failed,
        "ran": ran,
        "ran_from_report_counters": ran_counted,
        "ran_from_report_entries": ran_from_entries,
        "report_path": report_dir_abs,
        "error": None,
        "ue_exit_code": ue_exit,
        "tests": [{"name": name, "state": state} for name, state in tests],
        "engine": engine_detail,
        "selector": selector,
        "dll_stale": stale,
        "dll_detail": stale_detail,
    }

    if not parse_ok:
        result["error"] = parse_err or "Parse failed"
    elif ran > 0 and ue_exit not in (0, None):
        # Tests ran and reported, but the editor exited non-zero. Trust the report
        # over the exit code and say so, rather than discarding a real result.
        _log("warning", {
            "ue_exit_code": ue_exit,
            "message": "tests ran and reported, but the editor exited non-zero; "
                       "the report is being trusted over the exit code",
        })
        result["success"] = failed == 0
    elif ran == 0:
        # A run that executed nothing is not a pass. Previously this reported
        # success, because the verdict was computed as `failed == 0`.
        result["error"] = (
            "0 tests ran; the selector matched nothing, so this run proves nothing. "
            "Use --filter with a test-name prefix such as HomeWorld.T0."
        )
    else:
        result["success"] = failed == 0

    _write_result(project_dir, result)
    _log("completed", {
        "success": result["success"], "passed": passed, "failed": failed, "ran": ran,
        "error": result["error"],
    })
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
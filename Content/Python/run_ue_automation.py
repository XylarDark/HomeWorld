# run_ue_automation.py
# Host-side script: runs UnrealEditor with automation test args, parses the report, writes result JSON.
# Run from project root: py Content/Python/run_ue_automation.py
# Requires: UE_EDITOR env set to UnrealEditor.exe path. Optional: HOMEWORLD_PROJECT for .uproject path.
# Outputs: Saved/automation_run_result.json; exit 0 if all passed, 1 otherwise.
# See docs/FULL_AUTOMATION_RESEARCH.md (Implementation Phase 2).

import argparse
import json
import os
import subprocess
import sys
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
    for name in os.listdir(project_dir):
        if name.endswith(".uproject"):
            uproject = os.path.join(project_dir, name)
            break
    if not uproject or not os.path.isfile(uproject):
        _log("No .uproject found in project dir", {"project_dir": project_dir})
        return ue_editor, project_dir, None

    return ue_editor, project_dir, uproject


def _parse_report(report_dir: str) -> tuple:
    """Parse UE automation report JSON. Returns (success, passed, failed, error)."""
    index_path = os.path.join(report_dir, "index.json")
    if os.path.isfile(index_path):
        try:
            with open(index_path, encoding="utf-8") as f:
                data = json.load(f)
            succeeded = int(data.get("succeeded", 0))
            failed = int(data.get("failed", 0))
            return True, succeeded, failed, None
        except (json.JSONDecodeError, OSError) as e:
            return False, 0, 0, str(e)

    for name in os.listdir(report_dir):
        if name.endswith(".json") and name != "index.json":
            path = os.path.join(report_dir, name)
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                succeeded = int(data.get("succeeded", 0))
                failed = int(data.get("failed", 0))
                return True, succeeded, failed, None
            except (json.JSONDecodeError, OSError):
                continue

    return False, 0, 0, "No report JSON found in " + report_dir


def main() -> int:
    _log("started")
    ue_editor, project_dir, uproject = _resolve_paths()
    if not uproject:
        result = {"success": False, "passed": 0, "failed": 0, "report_path": "", "error": "Bad paths (see log)"}
        saved = os.path.join(project_dir or os.getcwd(), "Saved")
        os.makedirs(saved, exist_ok=True)
        out_path = os.path.join(saved, "automation_run_result.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        _log("completed", {"success": False, "error": result["error"]})
        return 1

    report_dir = os.path.join(project_dir, "Saved", "AutomationReport")
    os.makedirs(report_dir, exist_ok=True)
    report_dir_abs = os.path.abspath(report_dir)

    parser = argparse.ArgumentParser(description="Run UE automation and parse report")
    parser.add_argument("--group", default="Smoke", help="Test group (default: Smoke)")
    args = parser.parse_args()

    exec_cmd = f"Automation RunTest Group:{args.group};Quit"
    cmd = [
        ue_editor,
        uproject,
        f"-ExecCmds={exec_cmd}",
        f"-ReportExportPath={report_dir_abs}",
        "-Unattended",
    ]
    _log("invoking UE", {"cmd": cmd, "cwd": project_dir})

    try:
        proc = subprocess.run(
            cmd,
            cwd=project_dir,
            timeout=600,
            capture_output=True,
            text=True,
        )
    except subprocess.TimeoutExpired:
        result = {
            "success": False,
            "passed": 0,
            "failed": 0,
            "report_path": report_dir_abs,
            "error": "Process timed out (600s)",
        }
        out_path = os.path.join(project_dir, "Saved", "automation_run_result.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        _log("completed", {"success": False, "error": result["error"]})
        return 1
    except OSError as e:
        result = {
            "success": False,
            "passed": 0,
            "failed": 0,
            "report_path": report_dir_abs,
            "error": str(e),
        }
        out_path = os.path.join(project_dir, "Saved", "automation_run_result.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        _log("completed", {"success": False, "error": result["error"]})
        return 1

    parse_ok, passed, failed, parse_err = _parse_report(report_dir_abs)
    if not parse_ok:
        result = {
            "success": False,
            "passed": 0,
            "failed": 0,
            "report_path": report_dir_abs,
            "error": parse_err or "Parse failed",
        }
    else:
        result = {
            "success": failed == 0,
            "passed": passed,
            "failed": failed,
            "report_path": report_dir_abs,
            "error": None,
        }

    out_path = os.path.join(project_dir, "Saved", "automation_run_result.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    _log("completed", {"success": result["success"], "passed": passed, "failed": failed})
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())

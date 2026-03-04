# run_automation_cycle.py
# Host-side orchestrator: build, Editor lifecycle (launch, wait for port 55557, graceful close), optional headless script runs and tests.
# Run from project root: py Content/Python/run_automation_cycle.py [--task N] [--no-build] [--editor-mode headless|mcp] [--close-editor]
# Requires: UE_EDITOR env set to UnrealEditor.exe path. Optional: HOMEWORLD_PROJECT for project root.
# See plan: full_automation_development_cycle (CYCLE_TASKLIST, CYCLE_STATE); docs/FULL_AUTOMATION_RESEARCH.md.

import argparse
import json
import os
import socket
import subprocess
import sys
import time
from typing import Optional

PREFIX = "run_automation_cycle:"
MCP_PORT = 55557
PORT_WAIT_TIMEOUT = 300
PORT_POLL_INTERVAL = 5


def _log(msg: str, data: Optional[dict] = None) -> None:
    parts = [PREFIX, msg]
    if data is not None:
        parts.append(json.dumps(data))
    print(" ".join(parts))


def _project_root() -> Optional[str]:
    """Resolve project root (directory containing .uproject)."""
    project_dir = os.environ.get("HOMEWORLD_PROJECT", "").strip() or os.getcwd()
    project_dir = os.path.abspath(project_dir)
    if not os.path.isdir(project_dir):
        _log("Project dir not found", {"project_dir": project_dir})
        return None
    for name in os.listdir(project_dir):
        if name.endswith(".uproject"):
            return project_dir
    _log("No .uproject in project dir", {"project_dir": project_dir})
    return None


def _resolve_editor_and_project() -> tuple[Optional[str], Optional[str], Optional[str]]:
    """Return (ue_editor_exe, project_root, uproject_path) or (None,*,*) on failure."""
    ue_editor = os.environ.get("UE_EDITOR", "").strip()
    if not ue_editor or not os.path.isfile(ue_editor):
        _log("UE_EDITOR env not set or not a file", {"UE_EDITOR": ue_editor or "(empty)"})
        return None, _project_root(), None

    root = _project_root()
    if not root:
        return ue_editor, None, None

    uproject = None
    for name in os.listdir(root):
        if name.endswith(".uproject"):
            uproject = os.path.join(root, name)
            break
    if not uproject or not os.path.isfile(uproject):
        _log("No .uproject found", {"project_dir": root})
        return ue_editor, root, None

    return ue_editor, root, uproject


def is_editor_running() -> bool:
    """Return True if UnrealEditor.exe is running (Windows)."""
    try:
        out = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq UnrealEditor.exe", "/NH"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return "UnrealEditor.exe" in (out.stdout or "")
    except (subprocess.TimeoutExpired, OSError):
        return False


def run_build(project_root: str) -> tuple[bool, Optional[str]]:
    """Run Build-HomeWorld.bat from project_root. Parse Build-HomeWorld.log for success. Returns (success, error_message)."""
    build_bat = os.path.join(project_root, "Build-HomeWorld.bat")
    log_path = os.path.join(project_root, "Build-HomeWorld.log")
    if not os.path.isfile(build_bat):
        return False, "Build-HomeWorld.bat not found"

    _log("build started", {"cwd": project_root})
    try:
        proc = subprocess.run(
            [build_bat],
            cwd=project_root,
            timeout=600,
            capture_output=True,
            text=True,
            shell=True,
        )
    except subprocess.TimeoutExpired:
        return False, "Build timed out (600s)"
    except OSError as e:
        return False, str(e)

    if not os.path.isfile(log_path):
        return False, "Build-HomeWorld.log not found after run"

    with open(log_path, encoding="utf-8", errors="replace") as f:
        log_content = f.read()
    if "Exit code: 0" in log_content:
        _log("build completed", {"success": True})
        return True, None
    _log("build completed", {"success": False, "exit_code": proc.returncode})
    return False, f"Build failed (see {log_path})"


def wait_for_port(port: int = MCP_PORT, timeout: float = PORT_WAIT_TIMEOUT) -> bool:
    """Wait until port is accepting connections. Returns True if ready, False on timeout."""
    deadline = time.perf_counter() + timeout
    while time.perf_counter() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=5):
                pass
            _log("port ready", {"port": port})
            return True
        except OSError:
            time.sleep(min(PORT_POLL_INTERVAL, max(0, deadline - time.perf_counter())))
    _log("port wait timeout", {"port": port, "timeout": timeout})
    return False


def launch_editor(ue_editor: str, uproject: str, project_root: str, unattended: bool = True) -> Optional[subprocess.Popen]:
    """Launch UnrealEditor with uproject. Returns Popen instance or None on failure."""
    cmd = [ue_editor, uproject]
    if unattended:
        cmd.append("-UNATTENDED")
    _log("launching Editor", {"cmd": cmd})
    try:
        p = subprocess.Popen(
            cmd,
            cwd=project_root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return p
    except OSError as e:
        _log("launch failed", {"error": str(e)})
        return None


def run_headless_script(ue_editor: str, uproject: str, project_root: str, script_rel: str) -> tuple[bool, Optional[str]]:
    """Run one Editor Python script via -ExecutePythonScript (Editor starts, runs script, exits). Returns (success, error_message)."""
    script_path = os.path.join(project_root, "Content", "Python", script_rel.replace("/", os.sep))
    if not os.path.isfile(script_path):
        return False, f"Script not found: {script_path}"
    cmd = [ue_editor, uproject, f"-ExecutePythonScript={script_path}", "-UNATTENDED"]
    _log("headless script", {"script": script_rel})
    try:
        proc = subprocess.run(
            cmd,
            cwd=project_root,
            timeout=600,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            return False, f"Script exited with code {proc.returncode}"
        return True, None
    except subprocess.TimeoutExpired:
        return False, "Script run timed out (600s)"
    except OSError as e:
        return False, str(e)


def load_cycle_config(project_root: str) -> Optional[dict]:
    """Load automation_cycle_config.json from Content/Python. Returns None if missing or invalid."""
    path = os.path.join(project_root, "Content", "Python", "automation_cycle_config.json")
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def get_scripts_for_task(project_root: str, task_index: int) -> Optional[list]:
    """Return list of script names for task from config, or None if task is 'mcp' or not in config."""
    config = load_cycle_config(project_root)
    if not config:
        return None
    tasks = config.get("tasks") or {}
    val = tasks.get(str(task_index))
    if val == "mcp":
        return None
    if isinstance(val, list):
        return val
    return None


def run_ue_automation(project_root: str) -> tuple[bool, int, int]:
    """Run run_ue_automation.py; return (success, passed, failed)."""
    script = os.path.join(project_root, "Content", "Python", "run_ue_automation.py")
    if not os.path.isfile(script):
        _log("run_ue_automation: script not found")
        return False, 0, 0
    try:
        proc = subprocess.run(
            [sys.executable, script, "--group", "Smoke"],
            cwd=project_root,
            timeout=700,
            capture_output=True,
            text=True,
        )
    except (subprocess.TimeoutExpired, OSError) as e:
        _log("run_ue_automation failed", {"error": str(e)})
        return False, 0, 0
    result_path = os.path.join(project_root, "Saved", "automation_run_result.json")
    passed = failed = 0
    if os.path.isfile(result_path):
        try:
            with open(result_path, encoding="utf-8") as f:
                data = json.load(f)
            passed = int(data.get("passed", 0))
            failed = int(data.get("failed", 0))
        except (json.JSONDecodeError, OSError):
            pass
    success = proc.returncode == 0 and failed == 0
    _log("run_ue_automation done", {"success": success, "passed": passed, "failed": failed})
    return success, passed, failed


def update_cycle_state(project_root: str, task_index: int, outcome: str) -> None:
    """Update docs/workflow/CYCLE_STATE.md: current_task_index, last_outcome, retry_count."""
    path = os.path.join(project_root, "docs", "workflow", "CYCLE_STATE.md")
    if not os.path.isfile(path):
        return
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return
    lines = content.split("\n")
    new_lines = []
    for line in lines:
        if line.strip().startswith("- **current_task_index:**"):
            new_lines.append(f"- **current_task_index:** {task_index + 1}")
        elif line.strip().startswith("- **last_outcome:**"):
            new_lines.append(f"- **last_outcome:** {outcome}")
        elif line.strip().startswith("- **retry_count:**"):
            new_lines.append("- **retry_count:** 0")
        else:
            new_lines.append(line)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines))
        _log("updated CYCLE_STATE", {"current_task_index": task_index + 1, "last_outcome": outcome})
    except OSError:
        pass


EDITOR_EXIT_WAIT_TIMEOUT = 90
EDITOR_EXIT_POLL_INTERVAL = 2


def wait_for_editor_exit(timeout: float = EDITOR_EXIT_WAIT_TIMEOUT) -> bool:
    """Poll until UnrealEditor.exe is not running or timeout. Returns True if Editor exited."""
    deadline = time.perf_counter() + timeout
    while time.perf_counter() < deadline:
        if not is_editor_running():
            _log("editor_exit: Editor process gone")
            return True
        time.sleep(min(EDITOR_EXIT_POLL_INTERVAL, max(0, deadline - time.perf_counter())))
    _log("editor_exit: timeout", {"timeout": timeout})
    return False


def close_editor_gracefully() -> bool:
    """Send graceful close to UnrealEditor (taskkill without /f). Returns True if no error."""
    if not is_editor_running():
        _log("close_editor: Editor not running")
        return True
    _log("close_editor: sending taskkill (graceful)")
    try:
        subprocess.run(
            ["taskkill", "/im", "UnrealEditor.exe"],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (subprocess.TimeoutExpired, OSError) as e:
        _log("close_editor failed", {"error": str(e)})
        return False
    return True


def force_close_editor() -> bool:
    """Force-kill UnrealEditor (taskkill /f). Use after graceful close failed or build failed due to Editor."""
    if not is_editor_running():
        _log("force_close_editor: Editor not running")
        return True
    _log("force_close_editor: sending taskkill /f")
    try:
        subprocess.run(
            ["taskkill", "/f", "/im", "UnrealEditor.exe"],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (subprocess.TimeoutExpired, OSError) as e:
        _log("force_close_editor failed", {"error": str(e)})
        return False
    return True


def build_failure_likely_editor_related(log_path: str) -> bool:
    """Return True if Build-HomeWorld.log suggests failure was due to Editor (Live Coding / locked)."""
    if not os.path.isfile(log_path):
        return False
    try:
        with open(log_path, encoding="utf-8", errors="replace") as f:
            content = f.read()
    except OSError:
        return False
    content_lower = content.lower()
    if "exit code: 6" in content_lower or "exit code: 6 " in content:
        return True
    if "live coding" in content_lower or "unable to build while" in content_lower:
        return True
    if "editor" in content_lower and ("lock" in content_lower or "in use" in content_lower):
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Orchestrate build, Editor lifecycle, and optional tests")
    parser.add_argument("--task", type=int, default=None, help="Task index (1-based); for future cycle integration")
    parser.add_argument("--no-build", action="store_true", help="Skip build step")
    parser.add_argument(
        "--editor-mode",
        choices=("headless", "mcp"),
        default="mcp",
        help="headless: run scripts then exit; mcp: launch Editor and wait for port 55557",
    )
    parser.add_argument("--close-editor", action="store_true", help="If Editor is running, send graceful close (taskkill)")
    parser.add_argument("--launch-and-wait", action="store_true", help="Launch Editor and wait for port 55557 then exit (writes Saved/cycle_editor_ready.json)")
    parser.add_argument("--scripts", nargs="*", default=None, help="Run these Content/Python scripts headless (-ExecutePythonScript each); Editor starts and exits per script")
    args = parser.parse_args()

    _log("started", {"no_build": args.no_build, "editor_mode": args.editor_mode, "task": args.task})

    ue_editor, project_root, uproject = _resolve_editor_and_project()
    if not project_root:
        _log("abort: no project root")
        return 1

    scripts = args.scripts
    if args.task is not None and scripts is None:
        scripts = get_scripts_for_task(project_root, args.task)

    saved_dir = os.path.join(project_root, "Saved")
    os.makedirs(saved_dir, exist_ok=True)

    if args.close_editor:
        close_editor_gracefully()
        _log("close_editor done")
        return 0

    if not args.no_build:
        # Editor–build protocol: close Editor if running, then build; on Editor-related failure, force-close and retry once
        if is_editor_running():
            _log("build: Editor running; closing gracefully before build")
            close_editor_gracefully()
            if not wait_for_editor_exit():
                _log("abort: Editor did not exit in time")
                return 1
        ok, err = run_build(project_root)
        if not ok:
            log_path = os.path.join(project_root, "Build-HomeWorld.log")
            if build_failure_likely_editor_related(log_path):
                _log("build: failure likely Editor-related; force-closing and retrying build once")
                force_close_editor()
                if not wait_for_editor_exit():
                    _log("abort: Editor did not exit after force-close")
                    return 1
                ok, err = run_build(project_root)
            if not ok:
                _log("abort: build failed", {"error": err})
                return 1

    if scripts:
        if not ue_editor or not uproject:
            _log("abort: UE_EDITOR or uproject missing; cannot run headless scripts")
            return 1
        for script_rel in scripts:
            ok, err = run_headless_script(ue_editor, uproject, project_root, script_rel)
            if not ok:
                _log("abort: headless script failed", {"script": script_rel, "error": err})
                return 1
        _log("headless scripts completed", {"count": len(scripts)})

    build_ok = args.no_build or not args.no_build
    scripts_ok = True
    tests_ok = True
    tests_passed = tests_failed = 0

    if args.task is not None:
        tests_ok, tests_passed, tests_failed = run_ue_automation(project_root)
        cycle_result = {
            "task": args.task,
            "build_ok": build_ok,
            "scripts_ok": scripts_ok,
            "tests_ok": tests_ok,
            "tests_passed": tests_passed,
            "tests_failed": tests_failed,
        }
        cycle_result_path = os.path.join(saved_dir, "cycle_run_result.json")
        with open(cycle_result_path, "w", encoding="utf-8") as f:
            json.dump(cycle_result, f, indent=2)
        outcome = "pass" if tests_ok else "fail"
        update_cycle_state(project_root, args.task, outcome)
        _log("completed", {"task": args.task, "tests_ok": tests_ok})
        return 0 if tests_ok else 1

    if args.launch_and_wait:
        if not ue_editor or not uproject:
            _log("abort: UE_EDITOR or uproject missing; cannot launch Editor")
            return 1
        if is_editor_running():
            _log("Editor already running; waiting for port")
        else:
            p = launch_editor(ue_editor, uproject, project_root)
            if p is None:
                return 1
        if not wait_for_port(MCP_PORT, PORT_WAIT_TIMEOUT):
            _log("abort: Editor port not ready")
            return 1
        ready_path = os.path.join(saved_dir, "cycle_editor_ready.json")
        with open(ready_path, "w", encoding="utf-8") as f:
            json.dump({"ready": True, "port": MCP_PORT}, f, indent=2)
        _log("Editor ready; wrote cycle_editor_ready.json")
        return 0

    _log("completed", {"task": args.task})
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Open the interactive Editor and wait until MCP answers on 55557.

Idempotent: if the Editor is already up it reports readiness and does nothing,
if it is up but MCP is not ready it waits rather than starting a second
instance, and only launches when nothing is running.

Why this exists
---------------
There was no owned way to bring the Editor up. ``Safe-Build.ps1
-LaunchEditorAfter`` only relaunches an Editor *it* closed (line 139 gates on
``$editorWasRunning``), so with the Editor down it does nothing. The entry point
``docs/KNOWN_ERRORS.md`` told people to run, ``Start-AllAgents-InNewWindow.ps1``,
no longer exists anywhere in the repo. The result was that every session which
needed the Editor re-derived the launch by hand, or reported the Editor being
down as though it were a human's job.

The lock
--------
The engine version is read from ``.uproject`` ``EngineAssociation`` and never
from ``UE_EDITOR``. ``UE_EDITOR`` on this machine points at UE 5.7 against a
5.8 lock, and ``docs/KNOWN_ERRORS.md`` records a run that proceeded silently on
exactly that until 12 regression tests were added in 2026-10-03. Honouring the
environment variable when it *agrees* with the lock is fine; letting it become a
second source of truth is the failure that was already paid for once.

"Editor process exists" and "MCP answers" are deliberately separate. The Editor
can be alive and loading for a long time before the plugin listens, and work
started against a port that is not up yet fails in a way that reads like the
script's fault.
"""

from __future__ import annotations

import argparse
import os
import socket
import subprocess
import sys
import time
from typing import Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run_ue_automation import _engine_version_from_path, _locked_engine_version

MCP_PORT = 55557
EDITOR_PROCESS = "UnrealEditor.exe"


def canonical_editor_path(version: str) -> str:
    """The default install location for a given engine version."""
    return os.path.join(
        r"C:\Program Files\Epic Games",
        f"UE_{version}",
        "Engine",
        "Binaries",
        "Win64",
        "UnrealEditor.exe",
    )


def resolve_editor(uproject: str, override: Optional[str] = None) -> Tuple[Optional[str], str]:
    """Return ``(editor_path, detail)``. The project lock decides, not UE_EDITOR.

    Candidates are tried in order and a path naming the wrong engine is skipped,
    not fatal. This machine's ``UE_EDITOR`` points at 5.7 against a 5.8 lock, so
    a hard refusal would leave the tool unable to open the Editor at all even
    though a correct 5.8 install sits at the default location. The invariant that
    matters is narrower: a mismatched engine is never the one we launch. Skipping
    achieves that while still reporting what was skipped, which is what the
    original silent-5.7 run lacked.
    """
    lock = _locked_engine_version(uproject)
    if lock is None:
        return None, "could not read EngineAssociation from the .uproject; refusing to guess an engine"

    skipped = []
    candidates = [override, os.environ.get("UE_EDITOR"), canonical_editor_path(lock)]
    for candidate in candidates:
        if not candidate or not os.path.isfile(candidate):
            continue
        version = _engine_version_from_path(candidate)
        if version is not None and version != lock:
            skipped.append(f"{candidate} (UE {version})")
            continue
        detail = f"lock {lock}; using {candidate}"
        if skipped:
            detail += f" - skipped {', '.join(skipped)}"
        return candidate, detail

    message = f"lock is {lock} but no UnrealEditor.exe matching it was found"
    if skipped:
        message += f"; only {', '.join(skipped)} was found"
    return None, message


def mcp_listening(port: int = MCP_PORT) -> bool:
    """True when something is accepting connections on the MCP port."""
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1.0):
            return True
    except OSError:
        return False


def editor_running() -> bool:
    """True when an Editor process exists, whether or not MCP is ready.

    Needed to avoid launching a second instance into an already-loaded project,
    which is the case a port-only check cannot tell apart from "nothing running".
    """
    if os.name != "nt":
        return False
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"IMAGENAME eq {EDITOR_PROCESS}"],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return EDITOR_PROCESS.lower() in (result.stdout or "").lower()


def wait_for_mcp(
    timeout: float,
    port: int = MCP_PORT,
    poll: float = 3.0,
    alive: Optional[callable] = None,
) -> bool:
    """Poll until MCP listens, giving up on timeout or if the Editor exits.

    Checking that the process is still there matters: a launch that dies during
    loading would otherwise spin out the full timeout and report a slow failure
    instead of the real one.
    """
    is_alive = alive if alive is not None else editor_running
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if mcp_listening(port):
            return True
        if not is_alive():
            return False
        time.sleep(poll)
    return mcp_listening(port)


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--uproject", default=None, help="Path to the .uproject")
    parser.add_argument("--editor", default=None, help="Editor binary override (must match the lock)")
    parser.add_argument("--timeout", type=int, default=300, help="Seconds to wait for MCP (default: 300)")
    args = parser.parse_args(argv)

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    uproject = args.uproject or os.path.join(project_root, "HomeWorld.uproject")
    if not os.path.isfile(uproject):
        print(f"no project at {uproject}")
        return 1

    if mcp_listening():
        print(f"MCP already listening on {MCP_PORT}; nothing to do")
        return 0

    editor, detail = resolve_editor(uproject, args.editor)
    if editor is None:
        print(f"cannot launch: {detail}")
        return 1

    if editor_running():
        print(f"Editor running but MCP not ready on {MCP_PORT}; waiting ({detail})")
        if wait_for_mcp(args.timeout):
            print(f"MCP listening on {MCP_PORT}")
            return 0
        print(f"MCP did not open within {args.timeout}s while the Editor was running")
        return 1

    print(f"launching {editor}")
    try:
        process = subprocess.Popen([editor, uproject], cwd=os.path.dirname(uproject))
    except OSError as exc:
        print(f"launch failed: {exc}")
        return 1

    # Track the handle we just opened, not tasklist. On the first poll the new
    # process may not be listed yet, and editor_running() would then read a
    # starting Editor as one that had died - the slow, misattributed failure this
    # tool exists to remove.
    if wait_for_mcp(args.timeout, alive=lambda: process.poll() is None):
        print(f"MCP listening on {MCP_PORT}")
        return 0
    print(f"MCP did not open within {args.timeout}s ({detail})")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

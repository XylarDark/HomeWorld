# test_start_editor.py
# Guards the silent-failure paths in start_editor.py.
#
# Each test below is a way the script could report readiness it did not earn, or
# refuse the work it exists to do. They use ports they allocate themselves: the
# real MCP port is occupied whenever the Editor is up, so a test bound to it
# would pass for the wrong reason and fail whenever the Editor is closed.

import json
import os
import socket
import sys
import time

_script_dir = os.path.dirname(os.path.abspath(__file__))
_content_python = os.path.normpath(os.path.join(_script_dir, ".."))
if _content_python not in sys.path:
    sys.path.insert(0, _content_python)

import start_editor

LOCKED = "5.8"
STALE = "5.7"


def _uproject(dirpath, association=LOCKED):
    path = os.path.join(dirpath, "HomeWorld.uproject")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"FileVersion": 3, "EngineAssociation": association}, handle)
    return path


def _fake_editor(root, version):
    """An empty file at a path whose version is readable, so resolve_editor can judge it."""
    path = os.path.join(root, f"UE_{version}", "Engine", "Binaries", "Win64", "UnrealEditor.exe")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("not a real editor")
    return path


def _free_port():
    """A port with nothing on it, so these tests never depend on Editor state."""
    probe = socket.socket()
    probe.bind(("127.0.0.1", 0))
    port = probe.getsockname()[1]
    probe.close()
    return port


def test_stale_env_var_does_not_block_the_locked_engine(tmp_path, monkeypatch):
    """UE_EDITOR on 5.7 must not stop the 5.8 editor from being chosen.

    This machine's UE_EDITOR points at UE 5.7 against a 5.8 lock. The first
    version of resolve_editor hard-refused on the first mismatch, which meant the
    one tool built to open the Editor refused to open it. Refusing to launch the
    wrong engine is the guarantee; refusing to launch at all was the bug.
    """
    stale = _fake_editor(str(tmp_path), STALE)
    correct = _fake_editor(str(tmp_path), LOCKED)
    monkeypatch.setenv("UE_EDITOR", stale)
    monkeypatch.setattr(start_editor, "canonical_editor_path", lambda _v: correct)

    found, detail = start_editor.resolve_editor(_uproject(str(tmp_path)))

    assert found == correct, "the locked engine must be chosen over the stale env var"
    assert STALE in detail, "what was skipped has to be reported, not swallowed"
    assert LOCKED in detail


def test_a_mismatched_engine_is_never_the_one_launched(tmp_path, monkeypatch):
    """An explicit override naming the wrong engine is skipped, not used.

    canonical_editor_path is patched out: without it this test passes in CI (no
    engine installed) and fails on any dev box that does have one, which is the
    shape of test people learn to ignore.
    """
    wrong = _fake_editor(str(tmp_path), STALE)
    right = _fake_editor(str(tmp_path), LOCKED)
    absent = os.path.join(str(tmp_path), "absent")
    monkeypatch.delenv("UE_EDITOR", raising=False)
    monkeypatch.setattr(start_editor, "canonical_editor_path", lambda _v: absent)

    found, detail = start_editor.resolve_editor(_uproject(str(tmp_path)), override=wrong)
    assert found is None, "a wrong override must not be selected when nothing else matches"
    assert wrong in detail, "the refusal must still say what it turned down"

    monkeypatch.setenv("UE_EDITOR", right)
    found, detail = start_editor.resolve_editor(_uproject(str(tmp_path)), override=wrong)
    assert found == right, "the first candidate that agrees with the lock wins"
    assert wrong in detail


def test_no_matching_engine_says_what_it_did_find(tmp_path, monkeypatch):
    """Failure must name the version found and the version locked, or the next reader guesses."""
    only_stale = _fake_editor(str(tmp_path), STALE)
    monkeypatch.setenv("UE_EDITOR", only_stale)
    monkeypatch.setattr(start_editor, "canonical_editor_path", lambda _v: os.path.join(str(tmp_path), "absent"))

    found, detail = start_editor.resolve_editor(_uproject(str(tmp_path)))

    assert found is None
    assert STALE in detail and LOCKED in detail, "both versions must appear in the refusal"


def test_unreadable_lock_refuses_to_guess(tmp_path, monkeypatch):
    """No EngineAssociation means no basis for choosing an engine, so no launch."""
    path = os.path.join(str(tmp_path), "HomeWorld.uproject")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"FileVersion": 3}, handle)
    monkeypatch.delenv("UE_EDITOR", raising=False)

    found, detail = start_editor.resolve_editor(path)
    assert found is None
    assert "EngineAssociation" in detail


def test_a_path_with_no_version_is_not_treated_as_wrong(tmp_path, monkeypatch):
    """Absence of evidence is not a mismatch - matches _check_engine_match in the runner.

    Some installs live outside the Epic Games tree and name no version. Skipping
    those would make the tool useless on a perfectly valid machine.
    """
    unversioned = os.path.join(str(tmp_path), "Engine", "Binaries", "Win64", "UnrealEditor.exe")
    os.makedirs(os.path.dirname(unversioned), exist_ok=True)
    with open(unversioned, "w", encoding="utf-8") as handle:
        handle.write("x")
    monkeypatch.setenv("UE_EDITOR", unversioned)
    monkeypatch.setattr(start_editor, "canonical_editor_path", lambda _v: os.path.join(str(tmp_path), "absent"))

    found, _detail = start_editor.resolve_editor(_uproject(str(tmp_path)))
    assert found == unversioned


def test_mcp_listening_measures_a_socket_that_is_there():
    """Positive case must come from a real listener, or the check is decorative."""
    port = _free_port()
    listener = socket.socket()
    try:
        listener.bind(("127.0.0.1", port))
        listener.listen(1)
        assert start_editor.mcp_listening(port) is True
    finally:
        listener.close()


def test_mcp_listening_reports_silence_as_silence():
    port = _free_port()
    assert start_editor.mcp_listening(port) is False


def test_wait_gives_up_when_the_editor_has_died():
    """A launch that dies while loading must fail fast, not burn the full timeout.

    Burning the timeout hides the real cause behind a slow one, and the log then
    reads as a networking problem when the Editor never opened.
    """
    port = _free_port()
    started = time.monotonic()
    result = start_editor.wait_for_mcp(timeout=60, port=port, poll=0.01, alive=lambda: False)
    elapsed = time.monotonic() - started

    assert result is False
    assert elapsed < 5, f"took {elapsed:.1f}s to notice the process was gone"


def test_wait_returns_as_soon_as_mcp_answers():
    port = _free_port()
    listener = socket.socket()
    try:
        listener.bind(("127.0.0.1", port))
        listener.listen(1)
        result = start_editor.wait_for_mcp(timeout=5, port=port, poll=0.01, alive=lambda: True)
    finally:
        listener.close()
    assert result is True


def test_already_ready_short_circuits_without_launching(monkeypatch):
    """The idempotency guarantee: ready means no process is started at all.

    Relaunching an Editor that is already up is the failure that costs a session -
    two instances on one project, and a confusing save conflict to follow.
    """
    class _NoLaunch:
        def Popen(self, *args, **kwargs):
            raise AssertionError("launched an Editor that was already ready")

    monkeypatch.setattr(start_editor, "mcp_listening", lambda *a, **k: True)
    monkeypatch.setattr(start_editor, "subprocess", _NoLaunch())

    # argv=[] rather than None: under pytest, None would make argparse read the
    # runner's own argv and exit 2 before any of this logic ran.
    assert start_editor.main(argv=[]) == 0


def test_launch_tracks_the_process_handle_not_tasklist(tmp_path, monkeypatch):
    """After launching, liveness must come from the handle we opened.

    editor_running() shells out to tasklist. On the first poll the just-started
    process may not be listed yet, so using it would report "MCP did not open"
    for an Editor that is starting normally. The handle knows better, so main
    must judge liveness from the Popen object it just got.
    """
    editor = _fake_editor(str(tmp_path), LOCKED)
    monkeypatch.setattr(start_editor, "canonical_editor_path", lambda _v: editor)
    monkeypatch.delenv("UE_EDITOR", raising=False)
    monkeypatch.setattr(start_editor, "mcp_listening", lambda *a, **k: False)
    monkeypatch.setattr(start_editor, "editor_running", lambda: False)

    class _Process:
        alive = True

        def poll(self):
            return None if self.alive else 1

    process = _Process()

    class _Subprocess:
        @staticmethod
        def Popen(*args, **kwargs):
            return process

    monkeypatch.setattr(start_editor, "subprocess", _Subprocess)

    seen = {}

    def _wait(timeout, port=start_editor.MCP_PORT, poll=3.0, alive=None):
        seen["alive"] = alive
        return alive()

    monkeypatch.setattr(start_editor, "wait_for_mcp", _wait)

    assert start_editor.main(argv=["--uproject", _uproject(str(tmp_path))]) == 0
    assert seen["alive"]() is True, "a live handle must read as alive"
    process.alive = False
    assert seen["alive"]() is False, "an exited handle must read as dead"

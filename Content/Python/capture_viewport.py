# capture_viewport.py
# Captures a viewport screenshot and saves it to Saved/Screenshots/.
# Callable via MCP execute_python_script("capture_viewport.py").
# Result metadata written to Saved/screenshot_result.json.
#
# Console HighResShot first (Epic doc order: filename= then resolution);
# AutomationLibrary fallback if no PNG on disk.
# https://dev.epicgames.com/documentation/en-us/unreal-engine/taking-screenshots-in-unreal-engine
# See capture_shotlist.py (MRQ primary) / capture_shotlist_viewport.py / CAPTURE_REDUNDANCY.md.
# Harness P3 exempt: generic viewport still utility — not shotlist prove; no Arrange gate.

import json
import os
import sys
import time
from typing import Optional

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

WAIT_FILE_SEC = 120.0
MIN_BYTES = 1024
CAPTURE_DELAY_SEC = 0.35
POST_CONSOLE_SETTLE_FRAMES = 8
SLATE_WAIT_MECHANISM = "register_slate_pre_tick_callback"
# Blocking file wait cap for generic capture(); PS-C uses slate driver (no main-thread sleep).
WAIT_FILE_SEC_LEGACY = 330.0


def _abs_project_dir():
    raw = unreal.Paths.project_dir()
    return os.path.abspath(raw) if raw else os.path.abspath(os.getcwd())


def _output_dir():
    out = os.path.join(_abs_project_dir(), "Saved", "Screenshots")
    os.makedirs(out, exist_ok=True)
    return out


def _screenshot_search_roots():
    roots = [_output_dir()]
    screens = os.path.join(_abs_project_dir(), "Saved", "Screenshots")
    for sub in ("WindowsEditor", "Windows", "PA_E"):
        p = os.path.join(screens, sub)
        if os.path.isdir(p):
            roots.append(p)
    try:
        eng = unreal.Paths.engine_dir()
        if eng:
            win64 = os.path.join(eng, "Binaries", "Win64")
            if os.path.isdir(win64):
                roots.append(win64)
    except Exception:
        pass
    return roots


def _path_for_ue(abs_path):
    return os.path.abspath(abs_path).replace("\\", "/")


def _pump_editor_once():
    try:
        if hasattr(unreal.AutomationLibrary, "automation_wait_for_loading"):
            unreal.AutomationLibrary.automation_wait_for_loading(None, 0.05)
    except Exception:
        pass
    try:
        app = unreal.SlateApplication.get()
        if app is not None and hasattr(app, "tick"):
            app.tick(0.033)
    except Exception:
        pass


def _settle_pump_only(frames=POST_CONSOLE_SETTLE_FRAMES):
    """Advance Slate/editor without time.sleep (safe on MCP main thread between invokes)."""
    for _ in range(max(1, frames)):
        _pump_editor_once()


def _settle(frames=POST_CONSOLE_SETTLE_FRAMES):
    _settle_pump_only(frames)


def _finish_loading_before_screenshot():
    try:
        fn = getattr(unreal.AutomationLibrary, "finish_loading_before_screenshot", None)
        if callable(fn):
            fn()
            return True
    except Exception:
        pass
    return False


def _set_lit_view_mode():
    try:
        set_vm = getattr(unreal.AutomationLibrary, "set_editor_viewport_view_mode", None)
        if callable(set_vm):
            mode = getattr(unreal, "ViewModeIndex", None)
            if mode is not None and hasattr(mode, "VMI_LIT"):
                set_vm(mode.VMI_LIT)
                return "AutomationLibrary.set_editor_viewport_view_mode(VMI_LIT)"
            set_vm("Lit")
            return "AutomationLibrary.set_editor_viewport_view_mode(Lit)"
    except Exception:
        pass
    try:
        unreal.SystemLibrary.execute_console_command(None, "viewmode lit")
        return "console_viewmode_lit"
    except Exception:
        return None


def _high_res_shot_commands(resolution_x, resolution_y, ue_path):
    return (
        (
            "ConsoleCommand_filename_res_quoted",
            'HighResShot filename="%s" %dx%d' % (ue_path, resolution_x, resolution_y),
        ),
        (
            "ConsoleCommand_filename_res",
            "HighResShot filename=%s %dx%d" % (ue_path, resolution_x, resolution_y),
        ),
        ("ConsoleCommand_filename_only_quoted", 'HighResShot filename="%s"' % ue_path),
        ("ConsoleCommand_filename_only", "HighResShot filename=%s" % ue_path),
        (
            "ConsoleCommand_res_filename_legacy",
            'HighResShot %dx%d filename="%s"' % (resolution_x, resolution_y, ue_path),
        ),
    )


class _StableSizeTracker:
    """Tick-based PNG size stability (no sleep between polls)."""

    __slots__ = ("last_size", "same_count")

    def __init__(self) -> None:
        self.last_size = -1
        self.same_count = 0

    def reset(self) -> None:
        self.last_size = -1
        self.same_count = 0

    def observe(self, path: str) -> bool:
        if not os.path.isfile(path):
            self.reset()
            return False
        try:
            size = os.path.getsize(path)
        except OSError:
            self.reset()
            return False
        if size == self.last_size:
            self.same_count += 1
        else:
            self.last_size = size
            self.same_count = 1
        return self.same_count >= 2 and size >= MIN_BYTES


def _mtime_at_least(path: str, since_mtime: float) -> bool:
    try:
        return os.path.getmtime(path) >= since_mtime - 0.05
    except OSError:
        return False


def _copy_candidate_to_dest(candidate: str, filepath: str) -> bool:
    if candidate == filepath:
        return os.path.isfile(filepath)
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        import shutil

        shutil.copy2(candidate, filepath)
        return os.path.isfile(filepath)
    except OSError:
        return False


def probe_png_ready(
    filepath: str,
    since_mtime: float,
    basename: str,
    stable: Optional["_StableSizeTracker"] = None,
) -> Optional[str]:
    """Single-tick probe for fresh PNG (PS-C / slate drivers)."""
    if (
        os.path.isfile(filepath)
        and os.path.getsize(filepath) >= MIN_BYTES
        and _mtime_at_least(filepath, since_mtime)
    ):
        if stable is None or stable.observe(filepath):
            return filepath
    for root in _screenshot_search_roots():
        candidate = os.path.join(root, basename)
        if (
            os.path.isfile(candidate)
            and os.path.getsize(candidate) >= MIN_BYTES
            and _mtime_at_least(candidate, since_mtime)
        ):
            if _copy_candidate_to_dest(candidate, filepath):
                check = filepath if os.path.isfile(filepath) else candidate
                if stable is None or stable.observe(check):
                    return check
    return None


def _wait_for_file(filepath, since_mtime, basename, wait_sec=None):
    deadline = time.time() + (wait_sec if wait_sec is not None else WAIT_FILE_SEC_LEGACY)
    stable = _StableSizeTracker()
    while time.time() < deadline:
        found = probe_png_ready(filepath, since_mtime, basename, stable)
        if found:
            return found
        _settle_pump_only(frames=2)
    return None


def console_high_res_invoke_once(resolution_x, resolution_y, filepath, result, world=None):
    """Fire doc-ordered HighResShot once (no file wait — use slate tick probe)."""
    ue_path = _path_for_ue(filepath)
    result["ue_path"] = ue_path
    result["console_attempts"] = []
    _finish_loading_before_screenshot()
    _set_lit_view_mode()
    world_context = world
    for method, cmd in _high_res_shot_commands(resolution_x, resolution_y, ue_path):
        entry = {"method": method, "cmd": cmd}
        result["console_attempts"].append(entry)
        try:
            unreal.SystemLibrary.execute_console_command(world_context, cmd)
            result["method"] = method
            return True
        except Exception as e:
            entry["error"] = str(e)
            continue
    return False


def _console_high_res(resolution_x, resolution_y, filepath, result):
    """Try doc-ordered HighResShot forms; wait for PNG before next command."""
    ue_path = _path_for_ue(filepath)
    basename = os.path.basename(filepath)
    result["ue_path"] = ue_path
    result["console_attempts"] = []
    _finish_loading_before_screenshot()
    _set_lit_view_mode()
    for method, cmd in _high_res_shot_commands(resolution_x, resolution_y, ue_path):
        attempt_since = time.time()
        entry = {"method": method, "cmd": cmd}
        result["console_attempts"].append(entry)
        try:
            unreal.SystemLibrary.execute_console_command(None, cmd)
        except Exception as e:
            entry["error"] = str(e)
            continue
        _settle()
        found = _wait_for_file(filepath, attempt_since, basename)
        if found:
            result["method"] = method
            return True
    return False


def _take_high_res_automation_fallback(resolution_x, resolution_y, filepath, result):
    """Fallback: AutomationLibrary when console HighResShot did not write a PNG."""
    if not hasattr(unreal, "AutomationLibrary"):
        return False
    ue_path = _path_for_ue(filepath)
    basename = os.path.basename(filepath)
    _finish_loading_before_screenshot()
    delay = CAPTURE_DELAY_SEC
    attempts = (
        (
            "AutomationLibrary_delay_force_gv_kw",
            lambda: unreal.AutomationLibrary.take_high_res_screenshot(
                resolution_x,
                resolution_y,
                ue_path,
                camera=None,
                delay=delay,
                force_game_view=True,
            ),
        ),
        (
            "AutomationLibrary_force_game_view_kw",
            lambda: unreal.AutomationLibrary.take_high_res_screenshot(
                resolution_x, resolution_y, ue_path, camera=None, force_game_view=True
            ),
        ),
        (
            "AutomationLibrary_force_game_view_pos",
            lambda: unreal.AutomationLibrary.take_high_res_screenshot(
                resolution_x, resolution_y, ue_path, None, True
            ),
        ),
        (
            "AutomationLibrary",
            lambda: unreal.AutomationLibrary.take_high_res_screenshot(
                resolution_x, resolution_y, ue_path
            ),
        ),
    )
    for method, fn in attempts:
        fallback_since = time.time()
        try:
            task = fn()
            result["automation_task_type"] = type(task).__name__ if task else None
            result["method"] = method
            result["used_automation_fallback"] = True
            _settle()
            if _wait_for_file(filepath, fallback_since, basename):
                return True
        except TypeError:
            continue
        except Exception as e:
            result.setdefault("automation_errors", []).append({method: str(e)})
    return False


def capture(filename=None, resolution_x=1920, resolution_y=1080):
    """Capture viewport screenshot. Returns path to saved file."""
    out_dir = _output_dir()
    if not filename:
        filename = "viewport_%s.png" % time.strftime("%Y%m%d_%H%M%S")
    filepath = os.path.abspath(os.path.join(out_dir, filename))
    basename = os.path.basename(filepath)

    result = {
        "requested": filepath,
        "captured": False,
        "async_note": "wait_for_png_on_disk",
        "wait_file_sec": WAIT_FILE_SEC,
    }

    if _console_high_res(resolution_x, resolution_y, filepath, result):
        result["captured"] = True
        result["path"] = filepath
        result["file_produced_by"] = result.get("method")
        _write_result(result)
        return filepath

    if _take_high_res_automation_fallback(resolution_x, resolution_y, filepath, result):
        result["captured"] = True
        result["path"] = filepath
        result["file_produced_by"] = result.get("method")
        _write_result(result)
        return filepath

    since = time.time()
    try:
        if hasattr(unreal, "ScreenshotTools"):
            unreal.ScreenshotTools.request_screenshot(basename, False)
            result["method"] = "ScreenshotTools"
            if _wait_for_file(filepath, since, basename):
                result["captured"] = True
                result["path"] = filepath
                _write_result(result)
                return filepath
    except Exception as e:
        result["screenshot_tools_error"] = str(e)

    result["error"] = "Console + AutomationLibrary failed or async file never appeared"
    _write_result(result)
    return None


def _write_result(data):
    path = os.path.join(_abs_project_dir(), "Saved", "screenshot_result.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def main():
    capture()


if __name__ == "__main__":
    main()

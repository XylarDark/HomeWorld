# capture_viewport.py
# Captures a viewport screenshot and saves it to Saved/Screenshots/.
# Callable via MCP execute_python_script("capture_viewport.py").
# Result metadata written to Saved/screenshot_result.json.
#
# take_high_res_screenshot is asynchronous — wait for the PNG on disk before
# treating capture as success (see capture_shotlist_viewport.py / CAPTURE_REDUNDANCY.md).

import json
import os
import sys
import time

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

WAIT_FILE_SEC = 30.0
MIN_BYTES = 1024


def _output_dir():
    proj = unreal.Paths.project_dir()
    out = os.path.join(proj, "Saved", "Screenshots")
    os.makedirs(out, exist_ok=True)
    return out


def _take_high_res(resolution_x, resolution_y, filename, result):
    """AutomationLibrary with force_game_view when the UE build supports it."""
    if not hasattr(unreal, "AutomationLibrary"):
        return False
    attempts = (
        ("AutomationLibrary_force_game_view_kw", lambda: unreal.AutomationLibrary.take_high_res_screenshot(
            resolution_x, resolution_y, filename, camera=None, force_game_view=True
        )),
        ("AutomationLibrary_force_game_view_pos", lambda: unreal.AutomationLibrary.take_high_res_screenshot(
            resolution_x, resolution_y, filename, None, True
        )),
        ("AutomationLibrary", lambda: unreal.AutomationLibrary.take_high_res_screenshot(
            resolution_x, resolution_y, filename
        )),
    )
    for method, fn in attempts:
        try:
            fn()
            result["method"] = method
            return True
        except TypeError:
            continue
        except Exception as e:
            result.setdefault("automation_errors", []).append({method: str(e)})
    return False


def _wait_for_file(filepath, since_mtime):
    deadline = time.time() + WAIT_FILE_SEC
    while time.time() < deadline:
        if os.path.isfile(filepath) and os.path.getsize(filepath) >= MIN_BYTES:
            if os.path.getmtime(filepath) >= since_mtime:
                return True
        time.sleep(0.2)
    return os.path.isfile(filepath) and os.path.getsize(filepath) >= MIN_BYTES


def capture(filename=None, resolution_x=1920, resolution_y=1080):
    """Capture viewport screenshot. Returns path to saved file."""
    out_dir = _output_dir()
    if not filename:
        filename = "viewport_%s.png" % time.strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(out_dir, filename)

    result = {"requested": filepath, "captured": False, "async_note": "wait_for_png_on_disk"}

    since = time.time()
    if _take_high_res(resolution_x, resolution_y, filename, result):
        if _wait_for_file(filepath, since):
            result["captured"] = True
            result["path"] = filepath
            _write_result(result)
            return filepath
        result["error"] = "AutomationLibrary invoked but PNG missing or too small after wait"
        _write_result(result)
        return None

    # Method 2: Console command
    try:
        cmd = "HighResShot %dx%d filename=\"%s\"" % (
            resolution_x,
            resolution_y,
            filepath.replace("\\", "/"),
        )
        unreal.SystemLibrary.execute_console_command(None, cmd)
        result["method"] = "ConsoleCommand"
        if _wait_for_file(filepath, since):
            result["captured"] = True
            result["path"] = filepath
            _write_result(result)
            return filepath
    except Exception as e:
        result["method2_error"] = str(e)

    # Method 3: ScreenshotTools if available
    try:
        if hasattr(unreal, "ScreenshotTools"):
            unreal.ScreenshotTools.request_screenshot(filename, False)
            result["method"] = "ScreenshotTools"
            if _wait_for_file(filepath, since):
                result["captured"] = True
                result["path"] = filepath
                _write_result(result)
                return filepath
    except Exception as e:
        result["method3_error"] = str(e)

    result["error"] = "All screenshot methods failed or async file never appeared"
    _write_result(result)
    return None


def _write_result(data):
    proj = unreal.Paths.project_dir()
    path = os.path.join(proj, "Saved", "screenshot_result.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def main():
    capture()


if __name__ == "__main__":
    main()

# capture_viewport.py
# Captures a viewport screenshot and saves it to Saved/Screenshots/.
# Callable via MCP execute_python_script("capture_viewport.py").
# Result metadata written to Saved/screenshot_result.json.

import json
import os
import sys
import time

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)


def _output_dir():
    proj = unreal.Paths.project_dir()
    out = os.path.join(proj, "Saved", "Screenshots")
    os.makedirs(out, exist_ok=True)
    return out


def capture(filename=None, resolution_x=1920, resolution_y=1080):
    """Capture viewport screenshot. Returns path to saved file."""
    out_dir = _output_dir()
    if not filename:
        filename = "viewport_%s.png" % time.strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(out_dir, filename)

    result = {"requested": filepath, "captured": False}

    # Method 1: AutomationLibrary high-res screenshot
    try:
        if hasattr(unreal, "AutomationLibrary"):
            unreal.AutomationLibrary.take_high_res_screenshot(
                resolution_x, resolution_y, filename
            )
            result["method"] = "AutomationLibrary"
            result["captured"] = True
            result["path"] = filepath
            _write_result(result)
            return filepath
    except Exception as e:
        result["method1_error"] = str(e)

    # Method 2: Console command
    try:
        cmd = "HighResShot 1920x1080 filename=\"%s\"" % filepath.replace("\\", "/")
        unreal.SystemLibrary.execute_console_command(None, cmd)
        result["method"] = "ConsoleCommand"
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
            result["captured"] = True
            result["path"] = filepath
            _write_result(result)
            return filepath
    except Exception as e:
        result["method3_error"] = str(e)

    result["error"] = "All screenshot methods failed"
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

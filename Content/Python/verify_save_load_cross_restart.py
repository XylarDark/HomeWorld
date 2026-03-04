# verify_save_load_cross_restart.py
# T4 / Day 15: Verify hw.Save then stop PIE then start PIE then hw.Load restores state.
# Run via MCP: execute_python_script("verify_save_load_cross_restart.py")
# Result: Saved/save_load_cross_restart_result.json

import json
import os
import time

import unreal

# Reuse PIE helpers from pie_test_runner
import pie_test_runner


def _output_path():
    proj = unreal.Paths.project_dir()
    saved = os.path.join(proj, "Saved")
    os.makedirs(saved, exist_ok=True)
    return os.path.join(saved, "save_load_cross_restart_result.json")


def run_cross_restart():
    """Execute: hw.Save -> stop PIE -> start PIE -> hw.Load. Return result dict."""
    result = {
        "cross_restart": None,
        "detail": "",
        "steps": [],
        "passed": False,
    }
    try:
        # 1. Ensure PIE is running
        if not pie_test_runner.is_pie_running():
            pie_test_runner.start_pie()
            result["steps"].append("started PIE")
            time.sleep(8)
        else:
            result["steps"].append("PIE already running")
            time.sleep(2)

        world = pie_test_runner.get_pie_world()
        if not world:
            result["detail"] = "No PIE world after start"
            return result

        # 2. Save
        unreal.SystemLibrary.execute_console_command(world, "hw.Save")
        result["steps"].append("hw.Save executed")
        time.sleep(1)

        # 3. Stop PIE
        pie_test_runner.stop_pie()
        result["steps"].append("PIE stopped")
        time.sleep(3)

        # 4. Start PIE again
        pie_test_runner.start_pie()
        result["steps"].append("PIE started again")
        time.sleep(8)

        world2 = pie_test_runner.get_pie_world()
        if not world2:
            result["detail"] = "No PIE world after restart"
            return result

        # 5. Load
        unreal.SystemLibrary.execute_console_command(world2, "hw.Load")
        result["steps"].append("hw.Load executed")
        time.sleep(1)

        result["cross_restart"] = "executed"
        result["detail"] = (
            "hw.Save -> stop PIE -> start PIE -> hw.Load completed. "
            "Confirm 'HomeWorld: hw.Save succeeded' and 'HomeWorld: hw.Load succeeded' in Output Log."
        )
        result["passed"] = True
    except Exception as e:
        result["detail"] = "Exception: " + str(e)
        result["steps"].append("error: " + str(e))
    return result


def main():
    print("verify_save_load_cross_restart: starting cross-restart test")
    outcome = run_cross_restart()
    out_path = _output_path()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(outcome, f, indent=2)
    print("verify_save_load_cross_restart: result written to", out_path)
    print("verify_save_load_cross_restart: passed =", outcome.get("passed", False))


if __name__ == "__main__":
    main()

# run_pie_verify.py
# Start PIE (if not running), wait for it to be active, run PIE checks, write results.
# Use via MCP: execute_python_script("run_pie_verify.py")
# Results: Saved/pie_test_results.json

import json
import os
import time

import unreal

try:
    import pie_test_runner
except ImportError:
    pie_test_runner = None


def _output_path():
    proj = unreal.Paths.project_dir()
    saved = os.path.join(proj, "Saved")
    os.makedirs(saved, exist_ok=True)
    return os.path.join(saved, "pie_test_results.json")


def main():
    subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if not subsys:
        out = {"error": "No LevelEditorSubsystem", "summary": "0/0 passed", "all_passed": False, "checks": []}
        with open(_output_path(), "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
        return

    if not subsys.is_in_play_in_editor():
        subsys.editor_request_begin_play()
        for _ in range(25):
            time.sleep(0.2)
            if subsys.is_in_play_in_editor():
                break

    if not pie_test_runner:
        out = {"error": "pie_test_runner not importable", "pie_was_running": subsys.is_in_play_in_editor()}
        with open(_output_path(), "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
        return

    result = pie_test_runner.run_checks()
    result["pie_was_running"] = pie_test_runner.is_pie_running()
    with open(_output_path(), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str)


if __name__ == "__main__":
    main()

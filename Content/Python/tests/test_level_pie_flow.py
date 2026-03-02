# test_level_pie_flow.py
# PythonAutomationTest: full flow — load DemoMap, wait ready, start PIE, run PIE checks, stop PIE.
# Optional; takes ~30–60 s. Run via Editor: Tools > Test Automation.
# Requires DemoMap and default game mode/pawn.

import json
import os
import sys

import unreal

# Content/Python for level_loader and pie_test_runner
_script_dir = os.path.dirname(os.path.abspath(__file__))
_content_python = os.path.normpath(os.path.join(_script_dir, ".."))
if _content_python not in sys.path:
    sys.path.insert(0, _content_python)
import level_loader
import pie_test_runner
import importlib
importlib.reload(level_loader)
importlib.reload(pie_test_runner)

DEMO_MAP_PATH = "/Game/HomeWorld/Maps/DemoMap"
LEVEL_WAIT_SEC = 30
PIE_YIELDS = 12
LATENT_TIMEOUT_SEC = 90


def test_demo_map_pie_full_flow():
    """Load DemoMap, wait for ready, start PIE, run pie_test_runner checks, stop PIE."""
    try:
        lib = getattr(unreal, "PyAutomationTestLibrary", None)
        if lib and hasattr(lib, "set_latent_command_timeout"):
            lib.set_latent_command_timeout(LATENT_TIMEOUT_SEC)
    except Exception:
        pass
    # 1) Load level and wait for ready
    gen = level_loader.latent_load_level_and_wait(
        DEMO_MAP_PATH, level_loader.landscape_has_bounds, LEVEL_WAIT_SEC
    )
    for _ in gen:
        yield
    # 2) Start PIE
    pie_test_runner.start_pie()
    for _ in range(PIE_YIELDS):
        yield
    # 3) Run PIE checks
    results = pie_test_runner.run_checks()
    # 4) Stop PIE
    pie_test_runner.stop_pie()
    # 5) Assert and optionally write results
    out_path = pie_test_runner._output_path()
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({**results, "from_test": "test_level_pie_flow"}, f, indent=2)
    except Exception:
        pass
    assert results.get("all_passed", False), (
        "PIE checks failed: %s — %s" % (results.get("summary", "?"), results.get("checks", []))
    )

# test_level_loader.py
# PythonAutomationTest: validates smart level loader (latent load demo map and ready condition).
# Requires DemoMap to exist. Run via Editor: Tools > Test Automation.

import os
import sys

import unreal

# Allow importing level_loader from Content/Python
_script_dir = os.path.dirname(os.path.abspath(__file__))
_content_python = os.path.normpath(os.path.join(_script_dir, ".."))
if _content_python not in sys.path:
    sys.path.insert(0, _content_python)
import level_loader
import importlib
importlib.reload(level_loader)

DEMO_MAP_PATH = "/Game/HomeWorld/Maps/DemoMap"
MAX_WAIT_SEC = 30
LATENT_TIMEOUT_SEC = 45


def test_demo_map_loads_and_ready():
    """Load DemoMap via latent level loader and assert level is ready (landscape or WP bounds)."""
    try:
        lib = getattr(unreal, "PyAutomationTestLibrary", None)
        if lib and hasattr(lib, "set_latent_command_timeout"):
            lib.set_latent_command_timeout(LATENT_TIMEOUT_SEC)
    except Exception:
        pass
    gen = level_loader.latent_load_level_and_wait(
        DEMO_MAP_PATH, level_loader.landscape_has_bounds, MAX_WAIT_SEC
    )
    for _ in gen:
        yield
    is_loaded = level_loader.is_level_loaded(DEMO_MAP_PATH)
    has_bounds = level_loader.landscape_has_bounds()
    current_path = level_loader.get_current_level_path()
    assert is_loaded, (
        "Demo map level not loaded: current=%s" % current_path
    )
    assert has_bounds, (
        "Landscape or World Partition bounds not available after load"
    )

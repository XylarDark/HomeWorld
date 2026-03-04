# ensure_demo_portal.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Opens DemoMap (if not already), then places portal placeholder for planetoid travel (idempotent).
# Config: Content/Python/planetoid_map_config.json. See docs/tasks/DAYS_16_TO_30.md Day 16.

import sys
import os

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)
import level_loader
import place_portal_placeholder
import importlib
importlib.reload(level_loader)
importlib.reload(place_portal_placeholder)

DEMO_MAP_PATH = "/Game/HomeWorld/Maps/DemoMap"


def main():
    if not level_loader.is_level_loaded(DEMO_MAP_PATH):
        if not level_loader.open_level(DEMO_MAP_PATH):
            unreal.log("Ensure demo portal: Could not open DemoMap. Open it in the Editor and run again.")
            return
    place_portal_placeholder.main()


if __name__ == "__main__":
    main()

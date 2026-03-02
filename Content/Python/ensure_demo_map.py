# ensure_demo_map.py
# Run from Unreal Editor (Tools -> Execute Python Script or via MCP execute_python_script).
# Idempotent: only checks that DemoMap exists; does NOT duplicate from another level.
# If DemoMap does not exist, logs clear manual steps: File -> New Level -> Empty Open World -> Save As.
# Config: Content/Python/demo_map_config.json (demo_level_path).
# See docs/DEMO_MAP.md.

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)


def _log(msg):
    unreal.log("Demo Map: " + str(msg))
    print("Demo Map: " + str(msg))


def _load_config():
    """Load Content/Python/demo_map_config.json."""
    defaults = {"demo_level_path": "/Game/HomeWorld/Maps/DemoMap"}
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "demo_map_config.json")
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "demo_level_path" in data and not str("demo_level_path").startswith("_"):
            defaults["demo_level_path"] = data["demo_level_path"]
        return defaults
    except Exception as e:
        _log("Config load warning: " + str(e))
        return defaults


def ensure_demo_map_exists():
    """
    Return True if DemoMap exists at demo_level_path.
    If not, log manual steps (File -> New Level -> Empty Open World -> Save As) and return False.
    """
    config = _load_config()
    demo_path = config.get("demo_level_path", "/Game/HomeWorld/Maps/DemoMap")

    if unreal.EditorAssetLibrary.does_asset_exist(demo_path):
        _log("Demo map already exists at " + demo_path)
        return True

    _log("Demo map not found at " + demo_path + ".")
    _log("Create it once: File -> New Level -> Empty Open World -> Create. Then File -> Save As -> save to Content/HomeWorld/Maps/ as DemoMap (path " + demo_path + "). Then run this script again.")
    return False


def main():
    ensure_demo_map_exists()
    _log("Done. Open DemoMap in Editor if needed; World Partition is already enabled (Empty Open World).")


if __name__ == "__main__":
    main()

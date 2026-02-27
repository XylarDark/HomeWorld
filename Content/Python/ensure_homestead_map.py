# ensure_homestead_map.py
# Run from Unreal Editor (Tools -> Execute Python Script or via MCP execute_python_script).
# Idempotent: if Homestead map does not exist, duplicates Main to create it.
# Config: Content/Python/homestead_map_config.json (homestead_level_path, source_level_path).
# After run: open Homestead in Editor, enable World Partition in World Settings if needed.
# See docs/HOMESTEAD_MAP.md for layout and manual steps.

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)


def _log(msg):
    unreal.log("Homestead Map: " + str(msg))
    print("Homestead Map: " + str(msg))


def _load_config():
    """Load Content/Python/homestead_map_config.json."""
    defaults = {
        "homestead_level_path": "/Game/HomeWorld/Maps/Homestead",
        "source_level_path": "/Game/HomeWorld/Maps/Main",
    }
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "homestead_map_config.json")
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k in defaults:
            if k in data and not str(k).startswith("_"):
                defaults[k] = data[k]
        return defaults
    except Exception as e:
        _log("Config load warning: " + str(e))
        return defaults


def ensure_homestead_map_exists():
    """
    If Homestead level does not exist, duplicate Main (or source_level_path) to create it.
    Return True if Homestead exists (or was created).
    """
    config = _load_config()
    homestead_path = config.get("homestead_level_path", "/Game/HomeWorld/Maps/Homestead")
    source_path = config.get("source_level_path", "/Game/HomeWorld/Maps/Main")

    if unreal.EditorAssetLibrary.does_asset_exist(homestead_path):
        _log("Homestead map already exists at " + homestead_path)
        return True

    _log("Homestead map not found at " + homestead_path + "; attempting to duplicate from source.")
    if not unreal.EditorAssetLibrary.does_asset_exist(source_path):
        _log("Source level not found at " + source_path + ". Create Main first or set source_level_path in homestead_map_config.json.")
        _log("Manual step: In Content Browser duplicate Main to Homestead (/Game/HomeWorld/Maps/Homestead), then run this script again.")
        return False

    try:
        result = unreal.EditorAssetLibrary.duplicate_asset(source_path, homestead_path)
        if result:
            _log("Duplicated source to " + homestead_path)
            return True
    except Exception as e:
        _log("Level duplicate failed: " + str(e))

    _log("Manual step: In Content Browser duplicate Main to Homestead (/Game/HomeWorld/Maps/Homestead), then run this script again.")
    return False


def main():
    ensure_homestead_map_exists()
    _log("Done. Open Homestead map, enable World Partition in World Settings if needed.")


if __name__ == "__main__":
    main()

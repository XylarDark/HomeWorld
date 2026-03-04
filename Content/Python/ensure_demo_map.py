# ensure_demo_map.py
# Run from Unreal Editor (Tools -> Execute Python Script or via MCP execute_python_script).
# Idempotent: only checks that DemoMap exists; does NOT duplicate from another level.
# If DemoMap does not exist, tries to create it from template (config template_level_path) when set;
# otherwise logs clear manual steps: File -> New Level -> Empty Open World -> Save As.
# Config: Content/Python/demo_map_config.json (demo_level_path, template_level_path).
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
    defaults = {"demo_level_path": "/Game/HomeWorld/Maps/DemoMap", "template_level_path": None}
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "demo_map_config.json")
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "demo_level_path" in data and not str("demo_level_path").startswith("_"):
            defaults["demo_level_path"] = data["demo_level_path"]
        if "template_level_path" in data and data["template_level_path"]:
            defaults["template_level_path"] = data["template_level_path"]
        return defaults
    except Exception as e:
        _log("Config load warning: " + str(e))
        return defaults


def create_demo_map_from_template(demo_path, template_path):
    """
    Create a new level at demo_path from the template at template_path.
    Uses LevelEditorSubsystem.new_level_from_template (or EditorLevelLibrary fallback).
    Returns True if successful, False otherwise.
    """
    if not template_path or not demo_path:
        return False
    if not unreal.EditorAssetLibrary.does_asset_exist(template_path):
        _log("Template level does not exist at " + template_path + "; create it first (e.g. save Empty Open World as that path).")
        return False
    try:
        subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem) if hasattr(unreal, "get_editor_subsystem") else None
        if subsys and hasattr(subsys, "new_level_from_template"):
            ok = subsys.new_level_from_template(demo_path, template_path)
            if ok:
                _log("Created DemoMap from template: " + demo_path + " (template: " + template_path + ").")
            return bool(ok)
        if hasattr(unreal, "EditorLevelLibrary") and hasattr(unreal.EditorLevelLibrary, "new_level_from_template"):
            ok = unreal.EditorLevelLibrary.new_level_from_template(demo_path, template_path)
            if ok:
                _log("Created DemoMap from template: " + demo_path + " (template: " + template_path + ").")
            return bool(ok)
        _log("new_level_from_template not available; set template_level_path in config and use Editor that supports it.")
        return False
    except Exception as e:
        _log("create_demo_map_from_template failed: " + str(e))
        return False


def ensure_demo_map_exists():
    """
    Return True if DemoMap exists at demo_level_path.
    If not, tries to create from template (template_level_path in config) when set;
    otherwise logs manual steps (File -> New Level -> Empty Open World -> Save As) and return False.
    """
    config = _load_config()
    demo_path = config.get("demo_level_path", "/Game/HomeWorld/Maps/DemoMap")
    template_path = config.get("template_level_path")

    if unreal.EditorAssetLibrary.does_asset_exist(demo_path):
        _log("Demo map already exists at " + demo_path)
        return True

    _log("Demo map not found at " + demo_path + ".")
    if template_path:
        if create_demo_map_from_template(demo_path, template_path):
            return True
        _log("Template creation failed; see above. Alternatively create manually: File -> New Level -> Empty Open World -> Save As " + demo_path + ".")
    else:
        _log("Create it once: File -> New Level -> Empty Open World -> Create. Then File -> Save As -> save to Content/HomeWorld/Maps/ as DemoMap (path " + demo_path + "). Or set template_level_path in demo_map_config.json to a project-owned Empty Open World level and run again.")
    return False


def main():
    ensure_demo_map_exists()
    _log("Done. Open DemoMap in Editor if needed; World Partition is already enabled (Empty Open World).")


if __name__ == "__main__":
    main()

# ensure_planetoid_level.py
# Run from Unreal Editor (Tools -> Execute Python Script or via MCP execute_python_script).
# Idempotent: only checks that the planetoid level exists; does NOT duplicate.
# If missing, tries to create from template (planetoid_map_config template_level_path) when set;
# otherwise logs manual steps: File -> New Level -> Empty Open World -> Save As Planetoid_Pride.
# Config: Content/Python/planetoid_map_config.json.
# See docs/tasks/DAYS_16_TO_30.md (Day 16), docs/PLANETOID_DESIGN.md.

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)


def _log(msg):
    unreal.log("Planetoid: " + str(msg))
    print("Planetoid: " + str(msg))


def _load_config():
    """Load Content/Python/planetoid_map_config.json."""
    defaults = {
        "planetoid_level_path": "/Game/HomeWorld/Maps/Planetoid_Pride",
        "template_level_path": None,
    }
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "planetoid_map_config.json")
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "planetoid_level_path" in data and not str("planetoid_level_path").startswith("_"):
            defaults["planetoid_level_path"] = data["planetoid_level_path"]
        if "template_level_path" in data and data["template_level_path"]:
            defaults["template_level_path"] = data["template_level_path"]
        return defaults
    except Exception as e:
        _log("Config load warning: " + str(e))
        return defaults


def create_planetoid_from_template(planetoid_path, template_path):
    """Create level at planetoid_path from template_path. Returns True if successful."""
    if not template_path or not planetoid_path:
        return False
    if not unreal.EditorAssetLibrary.does_asset_exist(template_path):
        _log("Template level does not exist at " + template_path + "; create it first.")
        return False
    try:
        subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem) if hasattr(unreal, "get_editor_subsystem") else None
        if subsys and hasattr(subsys, "new_level_from_template"):
            ok = subsys.new_level_from_template(planetoid_path, template_path)
            if ok:
                _log("Created planetoid level from template: " + planetoid_path)
            return bool(ok)
        if hasattr(unreal, "EditorLevelLibrary") and hasattr(unreal.EditorLevelLibrary, "new_level_from_template"):
            ok = unreal.EditorLevelLibrary.new_level_from_template(planetoid_path, template_path)
            if ok:
                _log("Created planetoid level from template: " + planetoid_path)
            return bool(ok)
        _log("new_level_from_template not available.")
        return False
    except Exception as e:
        _log("create_planetoid_from_template failed: " + str(e))
        return False


def ensure_planetoid_level_exists():
    """
    Return True if planetoid level exists at planetoid_level_path.
    If not, tries to create from template when set; otherwise logs manual steps and return False.
    """
    config = _load_config()
    planetoid_path = config.get("planetoid_level_path", "/Game/HomeWorld/Maps/Planetoid_Pride")
    template_path = config.get("template_level_path")

    if unreal.EditorAssetLibrary.does_asset_exist(planetoid_path):
        _log("Planetoid level already exists at " + planetoid_path)
        return True

    _log("Planetoid level not found at " + planetoid_path + ".")
    if template_path:
        if create_planetoid_from_template(planetoid_path, template_path):
            return True
        _log("Template creation failed. Create manually: File -> New Level -> Empty Open World -> Save As " + planetoid_path)
    else:
        _log(
            "Create it once: File -> New Level -> Empty Open World -> Create. Then File -> Save As -> save to Content/HomeWorld/Maps/ as Planetoid_Pride (path "
            + planetoid_path
            + "). Or set template_level_path in planetoid_map_config.json and run again."
        )
    return False


def main():
    ensure_planetoid_level_exists()
    _log("Done. Planetoid level is used for Day 16+ (portal travel from DemoMap).")


if __name__ == "__main__":
    main()

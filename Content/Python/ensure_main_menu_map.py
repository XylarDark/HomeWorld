# ensure_main_menu_map.py
# Run from Unreal Editor (Tools -> Execute Python Script or via MCP execute_python_script).
# Idempotent: ensures MainMenu map exists at /Game/HomeWorld/Maps/MainMenu.
# If missing, creates from template when template_level_path is set in main_menu_config.json;
# otherwise logs manual steps. Game starts on MainMenu when GameDefaultMap is set to MainMenu.
# See docs/CHARACTER_GENERATION_AND_CUSTOMIZATION.md.

import json
import os

try:
    import unreal
except ImportError:
    import sys
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)


def _log(msg):
    unreal.log("Main Menu Map: " + str(msg))
    print("Main Menu Map: " + str(msg))


def _load_config():
    defaults = {"main_menu_level_path": "/Game/HomeWorld/Maps/MainMenu", "template_level_path": None}
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "main_menu_config.json")
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "main_menu_level_path" in data:
            defaults["main_menu_level_path"] = data["main_menu_level_path"]
        if "template_level_path" in data and data["template_level_path"]:
            defaults["template_level_path"] = data["template_level_path"]
        return defaults
    except Exception as e:
        _log("Config load warning: " + str(e))
        return defaults


def create_main_menu_from_template(level_path, template_path):
    if not template_path or not level_path:
        return False
    if not unreal.EditorAssetLibrary.does_asset_exist(template_path):
        _log("Template level does not exist at " + template_path)
        return False
    try:
        subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem) if hasattr(unreal, "get_editor_subsystem") else None
        if subsys and hasattr(subsys, "new_level_from_template"):
            ok = subsys.new_level_from_template(level_path, template_path)
            if ok:
                _log("Created MainMenu from template: " + level_path)
            return bool(ok)
        if hasattr(unreal, "EditorLevelLibrary") and hasattr(unreal.EditorLevelLibrary, "new_level_from_template"):
            ok = unreal.EditorLevelLibrary.new_level_from_template(level_path, template_path)
            if ok:
                _log("Created MainMenu from template: " + level_path)
            return bool(ok)
        _log("new_level_from_template not available.")
        return False
    except Exception as e:
        _log("create_main_menu_from_template failed: " + str(e))
        return False


def ensure_main_menu_map_exists():
    config = _load_config()
    level_path = config.get("main_menu_level_path", "/Game/HomeWorld/Maps/MainMenu")
    template_path = config.get("template_level_path")

    if unreal.EditorAssetLibrary.does_asset_exist(level_path):
        _log("MainMenu map already exists at " + level_path)
        return True

    _log("MainMenu map not found at " + level_path + ".")
    if template_path:
        if create_main_menu_from_template(level_path, template_path):
            return True
        _log("Template creation failed. Alternatively: File -> New Level -> Empty Level -> Save As " + level_path)
    else:
        _log("Create once: File -> New Level -> Empty Level (or Basic). Save As -> Content/HomeWorld/Maps/MainMenu. Or set template_level_path in Content/Python/main_menu_config.json.")
    return False


def main():
    ensure_main_menu_map_exists()
    _log("Done. Set GameDefaultMap to /Game/HomeWorld/Maps/MainMenu in DefaultEngine.ini to start game on main menu.")


if __name__ == "__main__":
    main()

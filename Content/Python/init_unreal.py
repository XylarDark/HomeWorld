# init_unreal.py
# Runs automatically when the Unreal Editor loads (Content/Python/ is a standard startup location).
# Ensures Enhanced Input assets (IA_Move, IA_Look, IMC_Default, etc.) exist so movement works
# without manually running setup_enhanced_input.py. Idempotent: safe to run every load.
# Also ensures MainMenu map exists (create from template if missing) and switches EditorStartupMap
# to MainMenu so the next Editor launch opens on the main menu.

import sys
import os

try:
    import unreal
except ImportError:
    # Not in Editor (e.g. standalone Python); skip
    sys.exit(0)

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

try:
    import setup_enhanced_input
    setup_enhanced_input.main()
except Exception as e:
    unreal.log_warning("InitUnreal: Enhanced Input setup failed: " + str(e))

try:
    import setup_gas_abilities
    setup_gas_abilities.main()
except Exception as e:
    unreal.log_warning("InitUnreal: GAS abilities setup failed: " + str(e))


def _set_editor_startup_map_to_main_menu():
    """If MainMenu exists, set EditorStartupMap=MainMenu in DefaultEngine.ini so next launch opens on main menu."""
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        ini_path = os.path.join(proj_dir, "Config", "DefaultEngine.ini")
        if not os.path.isfile(ini_path):
            return
        with open(ini_path, "r", encoding="utf-8") as f:
            content = f.read()
        main_menu_line = "EditorStartupMap=/Game/HomeWorld/Maps/MainMenu.MainMenu"
        if main_menu_line in content:
            return
        demo_line = "EditorStartupMap=/Game/HomeWorld/Maps/DemoMap.DemoMap"
        if demo_line not in content:
            return
        new_content = content.replace(demo_line, main_menu_line, 1)
        with open(ini_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        unreal.log("InitUnreal: EditorStartupMap set to MainMenu for next launch.")
    except Exception as e:
        unreal.log_warning("InitUnreal: Could not update EditorStartupMap: " + str(e))


try:
    import ensure_main_menu_map
    if ensure_main_menu_map.ensure_main_menu_map_exists():
        _set_editor_startup_map_to_main_menu()
except Exception as e:
    unreal.log_warning("InitUnreal: MainMenu ensure failed: " + str(e))

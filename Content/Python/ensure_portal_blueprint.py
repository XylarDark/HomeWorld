# ensure_portal_blueprint.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Creates or reuses BP_PortalToPlanetoid (Blueprint child of AHomeWorldDungeonEntrance) with default
# LevelToOpen = "Planetoid_Pride" so the portal opens the planetoid level without setting the
# property in Editor. Used by place_portal_placeholder.py when placing the DemoMap portal.
# Config: Content/Python/planetoid_map_config.json portal_level_to_open. Idempotent.

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

BP_NAME = "BP_PortalToPlanetoid"
BP_PATH = "/Game/HomeWorld"
BP_FULL = BP_PATH + "/" + BP_NAME
DEFAULT_LEVEL_TO_OPEN = "Planetoid_Pride"


def _log(msg):
    unreal.log("Portal blueprint: " + str(msg))
    print("Portal blueprint: " + str(msg))


def _set_level_to_open_default(bp, level_name):
    """Set LevelToOpen on the Blueprint's CDO so spawned instances open the correct level."""
    gen_class = None
    try:
        gen_class = bp.generated_class()
    except Exception:
        try:
            gen_class = bp.get_editor_property("generated_class")
        except Exception:
            pass
    if not gen_class:
        _log("Could not get generated class; set LevelToOpen in Editor.")
        return False
    try:
        cdo = unreal.get_default_object(gen_class)
        if not cdo:
            return False
        for prop_name in ("LevelToOpen", "level_to_open"):
            try:
                cdo.set_editor_property(prop_name, unreal.Name(level_name))
                _log("Set CDO LevelToOpen to '%s'." % level_name)
                return True
            except Exception:
                continue
        _log("Could not set LevelToOpen on CDO (tried %s)." % level_name)
        return False
    except Exception as e:
        _log("Could not set LevelToOpen on CDO: " + str(e))
        return False


def main():
    _log("Start.")
    level_to_open = DEFAULT_LEVEL_TO_OPEN
    try:
        import json
        import os
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "planetoid_map_config.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data.get("portal_level_to_open"), str) and data["portal_level_to_open"]:
                level_to_open = data["portal_level_to_open"]
    except Exception as e:
        _log("Config load: " + str(e))

    if unreal.EditorAssetLibrary.does_asset_exist(BP_FULL):
        bp = unreal.load_asset(BP_FULL)
        if bp:
            _log("Reusing existing Blueprint: " + BP_FULL)
            if _set_level_to_open_default(bp, level_to_open):
                unreal.EditorAssetLibrary.save_loaded_asset(bp)
            _log("Done.")
            return

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = getattr(unreal, "BlueprintFactory", None)
    if not factory:
        _log("BlueprintFactory not found. Create " + BP_NAME + " manually (parent HomeWorldDungeonEntrance), set LevelToOpen in Details.")
        return
    factory = factory()

    parent_class = None
    try:
        parent_class = unreal.load_class(None, "/Script/HomeWorld.HomeWorldDungeonEntrance")
    except Exception:
        pass
    if not parent_class:
        try:
            mod = getattr(unreal, "HomeWorld", None)
            if mod:
                cls = getattr(mod, "HomeWorldDungeonEntrance", None)
                if cls and hasattr(cls, "static_class"):
                    parent_class = cls.static_class()
        except Exception:
            pass
    if not parent_class:
        _log("Could not find AHomeWorldDungeonEntrance. Ensure C++ is compiled.")
        return

    factory.set_editor_property("parent_class", parent_class)
    bp = asset_tools.create_asset(BP_NAME, BP_PATH, None, factory)
    if not bp:
        _log("Failed to create " + BP_NAME)
        return

    _log("Created Blueprint: " + BP_FULL)
    _set_level_to_open_default(bp, level_to_open)
    unreal.EditorAssetLibrary.save_loaded_asset(bp)
    _log("Done. Portal placed via place_portal_placeholder will open '%s'." % level_to_open)


if __name__ == "__main__":
    main()

# setup_animation_blueprint.py
# Run from Unreal Editor: Tools -> Execute Python Script, or via MCP execute_python_script.
# Creates ABP_HomeWorldCharacter Animation Blueprint with the correct skeleton and
# C++ parent class (UHomeWorldAnimInstance). The AnimGraph must be populated manually.
# Idempotent: skips creation if the asset already exists.

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

ABP_NAME = "ABP_HomeWorldCharacter"
ABP_PATH = "/Game/HomeWorld/Characters"
ABP_FULL = ABP_PATH + "/" + ABP_NAME
CONFIG_FILE = "character_blueprint_config.json"


def _log(msg):
    unreal.log("AnimBP Setup: " + str(msg))
    print("AnimBP Setup: " + str(msg))


def _load_config():
    """Load skeleton mesh path from character config to derive the skeleton asset."""
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", CONFIG_FILE)
        if not os.path.exists(config_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, CONFIG_FILE)
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                return json.load(f)
    except Exception as e:
        _log("Config load warning: " + str(e))
    return {}


def _find_skeleton_from_mesh(sk_mesh_path):
    """Given a skeletal mesh asset path, load it and return its Skeleton asset."""
    if not sk_mesh_path:
        return None
    if not unreal.EditorAssetLibrary.does_asset_exist(sk_mesh_path):
        _log("Skeletal mesh not found: " + sk_mesh_path)
        return None
    sk_mesh = unreal.load_asset(sk_mesh_path)
    if not sk_mesh:
        return None
    skeleton = None
    try:
        skeleton = sk_mesh.get_editor_property("skeleton")
    except Exception:
        pass
    if not skeleton:
        try:
            skeleton = sk_mesh.skeleton
        except Exception:
            pass
    return skeleton


def _find_skeleton():
    """Try to find the skeleton from config mesh path, or fall back to known paths."""
    config = _load_config()
    sk_path = config.get("skeletal_mesh", "")
    if sk_path:
        skeleton = _find_skeleton_from_mesh(sk_path)
        if skeleton:
            _log("Found skeleton from config mesh: " + skeleton.get_path_name())
            return skeleton

    fallback_paths = [
        "/Game/Man/Demo/Mesh/UE4_Mannequin_Skeleton",
        "/Game/Characters/Mannequins/Meshes/SKM_Manny",
    ]
    for path in fallback_paths:
        if unreal.EditorAssetLibrary.does_asset_exist(path):
            asset = unreal.load_asset(path)
            if asset:
                if isinstance(asset, unreal.Skeleton):
                    _log("Using fallback skeleton: " + path)
                    return asset
                skeleton = _find_skeleton_from_mesh(path)
                if skeleton:
                    _log("Found skeleton from fallback mesh: " + skeleton.get_path_name())
                    return skeleton
    return None


def _get_anim_instance_class():
    """Load the C++ UHomeWorldAnimInstance class for use as parent."""
    try:
        cls = unreal.load_class(None, "/Script/HomeWorld.HomeWorldAnimInstance")
        if cls:
            return cls
    except Exception:
        pass
    anim_cls = getattr(unreal, "HomeWorldAnimInstance", None)
    if anim_cls:
        try:
            return anim_cls.static_class()
        except Exception:
            pass
    _log("UHomeWorldAnimInstance not found. Rebuild C++ first. Falling back to base UAnimInstance.")
    return None


def main():
    _log("Setting up Animation Blueprint...")

    if unreal.EditorAssetLibrary.does_asset_exist(ABP_FULL):
        _log("Skipping — " + ABP_FULL + " already exists.")
        return unreal.load_asset(ABP_FULL)

    skeleton = _find_skeleton()
    if not skeleton:
        _log("Could not find a skeleton asset. Set skeletal_mesh in " + CONFIG_FILE + " and ensure the mesh is imported.")
        return None

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    factory = None
    for factory_name in ("AnimBlueprintFactory", "AnimationBlueprintFactory", "AnimBlueprint_Factory"):
        factory_cls = getattr(unreal, factory_name, None)
        if factory_cls:
            factory = factory_cls()
            break
    if not factory:
        _log("No AnimBP factory found. Create the AnimBP manually in Editor.")
        return None

    try:
        factory.set_editor_property("target_skeleton", skeleton)
    except Exception as e:
        _log("Could not set target_skeleton on factory: " + str(e))

    parent_class = _get_anim_instance_class()
    if parent_class:
        try:
            factory.set_editor_property("parent_class", parent_class)
            _log("Set parent class to UHomeWorldAnimInstance.")
        except Exception as e:
            _log("Could not set parent_class: " + str(e) + ". AnimBP will use default UAnimInstance.")

    abp = asset_tools.create_asset(ABP_NAME, ABP_PATH, None, factory)
    if not abp:
        _log("Failed to create " + ABP_NAME + ". Check Output Log for details.")
        return None

    try:
        unreal.EditorAssetLibrary.save_loaded_asset(abp)
    except Exception:
        try:
            unreal.EditorAssetSubsystem().save_asset(ABP_FULL)
        except Exception:
            pass

    _log("Created " + ABP_FULL + " with skeleton: " + skeleton.get_path_name())
    _log("Next: Open the AnimBP in Editor and add a State Machine with Idle/Locomotion states.")
    _log("The C++ parent class (UHomeWorldAnimInstance) exposes Speed, bIsInAir, bIsMoving — use them in transitions.")
    return abp


if __name__ == "__main__":
    main()

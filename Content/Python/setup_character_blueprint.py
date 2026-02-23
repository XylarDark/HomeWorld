# setup_character_blueprint.py
# Run from Unreal Editor: Tools -> Execute Python Script.
# Creates BP_HomeWorldCharacter (Blueprint child of AHomeWorldCharacter) and assigns:
#   - MoveAction -> IA_Move, LookAction -> IA_Look, DefaultMappingContext -> IMC_Default
#   - Optional: skeletal mesh and Animation Blueprint from config
# Re-runnable: deletes existing Blueprint before creating a new one.

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

BP_NAME = "BP_HomeWorldCharacter"
BP_PATH = "/Game/HomeWorld/Characters"
BP_FULL = BP_PATH + "/" + BP_NAME
INPUT_PATH = "/Game/HomeWorld/Input"
CONFIG_FILE = "character_blueprint_config.json"


def _log(msg):
    unreal.log("CharBP: " + str(msg))
    print("CharBP: " + str(msg))


def _load_config():
    """Load optional config for skeletal mesh path, anim blueprint path, mesh forward yaw offset."""
    defaults = {
        "skeletal_mesh": "",
        "anim_blueprint": "",
        "mesh_forward_yaw_offset": 0.0,
    }
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", CONFIG_FILE)
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r") as f:
            data = json.load(f)
        for k in defaults:
            if k in data and not k.startswith("_"):
                defaults[k] = data[k]
        return defaults
    except Exception as e:
        _log("Config load warning: " + str(e))
        return defaults


def _delete_if_exists(asset_path):
    if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        unreal.EditorAssetLibrary.delete_asset(asset_path)


def _create_character_blueprint():
    """Create a Blueprint child of AHomeWorldCharacter."""
    _delete_if_exists(BP_FULL)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    factory = None
    for factory_name in ("BlueprintFactory",):
        cls = getattr(unreal, factory_name, None)
        if cls:
            factory = cls()
            break
    if not factory:
        _log("BlueprintFactory not found. Create " + BP_NAME + " manually.")
        return None

    parent_class = None
    try:
        parent_class = unreal.HomeWorldCharacter.static_class()
    except (AttributeError, Exception):
        pass
    if not parent_class:
        try:
            parent_class = unreal.load_class(None, "/Script/HomeWorld.HomeWorldCharacter")
        except Exception:
            pass
    if not parent_class:
        _log("Could not find AHomeWorldCharacter class. Ensure the module is compiled.")
        return None

    factory.set_editor_property("parent_class", parent_class)

    bp = asset_tools.create_asset(BP_NAME, BP_PATH, None, factory)
    if not bp:
        _log("Failed to create " + BP_NAME)
        return None

    _log("Created Blueprint: " + BP_FULL)
    return bp


def _get_cdo(bp):
    """Get the Class Default Object for the Blueprint's generated class."""
    gen_class = None
    try:
        gen_class = bp.generated_class()
    except Exception:
        pass
    if not gen_class:
        try:
            gen_class = bp.get_editor_property("generated_class")
        except Exception:
            pass
    if not gen_class:
        return None
    try:
        return unreal.get_default_object(gen_class)
    except Exception:
        return None


def _assign_input_assets(bp):
    """Load IA_Move, IA_Look, IMC_Default and assign to BP defaults."""
    cdo = _get_cdo(bp)
    if not cdo:
        _log("Could not get CDO; assign input assets in Editor on " + BP_NAME + " class defaults.")
        return

    assets = {
        "move_action": INPUT_PATH + "/IA_Move",
        "look_action": INPUT_PATH + "/IA_Look",
        "default_mapping_context": INPUT_PATH + "/IMC_Default",
    }
    for prop, path in assets.items():
        asset = unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else None
        if not asset:
            _log("Asset not found: " + path + " (run setup_enhanced_input.py first or create in Editor)")
            continue
        try:
            cdo.set_editor_property(prop, asset)
            _log("Assigned " + prop + " = " + path)
        except Exception as e:
            _log("Could not set " + prop + " on CDO: " + str(e) + ". Assign in Editor.")


def _assign_mesh_and_anim(bp, config):
    """Assign skeletal mesh and Animation Blueprint from config."""
    sk_path = config.get("skeletal_mesh", "")
    anim_path = config.get("anim_blueprint", "")
    yaw_offset = float(config.get("mesh_forward_yaw_offset", 0.0))

    cdo = _get_cdo(bp)

    if yaw_offset != 0.0 and cdo:
        try:
            cdo.set_editor_property("mesh_forward_yaw_offset", yaw_offset)
            _log("Set MeshForwardYawOffset = " + str(yaw_offset))
        except Exception as e:
            _log("Could not set MeshForwardYawOffset: " + str(e))

    if not sk_path and not anim_path:
        _log("No skeletal_mesh or anim_blueprint in config; set in Editor or add to " + CONFIG_FILE)
        return

    mesh_comp = None
    try:
        subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
        handles = subsystem.k2_gather_subobject_data_for_blueprint(bp)
        bp_lib = unreal.SubobjectDataBlueprintFunctionLibrary
        for handle in handles:
            data = bp_lib.get_data(handle)
            obj = bp_lib.get_object(data)
            if obj and obj.get_class().get_name() == "SkeletalMeshComponent":
                mesh_comp = obj
                break
    except Exception:
        pass

    if not mesh_comp and cdo:
        try:
            mesh_comp = cdo.get_editor_property("mesh")
        except Exception:
            pass

    if sk_path and mesh_comp:
        sk_asset = unreal.load_asset(sk_path) if unreal.EditorAssetLibrary.does_asset_exist(sk_path) else None
        if sk_asset:
            try:
                mesh_comp.set_editor_property("skeletal_mesh_asset", sk_asset)
                _log("Assigned skeletal mesh: " + sk_path)
            except Exception:
                try:
                    mesh_comp.set_editor_property("skeletal_mesh", sk_asset)
                    _log("Assigned skeletal mesh: " + sk_path)
                except Exception as e:
                    _log("Could not set skeletal mesh: " + str(e))
        else:
            _log("Skeletal mesh not found: " + sk_path)

    if anim_path and mesh_comp:
        anim_asset = unreal.load_asset(anim_path) if unreal.EditorAssetLibrary.does_asset_exist(anim_path) else None
        if anim_asset:
            try:
                anim_class = anim_asset.generated_class() if hasattr(anim_asset, "generated_class") else anim_asset.get_editor_property("generated_class")
                mesh_comp.set_editor_property("anim_class", anim_class)
                _log("Assigned Animation Blueprint: " + anim_path)
            except Exception as e:
                _log("Could not set anim_class: " + str(e) + ". Assign AnimBP in Editor.")
        else:
            _log("Animation Blueprint not found: " + anim_path)

    if not mesh_comp:
        _log("Could not access SkeletalMeshComponent on " + BP_NAME + "; assign mesh/anim in Editor.")


def main():
    _log("Creating character Blueprint...")
    config = _load_config()
    bp = _create_character_blueprint()
    if not bp:
        return None
    _assign_input_assets(bp)
    _assign_mesh_and_anim(bp, config)

    try:
        unreal.EditorAssetLibrary.save_loaded_asset(bp)
    except Exception:
        try:
            unreal.EditorAssetSubsystem().save_asset(BP_FULL)
        except Exception:
            pass

    try:
        unreal.KismetSystemLibrary.flush_persistent_debug_lines(None)
    except Exception:
        pass

    _log("Done. " + BP_NAME + " is at " + BP_FULL)
    _log("If skeletal mesh or AnimBP are not set, add paths to Content/Python/" + CONFIG_FILE + " and re-run, or assign in Editor.")
    return bp


if __name__ == "__main__":
    main()

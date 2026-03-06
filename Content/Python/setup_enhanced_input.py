# setup_enhanced_input.py
# Run from Unreal Editor: Tools -> Execute Python Script.
# Creates Enhanced Input assets: IA_Move (Axis2D), IA_Look (Axis2D), IMC_Default (WASD + Mouse).
# Idempotent: skips creation if assets already exist to preserve manual customizations.

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

INPUT_PATH = "/Game/HomeWorld/Input"
IA_MOVE_NAME = "IA_Move"
IA_LOOK_NAME = "IA_Look"
IA_MOVE_FORWARD_NAME = "IA_MoveForward"
IA_MOVE_BACK_NAME = "IA_MoveBack"
IA_STRAFE_LEFT_NAME = "IA_StrafeLeft"
IA_STRAFE_RIGHT_NAME = "IA_StrafeRight"
IA_ASTRAL_DEATH_NAME = "IA_AstralDeath"
IMC_NAME = "IMC_Default"


def _log(msg):
    unreal.log("InputSetup: " + str(msg))
    print("InputSetup: " + str(msg))


def _asset_exists(asset_path):
    return unreal.EditorAssetLibrary.does_asset_exist(asset_path)


def _create_input_action(name, value_type_name="Axis2D"):
    """Create an InputAction asset if it doesn't already exist. value_type_name: 'Boolean', 'Axis1D', 'Axis2D', 'Axis3D'."""
    asset_path = INPUT_PATH + "/" + name
    if _asset_exists(asset_path):
        _log("Skipping " + asset_path + " (already exists)")
        return unreal.load_asset(asset_path)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    factory = None
    for factory_name in ("InputActionFactory", "InputAction_Factory"):
        cls = getattr(unreal, factory_name, None)
        if cls:
            factory = cls()
            break
    if not factory:
        _log("No InputAction factory found. Create " + name + " manually in Editor.")
        return None

    ia = asset_tools.create_asset(name, INPUT_PATH, None, factory)
    if not ia:
        _log("Failed to create " + name)
        return None

    vtype_map = {"Boolean": 0, "Axis1D": 1, "Axis2D": 2, "Axis3D": 3}
    for enum_cls_name in ("EInputActionValueType", "InputActionValueType"):
        enum_cls = getattr(unreal, enum_cls_name, None)
        if enum_cls:
            val = getattr(enum_cls, value_type_name.upper(), None) or getattr(enum_cls, value_type_name, None)
            if val is not None:
                try:
                    ia.set_editor_property("value_type", val)
                    break
                except Exception:
                    pass
    else:
        idx = vtype_map.get(value_type_name)
        if idx is not None:
            try:
                ia.set_editor_property("value_type", idx)
            except Exception:
                _log("Could not set value_type on " + name + "; set to Axis2D in Editor.")

    unreal.EditorAssetLibrary.save_loaded_asset(ia)
    _log("Created " + asset_path)
    return ia


def _get_key(key_name):
    """Resolve key name to Unreal Key struct (required by InputMappingContext.map_key)."""
    key_cls = getattr(unreal, "Key", None)
    name_cls = getattr(unreal, "Name", None)
    if key_cls and name_cls:
        try:
            key_obj = key_cls()
            key_obj.set_editor_property("key_name", name_cls(key_name))
            return key_obj
        except Exception:
            pass
    # Fallback: Keys enum (e.g. Keys.W) may work in some UE versions
    keys_cls = getattr(unreal, "Keys", None)
    if keys_cls:
        attr_name = key_name.replace(" ", "_")
        k = getattr(keys_cls, attr_name, None)
        if k is not None and not callable(k):
            return k
    return None


def _add_default_mappings(imc, ia_move, ia_look):
    """Add WASD -> IA_Move and Mouse2D -> IA_Look to an IMC. Used for new and existing IMCs."""
    if not imc or not hasattr(imc, "map_key"):
        return

    def _add_modifier(mapping, modifier_cls, **mod_props):
        if not mapping or not modifier_cls:
            return
        mod = modifier_cls()
        for prop_name, prop_val in mod_props.items():
            try:
                mod.set_editor_property(prop_name, prop_val)
            except Exception:
                pass
        try:
            existing = list(mapping.get_editor_property("modifiers") or [])
            existing.append(mod)
            mapping.set_editor_property("modifiers", existing)
        except Exception:
            try:
                mapping.modifiers.append(mod)
            except Exception:
                pass

    swizzle_cls = getattr(unreal, "InputModifierSwizzleAxis", None)
    negate_cls = getattr(unreal, "InputModifierNegate", None)
    # YXZ = swap X and Y so 1D key value goes to Y axis (forward/back for Move).
    for enum_name in ("InputAxisSwizzle", "EInputAxisSwizzle"):
        swizzle_order_yxz = getattr(getattr(unreal, enum_name, None), "YXZ", None)
        if swizzle_order_yxz is not None:
            break

    def _map_key_safe(action, key_name):
        key_obj = _get_key(key_name)
        if key_obj is None:
            _log("Could not resolve key '" + key_name + "'; skipping.")
            return None
        try:
            return imc.map_key(action, key_obj)
        except Exception as e:
            _log("map_key failed for " + key_name + ": " + str(e))
            return None

    if ia_move:
        # W/S: 1D key defaults to Axis.X in UE -> we use Axis.X for forward/back. No swizzle; Negate for S.
        mapping_w = _map_key_safe(ia_move, "W")
        mapping_s = _map_key_safe(ia_move, "S")
        if negate_cls and mapping_s:
            _add_modifier(mapping_s, negate_cls)
        # D/A: 1D key -> Axis.Y (strafe). Swizzle YXZ puts key value on Y.
        mapping_d = _map_key_safe(ia_move, "D")
        if swizzle_cls and mapping_d:
            _add_modifier(mapping_d, swizzle_cls, **({"order": swizzle_order_yxz} if swizzle_order_yxz is not None else {}))
        mapping_a = _map_key_safe(ia_move, "A")
        if swizzle_cls and mapping_a:
            _add_modifier(mapping_a, swizzle_cls, **({"order": swizzle_order_yxz} if swizzle_order_yxz is not None else {}))
        if negate_cls and mapping_a:
            _add_modifier(mapping_a, negate_cls)

    if ia_look:
        for mouse_key_name in ("Mouse2D", "MouseXY", "Mouse_XY_2D_Axis", "Mouse XY 2D-Axis"):
            if _map_key_safe(ia_look, mouse_key_name) is not None:
                break
        else:
            _log("Could not map Mouse2D to IA_Look; bind mouse in Editor.")


def _add_four_directional_mappings(imc, ia_forward, ia_back, ia_left, ia_right):
    """Map W/S/A/D to the four Boolean actions (no modifiers). C++ uses these for reliable camera-relative movement."""
    if not imc or not hasattr(imc, "map_key"):
        return

    def _map_key_safe(action, key_name):
        key_obj = _get_key(key_name)
        if key_obj is None:
            _log("Could not resolve key '" + key_name + "'; skipping.")
            return None
        try:
            return imc.map_key(action, key_obj)
        except Exception as e:
            _log("map_key failed for " + key_name + ": " + str(e))
            return None

    if ia_forward:
        _map_key_safe(ia_forward, "W")
    if ia_back:
        _map_key_safe(ia_back, "S")
    if ia_left:
        _map_key_safe(ia_left, "A")
    if ia_right:
        _map_key_safe(ia_right, "D")


def _create_mapping_context(name, ia_move, ia_look, ia_forward=None, ia_back=None, ia_left=None, ia_right=None):
    """Create IMC_Default with WASD -> IA_Move and Mouse2D -> IA_Look. If already exists, ensures mappings are present."""
    asset_path = INPUT_PATH + "/" + name
    if _asset_exists(asset_path):
        _log("IMC already exists; ensuring WASD + Mouse mappings: " + asset_path)
        imc = unreal.load_asset(asset_path)
        if imc:
            # Remove existing Move/Look mappings so we don't duplicate; re-add with correct modifiers.
            if hasattr(imc, "unmap_all_keys_from_action"):
                if ia_move:
                    imc.unmap_all_keys_from_action(ia_move)
                if ia_look:
                    imc.unmap_all_keys_from_action(ia_look)
                for ia in (ia_forward, ia_back, ia_left, ia_right):
                    if ia:
                        imc.unmap_all_keys_from_action(ia)
            _add_default_mappings(imc, ia_move, ia_look)
            _add_four_directional_mappings(imc, ia_forward, ia_back, ia_left, ia_right)
            unreal.EditorAssetLibrary.save_loaded_asset(imc)
            _log("Updated " + asset_path + " with WASD + Mouse bindings")
        return imc

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    factory = None
    for factory_name in ("InputMappingContextFactory", "InputMappingContext_Factory"):
        cls = getattr(unreal, factory_name, None)
        if cls:
            factory = cls()
            break
    if not factory:
        _log("No InputMappingContext factory found. Create " + name + " manually in Editor.")
        return None

    imc = asset_tools.create_asset(name, INPUT_PATH, None, factory)
    if not imc:
        _log("Failed to create " + name)
        return None

    if not hasattr(imc, "map_key"):
        _log(name + " created but map_key() not available; add key bindings in Editor.")
        unreal.EditorAssetLibrary.save_loaded_asset(imc)
        return imc

    _add_default_mappings(imc, ia_move, ia_look)
    _add_four_directional_mappings(imc, ia_forward, ia_back, ia_left, ia_right)
    unreal.EditorAssetLibrary.save_loaded_asset(imc)
    _log("Created " + asset_path + " with WASD + Mouse bindings")
    return imc


def _add_astral_death_to_imc(imc, ia_astral):
    """Add F8 -> IA_AstralDeath to IMC_Default for in-game astral death trigger (T1). Idempotent."""
    if not imc or not ia_astral or not hasattr(imc, "map_key"):
        return
    try:
        if hasattr(imc, "unmap_all_keys_from_action") and ia_astral:
            imc.unmap_all_keys_from_action(ia_astral)
    except Exception:
        pass
    key = _get_key("F8")
    if key is None:
        _log("Could not resolve F8 for IA_AstralDeath; bind in Editor.")
        return
    try:
        imc.map_key(ia_astral, key)
        unreal.EditorAssetLibrary.save_loaded_asset(imc)
        _log("Added IA_AstralDeath (F8) to IMC_Default for astral death trigger.")
    except Exception as e:
        _log("map_key IA_AstralDeath failed: " + str(e))


def main():
    _log("Creating Enhanced Input assets...")
    ia_move = _create_input_action(IA_MOVE_NAME, "Axis2D")
    ia_look = _create_input_action(IA_LOOK_NAME, "Axis2D")
    ia_forward = _create_input_action(IA_MOVE_FORWARD_NAME, "Boolean")
    ia_back = _create_input_action(IA_MOVE_BACK_NAME, "Boolean")
    ia_left = _create_input_action(IA_STRAFE_LEFT_NAME, "Boolean")
    ia_right = _create_input_action(IA_STRAFE_RIGHT_NAME, "Boolean")
    imc = _create_mapping_context(IMC_NAME, ia_move, ia_look, ia_forward, ia_back, ia_left, ia_right)
    ia_astral = _create_input_action(IA_ASTRAL_DEATH_NAME, "Boolean")
    if ia_astral and imc:
        _add_astral_death_to_imc(imc, ia_astral)
    if ia_move and ia_look and imc:
        _log("Done. IA_Move, IA_Look, IMC_Default + IA_MoveForward/Back/StrafeLeft/Right + IA_AstralDeath (F8) at " + INPUT_PATH)
    else:
        _log("Some assets could not be created; check log above and finish in Editor.")
    return ia_move, ia_look, imc


if __name__ == "__main__":
    main()

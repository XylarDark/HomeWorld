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


def _create_mapping_context(name, ia_move, ia_look):
    """Create IMC_Default with WASD -> IA_Move and Mouse2D -> IA_Look. Skips if already exists."""
    asset_path = INPUT_PATH + "/" + name
    if _asset_exists(asset_path):
        _log("Skipping " + asset_path + " (already exists)")
        return unreal.load_asset(asset_path)

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

    def _get_key(name):
        key_cls = getattr(unreal, "Key", None)
        if key_cls:
            try:
                return key_cls(name)
            except Exception:
                pass
        keys_cls = getattr(unreal, "Keys", None)
        if keys_cls:
            k = getattr(keys_cls, name, None)
            if k:
                return k
        return name

    def _add_modifier(mapping, modifier_cls):
        """Try to append a modifier to an EnhancedActionKeyMapping."""
        if not mapping:
            return
        mod = modifier_cls()
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

    if ia_move:
        # W -> IA_Move: Swizzle (YXZ) so 1D key press maps to Y-axis (forward)
        mapping_w = imc.map_key(ia_move, _get_key("W"))
        if swizzle_cls and mapping_w:
            _add_modifier(mapping_w, swizzle_cls)

        # S -> IA_Move: Swizzle (YXZ) + Negate (backward)
        mapping_s = imc.map_key(ia_move, _get_key("S"))
        if swizzle_cls and mapping_s:
            _add_modifier(mapping_s, swizzle_cls)
        if negate_cls and mapping_s:
            _add_modifier(mapping_s, negate_cls)

        # D -> IA_Move: no modifiers (X-axis positive = right)
        imc.map_key(ia_move, _get_key("D"))

        # A -> IA_Move: Negate (X-axis negative = left)
        mapping_a = imc.map_key(ia_move, _get_key("A"))
        if negate_cls and mapping_a:
            _add_modifier(mapping_a, negate_cls)

    if ia_look:
        # Mouse 2D -> IA_Look
        for mouse_key_name in ("Mouse2D", "MouseXY", "Mouse XY 2D-Axis"):
            try:
                imc.map_key(ia_look, _get_key(mouse_key_name))
                break
            except Exception:
                continue
        else:
            _log("Could not map Mouse2D to IA_Look; bind mouse in Editor.")

    unreal.EditorAssetLibrary.save_loaded_asset(imc)
    _log("Created " + asset_path + " with WASD + Mouse bindings")
    return imc


def main():
    _log("Creating Enhanced Input assets...")
    ia_move = _create_input_action(IA_MOVE_NAME, "Axis2D")
    ia_look = _create_input_action(IA_LOOK_NAME, "Axis2D")
    imc = _create_mapping_context(IMC_NAME, ia_move, ia_look)
    if ia_move and ia_look and imc:
        _log("Done. IA_Move, IA_Look, IMC_Default created at " + INPUT_PATH)
    else:
        _log("Some assets could not be created; check log above and finish in Editor.")
    return ia_move, ia_look, imc


if __name__ == "__main__":
    main()

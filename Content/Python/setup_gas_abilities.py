# setup_gas_abilities.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP.
# Creates the survivor ability Blueprints (GA_PrimaryAttack, GA_Dodge, GA_Interact, GA_Place), ability input actions,
# adds them to IMC_Default, and assigns abilities + input on BP_HomeWorldCharacter.
# Idempotent: reuses existing assets.

import sys
import os

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

ABILITIES_PATH = "/Game/HomeWorld/Abilities"
INPUT_PATH = "/Game/HomeWorld/Input"
CHAR_BP_PATH = "/Game/HomeWorld/Characters/BP_HomeWorldCharacter"

GA_NAMES = ["GA_PrimaryAttack", "GA_Dodge", "GA_Interact", "GA_Place"]
IA_ABILITY_NAMES = ["IA_PrimaryAttack", "IA_Dodge", "IA_Interact", "IA_Place"]
# Use Unreal EKeys/FKey names (no spaces): LeftMouseButton, LeftShift, E, P
IA_KEYS = ["LeftMouseButton", "LeftShift", "E", "P"]
# GA_Place uses HomeWorldPlaceAbility; others use HomeWorldGameplayAbility
GA_SPECIFIC_PARENT = {"GA_Place": "HomeWorldPlaceAbility"}
IMC_NAME = "IMC_Default"


def _log(msg):
    unreal.log("GAS Abilities: " + str(msg))
    print("GAS Abilities: " + str(msg))


def _get_parent_class(ability_name=None):
    """Return C++ class for Blueprint parent. ability_name: e.g. GA_Place -> HomeWorldPlaceAbility; else HomeWorldGameplayAbility."""
    class_name = GA_SPECIFIC_PARENT.get(ability_name, "HomeWorldGameplayAbility")
    try:
        mod = getattr(unreal, "HomeWorld", None)
        if mod:
            cls = getattr(mod, class_name, None)
            if cls and hasattr(cls, "static_class"):
                return cls.static_class()
    except Exception:
        pass
    try:
        return unreal.load_class(None, "/Script/HomeWorld." + class_name)
    except Exception:
        pass
    return None


def _create_ability_blueprint(name):
    """Create a Blueprint child of the appropriate C++ ability class if it doesn't exist."""
    asset_path = ABILITIES_PATH + "/" + name
    if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        asset = unreal.load_asset(asset_path)
        if asset:
            _log("Reusing " + asset_path)
            return asset
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = getattr(unreal, "BlueprintFactory", None)
    if not factory:
        _log("BlueprintFactory not found. Create " + name + " manually.")
        return None
    factory = factory()
    parent_class = _get_parent_class(name)
    if not parent_class:
        _log("Parent class for " + name + " not found. Compile C++ and re-run.")
        return None
    factory.set_editor_property("parent_class", parent_class)
    bp = asset_tools.create_asset(name, ABILITIES_PATH, None, factory)
    if bp:
        unreal.EditorAssetLibrary.save_loaded_asset(bp)
        _log("Created " + asset_path)
    return bp


def _create_input_action(name, value_type="Boolean"):
    """Create InputAction (Boolean) if it doesn't exist."""
    asset_path = INPUT_PATH + "/" + name
    if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        return unreal.load_asset(asset_path)
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    for factory_name in ("InputActionFactory", "InputAction_Factory"):
        cls = getattr(unreal, factory_name, None)
        if cls:
            factory = cls()
            break
    else:
        _log("No InputAction factory. Create " + name + " manually.")
        return None
    ia = asset_tools.create_asset(name, INPUT_PATH, None, factory)
    if not ia:
        return None
    for enum_cls_name in ("EInputActionValueType", "InputActionValueType"):
        enum_cls = getattr(unreal, enum_cls_name, None)
        if enum_cls:
            val = getattr(enum_cls, value_type.upper(), None) or getattr(enum_cls, value_type, None)
            if val is not None:
                try:
                    ia.set_editor_property("value_type", val)
                    break
                except Exception:
                    pass
    unreal.EditorAssetLibrary.save_loaded_asset(ia)
    _log("Created " + asset_path)
    return ia


def _get_key(key_name):
    key_cls = getattr(unreal, "Key", None)
    name_cls = getattr(unreal, "Name", None)
    if key_cls and name_cls:
        try:
            key_obj = key_cls()
            key_obj.set_editor_property("key_name", name_cls(key_name))
            return key_obj
        except Exception:
            pass
    keys_cls = getattr(unreal, "Keys", None)
    if keys_cls:
        attr = key_name.replace(" ", "_")
        k = getattr(keys_cls, attr, None)
        if k is not None and not callable(k):
            return k
    return None


def _add_ability_mappings_to_imc(imc, actions_with_keys):
    """Add mappings (action -> key) to existing IMC. actions_with_keys: list of (InputAction, key_name)."""
    if not imc or not hasattr(imc, "map_key"):
        return
    for ia, key_name in actions_with_keys:
        if not ia:
            continue
        key_obj = _get_key(key_name)
        if key_obj is None:
            _log("Could not resolve key '" + key_name + "'")
            continue
        try:
            imc.map_key(ia, key_obj)
            _log("Mapped " + key_name + " -> " + (ia.get_name() if ia else ""))
        except Exception as e:
            _log("map_key failed for " + key_name + ": " + str(e))


def _assign_abilities_to_character():
    """Set BP_HomeWorldCharacter DefaultAbilities and the three ability-class + input-action properties."""
    if not unreal.EditorAssetLibrary.does_asset_exist(CHAR_BP_PATH):
        _log("BP_HomeWorldCharacter not found at " + CHAR_BP_PATH + ". Run setup_character_blueprint.py first.")
        return
    bp = unreal.load_asset(CHAR_BP_PATH)
    if not bp:
        return
    gen_class = getattr(bp, "generated_class", lambda: None)()
    if not gen_class:
        gen_class = bp.get_editor_property("generated_class")
    if not gen_class:
        _log("Could not get generated class from " + CHAR_BP_PATH)
        return
    cdo = unreal.get_default_object(gen_class)
    if not cdo:
        _log("Could not get CDO for " + CHAR_BP_PATH)
        return

    num_abilities = len(GA_NAMES)
    ability_classes = []
    for ga_name in GA_NAMES:
        path = ABILITIES_PATH + "/" + ga_name + "." + ga_name
        if unreal.EditorAssetLibrary.does_asset_exist(path):
            asset = unreal.load_asset(path)
            if asset and hasattr(asset, "generated_class"):
                cls = asset.generated_class()
                if not cls:
                    cls = asset.get_editor_property("generated_class")
                if cls:
                    ability_classes.append(cls)
                else:
                    ability_classes.append(None)
            else:
                ability_classes.append(None)
        else:
            ability_classes.append(None)

    ab_props_snake = ["primary_attack_ability_class", "dodge_ability_class", "interact_ability_class", "place_ability_class"]
    ab_props_pascal = ["PrimaryAttackAbilityClass", "DodgeAbilityClass", "InteractAbilityClass", "PlaceAbilityClass"]
    if len(ability_classes) >= num_abilities and all(ability_classes):
        for prop_name in ("default_abilities", "DefaultAbilities"):
            try:
                cdo.set_editor_property(prop_name, ability_classes)
                _log("Set DefaultAbilities on BP_HomeWorldCharacter")
                break
            except Exception:
                continue
        for i in range(num_abilities):
            for prop in (ab_props_snake[i], ab_props_pascal[i]):
                try:
                    cdo.set_editor_property(prop, ability_classes[i])
                    _log("Set ability class " + str(i) + " on BP_HomeWorldCharacter")
                    break
                except Exception:
                    continue
    else:
        _log("Not all ability Blueprints found; assign Default Abilities and ability classes in Editor.")

    input_actions = []
    for ia_name in IA_ABILITY_NAMES:
        path = INPUT_PATH + "/" + ia_name
        if unreal.EditorAssetLibrary.does_asset_exist(path):
            input_actions.append(unreal.load_asset(path))
        else:
            input_actions.append(None)
    ia_props_snake = ["primary_attack_action", "dodge_action", "interact_action", "place_action"]
    ia_props_pascal = ["PrimaryAttackAction", "DodgeAction", "InteractAction", "PlaceAction"]
    if len(input_actions) >= num_abilities:
        for i in range(num_abilities):
            if not input_actions[i]:
                continue
            for prop in (ia_props_snake[i], ia_props_pascal[i]):
                try:
                    cdo.set_editor_property(prop, input_actions[i])
                    _log("Set input action " + str(i) + " on BP_HomeWorldCharacter")
                    break
                except Exception:
                    continue

    try:
        unreal.EditorAssetLibrary.save_loaded_asset(bp)
    except Exception:
        pass


def main():
    _log("Setting up GAS survivor abilities...")
    parent = _get_parent_class("GA_PrimaryAttack")
    if not parent:
        _log("Abort: HomeWorldGameplayAbility not found.")
        return

    for name in GA_NAMES:
        _create_ability_blueprint(name)

    actions = []
    for ia_name in IA_ABILITY_NAMES:
        actions.append(_create_input_action(ia_name, "Boolean"))

    imc_path = INPUT_PATH + "/" + IMC_NAME
    if unreal.EditorAssetLibrary.does_asset_exist(imc_path):
        imc = unreal.load_asset(imc_path)
        if imc and len(actions) >= len(GA_NAMES) and len(IA_KEYS) >= len(GA_NAMES):
            _add_ability_mappings_to_imc(imc, list(zip(actions, IA_KEYS)))
            unreal.EditorAssetLibrary.save_loaded_asset(imc)
            _log("Added ability key mappings to " + IMC_NAME)
    else:
        _log("IMC_Default not found. Run setup_enhanced_input.py first.")

    _assign_abilities_to_character()
    _log("Done. Open BP_HomeWorldCharacter to confirm Default Abilities and input; open each GA_* to add cost/effects (GameplayEffect, etc.).")


if __name__ == "__main__":
    main()

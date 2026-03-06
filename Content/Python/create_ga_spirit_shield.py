# create_ga_spirit_shield.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP.
# Creates GA_SpiritShield (Blueprint, parent HomeWorldSpiritShieldAbility), adds to BP_HomeWorldCharacter
# Default Abilities, creates IA_SpiritShield and maps R key in IMC_Default, sets SpiritShieldAbilityClass
# and SpiritShieldAction on BP_HomeWorldCharacter. Idempotent.
# In PIE at night: press R or run hw.SpiritShield to trigger; HUD shows "SpiritShield: ready" or "N.Xs".

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

ABILITIES_PATH = "/Game/HomeWorld/Abilities"
INPUT_PATH = "/Game/HomeWorld/Input"
CHAR_BP_PATH = "/Game/HomeWorld/Characters/BP_HomeWorldCharacter"
GA_NAME = "GA_SpiritShield"
PARENT_CLASS_NAME = "HomeWorldSpiritShieldAbility"
IA_NAME = "IA_SpiritShield"
IMC_NAME = "IMC_Default"
SPIRIT_SHIELD_KEY = "R"


def _log(msg):
    unreal.log("GA_SpiritShield: " + str(msg))
    print("GA_SpiritShield: " + str(msg))


def _get_key(key_name):
    keys_cls = getattr(unreal, "Keys", None)
    if keys_cls:
        attr = key_name.replace(" ", "_")
        k = getattr(keys_cls, attr, None)
        if k is not None and not callable(k):
            return k
    key_cls = getattr(unreal, "Key", None)
    name_cls = getattr(unreal, "Name", None)
    if key_cls and name_cls:
        try:
            key_obj = key_cls()
            key_obj.set_editor_property("key_name", name_cls(key_name))
            return key_obj
        except Exception:
            pass
    return None


def main():
    _log("Start.")
    parent_class = None
    try:
        parent_class = unreal.load_class(None, "/Script/HomeWorld." + PARENT_CLASS_NAME)
    except Exception:
        pass
    if not parent_class:
        _log("HomeWorldSpiritShieldAbility not found. Build the project and restart Editor.")
        return

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory_class = getattr(unreal, "BlueprintFactory", None)
    if not factory_class:
        _log("BlueprintFactory not found.")
        return

    factory = factory_class()
    factory.set_editor_property("parent_class", parent_class)
    asset_path = ABILITIES_PATH + "/" + GA_NAME

    if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        _log("Reusing " + asset_path)
        ga_asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    else:
        ga_asset = asset_tools.create_asset(GA_NAME, ABILITIES_PATH, None, factory)
        if not ga_asset:
            _log("create_asset returned None.")
            return
        unreal.EditorAssetLibrary.save_loaded_asset(ga_asset)
        _log("Created " + asset_path)

    bp = unreal.EditorAssetLibrary.load_asset(CHAR_BP_PATH)
    if not bp:
        _log("BP_HomeWorldCharacter not found. Add GA_SpiritShield to Default Abilities and bind key manually.")
        _log("Done.")
        return

    cdo = unreal.get_default_object(bp)
    if not cdo:
        _log("Could not get CDO. Add GA_SpiritShield to Default Abilities manually.")
        _log("Done.")
        return

    # Add GA_SpiritShield to Default Abilities
    for prop in ("default_abilities", "DefaultAbilities"):
        try:
            arr = cdo.get_editor_property(prop)
            if arr is None:
                arr = []
            if ga_asset not in arr:
                arr.append(ga_asset)
                cdo.set_editor_property(prop, arr)
                unreal.EditorAssetLibrary.save_loaded_asset(bp)
                _log("Added GA_SpiritShield to BP_HomeWorldCharacter Default Abilities.")
            else:
                _log("GA_SpiritShield already in Default Abilities.")
            break
        except Exception:
            continue
    else:
        _log("Could not set DefaultAbilities. Add GA_SpiritShield manually in BP_HomeWorldCharacter.")

    # Set SpiritShieldAbilityClass on character to GA_SpiritShield's generated class
    ga_class = None
    if hasattr(ga_asset, "generated_class"):
        ga_class = ga_asset.generated_class()
    if not ga_class and hasattr(ga_asset, "get_editor_property"):
        ga_class = ga_asset.get_editor_property("generated_class")
    if ga_class:
        for prop in ("SpiritShieldAbilityClass", "spirit_shield_ability_class"):
            try:
                cdo.set_editor_property(prop, ga_class)
                _log("Set SpiritShieldAbilityClass on BP_HomeWorldCharacter.")
                break
            except Exception:
                continue
    else:
        _log("Could not get generated class from GA_SpiritShield; set SpiritShieldAbilityClass in Blueprint.")

    # Create IA_SpiritShield if missing
    ia_path = INPUT_PATH + "/" + IA_NAME
    if unreal.EditorAssetLibrary.does_asset_exist(ia_path):
        ia_asset = unreal.load_asset(ia_path)
        _log("Reusing " + ia_path)
    else:
        for factory_name in ("InputActionFactory", "InputAction_Factory"):
            cls = getattr(unreal, factory_name, None)
            if cls:
                factory_ia = cls()
                ia_asset = asset_tools.create_asset(IA_NAME, INPUT_PATH, None, factory_ia)
                if ia_asset:
                    unreal.EditorAssetLibrary.save_loaded_asset(ia_asset)
                    _log("Created " + ia_path)
                break
        else:
            ia_asset = None
            _log("No InputAction factory. Create IA_SpiritShield manually.")
    if ia_asset:
        for prop in ("SpiritShieldAction", "spirit_shield_action"):
            try:
                cdo.set_editor_property(prop, ia_asset)
                _log("Set SpiritShieldAction on BP_HomeWorldCharacter.")
                break
            except Exception:
                continue

    # Add R -> IA_SpiritShield to IMC_Default
    imc_path = INPUT_PATH + "/" + IMC_NAME
    if unreal.EditorAssetLibrary.does_asset_exist(imc_path) and ia_asset and hasattr(unreal.load_asset(imc_path), "map_key"):
        imc = unreal.load_asset(imc_path)
        key_obj = _get_key(SPIRIT_SHIELD_KEY)
        if key_obj:
            try:
                if hasattr(imc, "unmap_all_keys_from_action") and ia_asset:
                    imc.unmap_all_keys_from_action(ia_asset)
            except Exception:
                pass
            try:
                imc.map_key(ia_asset, key_obj)
                unreal.EditorAssetLibrary.save_loaded_asset(imc)
                _log("Mapped R -> IA_SpiritShield in IMC_Default.")
            except Exception as e:
                _log("map_key IA_SpiritShield failed: " + str(e))
        else:
            _log("Could not resolve key " + SPIRIT_SHIELD_KEY + "; bind IA_SpiritShield in Editor.")
    else:
        _log("IMC_Default not found or IA_SpiritShield missing; run setup_enhanced_input.py first or bind key in Editor.")

    try:
        unreal.EditorAssetLibrary.save_loaded_asset(bp)
    except Exception:
        pass

    _log("Done. In PIE: hw.TimeOfDay.Phase 2 then press R or hw.SpiritShield (night-only). HUD shows SpiritShield cooldown.")


if __name__ == "__main__":
    main()

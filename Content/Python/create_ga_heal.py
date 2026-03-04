# create_ga_heal.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP.
# Creates GA_Heal (Blueprint, parent HomeWorldHealAbility) and adds it to BP_HomeWorldCharacter DefaultAbilities.
# Idempotent. No input action; trigger via TryActivateAbilityByClass or add IA_Heal later for testing.

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

ABILITIES_PATH = "/Game/HomeWorld/Abilities"
CHAR_BP_PATH = "/Game/HomeWorld/Characters/BP_HomeWorldCharacter"
GA_NAME = "GA_Heal"
PARENT_CLASS_NAME = "HomeWorldHealAbility"


def _log(msg):
    unreal.log("GA_Heal: " + str(msg))
    print("GA_Heal: " + str(msg))


def main():
    _log("Start.")
    asset_path = ABILITIES_PATH + "/" + GA_NAME

    parent_class = None
    try:
        parent_class = unreal.load_class(None, "/Script/HomeWorld." + PARENT_CLASS_NAME)
    except Exception:
        pass
    if not parent_class:
        _log("HomeWorldHealAbility not found. Build the project and restart Editor.")
        return

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory_class = getattr(unreal, "BlueprintFactory", None)
    if not factory_class:
        _log("BlueprintFactory not found.")
        return

    factory = factory_class()
    factory.set_editor_property("parent_class", parent_class)

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
        _log("BP_HomeWorldCharacter not found. Add GA_Heal to Default Abilities manually.")
        _log("Done.")
        return

    cdo = unreal.get_default_object(bp)
    if not cdo:
        _log("Could not get CDO. Add GA_Heal to Default Abilities manually.")
        _log("Done.")
        return

    for prop in ("default_abilities", "DefaultAbilities"):
        try:
            arr = cdo.get_editor_property(prop)
            if arr is None:
                arr = []
            if ga_asset not in arr:
                arr.append(ga_asset)
                cdo.set_editor_property(prop, arr)
                unreal.EditorAssetLibrary.save_loaded_asset(bp)
                _log("Added GA_Heal to BP_HomeWorldCharacter Default Abilities.")
            else:
                _log("GA_Heal already in Default Abilities.")
            break
        except Exception:
            continue
    else:
        _log("Could not set DefaultAbilities. Add GA_Heal manually in BP_HomeWorldCharacter.")

    _log("Done. Trigger in C++ with AbilitySystemComponent->TryActivateAbilityByClass(GA_Heal class).")


if __name__ == "__main__":
    main()

# reparent_ga_interact_to_cpp.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP.
# Reparents GA_Interact Blueprint to HomeWorldInteractAbility (C++) so harvest
# runs in C++ and no Blueprint graph wiring is needed. Idempotent.

import sys
try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

GA_INTERACT_PATH = "/Game/HomeWorld/Abilities/GA_Interact"


def _log(msg):
    unreal.log("Reparent GA_Interact: " + str(msg))
    print("Reparent GA_Interact: " + str(msg))


def _get_interact_ability_class():
    """Return UHomeWorldInteractAbility class."""
    try:
        cls = getattr(unreal, "HomeWorldInteractAbility", None)
        if cls and hasattr(cls, "static_class"):
            return cls.static_class()
    except Exception:
        pass
    try:
        return unreal.load_class(None, "/Script/HomeWorld.HomeWorldInteractAbility")
    except Exception:
        pass
    return None


def main():
    if not unreal.EditorAssetLibrary.does_asset_exist(GA_INTERACT_PATH):
        _log("GA_Interact not found at " + GA_INTERACT_PATH + ". Run setup_gas_abilities.py first.")
        return False

    parent_class = _get_interact_ability_class()
    if not parent_class:
        _log("HomeWorldInteractAbility not found. Build C++ (Build-HomeWorld.bat) and re-run.")
        return False

    bp = unreal.load_asset(GA_INTERACT_PATH)
    if not bp:
        _log("Failed to load " + GA_INTERACT_PATH)
        return False

    try:
        current = bp.get_editor_property("parent_class")
        current_name = current.get_name() if current else ""
        target_name = parent_class.get_name()
        if current_name == target_name:
            _log("GA_Interact already parented to " + target_name + ". Done.")
            return True
    except Exception:
        pass

    reparent = getattr(unreal, "BlueprintEditorLibrary", None)
    if not reparent or not hasattr(reparent, "reparent_blueprint"):
        _log("BlueprintEditorLibrary.reparent_blueprint not available. Reparent manually: GA_Interact -> Class Settings -> Parent Class -> Home World Interact Ability.")
        return False

    try:
        reparent.reparent_blueprint(bp, parent_class)
        _log("Reparented GA_Interact to " + parent_class.get_name() + ".")
        unreal.EditorAssetLibrary.save_loaded_asset(bp)
        return True
    except Exception as e:
        _log("Reparent failed: " + str(e) + ". Reparent manually: GA_Interact -> Class Settings -> Parent Class -> Home World Interact Ability.")
        return False


if __name__ == "__main__":
    main()

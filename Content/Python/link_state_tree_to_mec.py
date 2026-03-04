# link_state_tree_to_mec.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Creates MEC_FamilyGatherer if missing, then links ST_FamilyGatherer to it (sets State Tree on the MassStateTree trait).
# Idempotent. Requires ST_FamilyGatherer to exist. Run after creating ST_FamilyGatherer in the Editor.

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

MEC_PATH = "/Game/HomeWorld/Mass/MEC_FamilyGatherer"
ST_PATH = "/Game/HomeWorld/AI/ST_FamilyGatherer"


def _log(msg):
    unreal.log("Link StateTree to MEC: " + str(msg))
    print("Link StateTree to MEC: " + str(msg))


def main():
    _log("Start.")
    if not unreal.EditorAssetLibrary.does_asset_exist(MEC_PATH):
        _log("MEC_FamilyGatherer not found; creating it.")
        try:
            import create_mec_family_gatherer
            create_mec_family_gatherer.main()
        except Exception as e:
            _log("create_mec_family_gatherer failed: " + str(e))
        if not unreal.EditorAssetLibrary.does_asset_exist(MEC_PATH):
            _log("MEC still missing. Create MEC_FamilyGatherer manually (Content -> HomeWorld -> Mass, add traits, set State Tree), then run this script again.")
            return
    if not unreal.EditorAssetLibrary.does_asset_exist(ST_PATH):
        _log("ST_FamilyGatherer not found at " + ST_PATH + ". Create it first (State Tree in AI folder).")
        return

    mec = unreal.EditorAssetLibrary.load_asset(MEC_PATH)
    st = unreal.EditorAssetLibrary.load_asset(ST_PATH)
    if not mec or not st:
        _log("Failed to load MEC or State Tree.")
        return

    # Try to set State Tree reference on MEC. Property names may vary by UE version.
    set_attempts = [
        "state_tree",
        "StateTree",
        "state_tree_asset",
        "StateTreeAsset",
        "mass_state_tree",
        "MassStateTree",
    ]
    for prop in set_attempts:
        try:
            mec.set_editor_property(prop, st)
            unreal.EditorAssetLibrary.save_loaded_asset(mec)
            _log("Set " + prop + " on MEC to ST_FamilyGatherer. Saved.")
            _log("Done.")
            return
        except Exception:
            pass

    # Try via Config or trait array (MEC may store traits in a config struct).
    for config_prop in ("config", "Config", "trait_configurations", "TraitConfigurations", "traits", "Traits"):
        try:
            config = mec.get_editor_property(config_prop)
            if config is not None and hasattr(config, "set_editor_property"):
                for prop in set_attempts:
                    try:
                        config.set_editor_property(prop, st)
                        unreal.EditorAssetLibrary.save_loaded_asset(mec)
                        _log("Set " + prop + " on MEC." + config_prop + " to ST_FamilyGatherer. Saved.")
                        _log("Done.")
                        return
                    except Exception:
                        pass
            if isinstance(config, (list, tuple)):
                for i, trait_inst in enumerate(config):
                    if hasattr(trait_inst, "set_editor_property"):
                        for prop in set_attempts:
                            try:
                                trait_inst.set_editor_property(prop, st)
                                unreal.EditorAssetLibrary.save_loaded_asset(mec)
                                _log("Set " + prop + " on trait " + str(i) + ". Saved.")
                                _log("Done.")
                                return
                            except Exception:
                                pass
        except Exception:
            pass

    _log("Could not set State Tree via script. Set it manually: Open MEC_FamilyGatherer -> Details -> StateTree trait -> State Tree = ST_FamilyGatherer.")


if __name__ == "__main__":
    main()

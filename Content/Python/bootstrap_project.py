# bootstrap_project.py
# Run from Unreal Editor: Tools -> Execute Python Script.
# One-click project setup: creates all Enhanced Input assets, character Blueprint,
# project settings, and level preparation in order.
# Re-runnable: each sub-script deletes existing assets before recreating.
#
# Usage:
#   1. Open the project in Unreal Editor
#   2. Open the Main level (Content/HomeWorld/Maps/Main)
#   3. Tools -> Execute Python Script -> Content/Python/bootstrap_project.py
#
# Optional: set skeletal mesh and Animation Blueprint paths in
# Content/Python/character_blueprint_config.json before running.

import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)


def _log(msg):
    unreal.log("Bootstrap: " + str(msg))
    print("Bootstrap: " + str(msg))


def main(run_pcg=True):
    _log("=== HomeWorld project bootstrap ===")

    # Step 1: Enhanced Input assets (IA_Move, IA_Look, IMC_Default)
    _log("--- Step 1/4: Enhanced Input ---")
    try:
        import setup_enhanced_input
        setup_enhanced_input.main()
    except Exception as e:
        _log("Enhanced Input setup error: " + str(e))

    # Step 2: Character Blueprint (BP_HomeWorldCharacter)
    _log("--- Step 2/4: Character Blueprint ---")
    try:
        import setup_character_blueprint
        setup_character_blueprint.main()
    except Exception as e:
        _log("Character Blueprint setup error: " + str(e))

    # Step 3: Project settings (game mode, default map, pawn class)
    _log("--- Step 3/4: Project Settings ---")
    try:
        import setup_project_settings
        setup_project_settings.main()
    except Exception as e:
        _log("Project settings error: " + str(e))

    # Step 4: Level setup (PlayerStart, optional PCG)
    _log("--- Step 4/4: Level Setup ---")
    try:
        import setup_level
        setup_level.main(run_pcg=run_pcg)
    except Exception as e:
        _log("Level setup error: " + str(e))

    _log("=== Bootstrap complete ===")
    _log("Next steps:")
    _log("  - If skeletal mesh/AnimBP are not set: add paths to Content/Python/character_blueprint_config.json and re-run, or assign in Editor on BP_HomeWorldCharacter.")
    _log("  - Verify in Editor: Project Settings > Maps & Modes shows HomeWorldGameMode and Main map.")
    _log("  - Play In Editor (PIE) to test movement and camera.")
    _log("  - Animation Blueprint state machine must be built manually in Editor (Python cannot create AnimGraph nodes).")


if __name__ == "__main__":
    main(run_pcg=False)

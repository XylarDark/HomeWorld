# bootstrap_project.py
# Run from Unreal Editor: Tools -> Execute Python Script.
# One-click project setup: creates all Enhanced Input assets, character Blueprint,
# project settings, and level preparation in order.
# Idempotent: each sub-script checks for existing assets and skips/reuses them.
#
# Usage:
#   1. Open the project in Unreal Editor
#   2. Open the Main level (Content/HomeWorld/Maps/Main)
#   3. Tools -> Execute Python Script -> Content/Python/bootstrap_project.py
#
# Optional: set skeletal mesh and Animation Blueprint paths in
# Content/Python/character_blueprint_config.json before running.

import importlib
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
    _log("--- Step 1/5: Enhanced Input ---")
    try:
        import setup_enhanced_input
        importlib.reload(setup_enhanced_input)
        setup_enhanced_input.main()
    except Exception as e:
        _log("Enhanced Input setup error: " + str(e))

    # Step 2: Animation Blueprint (ABP_HomeWorldCharacter)
    _log("--- Step 2/5: Animation Blueprint ---")
    try:
        import setup_animation_blueprint
        importlib.reload(setup_animation_blueprint)
        setup_animation_blueprint.main()
    except Exception as e:
        _log("Animation Blueprint setup error: " + str(e))

    # Step 3: Character Blueprint (BP_HomeWorldCharacter)
    _log("--- Step 3/5: Character Blueprint ---")
    try:
        import setup_character_blueprint
        importlib.reload(setup_character_blueprint)
        setup_character_blueprint.main()
    except Exception as e:
        _log("Character Blueprint setup error: " + str(e))

    # Step 4: Project settings (game mode, default map, pawn class)
    _log("--- Step 4/5: Project Settings ---")
    try:
        import setup_project_settings
        importlib.reload(setup_project_settings)
        setup_project_settings.main()
    except Exception as e:
        _log("Project settings error: " + str(e))

    # Step 5: Level setup (PlayerStart, optional PCG)
    _log("--- Step 5/5: Level Setup ---")
    try:
        import setup_level
        importlib.reload(setup_level)
        setup_level.main(run_pcg=run_pcg)
    except Exception as e:
        _log("Level setup error: " + str(e))

    _log("=== Bootstrap complete ===")
    _log("Next steps:")
    _log("  - If skeletal mesh/AnimBP are not set: add paths to Content/Python/character_blueprint_config.json and re-run, or assign in Editor on BP_HomeWorldCharacter.")
    _log("  - Verify in Editor: Project Settings > Maps & Modes shows HomeWorldGameMode and Main map.")
    _log("  - Play In Editor (PIE) to test movement and camera.")
    _log("  - Animation Blueprint state machine must be built manually in Editor (Python cannot create AnimGraph nodes).")
    _log("  - For PCG trees/rocks: run create_homestead_from_scratch.py (recreates Homestead and sets PCG to landscape size) or run setup_level with run_pcg=True; then set Get Landscape Data (By Tag + PCG_Landscape), mesh lists on spawners, click Generate. See docs/PCG_SETUP.md.")


if __name__ == "__main__":
    main(run_pcg=False)

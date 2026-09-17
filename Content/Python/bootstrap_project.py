# bootstrap_project.py
# Run from Unreal Editor: Tools -> Execute Python Script.
# One-click project setup: Enhanced Input, character Blueprint, project settings,
# then VS_MVP slice import (Docs/04) + markers per WAVE E canon.
# Idempotent: each sub-script checks for existing assets and skips/reuses them.
#
# Usage:
#   1. Open the project in Unreal Editor
#   2. Tools -> Execute Python Script -> Content/Python/bootstrap_project.py
#
# WAVE F removed DemoMap/Homestead map builders and gui_automation. VS_MVP slice only.
# See Docs/08_AUDIT_SIGN_OFF.md and Docs/08d_CONTENT_CANON.md §8.
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


def _run_slice_setup():
    """Docs/04 first pass: batch FBX import + VS_MVP markers/MPC (WAVE E primary)."""
    _log("--- Step 5a/5: Docs/04 batch import ---")
    try:
        import batch_import_asset_creation
        importlib.reload(batch_import_asset_creation)
        batch_import_asset_creation.main()
    except Exception as e:
        _log("Batch import error (non-fatal if no FBX in AssetCreation/Exports): " + str(e))

    _log("--- Step 5b/5: VS_MVP markers + NightMix MPC ---")
    try:
        import place_vs_mvp_markers
        importlib.reload(place_vs_mvp_markers)
        place_vs_mvp_markers.main()
    except Exception as e:
        _log("place_vs_mvp_markers error: " + str(e))


def main(run_slice=True):
    _log("=== HomeWorld project bootstrap (VS_MVP slice primary) ===")

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

    # Step 5: VS_MVP slice (primary)
    if run_slice:
        _run_slice_setup()

    _log("=== Bootstrap complete ===")
    _log("Next steps:")
    _log("  - Primary slice map: /Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers — see Maps/VS_MVP/README.md and Docs/04_UE_HANDOFF_NOTES.md")
    _log("  - If skeletal mesh/AnimBP are not set: add paths to Content/Python/character_blueprint_config.json and re-run, or assign in Editor on BP_HomeWorldCharacter.")
    _log("  - Verify in Editor: Project Settings > Maps & Modes shows HomeWorldGameMode.")
    _log("  - Play In Editor (PIE) on VS_MVP markers level to test movement; NightMix driven via TimeOfDaySubsystem when MPC exists.")
    _log("  - Animation Blueprint state machine must be built manually in Editor (Python cannot create AnimGraph nodes).")


if __name__ == "__main__":
    main(run_slice=True)

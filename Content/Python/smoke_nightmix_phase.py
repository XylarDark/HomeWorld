# smoke_nightmix_phase.py
# NP-C bonus: NightMix phase table smoke — ensures MPC exists and logs UE 5.7 MaterialLibrary path.
# Run in Editor after place_vs_mvp_markers.py. Does not require PIE.

from __future__ import annotations

import importlib
import sys

try:
    import unreal
except ImportError:
    print("smoke_nightmix_phase: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "smoke_nightmix_phase:"
MPC_PATH = "/Game/HomeWorld/Materials/MPC_HomeWorld_Time"
PHASE_VALUES = (
    (0, "Day", 0.0),
    (1, "Dusk", 0.35),
    (2, "Night", 0.85),
    (3, "Dawn", 0.15),
)


def _log(msg):
    unreal.log(PREFIX + " " + str(msg))
    print(PREFIX, msg)


def main():
    _log("NightMix phase smoke (NP-C residual from NP-B)")

    try:
        import place_vs_mvp_markers
        importlib.reload(place_vs_mvp_markers)
        mpc = place_vs_mvp_markers.create_nightmix_mpc()
    except Exception as exc:
        _log("MPC ensure failed: %s" % exc)
        mpc = unreal.EditorAssetLibrary.load_asset(MPC_PATH)

    if not mpc:
        _log("FAIL: MPC missing at %s — run place_vs_mvp_markers.py" % MPC_PATH)
        return 1

    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        _log("FAIL: no editor world")
        return 1

    material_lib = unreal.KismetMaterialLibrary
    if not material_lib:
        _log("FAIL: unreal.KismetMaterialLibrary unavailable")
        return 1

    ok = 0
    for phase_int, phase_name, expected in PHASE_VALUES:
        try:
            material_lib.set_scalar_parameter_value(
                world,
                mpc,
                unreal.Name("NightMix"),
                float(expected),
            )
            _log("OK phase=%s NightMix=%.2f (MaterialLibrary.set_scalar_parameter_value)" % (phase_name, expected))
            ok += 1
        except Exception as exc:
            _log("FAIL phase=%s: %s" % (phase_name, exc))

    _log("Smoke complete: %d/%d phases written to MPC" % (ok, len(PHASE_VALUES)))
    _log("Runtime: hw.TimeOfDay.Phase 0|1|2|3 → C++ SetPhase → ApplyNightMixForPhase")
    return 0 if ok == len(PHASE_VALUES) else 1


if __name__ == "__main__":
    code = main()
    if code != 0:
        unreal.log_error(PREFIX + " finished with code %s" % code)

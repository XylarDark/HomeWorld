# wire_nightmix_mpc_note.py
# WAVE E: documents NightMix → MPC_HomeWorld_Time wiring for slice masters.
# Run in Editor after place_vs_mvp_markers.py; idempotent log-only + MPC ensure.
#
# Runtime driver: UHomeWorldTimeOfDaySubsystem::SetPhase → ApplyNightMixForPhase
# (Day=0, Dusk=0.35, Night=0.85, Dawn=0.15). Masters consume NightMix per Docs/02_MATERIAL_SHEET.md.

from __future__ import annotations

import importlib
import sys

try:
    import unreal
except ImportError:
    print("wire_nightmix_mpc_note: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "wire_nightmix_mpc_note:"
MPC_PATH = "/Game/HomeWorld/Materials/MPC_HomeWorld_Time"

PHASE_NIGHTMIX = (
    ("Day", 0.0),
    ("Dusk", 0.35),
    ("Night", 0.85),
    ("Dawn", 0.15),
)


def _log(msg):
    unreal.log(PREFIX + " " + str(msg))
    print(PREFIX, msg)


def main():
    _log("NightMix wiring (WAVE E slice)")
    _log("Canon: Docs/02_MATERIAL_SHEET.md §1; Lib/06_Materials_Master/NIGHTMIX_DEMO.md")
    _log("MPC asset: %s — scalar parameter NightMix" % MPC_PATH)
    _log("C++ driver: TimeOfDaySubsystem SetPhase → ApplyNightMixForPhase → SetNightMixScalar")
    for phase, value in PHASE_NIGHTMIX:
        _log("  Phase %s → NightMix=%.2f" % (phase, value))
    _log("Masters M_* under /Game/HomeWorld/Materials/Masters/ — use create_master_materials_stub.py for empty shells")
    _log("FALLBACK FLIGHT: CRUMB_* markers from place_vs_mvp_markers; glide/portal BP wiring DEFERRED (Editor dress)")

    try:
        import place_vs_mvp_markers
        importlib.reload(place_vs_mvp_markers)
        mpc = place_vs_mvp_markers.create_nightmix_mpc()
        if mpc:
            _log("MPC ensure: OK (%s)" % MPC_PATH)
        else:
            _log("MPC ensure: failed — set NightMix scalar manually in Editor")
    except Exception as exc:
        _log("MPC ensure skipped: %s" % exc)

    return 0


if __name__ == "__main__":
    main()

"""PA-E homestead capture diagnostic — DESKTOP (MCP execute_python_script).

Lead prove loop steps 1–2 without running MRQ/AL capture:
  (1) Confirm homestead dress actors are in the loaded level.
  (2) Dump camera location vs homestead/framing bounds centroids + forward alignment.

Writes: Saved/pa_e_homestead_capture_diagnostic.json

Near-black PNGs from capture scripts are **prove-loop in progress**, not a closed FAIL.
"""
from __future__ import annotations

try:
    import unreal
except ImportError:
    print("pa_e_homestead_capture_diagnostic: Run inside Unreal Editor.")
    raise

import pa_e_shotlist_common as common

PREFIX = "pa_e_homestead_capture_diagnostic:"


def main() -> None:
    common.log(PREFIX, "started")
    level_ok = common.load_level(PREFIX)
    gate = common.arrange_pa_e_shotlist(PREFIX, level_loaded=level_ok, require_mrq=False)
    payload = common.write_homestead_capture_diagnostic(
        PREFIX,
        level_loaded=level_ok,
        homestead_night_environment=gate.get("lighting"),
        arrange_gate=gate,
    )
    common.log(
        PREFIX,
        "done",
        {
            "path": payload.get("written_path") or common.homestead_diagnostic_path(),
            "arrange_ready": gate.get("ready"),
            "shot1_inventory_ok": (
                payload.get("shots", [{}])[0].get("inventory", {}).get("inventory_ok")
                if payload.get("shots")
                else None
            ),
        },
    )


if __name__ == "__main__":
    main()

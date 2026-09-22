"""NF2-A: document / drive dusk↔dawn form-swap soft feedback evidence.

In PIE (or game), run:
  hw.TimeOfDay.SetPhase 1   # Dusk → spirit + NF2 soft_feedback
  hw.TimeOfDay.SetPhase 3   # Dawn → body + NF2 soft_feedback
  hw.TimeOfDay.SetPhase 2   # Night
  hw.TimeOfDay.SetPhase 0   # Day

Expect LogTemp lines:
  FORM: spirit|body form (phase=...)
  NF2: soft_feedback form=... phase=... sound=none|yes particles=none|yes

Writes Saved/nf2_a_form_swap_evidence.json (instructions + expected greps).
Idempotent: safe to re-run outside Editor (writes JSON only).
Harness P3 exempt: PIE log-grep instructions only — no Editor capture / Arrange.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone

OUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "Saved",
    "nf2_a_form_swap_evidence.json",
)


def main() -> None:
    result = {
        "ok": True,
        "phase": "NF2-A",
        "track": "Docs/27 Night Feel Build",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "feel_target": "safe home above a living world — soft handmade dusk/dawn form swap",
        "pie_commands": [
            "hw.TimeOfDay.SetPhase 1",
            "hw.TimeOfDay.SetPhase 3",
            "hw.TimeOfDay.SetPhase 2",
            "hw.TimeOfDay.SetPhase 0",
        ],
        "expected_log_greps": [
            "FORM:",
            "NF2: soft_feedback",
        ],
        "notes": [
            "Soft glow pulse is C++ PointLight (warm amber body / cool moon spirit) — no .uasset required.",
            "Assign SoftFormSwapSound / SoftFormSwapParticles on BP_HomeWorldCharacter defaults for audio/VFX sting (NF2-D).",
            "Run commands in PIE; grep Saved/Logs/HomeWorld.log or Editor Output Log.",
        ],
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print("Wrote", OUT)


if __name__ == "__main__":
    main()

"""Load L_VS_MVP_Markers then re-run night evidence (VNP-N2).

Runs conductor night preflight + arrange_pa_e_shotlist before vnp_night_tune_and_evidence.
"""
from __future__ import annotations

import importlib

import unreal

import pa_e_shotlist_common as common

LEVEL = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
PREFIX = "VNP-LOAD:"


def main() -> None:
    importlib.reload(common)
    ok = bool(unreal.EditorLoadingAndSavingUtils.load_map(LEVEL))
    unreal.log("VNP load map %s -> %s" % (LEVEL, ok))
    common.conductor_night_evidence_preflight(PREFIX)
    common.arrange_pa_e_shotlist(PREFIX, level_loaded=ok, require_mrq=False)
    import vnp_night_tune_and_evidence as ev

    importlib.reload(ev)
    ev.main()


if __name__ == "__main__":
    main()

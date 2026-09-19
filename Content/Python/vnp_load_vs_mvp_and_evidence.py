"""Load L_VS_MVP_Markers then re-run night evidence (VNP-N2)."""
from __future__ import annotations

import unreal

LEVEL = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"


def main() -> None:
    ok = unreal.EditorLoadingAndSavingUtils.load_map(LEVEL)
    unreal.log("VNP load map %s -> %s" % (LEVEL, ok))
    # Import and run evidence after load
    import importlib
    import vnp_night_tune_and_evidence as ev

    importlib.reload(ev)
    ev.main()


if __name__ == "__main__":
    main()

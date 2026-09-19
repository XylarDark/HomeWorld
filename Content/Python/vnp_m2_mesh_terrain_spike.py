"""VNP-M2: Mesh Terrain sandbox spike note (no Landscape replace).

Loads sandbox map if present, writes KEEP-LOCAL spike evidence JSON.
Does not sculpt Mesh Terrain via Python (Editor Mode). Records policy.
Writes Saved/vnp_m2_mesh_terrain_spike.json
"""
from __future__ import annotations

import json

import unreal

OUT = unreal.Paths.project_saved_dir() + "vnp_m2_mesh_terrain_spike.json"
SANDBOX = "/Game/HomeWorld/Maps/Sandbox/L_U58F_MeshTerrain"


def main() -> None:
    exists = unreal.EditorAssetLibrary.does_asset_exist(SANDBOX)
    loaded = False
    if exists:
        try:
            loaded = bool(unreal.EditorLoadingAndSavingUtils.load_map(SANDBOX))
        except Exception as e:
            unreal.log_warning("VNP-M2 load: %s" % e)

    result = {
        "ok": exists,
        "phase": "VNP-M2",
        "sandbox": SANDBOX,
        "sandbox_exists": exists,
        "loaded": loaded,
        "sculpt": "KEEP-LOCAL Editor Mesh Terrain Mode — not automated in Python",
        "vs_mvp_landscape_replaced": False,
        "policy": "No VS_MVP Landscape replace without AD + WLD + APPROVE U58F-G",
        "notes": [
            "Sandbox map created in M1.",
            "Cliff/overhang sculpt is Editor Mode KEEP-LOCAL; evidence is map existence + this stamp.",
            "5.8.2: if OOM, apply Mesh Terrain memory budget CVars from hotfix notes.",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    unreal.log("VNP-M2 spike wrote %s" % OUT)


if __name__ == "__main__":
    main()

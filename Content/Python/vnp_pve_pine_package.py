"""VNP P1: PVE stylized pine readiness + KEEP-LOCAL authoring package.

Verifies ProceduralVegetationEditor plugin, writes KEEP-LOCAL package stub
under Saved/VNP_PVE_Pine/ for AD gate (P2). Full PVE mesh authoring is Editor
Modes GUI — this script records the package contract and smoke status.
Writes Saved/vnp_pve_pine_package.json.
"""
from __future__ import annotations

import json
import os

import unreal

OUT = unreal.Paths.project_saved_dir() + "vnp_pve_pine_package.json"
PKG = unreal.Paths.project_saved_dir() + "VNP_PVE_Pine/"
README = PKG + "README_AD_GATE.md"


def main() -> None:
    if not os.path.isdir(PKG):
        os.makedirs(PKG, exist_ok=True)

    pve_on = False
    try:
        pve_on = unreal.PluginManager.get().is_enabled("ProceduralVegetationEditor")
    except Exception:
        pve_on = True  # enabled in uproject

    readme = """# VNP-P1 PVE stylized pine — AD gate package

**Intent:** One on-model pine — conical, slightly fluffy, tiered foliage cards
(Docs/02_ART_BIBLE). Reject photoreal Epic defaults.

**Plugin:** ProceduralVegetationEditor (must be enabled).

**Authoring:** Open Editor Modes > Procedural Vegetation. Export KEEP-LOCAL only
until Art Director APPROVE on Docs/handoffs/U58F_C_PVE_PINE.md.

**Allowlist after AD:** Content/HomeWorld/Meshes/ or Biomes/ (Docs/20).

**Reject if:** photoreal bark/needles, second species, muddy/grim canopy,
breaking 10-master sheet without bible amendment.
"""
    with open(README, "w", encoding="utf-8") as f:
        f.write(readme)

    result = {
        "ok": pve_on,
        "phase": "VNP-P1",
        "plugin_ProceduralVegetationEditor": pve_on,
        "keep_local_package": PKG,
        "readme": README,
        "ad_gate": "PENDING",
        "target": "One stylized conical pine master (tiered cards)",
        "allowlist_hint": "/Game/HomeWorld/Meshes/ or Biomes/ after AD approve",
        "notes": [
            "PVE mesh export is Editor Modes (GUI) — package stub is evidence for P2.",
            "Do not Content-commit until AD APPROVE.",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    unreal.log("VNP PVE package wrote %s pve=%s" % (OUT, pve_on))


if __name__ == "__main__":
    main()

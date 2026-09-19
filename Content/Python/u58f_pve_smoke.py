"""U58F-C Procedural Vegetation Editor readiness (Docs/23).

Verifies ProceduralVegetationEditor plugin, writes Saved/u58f_pve_smoke.json.
Does NOT author a photoreal pine. Art Director must approve any PVE export into
allowlisted Content/HomeWorld before commit. Target: conical stylized pine (Docs/02).
"""
from __future__ import annotations

import json
import unreal

OUT = unreal.Paths.project_saved_dir() + "u58f_pve_smoke.json"


def _plugin_enabled(name: str) -> bool:
    try:
        pm = unreal.PluginManager.get()
        if pm and hasattr(pm, "is_enabled_plugin"):
            return bool(pm.is_enabled_plugin(name))
    except Exception:
        pass
    try:
        path = unreal.Paths.project_dir() + "HomeWorld.uproject"
        with open(path, encoding="utf-8-sig") as f:
            data = json.load(f)
        for plug in data.get("Plugins", []):
            if plug.get("Name") == name and plug.get("Enabled", False):
                return True
    except Exception:
        pass
    return False


def main() -> None:
    enabled = _plugin_enabled("ProceduralVegetationEditor")
    result = {
        "ok": enabled,
        "plugin": "ProceduralVegetationEditor",
        "enabled": enabled,
        "ad_gate": "PENDING",
        "target": "One stylized conical pine master (tiered cards); reject photoreal Epic defaults",
        "allowlist_path_hint": "/Game/HomeWorld/Meshes/ or Biomes/ after AD approve (Docs/20)",
        "notes": [
            "Open Modes / PVE toolset in Editor after plugin load.",
            "Export only after Art Director shot approve; KEEP-LOCAL until allowlisted commit.",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    unreal.log("U58F PVE smoke wrote %s enabled=%s" % (OUT, enabled))


if __name__ == "__main__":
    main()

"""U58F-G Mesh Terrain sandbox readiness (Docs/23).

Verifies MeshTerrainMode plugin. Does NOT convert VS_MVP Landscape.
Sandbox map path: /Game/HomeWorld/Maps/Sandbox/L_U58F_MeshTerrain
Writes Saved/u58f_mesh_terrain_smoke.json.
"""
from __future__ import annotations

import json
import unreal

OUT = unreal.Paths.project_saved_dir() + "u58f_mesh_terrain_smoke.json"
SANDBOX = "/Game/HomeWorld/Maps/Sandbox/L_U58F_MeshTerrain"


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
    enabled = _plugin_enabled("MeshTerrainMode")
    sandbox_exists = unreal.EditorAssetLibrary.does_asset_exist(SANDBOX)
    result = {
        "ok": enabled,
        "plugin": "MeshTerrainMode",
        "enabled": enabled,
        "sandbox_map": SANDBOX,
        "sandbox_exists": sandbox_exists,
        "vs_mvp_policy": "Do not replace VS_MVP Landscape until AD + World Designer + Lead approve",
        "notes": [
            "Create empty sandbox level under Maps/Sandbox when sculpting.",
            "KEEP-LOCAL until allowlisted path approved.",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    unreal.log("U58F MeshTerrain smoke wrote %s enabled=%s" % (OUT, enabled))


if __name__ == "__main__":
    main()

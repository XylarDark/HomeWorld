"""U58F — PCG 5.8 nondestructive-edit smoke (Docs/23).

Idempotent Editor script: verify PCG + PCGBiomeCore + PCGPrimitives plugins, find ForestIsland_PCG,
write Saved/u58f_pcg_smoke.json. Does not mutate production graph structure.
"""
from __future__ import annotations

import json
import unreal

OUT = unreal.Paths.project_saved_dir() + "u58f_pcg_smoke.json"


def _plugin_enabled(name: str) -> bool:
    try:
        pm = unreal.PluginManager.get()
        if pm and hasattr(pm, "is_enabled_plugin"):
            return bool(pm.is_enabled_plugin(name))
    except Exception:
        pass
    # Fallback: uproject lists plugins as enabled; Editor may need restart after .uproject edit
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
    result = {
        "ok": False,
        "plugins": {},
        "forest_graph": None,
        "notes": [],
    }
    for name in ("PCG", "PCGPythonInterop", "PCGBiomeCore", "PCGPrimitives"):
        result["plugins"][name] = _plugin_enabled(name)

    graph_path = "/Game/HomeWorld/PCG/ForestIsland_PCG"
    graph = unreal.EditorAssetLibrary.load_asset(graph_path)
    if graph:
        result["forest_graph"] = graph_path
        result["notes"].append(
            "Production graph present. For 5.8 nondestructive edit: DuplicateAsset to "
            "ForestIsland_PCG_U58F_Edit, assign on a sandbox volume, use Editor PCG edit tools; "
            "do not overwrite ForestIsland_PCG without AD gate."
        )
    else:
        result["notes"].append(
            f"Optional graph {graph_path} not in Content (WAVE F / VS_MVP may use other PCG). "
            "Plugins still adopted; create duplicate graphs when forest PCG returns."
        )

    result["notes"].append(
        "Re-check PCG_VARIABLES_NO_ACCESS on 5.8 via pcg_settings_introspect.py after Editor open."
    )
    # ok if PCG enabled in uproject (or PluginManager); graph optional post-WAVE-F
    result["ok"] = bool(result["plugins"].get("PCG"))

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    unreal.log(f"U58F PCG smoke wrote {OUT} ok={result['ok']}")


if __name__ == "__main__":
    main()

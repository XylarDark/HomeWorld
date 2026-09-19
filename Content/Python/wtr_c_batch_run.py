"""WTR-C batch: pine import + PCG introspect + PCG spike + night evidence (optional).

Run via UnrealEditor-Cmd -ExecutePythonScript or MCP execute_python_script.
Arms keep_python_script_alive for Cmd latent screenshots.
"""
from __future__ import annotations

import json
import os

import unreal

SUMMARY = unreal.Paths.project_saved_dir() + "wtr_c_batch_summary.json"


def _run(mod_name: str) -> dict:
    entry = {"module": mod_name, "ok": False}
    try:
        import importlib

        mod = importlib.import_module(mod_name)
        importlib.reload(mod)
        if hasattr(mod, "main"):
            mod.main()
        entry["ok"] = True
    except Exception as e:
        entry["error"] = str(e)
        unreal.log_error("WTR-C batch %s failed: %s" % (mod_name, e))
    return entry


def main() -> None:
    try:
        import vnp_editor_keep_alive as keep

        keep.arm()
    except Exception:
        pass

    steps = [
        _run("vnp_p3_pine_import"),
        _run("pcg_settings_introspect"),
        _run("wtr_pcg_nondestructive_spike"),
    ]
    # Evidence needs VS_MVP loaded — best effort
    try:
        level = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
        unreal.EditorLoadingAndSavingUtils.load_map(level)
        steps.append(_run("vnp_night_tune_and_evidence"))
    except Exception as e:
        steps.append({"module": "vnp_night_tune_and_evidence", "ok": False, "error": str(e)})

    pine_ok = False
    pine_json = unreal.Paths.project_saved_dir() + "vnp_p3_pine_import.json"
    if os.path.isfile(pine_json):
        try:
            with open(pine_json, encoding="utf-8") as f:
                pine_ok = bool(json.load(f).get("ok"))
        except Exception:
            pass

    summary = {"ok": all(s.get("ok") for s in steps[:3]), "pine_ok": pine_ok, "steps": steps}
    with open(SUMMARY, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    unreal.log("WTR-C batch summary %s" % SUMMARY)

    try:
        import vnp_editor_keep_alive as keep

        keep.disarm()
    except Exception:
        pass


if __name__ == "__main__":
    main()

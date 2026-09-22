"""NF2-B: night lookdev pass + Shot 1/2/5 evidence on L_VS_MVP_Markers.

Sets night-oriented cvars, loads VS_MVP, runs conductor night preflight +
arrange_pa_e_shotlist, then vnp_night_tune_and_evidence (CAM_Hero /
CAM_CabinClose / CAM_PortalNight). P1 three-state capture_outcome in output.
Writes Saved/nf2_b_night_lookdev_evidence.json.
"""
from __future__ import annotations

import importlib
import json
import os
import time

import unreal

import pa_e_shotlist_common as common

OUT = unreal.Paths.project_saved_dir() + "nf2_b_night_lookdev_evidence.json"
LEVEL = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
SHOT_DIR = unreal.Paths.project_saved_dir() + "VNP_Evidence/"
PREFIX = "NF2-B:"


def main() -> None:
    importlib.reload(common)
    notes = []
    try:
        import vnp_editor_keep_alive as keep

        keep.arm()
    except Exception as e:
        notes.append("keep_alive skip: %s" % e)

    try:
        unreal.SystemLibrary.execute_console_command(None, "r.Fog.ScreenSpaceScattering 1")
        unreal.SystemLibrary.execute_console_command(None, "r.MegaLights.EnableForProject 1")
        unreal.SystemLibrary.execute_console_command(None, "hw.TimeOfDay.Phase 2")
        notes.append("cvars: Fog SSS, MegaLights, hw.TimeOfDay.Phase=2 (Night)")
    except Exception as e:
        notes.append("cvar warn: %s" % e)

    load_ok = False
    try:
        load_ok = bool(unreal.EditorLoadingAndSavingUtils.load_map(LEVEL))
        notes.append("load_map %s -> %s" % (LEVEL, load_ok))
        time.sleep(0.5)
    except Exception as e:
        notes.append("load_map failed: %s" % e)

    conductor_preflight = common.conductor_night_evidence_preflight(PREFIX)
    arrange_gate = common.arrange_pa_e_shotlist(
        PREFIX,
        level_loaded=load_ok,
        require_mrq=False,
    )
    gate_ready = load_ok and conductor_preflight.get("ready") and arrange_gate.get("ready")

    if not gate_ready:
        blocked = list(conductor_preflight.get("blocked_reasons") or [])
        blocked.extend(arrange_gate.get("blocked_reasons") or [])
        harness = common.summarize_evidence_png_harness([], arrange_gate=arrange_gate)
        result = {
            "ok": False,
            **harness,
            "phase": "NF2-B",
            "track": "Docs/27 Night Feel Build",
            "feel_target": "safe home above a living world",
            "level": LEVEL,
            "load_ok": load_ok,
            "conductor_preflight": conductor_preflight,
            "arrange_gate": arrange_gate,
            "arrange_gate_path": arrange_gate.get("written_path") or common.arrange_gate_path(),
            "blocked_reasons": blocked,
            "evidence": [],
            "shot_files": {},
            "notes": notes + ["capture blocked — complete Arrange before VNP evidence"],
        }
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, default=str)
        unreal.log("NF2-B blocked by preflight/arrange ok=%s" % result["ok"])
        _disarm_keep_alive()
        return

    evidence = []
    try:
        import vnp_night_tune_and_evidence as ev

        importlib.reload(ev)
        ev.main()
        notes.append("vnp_night_tune_and_evidence.main() ran")
        expected = [
            SHOT_DIR + "shot1_lookout.png",
            SHOT_DIR + "shot2_cabin.png",
            SHOT_DIR + "shot5_spirit.png",
        ]
        for _ in range(40):
            if all(os.path.isfile(p) and os.path.getsize(p) > 0 for p in expected):
                notes.append("all shot PNGs present after wait")
                break
            time.sleep(0.5)
        else:
            notes.append("shot PNG wait timed out (partial latent write ok)")
        vnp_json = unreal.Paths.project_saved_dir() + "vnp_night_evidence.json"
        if os.path.isfile(vnp_json):
            with open(vnp_json, encoding="utf-8") as f:
                vnp = json.load(f)
            evidence = vnp.get("evidence") or []
            notes.append("cameras_found=%s" % (vnp.get("cameras_found") or [])[:8])
    except Exception as e:
        notes.append("evidence script failed: %s" % e)

    shots = {}
    png_paths = []
    for name in ("shot1_lookout.png", "shot2_cabin.png", "shot5_spirit.png"):
        path = SHOT_DIR + name
        exists = os.path.isfile(path)
        size = os.path.getsize(path) if exists else 0
        shots[name] = {"path": path, "exists": exists, "bytes": size}
        if exists and size > 0:
            png_paths.append(path)

    bound = all(e.get("bound") for e in evidence) if evidence else False
    harness = common.summarize_evidence_png_harness(png_paths, arrange_gate=arrange_gate)
    ok = harness.get("capture_outcome") == common.CAPTURE_OUTCOME_PASS and bound

    result = {
        "ok": ok,
        **harness,
        "phase": "NF2-B",
        "track": "Docs/27 Night Feel Build",
        "feel_target": "safe home above a living world",
        "level": LEVEL,
        "load_ok": load_ok,
        "conductor_preflight": conductor_preflight,
        "arrange_gate": arrange_gate,
        "camera_bindings": {
            "shot1_lookout": "CAM_Hero",
            "shot2_cabin": "CAM_CabinClose",
            "shot5_spirit": "CAM_PortalNight",
        },
        "evidence": evidence,
        "shot_files": shots,
        "cameras_bound": bound,
        "notes": notes,
        "ad_status": "pending_AD_NF2-C",
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str)
    unreal.log("NF2-B night lookdev wrote %s ok=%s outcome=%s" % (OUT, ok, harness.get("capture_outcome")))

    _disarm_keep_alive()
    time.sleep(3.0)


def _disarm_keep_alive() -> None:
    try:
        import vnp_editor_keep_alive as keep

        keep.disarm()
    except Exception:
        pass


if __name__ == "__main__":
    main()

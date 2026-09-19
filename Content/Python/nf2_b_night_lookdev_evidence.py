"""NF2-B: night lookdev pass + Shot 1/2/5 evidence on L_VS_MVP_Markers.

Sets night-oriented cvars, loads VS_MVP, runs vnp_night_tune_and_evidence
(CAM_Hero / CAM_CabinClose / CAM_PortalNight), stamps Docs/27 feel target.
Writes Saved/nf2_b_night_lookdev_evidence.json.
"""
from __future__ import annotations

import json
import os
import time

import unreal

OUT = unreal.Paths.project_saved_dir() + "nf2_b_night_lookdev_evidence.json"
LEVEL = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
SHOT_DIR = unreal.Paths.project_saved_dir() + "VNP_Evidence/"


def main() -> None:
    notes = []
    try:
        import vnp_editor_keep_alive as keep

        keep.arm()
    except Exception as e:
        notes.append("keep_alive skip: %s" % e)

    try:
        unreal.SystemLibrary.execute_console_command(None, "r.Fog.ScreenSpaceScattering 1")
        unreal.SystemLibrary.execute_console_command(None, "r.MegaLights.EnableForProject 1")
        # Night phase for form/NightMix when playing; Editor viewport still benefits from fog/lights tune
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

    evidence = []
    try:
        import importlib
        import vnp_night_tune_and_evidence as ev

        importlib.reload(ev)
        ev.main()
        notes.append("vnp_night_tune_and_evidence.main() ran")
        # AutomationLibrary screenshots are latent — wait for PNGs
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
    for name in ("shot1_lookout.png", "shot2_cabin.png", "shot5_spirit.png"):
        path = SHOT_DIR + name
        exists = os.path.isfile(path)
        size = os.path.getsize(path) if exists else 0
        shots[name] = {"path": path, "exists": exists, "bytes": size}

    bound = all(e.get("bound") for e in evidence) if evidence else False
    files_ok = sum(1 for s in shots.values() if s.get("exists") and s.get("bytes", 0) > 0)
    ok = load_ok and bool(evidence) and bound and files_ok >= 2

    result = {
        "ok": ok,
        "phase": "NF2-B",
        "track": "Docs/27 Night Feel Build",
        "feel_target": "safe home above a living world",
        "level": LEVEL,
        "load_ok": load_ok,
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
        json.dump(result, f, indent=2)
    unreal.log("NF2-B night lookdev wrote %s ok=%s" % (OUT, ok))

    try:
        import vnp_editor_keep_alive as keep

        keep.disarm()
    except Exception:
        pass
    # Extra settle for latent HighResShot before Cmd exit
    time.sleep(3.0)


if __name__ == "__main__":
    main()

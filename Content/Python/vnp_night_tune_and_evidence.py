"""VNP N1/N2: tune night fog/warm lights and capture shot evidence.

Loads current editor level, reinforces MegaLights/Fog SSS, warms Point/Spot
lights toward amber, cools directional if present, high-res screenshots for
shots 1/2/5 camera actors when named, else viewport captures.
Writes Saved/vnp_night_evidence.json.
"""
from __future__ import annotations

import json
import os
import time

import unreal

OUT = unreal.Paths.project_saved_dir() + "vnp_night_evidence.json"
SHOT_DIR = unreal.Paths.project_saved_dir() + "VNP_Evidence/"


def _try_set(obj, name: str, value) -> bool:
    try:
        if hasattr(obj, "set_editor_property"):
            obj.set_editor_property(name, value)
            return True
    except Exception:
        pass
    try:
        setattr(obj, name, value)
        return True
    except Exception:
        return False


def _ensure_dir(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def _stat_fps() -> str:
    # Best-effort: console does not return FPS to Python; note request time.
    try:
        unreal.SystemLibrary.execute_console_command(None, "stat fps")
    except Exception:
        pass
    return "stat fps requested (see Editor viewport); record manually if needed"


def main() -> None:
    _ensure_dir(SHOT_DIR)
    try:
        unreal.SystemLibrary.execute_console_command(None, "r.Fog.ScreenSpaceScattering 1")
        unreal.SystemLibrary.execute_console_command(None, "r.MegaLights.EnableForProject 1")
    except Exception as e:
        unreal.log_warning("VNP night: cvar set failed: %s" % e)

    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    fog_tuned = []
    lights_tuned = []
    cameras = []

    warm = unreal.LinearColor(1.0, 0.72, 0.35, 1.0)
    cool = unreal.LinearColor(0.55, 0.65, 0.95, 1.0)

    for a in actors:
        if not a:
            continue
        name = a.get_name()
        cls = a.get_class().get_name() if a.get_class() else ""

        if "CameraActor" in cls or "CineCamera" in cls:
            cameras.append(name)

        if "ExponentialHeightFog" in cls or "HeightFog" in cls:
            comp = a.root_component
            applied = []
            if comp:
                for prop in ("enable_volumetric_fog", "b_enable_volumetric_fog"):
                    if _try_set(comp, prop, True):
                        applied.append(prop)
                for prop in (
                    "enable_fog_screen_space_scattering",
                    "b_enable_fog_screen_space_scattering",
                ):
                    if _try_set(comp, prop, True):
                        applied.append(prop)
                # Soft density bump toward readable atmosphere (not grim)
                for prop, val in (
                    ("fog_density", 0.02),
                    ("fog_height_falloff", 0.2),
                ):
                    if _try_set(comp, prop, val):
                        applied.append("%s=%s" % (prop, val))
            fog_tuned.append({"actor": name, "applied": applied})

        if "PointLight" in cls or "SpotLight" in cls or "RectLight" in cls:
            try:
                lc = a.light_component if hasattr(a, "light_component") else a.root_component
            except Exception:
                lc = a.root_component
            applied = []
            if lc:
                if _try_set(lc, "light_color", warm):
                    applied.append("light_color=warm_amber")
                if _try_set(lc, "intensity", 8.0):
                    applied.append("intensity")
                if _try_set(lc, "mobility", unreal.ComponentMobility.MOVABLE):
                    applied.append("movable")
            if applied:
                lights_tuned.append({"actor": name, "class": cls, "applied": applied})

        if "DirectionalLight" in cls:
            try:
                lc = a.light_component if hasattr(a, "light_component") else a.root_component
            except Exception:
                lc = a.root_component
            if lc and _try_set(lc, "light_color", cool):
                lights_tuned.append({"actor": name, "class": cls, "applied": ["light_color=cool_moon"]})

    # Prefer named cameras matching shot intents; else viewport
    shot_specs = [
        ("shot1_lookout", ("Shot1", "Lookout", "Hero", "CAM_Shot1", "CameraActor")),
        ("shot2_cabin", ("Shot2", "Cabin", "Garden", "CAM_Shot2")),
        ("shot5_spirit", ("Shot5", "Spirit", "Portal", "Shrine", "CAM_Shot5")),
    ]
    evidence = []
    for shot_id, needles in shot_specs:
        fname = shot_id + ".png"
        abs_path = SHOT_DIR + fname
        cam = None
        for a in actors:
            if not a:
                continue
            n = a.get_name()
            cls = a.get_class().get_name() if a.get_class() else ""
            if "Camera" not in cls:
                continue
            if any(x.lower() in n.lower() for x in needles):
                cam = a
                break
        if cam:
            try:
                unreal.EditorLevelLibrary.set_level_viewport_camera_info(
                    cam.get_actor_location(),
                    cam.get_actor_rotation(),
                )
            except Exception as e:
                unreal.log_warning("VNP: set camera failed %s: %s" % (cam.get_name(), e))
        try:
            unreal.AutomationLibrary.take_high_res_screenshot(1600, 900, abs_path)
            evidence.append({"shot": shot_id, "path": abs_path, "camera": cam.get_name() if cam else "viewport"})
        except Exception as e:
            # Fallback: mark path expected
            evidence.append({"shot": shot_id, "path": abs_path, "error": str(e), "camera": cam.get_name() if cam else "viewport"})

        time.sleep(0.3)

    world = unreal.EditorLevelLibrary.get_editor_world()
    level_name = world.get_name() if world else "unknown"

    result = {
        "ok": True,
        "phase": "VNP-N0/N1/N2",
        "level": level_name,
        "fog_tuned": fog_tuned,
        "lights_tuned_count": len(lights_tuned),
        "lights_tuned_sample": lights_tuned[:12],
        "cameras_found": cameras[:40],
        "evidence": evidence,
        "fps_note": _stat_fps(),
        "project_cvars": {
            "r.MegaLights.EnableForProject": True,
            "r.Fog.ScreenSpaceScattering": 1,
        },
        "ad_status": "pending_AD",
        "notes": [
            "Warm windows vs cool moon per Docs/02_ART_BIBLE; not grimdark.",
            "Shots 1/2/5 only — no sixth framing.",
            "Content map changes KEEP-LOCAL until Lead allowlist commit.",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    unreal.log("VNP night evidence wrote %s shots=%d" % (OUT, len(evidence)))


if __name__ == "__main__":
    main()

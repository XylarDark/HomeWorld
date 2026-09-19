"""VNP N1/N2: tune night fog/warm lights and capture shot evidence.

Loads current editor level, reinforces MegaLights/Fog SSS, warms Point/Spot
lights toward amber, cools directional if present, high-res screenshots for
shots 1/2/5 bound to named cameras on L_VS_MVP_Markers (CAM_Hero,
CAM_CabinClose, CAM_PortalNight). Uses AutomationLibrary.take_high_res_screenshot
and optional compare_image_against_reference when a golden exists under
Saved/VNP_Evidence/Goldens/.

Writes Saved/vnp_night_evidence.json.
"""
from __future__ import annotations

import json
import os
import time

import unreal

OUT = unreal.Paths.project_saved_dir() + "vnp_night_evidence.json"
SHOT_DIR = unreal.Paths.project_saved_dir() + "VNP_Evidence/"
GOLDEN_DIR = SHOT_DIR + "Goldens/"

# Canon shot → preferred actor labels (Maps/VS_MVP README + place_vs_mvp_markers CAM)
SHOT_CAMERA_BINDINGS = [
    (
        "shot1_lookout",
        ("CAM_Hero", "Shot1", "Lookout", "Hero", "CAM_Shot1"),
    ),
    (
        "shot2_cabin",
        ("CAM_CabinClose", "Shot2", "Cabin", "Garden", "CAM_Shot2"),
    ),
    (
        "shot5_spirit",
        ("CAM_PortalNight", "Shot5", "Spirit", "Portal", "Shrine", "CAM_Shot5"),
    ),
]


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


def _actor_label(a) -> str:
    try:
        return a.get_actor_label() or a.get_name()
    except Exception:
        return a.get_name() if a else ""


def _find_camera(actors, needles: tuple[str, ...]):
    """Prefer exact label match, then substring on label/name."""
    cams = []
    for a in actors:
        if not a:
            continue
        cls = a.get_class().get_name() if a.get_class() else ""
        if "Camera" not in cls:
            continue
        cams.append(a)

    needle_l = [n.lower() for n in needles]
    for needle in needle_l:
        for a in cams:
            label = _actor_label(a).lower()
            name = a.get_name().lower()
            if label == needle or name == needle:
                return a
    for a in cams:
        label = _actor_label(a).lower()
        name = a.get_name().lower()
        if any(n in label or n in name for n in needle_l):
            return a
    return None


def _compare_to_golden(shot_id: str, abs_path: str) -> dict | None:
    golden = GOLDEN_DIR + shot_id + ".png"
    if not os.path.isfile(golden):
        return None
    if not os.path.isfile(abs_path):
        return {"golden": golden, "compared": False, "reason": "screenshot missing"}
    try:
        # UE 5.8 AutomationLibrary — tolerance soft for lighting variance
        ok = unreal.AutomationLibrary.compare_image_against_reference(
            abs_path,
            golden,
            0.15,
        )
        return {"golden": golden, "compared": True, "match": bool(ok)}
    except TypeError:
        # Signature variants across 5.8 builds
        try:
            ok = unreal.AutomationLibrary.compare_image_against_reference(abs_path, golden)
            return {"golden": golden, "compared": True, "match": bool(ok)}
        except Exception as e:
            return {"golden": golden, "compared": False, "error": str(e)}
    except Exception as e:
        return {"golden": golden, "compared": False, "error": str(e)}


def _stat_fps() -> str:
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
        name = _actor_label(a)
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

    evidence = []
    for shot_id, needles in SHOT_CAMERA_BINDINGS:
        fname = shot_id + ".png"
        abs_path = SHOT_DIR + fname
        cam = _find_camera(actors, needles)
        if cam:
            try:
                unreal.EditorLevelLibrary.set_level_viewport_camera_info(
                    cam.get_actor_location(),
                    cam.get_actor_rotation(),
                )
            except Exception as e:
                unreal.log_warning("VNP: set camera failed %s: %s" % (_actor_label(cam), e))
        try:
            unreal.AutomationLibrary.take_high_res_screenshot(1600, 900, abs_path)
            entry = {
                "shot": shot_id,
                "path": abs_path,
                "camera": _actor_label(cam) if cam else "viewport",
                "bound": bool(cam),
            }
        except Exception as e:
            entry = {
                "shot": shot_id,
                "path": abs_path,
                "error": str(e),
                "camera": _actor_label(cam) if cam else "viewport",
                "bound": bool(cam),
            }
        cmp = _compare_to_golden(shot_id, abs_path)
        if cmp:
            entry["golden_compare"] = cmp
        evidence.append(entry)
        time.sleep(0.3)

    world = unreal.EditorLevelLibrary.get_editor_world()
    level_name = world.get_name() if world else "unknown"

    result = {
        "ok": True,
        "phase": "VNP-N0/N1/N2 + WTR-C",
        "level": level_name,
        "fog_tuned": fog_tuned,
        "lights_tuned_count": len(lights_tuned),
        "lights_tuned_sample": lights_tuned[:12],
        "cameras_found": cameras[:40],
        "camera_bindings": {
            "shot1_lookout": "CAM_Hero",
            "shot2_cabin": "CAM_CabinClose",
            "shot5_spirit": "CAM_PortalNight",
        },
        "evidence": evidence,
        "fps_note": _stat_fps(),
        "project_cvars": {
            "r.MegaLights.EnableForProject": True,
            "r.Fog.ScreenSpaceScattering": 1,
        },
        "ad_status": "pending_AD",
        "notes": [
            "Warm windows vs cool moon per Docs/02_ART_BIBLE; not grimdark.",
            "Shots 1/2/5 bound to CAM_Hero / CAM_CabinClose / CAM_PortalNight.",
            "Optional goldens: Saved/VNP_Evidence/Goldens/<shot_id>.png",
            "Content map changes KEEP-LOCAL until Lead allowlist commit.",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    unreal.log("VNP night evidence wrote %s shots=%d" % (OUT, len(evidence)))


if __name__ == "__main__":
    main()

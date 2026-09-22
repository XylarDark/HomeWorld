"""VNP N1/N2: tune night fog/warm lights and capture shot evidence.

Loads current editor level, reinforces MegaLights/Fog SSS, warms Point/Spot
lights toward amber, cools directional if present, high-res screenshots for
shots 1/2/5 bound to named cameras on L_VS_MVP_Markers (CAM_Hero,
CAM_CabinClose, CAM_PortalNight). Uses AutomationLibrary.take_high_res_screenshot
and optional compare_image_against_reference when a golden exists under
Saved/VNP_Evidence/Goldens/.

Canon preset: Lib/07_Night_SpiritLayer/PRESET_Homestead_Night.md

Public API (no screenshots):
- apply_homestead_night_tune() — cvars + fog + warm/cool lights
- verify_homestead_night_lighting_stack() — moon + skylight/directional + cabin warm

Writes Saved/vnp_night_evidence.json (full main() only).
"""
from __future__ import annotations

import json
import os
import time

import unreal

OUT = unreal.Paths.project_saved_dir() + "vnp_night_evidence.json"
SHOT_DIR = unreal.Paths.project_saved_dir() + "VNP_Evidence/"
GOLDEN_DIR = SHOT_DIR + "Goldens/"
PRESET_HOMESTEAD_NIGHT_DOC = "Lib/07_Night_SpiritLayer/PRESET_Homestead_Night.md"

# Expected in-level signals per PRESET_Homestead_Night (readable night, not pitch black).
_MOON_LABEL_NEEDLES = ("lit_moon", "moon_disc", "moon")
_SKY_AMBIENT_CLASSES = ("SkyLight", "DirectionalLight")
_CABIN_WARM_NEEDLES = ("lit_cabinwarm", "lit_cabinwindows", "cabinwindow", "cabin_warm", "window")

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


def apply_project_night_cvars() -> dict:
    """MegaLights + fog SSS — readable night ambient per PRESET_Homestead_Night."""
    meta: dict = {"commands": [], "ok": True}
    for cmd in (
        "r.Fog.ScreenSpaceScattering 1",
        "r.MegaLights.EnableForProject 1",
    ):
        try:
            unreal.SystemLibrary.execute_console_command(None, cmd)
            meta["commands"].append({"cmd": cmd, "ok": True})
        except Exception as e:
            meta["ok"] = False
            meta["commands"].append({"cmd": cmd, "ok": False, "error": str(e)})
    meta["preset_doc"] = PRESET_HOMESTEAD_NIGHT_DOC
    return meta


def _tune_level_night_lighting(actors: list) -> tuple[list, list]:
    """Warm point/spot, cool directional, volumetric fog — returns (fog_tuned, lights_tuned)."""
    fog_tuned: list = []
    lights_tuned: list = []
    warm = unreal.LinearColor(1.0, 0.72, 0.35, 1.0)
    cool = unreal.LinearColor(0.55, 0.65, 0.95, 1.0)

    for a in actors:
        if not a:
            continue
        name = _actor_label(a)
        cls = a.get_class().get_name() if a.get_class() else ""

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

    return fog_tuned, lights_tuned


def apply_homestead_night_tune(actors: list | None = None) -> dict:
    """Apply PRESET_Homestead_Night tune (cvars + fog + lights). No screenshots."""
    cvars = apply_project_night_cvars()
    if actors is None:
        actors = unreal.EditorLevelLibrary.get_all_level_actors()
    fog_tuned, lights_tuned = _tune_level_night_lighting(actors)
    return {
        "ok": bool(cvars.get("ok")),
        "preset_doc": PRESET_HOMESTEAD_NIGHT_DOC,
        "project_cvars": cvars,
        "fog_tuned": fog_tuned,
        "lights_tuned_count": len(lights_tuned),
        "lights_tuned_sample": lights_tuned[:12],
        "note": "Phase 2 alone does not apply this tune — call before PA-E/MRQ capture.",
    }


def verify_homestead_night_lighting_stack(actors: list | None = None) -> dict:
    """Verify moon + sky ambient + cabin warm signals exist (readable thematic night)."""
    if actors is None:
        actors = unreal.EditorLevelLibrary.get_all_level_actors()
    moon_hits: list[str] = []
    sky_hits: list[str] = []
    cabin_hits: list[str] = []
    fog_hits: list[str] = []

    for a in actors:
        if not a:
            continue
        label = _actor_label(a)
        label_l = label.lower()
        cls = a.get_class().get_name() if a.get_class() else ""

        if any(n in label_l for n in _MOON_LABEL_NEEDLES):
            moon_hits.append(label)
        if any(c in cls for c in _SKY_AMBIENT_CLASSES):
            sky_hits.append("%s (%s)" % (label, cls))
        if any(n in label_l for n in _CABIN_WARM_NEEDLES):
            cabin_hits.append(label)
        if "PointLight" in cls or "SpotLight" in cls or "RectLight" in cls:
            if "cabin" in label_l or "lit_" in label_l or "window" in label_l:
                cabin_hits.append("%s (%s)" % (label, cls))
        if "ExponentialHeightFog" in cls or "HeightFog" in cls:
            fog_hits.append(label)

    moon_ok = len(moon_hits) > 0
    sky_ok = len(sky_hits) > 0
    cabin_ok = len(cabin_hits) > 0
    stack_ok = moon_ok and sky_ok and cabin_ok
    return {
        "stack_ok": stack_ok,
        "preset_doc": PRESET_HOMESTEAD_NIGHT_DOC,
        "moon": {"ok": moon_ok, "actors": moon_hits[:20]},
        "skylight_or_moon_key": {"ok": sky_ok, "actors": sky_hits[:20]},
        "cabin_warm_or_windows": {"ok": cabin_ok, "actors": cabin_hits[:20]},
        "height_fog": {"present": bool(fog_hits), "actors": fog_hits[:10]},
        "phase_2_alone_insufficient": (
            "hw.TimeOfDay.Phase 2 sets gameplay night phase only; "
            "readable sky/moon/stars + cabin emissives require PRESET tune and in-level LIT actors."
        ),
        "do_not_switch_to_day": "Fix night stack per preset — do not use day phase to dodge black stills.",
    }


def _stat_fps() -> str:
    try:
        unreal.SystemLibrary.execute_console_command(None, "stat fps")
    except Exception:
        pass
    return "stat fps requested (see Editor viewport); record manually if needed"


def main() -> None:
    _ensure_dir(SHOT_DIR)
    tune = apply_homestead_night_tune()
    verify = verify_homestead_night_lighting_stack()
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    fog_tuned = tune.get("fog_tuned") or []
    lights_tuned_count = tune.get("lights_tuned_count") or 0
    lights_tuned_sample = tune.get("lights_tuned_sample") or []
    cameras = []
    for a in actors:
        if not a:
            continue
        cls = a.get_class().get_name() if a.get_class() else ""
        if "CameraActor" in cls or "CineCamera" in cls:
            cameras.append(_actor_label(a))

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
        # Relative filename under Saved/ — absolute paths often fail under UnrealEditor-Cmd
        fname_only = fname
        methods = []
        try:
            if cam:
                try:
                    unreal.EditorLevelLibrary.pilot_level_actor(cam)
                except Exception:
                    pass
            unreal.AutomationLibrary.take_high_res_screenshot(1600, 900, fname_only, cam if cam else None)
            methods.append("AutomationLibrary_rel")
        except Exception as e:
            methods.append("AutomationLibrary_fail:%s" % e)
        try:
            world = unreal.EditorLevelLibrary.get_editor_world()
            rel = "Saved/VNP_Evidence/" + fname
            unreal.SystemLibrary.execute_console_command(
                world,
                'HighResShot 1600x900 filename="%s"' % rel.replace("\\", "/"),
            )
            methods.append("HighResShot")
        except Exception as e2:
            methods.append("HighResShot_fail:%s" % e2)
        time.sleep(1.5)
        # Resolve: prefer explicit path; else newest matching under Saved/Screenshots
        if not os.path.isfile(abs_path):
            screens_root = unreal.Paths.project_saved_dir() + "Screenshots"
            candidates = []
            if os.path.isdir(screens_root):
                for root, _dirs, files in os.walk(screens_root):
                    for f in files:
                        if f.lower().endswith(".png") and (shot_id in f.lower() or f.lower() == fname.lower()):
                            candidates.append(os.path.join(root, f))
            if candidates:
                candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
                try:
                    import shutil

                    shutil.copy2(candidates[0], abs_path)
                    methods.append("copied_from_Screenshots")
                except Exception as ce:
                    methods.append("copy_fail:%s" % ce)
        entry = {
            "shot": shot_id,
            "path": abs_path,
            "camera": _actor_label(cam) if cam else "viewport",
            "bound": bool(cam),
            "methods": methods,
            "file_exists": os.path.isfile(abs_path),
        }
        if not os.path.isfile(abs_path):
            entry["note"] = "png missing after AutomationLibrary+HighResShot"
        cmp = _compare_to_golden(shot_id, abs_path)
        if cmp:
            entry["golden_compare"] = cmp
        evidence.append(entry)

    world = unreal.EditorLevelLibrary.get_editor_world()
    level_name = world.get_name() if world else "unknown"

    result = {
        "ok": True,
        "phase": "VNP-N0/N1/N2 + WTR-C",
        "level": level_name,
        "preset_doc": PRESET_HOMESTEAD_NIGHT_DOC,
        "night_tune": tune,
        "lighting_stack_verify": verify,
        "fog_tuned": fog_tuned,
        "lights_tuned_count": lights_tuned_count,
        "lights_tuned_sample": lights_tuned_sample,
        "cameras_found": cameras[:40],
        "camera_bindings": {
            "shot1_lookout": "CAM_Hero",
            "shot2_cabin": "CAM_CabinClose",
            "shot5_spirit": "CAM_PortalNight",
        },
        "evidence": evidence,
        "fps_note": _stat_fps(),
        "project_cvars": tune.get("project_cvars", {}),
        "ad_status": "pending_AD",
        "notes": [
            "Warm windows vs cool moon per Docs/02_ART_BIBLE; not grimdark.",
            "Shots 1/2/5 bound to CAM_Hero / CAM_CabinClose / CAM_PortalNight.",
            "Phase 2 + PRESET tune required for readable night — see apply_homestead_night_tune().",
            "Optional goldens: Saved/VNP_Evidence/Goldens/<shot_id>.png",
            "Content map changes KEEP-LOCAL until Lead allowlist commit.",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    unreal.log("VNP night evidence wrote %s shots=%d" % (OUT, len(evidence)))


if __name__ == "__main__":
    main()

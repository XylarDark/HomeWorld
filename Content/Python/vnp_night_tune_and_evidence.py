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
- apply_mrq_pie_homestead_night_stack() — exposure/SupportSkyAtmosphere, TMP in target world,
  SkyAtmosphere + moon AtmosphereSunLightIndex 0 + SkyLight RecaptureSky (MRQ PIE void-sky fix)
- apply_mrq_pie_homestead_night_stack_in_render_world() — call after PIE executor starts

Writes Saved/vnp_night_evidence.json (full main() only).
"""
from __future__ import annotations

from typing import Any

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


# Session-only fixtures (re-spawned after load_level; not saved to .umap by default).
TMP_PA_E_ARRANGE_FOLDER = "VS_MVP/TMP_PA_E_Arrange"
TMP_MOON_LABEL = "lit_moon"
TMP_SKY_LABEL = "TMP_PA_E_SkyLight"
TMP_CABIN_WARM_LABEL = "lit_cabinwarm"
TMP_SKY_ATMO_LABEL = "TMP_PA_E_SkyAtmosphere"
TMP_HEIGHT_FOG_LABEL = "TMP_PA_E_HeightFog"

# PRESET world.sky_color #0B1630 — readable open-sky ambient when capture sees void black.
_PRESET_SKY_AMBIENT_LINEAR = unreal.LinearColor(0.043, 0.086, 0.188, 1.0)
# PRESET horizon_glow #7EC8E8 — fog inscattering for readable night horizon in MRQ void.
_PRESET_HORIZON_FOG_LINEAR = unreal.LinearColor(0.494, 0.784, 0.910, 1.0)
# Global atmosphere anchor (not dress centroid — wrong planet origin → black sky in MRQ).
_SKY_ATMO_WORLD_ORIGIN = unreal.Vector(0.0, 0.0, 0.0)

MRQ_PIE_NIGHT_EXPOSURE_CVARS: tuple[str, ...] = (
    "r.DefaultFeature.AutoExposure 1",
    "r.DefaultFeature.AutoExposure.Bias 0",
    "r.DefaultFeature.AutoExposure.MinBrightness 0.03",
    "r.DefaultFeature.AutoExposure.MaxBrightness 2.0",
)

# Epic single Atmosphere Sun Light uses index 0; index 1 with one directional → void sky (forums).
MRQ_PIE_ATMOSPHERE_SUN_INDEX = 0

MRQ_PIE_RENDER_CVARS: tuple[str, ...] = (
    "r.SupportSkyAtmosphere 1",
    "r.SkyAtmosphere 1",
    "r.Fog 1",
    "r.VolumetricFog 1",
    "r.Fog.ScreenSpaceScattering 1",
) + MRQ_PIE_NIGHT_EXPOSURE_CVARS

_DEFAULT_HOMESTEAD_CENTROID = (-600.0, -100.0, 150.0)
_CENTROID_Z_MIN_SANE = -200.0
_CENTROID_Z_MAX_SANE = 50000.0


def _sanitize_homestead_centroid(homestead_centroid: list[float] | None) -> dict[str, Any]:
    """Reject void/insane dress centroids (e.g. cliff Z≈-3656) before moon aim/placement."""
    if not homestead_centroid or len(homestead_centroid) < 3:
        used = list(_DEFAULT_HOMESTEAD_CENTROID)
        return {"used": used, "rejected": None, "reason": "missing_or_short"}
    try:
        cx = float(homestead_centroid[0])
        cy = float(homestead_centroid[1])
        cz = float(homestead_centroid[2])
    except (TypeError, ValueError):
        used = list(_DEFAULT_HOMESTEAD_CENTROID)
        return {"used": used, "rejected": list(homestead_centroid), "reason": "non_numeric"}
    insane = (
        cz < _CENTROID_Z_MIN_SANE
        or cz > _CENTROID_Z_MAX_SANE
        or abs(cx) > 1.0e6
        or abs(cy) > 1.0e6
    )
    if insane:
        return {
            "used": list(_DEFAULT_HOMESTEAD_CENTROID),
            "rejected": [cx, cy, cz],
            "reason": "insane_centroid",
        }
    return {"used": [cx, cy, cz], "rejected": None, "reason": "ok"}


def _world_path_label(world) -> str:
    if world is None:
        return "editor"
    try:
        pn = (world.get_path_name() or "").upper()
        if "UEDPIE" in pn or "PIE" in pn:
            return "pie"
    except Exception:
        pass
    return "runtime"


def _is_editor_world(world) -> bool:
    return _world_path_label(world) == "editor"


def _actors_for_world(world) -> list:
    if world is None or _is_editor_world(world):
        return unreal.EditorLevelLibrary.get_all_level_actors()
    try:
        return list(unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor))
    except Exception:
        return []


def _spawn_actor_in_world(world, unreal_class, location: "unreal.Vector", rotation: "unreal.Rotator"):
    if world is None or _is_editor_world(world):
        return unreal.EditorLevelLibrary.spawn_actor_from_class(unreal_class, location, rotation)
    transform = unreal.Transform(
        location,
        rotation,
        unreal.Vector(1.0, 1.0, 1.0),
    )
    try:
        actor = unreal.GameplayStatics.begin_deferred_actor_spawn_from_class(
            world,
            unreal_class,
            transform,
            unreal.ActorSpawnParameters(),
        )
        if actor:
            return unreal.GameplayStatics.finish_spawning_actor(actor, transform)
    except Exception:
        pass
    return None


def resolve_mrq_pie_render_world() -> tuple[Any, str]:
    """World MoviePipelinePIEExecutor actually renders (not Editor TMP session actors)."""
    try:
        worlds = unreal.EditorLevelLibrary.get_pie_worlds(include_dedicated_server=False)
        if worlds:
            return worlds[0], "pie"
    except Exception:
        pass
    try:
        ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
        if ues and hasattr(ues, "get_game_world"):
            gw = ues.get_game_world()
            if gw and _world_path_label(gw) != "editor":
                return gw, "game_world"
    except Exception:
        pass
    return unreal.EditorLevelLibrary.get_editor_world(), "editor_fallback"


def _spawn_light_if_missing(
    actors: list,
    label: str,
    unreal_class,
    location: "unreal.Vector",
    rotation: "unreal.Rotator | None" = None,
    *,
    world=None,
) -> tuple[Any, bool]:
    for a in actors:
        if _actor_label(a) == label:
            return a, False
    rot = rotation if rotation is not None else unreal.Rotator(roll=0.0, pitch=0.0, yaw=0.0)
    actor = _spawn_actor_in_world(world, unreal_class, location, rot)
    if actor:
        try:
            actor.set_actor_label(label)
            if _is_editor_world(world):
                actor.set_folder_path(TMP_PA_E_ARRANGE_FOLDER)
        except Exception:
            pass
    return actor, True


def _light_component(actor):
    try:
        return actor.light_component if hasattr(actor, "light_component") else actor.root_component
    except Exception:
        return actor.root_component if actor else None


def _invoke_recapture_skylight(comp) -> bool:
    """RecaptureSky after atmosphere/moon changes — MRQ PIE needs fresh cubemap (Epic forums)."""
    if comp is None:
        return False
    for target in (comp,):
        for name in ("recapture_sky", "RecaptureSky"):
            fn = getattr(target, name, None)
            if callable(fn):
                try:
                    fn()
                    return True
                except Exception:
                    pass
    sky_cls = getattr(unreal, "SkyLightComponent", None)
    if sky_cls is not None:
        for name in ("recapture_sky", "RecaptureSky"):
            fn = getattr(sky_cls, name, None)
            if callable(fn):
                try:
                    fn(comp)
                    return True
                except Exception:
                    pass
    return False


def _configure_directional_moon(
    actor,
    intensity: float = 3.5,
    *,
    atmosphere_sun_index: int = MRQ_PIE_ATMOSPHERE_SUN_INDEX,
    mrq_key_boost: bool = False,
) -> list[str]:
    if mrq_key_boost:
        intensity = max(intensity, 8.0)
    applied: list[str] = []
    lc = _light_component(actor)
    warm = unreal.LinearColor(1.0, 0.88, 0.55, 1.0)
    if lc:
        if _try_set(lc, "light_color", warm):
            applied.append("light_color=moon_warm")
        if _try_set(lc, "intensity", intensity):
            applied.append("intensity")
        if _try_set(lc, "mobility", unreal.ComponentMobility.MOVABLE):
            applied.append("movable")
        for prop in ("atmosphere_sun_light", "b_atmosphere_sun_light", "AtmosphereSunLight"):
            if _try_set(lc, prop, True):
                applied.append("atmosphere_sun_light")
                break
        for prop in ("atmosphere_sun_light_index", "AtmosphereSunLightIndex"):
            if _try_set(lc, prop, int(atmosphere_sun_index)):
                applied.append("atmosphere_sun_light_index=%d" % atmosphere_sun_index)
                break
        if _try_set(lc, "affects_world", True):
            applied.append("affects_world")
    return applied


def _configure_skylight(
    actor,
    *,
    intensity: float = 1.35,
    recapture: bool = True,
    mrq_ambient_fill: bool = False,
) -> list[str]:
    applied: list[str] = []
    comp = _light_component(actor)
    if comp:
        if mrq_ambient_fill:
            intensity = max(intensity, 2.8)
            for prop in ("real_time_capture", "b_real_time_capture", "RealTimeCapture"):
                if _try_set(comp, prop, False):
                    applied.append("real_time_capture_off_mrq_fill")
                    break
        else:
            for prop in ("real_time_capture", "b_real_time_capture", "RealTimeCapture"):
                if _try_set(comp, prop, True):
                    applied.append("real_time_capture")
                    break
        if _try_set(comp, "intensity", intensity):
            applied.append("intensity")
        if _try_set(comp, "mobility", unreal.ComponentMobility.MOVABLE):
            applied.append("movable")
        for prop in ("lower_hemisphere_is_black", "b_lower_hemisphere_is_black"):
            if _try_set(comp, prop, False):
                applied.append("lower_hemisphere_not_black")
                break
        for prop in ("lower_hemisphere_color", "LowerHemisphereColor"):
            if _try_set(comp, prop, _PRESET_SKY_AMBIENT_LINEAR):
                applied.append("lower_hemisphere_color=preset_sky")
                break
        if _try_set(comp, "affects_world", True):
            applied.append("affects_world")
        if recapture and not mrq_ambient_fill:
            if _invoke_recapture_skylight(comp):
                applied.append("recapture_sky")
        elif mrq_ambient_fill:
            applied.append("recapture_skipped_mrq_hemisphere_fill")
    return applied


def _configure_cabin_warm_point(actor, intensity: float = 1200.0) -> list[str]:
    applied: list[str] = []
    try:
        lc = actor.light_component if hasattr(actor, "light_component") else actor.root_component
    except Exception:
        lc = actor.root_component
    warm = unreal.LinearColor(1.0, 0.72, 0.35, 1.0)
    if lc:
        if _try_set(lc, "light_color", warm):
            applied.append("light_color=warm_amber")
        if _try_set(lc, "intensity", intensity):
            applied.append("intensity")
        if _try_set(lc, "mobility", unreal.ComponentMobility.MOVABLE):
            applied.append("movable")
    return applied


def _homestead_centroid_xyz(homestead_centroid: list[float] | None) -> tuple[float, float, float]:
    meta = _sanitize_homestead_centroid(homestead_centroid)
    u = meta["used"]
    return u[0], u[1], u[2]


def apply_mrq_pie_night_exposure_cvars(world=None) -> dict:
    """Auto-exposure + SupportSkyAtmosphere in the world MRQ renders (PIE or Editor)."""
    meta: dict = {
        "commands": [],
        "ok": True,
        "preset_doc": PRESET_HOMESTEAD_NIGHT_DOC,
        "world_context": _world_path_label(world),
    }
    ctx = world if world is not None else None
    for cmd in MRQ_PIE_RENDER_CVARS:
        try:
            unreal.SystemLibrary.execute_console_command(ctx, cmd)
            meta["commands"].append({"cmd": cmd, "ok": True})
        except Exception as e:
            meta["ok"] = False
            meta["commands"].append({"cmd": cmd, "ok": False, "error": str(e)})
    return meta


def _apply_tod_phase_in_world(world, phase: int = 2) -> dict[str, Any]:
    meta: dict[str, Any] = {"phase": phase, "applied": False}
    cmd = "hw.TimeOfDay.Phase %d" % int(phase)
    ctx = world if world is not None else None
    try:
        unreal.SystemLibrary.execute_console_command(ctx, cmd)
        meta["applied"] = True
        meta["command"] = cmd
    except Exception as e:
        meta["error"] = str(e)
    return meta


def _configure_sky_atmosphere_actor(actor) -> list[str]:
    """Enable atmosphere component; anchor at world origin for planet sampling."""
    applied: list[str] = []
    try:
        actor.set_actor_location(_SKY_ATMO_WORLD_ORIGIN, False, False)
        applied.append("location=world_origin")
    except Exception:
        pass
    comp = actor.root_component
    if comp:
        for prop in ("enabled", "b_enabled"):
            if _try_set(comp, prop, True):
                applied.append("enabled")
                break
    return applied


def _ensure_sky_atmosphere(
    homestead_centroid: list[float] | None,
    *,
    world=None,
) -> dict:
    """Sky Atmosphere required for directional Atmosphere Sun Light + MRQ sky (community/Epic)."""
    actors = _actors_for_world(world)
    for a in actors:
        if not a:
            continue
        cls = a.get_class().get_name() if a.get_class() else ""
        if "SkyAtmosphere" in cls:
            cfg = _configure_sky_atmosphere_actor(a)
            return {
                "present": True,
                "spawned": False,
                "label": _actor_label(a),
                "configured": cfg,
                "world_context": _world_path_label(world),
            }
    atmo_cls = getattr(unreal, "SkyAtmosphere", None)
    if atmo_cls is None:
        return {"present": False, "spawned": False, "error": "SkyAtmosphere class missing"}
    actor = _spawn_actor_in_world(
        world, atmo_cls, _SKY_ATMO_WORLD_ORIGIN, unreal.Rotator(0.0, 0.0, 0.0)
    )
    if actor:
        cfg = _configure_sky_atmosphere_actor(actor)
        try:
            actor.set_actor_label(TMP_SKY_ATMO_LABEL)
            if _is_editor_world(world):
                actor.set_folder_path(TMP_PA_E_ARRANGE_FOLDER)
        except Exception:
            pass
        return {
            "present": True,
            "spawned": True,
            "label": TMP_SKY_ATMO_LABEL,
            "configured": cfg,
            "world_context": _world_path_label(world),
        }
    return {"present": False, "spawned": False, "error": "spawn_failed"}


def _fog_component(actor):
    comp = actor.root_component if actor else None
    if comp:
        return comp
    try:
        fog_cls = getattr(unreal, "ExponentialHeightFogComponent", None)
        if fog_cls is not None and actor:
            return actor.get_component_by_class(fog_cls)
    except Exception:
        pass
    return None


def _configure_height_fog(actor, *, mrq_visible_sky: bool = False) -> list[str]:
    applied: list[str] = []
    comp = _fog_component(actor)
    if not comp:
        return applied
    density = 0.045 if mrq_visible_sky else 0.02
    for prop in ("enable_volumetric_fog", "b_enable_volumetric_fog"):
        if _try_set(comp, prop, True):
            applied.append("volumetric_fog")
            break
    for prop in (
        "enable_fog_screen_space_scattering",
        "b_enable_fog_screen_space_scattering",
    ):
        if _try_set(comp, prop, True):
            applied.append("fog_sss")
            break
    if _try_set(comp, "fog_density", density):
        applied.append("fog_density=%s" % density)
    if _try_set(comp, "fog_height_falloff", 0.15):
        applied.append("fog_height_falloff")
    for prop in ("fog_inscattering_color", "FogInscatteringColor"):
        if _try_set(comp, prop, _PRESET_HORIZON_FOG_LINEAR):
            applied.append("fog_inscattering=preset_horizon")
            break
    for prop in ("directional_inscattering_color", "DirectionalInscatteringColor"):
        if _try_set(comp, prop, _PRESET_SKY_AMBIENT_LINEAR):
            applied.append("directional_inscattering=preset_sky")
            break
    if _try_set(comp, "volumetric_fog_scattering_distribution", 0.5):
        applied.append("volumetric_scattering_distribution")
    if _try_set(comp, "start_distance", 0.0):
        applied.append("start_distance=0")
    return applied


def _ensure_exponential_height_fog(
    homestead_centroid: list[float] | None,
    *,
    world=None,
    mrq_visible_sky: bool = False,
) -> dict:
    """Height fog gives readable horizon/sky tint when MRQ deferred shows void black."""
    cx, cy, cz = _homestead_centroid_xyz(homestead_centroid)
    actors = _actors_for_world(world)
    for a in actors:
        if not a:
            continue
        cls = a.get_class().get_name() if a.get_class() else ""
        if "ExponentialHeightFog" in cls or "HeightFog" in cls:
            cfg = _configure_height_fog(a, mrq_visible_sky=mrq_visible_sky)
            return {
                "present": True,
                "spawned": False,
                "label": _actor_label(a),
                "configured": cfg,
                "world_context": _world_path_label(world),
            }
    fog_cls = getattr(unreal, "ExponentialHeightFog", None)
    if fog_cls is None:
        return {"present": False, "spawned": False, "error": "ExponentialHeightFog class missing"}
    loc = unreal.Vector(cx, cy, cz)
    actor = _spawn_actor_in_world(world, fog_cls, loc, unreal.Rotator(0.0, 0.0, 0.0))
    if actor:
        cfg = _configure_height_fog(actor, mrq_visible_sky=mrq_visible_sky)
        try:
            actor.set_actor_label(TMP_HEIGHT_FOG_LABEL)
            if _is_editor_world(world):
                actor.set_folder_path(TMP_PA_E_ARRANGE_FOLDER)
        except Exception:
            pass
        return {
            "present": True,
            "spawned": True,
            "label": TMP_HEIGHT_FOG_LABEL,
            "configured": cfg,
            "world_context": _world_path_label(world),
        }
    return {"present": False, "spawned": False, "error": "spawn_failed"}


def _recapture_skylights_in_actors(actors: list) -> int:
    count = 0
    for a in actors:
        if not a:
            continue
        cls = a.get_class().get_name() if a.get_class() else ""
        if "SkyLight" not in cls:
            continue
        comp = _light_component(a)
        if comp and _invoke_recapture_skylight(comp):
            count += 1
    return count


def refresh_mrq_pie_skylight_recapture(world=None) -> dict[str, Any]:
    """Late RecaptureSky after atmo/fog/moon — call from MRQ wait ticks during warm-up."""
    w = world
    if w is None:
        w, _label = resolve_mrq_pie_render_world()
    actors = _actors_for_world(w)
    count = _recapture_skylights_in_actors(actors)
    return {
        "skylight_recaptures": count,
        "world_context": _world_path_label(w),
    }


def reconfigure_pa_e_mrq_night_fixtures(
    homestead_centroid: list[float] | None = None,
    *,
    world=None,
    mrq_pie_fill: bool = False,
) -> dict:
    """Moon AtmosphereSunLightIndex 0 + SkyLight fill in target world."""
    actors = _actors_for_world(world)
    tuned: list[dict] = []
    recaptures = 0
    cx, cy, cz = _homestead_centroid_xyz(homestead_centroid)
    target = unreal.Vector(cx, cy, cz)
    mrq_fill = mrq_pie_fill or _world_path_label(world) in ("pie", "runtime")

    for a in actors:
        if not a:
            continue
        label = _actor_label(a)
        label_l = label.lower()
        cls = a.get_class().get_name() if a.get_class() else ""

        if "DirectionalLight" in cls and (
            label == TMP_MOON_LABEL or any(n in label_l for n in _MOON_LABEL_NEEDLES)
        ):
            try:
                moon_loc = a.get_actor_location()
                moon_rot = unreal.MathLibrary.find_look_at_rotation(moon_loc, target)
                a.set_actor_rotation(moon_rot, False)
            except Exception:
                pass
            cfg = _configure_directional_moon(
                a,
                atmosphere_sun_index=MRQ_PIE_ATMOSPHERE_SUN_INDEX,
                mrq_key_boost=mrq_fill,
            )
            tuned.append({"label": label, "class": cls, "configured": cfg})
            continue

        if "SkyLight" in cls:
            cfg = _configure_skylight(
                a,
                recapture=not mrq_fill,
                mrq_ambient_fill=mrq_fill,
            )
            if "recapture_sky" in cfg:
                recaptures += 1
            tuned.append({"label": label, "class": cls, "configured": cfg})
            continue

        if label == TMP_CABIN_WARM_LABEL or any(n in label_l for n in _CABIN_WARM_NEEDLES):
            if "PointLight" in cls or "SpotLight" in cls or "RectLight" in cls:
                tuned.append(
                    {
                        "label": label,
                        "class": cls,
                        "configured": _configure_cabin_warm_point(a),
                    }
                )

    if not mrq_fill:
        recaptures += _recapture_skylights_in_actors(actors)
    return {
        "lights_reconfigured": tuned,
        "skylight_recaptures": recaptures,
        "homestead_centroid_used": [cx, cy, cz],
        "world_context": _world_path_label(world),
        "atmosphere_sun_index": MRQ_PIE_ATMOSPHERE_SUN_INDEX,
        "mrq_skylight_hemisphere_fill": mrq_fill,
    }


def apply_mrq_pie_homestead_night_stack(
    homestead_centroid: list[float] | None = None,
    *,
    world=None,
    world_label: str | None = None,
) -> dict:
    """Full MRQ PIE night stack in the world that will be rendered (Editor pre-pass and/or PIE)."""
    centroid_meta = _sanitize_homestead_centroid(homestead_centroid)
    used_centroid = centroid_meta["used"]
    wlabel = world_label or _world_path_label(world)
    mrq_pie = wlabel in ("pie", "game_world", "runtime")
    exposure = apply_mrq_pie_night_exposure_cvars(world)
    tod = _apply_tod_phase_in_world(world, phase=2)
    reseed = reseed_pa_e_tmp_night_fixtures(
        used_centroid, force_mrq_pie=True, world=world
    )
    atmosphere = _ensure_sky_atmosphere(used_centroid, world=world)
    height_fog = _ensure_exponential_height_fog(
        used_centroid, world=world, mrq_visible_sky=mrq_pie
    )
    reconfigure = reconfigure_pa_e_mrq_night_fixtures(
        used_centroid, world=world, mrq_pie_fill=mrq_pie
    )
    actors = _actors_for_world(world)
    tune = apply_homestead_night_tune(actors)
    late_recapture = (
        refresh_mrq_pie_skylight_recapture(world)
        if mrq_pie and not reconfigure.get("mrq_skylight_hemisphere_fill")
        else {"skylight_recaptures": 0, "skipped": "hemisphere_fill"}
    )
    verify = verify_homestead_night_lighting_stack(actors)
    visible_sky_ok = bool(
        verify.get("stack_ok")
        and (atmosphere.get("present"))
        and (height_fog.get("present"))
    )
    return {
        "ok": bool(exposure.get("ok") and tune.get("ok") and verify.get("stack_ok")),
        "world_context": wlabel,
        "homestead_centroid": centroid_meta,
        "exposure_cvars": exposure,
        "time_of_day": tod,
        "tmp_fixture_reseed": reseed,
        "sky_atmosphere": atmosphere,
        "height_fog": height_fog,
        "mrq_fixture_reconfigure": reconfigure,
        "late_skylight_recapture": late_recapture,
        "night_tune": tune,
        "lighting_stack_verify": verify,
        "stack_ok": bool(verify.get("stack_ok")),
        "visible_sky_stack_ok": visible_sky_ok,
        "atmosphere_sun_index": MRQ_PIE_ATMOSPHERE_SUN_INDEX,
        "note": (
            "PIE MRQ: height fog + atmo @ world origin + hemisphere skylight fill; "
            "re-apply during warm-up ticks before one-frame still."
        ),
    }


def apply_mrq_pie_homestead_night_stack_in_render_world(
    homestead_centroid: list[float] | None = None,
) -> dict[str, Any]:
    """Apply night stack in MRQ PIE / game world (call after executor starts PIE)."""
    world, label = resolve_mrq_pie_render_world()
    if world is None:
        return {
            "ok": False,
            "stack_ok": False,
            "error": "no_render_world",
            "world_context": label,
        }
    out = apply_mrq_pie_homestead_night_stack(
        homestead_centroid, world=world, world_label=label
    )
    out["render_world_resolved"] = True
    return out


def reseed_pa_e_tmp_night_fixtures(
    homestead_centroid: list[float] | None = None,
    *,
    force_mrq_pie: bool = False,
    world=None,
) -> dict:
    """Idempotent TMP moon + skylight + cabin warm after load_level (prove without saving .umap)."""
    actors = _actors_for_world(world)
    verify_before = verify_homestead_night_lighting_stack(actors)
    if verify_before.get("stack_ok") and not force_mrq_pie:
        return {
            "skipped": True,
            "reason": "stack_already_ok",
            "verify_before": verify_before,
            "verify_after": verify_before,
            "spawned": [],
        }

    cx, cy, cz = _homestead_centroid_xyz(homestead_centroid)
    target = unreal.Vector(cx, cy, cz)
    moon_loc = unreal.Vector(cx - 8000.0, cy - 6000.0, cz + 12000.0)
    sky_loc = unreal.Vector(cx, cy, cz + 400.0)
    cabin_loc = unreal.Vector(cx + 200.0, cy + 150.0, cz + 80.0)

    spawned: list[dict] = []
    try:
        moon_rot = unreal.MathLibrary.find_look_at_rotation(moon_loc, target)
    except Exception:
        moon_rot = unreal.Rotator(roll=0.0, pitch=-45.0, yaw=0.0)

    moon, moon_new = _spawn_light_if_missing(
        actors,
        TMP_MOON_LABEL,
        unreal.DirectionalLight,
        moon_loc,
        moon_rot,
        world=world,
    )
    mrq_fill = force_mrq_pie and _world_path_label(world) in ("pie", "runtime")
    if moon:
        cfg = _configure_directional_moon(
            moon,
            atmosphere_sun_index=MRQ_PIE_ATMOSPHERE_SUN_INDEX,
            mrq_key_boost=mrq_fill,
        )
        if moon_new:
            spawned.append({"label": TMP_MOON_LABEL, "class": "DirectionalLight", "configured": cfg})
        elif force_mrq_pie:
            spawned.append({"label": TMP_MOON_LABEL, "class": "DirectionalLight", "reconfigured": cfg})

    sky, sky_new = _spawn_light_if_missing(
        actors, TMP_SKY_LABEL, unreal.SkyLight, sky_loc, world=world
    )
    if sky:
        cfg = _configure_skylight(sky)
        if sky_new:
            spawned.append({"label": TMP_SKY_LABEL, "class": "SkyLight", "configured": cfg})
        elif force_mrq_pie:
            spawned.append({"label": TMP_SKY_LABEL, "class": "SkyLight", "reconfigured": cfg})

    cabin, cabin_new = _spawn_light_if_missing(
        actors, TMP_CABIN_WARM_LABEL, unreal.PointLight, cabin_loc, world=world
    )
    if cabin:
        cfg = _configure_cabin_warm_point(cabin)
        if cabin_new:
            spawned.append(
                {"label": TMP_CABIN_WARM_LABEL, "class": "PointLight", "configured": cfg}
            )
        elif force_mrq_pie:
            spawned.append(
                {"label": TMP_CABIN_WARM_LABEL, "class": "PointLight", "reconfigured": cfg}
            )

    actors_after = _actors_for_world(world)
    verify_after = verify_homestead_night_lighting_stack(actors_after)
    out: dict = {
        "skipped": False,
        "force_mrq_pie": force_mrq_pie,
        "world_context": _world_path_label(world),
        "homestead_centroid_used": [cx, cy, cz],
        "homestead_centroid_sanitize": _sanitize_homestead_centroid(homestead_centroid),
        "spawned": spawned,
        "verify_before": verify_before,
        "verify_after": verify_after,
        "stack_ok_after_reseed": bool(verify_after.get("stack_ok")),
        "note": "TMP actors under VS_MVP/TMP_PA_E_Arrange — re-run after load_level; optional KEEP-LOCAL save.",
    }
    if force_mrq_pie:
        out["reason"] = "mrq_pie_force_reconfigure"
    return out


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

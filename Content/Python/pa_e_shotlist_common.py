"""Shared PA-E shotlist constants and helpers (paths, validation, level/camera).

Used by capture_shotlist_mrq.py (primary) and capture_shotlist_viewport.py (diagnostic).
"""
from __future__ import annotations

import json
import os
import shutil
from typing import Any, Optional

try:
    import unreal
except ImportError:
    unreal = None  # type: ignore

LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
CINEMATICS_PA_E_DIR = "/Game/HomeWorld/Cinematics/PA_E"
RES_X, RES_Y = 1920, 1080
MIN_BYTES = 50 * 1024
MIN_MEAN_LUMINANCE = 8.0
DESKTOP_PA_E = r"C:\Users\User\Desktop\HomeWorld_PA_E"
ONE_FRAME_START = 0
ONE_FRAME_END = 1
# MRQ warm-up (Epic MoviePipelineAntiAliasingSetting — engine + GPU discard frames)
MRQ_ENGINE_WARMUP_COUNT = 32
MRQ_RENDER_WARMUP_COUNT = 8
MRQ_CAMERA_CUT_PREROLL_FRAME = -32

PROVE_CRITERIA = {
    "requires_lit_homestead_visible": True,
    "min_bytes": MIN_BYTES,
    "min_mean_luminance": MIN_MEAN_LUMINANCE,
    "file_exists_alone_is_not_pass": True,
    "note": (
        "Lead-visible scene content in Editor must appear in stills; near-black PNGs "
        "indicate wrong pose/game-view/buffer/camera binding, not missing level content."
    ),
}

SHOTS = (
    {
        "id": "shot1",
        "filename": "Shot1_lookout.png",
        "sequence_name": "LS_PA_E_Shot1_lookout",
        "camera_labels": ("CAM_Hero", "Shot1", "Lookout", "Hero"),
        "fallback_location_m": (-9.0, -4.0, 5.8),
        "fallback_rotation_deg": (41.61, 0.0, -108.43),
        "fallback_source": "Docs/handoffs/P6_FIX_shot1.md + AssetCreation CAM_Hero",
    },
    {
        "id": "shot2",
        "filename": "Shot2_cabin_garden.png",
        "sequence_name": "LS_PA_E_Shot2_cabin_garden",
        "camera_labels": ("CAM_CabinClose", "Shot2", "Cabin", "Garden", "CAM_CabinGarden"),
        "fallback_location_m": (-4.0, -2.5, 1.6),
        "fallback_rotation_deg": (81.08, 0.0, -26.56),
        "fallback_source": "Lib/00_Core/GRAYBOX_LAYOUT.md CAM_CabinClose (blender euler from JSON)",
    },
)


def log(prefix: str, msg: str, data: Optional[dict] = None) -> None:
    line = prefix + " " + msg
    if data:
        line += " " + json.dumps(data, default=str)
    if unreal is not None:
        unreal.log(line)
    print(line)


def abs_path(path: str) -> str:
    return os.path.abspath(os.path.normpath(path))


def project_dir() -> str:
    if unreal is None:
        return abs_path(os.getcwd())
    raw = unreal.Paths.project_dir()
    if raw:
        return abs_path(raw)
    return abs_path(os.getcwd())


def saved_pa_e_dir() -> str:
    path = abs_path(os.path.join(project_dir(), "Saved", "Screenshots", "PA_E"))
    os.makedirs(path, exist_ok=True)
    return path


def shot_dest_abs(filename: str) -> str:
    return abs_path(os.path.join(saved_pa_e_dir(), filename))


def mrq_staging_dir(shot_id: str) -> str:
    path = abs_path(os.path.join(project_dir(), "Saved", "Screenshots", "PA_E", "mrq_staging", shot_id))
    os.makedirs(path, exist_ok=True)
    return path


def report_path() -> str:
    return abs_path(os.path.join(project_dir(), "Saved", "pa_e_capture_report.json"))


def sequence_asset_path(sequence_name: str) -> str:
    return f"{CINEMATICS_PA_E_DIR}/{sequence_name}"


def pil_available() -> bool:
    try:
        from PIL import Image  # noqa: F401
        return True
    except ImportError:
        return False


def meters_to_ue(loc_m: tuple[float, float, float]) -> "unreal.Vector":
    x, y, z = loc_m
    return unreal.Vector(x * 100.0, -y * 100.0, z * 100.0)


def euler_deg_to_rotator(pitch: float, yaw: float, roll: float) -> "unreal.Rotator":
    return unreal.Rotator(pitch=pitch, yaw=yaw, roll=roll)


def actor_label(actor) -> str:
    try:
        return actor.get_actor_label() or actor.get_name()
    except Exception:
        return actor.get_name() if actor else ""


def find_camera(needles: tuple[str, ...]):
    cams = []
    for a in unreal.EditorLevelLibrary.get_all_level_actors():
        if not a:
            continue
        cls = a.get_class().get_name() if a.get_class() else ""
        if "Camera" not in cls:
            continue
        cams.append(a)
    needle_l = [n.lower() for n in needles]
    for needle in needle_l:
        for a in cams:
            label = actor_label(a).lower()
            name = a.get_name().lower()
            if label == needle or name == needle:
                return a
    for a in cams:
        label = actor_label(a).lower()
        name = a.get_name().lower()
        if any(n in label or n in name for n in needle_l):
            return a
    return None


def load_level(log_prefix: str) -> bool:
    log(log_prefix, "load_level start", {"path": LEVEL_PATH})
    try:
        subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        if subsys and hasattr(subsys, "load_level"):
            subsys.load_level(LEVEL_PATH)
            log(log_prefix, "load_level via LevelEditorSubsystem", {"ok": True})
            return True
    except Exception as e:
        log(log_prefix, "load_level LevelEditorSubsystem failed", {"error": str(e)})
    try:
        ok = unreal.EditorLevelLibrary.load_level(LEVEL_PATH)
        log(log_prefix, "load_level via EditorLevelLibrary", {"ok": bool(ok)})
        return bool(ok)
    except Exception as e:
        log(log_prefix, "load_level failed", {"error": str(e)})
        return False


def purge_stale_shot_pngs(dest_abs: str) -> dict[str, Any]:
    basename = os.path.basename(dest_abs)
    candidates: set[str] = {abs_path(dest_abs)}
    candidates.add(abs_path(os.path.join(DESKTOP_PA_E, basename)))
    removed: list[str] = []
    errors: list[dict[str, str]] = []
    for p in sorted(candidates):
        if not os.path.isfile(p):
            continue
        try:
            os.remove(p)
            removed.append(p)
        except OSError as e:
            errors.append({"path": p, "error": str(e)})
    return {"basename": basename, "removed": removed, "remove_errors": errors}


def mean_luminance(path: str) -> Optional[float]:
    try:
        from PIL import Image
    except ImportError:
        return None
    try:
        with Image.open(path) as im:
            im = im.convert("L")
            hist = im.histogram()
            total = sum(hist) or 1
            mean = sum(i * hist[i] for i in range(256)) / total
            return float(mean)
    except Exception:
        return None


def validate_png(path: Optional[str]) -> dict:
    out: dict[str, Any] = {"path": path, "pass": False}
    if not path or not os.path.isfile(path):
        out["error"] = "file_missing"
        return out
    size = os.path.getsize(path)
    out["bytes"] = size
    if size < MIN_BYTES:
        out["error"] = "file_too_small"
        return out
    lum = mean_luminance(path)
    out["mean_luminance"] = lum
    out["pil_available"] = pil_available()
    if lum is None:
        if not pil_available():
            out["error"] = "pil_unavailable"
            out["install_note"] = "Install Pillow into the Unreal Editor Python used by -ExecutePythonScript"
        else:
            out["error"] = "luminance_read_failed"
        return out
    if lum < MIN_MEAN_LUMINANCE:
        out["error"] = "near_black"
        return out
    out["pass"] = True
    return out


def copy_to_desktop(local_path: str, filename: str) -> dict:
    dest_dir = DESKTOP_PA_E
    dest = os.path.join(dest_dir, filename)
    try:
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(local_path, dest)
        return {"copied": True, "desktop_path": dest}
    except Exception as e:
        return {"copied": False, "desktop_path": dest, "error": str(e)}


def resolve_camera_transform(shot: dict, cam) -> tuple[Any, Any, dict[str, Any]]:
    meta: dict[str, Any] = {"used_camera_actor": bool(cam)}
    if cam:
        loc = cam.get_actor_location()
        rot = cam.get_actor_rotation()
        meta["camera_label"] = actor_label(cam)
        meta["location"] = [loc.x, loc.y, loc.z]
        meta["rotation"] = [rot.pitch, rot.yaw, rot.roll]
        return loc, rot, meta
    loc = meters_to_ue(tuple(shot["fallback_location_m"]))
    rot = euler_deg_to_rotator(*tuple(shot["fallback_rotation_deg"]))
    meta["fallback_location_m"] = list(shot["fallback_location_m"])
    meta["fallback_rotation_deg"] = list(shot["fallback_rotation_deg"])
    return loc, rot, meta


def ensure_cinematics_folder() -> None:
    if not unreal.EditorAssetLibrary.does_directory_exist(CINEMATICS_PA_E_DIR):
        unreal.EditorAssetLibrary.make_directory(CINEMATICS_PA_E_DIR)


def desktop_conductor_checklist() -> list[str]:
    """Checks Conductor runs on DESKTOP when capture fails or MRQ plugins block."""
    return [
        "Safe-Build after MovieRenderPipeline plugins; confirm MRQ Python types import.",
        "Open L_VS_MVP_Markers; rotate viewport — Lead must see homestead geometry/lighting.",
        "Select CAM_Hero / CAM_CabinClose; confirm framing matches Shot 1/2 before capture.",
        "Run execute_python_script('capture_shotlist.py'); read Saved/pa_e_capture_report.json.",
        "If AL diagnostic (capture_shotlist_viewport.py) still near-black: OPEN viewport capture bug — wrong game-view, pilot, or HighResShot buffer — not 'no content'.",
        "PASS only when both PNGs pass bytes + mean_luminance gates and show lit homestead (not empty/unlit buffer).",
    ]


def finish_loading_before_capture() -> dict[str, Any]:
    meta: dict[str, Any] = {"called": False}
    try:
        fn = getattr(unreal.AutomationLibrary, "finish_loading_before_screenshot", None)
        if callable(fn):
            fn()
            meta["called"] = True
    except Exception as e:
        meta["error"] = str(e)
    return meta


def apply_lit_game_view_for_capture() -> dict[str, Any]:
    """Align editor with lit + game view before MRQ/AL (same intent as viewport script)."""
    applied: dict[str, Any] = {}
    lit_method: Optional[str] = None
    try:
        set_vm = getattr(unreal.AutomationLibrary, "set_editor_viewport_view_mode", None)
        if callable(set_vm):
            mode = getattr(unreal, "ViewModeIndex", None)
            if mode is not None and hasattr(mode, "VMI_LIT"):
                set_vm(mode.VMI_LIT)
                lit_method = "AutomationLibrary.set_editor_viewport_view_mode(VMI_LIT)"
    except Exception as e:
        applied["automation_view_mode_error"] = str(e)
    if not lit_method:
        try:
            unreal.SystemLibrary.execute_console_command(None, "viewmode lit")
            lit_method = "console_viewmode_lit"
        except Exception as e:
            applied["viewmode_error"] = str(e)
    applied["viewmode"] = lit_method or "unknown"

    game_view = False
    try:
        ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
        if ues and hasattr(ues, "editor_set_game_view"):
            ues.editor_set_game_view(True)
            game_view = True
            applied["game_view_method"] = "UnrealEditorSubsystem.editor_set_game_view"
    except Exception as e:
        applied["game_view_error"] = str(e)
    if not game_view:
        try:
            unreal.SystemLibrary.execute_console_command(None, "gameview")
            game_view = True
            applied["game_view_method"] = "console_gameview"
        except Exception:
            pass
    applied["game_view"] = game_view
    return applied


def sync_editor_viewport_to_camera(cam, loc, rot) -> dict[str, Any]:
    """Pose editor viewport to shot camera (diagnostic — Lead-visible framing check)."""
    meta: dict[str, Any] = {"viewport_set": False, "pilot": False}
    try:
        ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
        if ues and hasattr(ues, "set_level_viewport_camera_info"):
            ues.set_level_viewport_camera_info(loc, rot)
            meta["viewport_set"] = True
            meta["viewport_api"] = "UnrealEditorSubsystem.set_level_viewport_camera_info"
    except Exception as e:
        meta["viewport_ues_error"] = str(e)
    if not meta["viewport_set"]:
        try:
            unreal.EditorLevelLibrary.set_level_viewport_camera_info(loc, rot)
            meta["viewport_set"] = True
            meta["viewport_api"] = "EditorLevelLibrary.set_level_viewport_camera_info"
        except Exception as e:
            meta["viewport_error"] = str(e)
    if cam:
        try:
            unreal.EditorLevelLibrary.pilot_level_actor(cam)
            meta["pilot"] = True
            meta["pilot_label"] = actor_label(cam)
        except Exception as e:
            meta["pilot_error"] = str(e)
    meta["location"] = [loc.x, loc.y, loc.z]
    meta["rotation"] = [rot.pitch, rot.yaw, rot.roll]
    return meta

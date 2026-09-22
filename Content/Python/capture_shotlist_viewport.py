"""PA-E / shotlist viewport capture — Editor Python only.

Loads L_VS_MVP_Markers, poses level viewport for Shot 1 (lookout) and Shot 2
(cabin/garden), lit + game view, take_high_res_screenshot (force_game_view),
validates PNGs, writes Saved/pa_e_capture_report.json.

Run: MCP execute_python_script("capture_shotlist_viewport.py") or UnrealEditor-Cmd
-ExecutePythonScript=... (uses vnp_editor_keep_alive).

Does NOT claim shotlist PASS — DESKTOP must verify report + stills.
"""
from __future__ import annotations

import json
import math
import os
import shutil
import time
from typing import Any, Optional

try:
    import unreal
except ImportError:
    print("capture_shotlist_viewport: Run inside Unreal Editor.")
    raise

PREFIX = "capture_shotlist_viewport:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
RES_X, RES_Y = 1920, 1080
MIN_BYTES = 50 * 1024
MIN_MEAN_LUMINANCE = 8.0  # reject near-black (0–255 scale)
SETTLE_FRAMES = 12
WAIT_FILE_SEC = 45.0

DESKTOP_PA_E = r"C:\Users\User\Desktop\HomeWorld_PA_E"

SHOTS = (
    {
        "id": "shot1",
        "filename": "Shot1_lookout.png",
        "camera_labels": ("CAM_Hero", "Shot1", "Lookout", "Hero"),
        "fallback_location_m": (-9.0, -4.0, 5.8),
        "fallback_rotation_deg": (41.61, 0.0, -108.43),
        "fallback_source": "Docs/handoffs/P6_FIX_shot1.md + AssetCreation CAM_Hero",
    },
    {
        "id": "shot2",
        "filename": "Shot2_cabin_garden.png",
        "camera_labels": ("CAM_CabinClose", "Shot2", "Cabin", "Garden", "CAM_CabinGarden"),
        "fallback_location_m": (-4.0, -2.5, 1.6),
        "fallback_rotation_deg": (81.08, 0.0, -26.56),
        "fallback_source": "Lib/00_Core/GRAYBOX_LAYOUT.md CAM_CabinClose (blender euler from JSON)",
    },
)


def _log(msg: str, data: Optional[dict] = None) -> None:
    line = PREFIX + " " + msg
    if data:
        line += " " + json.dumps(data, default=str)
    unreal.log(line)
    print(line)


def _project_dir() -> str:
    return unreal.Paths.project_dir()


def _saved_pa_e_dir() -> str:
    path = os.path.join(_project_dir(), "Saved", "Screenshots", "PA_E")
    os.makedirs(path, exist_ok=True)
    return path


def _report_path() -> str:
    return os.path.join(_project_dir(), "Saved", "pa_e_capture_report.json")


def _meters_to_ue(loc_m: tuple[float, float, float]) -> unreal.Vector:
    x, y, z = loc_m
    return unreal.Vector(x * 100.0, -y * 100.0, z * 100.0)


def _euler_deg_to_rotator(pitch: float, yaw: float, roll: float) -> unreal.Rotator:
    return unreal.Rotator(pitch=pitch, yaw=yaw, roll=roll)


def _blender_euler_rad_to_rotator(eulers: tuple[float, float, float]) -> unreal.Rotator:
    rx, ry, rz = eulers
    pitch = math.degrees(rx)
    yaw = math.degrees(-rz)
    roll = math.degrees(ry)
    return unreal.Rotator(pitch=pitch, yaw=yaw, roll=roll)


def _actor_label(actor) -> str:
    try:
        return actor.get_actor_label() or actor.get_name()
    except Exception:
        return actor.get_name() if actor else ""


def _find_camera(needles: tuple[str, ...]):
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


def _load_level() -> bool:
    _log("load_level start", {"path": LEVEL_PATH})
    try:
        subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        if subsys and hasattr(subsys, "load_level"):
            subsys.load_level(LEVEL_PATH)
            _log("load_level via LevelEditorSubsystem", {"ok": True})
            return True
    except Exception as e:
        _log("load_level LevelEditorSubsystem failed", {"error": str(e)})
    try:
        ok = unreal.EditorLevelLibrary.load_level(LEVEL_PATH)
        _log("load_level via EditorLevelLibrary", {"ok": bool(ok)})
        return bool(ok)
    except Exception as e:
        _log("load_level failed", {"error": str(e)})
        return False


def _set_lit_and_game_view() -> dict:
    applied: dict[str, Any] = {}
    try:
        unreal.SystemLibrary.execute_console_command(None, "viewmode lit")
        applied["viewmode"] = "lit"
    except Exception as e:
        applied["viewmode_error"] = str(e)
    game_view = False
    try:
        ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
        if ues and hasattr(ues, "editor_set_game_view"):
            ues.editor_set_game_view(True)
            game_view = True
    except Exception as e:
        applied["game_view_error"] = str(e)
    applied["game_view"] = game_view
    return applied


def _settle_viewport(frames: int = SETTLE_FRAMES) -> None:
    for _ in range(frames):
        try:
            if hasattr(unreal.AutomationLibrary, "automation_wait_for_loading"):
                unreal.AutomationLibrary.automation_wait_for_loading(None, 0.05)
        except Exception:
            pass
        time.sleep(0.05)


def _pose_viewport(
    cam,
    fallback_loc_m: tuple[float, float, float],
    fallback_rot_deg: tuple[float, float, float],
) -> dict:
    meta: dict[str, Any] = {"used_camera_actor": bool(cam)}
    if cam:
        loc = cam.get_actor_location()
        rot = cam.get_actor_rotation()
        meta["camera_label"] = _actor_label(cam)
        meta["location"] = [loc.x, loc.y, loc.z]
        meta["rotation"] = [rot.pitch, rot.yaw, rot.roll]
    else:
        loc = _meters_to_ue(fallback_loc_m)
        rot = _euler_deg_to_rotator(*fallback_rot_deg)
        meta["fallback_location_m"] = list(fallback_loc_m)
        meta["fallback_rotation_deg"] = list(fallback_rot_deg)
    try:
        unreal.EditorLevelLibrary.set_level_viewport_camera_info(loc, rot)
        meta["viewport_set"] = True
    except Exception as e:
        meta["viewport_set"] = False
        meta["viewport_error"] = str(e)
    if cam:
        try:
            unreal.EditorLevelLibrary.pilot_level_actor(cam)
            meta["pilot"] = True
        except Exception as e:
            meta["pilot"] = False
            meta["pilot_error"] = str(e)
    return meta


def _take_high_res_screenshot(
    filename_for_ue: str,
    camera,
) -> tuple[str, Optional[str]]:
    """Single capture; returns (method, error)."""
    last_err: Optional[str] = None
    attempts = (
        ("kwargs_force_gv", lambda: unreal.AutomationLibrary.take_high_res_screenshot(
            RES_X, RES_Y, filename_for_ue, camera=camera, force_game_view=True
        )),
        ("positional_force_gv", lambda: unreal.AutomationLibrary.take_high_res_screenshot(
            RES_X, RES_Y, filename_for_ue, camera, True
        )),
        ("legacy", lambda: unreal.AutomationLibrary.take_high_res_screenshot(
            RES_X, RES_Y, filename_for_ue, camera
        )),
    )
    for name, fn in attempts:
        try:
            fn()
            return name, None
        except TypeError:
            continue
        except Exception as e:
            last_err = str(e)
    try:
        rel = "Saved/Screenshots/PA_E/" + os.path.basename(filename_for_ue)
        unreal.SystemLibrary.execute_console_command(
            None,
            'HighResShot %dx%d filename="%s"' % (RES_X, RES_Y, rel.replace("\\", "/")),
        )
        return "HighResShot_console", None
    except Exception as e2:
        return "failed", last_err or str(e2)


def _newest_png_under(root: str, since_mtime: float) -> Optional[str]:
    if not os.path.isdir(root):
        return None
    best: Optional[str] = None
    best_m = since_mtime
    for dirpath, _dirs, files in os.walk(root):
        for f in files:
            if not f.lower().endswith(".png"):
                continue
            p = os.path.join(dirpath, f)
            try:
                m = os.path.getmtime(p)
            except OSError:
                continue
            if m >= since_mtime and m >= best_m:
                best = p
                best_m = m
    return best


def _wait_for_capture(dest_abs: str, since_mtime: float) -> Optional[str]:
    """Wait for PNG at dest or newest under Saved/Screenshots."""
    deadline = time.time() + WAIT_FILE_SEC
    screens = os.path.join(_project_dir(), "Saved", "Screenshots")
    base = os.path.basename(dest_abs)
    while time.time() < deadline:
        if os.path.isfile(dest_abs) and os.path.getsize(dest_abs) >= MIN_BYTES:
            return dest_abs
        for candidate in (
            _newest_png_under(_saved_pa_e_dir(), since_mtime),
            _newest_png_under(screens, since_mtime),
        ):
            if candidate and os.path.getsize(candidate) >= MIN_BYTES:
                if candidate != dest_abs:
                    try:
                        shutil.copy2(candidate, dest_abs)
                    except Exception:
                        return candidate
                return dest_abs if os.path.isfile(dest_abs) else candidate
        if os.path.isfile(dest_abs) and os.path.getsize(dest_abs) > 0:
            time.sleep(0.25)
            continue
        alt = os.path.join(screens, "WindowsEditor", base)
        if os.path.isfile(alt):
            try:
                shutil.copy2(alt, dest_abs)
            except Exception:
                return alt
        time.sleep(0.25)
    return dest_abs if os.path.isfile(dest_abs) else None


def _mean_luminance(path: str) -> Optional[float]:
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


def _validate_png(path: Optional[str]) -> dict:
    out: dict[str, Any] = {"path": path, "pass": False}
    if not path or not os.path.isfile(path):
        out["error"] = "file_missing"
        return out
    size = os.path.getsize(path)
    out["bytes"] = size
    if size < MIN_BYTES:
        out["error"] = "file_too_small"
        return out
    lum = _mean_luminance(path)
    out["mean_luminance"] = lum
    if lum is not None and lum < MIN_MEAN_LUMINANCE:
        out["error"] = "near_black"
        return out
    out["pass"] = True
    return out


def _copy_to_desktop(local_path: str, filename: str) -> dict:
    dest_dir = DESKTOP_PA_E
    dest = os.path.join(dest_dir, filename)
    try:
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(local_path, dest)
        return {"copied": True, "desktop_path": dest}
    except Exception as e:
        return {"copied": False, "desktop_path": dest, "error": str(e)}


def _capture_shot(shot: dict) -> dict:
    _log("shot start", {"id": shot["id"]})
    cam = _find_camera(shot["camera_labels"])
    pose_meta = _pose_viewport(
        cam,
        tuple(shot["fallback_location_m"]),
        tuple(shot["fallback_rotation_deg"]),
    )
    pose_meta["fallback_source"] = shot.get("fallback_source")
    _settle_viewport()
    dest = os.path.join(_saved_pa_e_dir(), shot["filename"])
    since = time.time()
    rel_name = "PA_E/" + shot["filename"]
    method, cap_err = _take_high_res_screenshot(rel_name, cam if cam else None)
    _settle_viewport(frames=6)
    resolved = _wait_for_capture(dest, since)
    validation = _validate_png(resolved)
    desktop = _copy_to_desktop(resolved, shot["filename"]) if resolved else {"copied": False}
    entry = {
        "id": shot["id"],
        "filename": shot["filename"],
        "capture_method": method,
        "capture_error": cap_err,
        "saved_path": resolved,
        "pose": pose_meta,
        "validation": validation,
        "desktop_copy": desktop,
        "pass": bool(validation.get("pass")),
    }
    _log("shot done", {"id": shot["id"], "pass": entry["pass"], "bytes": validation.get("bytes")})
    return entry


def main() -> None:
    _log("started")
    keep_ok = False
    try:
        import vnp_editor_keep_alive as keep

        keep_ok = keep.arm()
    except Exception as e:
        _log("keep_alive import/arm skipped", {"error": str(e)})

    level_ok = _load_level()
    viewport_prep = _set_lit_and_game_view()
    _settle_viewport()

    try:
        unreal.SystemLibrary.execute_console_command(None, "hw.TimeOfDay.Phase 2")
        viewport_prep["night_phase"] = 2
    except Exception:
        viewport_prep["night_phase"] = "skipped"

    results = [_capture_shot(s) for s in SHOTS]
    all_pass = all(r.get("pass") for r in results)

    report = {
        "ok": all_pass,
        "prefix": PREFIX.strip(":"),
        "level_path": LEVEL_PATH,
        "level_loaded": level_ok,
        "viewport_prep": viewport_prep,
        "keep_python_script_alive": keep_ok,
        "resolution": [RES_X, RES_Y],
        "shots": results,
        "policy": "Does not claim shotlist PASS — verify on DESKTOP; no host ImageGrab",
        "ladder_doc": "docs/Automation/CAPTURE_REDUNDANCY.md",
    }
    with open(_report_path(), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    _log("report written", {"path": _report_path(), "all_pass": all_pass})

    try:
        if keep_ok:
            import vnp_editor_keep_alive as keep

            keep.disarm()
    except Exception:
        pass

    _log("finished", {"all_pass": all_pass})


if __name__ == "__main__":
    main()

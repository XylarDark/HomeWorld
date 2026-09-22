"""PA-E / shotlist viewport capture — Editor Python only.

Loads L_VS_MVP_Markers, poses level viewport for Shot 1 (lookout) and Shot 2
(cabin/garden), lit + game view, console HighResShot (primary) with
AutomationLibrary fallback if no PNG appears, validates PNGs, writes
Saved/pa_e_capture_report.json.

Console HighResShot parameter order per Epic UE 5.8 "Taking Screenshots":
  HighResShot filename=PATH (XxY OR Multiplier) ...
  https://dev.epicgames.com/documentation/en-us/unreal-engine/taking-screenshots-in-unreal-engine
HighResShot is a global one-request-per-tick flag — try one command form, wait
for file on disk, then try the next form only if the PNG is still missing.

Run: MCP execute_python_script("capture_shotlist_viewport.py") or UnrealEditor-Cmd
-ExecutePythonScript=... (uses vnp_editor_keep_alive).

Does NOT claim shotlist PASS — DESKTOP must verify report + stills.
"""
from __future__ import annotations

import json
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
INTER_SHOT_SETTLE_FRAMES = 24
POST_CONSOLE_SETTLE_FRAMES = 8
WAIT_FILE_SEC = 330.0
CAPTURE_DELAY_SEC = 0.35
STABLE_POLL_INTERVAL = 0.35
STABLE_SIZE_POLLS = 4
FINAL_DRAIN_SEC = 45.0

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


def _abs_path(path: str) -> str:
    """unreal.Paths.project_dir() may be relative to engine CWD — always normalize."""
    return os.path.abspath(os.path.normpath(path))


def _project_dir() -> str:
    raw = unreal.Paths.project_dir()
    if raw:
        return _abs_path(raw)
    return _abs_path(os.getcwd())


def _saved_pa_e_dir() -> str:
    path = _abs_path(os.path.join(_project_dir(), "Saved", "Screenshots", "PA_E"))
    os.makedirs(path, exist_ok=True)
    return path


def _shot_dest_abs(filename: str) -> str:
    return _abs_path(os.path.join(_saved_pa_e_dir(), filename))


def _path_for_ue(abs_path: str) -> str:
    """AutomationLibrary / HighResShot: absolute path, forward slashes."""
    return _abs_path(abs_path).replace("\\", "/")


def _pil_available() -> bool:
    try:
        from PIL import Image  # noqa: F401
        return True
    except ImportError:
        return False


def _mtime_at_least(path: str, since: float) -> bool:
    try:
        return os.path.getmtime(path) >= since - 0.05
    except OSError:
        return False


def _purge_stale_shot_pngs(dest_abs: str) -> dict[str, Any]:
    """Remove prior PNGs so wait/validation cannot latch stale frames."""
    basename = os.path.basename(dest_abs)
    candidates: set[str] = {_abs_path(dest_abs)}
    candidates.add(_abs_path(os.path.join(DESKTOP_PA_E, basename)))
    for root in _engine_search_roots():
        candidates.add(_abs_path(os.path.join(root, basename)))
        candidates.add(_abs_path(os.path.join(root, "PA_E", basename)))
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


def _engine_search_roots() -> list[str]:
    """UE often writes relative HighResShot paths under Engine Binaries Win64 (engine CWD)."""
    roots: list[str] = []
    seen: set[str] = set()

    def add(p: str) -> None:
        p = _abs_path(p)
        if p not in seen and os.path.isdir(p):
            seen.add(p)
            roots.append(p)

    try:
        eng = unreal.Paths.engine_dir()
        if eng:
            win64 = os.path.join(eng, "Binaries", "Win64")
            add(win64)
            add(os.path.join(win64, "PA_E"))
    except Exception:
        pass
    try:
        eng_b = unreal.Paths.engine_binary_dir()
        if eng_b:
            add(eng_b)
            add(os.path.join(eng_b, "PA_E"))
    except Exception:
        pass
    cwd = os.getcwd()
    add(cwd)
    add(os.path.join(cwd, "PA_E"))
    screens = os.path.join(_project_dir(), "Saved", "Screenshots")
    add(screens)
    add(_saved_pa_e_dir())
    add(os.path.join(screens, "WindowsEditor"))
    add(os.path.join(screens, "Windows"))
    return roots


def _report_path() -> str:
    return _abs_path(os.path.join(_project_dir(), "Saved", "pa_e_capture_report.json"))


def _meters_to_ue(loc_m: tuple[float, float, float]) -> unreal.Vector:
    x, y, z = loc_m
    return unreal.Vector(x * 100.0, -y * 100.0, z * 100.0)


def _euler_deg_to_rotator(pitch: float, yaw: float, roll: float) -> unreal.Rotator:
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


def _finish_loading_before_screenshot() -> dict[str, Any]:
    """Epic AutomationLibrary — flush streaming before capture when exposed."""
    meta: dict[str, Any] = {"called": False}
    try:
        fn = getattr(unreal.AutomationLibrary, "finish_loading_before_screenshot", None)
        if callable(fn):
            fn()
            meta["called"] = True
    except Exception as e:
        meta["error"] = str(e)
    return meta


def _set_lit_and_game_view() -> dict:
    applied: dict[str, Any] = {}
    lit_method: Optional[str] = None
    try:
        set_vm = getattr(unreal.AutomationLibrary, "set_editor_viewport_view_mode", None)
        if callable(set_vm):
            for mode in (
                getattr(unreal, "ViewModeIndex", None),
            ):
                if mode is not None and hasattr(mode, "VMI_LIT"):
                    set_vm(mode.VMI_LIT)
                    lit_method = "AutomationLibrary.set_editor_viewport_view_mode(VMI_LIT)"
                    break
            if lit_method is None:
                set_vm("Lit")
                lit_method = "AutomationLibrary.set_editor_viewport_view_mode(Lit)"
    except Exception as e:
        applied["automation_view_mode_error"] = str(e)
    if not lit_method:
        try:
            unreal.SystemLibrary.execute_console_command(None, "viewmode lit")
            lit_method = "console_viewmode_lit"
        except Exception as e:
            applied["viewmode_error"] = str(e)
    applied["viewmode"] = lit_method or "unknown"

    attempts: list[dict[str, Any]] = []
    game_view = False
    game_view_method: Optional[str] = None

    def try_gv(label: str, fn) -> None:
        nonlocal game_view, game_view_method
        if game_view:
            return
        try:
            fn()
            attempts.append({"method": label, "ok": True})
            game_view = True
            game_view_method = label
        except Exception as e:
            attempts.append({"method": label, "ok": False, "error": str(e)})

    try:
        ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
        if ues:
            if hasattr(ues, "editor_set_game_view"):
                try_gv("UnrealEditorSubsystem.editor_set_game_view", lambda: ues.editor_set_game_view(True))
            if hasattr(ues, "set_game_view"):
                try_gv("UnrealEditorSubsystem.set_game_view", lambda: ues.set_game_view(True))
    except Exception as e:
        attempts.append({"method": "UnrealEditorSubsystem", "ok": False, "error": str(e)})

    try:
        les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        if les:
            for attr in ("set_game_view", "editor_set_game_view"):
                if hasattr(les, attr):
                    try_gv(
                        "LevelEditorSubsystem.%s" % attr,
                        lambda a=attr: getattr(les, a)(True),
                    )
    except Exception as e:
        attempts.append({"method": "LevelEditorSubsystem", "ok": False, "error": str(e)})

    if not game_view:
        try_gv(
            "console_gameview",
            lambda: unreal.SystemLibrary.execute_console_command(None, "gameview"),
        )

    applied["game_view"] = game_view
    applied["game_view_method"] = game_view_method
    applied["game_view_attempts"] = attempts
    return applied


def _settle_viewport(frames: int = SETTLE_FRAMES) -> None:
    for _ in range(frames):
        _pump_editor_once()
        time.sleep(0.05)


def _pump_editor_once() -> None:
    try:
        if hasattr(unreal.AutomationLibrary, "automation_wait_for_loading"):
            unreal.AutomationLibrary.automation_wait_for_loading(None, 0.05)
    except Exception:
        pass
    try:
        if hasattr(unreal, "SlateApplication"):
            app = unreal.SlateApplication.get()
            if app is not None and hasattr(app, "tick"):
                app.tick(0.033)
    except Exception:
        pass


def _focus_level_viewport() -> dict[str, Any]:
    """Bring level viewport to foreground / realtime before HighResShot."""
    attempts: list[dict[str, Any]] = []
    any_ok = False

    def try_call(label: str, fn) -> None:
        nonlocal any_ok
        try:
            fn()
            attempts.append({"method": label, "ok": True})
            any_ok = True
        except Exception as e:
            attempts.append({"method": label, "ok": False, "error": str(e)})

    try:
        les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        if les:
            for attr in (
                "set_level_viewport_realtime",
                "editor_set_level_viewport_realtime",
            ):
                if hasattr(les, attr):
                    try_call(
                        "LevelEditorSubsystem.%s" % attr,
                        lambda a=attr: getattr(les, a)(True),
                    )
            for attr in ("focus_level_viewport", "set_focus_to_level_viewport"):
                if hasattr(les, attr):
                    try_call(
                        "LevelEditorSubsystem.%s" % attr,
                        lambda a=attr: getattr(les, a)(),
                    )
    except Exception as e:
        attempts.append({"method": "LevelEditorSubsystem", "ok": False, "error": str(e)})

    try:
        ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
        if ues:
            for attr in (
                "focus_level_viewport",
                "set_focus_to_level_viewport",
                "editor_focus_viewport",
            ):
                if hasattr(ues, attr):
                    try_call(
                        "UnrealEditorSubsystem.%s" % attr,
                        lambda a=attr: getattr(ues, a)(),
                    )
    except Exception as e:
        attempts.append({"method": "UnrealEditorSubsystem", "ok": False, "error": str(e)})

    for cmd in ("FOCUSVIEWPORT", "focus"):
        try_call(
            "console_%s" % cmd,
            lambda c=cmd: unreal.SystemLibrary.execute_console_command(None, c),
        )

    meta = {"attempts": attempts, "any_ok": any_ok}
    _log("viewport_focus", meta)
    return meta


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
    viewport_set = False
    try:
        ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
        if ues and hasattr(ues, "set_level_viewport_camera_info"):
            ues.set_level_viewport_camera_info(loc, rot)
            viewport_set = True
            meta["viewport_api"] = "UnrealEditorSubsystem.set_level_viewport_camera_info"
    except Exception as e:
        meta["viewport_ues_error"] = str(e)
    if not viewport_set:
        try:
            unreal.EditorLevelLibrary.set_level_viewport_camera_info(loc, rot)
            viewport_set = True
            meta["viewport_api"] = "EditorLevelLibrary.set_level_viewport_camera_info"
        except Exception as e:
            meta["viewport_error"] = str(e)
    meta["viewport_set"] = viewport_set
    if cam:
        try:
            unreal.EditorLevelLibrary.pilot_level_actor(cam)
            meta["pilot"] = True
        except Exception as e:
            meta["pilot"] = False
            meta["pilot_error"] = str(e)
    return meta


def _poll_automation_editor_task(task: Any, timeout_sec: float = 60.0) -> dict[str, Any]:
    """If take_high_res_screenshot returns AutomationEditorTask, wait for is_task_done."""
    meta: dict[str, Any] = {
        "had_task": task is not None,
        "task_type": type(task).__name__ if task is not None else None,
        "task_done": None,
    }
    if task is None:
        return meta
    done_fn = getattr(task, "is_task_done", None)
    if not callable(done_fn):
        meta["poll_skipped"] = "no is_task_done"
        return meta
    poll_cap = min(timeout_sec, 45.0)
    deadline = time.time() + poll_cap
    t0 = time.time()
    while time.time() < deadline:
        try:
            if done_fn():
                meta["task_done"] = True
                meta["poll_elapsed_sec"] = round(time.time() - t0, 2)
                meta["note"] = "task_done; file wait on disk is authoritative"
                return meta
        except Exception as e:
            meta["poll_error"] = str(e)
            break
        _settle_viewport(frames=1)
    meta["task_done"] = False
    meta["note"] = "task_done false is non-fatal while file wait continues"
    meta["poll_elapsed_sec"] = round(time.time() - t0, 2)
    return meta


def _high_res_shot_console_command_forms(ue_path: str) -> tuple[tuple[str, str], ...]:
    """Doc-first order (Epic Taking Screenshots), then legacy res-before-filename."""
    return (
        (
            "HighResShot_filename_res_quoted",
            'HighResShot filename="%s" %dx%d' % (ue_path, RES_X, RES_Y),
        ),
        (
            "HighResShot_filename_res",
            "HighResShot filename=%s %dx%d" % (ue_path, RES_X, RES_Y),
        ),
        ("HighResShot_filename_only_quoted", 'HighResShot filename="%s"' % ue_path),
        ("HighResShot_filename_only", "HighResShot filename=%s" % ue_path),
        (
            "HighResShot_res_filename_legacy",
            'HighResShot %dx%d filename="%s"' % (RES_X, RES_Y, ue_path),
        ),
    )


def _invoke_console_high_res_shot_sequence(dest_abs: str) -> dict[str, Any]:
    """Try each HighResShot form once; wait for PNG before next (no stacked requests)."""
    ue_path = _path_for_ue(dest_abs)
    meta: dict[str, Any] = {
        "ue_path": ue_path,
        "commands_tried": [],
        "method_used": None,
        "error": None,
        "saved_path": None,
    }
    last_err: Optional[str] = None
    for label, cmd in _high_res_shot_console_command_forms(ue_path):
        attempt_since = time.time()
        entry: dict[str, Any] = {"label": label, "cmd": cmd, "attempt_since": attempt_since}
        meta["commands_tried"].append(entry)
        try:
            unreal.SystemLibrary.execute_console_command(None, cmd)
            _log("console HighResShot invoked", {"label": label, "ue_path": ue_path})
        except Exception as e:
            last_err = str(e)
            entry["error"] = last_err
            continue
        _settle_viewport(frames=POST_CONSOLE_SETTLE_FRAMES)
        resolved, wait_meta = _wait_for_capture(dest_abs, attempt_since, WAIT_FILE_SEC)
        entry["wait"] = wait_meta
        if resolved:
            meta["method_used"] = label
            meta["saved_path"] = resolved
            meta["wait"] = wait_meta
            return meta
    meta["error"] = last_err or "no console HighResShot form produced a fresh PNG"
    return meta


def _invoke_automation_library_shot(
    dest_abs: str,
    camera,
) -> tuple[str, Optional[str], str, Any, dict[str, Any]]:
    """Fallback capture when console HighResShot did not produce a file."""
    ue_path = _path_for_ue(dest_abs)
    last_err: Optional[str] = None
    delay = CAPTURE_DELAY_SEC
    attempts = (
        (
            "kwargs_delay_force_gv",
            lambda: unreal.AutomationLibrary.take_high_res_screenshot(
                RES_X,
                RES_Y,
                ue_path,
                camera=camera,
                delay=delay,
                force_game_view=True,
            ),
        ),
        (
            "kwargs_force_gv",
            lambda: unreal.AutomationLibrary.take_high_res_screenshot(
                RES_X, RES_Y, ue_path, camera=camera, force_game_view=True
            ),
        ),
        (
            "positional_force_gv",
            lambda: unreal.AutomationLibrary.take_high_res_screenshot(
                RES_X, RES_Y, ue_path, camera, True
            ),
        ),
        (
            "legacy_abs",
            lambda: unreal.AutomationLibrary.take_high_res_screenshot(
                RES_X, RES_Y, ue_path, camera
            ),
        ),
    )
    for name, fn in attempts:
        try:
            task = fn()
            poll = _poll_automation_editor_task(task)
            _log("AutomationLibrary fallback invoked", {"method": name, "task_poll": poll})
            return name, None, ue_path, task, poll
        except TypeError:
            continue
        except Exception as e:
            last_err = str(e)
    return "automation_failed", last_err or "AutomationLibrary unavailable", ue_path, None, {
        "had_task": False,
    }


def _capture_with_console_then_fallback(
    dest_abs: str,
    camera,
    since_mtime: float,
) -> dict[str, Any]:
    """Console first (doc-ordered forms + per-form wait); AutomationLibrary if all miss."""
    finish_load = _finish_loading_before_screenshot()
    focus = _focus_level_viewport()
    console = _invoke_console_high_res_shot_sequence(dest_abs)
    resolved = console.get("saved_path")
    wait_meta = console.get("wait") or {}
    out: dict[str, Any] = {
        "finish_loading_before_screenshot": finish_load,
        "viewport_focus": focus,
        "console_capture": console,
        "primary_path": "console",
        "capture_method": console.get("method_used") or "console_failed",
        "capture_error": console.get("error"),
        "ue_path": console.get("ue_path"),
        "automation_task_poll": {"had_task": False},
        "automation_fallback": None,
        "saved_path": resolved,
        "wait": wait_meta,
        "file_produced_by": console.get("method_used") if resolved else None,
    }

    if resolved:
        _log("capture file from console path", {"dest": dest_abs, "method": out["file_produced_by"]})
        return out

    _log("console path produced no file; trying AutomationLibrary fallback", {"dest": dest_abs})
    finish_load_fb = _finish_loading_before_screenshot()
    fallback_since = time.time()
    method, cap_err, ue_path, _task, task_poll = _invoke_automation_library_shot(
        dest_abs, camera
    )
    _settle_viewport(frames=POST_CONSOLE_SETTLE_FRAMES)
    resolved_fb, wait_fb = _wait_for_capture(dest_abs, fallback_since, WAIT_FILE_SEC)
    out["automation_fallback"] = {
        "finish_loading_before_screenshot": finish_load_fb,
        "capture_method": method,
        "capture_error": cap_err,
        "ue_path": ue_path,
        "automation_task_poll": task_poll,
        "wait": wait_fb,
        "capture_since": fallback_since,
        "capture_delay_sec": CAPTURE_DELAY_SEC,
    }
    out["capture_method"] = method
    out["capture_error"] = cap_err
    out["ue_path"] = ue_path
    out["automation_task_poll"] = task_poll
    out["primary_path"] = "console_then_automation_fallback"
    out["wait"] = {"console_wait": wait_meta, "fallback_wait": wait_fb}
    if resolved_fb:
        out["saved_path"] = resolved_fb
        out["file_produced_by"] = method
        _log("capture file from AutomationLibrary fallback", {"dest": dest_abs, "method": method})
    else:
        out["saved_path"] = None
        out["file_produced_by"] = None
    return out


def _find_named_png(
    basename: str,
    since_mtime: float,
    roots: Optional[list[str]] = None,
) -> Optional[str]:
    """Newest matching basename under search roots (mtime >= since)."""
    roots = roots if roots is not None else _engine_search_roots()
    best: Optional[str] = None
    best_m = since_mtime
    for root in roots:
        if not os.path.isdir(root):
            continue
        direct = os.path.join(root, basename)
        if os.path.isfile(direct):
            try:
                m = os.path.getmtime(direct)
            except OSError:
                m = 0
            if m >= since_mtime and m >= best_m:
                best = direct
                best_m = m
        try:
            for name in os.listdir(root):
                if name.lower() != basename.lower():
                    continue
                p = os.path.join(root, name)
                if not os.path.isfile(p):
                    continue
                try:
                    m = os.path.getmtime(p)
                except OSError:
                    continue
                if m >= since_mtime and m >= best_m:
                    best = p
                    best_m = m
        except OSError:
            continue
    return best


def _copy_into_dest(source: str, dest_abs: str) -> bool:
    if source == dest_abs:
        return True
    try:
        os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
        shutil.copy2(source, dest_abs)
        return os.path.isfile(dest_abs)
    except Exception:
        return False


def _file_size_stable(path: str) -> bool:
    if not os.path.isfile(path):
        return False
    try:
        sizes = []
        for _ in range(STABLE_SIZE_POLLS):
            sizes.append(os.path.getsize(path))
            if sizes[-1] < MIN_BYTES:
                time.sleep(STABLE_POLL_INTERVAL)
                continue
            time.sleep(STABLE_POLL_INTERVAL)
        return len(sizes) >= STABLE_SIZE_POLLS and sizes[-1] >= MIN_BYTES and sizes[-1] == sizes[-2]
    except OSError:
        return False


def _wait_for_capture(dest_abs: str, since_mtime: float, timeout_sec: float) -> tuple[Optional[str], dict]:
    """Poll absolute dest + engine Win64/PA_E fallbacks until size stable."""
    meta: dict[str, Any] = {
        "dest_abs": dest_abs,
        "timeout_sec": timeout_sec,
        "discovered_from": None,
        "wait_elapsed_sec": 0.0,
        "stable": False,
    }
    basename = os.path.basename(dest_abs)
    deadline = time.time() + timeout_sec
    t0 = time.time()
    while time.time() < deadline:
        _settle_viewport(frames=2)
        if (
            os.path.isfile(dest_abs)
            and _mtime_at_least(dest_abs, since_mtime)
            and _file_size_stable(dest_abs)
        ):
            meta["stable"] = True
            meta["discovered_from"] = dest_abs
            meta["wait_elapsed_sec"] = round(time.time() - t0, 2)
            return dest_abs, meta
        found = _find_named_png(basename, since_mtime)
        if found and os.path.getsize(found) >= MIN_BYTES and _mtime_at_least(found, since_mtime):
            if _copy_into_dest(found, dest_abs) and _mtime_at_least(dest_abs, since_mtime) and _file_size_stable(dest_abs):
                meta["stable"] = True
                meta["discovered_from"] = found
                meta["wait_elapsed_sec"] = round(time.time() - t0, 2)
                return dest_abs, meta
            if os.path.isfile(found) and _file_size_stable(found) and _mtime_at_least(found, since_mtime):
                meta["discovered_from"] = found
                meta["wait_elapsed_sec"] = round(time.time() - t0, 2)
                return found, meta
        time.sleep(STABLE_POLL_INTERVAL)
    meta["wait_elapsed_sec"] = round(time.time() - t0, 2)
    if os.path.isfile(dest_abs) and _mtime_at_least(dest_abs, since_mtime):
        meta["discovered_from"] = dest_abs
        meta["stable"] = _file_size_stable(dest_abs)
        return dest_abs, meta
    found = _find_named_png(basename, since_mtime)
    if found and _mtime_at_least(found, since_mtime):
        _copy_into_dest(found, dest_abs)
        meta["discovered_from"] = found
        dest_ok = os.path.isfile(dest_abs) and _mtime_at_least(dest_abs, since_mtime)
        return (dest_abs if dest_ok else found), meta
    return None, meta


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
    out["pil_available"] = _pil_available()
    if lum is None:
        if not _pil_available():
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
    _finish_loading_before_screenshot()
    dest = _shot_dest_abs(shot["filename"])
    purge = _purge_stale_shot_pngs(dest)
    since = time.time()
    cap = _capture_with_console_then_fallback(dest, cam if cam else None, since)
    resolved = cap.get("saved_path")
    _log(
        "capture invoked",
        {
            "id": shot["id"],
            "method": cap.get("capture_method"),
            "file_produced_by": cap.get("file_produced_by"),
            "dest_abs": dest,
        },
    )
    validation = _validate_png(resolved)
    desktop = _copy_to_desktop(resolved, shot["filename"]) if resolved else {"copied": False}
    entry = {
        "id": shot["id"],
        "filename": shot["filename"],
        "dest_abs": dest,
        "purge_before_capture": purge,
        "capture_method": cap.get("capture_method"),
        "capture_error": cap.get("capture_error"),
        "file_produced_by": cap.get("file_produced_by"),
        "primary_path": cap.get("primary_path"),
        "ue_path": cap.get("ue_path"),
        "viewport_focus": cap.get("viewport_focus"),
        "console_capture": cap.get("console_capture"),
        "automation_fallback": cap.get("automation_fallback"),
        "automation_task_poll": cap.get("automation_task_poll"),
        "saved_path": resolved,
        "wait": cap.get("wait"),
        "engine_search_roots": _engine_search_roots(),
        "capture_since": since,
        "pose": pose_meta,
        "validation": validation,
        "desktop_copy": desktop,
        "pass": bool(validation.get("pass")),
    }
    _log("shot done", {"id": shot["id"], "pass": entry["pass"], "bytes": validation.get("bytes")})
    return entry


def _final_drain_shots(results: list[dict]) -> list[dict]:
    """Late async flush: re-poll after last shot before disarming keep_alive."""
    _log("final_drain start", {"sec": FINAL_DRAIN_SEC})
    deadline = time.time() + FINAL_DRAIN_SEC
    while time.time() < deadline:
        any_pending = False
        for entry in results:
            if entry.get("pass"):
                continue
            any_pending = True
            dest = _shot_dest_abs(entry["filename"])
            since = float(entry.get("capture_since") or 0.0)
            resolved, wait_meta = _wait_for_capture(dest, since, timeout_sec=5.0)
            entry["wait_final"] = wait_meta
            if resolved:
                validation = _validate_png(resolved)
                entry["validation"] = validation
                entry["saved_path"] = resolved
                entry["desktop_copy"] = _copy_to_desktop(resolved, entry["filename"])
                entry["pass"] = bool(validation.get("pass"))
        if not any_pending:
            break
        _settle_viewport(frames=4)
    for entry in results:
        if entry.get("pass"):
            continue
        dest = _shot_dest_abs(entry["filename"])
        since = float(entry.get("capture_since") or 0.0)
        resolved, wait_meta = _wait_for_capture(dest, since, timeout_sec=FINAL_DRAIN_SEC)
        entry["wait_final"] = wait_meta
        if resolved:
            validation = _validate_png(resolved)
            entry["validation"] = validation
            entry["saved_path"] = resolved
            entry["desktop_copy"] = _copy_to_desktop(resolved, entry["filename"])
            entry["pass"] = bool(validation.get("pass"))
    _log("final_drain done")
    return results


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

    results: list[dict] = []
    for idx, s in enumerate(SHOTS):
        if idx > 0:
            _log("inter_shot_settle", {"frames": INTER_SHOT_SETTLE_FRAMES})
            _settle_viewport(frames=INTER_SHOT_SETTLE_FRAMES)
        results.append(_capture_shot(s))
    results = _final_drain_shots(results)
    all_pass = all(r.get("pass") for r in results)

    report = {
        "ok": all_pass,
        "prefix": PREFIX.strip(":"),
        "project_dir_abs": _project_dir(),
        "pil_available": _pil_available(),
        "level_path": LEVEL_PATH,
        "level_loaded": level_ok,
        "viewport_prep": viewport_prep,
        "keep_python_script_alive": keep_ok,
        "resolution": [RES_X, RES_Y],
        "shots": results,
        "policy": "Does not claim shotlist PASS — verify on DESKTOP; no host ImageGrab",
        "ladder_doc": "docs/Automation/CAPTURE_REDUNDANCY.md",
        "ladder_rung": "1_built_in_and_in_repo",
        "scout_requires": "APPROVE TOOL SCOUT <name>",
        "build_requires": "APPROVE TOOL BUILD <name>",
    }
    with open(_report_path(), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    _log("report written", {"path": _report_path(), "all_pass": all_pass})

    _log("finished", {"all_pass": all_pass})

    try:
        if keep_ok:
            import vnp_editor_keep_alive as keep

            keep.disarm()
    except Exception:
        pass


if __name__ == "__main__":
    main()

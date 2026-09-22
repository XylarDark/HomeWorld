"""PA-E / shotlist viewport capture — AutomationLibrary diagnostic (not PASS primary).

**Primary (DESKTOP prove):** [capture_shotlist.py](capture_shotlist.py) /
[capture_shotlist_mrq.py](capture_shotlist_mrq.py) — Movie Render Queue one-frame.
This script is **diagnostic** for the **OPEN** AutomationLibrary viewport capture bug
(near-black PNG while Lead sees lit homestead when rotating viewport — wrong pose /
game-view / pilot / buffer, not missing content).

Loads L_VS_MVP_Markers, poses level viewport for Shot 1 (lookout) and Shot 2
(cabin/garden), lit + game view, then **AutomationLibrary.take_high_res_screenshot**
(one request in flight) with **Slate pre-tick** wait (not blocking sleep
on the editor main thread after invoke), validates PNGs, writes
Saved/pa_e_capture_report.json.

Wait pattern (post-#163 DESKTOP): async HighResShot needs editor ticks; blocking
``time.sleep`` / settle loops in Python freeze ticks and leave ``is_task_done()`` false.
Community pattern: ``unreal.register_slate_pre_tick_callback`` — fire one capture,
check task + file on later ticks, unregister when finished.

Forum refs:
- https://forums.unrealengine.com/t/how-to-wait-for-take-high-res-screenshot/139285
- https://forums.unrealengine.com/t/python-api-highrescreenshot/132783

Policy: [docs/Automation/CAPTURE_REDUNDANCY.md](docs/Automation/CAPTURE_REDUNDANCY.md) § Shotlist.
Multi-form console HighResShot ladders are **not** used.

Run: MCP execute_python_script("capture_shotlist_viewport.py") — diagnostic only.
Primary: execute_python_script("capture_shotlist.py"). UnrealEditor-Cmd
-ExecutePythonScript=... (uses vnp_editor_keep_alive).

Does NOT claim shotlist PASS — DESKTOP must verify report + stills.
"""
from __future__ import annotations

import json
import os
import shutil
import time
from enum import Enum
from typing import Any, Callable, Optional

try:
    import unreal
except ImportError:
    print("capture_shotlist_viewport: Run inside Unreal Editor.")
    raise

import pa_e_shotlist_common as common

PREFIX = "capture_shotlist_viewport:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
RES_X, RES_Y = 1920, 1080
MIN_BYTES = 50 * 1024
MIN_MEAN_LUMINANCE = 8.0  # reject near-black (0–255 scale)
SETTLE_FRAMES = 12
INTER_SHOT_SETTLE_FRAMES = 24
WAIT_FILE_SEC = 120.0
CAPTURE_DELAY_SEC = 0.35
STABLE_SIZE_POLLS = 4
FINAL_DRAIN_SEC = 75.0
PRIMARY_PATH = "automation_library_slate_pretick"
SLATE_WAIT_MECHANISM = "register_slate_pre_tick_callback"

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


class _Phase(str, Enum):
    IDLE = "idle"
    POSED = "posed"
    PREPARING = "preparing"
    CAPTURE_PENDING = "capture_pending"
    WAITING_FILE = "waiting_file"
    INTER_SHOT_SETTLE = "inter_shot_settle"
    FINAL_DRAIN = "final_drain"
    WRITE_REPORT = "write_report"
    DISARM = "disarm"
    DONE = "done"


class _StableSizeTracker:
    """Tick-based file size stability (no sleep between polls)."""

    __slots__ = ("last_size", "same_count", "samples")

    def __init__(self) -> None:
        self.last_size = -1
        self.same_count = 0
        self.samples: list[int] = []

    def reset(self) -> None:
        self.last_size = -1
        self.same_count = 0
        self.samples = []

    def observe(self, path: str) -> bool:
        if not os.path.isfile(path):
            self.reset()
            return False
        try:
            size = os.path.getsize(path)
        except OSError:
            self.reset()
            return False
        self.samples.append(size)
        if len(self.samples) > STABLE_SIZE_POLLS:
            self.samples = self.samples[-STABLE_SIZE_POLLS:]
        if size == self.last_size:
            self.same_count += 1
        else:
            self.last_size = size
            self.same_count = 1
        # MIN_BYTES is enforced in _validate_png only — small but complete PNGs must not
        # block wait discovery (post-#165 DESKTOP: ~38KB Shot1 timed out as file_missing).
        return (
            self.same_count >= 2
            and len(self.samples) >= STABLE_SIZE_POLLS
            and self.samples[-1] == self.samples[-2]
        )


class _ShotlistOrchestrator:
    """Async shotlist driver: one HighResShot in flight; Slate pre-tick state machine."""

    def __init__(
        self,
        *,
        keep_ok: bool,
        level_ok: bool,
        viewport_prep: dict[str, Any],
    ) -> None:
        self.keep_ok = keep_ok
        self.level_ok = level_ok
        self.viewport_prep = viewport_prep
        self.phase = _Phase.IDLE
        self.shot_index = 0
        self.results: list[dict[str, Any]] = []
        self._tick_handle: Any = None
        self._settle_frames_left = 0
        self._current_shot: Optional[dict] = None
        self._current_cam: Any = None
        self._dest_abs = ""
        self._capture_since = 0.0
        self._wait_deadline = 0.0
        self._task: Any = None
        self._task_poll: dict[str, Any] = {}
        self._capture_meta: dict[str, Any] = {}
        self._wait_meta: dict[str, Any] = {}
        self._stable = _StableSizeTracker()
        self._wait_t0 = 0.0
        self._final_drain_deadline = 0.0
        self._driver_error: Optional[str] = None
        self._capture_in_flight = False

    def start(self) -> bool:
        register = getattr(unreal, "register_slate_pre_tick_callback", None)
        if not callable(register):
            self._driver_error = "register_slate_pre_tick_callback unavailable"
            _log("slate pre_tick unavailable", {"error": self._driver_error})
            return False
        try:
            self._tick_handle = register(self._on_slate_pre_tick)
        except Exception as e:
            self._driver_error = str(e)
            _log("slate pre_tick register failed", {"error": self._driver_error})
            return False
        self.phase = _Phase.POSED
        self.shot_index = 0
        _log(
            "slate pre_tick driver armed",
            {"mechanism": SLATE_WAIT_MECHANISM, "wait_file_sec": WAIT_FILE_SEC},
        )
        return True

    def _unregister_tick(self) -> None:
        if self._tick_handle is None:
            return
        unregister = getattr(unreal, "unregister_slate_pre_tick_callback", None)
        if callable(unregister):
            try:
                unregister(self._tick_handle)
            except Exception as e:
                _log("slate pre_tick unregister failed", {"error": str(e)})
        self._tick_handle = None

    def _on_slate_pre_tick(self, _delta: float) -> None:
        try:
            self._tick()
        except Exception as e:
            _log("orchestrator tick error", {"error": str(e), "phase": self.phase.value})
            self.phase = _Phase.WRITE_REPORT
            self._driver_error = self._driver_error or str(e)

    def _tick(self) -> None:
        if self.phase == _Phase.POSED:
            self._begin_shot_prepare()
        elif self.phase == _Phase.PREPARING:
            pass
        elif self.phase == _Phase.CAPTURE_PENDING:
            self._invoke_capture_once()
        elif self.phase == _Phase.WAITING_FILE:
            self._poll_capture_wait()
        elif self.phase == _Phase.INTER_SHOT_SETTLE:
            self._settle_frames_left -= 1
            if self._settle_frames_left <= 0:
                self.phase = _Phase.POSED
        elif self.phase == _Phase.FINAL_DRAIN:
            self._tick_final_drain()
        elif self.phase == _Phase.WRITE_REPORT:
            self._write_report_and_finish()
        elif self.phase == _Phase.DISARM:
            self._disarm_only()

    def _begin_shot_prepare(self) -> None:
        if self.phase != _Phase.POSED:
            return
        # Lock before pose/purge/logging — nested pre_tick while still POSED re-entered
        # prepare and stacked multiple take_high_res_screenshot calls (post-#165).
        self.phase = _Phase.PREPARING
        self._capture_in_flight = True
        if self.shot_index >= len(SHOTS):
            self.phase = _Phase.FINAL_DRAIN
            self._final_drain_deadline = time.time() + FINAL_DRAIN_SEC
            self._capture_in_flight = False
            _log("final_drain start", {"sec": FINAL_DRAIN_SEC})
            return
        shot = SHOTS[self.shot_index]
        self._current_shot = shot
        _log("shot start", {"id": shot["id"], "phase": "posed"})
        self._current_cam = _find_camera(shot["camera_labels"])
        pose_meta = _pose_viewport(
            self._current_cam,
            tuple(shot["fallback_location_m"]),
            tuple(shot["fallback_rotation_deg"]),
        )
        pose_meta["fallback_source"] = shot.get("fallback_source")
        _finish_loading_before_screenshot()
        self._dest_abs = _shot_dest_abs(shot["filename"])
        purge = _purge_stale_shot_pngs(self._dest_abs)
        self._capture_meta = {
            "pose": pose_meta,
            "purge_before_capture": purge,
            "dest_abs": self._dest_abs,
        }
        self._capture_since = time.time()
        self._stable.reset()
        self._task = None
        self._task_poll = {"had_task": False}
        self.phase = _Phase.CAPTURE_PENDING

    def _invoke_capture_once(self) -> None:
        if self.phase != _Phase.CAPTURE_PENDING:
            return
        if not self._current_shot:
            self.phase = _Phase.WRITE_REPORT
            return
        finish_load = _finish_loading_before_screenshot()
        focus = _focus_level_viewport()
        method, cap_err, ue_path, task = _invoke_automation_library_shot_only(
            self._dest_abs,
            self._current_cam if self._current_cam else None,
        )
        self._capture_in_flight = True
        self._task = task
        self._task_poll = _task_snapshot(task)
        self._wait_t0 = time.time()
        self._wait_deadline = time.time() + WAIT_FILE_SEC
        self._wait_meta = {
            "dest_abs": self._dest_abs,
            "timeout_sec": WAIT_FILE_SEC,
            "wait_mechanism": SLATE_WAIT_MECHANISM,
            "discovered_from": None,
            "wait_elapsed_sec": 0.0,
            "stable": False,
        }
        self._capture_meta.update(
            {
                "finish_loading_before_screenshot": finish_load,
                "viewport_focus": focus,
                "primary_path": PRIMARY_PATH,
                "capture_method": method,
                "capture_error": cap_err,
                "ue_path": ue_path,
                "automation_task_poll": self._task_poll,
                "capture_since": self._capture_since,
                "capture_delay_sec": CAPTURE_DELAY_SEC,
                "wait_file_budget_sec": WAIT_FILE_SEC,
            }
        )
        _log(
            "AutomationLibrary invoke (one in flight)",
            {"method": method, "task_poll": self._task_poll},
        )
        self.phase = _Phase.WAITING_FILE

    def _poll_capture_wait(self) -> None:
        now = time.time()
        self._wait_meta["wait_elapsed_sec"] = round(now - self._wait_t0, 2)
        task_done = _task_is_done(self._task)
        if task_done is True:
            self._task_poll["task_done"] = True
            self._task_poll["note"] = "task_done; file on disk is authoritative"

        resolved, probe = _probe_capture_file(
            self._dest_abs,
            self._capture_since,
            self._stable,
        )
        self._wait_meta.update(probe)
        if resolved:
            self._wait_meta["stable"] = True
            self._wait_meta["discovered_from"] = probe.get("discovered_from")
            self._finish_shot(resolved)
            return
        if task_done is True and resolved is None:
            pass
        if now >= self._wait_deadline:
            self._task_poll["task_done"] = task_done
            self._task_poll.setdefault(
                "note",
                "timeout; task_done=%s file authoritative if appears later in final_drain"
                % task_done,
            )
            resolved = _find_fresh_capture_path(self._dest_abs, self._capture_since)
            if resolved:
                self._wait_meta["discovered_from"] = resolved
                self._wait_meta["stable"] = False
                self._wait_meta["timeout_authoritative"] = True
            self._finish_shot(resolved)
            return

    def _finish_shot(self, resolved: Optional[str]) -> None:
        shot = self._current_shot
        if not shot:
            self.phase = _Phase.WRITE_REPORT
            return
        if not resolved and self._dest_abs and self._capture_since:
            resolved = _find_fresh_capture_path(self._dest_abs, self._capture_since)
        cap = dict(self._capture_meta)
        cap["saved_path"] = resolved
        cap["wait"] = dict(self._wait_meta)
        cap["file_produced_by"] = cap.get("capture_method") if resolved else None
        cap["automation_task_poll"] = dict(self._task_poll)
        if resolved:
            _log("capture file from AutomationLibrary", {"dest": self._dest_abs})
        else:
            _log("capture missing after slate wait", {"dest": self._dest_abs})
        validation = _validate_png(resolved)
        desktop = _copy_to_desktop(resolved, shot["filename"]) if resolved else {"copied": False}
        entry = {
            "id": shot["id"],
            "filename": shot["filename"],
            "dest_abs": self._dest_abs,
            "purge_before_capture": cap.get("purge_before_capture"),
            "capture_method": cap.get("capture_method"),
            "capture_error": cap.get("capture_error"),
            "file_produced_by": cap.get("file_produced_by"),
            "primary_path": PRIMARY_PATH,
            "ue_path": cap.get("ue_path"),
            "viewport_focus": cap.get("viewport_focus"),
            "automation_task_poll": cap.get("automation_task_poll"),
            "wait_file_budget_sec": WAIT_FILE_SEC,
            "wait_mechanism": SLATE_WAIT_MECHANISM,
            "saved_path": resolved,
            "wait": cap.get("wait"),
            "engine_search_roots": _engine_search_roots(),
            "capture_since": self._capture_since,
            "pose": cap.get("pose"),
            "validation": validation,
            "desktop_copy": desktop,
            "pass": bool(validation.get("pass")),
        }
        self.results.append(entry)
        _log("shot done", {"id": shot["id"], "pass": entry["pass"], "bytes": validation.get("bytes")})
        self._capture_in_flight = False
        self.shot_index += 1
        if self.shot_index < len(SHOTS):
            self._settle_frames_left = INTER_SHOT_SETTLE_FRAMES
            self.phase = _Phase.INTER_SHOT_SETTLE
            _log("inter_shot_settle", {"frames": INTER_SHOT_SETTLE_FRAMES})
        else:
            self.phase = _Phase.FINAL_DRAIN
            self._final_drain_deadline = time.time() + FINAL_DRAIN_SEC
            _log("final_drain start", {"sec": FINAL_DRAIN_SEC})

    def _tick_final_drain(self) -> None:
        now = time.time()
        any_pending = False
        for entry in self.results:
            if entry.get("pass"):
                continue
            any_pending = True
            dest = _shot_dest_abs(entry["filename"])
            since = float(entry.get("capture_since") or 0.0)
            tracker = _StableSizeTracker()
            resolved, wait_meta = _probe_capture_file(dest, since, tracker)
            entry["wait_final"] = wait_meta
            if resolved:
                validation = _validate_png(resolved)
                entry["validation"] = validation
                entry["saved_path"] = resolved
                entry["desktop_copy"] = _copy_to_desktop(resolved, entry["filename"])
                entry["pass"] = bool(validation.get("pass"))
        if now >= self._final_drain_deadline:
            for entry in self.results:
                if entry.get("pass"):
                    continue
                dest = _shot_dest_abs(entry["filename"])
                since = float(entry.get("capture_since") or 0.0)
                resolved = _find_fresh_capture_path(dest, since)
                if resolved:
                    validation = _validate_png(resolved)
                    entry["validation"] = validation
                    entry["saved_path"] = resolved
                    entry["desktop_copy"] = _copy_to_desktop(resolved, entry["filename"])
                    entry["pass"] = bool(validation.get("pass"))
                    entry["wait_final"] = entry.get("wait_final") or {}
                    entry["wait_final"]["final_authoritative"] = True
            _log("final_drain done")
            self.phase = _Phase.WRITE_REPORT
        elif not any_pending:
            _log("final_drain done")
            self.phase = _Phase.WRITE_REPORT

    def _write_report_and_finish(self) -> None:
        if self.phase == _Phase.DONE:
            return
        status = common.summarize_capture_report(self.results)
        all_pass = status["capture_pass"]
        report = {
            **status,
            "prefix": PREFIX.strip(":"),
            "primary_path": PRIMARY_PATH,
            "wait_mechanism": SLATE_WAIT_MECHANISM,
            "project_dir_abs": _project_dir(),
            "pil_available": _pil_available(),
            "level_path": LEVEL_PATH,
            "level_loaded": self.level_ok,
            "viewport_prep": self.viewport_prep,
            "keep_python_script_alive": self.keep_ok,
            "resolution": [RES_X, RES_Y],
            "wait_file_budget_sec": WAIT_FILE_SEC,
            "final_drain_sec": FINAL_DRAIN_SEC,
            "shots": self.results,
            "driver_error": self._driver_error,
            "state_machine_phases": [p.value for p in _Phase],
            "lead_prove_loop": list(common.LEAD_PROVE_LOOP),
            "universal_testing_preconditions": list(common.UNIVERSAL_TESTING_PRECONDITIONS),
            "homestead_diagnostic_script": "pa_e_homestead_capture_diagnostic.py",
            "policy": (
                "AutomationLibrary + slate pre-tick wait (post-#163: blocking sleep freezes ticks); "
                "near-black = prove loop in progress, not closed FAIL; "
                "no console multi-form ladder; does not claim shotlist PASS — verify on DESKTOP; "
                "no host ImageGrab"
            ),
            "forum_refs": [
                "https://forums.unrealengine.com/t/how-to-wait-for-take-high-res-screenshot/139285",
                "https://forums.unrealengine.com/t/python-api-highrescreenshot/132783",
            ],
            "ladder_doc": "docs/Automation/CAPTURE_REDUNDANCY.md",
            "ladder_rung": "1_built_in_and_in_repo",
            "scout_requires": "APPROVE TOOL SCOUT <name>",
            "build_requires": "APPROVE TOOL BUILD <name>",
        }
        with open(_report_path(), "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        _log("report written", {"path": _report_path(), "all_pass": all_pass})
        _log("finished", {"all_pass": all_pass})
        self._unregister_tick()
        self.phase = _Phase.DISARM
        self._disarm_only()
        self.phase = _Phase.DONE

    def _disarm_only(self) -> None:
        if not self.keep_ok:
            return
        try:
            import vnp_editor_keep_alive as keep

            keep.disarm()
        except Exception:
            pass


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
    """AutomationLibrary: absolute path, forward slashes."""
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
    """UE often writes relative paths under Engine Binaries Win64 (engine CWD)."""
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

    def try_gv(label: str, fn: Callable[[], None]) -> None:
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


def _settle_viewport_before_first_capture(frames: int = SETTLE_FRAMES) -> None:
    """Short sleep settle only before the first capture (level load); not used after invoke."""
    for _ in range(frames):
        try:
            if hasattr(unreal, "SlateApplication"):
                app = unreal.SlateApplication.get()
                if app is not None and hasattr(app, "tick"):
                    app.tick(0.033)
        except Exception:
            pass
        time.sleep(0.05)


def _focus_level_viewport() -> dict[str, Any]:
    """Bring level viewport to foreground / realtime before HighResShot."""
    attempts: list[dict[str, Any]] = []
    any_ok = False

    def try_call(label: str, fn: Callable[[], None]) -> None:
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


def _task_snapshot(task: Any) -> dict[str, Any]:
    meta: dict[str, Any] = {
        "had_task": task is not None,
        "task_type": type(task).__name__ if task is not None else None,
        "task_done": None,
        "poll_skipped": None,
    }
    if task is None:
        return meta
    done_fn = getattr(task, "is_task_done", None)
    if not callable(done_fn):
        meta["poll_skipped"] = "no is_task_done"
        return meta
    try:
        meta["task_done"] = bool(done_fn())
    except Exception as e:
        meta["poll_error"] = str(e)
    return meta


def _task_is_done(task: Any) -> Optional[bool]:
    if task is None:
        return None
    done_fn = getattr(task, "is_task_done", None)
    if not callable(done_fn):
        return None
    try:
        return bool(done_fn())
    except Exception:
        return None


def _invoke_automation_library_shot_only(
    dest_abs: str,
    camera,
) -> tuple[str, Optional[str], str, Any]:
    """Fire take_high_res_screenshot once; caller waits on Slate pre-tick (no blocking poll)."""
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
            return name, None, ue_path, task
        except TypeError:
            continue
        except Exception as e:
            last_err = str(e)
    return "automation_failed", last_err or "AutomationLibrary unavailable", ue_path, None


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


def _find_fresh_capture_path(dest_abs: str, since_mtime: float) -> Optional[str]:
    """Return newest PNG for this shot with mtime >= since (no MIN_BYTES / stability gate)."""
    basename = os.path.basename(dest_abs)
    if (
        os.path.isfile(dest_abs)
        and _mtime_at_least(dest_abs, since_mtime)
    ):
        return dest_abs
    found = _find_named_png(basename, since_mtime)
    if found and _mtime_at_least(found, since_mtime):
        if found != dest_abs:
            _copy_into_dest(found, dest_abs)
        if os.path.isfile(dest_abs) and _mtime_at_least(dest_abs, since_mtime):
            return dest_abs
        return found
    return None


def _probe_capture_file(
    dest_abs: str,
    since_mtime: float,
    stable: _StableSizeTracker,
) -> tuple[Optional[str], dict[str, Any]]:
    """Non-blocking single-tick probe for fresh PNG (task wait path)."""
    meta: dict[str, Any] = {"discovered_from": None}
    basename = os.path.basename(dest_abs)
    if (
        os.path.isfile(dest_abs)
        and _mtime_at_least(dest_abs, since_mtime)
        and stable.observe(dest_abs)
    ):
        meta["discovered_from"] = dest_abs
        return dest_abs, meta
    found = _find_named_png(basename, since_mtime)
    if found and _mtime_at_least(found, since_mtime):
        if found != dest_abs:
            _copy_into_dest(found, dest_abs)
        check_path = dest_abs if os.path.isfile(dest_abs) else found
        if _mtime_at_least(check_path, since_mtime) and stable.observe(check_path):
            meta["discovered_from"] = found
            return check_path, meta
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
        out["prove_loop_status"] = "in_progress"
        out["closed_fail"] = False
        out["lead_rule"] = common.PROVE_CRITERIA.get("note", "")
        out["prove_loop"] = list(common.LEAD_PROVE_LOOP)
        return out
    out["pass"] = True
    out["prove_loop_status"] = "complete"
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


def main() -> None:
    _log("started")
    keep_ok = False
    try:
        import vnp_editor_keep_alive as keep

        keep_ok = keep.arm()
    except Exception as e:
        _log("keep_alive import/arm skipped", {"error": str(e)})

    level_ok = _load_level()
    arrange_gate = common.arrange_pa_e_shotlist(
        PREFIX,
        level_loaded=level_ok,
        require_mrq=False,
    )
    viewport_prep: dict[str, Any] = {
        "arrange_gate": arrange_gate,
        "finish_loading": arrange_gate.get("finish_loading"),
        "homestead_night_environment": arrange_gate.get("lighting"),
    }
    viewport_prep.update(arrange_gate.get("view") or common.apply_lit_game_view_for_capture())
    _settle_viewport_before_first_capture()

    if not arrange_gate.get("ready"):
        common.write_blocked_capture_report(
            prefix=PREFIX,
            primary_path=PRIMARY_PATH,
            arrange_gate=arrange_gate,
            level_loaded=level_ok,
            keep_python_script_alive=keep_ok,
            extra={
                "wait_mechanism": SLATE_WAIT_MECHANISM,
                "driver_error": "arrange_gate_not_ready",
            },
        )
        if keep_ok:
            try:
                import vnp_editor_keep_alive as keep

                keep.disarm()
            except Exception:
                pass
        return

    orch = _ShotlistOrchestrator(
        keep_ok=keep_ok,
        level_ok=level_ok,
        viewport_prep=viewport_prep,
    )
    if not orch.start():
        report = {
            "ok": False,
            "prefix": PREFIX.strip(":"),
            "primary_path": PRIMARY_PATH,
            "wait_mechanism": SLATE_WAIT_MECHANISM,
            "driver_error": orch._driver_error,
            "level_loaded": level_ok,
            "keep_python_script_alive": keep_ok,
            "shots": [],
            "policy": "Slate pre-tick driver failed to register",
        }
        with open(_report_path(), "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        if keep_ok:
            try:
                import vnp_editor_keep_alive as keep

                keep.disarm()
            except Exception:
                pass
        return

    # keep_alive + pre_tick callback run the state machine; main returns without blocking wait.


if __name__ == "__main__":
    main()

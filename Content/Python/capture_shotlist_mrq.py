"""PA-E shotlist capture — Movie Render Queue (MRQ) one-frame primary.

Loads L_VS_MVP_Markers, ensures minimal Level Sequences under
/Game/HomeWorld/Cinematics/PA_E/ (runtime create-if-missing; DESKTOP first run
may save tiny .uasset binaries locally), queues MRQ jobs with custom one-frame
playback range, PNG deferred pass, async PIE executor + Slate pre-tick wait.

Near-black AutomationLibrary stills are an **OPEN viewport capture bug** (wrong pose /
game-view / pilot / empty buffer) — scene content is visible to Lead in Editor;
Arrange relocates in-level **CAM_Hero** / **CAM_CabinClose**; MRQ renders via spawned
**PA_E_MRQ_{shot_id}** cine cameras at the same resolved loc/rot (stale sequence
possessable Transform tracks do not override Arrange). Deferred lit pass + warm-up.
PASS requires **lit homestead** stills, not file-exists-only.

Policy: [docs/Automation/CAPTURE_REDUNDANCY.md](docs/Automation/CAPTURE_REDUNDANCY.md)
Primary entry: capture_shotlist.py or this script via MCP
execute_python_script("capture_shotlist_mrq.py").

Requires plugins: MovieRenderPipeline, MovieRenderPipelineEditor (and SequencerScripting).

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
    print("capture_shotlist_mrq: Run inside Unreal Editor.")
    raise

import pa_e_shotlist_common as common

PREFIX = "capture_shotlist_mrq:"
PRIMARY_PATH = "movie_render_queue_one_frame"
WAIT_MECHANISM = "register_slate_pre_tick_callback_and_executor_delegate"
WAIT_RENDER_SEC = 300.0
CUSTOM_START = common.ONE_FRAME_START
CUSTOM_END = common.ONE_FRAME_END


class _Phase(str, Enum):
    IDLE = "idle"
    RENDER_SHOT = "render_shot"
    PREPARING = "preparing"
    WAIT_RENDER = "wait_render"
    FINALIZE_SHOT = "finalize_shot"
    INTER_SHOT_DRAIN = "inter_shot_drain"
    WRITE_REPORT = "write_report"
    DISARM = "disarm"
    DONE = "done"


# One orchestrator per Editor Python session — prevents nested MCP re-entry from
# double-arming Slate pre-tick / keep_alive (post-#168 DESKTOP duplicate LogPython).
_ACTIVE_DRIVER: Optional["_MrqOrchestrator"] = None
_MAIN_ENTRY_ACTIVE = False
# Epic MRQ Python pattern: keep finished callback reachable (avoid GC before delegate fires).
_EXECUTOR_FINISHED_HANDLER: Optional[Callable[[Any, bool], None]] = None


class _MrqOrchestrator:
    """One MRQ job in flight; Slate pre-tick for completion + PNG discovery."""

    def __init__(
        self,
        *,
        keep_ok: bool,
        level_ok: bool,
        mrq_ok: bool,
        mrq_probe: dict[str, Any],
        viewport_prep: dict[str, Any],
    ) -> None:
        self.keep_ok = keep_ok
        self.level_ok = level_ok
        self.mrq_ok = mrq_ok
        self.mrq_probe = mrq_probe
        self.viewport_prep = viewport_prep
        self.phase = _Phase.IDLE
        self.shot_index = 0
        self.results: list[dict[str, Any]] = []
        self._tick_handle: Any = None
        self._subsystem: Any = None
        self._executor: Any = None
        self._render_since = 0.0
        self._wait_deadline = 0.0
        self._current_shot: Optional[dict] = None
        self._staging_dir = ""
        self._dest_abs = ""
        self._sequence_path = ""
        self._sequence_meta: dict[str, Any] = {}
        self._job_meta: dict[str, Any] = {}
        self._driver_error: Optional[str] = None
        self._executor_finished_handler_ref: Optional[Callable[[Any, bool], None]] = None
        self._executor_finished = False
        self._executor_success = False
        self._in_tick = False
        self._inter_shot_drain_deadline = 0.0
        self._pie_night_stack_attempts = 0

    def start(self) -> bool:
        if self._tick_handle is not None:
            _log("start skipped — tick callback already registered", {})
            return True
        if not self.mrq_ok:
            self._driver_error = self.mrq_probe.get("error") or "MRQ subsystem unavailable"
            return False
        register = getattr(unreal, "register_slate_pre_tick_callback", None)
        if not callable(register):
            self._driver_error = "register_slate_pre_tick_callback unavailable"
            return False
        try:
            self._subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
            self._tick_handle = register(self._on_slate_pre_tick)
        except Exception as e:
            self._driver_error = str(e)
            return False
        self.phase = _Phase.RENDER_SHOT
        self.shot_index = 0
        _log("slate pre_tick driver armed", {"wait_render_sec": WAIT_RENDER_SEC})
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
        if self._in_tick:
            return
        self._in_tick = True
        try:
            self._tick()
        except Exception as e:
            _log("orchestrator tick error", {"error": str(e), "phase": self.phase.value})
            self.phase = _Phase.WRITE_REPORT
            self._driver_error = self._driver_error or str(e)
        finally:
            self._in_tick = False

    def _is_subsystem_rendering(self) -> bool:
        try:
            if self._subsystem and hasattr(self._subsystem, "is_rendering"):
                return bool(self._subsystem.is_rendering())
        except Exception:
            pass
        return False

    def _tick(self) -> None:
        if self.phase == _Phase.RENDER_SHOT:
            self._begin_shot_render()
        elif self.phase == _Phase.PREPARING:
            pass
        elif self.phase == _Phase.WAIT_RENDER:
            self._poll_render_wait()
        elif self.phase == _Phase.FINALIZE_SHOT:
            self._finalize_shot()
        elif self.phase == _Phase.INTER_SHOT_DRAIN:
            self._poll_inter_shot_drain()
        elif self.phase == _Phase.WRITE_REPORT:
            self._write_report_and_finish()
        elif self.phase == _Phase.DISARM:
            self._disarm_only()

    def _begin_shot_render(self) -> None:
        if self.phase != _Phase.RENDER_SHOT:
            return
        # Lock before queue/executor — nested pre_tick during render_queue_with_executor_instance
        # re-entered prepare and duplicated shot1 (post-#168 DESKTOP).
        self.phase = _Phase.PREPARING
        if self.shot_index >= len(common.SHOTS):
            self.phase = _Phase.WRITE_REPORT
            return
        shot = common.SHOTS[self.shot_index]
        self._current_shot = shot
        _log("shot start", {"id": shot["id"]})
        self._dest_abs = common.shot_dest_abs(shot["filename"])
        purge = common.purge_stale_shot_pngs(self._dest_abs)
        self._staging_dir = common.mrq_staging_dir(shot["id"])
        _clear_dir_pngs(self._staging_dir)
        cam = common.find_camera(shot["camera_labels"])
        loc, rot, pose_meta = common.resolve_camera_transform(shot, cam)
        pose_meta["fallback_source"] = shot.get("fallback_source")
        pose_meta["mrq_pie_night_reapply"] = common.reapply_night_environment_for_mrq_shot(
            shot["id"], PREFIX
        )
        prep = common.apply_lit_game_view_for_capture()
        finish = common.finish_loading_before_capture()
        viewport_diag = common.sync_editor_viewport_to_camera(cam, loc, rot)
        pose_meta["editor_prep"] = {
            "lit_game_view": prep,
            "finish_loading": finish,
            "viewport_sync": viewport_diag,
        }
        if cam:
            pose_meta["in_level_camera"] = common.actor_label(cam)
        else:
            pose_meta["in_level_camera"] = None
            pose_meta["warning"] = "no CAM_* actor — using fallback transform; verify vs Lead-visible framing"
        sequence, seq_meta = _ensure_shot_level_sequence(shot, loc, rot, in_level_cam=cam)
        self._sequence_meta = {**seq_meta, "pose": pose_meta, "purge_before_capture": purge}
        if sequence is None:
            self._finish_shot_failure("sequence_create_failed", pose_meta, purge)
            return
        self._sequence_path = common.sequence_asset_path(shot["sequence_name"])
        job_ok, job_meta = _queue_one_frame_job(
            self._subsystem,
            sequence,
            self._staging_dir,
            shot["id"],
        )
        self._job_meta = job_meta
        if not job_ok:
            self._finish_shot_failure(job_meta.get("error") or "job_setup_failed", pose_meta, purge)
            return
        self._executor_finished = False
        self._executor_success = False
        self._pie_night_stack_attempts = 0
        self._render_since = time.time()
        self._wait_deadline = time.time() + WAIT_RENDER_SEC
        exec_ok, self._executor, exec_err = _start_pie_executor(
            self._subsystem,
            self._bind_executor_finished_handler(),
        )
        job_meta["executor_started"] = exec_ok
        if exec_err:
            job_meta["executor_start_error"] = exec_err
        if not exec_ok:
            fail_msg = exec_err or "executor_start_failed"
            self._finish_shot_failure(fail_msg, pose_meta, purge)
            return
        self.phase = _Phase.WAIT_RENDER
        _log("MRQ render started", {"shot": shot["id"], "staging": self._staging_dir})

    def _bind_executor_finished_handler(self) -> Callable[[Any, bool], None]:
        """OnMoviePipelineExecutorFinished: (pipeline_executor, success) — UE 5.8 Python."""

        def _on_finished(pipeline_executor: Any, success: bool) -> None:
            self._on_executor_finished(pipeline_executor, success)

        self._executor_finished_handler_ref = _on_finished
        global _EXECUTOR_FINISHED_HANDLER
        _EXECUTOR_FINISHED_HANDLER = _on_finished
        return _on_finished

    def _on_executor_finished(self, _executor: Any, _success: bool) -> None:
        self._executor_finished = True
        self._executor_success = bool(_success)
        self._job_meta["executor_finished_delegate"] = True
        self._job_meta["executor_success"] = self._executor_success
        _log(
            "executor finished delegate",
            {"success": self._executor_success, "rendering": self._is_subsystem_rendering()},
        )

    def _centroid_for_pie_night_stack(self) -> Optional[list[float]]:
        pose = self._sequence_meta.get("pose") or {}
        reapply = pose.get("mrq_pie_night_reapply") or {}
        stack = reapply.get("mrq_pie_night_stack") or {}
        cent = stack.get("homestead_centroid") or {}
        if cent.get("used"):
            return cent["used"]
        rc = stack.get("mrq_fixture_reconfigure") or {}
        if rc.get("homestead_centroid_used"):
            return rc["homestead_centroid_used"]
        return None

    def _try_apply_mrq_pie_world_night_stack(self) -> None:
        """Re-apply PIE sky/fog/atmo during MRQ warm-up — one pre-tick apply is often too late."""
        if self._job_meta.get("executor_finished"):
            return
        import vnp_night_tune_and_evidence as vnp

        world, wl = vnp.resolve_mrq_pie_render_world()
        if not (world and wl in ("pie", "game_world")):
            self._pie_night_stack_attempts += 1
            if self._pie_night_stack_attempts >= 120:
                self._job_meta["mrq_pie_world_night_stack"] = {
                    "ok": False,
                    "error": "pie_world_never_available",
                    "attempts": self._pie_night_stack_attempts,
                }
            return

        self._pie_night_stack_attempts += 1
        att = self._pie_night_stack_attempts
        centroid = self._centroid_for_pie_night_stack()
        recapture_log = self._job_meta.setdefault("mrq_pie_skylight_recapture_ticks", [])

        if att == 1 or att % 8 == 0:
            meta = vnp.apply_mrq_pie_homestead_night_stack(
                centroid, world=world, world_label=wl
            )
            meta["render_world_resolved"] = True
            meta["apply_pass"] = "full_stack"
            meta["tick_attempt"] = att
            self._job_meta["mrq_pie_world_night_stack"] = meta
            self._job_meta["mrq_pie_world_context"] = wl
        elif att % 2 == 0:
            recap = vnp.refresh_mrq_pie_skylight_recapture(world)
            recap["tick_attempt"] = att
            recapture_log.append(recap)
            self._job_meta["mrq_pie_skylight_recapture_last"] = recap

        self._job_meta["mrq_pie_world_stack_attempts"] = att
        _log(
            "mrq pie world night stack tick",
            {
                "attempt": att,
                "world": wl,
                "full_stack": att == 1 or att % 8 == 0,
            },
        )

    def _poll_render_wait(self) -> None:
        self._try_apply_mrq_pie_world_night_stack()
        now = time.time()
        rendering = self._is_subsystem_rendering()
        found = _newest_png_since(self._staging_dir, self._render_since)
        if found:
            self._job_meta["mrq_output_path_candidate"] = found
        # Do not finalize on PNG alone — wait for OnMoviePipelineExecutorFinished + !is_rendering().
        if self._executor_finished and not rendering:
            if found:
                self._job_meta["mrq_output_path"] = found
            self._job_meta["wait_elapsed_sec"] = round(now - self._render_since, 2)
            self._job_meta["wait_gate"] = "executor_finished_and_not_rendering"
            self.phase = _Phase.FINALIZE_SHOT
            return
        if now >= self._wait_deadline:
            self._job_meta["timeout"] = True
            self._job_meta["wait_elapsed_sec"] = round(now - self._render_since, 2)
            self._job_meta["rendering_at_timeout"] = rendering
            self._job_meta["executor_finished_at_timeout"] = self._executor_finished
            if self._executor_finished and not rendering:
                if found:
                    self._job_meta["mrq_output_path"] = found
                self.phase = _Phase.FINALIZE_SHOT
            else:
                self._finish_shot_failure(
                    "render_wait_timeout_before_executor_finished",
                    (self._sequence_meta.get("pose") or {}),
                    self._sequence_meta.get("purge_before_capture") or {},
                )

    def _finalize_shot(self) -> None:
        shot = self._current_shot
        if not shot:
            self.phase = _Phase.WRITE_REPORT
            return
        mrq_out = self._job_meta.get("mrq_output_path")
        if not mrq_out:
            mrq_out = _newest_png_since(self._staging_dir, self._render_since)
        saved: Optional[str] = None
        if mrq_out and os.path.isfile(mrq_out):
            try:
                os.makedirs(os.path.dirname(self._dest_abs), exist_ok=True)
                shutil.copy2(mrq_out, self._dest_abs)
                saved = self._dest_abs if os.path.isfile(self._dest_abs) else mrq_out
            except Exception as e:
                self._job_meta["copy_error"] = str(e)
                saved = mrq_out
        validation = common.validate_png(saved)
        pose_meta = (self._sequence_meta.get("pose") or {}) if self._sequence_meta else {}
        validation = common.finalize_shot_validation(validation, shot["id"], pose_meta)
        desktop = common.copy_to_desktop(saved, shot["filename"]) if saved else {"copied": False}
        harness_pass = bool(validation.get("harness_pass"))
        entry = {
            "id": shot["id"],
            "filename": shot["filename"],
            "dest_abs": self._dest_abs,
            "sequence_path": self._sequence_path,
            "sequence_meta": self._sequence_meta,
            "mrq_job": self._job_meta,
            "primary_path": PRIMARY_PATH,
            "wait_mechanism": WAIT_MECHANISM,
            "wait_render_budget_sec": WAIT_RENDER_SEC,
            "saved_path": saved,
            "validation": validation,
            "desktop_copy": desktop,
            "harness_pass": harness_pass,
            "pass": harness_pass,
        }
        self.results.append(entry)
        _log("shot done", {"id": shot["id"], "pass": entry["pass"], "bytes": validation.get("bytes")})
        self._executor = None
        self.shot_index += 1
        if self.shot_index >= len(common.SHOTS):
            self.phase = _Phase.WRITE_REPORT
        else:
            self._inter_shot_drain_deadline = time.time() + 120.0
            self.phase = _Phase.INTER_SHOT_DRAIN
            _log("inter_shot_drain start", {"next_shot": common.SHOTS[self.shot_index]["id"]})

    def _poll_inter_shot_drain(self) -> None:
        now = time.time()
        rendering = self._is_subsystem_rendering()
        if rendering:
            return
        if now >= self._inter_shot_drain_deadline:
            _log("inter_shot_drain timeout — proceeding", {"rendering": rendering})
        self.phase = _Phase.RENDER_SHOT

    def _finish_shot_failure(
        self,
        error: str,
        pose_meta: dict[str, Any],
        purge: dict[str, Any],
    ) -> None:
        shot = self._current_shot
        if not shot:
            self.phase = _Phase.WRITE_REPORT
            return
        validation = common.validate_png(None)
        validation["error"] = error
        entry = {
            "id": shot["id"],
            "filename": shot["filename"],
            "dest_abs": self._dest_abs,
            "sequence_path": self._sequence_path,
            "sequence_meta": {**self._sequence_meta, "pose": pose_meta, "purge_before_capture": purge},
            "mrq_job": self._job_meta,
            "primary_path": PRIMARY_PATH,
            "error": error,
            "validation": validation,
            "desktop_copy": {"copied": False},
            "pass": False,
        }
        self.results.append(entry)
        _log("shot failed", {"id": shot["id"], "error": error})
        self._executor = None
        self.shot_index += 1
        if self.shot_index >= len(common.SHOTS):
            self.phase = _Phase.WRITE_REPORT
        else:
            self._inter_shot_drain_deadline = time.time() + 120.0
            self.phase = _Phase.INTER_SHOT_DRAIN

    def _write_report_and_finish(self) -> None:
        if self.phase == _Phase.DONE:
            return
        status = common.summarize_capture_report(self.results)
        all_pass = status["capture_pass"]
        executor_start_error = self._driver_error
        for shot_entry in self.results:
            err = (shot_entry.get("mrq_job") or {}).get("executor_start_error")
            if err:
                executor_start_error = executor_start_error or err
                break
        report = {
            **status,
            "prefix": PREFIX.strip(":"),
            "primary_path": PRIMARY_PATH,
            "wait_mechanism": WAIT_MECHANISM,
            "executor_start_error": executor_start_error,
            "project_dir_abs": common.project_dir(),
            "pil_available": common.pil_available(),
            "level_path": common.LEVEL_PATH,
            "level_loaded": self.level_ok,
            "mrq_available": self.mrq_ok,
            "mrq_probe": self.mrq_probe,
            "viewport_prep": self.viewport_prep,
            "keep_python_script_alive": self.keep_ok,
            "resolution": [common.RES_X, common.RES_Y],
            "custom_playback_range": [CUSTOM_START, CUSTOM_END],
            "wait_render_budget_sec": WAIT_RENDER_SEC,
            "cinematics_dir": common.CINEMATICS_PA_E_DIR,
            "shots": self.results,
            "driver_error": self._driver_error,
            "policy": (
                "Movie Render Queue one-frame PNG (PIE executor, deferred lit pass, warm-up); "
                "capture_outcome pass = harness + Lead visual framing; capture_pass = harness only; "
                "luminance PASS ≠ framing PASS (wide anchor + aim_ok + Lead eyeball); "
                "near-black = soft_fail / prove loop, not closed FAIL unless void after visible_sky_stack_ok; "
                "AL near-black = OPEN viewport capture bug (wrong buffer/pose/game-view)"
            ),
            "conductor_preflight": self.viewport_prep.get("conductor_preflight"),
            "lead_prove_loop": list(common.LEAD_PROVE_LOOP),
            "universal_testing_preconditions": list(common.UNIVERSAL_TESTING_PRECONDITIONS),
            "homestead_diagnostic_path": common.homestead_diagnostic_path(),
            "homestead_diagnostic_script": "pa_e_homestead_capture_diagnostic.py",
            "prove_criteria": common.PROVE_CRITERIA,
            "desktop_conductor_checklist": common.desktop_conductor_checklist(),
            "al_viewport_capture_bug": {
                "status": "OPEN",
                "symptom": "AutomationLibrary/HighResShot PNG on disk but near-black while Lead sees scene when rotating viewport",
                "likely_causes": [
                    "wrong viewport game-view or unlit buffer",
                    "camera pilot / pose mismatch vs CAM_Hero / CAM_CabinClose",
                    "HighResShot not bound to shot camera",
                ],
                "diagnostic_script": "capture_shotlist_viewport.py",
                "homestead_centroid_script": "pa_e_homestead_capture_diagnostic.py",
            },
            "epic_refs": [
                "https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/OnMoviePipelineExecutorFinished?application_version=5.8",
                "https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/MoviePipelineQueueSubsystem?application_version=5.8",
                "https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/MoviePipelineOutputSetting?application_version=5.8",
                "https://forums.unrealengine.com/t/unable-to-execute-moviepipelinequeue-from-python/467250",
            ],
            "ladder_doc": "docs/Automation/CAPTURE_REDUNDANCY.md",
            "ladder_rung": "1_built_in_and_in_repo",
            "fallback_script": "capture_shotlist_viewport.py",
        }
        with open(common.report_path(), "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        _log("report written", {"path": common.report_path(), "all_pass": all_pass})
        self._unregister_tick()
        self.phase = _Phase.DISARM
        self._disarm_only()
        self.phase = _Phase.DONE
        global _ACTIVE_DRIVER, _MAIN_ENTRY_ACTIVE
        if _ACTIVE_DRIVER is self:
            _ACTIVE_DRIVER = None
        _MAIN_ENTRY_ACTIVE = False

    def _disarm_only(self) -> None:
        if not self.keep_ok:
            return
        try:
            import vnp_editor_keep_alive as keep

            keep.disarm()
        except Exception:
            pass


def _log(msg: str, data: Optional[dict] = None) -> None:
    common.log(PREFIX, msg, data)


def _clear_dir_pngs(directory: str) -> None:
    if not os.path.isdir(directory):
        return
    for name in os.listdir(directory):
        if not name.lower().endswith(".png"):
            continue
        try:
            os.remove(os.path.join(directory, name))
        except OSError:
            pass


def _newest_png_since(directory: str, since_mtime: float) -> Optional[str]:
    if not os.path.isdir(directory):
        return None
    best: Optional[str] = None
    best_m = since_mtime - 0.05
    for root, _dirs, files in os.walk(directory):
        for name in files:
            if not name.lower().endswith(".png"):
                continue
            path = os.path.join(root, name)
            try:
                m = os.path.getmtime(path)
            except OSError:
                continue
            if m >= since_mtime - 0.05 and m >= best_m:
                best = path
                best_m = m
    return best


def _probe_mrq() -> dict[str, Any]:
    return common.probe_mrq_tool_readiness()


def _resolve_class(*names: str):
    for name in names:
        cls = getattr(unreal, name, None)
        if cls is not None:
            return cls, name
    return None, None


def _ensure_spawned_cine_camera(shot_id: str, loc, rot):
    label = f"PA_E_MRQ_{shot_id}"
    for a in unreal.EditorLevelLibrary.get_all_level_actors():
        if common.actor_label(a) == label:
            try:
                a.set_actor_location(loc, False, False)
                a.set_actor_rotation(rot, False)
            except Exception:
                pass
            return a, {"reused_spawned_camera": True, "label": label}
    cam_class = getattr(unreal, "CineCameraActor", None) or unreal.CameraActor
    spawned = unreal.EditorLevelLibrary.spawn_actor_from_class(cam_class, loc, rot)
    if spawned:
        try:
            spawned.set_actor_label(label)
        except Exception:
            pass
    return spawned, {"spawned_camera": True, "label": label}


def _ensure_shot_level_sequence(
    shot: dict,
    loc,
    rot,
    *,
    in_level_cam=None,
) -> tuple[Any, dict[str, Any]]:
    meta: dict[str, Any] = {"asset_path": common.sequence_asset_path(shot["sequence_name"])}
    common.ensure_cinematics_folder()
    asset_path = meta["asset_path"]
    sequence = None
    created = False
    if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        sequence = unreal.EditorAssetLibrary.load_asset(asset_path)
        meta["reused_asset"] = True
    else:
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        factory = unreal.LevelSequenceFactoryNew()
        sequence = asset_tools.create_asset(
            shot["sequence_name"],
            common.CINEMATICS_PA_E_DIR,
            unreal.LevelSequence,
            factory,
        )
        created = sequence is not None
        meta["created_asset"] = created
    if sequence is None:
        meta["error"] = "level_sequence_null"
        return None, meta

    # MRQ must follow Arrange loc/rot — reused sequences bound to CAM_Hero/CAM_CabinClose keep stale
    # Transform tracks; live actor relocate does not change the MRQ frame (post-#172 DESKTOP scrap).
    camera_actor, cam_meta = _ensure_spawned_cine_camera(shot["id"], loc, rot)
    meta.update(cam_meta)
    meta["mrq_camera_source"] = "spawned_pa_e_mrq_cine"
    if in_level_cam is not None:
        meta["in_level_cam_reference"] = common.actor_label(in_level_cam)
    if camera_actor is None:
        meta["error"] = "no_camera_actor"
        return None, meta

    try:
        unreal.MovieSceneSequenceExtensions.set_playback_start(sequence, 0)
        unreal.MovieSceneSequenceExtensions.set_playback_end(sequence, 1)
    except Exception as e:
        meta["playback_range_error"] = str(e)

    try:
        _rebuild_camera_cut(sequence, camera_actor, meta)
    except Exception as e:
        meta["camera_cut_error"] = str(e)
        return None, meta

    try:
        unreal.EditorAssetLibrary.save_asset(asset_path, only_if_is_dirty=not created)
        meta["saved"] = True
    except Exception as e:
        meta["save_error"] = str(e)
    return sequence, meta


def _strip_transform_tracks_from_binding(binding) -> int:
    removed = 0
    ext_binding = getattr(unreal, "MovieSceneBindingExtensions", None)
    ext_track = getattr(unreal, "MovieSceneTrackExtensions", None)
    transform_cls = getattr(unreal, "MovieScene3DTransformTrack", None)
    if ext_binding is None or transform_cls is None:
        return 0
    find_tracks = getattr(ext_binding, "find_tracks_by_exact_type", None)
    if not callable(find_tracks):
        find_tracks = getattr(ext_binding, "find_tracks_by_type", None)
    remove_track = getattr(ext_binding, "remove_track", None)
    if not callable(find_tracks):
        return 0
    try:
        tracks = list(find_tracks(binding, transform_cls))
    except Exception:
        return 0
    for tr in tracks:
        if ext_track is not None:
            try:
                for sec in ext_track.get_sections(tr):
                    ext_track.remove_section(tr, sec)
            except Exception:
                pass
        if callable(remove_track):
            try:
                remove_track(binding, tr)
                removed += 1
            except Exception:
                pass
    return removed


def _purge_stale_sequence_bindings(ext_seq, sequence, meta: dict[str, Any]) -> None:
    """Drop named CAM_* possessables and transform tracks so MRQ uses fresh spawned camera pose."""
    try:
        bindings = list(ext_seq.get_bindings(sequence))
    except Exception as e:
        meta["get_bindings_error"] = str(e)
        return
    meta["bindings_before_purge"] = len(bindings)
    stripped = 0
    removed = 0
    remove_binding = getattr(ext_seq, "remove_binding", None)
    for binding in bindings:
        stripped += _strip_transform_tracks_from_binding(binding)
        if callable(remove_binding):
            try:
                remove_binding(sequence, binding)
                removed += 1
            except Exception as e:
                meta.setdefault("remove_binding_errors", []).append(str(e))
    meta["transform_tracks_stripped"] = stripped
    meta["bindings_removed"] = removed


def _rebuild_camera_cut(sequence, camera_actor, meta: dict[str, Any]) -> None:
    ext_seq = unreal.MovieSceneSequenceExtensions
    ext_track = unreal.MovieSceneTrackExtensions
    ext_section = unreal.MovieSceneSectionExtensions

    _purge_stale_sequence_bindings(ext_seq, sequence, meta)

    existing = ext_seq.find_tracks_by_exact_type(sequence, unreal.MovieSceneCameraCutTrack)
    for tr in existing:
        for sec in ext_track.get_sections(tr):
            ext_track.remove_section(tr, sec)
        # remove track if API allows — else leave empty
    if not existing:
        cut_track = ext_seq.add_track(sequence, unreal.MovieSceneCameraCutTrack)
    else:
        cut_track = existing[0]
        if cut_track is None:
            cut_track = ext_seq.add_track(sequence, unreal.MovieSceneCameraCutTrack)

    binding = _resolve_possessable_binding(ext_seq, sequence, camera_actor, meta)
    binding_id = ext_seq.get_binding_id(sequence, binding)
    section = ext_track.add_section(cut_track)
    preroll = common.MRQ_CAMERA_CUT_PREROLL_FRAME
    ext_section.set_range(section, preroll, 1)
    section.set_editor_property("camera_binding_id", binding_id)
    meta["camera_binding_id"] = str(binding_id)
    meta["camera_cut_range"] = [preroll, 1]
    meta["camera_cut_track"] = True
    meta["possessable_actor"] = common.actor_label(camera_actor)


def _resolve_possessable_binding(ext_seq, sequence, camera_actor, meta: dict[str, Any]):
    """Always possess the spawned PA_E_MRQ_* camera — never reuse stale CAM_Hero bindings."""
    binding = ext_seq.add_possessable(sequence, camera_actor)
    meta["binding_match"] = "add_possessable_mrq_cam"
    meta["possessable_actor_label"] = common.actor_label(camera_actor)
    return binding


def _clear_queue(queue) -> None:
    delete_all = getattr(queue, "delete_all_jobs", None)
    if callable(delete_all):
        delete_all()
        return
    get_jobs = getattr(queue, "get_jobs", None)
    delete_job = getattr(queue, "delete_job", None)
    if callable(get_jobs) and callable(delete_job):
        for job in list(get_jobs()):
            delete_job(job)


def _add_mrq_pie_night_console_settings(cfg, meta: dict[str, Any]) -> None:
    """Push exposure clamps into MRQ job so PIE render world matches Editor night stack."""
    try:
        import vnp_night_tune_and_evidence as vnp

        cvar_cmds = vnp.MRQ_PIE_RENDER_CVARS
    except Exception as e:
        meta["mrq_pie_console_cvars"] = {"error": str(e)}
        return
    setting_cls = getattr(unreal, "MoviePipelineConsoleVariableSetting", None)
    if setting_cls is None:
        meta["mrq_pie_console_cvars"] = "MoviePipelineConsoleVariableSetting_missing"
        return
    try:
        setting = cfg.find_or_add_setting_by_class(setting_cls)
        applied: list[dict[str, Any]] = []
        for cmd in cvar_cmds:
            parts = cmd.split()
            if len(parts) < 2:
                continue
            name, value = parts[0], parts[1]
            ok = False
            for method_name in ("add_or_update_console_variable", "add_console_variable", "set_console_variable"):
                fn = getattr(setting, method_name, None)
                if not callable(fn):
                    continue
                try:
                    fn(name, value)
                    ok = True
                    break
                except TypeError:
                    try:
                        fn(name, value, True)
                        ok = True
                        break
                    except Exception:
                        pass
                except Exception:
                    pass
            applied.append({"name": name, "value": value, "ok": ok})
        meta["mrq_pie_console_cvars"] = applied
    except Exception as e:
        meta["mrq_pie_console_cvars_error"] = str(e)


def _queue_one_frame_job(
    subsystem,
    sequence,
    output_dir_abs: str,
    shot_id: str,
) -> tuple[bool, dict[str, Any]]:
    meta: dict[str, Any] = {"output_dir_abs": output_dir_abs}
    queue = subsystem.get_queue()
    _clear_queue(queue)
    job = None
    create_from_seq = getattr(unreal.MoviePipelineEditorLibrary, "create_job_from_sequence", None)
    if callable(create_from_seq):
        try:
            job = create_from_seq(queue, sequence)
            meta["job_create"] = "MoviePipelineEditorLibrary.create_job_from_sequence"
        except Exception as e:
            meta["create_job_from_sequence_error"] = str(e)
    if job is None:
        try:
            job = queue.allocate_new_job(unreal.MoviePipelineExecutorJob)
            for setter in (
                lambda: job.set_editor_property("sequence", sequence),
                lambda: job.set_sequence(sequence),
            ):
                try:
                    setter()
                    break
                except Exception:
                    continue
            meta["job_create"] = "allocate_new_job"
        except Exception as e:
            meta["error"] = str(e)
            return False, meta

    try:
        job.set_editor_property("map", unreal.SoftObjectPath(common.LEVEL_PATH))
    except Exception as e:
        meta["map_set_error"] = str(e)

    cfg = job.get_configuration()
    deferred_cls, deferred_name = _resolve_class(
        "MoviePipelineDeferredPassBase",
        "MoviePipelineDeferredPass",
    )
    png_cls, png_name = _resolve_class("MoviePipelineImageSequenceOutput_PNG")
    if deferred_cls:
        deferred = cfg.find_or_add_setting_by_class(deferred_cls)
        meta["deferred_pass"] = deferred_name
        try:
            deferred.set_is_enabled(True)
        except Exception:
            pass
    else:
        meta["deferred_pass"] = "missing"
    if png_cls:
        cfg.find_or_add_setting_by_class(png_cls)
        meta["png_output"] = png_name
    else:
        meta["error"] = "MoviePipelineImageSequenceOutput_PNG missing"
        return False, meta

    output = cfg.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
    output.use_custom_playback_range = True
    output.custom_start_frame = CUSTOM_START
    output.custom_end_frame = CUSTOM_END
    output.output_resolution = unreal.IntPoint(common.RES_X, common.RES_Y)
    # Level-sequence jobs without MRQ shot tracks leave {shot_name} empty → ".0" / "shot.0" files.
    output.file_name_format = f"{shot_id}_{{frame_number}}"
    meta["file_name_format"] = output.file_name_format
    output.override_existing_output = True
    output.zero_pad_frame_numbers = 0
    output.output_directory = unreal.DirectoryPath(output_dir_abs.replace("\\", "/"))
    try:
        job.set_editor_property("job_name", f"PA_E_{shot_id}")
    except Exception:
        pass
    meta["custom_playback_range"] = [CUSTOM_START, CUSTOM_END]
    meta["resolution"] = [common.RES_X, common.RES_Y]

    aa_cls = getattr(unreal, "MoviePipelineAntiAliasingSetting", None)
    if aa_cls is not None:
        try:
            aa = cfg.find_or_add_setting_by_class(aa_cls)
            aa.engine_warm_up_count = common.MRQ_ENGINE_WARMUP_COUNT
            aa.render_warm_up_count = common.MRQ_RENDER_WARMUP_COUNT
            aa.render_warm_up_frames = True
            aa.use_camera_cut_for_warm_up = True
            meta["anti_aliasing_warmup"] = {
                "engine_warm_up_count": common.MRQ_ENGINE_WARMUP_COUNT,
                "render_warm_up_count": common.MRQ_RENDER_WARMUP_COUNT,
                "render_warm_up_frames": True,
                "use_camera_cut_for_warm_up": True,
            }
        except Exception as e:
            meta["anti_aliasing_warmup_error"] = str(e)
    _add_mrq_pie_night_console_settings(cfg, meta)
    return True, meta


def _start_pie_executor(
    subsystem,
    on_finished: Callable[[Any, bool], None],
) -> tuple[bool, Any, Optional[str]]:
    """Bind OnMoviePipelineExecutorFinished (2 args) then start PIE executor."""
    executor = None
    err: Optional[str] = None
    try:
        executor_cls = unreal.MoviePipelinePIEExecutor
        if hasattr(subsystem, "render_queue_with_executor_instance"):
            executor = executor_cls(subsystem)
            if hasattr(executor, "on_executor_finished_delegate"):
                delegate = executor.on_executor_finished_delegate
                bind = getattr(delegate, "add_callable_unique", None)
                if callable(bind):
                    bind(on_finished)
                else:
                    delegate.add_callable(on_finished)
            subsystem.render_queue_with_executor_instance(executor)
            return True, executor, None
        subsystem.render_queue_with_executor(executor_cls)
        return True, executor, None
    except Exception as e:
        err = str(e)
        _log("executor start failed", {"error": err})
        return False, executor, err


def _release_main_entry() -> None:
    global _MAIN_ENTRY_ACTIVE
    _MAIN_ENTRY_ACTIVE = False


def reset_mrq_session_guards() -> None:
    """Clear stale orchestrator flags so MCP re-prove does not no-op (DESKTOP prove PASS)."""
    global _ACTIVE_DRIVER, _MAIN_ENTRY_ACTIVE
    driver = _ACTIVE_DRIVER
    if driver is not None:
        try:
            driver._unregister_tick()
        except Exception:
            pass
    _ACTIVE_DRIVER = None
    _MAIN_ENTRY_ACTIVE = False


def main() -> None:
    global _ACTIVE_DRIVER, _MAIN_ENTRY_ACTIVE
    reset_mrq_session_guards()
    _MAIN_ENTRY_ACTIVE = True
    _log("started")
    common.reload_pa_e_capture_python_modules()
    keep_ok = False
    try:
        import vnp_editor_keep_alive as keep

        keep_ok = keep.arm()
    except Exception as e:
        _log("keep_alive import/arm skipped", {"error": str(e)})

    mrq_probe = _probe_mrq()
    mrq_ok = bool(mrq_probe.get("available"))

    conductor_preflight = common.conductor_mrq_capture_preflight(PREFIX)
    if not conductor_preflight.get("ready"):
        common.write_blocked_capture_report(
            prefix=PREFIX,
            primary_path=PRIMARY_PATH,
            arrange_gate={
                "ready": False,
                "blocked_reasons": conductor_preflight.get("blocked_reasons") or [],
                "conductor_preflight": conductor_preflight,
            },
            level_loaded=False,
            keep_python_script_alive=keep_ok,
            mrq_probe=mrq_probe,
            extra={"conductor_preflight": conductor_preflight},
        )
        if keep_ok:
            try:
                import vnp_editor_keep_alive as keep

                keep.disarm()
            except Exception:
                pass
        _release_main_entry()
        return

    level_ok = common.load_level(PREFIX)
    world_recheck = common.ensure_markers_editor_world(PREFIX)
    if not world_recheck.get("ok"):
        level_ok = False
    arrange_gate = common.arrange_pa_e_shotlist(
        PREFIX,
        level_loaded=level_ok,
        require_mrq=True,
        mrq_probe=mrq_probe,
    )
    homestead_diag = common.write_homestead_capture_diagnostic(
        PREFIX,
        level_loaded=level_ok,
        homestead_night_environment=arrange_gate.get("lighting"),
        arrange_gate=arrange_gate,
    )
    viewport_prep: dict[str, Any] = {
        "homestead_diagnostic": homestead_diag,
        "arrange_gate": arrange_gate,
        "conductor_preflight": conductor_preflight,
        "world_gate": world_recheck,
        "finish_loading": arrange_gate.get("finish_loading"),
        "homestead_night_environment": arrange_gate.get("lighting"),
    }
    viewport_prep.update(arrange_gate.get("view") or {})

    if not arrange_gate.get("ready"):
        common.write_blocked_capture_report(
            prefix=PREFIX,
            primary_path=PRIMARY_PATH,
            arrange_gate=arrange_gate,
            level_loaded=level_ok,
            keep_python_script_alive=keep_ok,
            mrq_probe=mrq_probe,
        )
        if keep_ok:
            try:
                import vnp_editor_keep_alive as keep

                keep.disarm()
            except Exception:
                pass
        _release_main_entry()
        return

    orch = _MrqOrchestrator(
        keep_ok=keep_ok,
        level_ok=level_ok,
        mrq_ok=mrq_ok,
        mrq_probe=mrq_probe,
        viewport_prep=viewport_prep,
    )
    if not orch.start():
        report = {
            "ok": False,
            "prefix": PREFIX.strip(":"),
            "primary_path": PRIMARY_PATH,
            "driver_error": orch._driver_error,
            "executor_start_error": orch._driver_error,
            "mrq_probe": mrq_probe,
            "level_loaded": level_ok,
            "shots": [],
        }
        with open(common.report_path(), "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        if keep_ok:
            try:
                import vnp_editor_keep_alive as keep

                keep.disarm()
            except Exception:
                pass
        _release_main_entry()
        return
    _ACTIVE_DRIVER = orch


if __name__ == "__main__":
    main()

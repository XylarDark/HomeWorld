"""PA-E shotlist capture — Movie Render Queue (MRQ) one-frame primary.

Loads L_VS_MVP_Markers, ensures minimal Level Sequences under
/Game/HomeWorld/Cinematics/PA_E/ (runtime create-if-missing; DESKTOP first run
may save tiny .uasset binaries locally), queues MRQ jobs with custom one-frame
playback range, PNG deferred pass, async PIE executor + Slate pre-tick wait.

Near-black AutomationLibrary stills are an **OPEN viewport capture bug** (wrong pose /
game-view / pilot / empty buffer) — scene content is visible to Lead in Editor;
MRQ must frame the same in-level **CAM_Hero** / **CAM_CabinClose** with deferred
lit pass + warm-up. PASS requires **lit homestead** stills, not file-exists-only.

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
    WAIT_RENDER = "wait_render"
    FINALIZE_SHOT = "finalize_shot"
    WRITE_REPORT = "write_report"
    DISARM = "disarm"
    DONE = "done"


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

    def start(self) -> bool:
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
        try:
            self._tick()
        except Exception as e:
            _log("orchestrator tick error", {"error": str(e), "phase": self.phase.value})
            self.phase = _Phase.WRITE_REPORT
            self._driver_error = self._driver_error or str(e)

    def _tick(self) -> None:
        if self.phase == _Phase.RENDER_SHOT:
            self._begin_shot_render()
        elif self.phase == _Phase.WAIT_RENDER:
            self._poll_render_wait()
        elif self.phase == _Phase.FINALIZE_SHOT:
            self._finalize_shot()
        elif self.phase == _Phase.WRITE_REPORT:
            self._write_report_and_finish()
        elif self.phase == _Phase.DISARM:
            self._disarm_only()

    def _begin_shot_render(self) -> None:
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
        sequence, seq_meta = _ensure_shot_level_sequence(shot, cam, loc, rot)
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
        self._render_since = time.time()
        self._wait_deadline = time.time() + WAIT_RENDER_SEC
        exec_ok, self._executor = _start_pie_executor(self._subsystem, self._on_executor_finished)
        job_meta["executor_started"] = exec_ok
        if not exec_ok:
            self._finish_shot_failure("executor_start_failed", pose_meta, purge)
            return
        self.phase = _Phase.WAIT_RENDER
        _log("MRQ render started", {"shot": shot["id"], "staging": self._staging_dir})

    def _on_executor_finished(self, _executor: Any, _success: bool, _info: Any) -> None:
        _log("executor finished delegate", {"success": bool(_success)})

    def _poll_render_wait(self) -> None:
        now = time.time()
        rendering = False
        try:
            if self._subsystem and hasattr(self._subsystem, "is_rendering"):
                rendering = bool(self._subsystem.is_rendering())
        except Exception:
            rendering = False
        found = _newest_png_since(self._staging_dir, self._render_since)
        if found and not rendering:
            self._job_meta["mrq_output_path"] = found
            self._job_meta["wait_elapsed_sec"] = round(now - self._render_since, 2)
            self.phase = _Phase.FINALIZE_SHOT
            return
        if found and (now - self._render_since) > 5.0:
            self._job_meta["mrq_output_path"] = found
            self._job_meta["wait_elapsed_sec"] = round(now - self._render_since, 2)
            self._job_meta["note"] = "png_found_while_is_rendering_true"
            self.phase = _Phase.FINALIZE_SHOT
            return
        if now >= self._wait_deadline:
            self._job_meta["timeout"] = True
            self._job_meta["wait_elapsed_sec"] = round(now - self._render_since, 2)
            self._job_meta["rendering_at_timeout"] = rendering
            if found:
                self._job_meta["mrq_output_path"] = found
            self.phase = _Phase.FINALIZE_SHOT

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
        desktop = common.copy_to_desktop(saved, shot["filename"]) if saved else {"copied": False}
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
            "pass": bool(validation.get("pass")),
        }
        self.results.append(entry)
        _log("shot done", {"id": shot["id"], "pass": entry["pass"], "bytes": validation.get("bytes")})
        self._executor = None
        self.shot_index += 1
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
        self.phase = _Phase.RENDER_SHOT

    def _write_report_and_finish(self) -> None:
        if self.phase == _Phase.DONE:
            return
        status = common.summarize_capture_report(self.results)
        all_pass = status["capture_pass"]
        report = {
            **status,
            "prefix": PREFIX.strip(":"),
            "primary_path": PRIMARY_PATH,
            "wait_mechanism": WAIT_MECHANISM,
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
                "PASS = lit homestead visible (luminance gate), not file-exists-only; "
                "near-black = prove loop in progress (inventory→aim→capture→bug-fix), not closed FAIL; "
                "AL near-black = OPEN viewport capture bug (wrong buffer/pose/game-view)"
            ),
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
                "https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/MoviePipelineQueueSubsystem?application_version=5.7",
                "https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/MoviePipelineOutputSetting?application_version=5.7",
                "https://forums.unrealengine.com/t/unable-to-render-movie-render-queue-pie-executor-from-commandline-python-script/2556294",
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
    probe: dict[str, Any] = {"available": False}
    required = (
        "MoviePipelineQueueSubsystem",
        "MoviePipelineExecutorJob",
        "MoviePipelinePIEExecutor",
        "MoviePipelineOutputSetting",
        "MoviePipelineImageSequenceOutput_PNG",
    )
    missing = [n for n in required if not hasattr(unreal, n)]
    probe["missing_types"] = missing
    if missing:
        probe["error"] = "missing_unreal_types: " + ", ".join(missing)
        probe["plugin_hint"] = [
            "MovieRenderPipeline",
            "MovieRenderPipelineEditor",
            "SequencerScripting",
        ]
        return probe
    try:
        subsys = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
        probe["subsystem"] = subsys is not None
        if subsys is None:
            probe["error"] = "MoviePipelineQueueSubsystem get_editor_subsystem returned None"
            return probe
    except Exception as e:
        probe["error"] = str(e)
        return probe
    probe["available"] = True
    return probe


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


def _ensure_shot_level_sequence(shot: dict, cam, loc, rot) -> tuple[Any, dict[str, Any]]:
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

    camera_actor = cam
    cam_meta: dict[str, Any] = {}
    if camera_actor is None:
        camera_actor, cam_meta = _ensure_spawned_cine_camera(shot["id"], loc, rot)
    meta.update(cam_meta)
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


def _rebuild_camera_cut(sequence, camera_actor, meta: dict[str, Any]) -> None:
    ext_seq = unreal.MovieSceneSequenceExtensions
    ext_track = unreal.MovieSceneTrackExtensions
    ext_section = unreal.MovieSceneSectionExtensions

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
    label = common.actor_label(camera_actor)
    find_by_name = getattr(ext_seq, "find_binding_by_name", None)
    if callable(find_by_name):
        try:
            found = find_by_name(sequence, label)
            if found is not None:
                meta["binding_match"] = "find_binding_by_name"
                return found
        except Exception as e:
            meta["find_binding_by_name_error"] = str(e)
    bindings = ext_seq.get_bindings(sequence)
    if len(bindings) == 1:
        meta["binding_match"] = "single_existing_binding"
        return bindings[0]
    binding = ext_seq.add_possessable(sequence, camera_actor)
    meta["binding_match"] = "add_possessable"
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
    output.file_name_format = "{shot_name}.{frame_number}"
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
    return True, meta


def _start_pie_executor(subsystem, on_finished: Callable) -> tuple[bool, Any]:
    executor = None
    try:
        executor_cls = unreal.MoviePipelinePIEExecutor
        if hasattr(subsystem, "render_queue_with_executor_instance"):
            executor = executor_cls(subsystem)
            if hasattr(executor, "on_executor_finished_delegate"):
                executor.on_executor_finished_delegate.add_callable(on_finished)
            subsystem.render_queue_with_executor_instance(executor)
            return True, executor
        subsystem.render_queue_with_executor(executor_cls)
        return True, executor
    except Exception as e:
        _log("executor start failed", {"error": str(e)})
        return False, executor


def _apply_mrq_scene_prep(viewport_prep: dict[str, Any]) -> None:
    viewport_prep["finish_loading"] = common.finish_loading_before_capture()
    viewport_prep.update(common.apply_lit_game_view_for_capture())
    viewport_prep["time_of_day"] = common.apply_pa_e_shotlist_time_of_day(PREFIX)


def main() -> None:
    _log("started")
    keep_ok = False
    try:
        import vnp_editor_keep_alive as keep

        keep_ok = keep.arm()
    except Exception as e:
        _log("keep_alive import/arm skipped", {"error": str(e)})

    mrq_probe = _probe_mrq()
    mrq_ok = bool(mrq_probe.get("available"))

    level_ok = common.load_level(PREFIX)
    homestead_diag = common.write_homestead_capture_diagnostic(PREFIX)
    viewport_prep: dict[str, Any] = {"homestead_diagnostic": homestead_diag}
    _apply_mrq_scene_prep(viewport_prep)

    if not mrq_ok:
        report = {
            "ok": False,
            "capture_pass": False,
            "closed_fail": True,
            "prove_loop_status": "blocked",
            "lead_prove_loop": list(common.LEAD_PROVE_LOOP),
            "homestead_diagnostic_path": common.homestead_diagnostic_path(),
            "prefix": PREFIX.strip(":"),
            "primary_path": PRIMARY_PATH,
            "mrq_available": False,
            "mrq_probe": mrq_probe,
            "level_loaded": level_ok,
            "keep_python_script_alive": keep_ok,
            "prove_criteria": common.PROVE_CRITERIA,
            "desktop_conductor_checklist": common.desktop_conductor_checklist(),
            "shots": [],
            "policy": "Enable MovieRenderPipeline + MovieRenderPipelineEditor in HomeWorld.uproject then Safe-Build",
        }
        with open(common.report_path(), "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        if keep_ok:
            try:
                import vnp_editor_keep_alive as keep

                keep.disarm()
            except Exception:
                pass
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


if __name__ == "__main__":
    main()

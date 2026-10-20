# quest_test_runner.py
# The in-editor opening quest sweep. Runs inside the Unreal Editor through
# execute_python_script("quest_tests.py"). One fresh PIE per stop, real
# hw.Playtest.FastForward, then a read-only state snapshot and assertions.
#
# It is tick-driven: the MCP call arms it and returns; the Slate post-tick
# callback advances the run so the Editor keeps ticking. Poll
# Saved/quest_tests_status.json for progress and Saved/quest_tests.json for
# the result. Never block the game thread with sleep here.
#
# Results are preconditions, not the human pass. The queue tables in
# Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md stay human-owned. Check validation and
# evaluation live in quest_test_contract.py so host pytest can run them.

import importlib
import json
import os
import time
import traceback

import unreal

import quest_test_contract as contract
import quest_test_manifest as manifest

LEVEL_PATH = "/Game/HomeWorld/Maps/SizeTest/L_SizeTest"
LEVEL_TOKEN = "L_SizeTest"

POLL_S = 0.25
SETTLE_S = 0.75
# A Slate tick gap longer than this is an Editor stall, not test time. The phase
# clock pauses so a shader compile or another editor task does not fail a beat.
STALL_S = 2.0

PHASE_LIMIT = {
    "precheck": 90.0,
    "wait_stop_pre": 45.0,
    "load_level": 90.0,
    "stop_pie": 15.0,
    "wait_stop_pie": 45.0,
    "start_pie": 15.0,
    "wait_pie": 60.0,
    "wait_pawn": 30.0,
    "send": 10.0,
    "wait_ready": 150.0,
    "snapshot": 15.0,
    "end_pie": 15.0,
    "wait_end_pie": 45.0,
    "settle": 10.0,
}

FAILURE_MARKERS = (
    "timed out",
    " failed",
    "unknown",
    "missing",
    "refused",
    "no opening reveal",
    "already night",
)

_RUN = {
    "active": False,
    "done": False,
    "phase": "idle",
}
_TICK_HANDLE = None


# ---------------------------------------------------------------------------
# Paths and small helpers
# ---------------------------------------------------------------------------

def _project_dir():
    return unreal.Paths.project_dir().rstrip("/\\")


def _saved_path(name):
    saved = os.path.join(_project_dir(), "Saved")
    os.makedirs(saved, exist_ok=True)
    return os.path.join(saved, name)


def _now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())


def _clock():
    """Suite time: wall time minus Editor stalls, so phase limits do not count a frozen tick."""
    return time.time() - _RUN.get("clock_offset", 0.0)


def _write_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, default=str)
    os.replace(tmp, path)


def _log_path():
    logs = os.path.join(_project_dir(), "Saved", "Logs")
    preferred = os.path.join(logs, "HomeWorld.log")
    if os.path.isfile(preferred):
        return preferred
    try:
        candidates = [
            os.path.join(logs, name)
            for name in os.listdir(logs)
            if name.lower().endswith(".log")
        ]
        if candidates:
            return max(candidates, key=os.path.getmtime)
    except OSError:
        pass
    return preferred


def _log_size():
    try:
        return os.path.getsize(_log_path())
    except OSError:
        return 0


def _log_since(offset):
    path = _log_path()
    try:
        size = os.path.getsize(path)
        if size < offset:
            offset = 0
        with open(path, "rb") as handle:
            handle.seek(offset)
            data = handle.read()
    except OSError:
        return []
    lines = [
        line for line in data.decode("utf-8", errors="replace").splitlines()
        if "playtest_ff:" in line
    ]
    return lines[-8:]


def _mcp_since(offset):
    """Raw Editor commands received after offset. The suite itself is armed before start()."""
    path = _log_path()
    try:
        size = os.path.getsize(path)
        if size < offset:
            offset = 0
        with open(path, "rb") as handle:
            handle.seek(offset)
            data = handle.read()
    except OSError:
        return []
    hits = []
    for line in data.decode("utf-8", errors="replace").splitlines():
        if "MCPServerRunnable: Received:" not in line or '"type"' not in line:
            continue
        # The host's arm call can be flushed just after start(). It is the suite
        # itself; a second call is rejected by quest_tests.py while active.
        if "quest_tests.py" in line:
            continue
        hits.append(line.strip())
    return hits[-4:]


def _subsys():
    return unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)


def _editor_world():
    try:
        return unreal.EditorLevelLibrary.get_editor_world()
    except Exception:
        return None


def _pie_world():
    try:
        worlds = unreal.EditorLevelLibrary.get_pie_worlds(False)
        return worlds[0] if worlds else None
    except Exception:
        return None


def _pawn():
    world = _pie_world()
    if not world:
        return None
    try:
        return unreal.GameplayStatics.get_player_pawn(world, 0)
    except Exception:
        return None


def _state(pawn):
    """Return (state dict, error). The getter is the versioned contract."""
    if pawn is None:
        return None, "no pawn"
    getter = getattr(pawn, "get_playtest_state_json", None)
    if getter is None:
        return None, "GetPlaytestStateJson missing - rebuild the editor module"
    try:
        return json.loads(getter()), None
    except Exception as exc:
        return None, "state JSON failed: " + str(exc)


def _all_actors(world):
    try:
        return list(unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor) or [])
    except Exception:
        return []


def _first_of_class(world, cls):
    try:
        actors = unreal.GameplayStatics.get_all_actors_of_class(world, cls) or []
        return actors[0] if actors else None
    except Exception:
        return None


def _tags(actor):
    try:
        return [str(tag) for tag in actor.tags]
    except Exception:
        return []


def _loc(actor):
    try:
        point = actor.get_actor_location()
        return [round(float(point.x), 2), round(float(point.y), 2), round(float(point.z), 2)]
    except Exception:
        return None


def _vec(value):
    if value is None:
        return None
    try:
        return [round(float(value.x), 2), round(float(value.y), 2), round(float(value.z), 2)]
    except Exception:
        return None


def _call(obj, method):
    if obj is None:
        return None
    fn = getattr(obj, method, None)
    if fn is None:
        return None
    try:
        return fn()
    except Exception:
        return None


def _bounds(actor):
    result = actor.get_actor_bounds(False)
    if isinstance(result, tuple):
        origin, extent = result
    else:
        origin = result.origin
        extent = result.box_extent
    return origin, extent


# ---------------------------------------------------------------------------
# Status and results
# ---------------------------------------------------------------------------

def _all_passed():
    selected = _RUN.get("selected", [])
    results = _RUN.get("results", [])
    return contract.all_passed(
        [quest.get("id") for quest in selected],
        results,
    )


def _result_doc():
    results = _RUN.get("results", [])
    counted = contract.counts(results)
    passed = counted["passed"]
    failed = counted["failed"]
    inconclusive = counted["inconclusive"]
    return {
        "suite": "opening quest sweep",
        "run_id": _RUN.get("run_id"),
        "level": LEVEL_PATH,
        "started_at": _RUN.get("started_at"),
        "finished_at": _RUN.get("finished_at"),
        "done": bool(_RUN.get("done", False)),
        "active": bool(_RUN.get("active", False)),
        "error": _RUN.get("error"),
        "selected": [quest.get("id") for quest in _RUN.get("selected", [])],
        "beats_run": len(results),
        "passed": passed,
        "failed": failed,
        "inconclusive": inconclusive,
        "all_passed": _all_passed(),
        "stalls": _RUN.get("stalls", []),
        "beats": results,
        "note": (
            "Preconditions only. The queue pass tables in "
            "Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md stay human."
        ),
    }


def _write_results():
    _write_json(_saved_path("quest_tests.json"), _result_doc())


def _write_status(force=False):
    now = time.time()
    if not force and now - _RUN.get("last_status", 0.0) < 0.5:
        return
    _RUN["last_status"] = now
    current = _RUN.get("current") or {}
    selected = _RUN.get("selected", [])
    index = _RUN.get("index", 0)
    _write_json(_saved_path("quest_tests_status.json"), {
        "suite": "opening quest sweep",
        "run_id": _RUN.get("run_id"),
        "phase": _RUN.get("phase", "idle"),
        "beat": current.get("id"),
        "index": min(index + 1, len(selected)) if selected else 0,
        "total": len(selected),
        "done": bool(_RUN.get("done", False)),
        "active": bool(_RUN.get("active", False)),
        "error": _RUN.get("error"),
        "updated_at": now,
    })


# ---------------------------------------------------------------------------
# Assertions and snapshot
# ---------------------------------------------------------------------------

def _evaluate(beat, snapshot):
    assertions, status = contract.evaluate_checks(beat.get("checks", []), snapshot)
    return {
        "id": beat.get("id"),
        "stop": beat.get("stop"),
        "section": beat.get("section"),
        "note": beat.get("note"),
        "status": status,
        "duration_s": round(_clock() - _RUN.get("beat_started", _clock()), 2),
        "assertions": assertions,
        "snapshot": snapshot,
    }


def _build_snapshot(world, pawn):
    state, error = _state(pawn)
    if state is None:
        raise RuntimeError(error or "state missing")

    quest = dict(state)
    beat = {
        "ready_for": quest.pop("ready_for", ""),
        "ready_distance": quest.pop("ready_distance", -1.0),
        "fast_forward_step": quest.pop("fast_forward_step", -1),
    }

    all_actors = _all_actors(world)
    tag_counts = {}
    tagged = {}
    wanted = ("NPC_PARTNER", "KettleCounter", "NODE_CONSUMABLE_STATION")
    for actor in all_actors:
        for tag in _tags(actor):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
            if tag in wanted and tag not in tagged:
                tagged[tag] = actor

    actors = {"pawn": {"location": _loc(pawn)}}

    reveal = _first_of_class(world, unreal.HomeWorldOpeningReveal)
    if reveal is not None:
        actors["reveal"] = {
            "location": _loc(reveal),
            "spirit_visible": _call(reveal, "is_spirit_visible"),
            "partner_waiting": _call(reveal, "is_partner_waiting"),
            "partner_stand": _vec(_call(reveal, "get_partner_stand_cm")),
        }

    partner = tagged.get("NPC_PARTNER")
    if partner is not None:
        actors["partner"] = {"location": _loc(partner)}

    counter = tagged.get("KettleCounter") or tagged.get("NODE_CONSUMABLE_STATION")
    if counter is not None:
        try:
            origin, extent = _bounds(counter)
            actors["counter"] = {
                "location": _vec(origin),
                "east_face": round(float(origin.x + extent.x), 2),
                "west_face": round(float(origin.x - extent.x), 2),
            }
        except Exception as exc:
            actors["counter"] = {"error": str(exc)}

    dog = _first_of_class(world, unreal.HomeWorldOpeningDog)
    if dog is not None:
        actors["dog"] = {
            "location": _loc(dog),
            "tamed": _call(dog, "is_dog_tamed"),
        }

    actors["wisps"] = {"count": tag_counts.get("NODE_OPENING_WISP", 0)}
    return {
        "quest": quest,
        "beat": beat,
        "actors": actors,
        "tag_counts": tag_counts,
    }


# ---------------------------------------------------------------------------
# Run state
# ---------------------------------------------------------------------------

def is_running():
    return bool(_RUN.get("active", False))


def shutdown():
    global _TICK_HANDLE
    if _TICK_HANDLE is not None:
        try:
            unreal.unregister_slate_post_tick_callback(_TICK_HANDLE)
        except Exception:
            pass
        _TICK_HANDLE = None
    _RUN["active"] = False


def _read_request():
    path = _saved_path("quest_tests_request.json")
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            request = json.load(handle)
    except Exception as exc:
        unreal.log_warning("quest_tests: bad request JSON: " + str(exc))
        request = {}
    try:
        os.remove(path)
    except OSError:
        pass
    return request


def _start_error(message, run_id=None):
    _RUN.clear()
    _RUN.update({
        "active": False,
        "done": True,
        "phase": "done",
        "run_id": run_id,
        "selected": [],
        "results": [],
        "index": 0,
        "current": None,
        "error": message,
        "started_at": _now_iso(),
        "finished_at": _now_iso(),
        "last_status": 0.0,
    })
    _write_results()
    _write_status(force=True)
    unreal.log_error("quest_tests: " + message)


def start():
    global _TICK_HANDLE
    if _RUN.get("active"):
        current = _RUN.get("current") or {}
        unreal.log("quest_tests: already running (%s, phase %s)" % (
            current.get("id") or "starting", _RUN.get("phase")))
        return

    request = _read_request()
    run_id = str(request.get("run_id") or ("local-%s-%d" % (
        time.strftime("%Y%m%d-%H%M%S", time.localtime()), os.getpid())))
    try:
        importlib.reload(manifest)
        importlib.reload(contract)
    except Exception as exc:
        _start_error("manifest/contract reload failed: " + str(exc), run_id)
        return

    contract_errors = contract.validate_manifest(manifest.QUESTS)
    if contract_errors:
        _start_error(
            "manifest contract failed: " + "; ".join(contract_errors),
            run_id,
        )
        return

    wanted = request.get("only") or []
    if wanted:
        wanted = [str(item) for item in wanted]
        unknown = [item for item in wanted if manifest.by_id(item) is None]
        if unknown:
            _start_error("unknown quest id(s): " + ", ".join(unknown), run_id)
            return
        wanted_set = set(wanted)
        selected = [quest for quest in manifest.QUESTS if quest.get("id") in wanted_set]
    else:
        selected = list(manifest.QUESTS)

    if not selected:
        _start_error("no beats selected", run_id)
        return

    if _TICK_HANDLE is not None:
        shutdown()

    _RUN.clear()
    _RUN.update({
        "active": True,
        "done": False,
        "phase": "precheck",
        "run_id": run_id,
        "phase_started": time.time(),
        "selected": selected,
        "index": 0,
        "current": None,
        "current_recorded": False,
        "results": [],
        "error": None,
        "started_at": _now_iso(),
        "finished_at": None,
        "load_level": bool(request.get("load_level", True)),
        "log_offset": 0,
        "command_sent_at": 0.0,
        "last_poll": 0.0,
        "beat_started": 0.0,
        "settle_until": 0.0,
        "last_status": 0.0,
        "last_tick_at": None,
        "clock_offset": 0.0,
        "stalls": [],
        "mcp_offset": 0,
    })
    _write_results()
    _write_status(force=True)

    try:
        _TICK_HANDLE = unreal.register_slate_post_tick_callback(_tick)
    except Exception as exc:
        _RUN["active"] = False
        _RUN["done"] = True
        _RUN["error"] = "tick registration failed: " + str(exc)
        _RUN["finished_at"] = _now_iso()
        _write_results()
        _write_status(force=True)
        unreal.log_error("quest_tests: " + _RUN["error"])
        return

    unreal.log("quest_tests: armed %d beats: %s" % (
        len(selected), ", ".join(quest.get("id", "?") for quest in selected)))
    _RUN["mcp_offset"] = _log_size()


def _set_phase(phase):
    _RUN["phase"] = phase
    _RUN["phase_started"] = _clock()
    _write_status(force=True)


def _end_pie_if_running():
    try:
        subsys = _subsys()
        if subsys and subsys.is_in_play_in_editor():
            subsys.editor_request_end_play()
    except Exception:
        pass


def _finish(success, error=None):
    if _RUN.get("done"):
        return
    _RUN["active"] = False
    _RUN["done"] = True
    _RUN["finished_at"] = _now_iso()
    _RUN["phase"] = "done"
    if error:
        _RUN["error"] = error
    _end_pie_if_running()
    _write_results()
    _write_status(force=True)
    doc = _result_doc()
    unreal.log("quest_tests: %d/%d passed, %d failed, %d inconclusive%s" % (
        doc["passed"], doc["beats_run"], doc["failed"], doc["inconclusive"],
        "" if doc["all_passed"] else " (not green)"))
    shutdown()


def _fail_current(message, inconclusive=False):
    current = _RUN.get("current")
    if current and not _RUN.get("current_recorded"):
        _RUN["results"].append({
            "id": current.get("id"),
            "stop": current.get("stop"),
            "section": current.get("section"),
            "note": current.get("note"),
            "status": "inconclusive" if inconclusive else "failed",
            "duration_s": round(_clock() - _RUN.get("beat_started", _clock()), 2),
            "error": message,
            "assertions": [],
            "log": _log_since(_RUN.get("log_offset", 0)),
        })
        _RUN["current_recorded"] = True
    _finish(False, error=message)


def _begin_beat():
    selected = _RUN.get("selected", [])
    index = _RUN.get("index", 0)
    if index >= len(selected):
        _finish(True)
        return
    _RUN["current"] = selected[index]
    _RUN["current_recorded"] = False
    _RUN["beat_started"] = _clock()
    _RUN["log_offset"] = 0
    _RUN["last_poll"] = 0.0
    _set_phase("stop_pie")


# ---------------------------------------------------------------------------
# Phases
# ---------------------------------------------------------------------------

def _phase_precheck(now):
    subsys = _subsys()
    if subsys is None:
        _fail_current("LevelEditorSubsystem missing")
        return
    if subsys.is_in_play_in_editor():
        subsys.editor_request_end_play()
        _set_phase("wait_stop_pre")
        return

    world = _editor_world()
    if world is None:
        # The Editor just launched and the default map may still be loading.
        if now - _RUN.get("phase_started", now) < 60.0:
            return
        _fail_current("no editor world after 60s")
        return
    if LEVEL_TOKEN in world.get_path_name():
        _begin_beat()
        return

    if not _RUN.get("load_level", True):
        _fail_current("editor is on %s; open L_SizeTest" % world.get_path_name())
        return
    try:
        loaded = subsys.load_level(LEVEL_PATH)
    except Exception as exc:
        _fail_current("load_level failed: " + str(exc))
        return
    if loaded is False:
        _fail_current("load_level returned false for " + LEVEL_PATH)
        return
    _set_phase("load_level")


def _phase_wait_stop_pre(now):
    if not _subsys().is_in_play_in_editor():
        _set_phase("precheck")


def _phase_load_level(now):
    world = _editor_world()
    if world is not None and LEVEL_TOKEN in world.get_path_name():
        _begin_beat()


def _phase_stop_pie(now):
    subsys = _subsys()
    if subsys.is_in_play_in_editor():
        subsys.editor_request_end_play()
        _set_phase("wait_stop_pie")
    else:
        _set_phase("start_pie")


def _phase_wait_stop_pie(now):
    if not _subsys().is_in_play_in_editor():
        _set_phase("start_pie")


def _phase_start_pie(now):
    subsys = _subsys()
    if subsys.is_in_play_in_editor():
        subsys.editor_request_end_play()
        _set_phase("wait_stop_pie")
        return
    subsys.editor_request_begin_play()
    _set_phase("wait_pie")


def _phase_wait_pie(now):
    if _subsys().is_in_play_in_editor() and _pie_world() is not None:
        _set_phase("wait_pawn")


def _phase_wait_pawn(now):
    pawn = _pawn()
    if pawn is not None and getattr(pawn, "get_playtest_state_json", None) is not None:
        _set_phase("send")


def _phase_send(now):
    world = _pie_world()
    pawn = _pawn()
    if world is None or pawn is None:
        _fail_current("PIE world or pawn missing before the command")
        return
    current = _RUN.get("current") or {}
    stop = current.get("stop", "")
    command = "hw.Playtest.FastForward" + ((" " + stop) if stop else "")
    _RUN["log_offset"] = _log_size()
    try:
        unreal.SystemLibrary.execute_console_command(world, command)
    except Exception as exc:
        _fail_current("console command failed: " + str(exc))
        return
    _RUN["command_sent_at"] = now
    _RUN["last_poll"] = 0.0
    unreal.log("quest_tests: %s -> %s" % (current.get("id"), command))
    _set_phase("wait_ready")


def _phase_wait_ready(now):
    if now - _RUN.get("last_poll", 0.0) < POLL_S:
        return
    _RUN["last_poll"] = now

    tail = _log_since(_RUN.get("log_offset", 0))
    for line in reversed(tail):
        lowered = line.lower()
        if any(marker in lowered for marker in FAILURE_MARKERS):
            _fail_current("fast-forward: " + line.strip())
            return

    pawn = _pawn()
    state, error = _state(pawn)
    current = _RUN.get("current") or {}
    expected = current.get("id")
    sent_at = _RUN.get("command_sent_at", now)

    if state is None:
        if error and "missing" in error.lower() and now - sent_at > 5.0:
            _fail_current(error, inconclusive=True)
        return

    ready_for = state.get("ready_for", "")
    if ready_for == expected:
        _RUN["ready_state"] = state
        _set_phase("snapshot")
        return
    if ready_for:
        _fail_current("ready for %s, expected %s" % (ready_for, expected))
        return

    step = state.get("fast_forward_step", -1)
    if step == 0 and now - sent_at > 5.0:
        detail = tail[-1].strip() if tail else "no playtest_ff line"
        _fail_current("fast-forward stopped before ready: " + detail)


def _phase_snapshot(now):
    world = _pie_world()
    pawn = _pawn()
    if world is None or pawn is None:
        _fail_current("PIE world or pawn missing at snapshot")
        return
    try:
        snapshot = _build_snapshot(world, pawn)
    except Exception as exc:
        message = str(exc)
        _fail_current(
            "snapshot failed: " + message,
            inconclusive=("GetPlaytestStateJson" in message or "state missing" in message.lower()),
        )
        return

    current = _RUN.get("current") or {}
    result = _evaluate(current, snapshot)
    _RUN["results"].append(result)
    _RUN["current_recorded"] = True
    unreal.log("quest_tests: %s %s" % (result.get("id"), result.get("status")))
    _set_phase("end_pie")


def _phase_end_pie(now):
    subsys = _subsys()
    if subsys.is_in_play_in_editor():
        subsys.editor_request_end_play()
        _set_phase("wait_end_pie")
    else:
        _RUN["index"] = _RUN.get("index", 0) + 1
        _RUN["settle_until"] = now + SETTLE_S
        _set_phase("settle")


def _phase_wait_end_pie(now):
    if not _subsys().is_in_play_in_editor():
        _RUN["index"] = _RUN.get("index", 0) + 1
        _RUN["settle_until"] = now + SETTLE_S
        _set_phase("settle")


def _phase_settle(now):
    if now >= _RUN.get("settle_until", 0.0):
        _begin_beat()


_PHASES = {
    "precheck": _phase_precheck,
    "wait_stop_pre": _phase_wait_stop_pre,
    "load_level": _phase_load_level,
    "stop_pie": _phase_stop_pie,
    "wait_stop_pie": _phase_wait_stop_pie,
    "start_pie": _phase_start_pie,
    "wait_pie": _phase_wait_pie,
    "wait_pawn": _phase_wait_pawn,
    "send": _phase_send,
    "wait_ready": _phase_wait_ready,
    "snapshot": _phase_snapshot,
    "end_pie": _phase_end_pie,
    "wait_end_pie": _phase_wait_end_pie,
    "settle": _phase_settle,
}


def _tick(delta_seconds):
    if not _RUN.get("active"):
        return
    try:
        raw = time.time()
        phase = _RUN.get("phase", "idle")
        last = _RUN.get("last_tick_at")
        if last is not None:
            gap = raw - last
            if gap > STALL_S:
                _RUN["clock_offset"] = _RUN.get("clock_offset", 0.0) + gap
                current = _RUN.get("current") or {}
                _RUN["stalls"].append({
                    "at": _now_iso(),
                    "phase": phase,
                    "beat": current.get("id"),
                    "seconds": round(gap, 1),
                })
                unreal.log("quest_tests: WARNING Editor stalled %.1fs; test deadlines extended" % gap)
        _RUN["last_tick_at"] = raw
        now = raw - _RUN.get("clock_offset", 0.0)
        _write_status()

        external = _mcp_since(_RUN.get("mcp_offset", 0))
        if external:
            _RUN["mcp_offset"] = _log_size()
            _fail_current(
                "external Editor command during sweep: " + external[-1][-180:],
                inconclusive=True,
            )
            return

        limit = PHASE_LIMIT.get(phase)
        if limit and now - _RUN.get("phase_started", now) > limit:
            _fail_current("timeout in %s after %.0fs" % (phase, limit))
            return
        handler = _PHASES.get(phase)
        if handler is not None:
            handler(now)
    except Exception:
        _RUN["error"] = traceback.format_exc()
        _fail_current("exception: " + _RUN["error"])

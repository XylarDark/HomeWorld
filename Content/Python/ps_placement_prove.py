# ps_placement_prove.py
# PS-C: Automated placement metrics + viewport still capture on L_VS_MVP_Markers.
# Run in Unreal Editor or MCP: execute_python_script("ps_placement_prove.py").
# Chain (DESKTOP): markers → dress → pa_d → arrange_ps_homestead.py → this script.
# Harness P3 exempt: PS track prove (Arrange gate via ps_arrange_gate.json / arrange_ps_homestead).
# Writes Saved/ps_placement_metrics.json, Saved/ps_stills/*, Saved/ps_c_prove_gate.json.
# Stills: slate pre-tick state machine + pump-until-done (≤300s, no sleep) so MCP prove
# always finalizes gate and PNGs; module-level callback + keep_python_script_alive.

from __future__ import annotations

import importlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

try:
    import unreal
except ImportError:
    print("ps_placement_prove: Run inside Unreal Editor.")
    sys.exit(1)

import pa_e_shotlist_common as common

importlib.reload(common)

try:
    import arrange_ps_homestead as ps_arrange

    importlib.reload(ps_arrange)
except ImportError:
    ps_arrange = None  # type: ignore

LOG_PREFIX = "PS Prove:"

OUTCOME_PASS = common.CAPTURE_OUTCOME_PASS
OUTCOME_SOFT = common.CAPTURE_OUTCOME_SOFT_FAIL
OUTCOME_CLOSED = common.CAPTURE_OUTCOME_CLOSED_FAIL

THRESHOLD_GROUND_Z_DELTA = 8.0
THRESHOLD_FLOAT_GAP_KIT = 4.0
THRESHOLD_FLOAT_GAP_CLIFF = 12.0
THRESHOLD_DRESS_MARGIN = 50.0
THRESHOLD_PAIR_OVERLAP = 2.0

CORE_DRESS_SUBSTRINGS = (
    "IslandTop",
    "SM_Cabin",
    "Lookout_Pad",
    "Shrine_Homestead",
    "LandingCircle",
    "Glider_Perch",
    "Garden_Fence",
    "Planter",
    "PathStone",
    "Planet_GroundPlate",
)

CLIFF_LABEL_MARKERS = ("Cliff",)

STILL_CAM_LABELS = (
    "PS_N_HighIso",
    "PS_E_HighIso",
    "PS_Cliff_Underside",
    "PS_Path_Corridor",
    "PS_Garden_Close",
    "CAM_Hero",
    "CAM_CabinClose",
)

STILL_RES_X, STILL_RES_Y = 1600, 900
PS_C_WAIT_FILE_SEC = 42.0
PS_C_INTER_SHOT_SETTLE_FRAMES = 12
PS_C_DRIVE_TIMEOUT_SEC = 300.0
PS_C_WAIT_RETRY_TICKS = 10
PS_C_STABLE_POLLS_REQUIRED = 2
PS_C_SLATE_MECHANISM = "register_slate_pre_tick_callback"
PS_C_DRIVE_MECHANISM = "slate_callback_plus_pump_until_done"
TRACE_TOP_OFFSET_UU = 120.0
TRACE_DEPTH_UU = 12000.0
# PS-C baseline: metric over-threshold → soft_fail (Lead tunes before closed_fail).
METRICS_CAP_OUTCOME_AT_SOFT = True
ISLAND_TOP_LABEL = "DRESS_SM_IslandTop"
INTENTIONAL_OVERLAP_SUBSTRINGS = (
    ("Planter", "Cabin"),
    ("Planter", "Foundation"),
    ("Fence", "Cabin"),
    ("PathStone", "IslandTop"),
)
# Same-act MRQ PNG copy only when mtime >= capture_since (no 24h stale reuse).
MRQ_SHOT_STILL_FALLBACK = {
    "CAM_Hero": ("shot1", "Shot1_lookout"),
    "CAM_CabinClose": ("shot2", "Shot2_cabin"),
}


def _log(msg: str, data: Optional[dict[str, Any]] = None) -> None:
    line = f"{LOG_PREFIX} {msg}"
    if data:
        line += " " + json.dumps(data, default=str)
    unreal.log(line)


def _project_saved_path(*parts: str) -> str:
    return common.abs_path(os.path.join(common.project_dir(), "Saved", *parts))


def _all_level_actors() -> list:
    return [a for a in unreal.EditorLevelLibrary.get_all_level_actors() if a]


def _find_actor_label(label: str):
    for a in _all_level_actors():
        if common.actor_label(a) == label:
            return a
    return None


def _actor_aabb(actor) -> Optional[dict[str, list[float]]]:
    try:
        origin, extent = actor.get_actor_bounds(False)
    except Exception:
        return None
    mn = [origin.x - extent.x, origin.y - extent.y, origin.z - extent.z]
    mx = [origin.x + extent.x, origin.y + extent.y, origin.z + extent.z]
    return {
        "origin": [origin.x, origin.y, origin.z],
        "extent": [extent.x, extent.y, extent.z],
        "min": mn,
        "max": mx,
        "bottom_z": origin.z - extent.z,
    }


def _outcome_from_value(
    value: float, threshold: float, *, higher_is_worse: bool = True
) -> str:
    if higher_is_worse:
        if value <= threshold:
            return OUTCOME_PASS
        if METRICS_CAP_OUTCOME_AT_SOFT:
            return OUTCOME_SOFT
        if value <= threshold * 2.0:
            return OUTCOME_SOFT
        return OUTCOME_CLOSED
    if value >= threshold:
        return OUTCOME_PASS
    return OUTCOME_SOFT


def _is_island_top_label(label: str) -> bool:
    return label == ISLAND_TOP_LABEL or label.startswith("DRESS_SM_IslandTop")


def _skip_ground_metrics(label: str) -> bool:
    if _is_island_top_label(label):
        return True
    return _is_cliff_actor(label)


def _intentional_overlap_pair(a: str, b: str) -> bool:
    for needle_a, needle_b in INTENTIONAL_OVERLAP_SUBSTRINGS:
        if (needle_a in a and needle_b in b) or (needle_a in b and needle_b in a):
            return True
    return False


def _hit_actor_label(hit) -> Optional[str]:
    if hit is None:
        return None
    actor = getattr(hit, "get_actor", None)
    if callable(actor):
        try:
            act = hit.get_actor()
            if act:
                return common.actor_label(act)
        except Exception:
            pass
    act = getattr(hit, "actor", None)
    if act:
        try:
            return common.actor_label(act)
        except Exception:
            return None
    return None


def _load_json(path: str) -> Optional[dict[str, Any]]:
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _dress_bounds_from_file() -> tuple[Optional[dict[str, Any]], str]:
    path = _project_saved_path("ps_dress_bounds.json")
    data = _load_json(path)
    if not data:
        return None, path
    aabb = data.get("dress_aabb") or {}
    center = aabb.get("center")
    extent = aabb.get("extent")
    minmax = data.get("dress_aabb_minmax") or {}
    if center and extent:
        cx, cy, cz = center[0], center[1], center[2]
        ex, ey, ez = extent[0], extent[1], extent[2]
        return {
            "centroid": [cx, cy, cz],
            "extent": [ex, ey, ez],
            "min": [cx - ex, cy - ey, cz - ez],
            "max": [cx + ex, cy + ey, cz + ez],
            "margin_uu": float(data.get("margin_uu") or THRESHOLD_DRESS_MARGIN),
            "source_path": path,
        }, path
    if minmax.get("min") and minmax.get("max"):
        mn, mx = minmax["min"], minmax["max"]
        cx = (mn[0] + mx[0]) * 0.5
        cy = (mn[1] + mx[1]) * 0.5
        cz = (mn[2] + mx[2]) * 0.5
        return {
            "centroid": [cx, cy, cz],
            "extent": [(mx[0] - mn[0]) * 0.5, (mx[1] - mn[1]) * 0.5, (mx[2] - mn[2]) * 0.5],
            "min": mn,
            "max": mx,
            "margin_uu": float(data.get("margin_uu") or THRESHOLD_DRESS_MARGIN),
            "source_path": path,
        }, path
    return None, path


def _ensure_arrange_gate() -> tuple[dict[str, Any], list[str]]:
    """Return arrange gate dict; run Arrange if missing or not ready."""
    blocked: list[str] = []
    gate_path = _project_saved_path("ps_arrange_gate.json")
    gate = _load_json(gate_path)
    if gate and gate.get("ready_for_ps_c"):
        gate["read_from"] = gate_path
        return gate, blocked

    if gate and not gate.get("ready_for_ps_c"):
        blocked.append("ps_arrange_gate_not_ready")
    else:
        blocked.append("ps_arrange_gate_missing")

    if ps_arrange is None:
        blocked.append("arrange_ps_homestead_import_failed")
        return gate or {}, blocked

    _log("running arrange_ps_homestead (gate missing or not ready)")
    try:
        gate = ps_arrange.arrange_ps_homestead()
    except Exception as e:
        blocked.append(f"arrange_failed:{e}")
        return gate or {}, blocked

    if not gate.get("ready_for_ps_c"):
        blocked.append("arrange_still_not_ready_for_ps_c")
    return gate, blocked


def _sample_metric_actors() -> tuple[list, dict[str, Any]]:
    """All PA_D_* plus core DRESS anchors (not full 90+ DRESS sweep)."""
    meta: dict[str, Any] = {"policy": "all_PA_D_plus_core_DRESS_substrings"}
    pa_d: list = []
    dress_core: list = []
    for a in _all_level_actors():
        label = common.actor_label(a)
        if label.startswith("PA_D_"):
            pa_d.append(a)
        elif label.startswith(common.DRESS_LABEL_PREFIX):
            if any(sub in label for sub in CORE_DRESS_SUBSTRINGS):
                dress_core.append(a)
    actors = pa_d + dress_core
    meta["pa_d_count"] = len(pa_d)
    meta["dress_core_count"] = len(dress_core)
    meta["total_sampled"] = len(actors)
    return actors, meta


def _is_cliff_actor(label: str) -> bool:
    return label.startswith("PA_D_") and any(m in label for m in CLIFF_LABEL_MARKERS)


def _parse_trace_hit(hit, method: str) -> tuple[Optional[float], str, Optional[str]]:
    if hit is None:
        return None, f"{method}:no_hit", None
    try:
        if hasattr(hit, "blocking_hit") and not hit.blocking_hit:
            return None, f"{method}:non_blocking", _hit_actor_label(hit)
        loc = hit.location
        return float(loc.z), f"{method}:trace_hit", _hit_actor_label(hit)
    except Exception:
        return None, f"{method}:hit_parse_failed", None


def _line_trace_ground_z(
    world,
    x: float,
    y: float,
    z_top: float,
    z_bottom: float,
    *,
    ignore_actors: Optional[list] = None,
) -> tuple[Optional[float], str, Optional[str]]:
    """Trace downward at XY; never fall back to island max-Z proxy."""
    ignore_actors = ignore_actors or []
    start = unreal.Vector(x, y, z_top + TRACE_TOP_OFFSET_UU)
    end = unreal.Vector(x, y, z_bottom - TRACE_DEPTH_UU)
    draw = unreal.DrawDebugTrace.NONE

    object_types: list = []
    for name in ("WORLD_STATIC", "OBJECT_TYPE_QUERY1", "OBJECT_TYPE_QUERY2"):
        q = getattr(unreal.ObjectTypeQuery, name, None)
        if q is not None and q not in object_types:
            object_types.append(q)

    if object_types:
        for variant in ("short", "long"):
            try:
                if variant == "short":
                    hit = unreal.SystemLibrary.line_trace_single_for_objects(
                        world,
                        start,
                        end,
                        object_types,
                        False,
                        ignore_actors,
                        draw,
                        True,
                    )
                else:
                    hit = unreal.SystemLibrary.line_trace_single_for_objects(
                        world,
                        start,
                        end,
                        object_types,
                        False,
                        ignore_actors,
                        draw,
                        True,
                        unreal.LinearColor(0, 0, 0, 0),
                        unreal.LinearColor(0, 0, 0, 0),
                        0.0,
                    )
                z, src, al = _parse_trace_hit(hit, "line_trace_single_for_objects")
                if z is not None:
                    return z, src, al
            except TypeError:
                continue
            except Exception as e:
                return None, f"line_trace_for_objects_error:{e}", None

    for profile in ("BlockAll", "Visibility", "WorldStatic"):
        fn = getattr(unreal.SystemLibrary, "line_trace_single_by_profile", None)
        if not callable(fn):
            break
        try:
            hit = fn(
                world,
                start,
                end,
                profile,
                False,
                ignore_actors,
                draw,
                True,
            )
            z, src, al = _parse_trace_hit(hit, f"line_trace_by_profile:{profile}")
            if z is not None:
                return z, src, al
        except TypeError:
            try:
                hit = fn(
                    world,
                    start,
                    end,
                    profile,
                    False,
                    ignore_actors,
                    draw,
                    True,
                    unreal.LinearColor(0, 0, 0, 0),
                    unreal.LinearColor(0, 0, 0, 0),
                    0.0,
                )
                z, src, al = _parse_trace_hit(hit, f"line_trace_by_profile:{profile}")
                if z is not None:
                    return z, src, al
            except Exception:
                continue
        except Exception:
            continue

    for query_name in (
        "TRACE_TYPE_QUERY1",
        "TRACE_TYPE_QUERY2",
        "TRACE_TYPE_QUERY3",
        "VISIBILITY",
        "WORLD_STATIC",
    ):
        channel = getattr(unreal.TraceTypeQuery, query_name, None)
        if channel is None:
            continue
        try:
            hit = unreal.SystemLibrary.line_trace_single(
                world,
                start,
                end,
                channel,
                False,
                ignore_actors,
                draw,
                True,
            )
            z, src, al = _parse_trace_hit(hit, f"line_trace_single:{query_name}")
            if z is not None:
                return z, src, al
        except TypeError:
            try:
                hit = unreal.SystemLibrary.line_trace_single(
                    world,
                    start,
                    end,
                    channel,
                    False,
                    ignore_actors,
                    draw,
                    True,
                    unreal.LinearColor(0, 0, 0, 0),
                    unreal.LinearColor(0, 0, 0, 0),
                    0.0,
                )
                z, src, al = _parse_trace_hit(hit, f"line_trace_single:{query_name}")
                if z is not None:
                    return z, src, al
            except Exception:
                continue
        except Exception:
            continue

    return None, "no_ground_trace_hit", None


def _aabb_inside_dress(aabb: dict[str, list[float]], dress: dict[str, Any]) -> tuple[bool, float]:
    margin = float(dress.get("margin_uu") or THRESHOLD_DRESS_MARGIN)
    dmin = dress["min"]
    dmax = dress["max"]
    allowed_min = [dmin[i] - margin for i in range(3)]
    allowed_max = [dmax[i] + margin for i in range(3)]
    worst = 0.0
    for i in range(3):
        if aabb["min"][i] < allowed_min[i]:
            worst = max(worst, allowed_min[i] - aabb["min"][i])
        if aabb["max"][i] > allowed_max[i]:
            worst = max(worst, aabb["max"][i] - allowed_max[i])
    return worst <= 0.0, worst


def _pair_overlap_max_uu(a: dict[str, list[float]], b: dict[str, list[float]]) -> float:
    overlap = 0.0
    for i in range(3):
        depth = min(a["max"][i], b["max"][i]) - max(a["min"][i], b["min"][i])
        if depth <= 0:
            return 0.0
        overlap = max(overlap, depth)
    return overlap


def _aggregate_outcome(outcomes: list[str]) -> str:
    if OUTCOME_CLOSED in outcomes:
        return OUTCOME_CLOSED
    if OUTCOME_SOFT in outcomes:
        return OUTCOME_SOFT
    return OUTCOME_PASS if outcomes else OUTCOME_SOFT


def _compute_metrics(
    *,
    world,
    dress_bounds: dict[str, Any],
    island_actor,
) -> dict[str, Any]:
    actors, sample_meta = _sample_metric_actors()
    actor_rows: list[dict[str, Any]] = []
    pair_flags: list[dict[str, Any]] = []

    for actor in actors:
        label = common.actor_label(actor)
        aabb = _actor_aabb(actor)
        row: dict[str, Any] = {"label": label, "metrics": {}}
        if not aabb:
            row["actor_outcome"] = OUTCOME_SOFT
            row["note"] = "bounds_unavailable"
            actor_rows.append(row)
            continue

        outcomes: list[str] = []
        cx, cy = aabb["origin"][0], aabb["origin"][1]
        bottom_z = aabb["bottom_z"]
        z_top = aabb["max"][2]
        z_bottom = aabb["min"][2]

        if _skip_ground_metrics(label):
            skip_note = (
                "skipped_island_top_self"
                if _is_island_top_label(label)
                else "skipped_cliff_ground_metrics"
            )
            row["metrics"]["ground_z_delta_uu"] = {
                "value": None,
                "outcome": OUTCOME_PASS,
                "note": skip_note,
            }
            row["metrics"]["float_gap_uu"] = {
                "value": None,
                "outcome": OUTCOME_PASS,
                "note": skip_note,
            }
        else:
            ground_z, ground_src, hit_label = _line_trace_ground_z(
                world,
                cx,
                cy,
                z_top,
                z_bottom,
                ignore_actors=[actor],
            )
            if ground_z is None:
                row["metrics"]["ground_z_delta_uu"] = {
                    "value": None,
                    "outcome": OUTCOME_SOFT,
                    "note": ground_src,
                }
                row["metrics"]["float_gap_uu"] = {
                    "value": None,
                    "outcome": OUTCOME_SOFT,
                    "note": "no_ground",
                }
                outcomes.append(OUTCOME_SOFT)
            else:
                delta = abs(bottom_z - ground_z)
                gz_out = _outcome_from_value(delta, THRESHOLD_GROUND_Z_DELTA)
                row["metrics"]["ground_z_delta_uu"] = {
                    "value": round(delta, 3),
                    "threshold": THRESHOLD_GROUND_Z_DELTA,
                    "ground_source": ground_src,
                    "hit_actor_label": hit_label,
                    "outcome": gz_out,
                }
                outcomes.append(gz_out)

                gap = max(0.0, bottom_z - ground_z)
                gap_thresh = THRESHOLD_FLOAT_GAP_KIT
                gap_out = _outcome_from_value(gap, gap_thresh)
                row["metrics"]["float_gap_uu"] = {
                    "value": round(gap, 3),
                    "threshold": gap_thresh,
                    "hit_actor_label": hit_label,
                    "outcome": gap_out,
                }
                outcomes.append(gap_out)

        inside, exit_uu = _aabb_inside_dress(aabb, dress_bounds)
        dress_out = OUTCOME_PASS if inside else _outcome_from_value(exit_uu, THRESHOLD_DRESS_MARGIN)
        row["metrics"]["dress_aabb_inside"] = {
            "inside": inside,
            "worst_exit_uu": round(exit_uu, 3),
            "margin_uu": dress_bounds.get("margin_uu", THRESHOLD_DRESS_MARGIN),
            "outcome": dress_out,
        }
        outcomes.append(dress_out)

        row["metrics"]["anchor_height_delta_uu"] = {
            "value": None,
            "outcome": OUTCOME_PASS,
            "note": "skipped_no_sidecar_table",
        }

        row["metrics"]["facing_dot_look_at"] = {
            "value": None,
            "outcome": OUTCOME_PASS,
            "note": "skipped_optional",
        }

        row["actor_outcome"] = _aggregate_outcome(outcomes)
        actor_rows.append(row)

    labeled_aabb: list[tuple[str, dict[str, list[float]]]] = []
    for actor in actors:
        label = common.actor_label(actor)
        aabb = _actor_aabb(actor)
        if aabb:
            labeled_aabb.append((label, aabb))

    for i in range(len(labeled_aabb)):
        li, la = labeled_aabb[i]
        for j in range(i + 1, len(labeled_aabb)):
            lj, lb = labeled_aabb[j]
            if li.startswith("PA_D_") or lj.startswith("PA_D_"):
                if _intentional_overlap_pair(li, lj):
                    continue
                ov = _pair_overlap_max_uu(la, lb)
                if ov > THRESHOLD_PAIR_OVERLAP:
                    po_out = OUTCOME_SOFT if METRICS_CAP_OUTCOME_AT_SOFT else _outcome_from_value(
                        ov, THRESHOLD_PAIR_OVERLAP
                    )
                    pair_flags.append(
                        {
                            "a": li,
                            "b": lj,
                            "overlap_uu": round(ov, 3),
                            "threshold": THRESHOLD_PAIR_OVERLAP,
                            "outcome": po_out,
                        }
                    )

    pair_outcome = OUTCOME_PASS
    if pair_flags:
        pair_outcome = _aggregate_outcome([p["outcome"] for p in pair_flags])

    actor_outcomes = [r.get("actor_outcome", OUTCOME_SOFT) for r in actor_rows]
    placement_outcome = _aggregate_outcome(actor_outcomes + [pair_outcome])

    return {
        "version": 2,
        "track": "PS-C",
        "level_path": common.LEVEL_PATH,
        "metrics_cap_outcome_at_soft": METRICS_CAP_OUTCOME_AT_SOFT,
        "ground_trace_policy": "multi_channel_line_trace_no_island_max_z_proxy",
        "sample_policy": sample_meta,
        "thresholds": {
            "ground_z_delta_uu": THRESHOLD_GROUND_Z_DELTA,
            "float_gap_uu_kit": THRESHOLD_FLOAT_GAP_KIT,
            "float_gap_uu_cliff": THRESHOLD_FLOAT_GAP_CLIFF,
            "dress_aabb_inside_margin_uu": THRESHOLD_DRESS_MARGIN,
            "pair_overlap_uu": THRESHOLD_PAIR_OVERLAP,
        },
        "dress_bounds_source": dress_bounds.get("source_path"),
        "island_top_reference_label": common.actor_label(island_actor) if island_actor else None,
        "actors": actor_rows,
        "pair_overlap_flags": pair_flags,
        "pair_overlap_outcome": pair_outcome,
        "placement_outcome": placement_outcome,
        "generated_at_iso": datetime.now(timezone.utc).isoformat(),
        "note": (
            "Metric outcomes gate placement physics; framing/mood vs benchmarks is PS-D Lead eyeball. "
            "First DESKTOP run may soft_fail thresholds — tune after prove."
        ),
    }


def _focus_ps_c_viewport() -> None:
    """Bring level viewport to foreground before HighResShot (shotlist pattern)."""
    try:
        les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        if les:
            for attr in ("editor_set_level_viewport_realtime", "set_level_viewport_realtime"):
                if hasattr(les, attr):
                    getattr(les, attr)(True)
            for attr in ("set_focus_to_level_viewport", "focus_level_viewport"):
                if hasattr(les, attr):
                    getattr(les, attr)()
                    break
    except Exception:
        pass
    try:
        unreal.SystemLibrary.execute_console_command(None, "FOCUSVIEWPORT")
    except Exception:
        pass


def _pilot_camera(cam) -> None:
    try:
        unreal.EditorLevelLibrary.set_level_viewport_camera_info(
            cam.get_actor_location(),
            cam.get_actor_rotation(),
        )
    except Exception:
        pass
    try:
        unreal.EditorLevelLibrary.pilot_level_actor(cam)
    except Exception:
        pass


def _resolve_still_path(stills_dir: str, cam_label: str) -> str:
    safe = cam_label.replace("/", "_")
    return os.path.join(stills_dir, f"{safe}.png")


def _mtime_at_least(path: str, since: float) -> bool:
    try:
        return os.path.getmtime(path) >= since - 0.05
    except OSError:
        return False


def _ps_c_engine_search_roots() -> list[str]:
    """Engine Win64 / Saved search roots (PA-E shotlist pattern)."""
    roots: list[str] = []
    seen: set[str] = set()
    proj = common.abs_path(common.project_dir())

    def add(p: str) -> None:
        p = common.abs_path(p)
        if p not in seen and os.path.isdir(p):
            seen.add(p)
            roots.append(p)

    screens = os.path.join(proj, "Saved", "Screenshots")
    add(screens)
    for sub in ("WindowsEditor", "Windows", "PA_E"):
        add(os.path.join(screens, sub))
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
    add(os.getcwd())
    add(os.path.join(os.getcwd(), "PA_E"))
    return roots


def _purge_ps_c_still_png(dest_abs: str) -> dict[str, Any]:
    """Remove prior PNGs so wait/finalize cannot latch stale CAM/PS frames."""
    dest_abs = common.abs_path(dest_abs)
    basename = os.path.basename(dest_abs)
    candidates: set[str] = {dest_abs}
    for root in _ps_c_engine_search_roots():
        candidates.add(common.abs_path(os.path.join(root, basename)))
        candidates.add(common.abs_path(os.path.join(root, "PA_E", basename)))
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


def _find_fresh_ps_still_path(dest_abs: str, since_mtime: float) -> Optional[str]:
    """Newest absolute dest or engine CWD basename with mtime >= capture_since."""
    import shutil

    dest_abs = common.abs_path(dest_abs)
    basename = os.path.basename(dest_abs)
    if os.path.isfile(dest_abs) and _mtime_at_least(dest_abs, since_mtime):
        return dest_abs
    best: Optional[str] = None
    best_m = since_mtime
    for root in _ps_c_engine_search_roots():
        candidate = os.path.join(root, basename)
        if not os.path.isfile(candidate):
            continue
        try:
            mtime = os.path.getmtime(candidate)
        except OSError:
            continue
        if mtime >= since_mtime - 0.05 and mtime >= best_m:
            best = candidate
            best_m = mtime
    if best:
        try:
            os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
            shutil.copy2(best, dest_abs)
        except OSError:
            return best if _mtime_at_least(best, since_mtime) else None
        if os.path.isfile(dest_abs) and _mtime_at_least(dest_abs, since_mtime):
            return dest_abs
        return best if _mtime_at_least(best, since_mtime) else None
    return None


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


def _load_capture_viewport():
    import capture_viewport as cv

    importlib.reload(cv)
    return cv


class _PsCStillsPhase(str, Enum):
    IDLE = "idle"
    POSED = "posed"
    PREPARING = "preparing"
    CAPTURE_PENDING = "capture_pending"
    WAITING_FILE = "waiting_file"
    INTER_SHOT_SETTLE = "inter_shot_settle"
    WRITE_MANIFEST = "write_manifest"
    DISARM = "disarm"
    DONE = "done"


class _PsCStillsOrchestrator:
    """Seven PS stills — one HighResShot/AL invoke in flight; Slate pre-tick wait."""

    def __init__(
        self,
        *,
        world,
        stills_dir: str,
        gate_context: dict[str, Any],
    ) -> None:
        self.world = world
        self.stills_dir = stills_dir
        self.gate_context = gate_context
        self.phase = _PsCStillsPhase.IDLE
        self.shot_index = 0
        self.entries: list[dict[str, Any]] = []
        self._tick_handle: Any = None
        self._settle_frames_left = 0
        self._cam_label = ""
        self._filepath = ""
        self._cam: Any = None
        self._since = 0.0
        self._wait_deadline = 0.0
        self._methods: list[str] = []
        self._capture_result: dict[str, Any] = {}
        self._task: Any = None
        self._stable: Any = None
        self._driver_error: Optional[str] = None
        self._cv: Any = None
        self._in_tick = False
        self._manifest_path = ""
        self._drive_ticks = 0
        self._registered_tick_callable: Any = None
        self._drive_deadline = 0.0
        self._console_cmd_index = 0
        self._console_cmd_total = 0
        self._al_invoked = False
        self._ticks_in_wait = 0
        self._act_started_at = 0.0

    def start(self) -> bool:
        register = getattr(unreal, "register_slate_pre_tick_callback", None)
        if not callable(register):
            self._driver_error = "register_slate_pre_tick_callback unavailable"
            return False
        self._cv = _load_capture_viewport()
        self._stable = self._cv._StableSizeTracker()
        self._registered_tick_callable = _ps_c_slate_pre_tick_dispatcher
        _PS_C_SLATE_CALLBACK_REFS.append(self._registered_tick_callable)
        _PS_C_DRIVER_ROOTS.append(self)
        try:
            self._tick_handle = register(self._registered_tick_callable)
        except Exception as e:
            self._driver_error = str(e)
            return False
        self.phase = _PsCStillsPhase.POSED
        self.shot_index = 0
        self._act_started_at = time.time()
        self._drive_deadline = self._act_started_at + PS_C_DRIVE_TIMEOUT_SEC
        _log(
            "stills slate driver armed",
            {
                "mechanism": PS_C_SLATE_MECHANISM,
                "drive_mechanism": PS_C_DRIVE_MECHANISM,
                "wait_file_sec": PS_C_WAIT_FILE_SEC,
                "drive_timeout_sec": PS_C_DRIVE_TIMEOUT_SEC,
            },
        )
        return True

    def _unregister_tick(self) -> None:
        if self._tick_handle is None:
            return
        unregister = getattr(unreal, "unregister_slate_pre_tick_callback", None)
        if callable(unregister):
            try:
                unregister(self._tick_handle)
            except Exception:
                pass
        self._tick_handle = None

    def _on_slate_pre_tick(self, _delta: float) -> None:
        if self._in_tick:
            return
        self._in_tick = True
        try:
            self._tick()
            self._drive_ticks += 1
        except Exception as e:
            _log("stills orchestrator tick error", {"error": str(e), "phase": self.phase.value})
            self.phase = _PsCStillsPhase.WRITE_MANIFEST
            self._driver_error = self._driver_error or str(e)
        finally:
            self._in_tick = False

    def _tick(self) -> None:
        if self.phase == _PsCStillsPhase.POSED:
            self._begin_shot_prepare()
            if self.phase == _PsCStillsPhase.CAPTURE_PENDING:
                self._invoke_capture_once()
        elif self.phase == _PsCStillsPhase.PREPARING:
            pass
        elif self.phase == _PsCStillsPhase.CAPTURE_PENDING:
            self._invoke_capture_once()
        elif self.phase == _PsCStillsPhase.WAITING_FILE:
            self._poll_capture_wait()
        elif self.phase == _PsCStillsPhase.INTER_SHOT_SETTLE:
            self._settle_frames_left -= 1
            if self._settle_frames_left <= 0:
                self.phase = _PsCStillsPhase.POSED
        elif self.phase == _PsCStillsPhase.WRITE_MANIFEST:
            self._finish_all()
        elif self.phase == _PsCStillsPhase.DISARM:
            self._disarm_keep_alive()

    def _begin_shot_prepare(self) -> None:
        if self.phase != _PsCStillsPhase.POSED:
            return
        self.phase = _PsCStillsPhase.PREPARING
        if self.shot_index >= len(STILL_CAM_LABELS):
            self.phase = _PsCStillsPhase.WRITE_MANIFEST
            return
        self._cam_label = STILL_CAM_LABELS[self.shot_index]
        self._filepath = _resolve_still_path(self.stills_dir, self._cam_label)
        self._cam = _find_actor_label(self._cam_label)
        self._methods = []
        self._capture_result = {}
        self._task = None
        if not self._cam:
            self.entries.append(
                {
                    "camera_label": self._cam_label,
                    "path": self._filepath,
                    "capture_outcome": OUTCOME_CLOSED,
                    "error": "camera_missing",
                    "file_exists": False,
                }
            )
            self.shot_index += 1
            self.phase = _PsCStillsPhase.POSED
            return
        os.makedirs(os.path.dirname(self._filepath), exist_ok=True)
        purge = _purge_ps_c_still_png(self._filepath)
        self._methods.append(f"purge_before_capture:{len(purge.get('removed', []))}")
        _pilot_camera(self._cam)
        self._cv._finish_loading_before_screenshot()
        lit = self._cv._set_lit_view_mode()
        if lit:
            self._methods.append(lit)
        self._cv._settle_pump_only(frames=PS_C_INTER_SHOT_SETTLE_FRAMES)
        self._since = time.time()
        self._stable.reset()
        self._console_cmd_index = 0
        self._console_cmd_total = self._cv.console_high_res_command_count(
            STILL_RES_X, STILL_RES_Y, self._filepath
        )
        self._al_invoked = False
        self._task = None
        self._capture_result = {}
        self._ticks_in_wait = 0
        self.phase = _PsCStillsPhase.CAPTURE_PENDING

    def _reset_wait_deadline(self) -> None:
        now = time.time()
        shots_left = max(1, len(STILL_CAM_LABELS) - self.shot_index)
        remaining_drive = max(0.0, self._drive_deadline - now)
        per_shot = min(
            PS_C_WAIT_FILE_SEC,
            max(12.0, (remaining_drive - 1.5) / shots_left),
        )
        self._wait_deadline = now + per_shot

    def _invoke_console_ladder_step(self) -> bool:
        if self._console_cmd_index >= self._console_cmd_total:
            return False
        _focus_ps_c_viewport()
        fired = self._cv.console_high_res_invoke_at_index(
            STILL_RES_X,
            STILL_RES_Y,
            self._filepath,
            self._capture_result,
            self._console_cmd_index,
            world=self.world,
        )
        if fired:
            self._methods.append(
                f"capture_viewport_console:{self._capture_result.get('method')}"
            )
            self._console_cmd_index += 1
        return fired

    def _invoke_capture_once(self) -> None:
        if self.phase != _PsCStillsPhase.CAPTURE_PENDING:
            return
        _focus_ps_c_viewport()
        if not self._al_invoked:
            _ok_al, al_methods, task = _automation_abs_screenshot(self._filepath, self._cam)
            self._methods.extend(al_methods)
            self._task = task
            self._al_invoked = True
            self._methods.append("primary:AutomationLibrary_abs")
        else:
            self._invoke_console_ladder_step()
        self._reset_wait_deadline()
        self._ticks_in_wait = 0
        self.phase = _PsCStillsPhase.WAITING_FILE

    def _poll_capture_wait(self) -> None:
        found = self._cv.probe_png_ready(
            self._filepath, self._since, os.path.basename(self._filepath), self._stable
        )
        if found:
            self._finish_shot(found)
            return
        task_done = _task_is_done(self._task)
        if task_done is True and not found:
            self._methods.append("automation_task_done_no_file_yet")
        self._ticks_in_wait += 1
        if self._ticks_in_wait > 0 and self._ticks_in_wait % PS_C_WAIT_RETRY_TICKS == 0:
            if self._console_cmd_index < self._console_cmd_total:
                if self._invoke_console_ladder_step():
                    self._reset_wait_deadline()
            elif not self._al_invoked:
                self.phase = _PsCStillsPhase.CAPTURE_PENDING
                self._invoke_capture_once()
                return
        if time.time() >= self._wait_deadline:
            resolved = _find_fresh_ps_still_path(self._filepath, self._since)
            self._finish_shot(resolved)

    def _finish_shot(self, resolved_path: Optional[str]) -> None:
        entry = _finalize_still_entry(
            self._cam_label,
            self._filepath,
            self._methods,
            since=self._since,
            resolved_on_disk=resolved_path,
        )
        self.entries.append(entry)
        self.shot_index += 1
        if self.shot_index < len(STILL_CAM_LABELS):
            self._settle_frames_left = PS_C_INTER_SHOT_SETTLE_FRAMES
            self.phase = _PsCStillsPhase.INTER_SHOT_SETTLE
        else:
            self.phase = _PsCStillsPhase.WRITE_MANIFEST

    def _finish_all(self) -> None:
        if self.phase == _PsCStillsPhase.DONE:
            return
        self._manifest_path = _write_stills_manifest(self.entries, self.stills_dir)
        self._unregister_tick()
        self.phase = _PsCStillsPhase.DISARM
        self._disarm_keep_alive()
        self.phase = _PsCStillsPhase.DONE
        _log(
            "stills driver finished",
            {
                "shots": len(self.entries),
                "manifest": self._manifest_path,
                "drive_ticks": self._drive_ticks,
            },
        )

    def _disarm_keep_alive(self) -> None:
        try:
            import vnp_editor_keep_alive as keep

            keep.disarm()
        except Exception:
            pass

    def _abort_in_flight_and_remaining(self) -> None:
        labels_done = {e.get("camera_label") for e in self.entries}
        while self.shot_index < len(STILL_CAM_LABELS):
            label = STILL_CAM_LABELS[self.shot_index]
            if label not in labels_done:
                path = _resolve_still_path(self.stills_dir, label)
                if (
                    self.phase
                    in (
                        _PsCStillsPhase.WAITING_FILE,
                        _PsCStillsPhase.CAPTURE_PENDING,
                        _PsCStillsPhase.PREPARING,
                    )
                    and label == self._cam_label
                ):
                    self.entries.append(
                        _finalize_still_entry(
                            label,
                            path,
                            list(self._methods),
                            since=self._since,
                            resolved_on_disk=None,
                        )
                    )
                else:
                    self.entries.append(
                        {
                            "camera_label": label,
                            "path": path,
                            "capture_outcome": OUTCOME_SOFT,
                            "error": "driver_timeout_before_shot",
                            "file_exists": False,
                            "note": "png_missing_black_or_path_soft_fail",
                        }
                    )
                labels_done.add(label)
            self.shot_index += 1


_ACTIVE_PS_C_STILLS: Optional[_PsCStillsOrchestrator] = None
_PS_C_SLATE_CALLBACK_REFS: list[Any] = []
_PS_C_DRIVER_ROOTS: list[Any] = []


def _ps_c_slate_pre_tick_dispatcher(delta: float) -> None:
    """Module-level Slate callback (strong ref; survives MCP script return)."""
    orch = _ACTIVE_PS_C_STILLS
    if orch is not None:
        orch._on_slate_pre_tick(delta)


def _drive_ps_c_stills_orchestrator(
    orch: _PsCStillsOrchestrator, timeout_sec: float
) -> bool:
    """Pump Slate + run driver ticks until DONE or timeout (no time.sleep)."""
    deadline = time.time() + timeout_sec
    cv = orch._cv or _load_capture_viewport()
    last_log = time.time()
    while orch.phase != _PsCStillsPhase.DONE and time.time() < deadline:
        orch._on_slate_pre_tick(0.033)
        cv._pump_editor_once()
        if time.time() - last_log >= 15.0:
            last_log = time.time()
            _log(
                "stills drive progress",
                {
                    "phase": orch.phase.value,
                    "shot_index": orch.shot_index,
                    "entries": len(orch.entries),
                    "drive_ticks": orch._drive_ticks,
                },
            )
    if orch.phase != _PsCStillsPhase.DONE:
        orch._driver_error = orch._driver_error or "stills_driver_timeout"
        _log("stills drive timeout", {"phase": orch.phase.value, "timeout_sec": timeout_sec})
        orch._abort_in_flight_and_remaining()
        orch.phase = _PsCStillsPhase.WRITE_MANIFEST
        orch._finish_all()
        return False
    return True


def _finalize_still_entry(
    cam_label: str,
    filepath: str,
    methods: list[str],
    *,
    since: float,
    resolved_on_disk: Optional[str],
) -> dict[str, Any]:
    entry: dict[str, Any] = {"camera_label": cam_label, "path": filepath, "methods": methods}
    entry["capture_path"] = (
        "slate_pretick capture_viewport HighResShot abs + AutomationLibrary abs "
        "(Saved/ps_stills/)"
    )
    entry["wait_mechanism"] = PS_C_SLATE_MECHANISM
    entry["capture_since"] = since
    if not os.path.isfile(filepath):
        copied = _copy_newest_png_matching(
            (cam_label, os.path.basename(filepath)), filepath, since
        )
        if copied:
            methods.append(f"copied_from:{copied}")
    if not os.path.isfile(filepath):
        shot_ids = MRQ_SHOT_STILL_FALLBACK.get(cam_label)
        if shot_ids:
            copied = _copy_newest_png_matching(shot_ids, filepath, since)
            if copied:
                methods.append(f"pa_e_mrq_fallback_copy:{copied}")
    entry["methods"] = methods
    entry["file_exists"] = os.path.isfile(filepath)
    if not entry["file_exists"]:
        entry["capture_outcome"] = OUTCOME_SOFT
        entry["note"] = "png_missing_black_or_path_soft_fail"
        return entry
    try:
        entry["file_mtime"] = os.path.getmtime(filepath)
    except OSError:
        entry["file_mtime"] = None
    if not _mtime_at_least(filepath, since):
        entry["capture_outcome"] = OUTCOME_SOFT
        entry["note"] = "stale_png_reuse_mtime_before_capture"
        entry["fresh_this_act"] = False
        return entry
    entry["fresh_this_act"] = True
    size = os.path.getsize(filepath)
    entry["bytes"] = size
    lum, lum_src = common.mean_luminance(filepath)
    entry["mean_luminance"] = lum
    entry["luminance_source"] = lum_src
    if size < common.MIN_BYTES:
        entry["capture_outcome"] = OUTCOME_SOFT
        entry["note"] = "file_too_small"
        return entry
    if lum is None or (lum is not None and lum < common.MIN_MEAN_LUMINANCE):
        entry["capture_outcome"] = OUTCOME_SOFT
        entry["note"] = "black_or_dark_still_soft_fail_not_closed_without_arrange_miss"
        return entry
    entry["capture_outcome"] = OUTCOME_PASS
    if resolved_on_disk:
        entry["resolved_path"] = resolved_on_disk
    return entry


def _write_stills_manifest(entries: list[dict[str, Any]], stills_dir: str) -> str:
    manifest = {
        "version": 1,
        "generated_at_iso": datetime.now(timezone.utc).isoformat(),
        "capture_path": (
            "slate pre-tick: purge stale PNG; AutomationLibrary abs primary; console HighResShot "
            "ladder retries on ticks; absolute Saved/ps_stills/; MRQ copy only if mtime >= capture_since"
        ),
        "wait_mechanism": PS_C_SLATE_MECHANISM,
        "resolution": [STILL_RES_X, STILL_RES_Y],
        "stills": entries,
    }
    manifest_path = os.path.join(stills_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, default=str)
    return manifest_path


def _automation_abs_screenshot(filepath: str, cam) -> tuple[bool, list[str], Any]:
    """Absolute-path AutomationLibrary (PL-D / capture_shotlist_viewport pattern)."""
    methods: list[str] = []
    ue_path = os.path.abspath(filepath).replace("\\", "/")
    delay = 0.35
    attempts = (
        ("abs_kwargs_force_gv", lambda: unreal.AutomationLibrary.take_high_res_screenshot(
            STILL_RES_X, STILL_RES_Y, ue_path, camera=cam, delay=delay, force_game_view=True
        )),
        ("abs_kwargs_gv", lambda: unreal.AutomationLibrary.take_high_res_screenshot(
            STILL_RES_X, STILL_RES_Y, ue_path, camera=cam, force_game_view=True
        )),
        ("abs_positional_gv", lambda: unreal.AutomationLibrary.take_high_res_screenshot(
            STILL_RES_X, STILL_RES_Y, ue_path, cam, True
        )),
        ("abs_legacy", lambda: unreal.AutomationLibrary.take_high_res_screenshot(
            STILL_RES_X, STILL_RES_Y, ue_path, cam
        )),
    )
    for name, fn in attempts:
        try:
            task = fn()
            methods.append(name)
            return True, methods, task
        except TypeError:
            continue
        except Exception as e:
            methods.append(f"{name}_fail:{e}")
    return False, methods, None


def _copy_newest_png_matching(needles: tuple[str, ...], dest: str, since: float) -> Optional[str]:
    import shutil

    roots = [
        os.path.join(common.project_dir(), "Saved", "Screenshots"),
        os.path.join(common.project_dir(), "Saved", "Screenshots", "PA_E"),
        os.path.join(common.project_dir(), "Saved", "MovieRenders"),
        os.path.dirname(dest),
    ]
    best: Optional[str] = None
    best_m = since
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, _dirs, files in os.walk(root):
            for fname in files:
                if not fname.lower().endswith(".png"):
                    continue
                lower = fname.lower()
                if not any(n.lower() in lower for n in needles):
                    continue
                path = os.path.join(dirpath, fname)
                try:
                    mtime = os.path.getmtime(path)
                except OSError:
                    continue
                if mtime >= since - 2.0 and mtime >= best_m:
                    best = path
                    best_m = mtime
    if best and os.path.isfile(best):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(best, dest)
        return best
    return None


def _build_ps_c_gate(
    *,
    blocked: list[str],
    pre_closed: bool,
    dress_count: int,
    pa_d_count: int,
    arrange_gate: dict[str, Any],
    dress_path: str,
    metrics: Optional[dict[str, Any]],
    metrics_path: str,
    still_entries: list[dict[str, Any]],
    manifest_path: str,
    stills_in_progress: bool = False,
    driver_error: Optional[str] = None,
) -> dict[str, Any]:
    stills_present = sum(1 for e in still_entries if e.get("file_exists"))
    stills_required = len(STILL_CAM_LABELS)
    capture_outcomes = [e.get("capture_outcome", OUTCOME_SOFT) for e in still_entries]

    placement_outcome = metrics.get("placement_outcome") if metrics else OUTCOME_CLOSED
    if pre_closed:
        placement_outcome = OUTCOME_CLOSED

    ready_for_ps_d = (
        not pre_closed
        and not stills_in_progress
        and metrics is not None
        and stills_present >= stills_required
        and placement_outcome in (OUTCOME_PASS, OUTCOME_SOFT)
    )
    if not ready_for_ps_d and not stills_in_progress:
        if metrics is None:
            blocked = list(blocked) + ["metrics_not_written"]
        if stills_present < stills_required:
            blocked = list(blocked) + [f"stills_incomplete:{stills_present}/{stills_required}"]

    gate: dict[str, Any] = {
        "version": 1,
        "track": "PS-C",
        "level_path": common.LEVEL_PATH,
        "preconditions": {
            "dress_count": dress_count,
            "pa_d_count": pa_d_count,
            "ps_arrange_gate_ready_for_ps_c": bool(arrange_gate.get("ready_for_ps_c")),
        },
        "placement_outcome": placement_outcome,
        "stills_present_count": stills_present,
        "stills_required_count": stills_required,
        "stills_capture_outcomes": capture_outcomes,
        "stills_in_progress": stills_in_progress,
        "stills_wait_mechanism": PS_C_DRIVE_MECHANISM,
        "stills_slate_callback": PS_C_SLATE_MECHANISM,
        "metrics_path": metrics_path if metrics else None,
        "stills_manifest_path": manifest_path or None,
        "dress_bounds_path": dress_path,
        "ready_for_ps_d": ready_for_ps_d,
        "blocked_reasons": blocked,
        "generated_at_iso": datetime.now(timezone.utc).isoformat(),
        "gate_string": "APPROVE PS-C",
        "note": (
            "ready_for_ps_d = metrics + still files on disk; PS-D is Lead eyeball vs benchmarks. "
            "Black/dark stills → soft_fail on capture, not closed_fail if Arrange gate was ready."
        ),
    }
    if driver_error:
        gate["stills_driver_error"] = driver_error
    return gate


def _write_ps_c_gate_file(gate: dict[str, Any]) -> str:
    gate_path = _project_saved_path("ps_c_prove_gate.json")
    with open(gate_path, "w", encoding="utf-8") as f:
        json.dump(gate, f, indent=2, default=str)
    gate["written_path"] = gate_path
    return gate_path


def _start_ps_c_stills_async(world, gate_context: dict[str, Any]) -> tuple[bool, Optional[str]]:
    global _ACTIVE_PS_C_STILLS
    if _ACTIVE_PS_C_STILLS is not None:
        return False, "ps_c_stills_driver_already_active"
    stills_dir = _project_saved_path("ps_stills")
    os.makedirs(stills_dir, exist_ok=True)
    keep_ok = False
    try:
        import vnp_editor_keep_alive as keep

        keep_ok = keep.arm()
    except Exception as e:
        return False, f"keep_alive_arm_failed:{e}"
    gate_context["keep_python_script_alive"] = keep_ok
    orch = _PsCStillsOrchestrator(
        world=world,
        stills_dir=stills_dir,
        gate_context=gate_context,
    )
    if not orch.start():
        gate_context["driver_error"] = orch._driver_error
        if keep_ok:
            try:
                import vnp_editor_keep_alive as keep

                keep.disarm()
            except Exception:
                pass
        return False, orch._driver_error or "slate_driver_start_failed"
    _ACTIVE_PS_C_STILLS = orch
    return True, None


def prove_ps_placement(*, skip_stills: bool = False) -> dict[str, Any]:
    """PS-C entry: preconditions, metrics, stills, gate sidecar."""
    global _ACTIVE_PS_C_STILLS
    blocked: list[str] = []
    pre_closed = False

    try:
        world_status = common.editor_world_markers_status()
        if not world_status.get("ok"):
            blocked.append("world_not_L_VS_MVP_Markers")
            pre_closed = True
    except Exception as e:
        blocked.append(f"world_check_failed:{e}")
        pre_closed = True

    dress_count = sum(
        1 for a in _all_level_actors() if common.actor_label(a).startswith(common.DRESS_LABEL_PREFIX)
    )
    pa_d_count = sum(1 for a in _all_level_actors() if common.actor_label(a).startswith("PA_D_"))
    if dress_count < 1:
        blocked.append("dress_count_zero")
        pre_closed = True
    if pa_d_count < 1:
        blocked.append("pa_d_count_zero")
        pre_closed = True

    arrange_gate, arrange_blocked = _ensure_arrange_gate()
    blocked.extend(arrange_blocked)
    if arrange_blocked and any(
        b in arrange_blocked
        for b in ("arrange_failed:", "arrange_ps_homestead_import_failed", "dress_count_zero")
    ):
        pre_closed = True

    dress_bounds, dress_path = _dress_bounds_from_file()
    if not dress_bounds:
        blocked.append("ps_dress_bounds_missing")
        pre_closed = True

    metrics: Optional[dict[str, Any]] = None
    metrics_path = _project_saved_path("ps_placement_metrics.json")
    still_entries: list[dict[str, Any]] = []
    manifest_path = ""

    world = unreal.EditorLevelLibrary.get_editor_world()
    island = _find_actor_label("DRESS_SM_IslandTop")

    if not pre_closed and dress_bounds:
        metrics = _compute_metrics(world=world, dress_bounds=dress_bounds, island_actor=island)
        os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2, default=str)
        _log("wrote ps_placement_metrics.json", {"path": metrics_path})

    stills_in_progress = False
    driver_error: Optional[str] = None

    if skip_stills:
        blocked.append("stills_skipped_by_flag")
    elif not pre_closed:
        gate_context = {
            "blocked": blocked,
            "pre_closed": pre_closed,
            "dress_count": dress_count,
            "pa_d_count": pa_d_count,
            "arrange_gate": arrange_gate,
            "dress_path": dress_path,
            "metrics": metrics,
            "metrics_path": metrics_path,
        }
        started, err = _start_ps_c_stills_async(world, gate_context)
        if started:
            orch = _ACTIVE_PS_C_STILLS
            if orch is not None:
                completed = _drive_ps_c_stills_orchestrator(orch, PS_C_DRIVE_TIMEOUT_SEC)
                still_entries = list(orch.entries)
                manifest_path = orch._manifest_path or ""
                driver_error = orch._driver_error
                if not completed:
                    blocked = list(blocked) + ["stills_driver_timeout"]
                _ACTIVE_PS_C_STILLS = None
        else:
            driver_error = err
            blocked.append(f"stills_driver_failed:{err}")

    gate = _build_ps_c_gate(
        blocked=blocked,
        pre_closed=pre_closed,
        dress_count=dress_count,
        pa_d_count=pa_d_count,
        arrange_gate=arrange_gate,
        dress_path=dress_path,
        metrics=metrics,
        metrics_path=metrics_path,
        still_entries=still_entries,
        manifest_path=manifest_path,
        stills_in_progress=stills_in_progress,
        driver_error=driver_error,
    )
    _write_ps_c_gate_file(gate)
    _log(
        "prove complete",
        {
            "ready_for_ps_d": gate.get("ready_for_ps_d"),
            "placement_outcome": gate.get("placement_outcome"),
            "stills_in_progress": stills_in_progress,
            "stills": gate.get("stills_present_count"),
            "blocked": blocked,
        },
    )
    return gate


def main() -> None:
    gate = prove_ps_placement()
    print(
        json.dumps(
            {
                "ok": gate.get("ready_for_ps_d"),
                "stills_in_progress": gate.get("stills_in_progress"),
                "placement_outcome": gate.get("placement_outcome"),
                "gate_path": gate.get("written_path"),
                "wait_mechanism": gate.get("stills_wait_mechanism"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

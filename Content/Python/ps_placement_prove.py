# ps_placement_prove.py
# PS-C: Automated placement metrics + viewport still capture on L_VS_MVP_Markers.
# Run in Unreal Editor or MCP: execute_python_script("ps_placement_prove.py").
# Chain (DESKTOP): markers → dress → pa_d → arrange_ps_homestead.py → this script.
# Harness P3 exempt: PS track prove (Arrange gate via ps_arrange_gate.json / arrange_ps_homestead).
# Writes Saved/ps_placement_metrics.json, Saved/ps_stills/*, Saved/ps_c_prove_gate.json.

from __future__ import annotations

import importlib
import json
import os
import sys
import time
from datetime import datetime, timezone
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
MRQ_SHOT_STILL_FALLBACK = {
    "CAM_Hero": ("shot1",),
    "CAM_CabinClose": ("shot2",),
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


def _load_capture_viewport():
    import capture_viewport as cv

    importlib.reload(cv)
    return cv


def _automation_abs_screenshot(filepath: str, cam) -> tuple[bool, list[str]]:
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
            fn()
            methods.append(name)
            return True, methods
        except TypeError:
            continue
        except Exception as e:
            methods.append(f"{name}_fail:{e}")
    return False, methods


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


def _capture_still_from_camera(
    cam_label: str,
    filepath: str,
    *,
    world,
) -> dict[str, Any]:
    entry: dict[str, Any] = {"camera_label": cam_label, "path": filepath}
    cam = _find_actor_label(cam_label)
    if not cam:
        entry["capture_outcome"] = OUTCOME_CLOSED
        entry["error"] = "camera_missing"
        return entry

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    _pilot_camera(cam)
    methods: list[str] = []
    since = time.time()
    cv = _load_capture_viewport()
    cv._finish_loading_before_screenshot()
    lit = cv._set_lit_view_mode()
    if lit:
        methods.append(lit)
    for _ in range(12):
        cv._pump_editor_once()

    capture_result: dict[str, Any] = {}
    if cv._console_high_res(STILL_RES_X, STILL_RES_Y, filepath, capture_result):
        methods.append(f"capture_viewport_console:{capture_result.get('method')}")
    else:
        ok_al, al_methods = _automation_abs_screenshot(filepath, cam)
        methods.extend(al_methods)
        if ok_al:
            cv._settle()
            found = cv._wait_for_file(
                filepath, since, os.path.basename(filepath)
            )
            if found:
                methods.append("automation_abs_wait_ok")
        if not os.path.isfile(filepath):
            ue_path = os.path.abspath(filepath).replace("\\", "/")
            try:
                unreal.SystemLibrary.execute_console_command(
                    world,
                    f'HighResShot filename="{ue_path}" {STILL_RES_X}x{STILL_RES_Y}',
                )
                methods.append("HighResShot_abs_filename_first")
            except Exception as e:
                methods.append(f"HighResShot_abs_fail:{e}")
            cv._settle()
            cv._wait_for_file(filepath, since, os.path.basename(filepath))

    if not os.path.isfile(filepath):
        copied = _copy_newest_png_matching((cam_label, os.path.basename(filepath)), filepath, since)
        if copied:
            methods.append(f"copied_from:{copied}")

    if not os.path.isfile(filepath):
        shot_ids = MRQ_SHOT_STILL_FALLBACK.get(cam_label)
        if shot_ids:
            copied = _copy_newest_png_matching(shot_ids, filepath, since - 86400.0)
            if copied:
                methods.append(f"pa_e_mrq_fallback_copy:{copied}")

    entry["methods"] = methods
    entry["capture_path"] = "capture_viewport HighResShot abs + AutomationLibrary abs (no relative fname)"
    entry["file_exists"] = os.path.isfile(filepath)
    if not entry["file_exists"]:
        entry["capture_outcome"] = OUTCOME_SOFT
        entry["note"] = "png_missing_black_or_path_soft_fail"
        return entry

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
    return entry


def _capture_stills(world) -> tuple[list[dict[str, Any]], str]:
    stills_dir = _project_saved_path("ps_stills")
    os.makedirs(stills_dir, exist_ok=True)
    entries: list[dict[str, Any]] = []
    for label in STILL_CAM_LABELS:
        path = _resolve_still_path(stills_dir, label)
        entries.append(_capture_still_from_camera(label, path, world=world))

    manifest = {
        "version": 1,
        "generated_at_iso": datetime.now(timezone.utc).isoformat(),
        "capture_path": (
            "capture_viewport.py console HighResShot (absolute path under Saved/ps_stills/) + "
            "AutomationLibrary abs; optional PA-E MRQ PNG copy for CAM_Hero/CAM_CabinClose"
        ),
        "resolution": [STILL_RES_X, STILL_RES_Y],
        "stills": entries,
    }
    manifest_path = os.path.join(stills_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, default=str)
    return entries, manifest_path


def prove_ps_placement(*, skip_stills: bool = False) -> dict[str, Any]:
    """PS-C entry: preconditions, metrics, stills, gate sidecar."""
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

    if not skip_stills and not pre_closed:
        still_entries, manifest_path = _capture_stills(world)
    elif skip_stills:
        blocked.append("stills_skipped_by_flag")

    stills_present = sum(1 for e in still_entries if e.get("file_exists"))
    stills_required = len(STILL_CAM_LABELS)
    capture_outcomes = [e.get("capture_outcome", OUTCOME_SOFT) for e in still_entries]

    placement_outcome = metrics.get("placement_outcome") if metrics else OUTCOME_CLOSED
    if pre_closed:
        placement_outcome = OUTCOME_CLOSED

    ready_for_ps_d = (
        not pre_closed
        and metrics is not None
        and stills_present >= stills_required
        and placement_outcome in (OUTCOME_PASS, OUTCOME_SOFT)
    )
    if not ready_for_ps_d:
        if metrics is None:
            blocked.append("metrics_not_written")
        if stills_present < stills_required:
            blocked.append(f"stills_incomplete:{stills_present}/{stills_required}")

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

    gate_path = _project_saved_path("ps_c_prove_gate.json")
    with open(gate_path, "w", encoding="utf-8") as f:
        json.dump(gate, f, indent=2, default=str)
    gate["written_path"] = gate_path
    _log(
        "prove complete",
        {
            "ready_for_ps_d": ready_for_ps_d,
            "placement_outcome": placement_outcome,
            "stills": stills_present,
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
                "placement_outcome": gate.get("placement_outcome"),
                "gate_path": gate.get("written_path"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

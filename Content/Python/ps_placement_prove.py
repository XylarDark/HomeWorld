# ps_placement_prove.py
# PS-C: Automated placement metrics + viewport still capture on L_VS_MVP_Markers.
# Run in Unreal Editor or MCP: execute_python_script("ps_placement_prove.py").
# One-cam bite (CAP-001 isolate): set PS_C_ONE_CAM_LABEL=CAM_CabinClose or PS_C_ONE_CAM=1
# before Act, or argv --one-cam CAM_CabinClose. Full 7-still path when unset (Conductor default later).
# Chain (DESKTOP): markers → dress → pa_d → arrange_ps_homestead.py → this script.
# Harness P3 exempt: PS track prove (Arrange gate via ps_arrange_gate.json / arrange_ps_homestead).
# Writes Saved/ps_placement_metrics.json, Saved/ps_stills/*, Saved/ps_c_prove_gate.json.
# Stills: full 7 = slate pre-tick driver + pump-until-done (≤300s). One-cam bite =
# CAP001_SETTLE_AFTER_YIELD_V1 Phase A: single AL fire + act_fired_at stamp, return (Phase B = host).

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

# Design canon: Docs/handoffs/PS_C_METRICS.md § Still capture set (7 PNGs).
# Maps PS-A strategy IDs (PS_A_INVENTORY.md §2): PS_Lookout_Hero→CAM_Hero,
# PS_Cabin_ThreeQuarter→CAM_CabinClose; spawned PS_* per PS-B arrange_ps_homestead.
# Do not add labels here without Lead/Design handoff update (no invented cams).
_PS_C_STILL_LABELS_CANON = frozenset(
    {
        "PS_N_HighIso",
        "PS_E_HighIso",
        "PS_Cliff_Underside",
        "PS_Path_Corridor",
        "PS_Garden_Close",
        "CAM_Hero",
        "CAM_CabinClose",
    }
)

STILL_CAM_LABELS = (
    "PS_N_HighIso",
    "PS_E_HighIso",
    "PS_Cliff_Underside",
    "PS_Path_Corridor",
    "PS_Garden_Close",
    "CAM_Hero",
    "CAM_CabinClose",
)

# Runtime still set (full 7 default; one-cam bite overrides per Act — see PS_C_ONE_CAM_LABEL).
_ACTIVE_STILL_CAM_LABELS: tuple[str, ...] = STILL_CAM_LABELS
PS_C_ONE_CAM_DEFAULT_LABEL = "CAM_CabinClose"

STILL_RES_X, STILL_RES_Y = 1600, 900
PS_C_WAIT_FILE_SEC = 48.0
PS_C_ONE_CAM_WAIT_FILE_SEC = 72.0
PS_C_INTER_SHOT_SETTLE_FRAMES = 8
PS_C_DRIVE_TIMEOUT_SEC = 300.0
PS_C_ONE_CAM_DRIVE_TIMEOUT_SEC = 120.0
PS_C_WAIT_RETRY_TICKS = 6
PS_C_FINAL_DRAIN_SEC = 12.0
PS_C_GATE_SETTLE_SEC = 120.0
PS_C_ONE_CAM_GATE_SETTLE_SEC = 180.0
# Windows/FAT mtime often 1s — allow gate stamp slightly after file mtime (not post-gate async).
PS_C_ACT_END_MTIME_SLACK_SEC = 1.05
PS_C_PS_CAM_PREFIX = "PS_"
PS_C_STABLE_POLLS_REQUIRED = 2
PS_C_SLATE_MECHANISM = "register_slate_pre_tick_callback"
PS_C_DRIVE_MECHANISM = "slate_callback_plus_pump_until_done"
CAP001_SETTLE_AFTER_YIELD_V1 = "CAP001_SETTLE_AFTER_YIELD_V1"
CAP001_DARK_STILL_LIT_AIM_V1 = "CAP001_DARK_STILL_LIT_AIM_V1"
CAP001_DARK_STILL_NIGHT_STACK_V2 = "CAP001_DARK_STILL_NIGHT_STACK_V2"
CAP001_PHASE_B_SIDECAR = "ps_c_cap001_phase_b.json"
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


def _still_labels() -> tuple[str, ...]:
    return _ACTIVE_STILL_CAM_LABELS


def _resolve_one_cam_label_from_env_or_argv() -> Optional[str]:
    """One-cam bite: env PS_C_ONE_CAM_LABEL / PS_C_ONE_CAM or argv --one-cam <label>."""
    import sys

    for i, arg in enumerate(sys.argv):
        if arg in ("--one-cam", "--one_cam") and i + 1 < len(sys.argv):
            return sys.argv[i + 1].strip()
    raw = (os.environ.get("PS_C_ONE_CAM_LABEL") or os.environ.get("PS_C_ONE_CAM") or "").strip()
    if raw.lower() in ("1", "true", "yes", "bite"):
        return PS_C_ONE_CAM_DEFAULT_LABEL
    return raw or None


def _apply_prove_still_label_set(
    one_cam_label: Optional[str] = None,
) -> dict[str, Any]:
    """Configure full vs one-cam still Act (Design canon labels only)."""
    global _ACTIVE_STILL_CAM_LABELS
    label = one_cam_label if one_cam_label is not None else _resolve_one_cam_label_from_env_or_argv()
    if not label:
        _ACTIVE_STILL_CAM_LABELS = STILL_CAM_LABELS
        return {
            "prove_mode": "full",
            "stills_required_count": len(STILL_CAM_LABELS),
            "still_labels": list(_ACTIVE_STILL_CAM_LABELS),
        }
    if label not in _PS_C_STILL_LABELS_CANON:
        return {
            "prove_mode": "one_cam_invalid",
            "one_cam_label": label,
            "error": f"one_cam_label_not_in_design_canon:{label}",
        }
    _ACTIVE_STILL_CAM_LABELS = (label,)
    return {
        "prove_mode": "one_cam",
        "one_cam_label": label,
        "stills_required_count": 1,
        "still_labels": [label],
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


def _still_cam_labels_missing() -> list[str]:
    """Prove still labels that must exist after PS-B Arrange (inventory gate)."""
    return [lbl for lbl in _still_labels() if _find_actor_label(lbl) is None]


def _prove_still_labels_drift_from_design() -> Optional[str]:
    """None if STILL_CAM_LABELS matches PS-C handoff; else bounce-to-Design message."""
    current = frozenset(STILL_CAM_LABELS)
    if current == _PS_C_STILL_LABELS_CANON:
        return None
    only_prove = sorted(current - _PS_C_STILL_LABELS_CANON)
    only_canon = sorted(_PS_C_STILL_LABELS_CANON - current)
    return (
        "prove_camera_labels_drift_design_bounce:"
        f"prove_only={only_prove or []};canon_only={only_canon or []};"
        "patch Docs/handoffs/PS_C_METRICS.md + PS_A_INVENTORY.md — do not invent cams"
    )


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


def _ensure_arrange_gate() -> tuple[dict[str, Any], list[str], bool]:
    """Return arrange gate, blocked reasons, and whether prove may Act (cameras in level)."""
    blocked: list[str] = []
    gate_path = _project_saved_path("ps_arrange_gate.json")
    gate = _load_json(gate_path)
    missing_cams = _still_cam_labels_missing()
    if gate and gate.get("ready_for_ps_c") and not missing_cams:
        gate["read_from"] = gate_path
        return gate, blocked, True

    if gate and gate.get("ready_for_ps_c") and missing_cams:
        _log(
            "stale ps_arrange_gate ready but prove cameras missing; re-running arrange_ps_homestead",
            {"missing": missing_cams},
        )

    if gate and not gate.get("ready_for_ps_c"):
        blocked.append("ps_arrange_gate_not_ready")
    elif not gate:
        blocked.append("ps_arrange_gate_missing")

    if ps_arrange is None:
        blocked.append("arrange_ps_homestead_import_failed")
        return gate or {}, blocked, False

    _log(
        "running arrange_ps_homestead.py",
        {"missing_before": missing_cams, "gate_ready": bool(gate and gate.get("ready_for_ps_c"))},
    )
    try:
        gate = ps_arrange.arrange_ps_homestead()
    except Exception as e:
        blocked.append(f"arrange_failed:{e}")
        return gate or {}, blocked, False

    missing_after = _still_cam_labels_missing()
    if missing_after:
        blocked.append(f"inventory_cameras_missing_closed_fail:{','.join(missing_after)}")
        if not gate.get("ready_for_ps_c"):
            blocked.append("arrange_still_not_ready_for_ps_c")
        return gate, blocked, False

    if not gate.get("ready_for_ps_c"):
        blocked.append("arrange_still_not_ready_for_ps_c")
        return gate, blocked, False

    return gate, blocked, True


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


def _ps_c_stills_dir_abs() -> str:
    """Canonical Saved/ps_stills under project_dir (AL write ≡ settle ≡ gate score)."""
    path = common.abs_path(os.path.join(common.project_dir(), "Saved", "ps_stills"))
    os.makedirs(path, exist_ok=True)
    return path


def _ps_c_canonical_still_path(cam_label: str) -> str:
    """Single abs path for a still label — same as capture_viewport._ensure_abs_dest."""
    cv = _load_capture_viewport()
    safe = cam_label.replace("/", "_")
    return cv._ensure_abs_dest(os.path.join(_ps_c_stills_dir_abs(), f"{safe}.png"))


def _resolve_still_path(stills_dir: str, cam_label: str) -> str:
    """Absolute path under {Project}/Saved/ps_stills/ (never basename-only / engine CWD)."""
    _ = stills_dir
    return _ps_c_canonical_still_path(cam_label)


def _mtime_at_least(path: str, since: float) -> bool:
    try:
        return os.path.getmtime(path) >= since - 0.05
    except OSError:
        return False


def _mtime_in_act_window(path: str, act_start: float, act_end: Optional[float]) -> bool:
    """True when file mtime is within [act_start, act_end] (inclusive slack)."""
    path = common.abs_path(path)
    if not _mtime_at_least(path, act_start):
        return False
    if act_end is None:
        return True
    try:
        return os.path.getmtime(path) <= act_end + PS_C_ACT_END_MTIME_SLACK_SEC
    except OSError:
        return False


def _ps_still_counts_for_gate(
    path: str, act_start: float, act_end: Optional[float]
) -> bool:
    """Gate truth: on disk, MIN_BYTES, mtime inside Act window (excludes stale + post-settle)."""
    path = common.abs_path(path)
    if not os.path.isfile(path):
        return False
    try:
        if os.path.getsize(path) < common.MIN_BYTES:
            return False
    except OSError:
        return False
    return _mtime_in_act_window(path, act_start, act_end)


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


def _ps_still_fresh_on_disk(
    path: str, act_since: float, act_end: Optional[float] = None
) -> bool:
    return _ps_still_counts_for_gate(path, act_since, act_end)


def _audit_ps_stills_disk(
    stills_dir: str, act_since: float, act_end: Optional[float] = None
) -> dict[str, Any]:
    """Authoritative fresh PNG count for gate (Act window mtime + MIN_BYTES)."""
    per_label: list[dict[str, Any]] = []
    fresh_count = 0
    for label in _still_labels():
        path = common.abs_path(_resolve_still_path(stills_dir, label))
        fresh = _ps_still_fresh_on_disk(path, act_since, act_end)
        mtime: Optional[float] = None
        if os.path.isfile(path):
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                mtime = None
        if fresh:
            fresh_count += 1
        per_label.append(
            {
                "camera_label": label,
                "path": path,
                "fresh_this_act": fresh,
                "file_mtime": mtime,
                "capture_act_since": act_since,
                "capture_act_end": act_end,
            }
        )
    return {
        "fresh_count": fresh_count,
        "required_count": len(_still_labels()),
        "per_label": per_label,
        "stills_dir": common.abs_path(stills_dir),
        "capture_act_end": act_end,
    }


def _reconcile_still_entries_from_disk(
    entries: list[dict[str, Any]],
    act_since: float,
    stills_dir: str,
    *,
    act_end: Optional[float] = None,
) -> list[dict[str, Any]]:
    """Align manifest rows with disk truth; never count stale file_exists toward gate."""
    by_label: dict[str, dict[str, Any]] = {}
    for ent in entries:
        label = ent.get("camera_label")
        if label:
            by_label[str(label)] = ent
    reconciled: list[dict[str, Any]] = []
    for label in _still_labels():
        path = common.abs_path(_resolve_still_path(stills_dir, label))
        ent = dict(by_label.get(label) or {"camera_label": label, "path": path, "methods": []})
        ent["path"] = path
        since = float(ent.get("capture_since") or act_since)
        resolved = _find_fresh_ps_still_path(path, since)
        if resolved and resolved != path:
            methods = list(ent.get("methods") or [])
            if f"reconcile_copy:{resolved}" not in methods:
                methods.append(f"reconcile_copy:{resolved}")
            ent = _finalize_still_entry(
                label,
                path,
                methods,
                since=since,
                resolved_on_disk=resolved,
                act_end=act_end,
            )
        elif _ps_still_fresh_on_disk(path, since, act_end):
            methods = list(ent.get("methods") or [])
            ent = _finalize_still_entry(
                label,
                path,
                methods,
                since=since,
                resolved_on_disk=path,
                act_end=act_end,
            )
        else:
            on_disk = os.path.isfile(path)
            in_window = _ps_still_counts_for_gate(path, since, act_end) if on_disk else False
            ent["on_disk"] = on_disk
            ent["file_exists"] = in_window
            ent["exists"] = in_window
            if on_disk:
                try:
                    ent["bytes"] = os.path.getsize(path)
                    ent["file_mtime"] = os.path.getmtime(path)
                except OSError:
                    pass
            ent["fresh_this_act"] = False
            ent["counts_toward_gate"] = False
            if on_disk and not _mtime_at_least(path, since):
                ent["capture_outcome"] = OUTCOME_SOFT
                ent["note"] = ent.get("note") or "stale_png_reuse_mtime_before_capture"
            elif on_disk and act_end is not None and not _mtime_in_act_window(path, since, act_end):
                ent["capture_outcome"] = OUTCOME_SOFT
                ent["note"] = ent.get("note") or "post_settle_png_landing_excluded_from_gate"
            elif not on_disk:
                ent.setdefault("capture_outcome", OUTCOME_SOFT)
                ent.setdefault("note", "png_missing_black_or_path_soft_fail")
        ent["counts_toward_gate"] = bool(ent.get("fresh_this_act"))
        ent["exists"] = bool(ent.get("file_exists"))
        reconciled.append(ent)
    return reconciled


def _ps_c_pending_tasks_done(orch: "_PsCStillsOrchestrator") -> bool:
    for task in list(getattr(orch, "_pending_automation_tasks", []) or []):
        done = _task_is_done(task)
        if done is False:
            return False
    return True


def _ps_c_path_stable_for_gate(
    path: str,
    act_start: float,
    tracker: Any,
) -> bool:
    """capture_viewport _StableSizeTracker: MIN_BYTES + mtime >= act_start + size stable."""
    path = common.abs_path(path)
    if not os.path.isfile(path) or not _mtime_at_least(path, act_start):
        tracker.reset()
        return False
    try:
        if os.path.getsize(path) < common.MIN_BYTES:
            tracker.reset()
            return False
    except OSError:
        tracker.reset()
        return False
    return bool(tracker.observe(path))


def _ps_c_all_still_paths_stable(
    act_start: float,
    labels: tuple[str, ...],
    trackers: dict[str, Any],
) -> bool:
    for label in labels:
        path = _ps_c_canonical_still_path(label)
        if not _ps_c_path_stable_for_gate(path, act_start, trackers[label]):
            return False
    return True


def _ps_c_probe_canonical_still_paths(
    orch: "_PsCStillsOrchestrator",
    act_start: float,
    trackers: dict[str, Any],
) -> None:
    """Pull async AL/console PNG onto canonical abs paths (probe_png_ready each tick)."""
    cv = orch._cv or _load_capture_viewport()
    for label in orch._still_labels:
        path = _ps_c_canonical_still_path(label)
        tracker = trackers[label]
        cv.probe_png_ready(path, act_start, os.path.basename(path), tracker)


def _ps_c_poll_late_still_pngs(orch: "_PsCStillsOrchestrator", act_end: Optional[float]) -> None:
    """One pass: copy/probe late PNGs into orch.entries (keep slate pump in settle loop)."""
    if orch.phase != _PsCStillsPhase.DONE:
        return
    act = orch._act_started_at
    labels = orch._still_labels
    for idx, label in enumerate(labels):
        if idx >= len(orch.entries):
            break
        ent = orch.entries[idx]
        if ent.get("fresh_this_act") and ent.get("counts_toward_gate"):
            continue
        path = common.abs_path(ent.get("path") or _resolve_still_path(orch.stills_dir, label))
        since = float(ent.get("capture_since") or act)
        found = _find_fresh_ps_still_path(path, since)
        if found and _ps_still_counts_for_gate(found, since, act_end):
            orch.entries[idx] = _finalize_still_entry(
                label,
                path,
                list(ent.get("methods") or []),
                since=since,
                resolved_on_disk=found,
                act_end=act_end,
            )


def _ps_c_settle_stills_before_gate(
    orch: "_PsCStillsOrchestrator",
    stills_dir: str,
    act_start: float,
    max_sec: float,
) -> tuple[list[dict[str, Any]], float, list[str], bool]:
    """Wait for stable PNG on canonical abs paths; gate/manifest only after paths_ready."""
    cv = orch._cv or _load_capture_viewport()
    deadline = time.time() + max_sec
    stable_polls = 0
    labels = orch._still_labels
    trackers = {label: cv._StableSizeTracker() for label in labels}
    canonical = {label: _ps_c_canonical_still_path(label) for label in labels}
    settle_blocked: list[str] = []
    _log(
        "stills gate settle start",
        {
            "max_sec": max_sec,
            "labels": list(labels),
            "canonical_paths": canonical,
            "pending_tasks": len(getattr(orch, "_pending_automation_tasks", []) or []),
            "mechanism": "AutomationLibrary_probe_png_ready_stable_size",
        },
    )
    while time.time() < deadline:
        for task in list(getattr(orch, "_pending_automation_tasks", []) or []):
            _task_is_done(task)
        cv._pump_editor_once()
        if orch._tick_handle is not None:
            orch._on_slate_pre_tick(0.033)
        _ps_c_probe_canonical_still_paths(orch, act_start, trackers)
        _ps_c_poll_late_still_pngs(orch, None)
        paths_stable = _ps_c_all_still_paths_stable(act_start, labels, trackers)
        tasks_done = _ps_c_pending_tasks_done(orch)
        if paths_stable and tasks_done:
            stable_polls += 1
            if stable_polls >= PS_C_STABLE_POLLS_REQUIRED:
                break
        else:
            stable_polls = 0
    for _ in range(4):
        cv._pump_editor_once()
        if orch._tick_handle is not None:
            orch._on_slate_pre_tick(0.033)
        _ps_c_probe_canonical_still_paths(orch, act_start, trackers)
    paths_stable_final = _ps_c_all_still_paths_stable(act_start, labels, trackers)
    if not paths_stable_final:
        settle_blocked.append("one_cam_still_not_stable_in_act_window")
        for label in labels:
            path = canonical[label]
            stamp = common.stamp_file_artifact(path)
            settle_blocked.append(f"settle_polled_path:{label}:{json.dumps(stamp, default=str)}")
    paths_ready = paths_stable_final
    act_end: Optional[float] = time.time() if paths_ready else None
    still_entries: list[dict[str, Any]] = []
    if paths_ready:
        act_end = time.time()
        still_entries = _reconcile_still_entries_from_disk(
            list(orch.entries), act_start, stills_dir, act_end=act_end
        )
    _log(
        "stills gate settle complete",
        {
            "act_end": act_end,
            "paths_stable_final": paths_stable_final,
            "paths_ready": paths_ready,
            "fresh": (
                _audit_ps_stills_disk(stills_dir, act_start, act_end).get("fresh_count")
                if paths_ready
                else 0
            ),
            "tasks_done": _ps_c_pending_tasks_done(orch),
            "canonical_paths": canonical,
        },
    )
    return still_entries, act_end, settle_blocked, paths_ready


def _ps_c_gate_hold_until_canonical_paths(
    orch: "_PsCStillsOrchestrator",
    stills_dir: str,
    act_start: float,
    max_sec: float,
) -> tuple[list[dict[str, Any]], float, list[str], bool]:
    """One-cam: forbid gate until canonical abs path has MIN_BYTES + stable (AL async flush)."""
    cv = orch._cv or _load_capture_viewport()
    labels = orch._still_labels
    trackers = {label: cv._StableSizeTracker() for label in labels}
    canonical = {label: _ps_c_canonical_still_path(label) for label in labels}
    blocked: list[str] = []
    deadline = time.time() + max_sec
    stable_polls = 0
    _log("one-cam gate hold until canonical path ready", {"max_sec": max_sec, "paths": canonical})
    while time.time() < deadline:
        for task in list(getattr(orch, "_pending_automation_tasks", []) or []):
            _task_is_done(task)
        cv._pump_editor_once()
        if orch._tick_handle is not None:
            orch._on_slate_pre_tick(0.033)
        _ps_c_probe_canonical_still_paths(orch, act_start, trackers)
        if _ps_c_all_still_paths_stable(act_start, labels, trackers) and _ps_c_pending_tasks_done(
            orch
        ):
            stable_polls += 1
            if stable_polls >= PS_C_STABLE_POLLS_REQUIRED:
                act_end = time.time()
                still_entries = _reconcile_still_entries_from_disk(
                    list(orch.entries), act_start, stills_dir, act_end=act_end
                )
                _log("one-cam gate hold satisfied", {"act_end": act_end, "paths": canonical})
                return still_entries, act_end, blocked, True
        else:
            stable_polls = 0
    for label in labels:
        blocked.append(
            f"gate_hold_timeout:{label}:{json.dumps(common.stamp_file_artifact(canonical[label]), default=str)}"
        )
    act_end = time.time()
    still_entries = _reconcile_still_entries_from_disk(
        list(orch.entries), act_start, stills_dir, act_end=act_end
    )
    return still_entries, act_end, blocked, False


def _automation_abs_screenshot_one_invoke(filepath: str, cam) -> tuple[bool, list[str], Any]:
    """Single AL invoke (one-cam Phase A — fire only; no in-script wait)."""
    cv = _load_capture_viewport()
    dest_abs = cv._ensure_abs_dest(filepath)
    ue_path = cv._path_for_ue(dest_abs)
    methods: list[str] = [
        f"al_canonical_dest:{ue_path}",
        "one_cam:AutomationLibrary_abs_sync_single",
    ]
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


def _cap001_env_phase_b_absorb_only() -> bool:
    """Conductor: host poll wrote phase B sidecar — absorb gate without re-firing AL."""
    raw = (os.environ.get("PS_C_CAP001_PHASE_B_ABSORB") or "").strip().lower()
    return raw in ("1", "true", "yes")


def _cap001_phase_b_sidecar_path() -> str:
    return _project_saved_path(CAP001_PHASE_B_SIDECAR)


def _cap001_load_json_sidecar(path: str) -> Optional[dict[str, Any]]:
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else None
    except (OSError, json.JSONDecodeError) as e:
        _log("cap001 sidecar read failed", {"path": path, "error": str(e)})
        return None


def _cap001_load_phase_a_from_saved_gate() -> Optional[dict[str, Any]]:
    gate = _cap001_load_json_sidecar(_project_saved_path("ps_c_prove_gate.json"))
    if not gate:
        return None
    cap = gate.get("cap001_settle_after_yield_v1")
    if isinstance(cap, dict):
        if cap.get("phase") == "B" and isinstance(cap.get("phase_a"), dict):
            return cap["phase_a"]
        if cap.get("phase") == "A":
            return cap
    act_fired = gate.get("act_fired_at")
    path_abs = gate.get("canonical_still_path_abs")
    label = gate.get("one_cam_label")
    if act_fired is not None and path_abs and label:
        return {
            "contract": CAP001_SETTLE_AFTER_YIELD_V1,
            "phase": "A",
            "camera_label": label,
            "canonical_still_path_abs": path_abs,
            "act_fired_at": act_fired,
            "fire_ok": True,
            "fire_error": None,
        }
    return None


def _cap001_load_still_entries_from_manifest() -> list[dict[str, Any]]:
    manifest_path = os.path.join(_ps_c_stills_dir_abs(), "manifest.json")
    manifest = _cap001_load_json_sidecar(manifest_path)
    if not manifest:
        return []
    stills = manifest.get("stills")
    return list(stills) if isinstance(stills, list) else []


def _cap001_validate_phase_b_settle(
    phase_a: dict[str, Any],
    phase_b: dict[str, Any],
) -> tuple[bool, str]:
    if not phase_a.get("fire_ok"):
        return False, "phase_a_not_fire_ok"
    act_fired = phase_a.get("act_fired_at")
    if act_fired is None:
        return False, "phase_a_no_act_fired_at"
    path_a = common.abs_path(str(phase_a.get("canonical_still_path_abs") or ""))
    path_b = common.abs_path(
        str(phase_b.get("canonical_still_path_abs") or path_a or "")
    )
    if not path_a or path_a != path_b:
        return False, "canonical_path_mismatch"
    b_fired = phase_b.get("act_fired_at")
    if b_fired is not None and abs(float(b_fired) - float(act_fired)) > 0.5:
        return False, "act_fired_at_mismatch"
    if phase_b.get("settle_ok") is False:
        return False, "phase_b_settle_ok_false"
    if not os.path.isfile(path_b):
        return False, "png_missing_on_disk"
    try:
        size = os.path.getsize(path_b)
        mtime = os.path.getmtime(path_b)
    except OSError as exc:
        return False, f"stat_failed:{exc}"
    if size < common.MIN_BYTES:
        return False, "below_min_bytes"
    if mtime < float(act_fired) - 0.05:
        return False, "mtime_before_act_fired_at"
    stamp_bytes = phase_b.get("bytes")
    if stamp_bytes is not None:
        try:
            if int(stamp_bytes) < common.MIN_BYTES:
                return False, "phase_b_stamp_bytes_below_min"
        except (TypeError, ValueError):
            pass
    return True, "ok"


def _cap001_apply_phase_b_to_entries(
    phase_a: dict[str, Any],
    phase_b: dict[str, Any],
    entries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    act_fired = float(phase_a["act_fired_at"])
    path = common.abs_path(str(phase_a["canonical_still_path_abs"]))
    cam_label = str(phase_a.get("camera_label") or "")
    act_end = float(
        phase_b.get("settle_observed_at")
        or phase_b.get("host_poll_at")
        or time.time()
    )
    methods_base = ["CAP001_SETTLE_AFTER_YIELD_V1:phase_b_host_absorbed"]
    if not entries:
        entries = [
            {
                "camera_label": cam_label,
                "path": path,
                "methods": list(methods_base),
            }
        ]
    updated: list[dict[str, Any]] = []
    matched = False
    for ent in entries:
        e = dict(ent)
        if str(e.get("camera_label")) == cam_label:
            matched = True
            merged_methods = list(e.get("methods") or []) + methods_base
            e = _finalize_still_entry(
                cam_label,
                path,
                merged_methods,
                since=act_fired,
                resolved_on_disk=path,
                act_end=act_end,
            )
            e["cap001_phase"] = "B"
            e["act_fired_at"] = act_fired
            e["canonical_still_path_abs"] = path
        updated.append(e)
    if not matched:
        updated.append(
            _finalize_still_entry(
                cam_label,
                path,
                methods_base,
                since=act_fired,
                resolved_on_disk=path,
                act_end=act_end,
            )
        )
        updated[-1]["cap001_phase"] = "B"
    return updated


def _cap001_try_absorb_phase_b(
    phase_a: Optional[dict[str, Any]],
    entries: list[dict[str, Any]],
    blocked: list[str],
) -> tuple[
    Optional[dict[str, Any]],
    Optional[dict[str, Any]],
    list[dict[str, Any]],
    list[str],
    Optional[float],
    bool,
]:
    """Read host Phase B sidecar; score gate from settle evidence (not Phase A alone)."""
    if phase_a is None or not phase_a.get("fire_ok"):
        return None, phase_a, entries, blocked, None, False
    phase_b = _cap001_load_json_sidecar(_cap001_phase_b_sidecar_path())
    if phase_b is None:
        return None, phase_a, entries, blocked, None, False
    ok, reason = _cap001_validate_phase_b_settle(phase_a, phase_b)
    if not ok:
        blocked = list(blocked) + [f"cap001_phase_b_invalid:{reason}"]
        return phase_b, phase_a, entries, blocked, None, False
    entries = _cap001_apply_phase_b_to_entries(phase_a, phase_b, entries)
    act_settled = float(
        phase_b.get("settle_observed_at")
        or phase_b.get("host_poll_at")
        or time.time()
    )
    combined: dict[str, Any] = {
        "contract": CAP001_SETTLE_AFTER_YIELD_V1,
        "phase": "B",
        "settle_ok": True,
        "act_fired_at": phase_a.get("act_fired_at"),
        "canonical_still_path_abs": phase_a.get("canonical_still_path_abs"),
        "camera_label": phase_a.get("camera_label"),
        "phase_a": phase_a,
        "phase_b": phase_b,
    }
    blocked = [
        b
        for b in blocked
        if b != "cap001_phase_b_settle_pending_after_mcp_yield"
    ]
    _log("cap001 Phase B absorbed into gate scoring", {"path": combined.get("canonical_still_path_abs")})
    return phase_b, combined, entries, blocked, act_settled, True


def _cap001_phase_a_stamp(
    *,
    cam_label: str,
    canonical_path_abs: str,
    act_fired_at: Optional[float],
    fire_ok: bool,
    fire_error: Optional[str],
    methods: list[str],
    lit_aim_prep: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Conductor-readable Phase B inputs (host poll after MCP yield)."""
    stamp: dict[str, Any] = {
        "contract": CAP001_SETTLE_AFTER_YIELD_V1,
        "phase": "A",
        "camera_label": cam_label,
        "canonical_still_path_abs": canonical_path_abs,
        "act_fired_at": act_fired_at,
        "fire_ok": fire_ok,
        "fire_error": fire_error,
        "methods": methods,
    }
    if lit_aim_prep is not None:
        stamp[CAP001_DARK_STILL_LIT_AIM_V1] = lit_aim_prep
    return stamp


def _cap001_shot2_for_cabin_close() -> Optional[dict[str, Any]]:
    for shot in common.SHOTS:
        if shot.get("id") == "shot2":
            return shot
    return common._shot_def("shot2")  # type: ignore[attr-defined]


def _cap001_cabin_aim_bounds_centroid() -> Optional[list[float]]:
    inv = common.inventory_homestead_in_level("shot2")
    bounds = (
        inv.get("aim_bounds")
        or inv.get("framing_bounds")
        or inv.get("homestead_bounds")
    )
    if bounds and bounds.get("centroid"):
        return list(bounds["centroid"])
    return None


def _cap001_prepare_one_cam_lit_aim_before_fire(
    cam,
    cam_label: str,
) -> tuple[list[str], list[str], dict[str, Any]]:
    """Night stack + exposure, then lit/aim/warm (pre-AL one-cam)."""
    methods: list[str] = [
        CAP001_DARK_STILL_NIGHT_STACK_V2,
        CAP001_DARK_STILL_LIT_AIM_V1,
    ]
    blocked: list[str] = []
    prep_meta: dict[str, Any] = {
        "camera_label": cam_label,
        "has_v2": True,
        CAP001_DARK_STILL_NIGHT_STACK_V2: True,
    }

    homestead_centroid = _cap001_cabin_aim_bounds_centroid()
    prep_meta["homestead_centroid"] = homestead_centroid
    night_env = common.apply_pa_e_homestead_night_environment(
        LOG_PREFIX,
        reseed_tmp_fixtures=True,
        homestead_centroid=homestead_centroid,
        mrq_pie_shot=False,
    )
    prep_meta["night_environment"] = night_env
    lighting_verify = night_env.get("lighting_stack_verify") or {}
    prep_meta["lighting_stack_verify"] = lighting_verify
    prep_meta["lighting_stack_stack_ok"] = lighting_verify.get("stack_ok")
    prep_meta["environment_preconditions_ok"] = night_env.get("environment_preconditions_ok")
    methods.append("apply_pa_e_homestead_night_environment")
    if not night_env.get("environment_preconditions_ok"):
        blocked.append("cap001_night_stack_preconditions_not_ok")

    import vnp_night_tune_and_evidence as vnp

    importlib.reload(vnp)
    exposure_cvars = vnp.apply_mrq_pie_night_exposure_cvars()
    prep_meta["exposure_cvars"] = exposure_cvars
    methods.append("apply_mrq_pie_night_exposure_cvars")

    view = common.apply_lit_game_view_for_capture()
    prep_meta["lit_game_view"] = view
    methods.append(f"apply_lit_game_view:{view.get('viewmode')}")

    if cam_label == "CAM_CabinClose":
        shot = _cap001_shot2_for_cabin_close()
        if shot is None:
            blocked.append("cap001_shot2_missing_design_bounce")
            prep_meta["aim_error"] = "shot2_def_missing"
        else:
            loc, rot, aim_meta = common.resolve_camera_transform(shot, cam)
            prep_meta["resolve_camera_transform"] = {
                k: aim_meta.get(k)
                for k in (
                    "pose_source",
                    "aim_after",
                    "aim_after_bounds_relocate",
                    "aim_before",
                    "camera_relocated_from_bounds",
                    "camera_relocated_wide_cabin_anchor",
                    "expected_framing",
                )
            }
            aim_after = (
                aim_meta.get("aim_after")
                or aim_meta.get("aim_after_bounds_relocate")
                or aim_meta.get("aim_after_doc_fallback")
                or {}
            )
            prep_meta["aim_ok"] = bool(aim_after.get("aim_ok"))
            prep_meta["forward_ray_hits_dress_aabb"] = aim_after.get(
                "forward_ray_hits_dress_aabb"
            )
            inv = aim_meta.get("prove_loop_step1_inventory") or {}
            prep_meta["aim_bounds_ok"] = inv.get("aim_bounds_ok")
            if not inv.get("aim_bounds_ok"):
                blocked.append("cap001_aim_bounds_missing_cabin_dress_labels")
            elif not prep_meta.get("aim_ok"):
                blocked.append("cap001_cabin_aim_not_ok")
                if aim_after.get("forward_ray_hits_dress_aabb") is False:
                    blocked.append("cap001_forward_ray_miss_dress_aabb")
            sync = common.sync_editor_viewport_to_camera(cam, loc, rot)
            prep_meta["viewport_sync"] = sync
            methods.append(f"sync_editor_viewport:{sync.get('viewport_api')}")
            _pilot_camera(cam)
    else:
        _pilot_camera(cam)
        prep_meta["aim_skipped"] = "non_CAM_CabinClose_one_cam_label"

    _focus_ps_c_viewport()
    cv = _load_capture_viewport()
    if cv._finish_loading_before_screenshot():
        methods.append("AutomationLibrary.finish_loading_before_screenshot")
    cv._settle_pump_only(frames=PS_C_INTER_SHOT_SETTLE_FRAMES)
    methods.append(f"slate_warm_pump_frames:{PS_C_INTER_SHOT_SETTLE_FRAMES}")
    prep_meta["slate_warm_frames"] = PS_C_INTER_SHOT_SETTLE_FRAMES
    return methods, blocked, prep_meta


def _ps_c_one_cam_phase_a_fire_and_return(
    world,
    cam_label: str,
    stills_dir: str,
) -> tuple[
    list[dict[str, Any]],
    float,
    Optional[float],
    Optional[str],
    list[str],
    dict[str, Any],
]:
    """CAP001 Phase A: one AL fire, stamp act_fired_at + path, return (no in-script PNG wait)."""
    blocked: list[str] = []
    act_start = time.time()
    path = common.abs_path(_ps_c_canonical_still_path(cam_label))
    _ = stills_dir
    _ = world
    cam = _find_actor_label(cam_label)
    act_fired_at: Optional[float] = None
    fire_error: Optional[str] = None

    if not cam:
        fire_error = "camera_missing"
        blocked.append(f"one_cam_camera_missing:{cam_label}")
        stamp = _cap001_phase_a_stamp(
            cam_label=cam_label,
            canonical_path_abs=path,
            act_fired_at=None,
            fire_ok=False,
            fire_error=fire_error,
            methods=["CAP001_SETTLE_AFTER_YIELD_V1:phase_a_fire_only"],
        )
        return [], act_start, None, fire_error, blocked, stamp

    prep_methods, prep_blocked, lit_aim_prep = _cap001_prepare_one_cam_lit_aim_before_fire(
        cam, cam_label
    )
    blocked.extend(prep_blocked)
    _purge_ps_c_still_png(path)
    methods: list[str] = ["CAP001_SETTLE_AFTER_YIELD_V1:phase_a_fire_only"]
    methods.extend(prep_methods)

    act_fired_at = time.time()
    ok, al_methods, _task = _automation_abs_screenshot_one_invoke(path, cam)
    methods.extend(al_methods)
    if not ok:
        act_fired_at = None
        fire_error = "automation_invoke_failed"
        blocked.append("one_cam_automation_invoke_failed")

    stamp = _cap001_phase_a_stamp(
        cam_label=cam_label,
        canonical_path_abs=path,
        act_fired_at=act_fired_at,
        fire_ok=ok,
        fire_error=fire_error,
        methods=methods,
        lit_aim_prep=lit_aim_prep,
    )
    entry: dict[str, Any] = {
        "camera_label": cam_label,
        "path": path,
        "methods": methods,
        "act_fired_at": act_fired_at,
        "canonical_still_path_abs": path,
        "cap001_dark_still_lit_aim_v1": lit_aim_prep,
        "capture_outcome": OUTCOME_SOFT if ok else OUTCOME_SOFT,
        "counts_toward_gate": False,
        "fresh_this_act": False,
        "file_exists": False,
        "exists": False,
        "on_disk": False,
        "note": "cap001_phase_a_pending_host_settle_after_mcp_yield",
    }
    if fire_error:
        entry["error"] = fire_error

    _log("one-cam Phase A fire+stamp+return", stamp)
    driver_err = fire_error if not ok else None
    return [entry], act_start, None, driver_err, blocked, stamp


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
        self.stills_dir = common.abs_path(stills_dir)
        self.gate_context = gate_context
        self._still_labels = tuple(gate_context.get("still_labels") or _still_labels())
        self._wait_file_sec = float(
            gate_context.get("wait_file_sec")
            or (
                PS_C_ONE_CAM_WAIT_FILE_SEC
                if gate_context.get("prove_mode") == "one_cam"
                else PS_C_WAIT_FILE_SEC
            )
        )
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
        self._al_second_round = False
        self._pending_automation_tasks: list[Any] = []

    def _track_automation_task(self, task: Any) -> None:
        if task is not None:
            self._pending_automation_tasks.append(task)

    def _uses_ps_placement_cam(self) -> bool:
        return self._cam_label.startswith(PS_C_PS_CAM_PREFIX)

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
        if self.shot_index >= len(self._still_labels):
            self.phase = _PsCStillsPhase.WRITE_MANIFEST
            return
        self._cam_label = self._still_labels[self.shot_index]
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
        self._al_second_round = False
        self.phase = _PsCStillsPhase.CAPTURE_PENDING

    def _reset_wait_deadline(self) -> None:
        now = time.time()
        shots_left = max(1, len(self._still_labels) - self.shot_index)
        remaining_drive = max(0.0, self._drive_deadline - now)
        floor = 16.0 if self._uses_ps_placement_cam() else 12.0
        per_shot = min(
            self._wait_file_sec,
            max(floor, (remaining_drive - 1.5) / shots_left),
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
        self._cv._finish_loading_before_screenshot()
        one_cam = self.gate_context.get("prove_mode") == "one_cam"
        if one_cam:
            # One-cam bite: proven shotlist path — AutomationLibrary abs only (no HighResShot ladder).
            if not self._al_invoked:
                _ok_al, al_methods, task = _automation_abs_screenshot(self._filepath, self._cam)
                self._methods.extend(al_methods)
                self._task = task
                self._track_automation_task(task)
                self._al_invoked = True
                self._methods.append("one_cam:AutomationLibrary_abs_only")
        elif self._uses_ps_placement_cam():
            # PS placement cams: doc-ordered HighResShot abs first, then AL (viewport pilot).
            if self._console_cmd_index == 0:
                self._invoke_console_ladder_step()
            if not self._al_invoked:
                _ok_al, al_methods, task = _automation_abs_screenshot(self._filepath, self._cam)
                self._methods.extend(al_methods)
                self._task = task
                self._track_automation_task(task)
                self._al_invoked = True
                self._methods.append("ps_cam:console_then_AutomationLibrary_abs")
        elif not self._al_invoked:
            _ok_al, al_methods, task = _automation_abs_screenshot(self._filepath, self._cam)
            self._methods.extend(al_methods)
            self._task = task
            self._track_automation_task(task)
            self._al_invoked = True
            self._methods.append("primary:AutomationLibrary_abs")
        else:
            self._invoke_console_ladder_step()
        self._cv._settle_pump_only(frames=4)
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
            if self.gate_context.get("prove_mode") == "one_cam":
                pass
            elif self._console_cmd_index < self._console_cmd_total:
                if self._invoke_console_ladder_step():
                    self._reset_wait_deadline()
            elif not self._al_invoked:
                self.phase = _PsCStillsPhase.CAPTURE_PENDING
                self._invoke_capture_once()
                return
        if time.time() >= self._wait_deadline:
            drive_left = self._drive_deadline - time.time()
            if self.gate_context.get("prove_mode") != "one_cam":
                if (
                    self._console_cmd_index < self._console_cmd_total
                    and drive_left > 4.0
                ):
                    if self._invoke_console_ladder_step():
                        self._reset_wait_deadline()
                        return
            if not self._al_second_round and drive_left > 6.0:
                self._al_second_round = True
                self._al_invoked = False
                self._task = None
                self.phase = _PsCStillsPhase.CAPTURE_PENDING
                return
            resolved = _find_fresh_ps_still_path(self._filepath, self._since)
            if (
                not resolved
                and os.path.isfile(self._filepath)
                and _mtime_at_least(self._filepath, self._since)
            ):
                try:
                    if os.path.getsize(self._filepath) >= common.MIN_BYTES:
                        resolved = self._filepath
                except OSError:
                    pass
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
        if self.shot_index < len(self._still_labels):
            self._settle_frames_left = PS_C_INTER_SHOT_SETTLE_FRAMES
            self.phase = _PsCStillsPhase.INTER_SHOT_SETTLE
        else:
            self.phase = _PsCStillsPhase.WRITE_MANIFEST

    def _finish_all(self) -> None:
        if self.phase == _PsCStillsPhase.DONE:
            return
        self.phase = _PsCStillsPhase.DONE
        _log(
            "stills driver finished pending gate settle",
            {
                "shots": len(self.entries),
                "drive_ticks": self._drive_ticks,
                "pending_tasks": len(self._pending_automation_tasks),
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
        while self.shot_index < len(self._still_labels):
            label = self._still_labels[self.shot_index]
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
    act_end: Optional[float] = None,
) -> dict[str, Any]:
    filepath = common.abs_path(filepath)
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
    on_disk = os.path.isfile(filepath)
    entry["on_disk"] = on_disk
    if not on_disk:
        entry["file_exists"] = False
        entry["exists"] = False
        entry["capture_outcome"] = OUTCOME_SOFT
        entry["note"] = "png_missing_black_or_path_soft_fail"
        entry["counts_toward_gate"] = False
        return entry
    try:
        entry["file_mtime"] = os.path.getmtime(filepath)
        entry["bytes"] = os.path.getsize(filepath)
    except OSError:
        entry["file_mtime"] = None
    if not _ps_still_counts_for_gate(filepath, since, act_end):
        entry["file_exists"] = False
        entry["exists"] = False
        entry["fresh_this_act"] = False
        entry["counts_toward_gate"] = False
        if not _mtime_at_least(filepath, since):
            entry["capture_outcome"] = OUTCOME_SOFT
            entry["note"] = "stale_png_reuse_mtime_before_capture"
        elif act_end is not None and not _mtime_in_act_window(filepath, since, act_end):
            entry["capture_outcome"] = OUTCOME_SOFT
            entry["note"] = "post_settle_png_landing_excluded_from_gate"
        else:
            entry["capture_outcome"] = OUTCOME_SOFT
            entry["note"] = "file_too_small_or_outside_act_window"
        return entry
    entry["file_exists"] = True
    entry["exists"] = True
    size = int(entry.get("bytes") or os.path.getsize(filepath))
    entry["bytes"] = size
    lum, lum_src = common.mean_luminance(filepath)
    entry["mean_luminance"] = lum
    entry["luminance_source"] = lum_src
    if size < common.MIN_BYTES:
        entry["capture_outcome"] = OUTCOME_SOFT
        entry["note"] = "file_too_small"
        entry["fresh_this_act"] = False
        entry["counts_toward_gate"] = False
        entry["file_exists"] = False
        entry["exists"] = False
        return entry
    if lum is None or (lum is not None and lum < common.MIN_MEAN_LUMINANCE):
        entry["capture_outcome"] = OUTCOME_SOFT
        entry["note"] = "black_or_dark_still_soft_fail_not_closed_without_arrange_miss"
        entry["fresh_this_act"] = False
        entry["counts_toward_gate"] = False
        return entry
    entry["fresh_this_act"] = True
    entry["counts_toward_gate"] = True
    entry["capture_outcome"] = OUTCOME_PASS
    if resolved_on_disk:
        entry["resolved_path"] = resolved_on_disk
    return entry


def _write_stills_manifest(
    entries: list[dict[str, Any]],
    stills_dir: str,
    *,
    act_since: Optional[float] = None,
    act_end: Optional[float] = None,
    cap001_phase_a: Optional[dict[str, Any]] = None,
) -> str:
    stills_dir = _ps_c_stills_dir_abs()
    rows = entries
    if act_since is not None and cap001_phase_a is None:
        rows = _reconcile_still_entries_from_disk(
            entries, act_since, stills_dir, act_end=act_end
        )
    for ent in rows:
        path = common.abs_path(str(ent.get("path") or ""))
        if path and act_since is not None:
            ent["path"] = path
            in_window = _ps_still_counts_for_gate(path, act_since, act_end)
            ent["on_disk"] = os.path.isfile(path)
            ent["file_exists"] = in_window
            ent["exists"] = in_window
            ent["counts_toward_gate"] = bool(in_window and ent.get("fresh_this_act"))
            if ent["on_disk"] and not in_window:
                try:
                    ent["bytes"] = os.path.getsize(path)
                    ent["file_mtime"] = os.path.getmtime(path)
                except OSError:
                    pass
    manifest = {
        "version": 1,
        "generated_at_iso": datetime.now(timezone.utc).isoformat(),
        "capture_act_started_at": act_since,
        "capture_act_settled_at": act_end,
        "capture_path": (
            "slate pre-tick: purge stale PNG; PS_* = console HighResShot abs then AL; CAM_* = AL then "
            "console ladder on ticks; absolute Saved/ps_stills/; gate counts disk-fresh only"
        ),
        "wait_mechanism": PS_C_SLATE_MECHANISM,
        "resolution": [STILL_RES_X, STILL_RES_Y],
        "stills": rows,
    }
    if cap001_phase_a is not None:
        manifest["cap001_settle_after_yield_v1"] = cap001_phase_a
        manifest["act_fired_at"] = cap001_phase_a.get("act_fired_at")
        manifest["canonical_still_path_abs"] = cap001_phase_a.get("canonical_still_path_abs")
    manifest_path = os.path.join(stills_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, default=str)
    return manifest_path


def _automation_abs_screenshot(filepath: str, cam) -> tuple[bool, list[str], Any]:
    """Absolute-path AutomationLibrary (PL-D / capture_shotlist_viewport pattern)."""
    methods: list[str] = []
    cv = _load_capture_viewport()
    dest_abs = cv._ensure_abs_dest(filepath)
    ue_path = cv._path_for_ue(dest_abs)
    methods.append(f"al_canonical_dest:{ue_path}")
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
    stills_act_started_at: Optional[float] = None,
    stills_act_settled_at: Optional[float] = None,
    stills_disk_audit: Optional[dict[str, Any]] = None,
    prove_mode: str = "full",
    one_cam_label: Optional[str] = None,
    cap001_phase_a: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    stills_required = len(_still_labels())
    one_cam_bite = prove_mode == "one_cam"
    capture_outcomes = [e.get("capture_outcome", OUTCOME_SOFT) for e in still_entries]
    stills_manifest_fresh = sum(
        1 for e in still_entries if e.get("counts_toward_gate") or e.get("fresh_this_act")
    )
    stills_stale_manifest = sum(
        1
        for e in still_entries
        if e.get("file_exists") and not (e.get("fresh_this_act") or e.get("counts_toward_gate"))
    )
    disk_fresh = (
        int(stills_disk_audit.get("fresh_count", 0)) if stills_disk_audit else stills_manifest_fresh
    )
    stills_present = disk_fresh
    gate_count_matches_disk = stills_manifest_fresh == disk_fresh

    if metrics is not None:
        placement_outcome = metrics.get("placement_outcome", OUTCOME_CLOSED)
    elif one_cam_bite:
        placement_outcome = OUTCOME_SOFT
    else:
        placement_outcome = OUTCOME_CLOSED
    if pre_closed:
        placement_outcome = OUTCOME_CLOSED

    metrics_ok = metrics is not None and placement_outcome in (OUTCOME_PASS, OUTCOME_SOFT)
    ready_for_ps_d = (
        not pre_closed
        and not stills_in_progress
        and stills_present >= stills_required
        and gate_count_matches_disk
        and (one_cam_bite or metrics_ok)
    )
    cap001_settled_phase_b = (
        cap001_phase_a is not None
        and cap001_phase_a.get("phase") == "B"
        and bool(cap001_phase_a.get("settle_ok"))
    )
    cap001_phase_a_pending = (
        one_cam_bite
        and cap001_phase_a is not None
        and bool(cap001_phase_a.get("fire_ok"))
        and not cap001_settled_phase_b
    )
    if cap001_phase_a_pending:
        blocked = list(blocked) + ["cap001_phase_b_settle_pending_after_mcp_yield"]

    if not ready_for_ps_d and not stills_in_progress and not cap001_phase_a_pending:
        if metrics is None and not one_cam_bite:
            blocked = list(blocked) + ["metrics_not_written"]
        if stills_present < stills_required:
            blocked = list(blocked) + [f"stills_incomplete:{stills_present}/{stills_required}"]
        if not gate_count_matches_disk:
            blocked = list(blocked) + [
                f"stills_gate_disk_mismatch:manifest={stills_manifest_fresh}/disk={disk_fresh}"
            ]
        if stills_stale_manifest > 0:
            blocked = list(blocked) + [f"stills_stale_manifest_rows:{stills_stale_manifest}"]

    gate: dict[str, Any] = {
        "version": 1,
        "track": "PS-C",
        "prove_mode": prove_mode,
        "one_cam_label": one_cam_label,
        "level_path": common.LEVEL_PATH,
        "preconditions": {
            "dress_count": dress_count,
            "pa_d_count": pa_d_count,
            "ps_arrange_gate_ready_for_ps_c": bool(arrange_gate.get("ready_for_ps_c")),
        },
        "placement_outcome": placement_outcome,
        "stills_present_count": stills_present,
        "stills_fresh_disk_count": disk_fresh,
        "stills_fresh_manifest_count": stills_manifest_fresh,
        "stills_stale_manifest_count": stills_stale_manifest,
        "gate_count_matches_disk": gate_count_matches_disk,
        "stills_required_count": stills_required,
        "stills_capture_outcomes": capture_outcomes,
        "stills_capture_act_started_at": stills_act_started_at,
        "stills_capture_act_settled_at": stills_act_settled_at,
        "stills_disk_audit": stills_disk_audit,
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
            "ready_for_ps_d = metrics + still files on disk (full); one_cam bite = 1/1 Act-window still only. "
            "PS-D is Lead eyeball vs benchmarks. Black/dark stills → soft_fail on capture, not closed_fail if Arrange gate was ready."
        ),
    }
    if one_cam_bite:
        gate["one_cam_bite_pass"] = ready_for_ps_d
        gate["one_cam_stills_required_count"] = stills_required
    if cap001_phase_a is not None:
        gate["cap001_settle_after_yield_v1"] = cap001_phase_a
        gate["act_fired_at"] = cap001_phase_a.get("act_fired_at")
        gate["canonical_still_path_abs"] = cap001_phase_a.get("canonical_still_path_abs")
        if cap001_settled_phase_b:
            gate["cap001_phase_b_sidecar_path"] = _cap001_phase_b_sidecar_path()
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
    stills_dir = _ps_c_stills_dir_abs()
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


def prove_ps_placement(
    *,
    skip_stills: bool = False,
    one_cam_label: Optional[str] = None,
) -> dict[str, Any]:
    """PS-C entry: preconditions, metrics, stills, gate sidecar."""
    global _ACTIVE_PS_C_STILLS
    blocked: list[str] = []
    pre_closed = False

    prove_mode_info = _apply_prove_still_label_set(one_cam_label)
    prove_mode = str(prove_mode_info.get("prove_mode") or "full")
    one_cam_active = prove_mode_info.get("one_cam_label")
    if prove_mode_info.get("error"):
        blocked.append(str(prove_mode_info["error"]))
        pre_closed = True
        _log("prove blocked: invalid one-cam label", prove_mode_info)
    elif prove_mode == "one_cam":
        _log("prove one-cam bite Act", prove_mode_info)
    else:
        label_drift = _prove_still_labels_drift_from_design()
        if label_drift:
            blocked.append(label_drift)
            pre_closed = True
            _log("prove blocked: still camera labels ≠ Design handoff", {"reason": label_drift})

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

    arrange_gate, arrange_blocked, cameras_ready = _ensure_arrange_gate()
    blocked.extend(arrange_blocked)
    if not cameras_ready:
        pre_closed = True
        blocked.append("prove_closed_fail_inventory_cameras_before_act")
    if any(b.startswith("arrange_failed:") for b in arrange_blocked):
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

    if not pre_closed and dress_bounds and prove_mode != "one_cam":
        metrics = _compute_metrics(world=world, dress_bounds=dress_bounds, island_actor=island)
        os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2, default=str)
        _log("wrote ps_placement_metrics.json", {"path": metrics_path})
    elif prove_mode == "one_cam" and not pre_closed:
        _log("one-cam bite: skipping full placement metrics (still writer isolate)")

    stills_in_progress = False
    driver_error: Optional[str] = None
    stills_act_started_at: Optional[float] = None
    stills_act_settled_at: Optional[float] = None
    stills_disk_audit: Optional[dict[str, Any]] = None
    stills_dir = _ps_c_stills_dir_abs()
    cap001_phase_a: Optional[dict[str, Any]] = None

    if skip_stills:
        blocked.append("stills_skipped_by_flag")
    elif not pre_closed and prove_mode == "one_cam":
        bite_label = str(one_cam_active or _still_labels()[0])
        cap001_phase_b: Optional[dict[str, Any]] = None
        if _cap001_env_phase_b_absorb_only():
            cap001_phase_a = _cap001_load_phase_a_from_saved_gate()
            if cap001_phase_a is None:
                blocked.append("cap001_phase_b_absorb_missing_phase_a_gate")
            still_entries = _cap001_load_still_entries_from_manifest()
            stills_act_started_at = None
            manifest_existing = _cap001_load_json_sidecar(
                os.path.join(stills_dir, "manifest.json")
            )
            if manifest_existing:
                stills_act_started_at = manifest_existing.get("capture_act_started_at")
            if stills_act_started_at is None and cap001_phase_a:
                stills_act_started_at = float(cap001_phase_a.get("act_fired_at") or time.time())
            driver_error = None
            _log("one-cam CAP001 Phase B absorb-only (no AL re-fire)", {"label": bite_label})
        else:
            (
                still_entries,
                stills_act_started_at,
                stills_act_settled_at,
                driver_error,
                cap_blocked,
                cap001_phase_a,
            ) = _ps_c_one_cam_phase_a_fire_and_return(world, bite_label, stills_dir)
            blocked.extend(cap_blocked)
            if driver_error:
                blocked.append(f"stills_driver_failed:{driver_error}")
        (
            cap001_phase_b,
            cap001_combined,
            still_entries,
            blocked,
            phase_b_act_end,
            _phase_b_absorbed,
        ) = _cap001_try_absorb_phase_b(cap001_phase_a, still_entries, blocked)
        if cap001_combined is not None:
            cap001_phase_a = cap001_combined
        if phase_b_act_end is not None:
            stills_act_settled_at = phase_b_act_end
        manifest_path = _write_stills_manifest(
            still_entries,
            stills_dir,
            act_since=stills_act_started_at,
            act_end=stills_act_settled_at,
            cap001_phase_a=cap001_phase_a,
        )
        stills_disk_audit = _audit_ps_stills_disk(
            stills_dir, stills_act_started_at, stills_act_settled_at
        )
    elif not pre_closed:
        drive_timeout = PS_C_DRIVE_TIMEOUT_SEC
        gate_context = {
            "blocked": blocked,
            "pre_closed": pre_closed,
            "dress_count": dress_count,
            "pa_d_count": pa_d_count,
            "arrange_gate": arrange_gate,
            "dress_path": dress_path,
            "metrics": metrics,
            "metrics_path": metrics_path,
            "prove_mode": prove_mode,
            "still_labels": list(_still_labels()),
            "wait_file_sec": PS_C_WAIT_FILE_SEC,
        }
        started, err = _start_ps_c_stills_async(world, gate_context)
        if started:
            orch = _ACTIVE_PS_C_STILLS
            if orch is not None:
                for lbl in orch._still_labels:
                    _purge_ps_c_still_png(_resolve_still_path(stills_dir, lbl))
                completed = _drive_ps_c_stills_orchestrator(orch, drive_timeout)
                stills_act_started_at = orch._act_started_at
                still_entries, stills_act_settled_at, settle_blocked, paths_ready = (
                    _ps_c_settle_stills_before_gate(
                        orch,
                        stills_dir,
                        stills_act_started_at,
                        PS_C_GATE_SETTLE_SEC,
                    )
                )
                blocked.extend(settle_blocked)
                if paths_ready and stills_act_settled_at is not None:
                    still_entries = _reconcile_still_entries_from_disk(
                        list(orch.entries),
                        stills_act_started_at,
                        stills_dir,
                        act_end=stills_act_settled_at,
                    )
                manifest_path = _write_stills_manifest(
                    still_entries,
                    stills_dir,
                    act_since=stills_act_started_at,
                    act_end=stills_act_settled_at,
                )
                stills_disk_audit = _audit_ps_stills_disk(
                    stills_dir, stills_act_started_at, stills_act_settled_at
                )
                driver_error = orch._driver_error
                if not completed:
                    blocked = list(blocked) + ["stills_driver_timeout"]
                try:
                    orch._unregister_tick()
                    orch._disarm_keep_alive()
                except Exception:
                    pass
                _ACTIVE_PS_C_STILLS = None
        else:
            driver_error = err
            blocked.append(f"stills_driver_failed:{err}")

    if stills_act_started_at is not None and stills_disk_audit is None:
        stills_disk_audit = _audit_ps_stills_disk(
            stills_dir, stills_act_started_at, stills_act_settled_at
        )

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
        stills_act_started_at=stills_act_started_at,
        stills_act_settled_at=stills_act_settled_at,
        stills_disk_audit=stills_disk_audit,
        prove_mode=prove_mode,
        one_cam_label=one_cam_active if isinstance(one_cam_active, str) else None,
        cap001_phase_a=cap001_phase_a,
    )
    gate["gate_written_at"] = time.time()
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
    bite_label = _resolve_one_cam_label_from_env_or_argv()
    gate = prove_ps_placement(one_cam_label=bite_label)
    print(
        json.dumps(
            {
                "ok": gate.get("ready_for_ps_d"),
                "prove_mode": gate.get("prove_mode"),
                "one_cam_label": gate.get("one_cam_label"),
                "one_cam_bite_pass": gate.get("one_cam_bite_pass"),
                "act_fired_at": gate.get("act_fired_at"),
                "canonical_still_path_abs": gate.get("canonical_still_path_abs"),
                "cap001_settle_after_yield_v1": gate.get("cap001_settle_after_yield_v1"),
                "stills_present_count": gate.get("stills_present_count"),
                "stills_required_count": gate.get("stills_required_count"),
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

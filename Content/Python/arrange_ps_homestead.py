# arrange_ps_homestead.py
# PS-B: Idempotent placement-stills camera Arrange on L_VS_MVP_Markers (homestead kit only).
# Run in Unreal Editor or MCP: execute_python_script("arrange_ps_homestead.py").
# Chain (DESKTOP): place_vs_mvp_markers.py → place_vs_mvp_dress.py → place_vs_mvp_pa_d.py → this script.
# Does not capture stills (PS-C) or run MRQ — writes Saved/ps_dress_bounds.json + Saved/ps_arrange_gate.json.

from __future__ import annotations

import importlib
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Optional

try:
    import unreal
except ImportError:
    print("arrange_ps_homestead: Run inside Unreal Editor.")
    sys.exit(1)

import pa_e_shotlist_common as common

importlib.reload(common)

LOG_PREFIX = "PS Arrange:"
PS_ACTOR_FOLDER = "VS_MVP/PS"
DRESS_BOUNDS_MARGIN_UU = 50
INCLUDE_PS_SHRINE_READ = False  # Set True to spawn PS_Shrine_Read (optional P0+ view).

JSON_CAM_LABELS = (
    "CAM_CabinClose",
    "CAM_GlideDepart",
    "CAM_Hero",
    "CAM_LandingDay",
    "CAM_PortalNight",
)

RELOCATE_CAM_LABELS = ("CAM_Hero", "CAM_CabinClose")
MRQ_OPTIONAL_LABELS = ("PA_E_MRQ_shot1", "PA_E_MRQ_shot2")

NEW_PS_CAMERA_LABELS = (
    "PS_N_HighIso",
    "PS_E_HighIso",
    "PS_S_HighIso",
    "PS_W_HighIso",
    "PS_Cliff_Underside",
    "PS_Path_Corridor",
    "PS_Garden_Close",
)

FORBIDDEN_ALIAS_LABELS = ("Shot1", "Shot2", "CAM_CabinGarden")

HIGH_ISO_DIRECTIONS = ("N", "E", "S", "W")
HIGH_ISO_RING_SCALE = 2.2
HIGH_ISO_RING_MIN_UU = 4200.0
HIGH_ISO_HEIGHT_ABOVE_CENTER_UU = 3200.0
HIGH_ISO_PITCH_BIAS_DEG = -38.0

GARDEN_CLOSE_STANDOFF_UU = (420.0, -780.0, 520.0)
CLIFF_UNDERSIDE_Z_OFFSET_UU = -900.0
CLIFF_UNDERSIDE_HORIZ_UU = 1400.0
PATH_CORRIDOR_HEIGHT_UU = 420.0
PATH_CORRIDOR_STANDOFF_UU = 1100.0
SHRINE_STANDOFF_UU = (1800.0, -1200.0, 650.0)


def _log(msg: str, data: Optional[dict[str, Any]] = None) -> None:
    line = f"{LOG_PREFIX} {msg}"
    if data:
        line += " " + json.dumps(data, default=str)
    unreal.log(line)


def _project_saved_path(filename: str) -> str:
    return common.abs_path(os.path.join(common.project_dir(), "Saved", filename))


def _assert_markers_world() -> dict[str, Any]:
    status = common.editor_world_markers_status()
    if not status.get("ok"):
        raise RuntimeError(
            "Editor world must contain L_VS_MVP_Markers — load "
            f"{common.LEVEL_PATH} before arrange_ps_homestead.py. "
            f"Got: {status}"
        )
    return status


def _all_level_actors() -> list:
    return [a for a in unreal.EditorLevelLibrary.get_all_level_actors() if a]


def _find_actor_exact_label(label: str):
    for a in _all_level_actors():
        if common.actor_label(a) == label:
            return a
    return None


def _count_label_prefix(prefix: str) -> int:
    return sum(1 for a in _all_level_actors() if common.actor_label(a).startswith(prefix))


def _actors_for_dress_bounds(*, include_pa_d: bool = True) -> list:
    actors: list = []
    for a in _all_level_actors():
        label = common.actor_label(a)
        if label.startswith(common.DRESS_LABEL_PREFIX):
            actors.append(a)
        elif include_pa_d and label.startswith("PA_D_"):
            actors.append(a)
    return actors


def _ensure_camera_actor(label: str, loc, rot) -> tuple[Any, dict[str, Any]]:
    meta: dict[str, Any] = {"label": label}
    existing = _find_actor_exact_label(label)
    cam_class = getattr(unreal, "CineCameraActor", None) or unreal.CameraActor
    if existing:
        try:
            existing.set_actor_location(loc, False, False)
            existing.set_actor_rotation(rot, False)
            try:
                existing.set_folder_path(PS_ACTOR_FOLDER)
            except Exception:
                pass
        except Exception as e:
            meta["update_error"] = str(e)
        meta["action"] = "updated"
        return existing, meta
    spawned = unreal.EditorLevelLibrary.spawn_actor_from_class(cam_class, loc, rot)
    if spawned:
        try:
            spawned.set_actor_label(label)
            spawned.set_folder_path(PS_ACTOR_FOLDER)
        except Exception:
            pass
        meta["action"] = "spawned"
    else:
        meta["action"] = "spawn_failed"
    return spawned, meta


def _high_iso_offset(direction: str, ring: float) -> tuple[float, float]:
    if direction == "N":
        return 0.0, ring
    if direction == "E":
        return ring, 0.0
    if direction == "S":
        return 0.0, -ring
    if direction == "W":
        return -ring, 0.0
    raise ValueError(f"unknown iso direction {direction}")


def _pose_high_iso(direction: str, dress_bounds: dict[str, Any]) -> tuple[Any, Any, dict[str, Any]]:
    centroid = dress_bounds["centroid"]
    extent = dress_bounds["extent"]
    cx, cy, cz = float(centroid[0]), float(centroid[1]), float(centroid[2])
    ring = max(float(extent[0]), float(extent[1])) * HIGH_ISO_RING_SCALE + HIGH_ISO_RING_MIN_UU
    height = cz + float(extent[2]) + HIGH_ISO_HEIGHT_ABOVE_CENTER_UU
    dx, dy = _high_iso_offset(direction, ring)
    loc = unreal.Vector(cx + dx, cy + dy, height)
    target = unreal.Vector(cx, cy, cz + float(extent[2]) * 0.35)
    rot = common.look_at_rotation(loc, target)
    rot = unreal.Rotator(pitch=HIGH_ISO_PITCH_BIAS_DEG, yaw=rot.yaw, roll=0.0)
    meta = {
        "pose_source": "dress_aabb_high_iso_ring",
        "direction": direction,
        "ring_uu": round(ring, 1),
        "camera_location": [loc.x, loc.y, loc.z],
        "target": [target.x, target.y, target.z],
    }
    return loc, rot, meta


def _pose_cliff_underside(dress_bounds: dict[str, Any]) -> tuple[Any, Any, dict[str, Any]]:
    cliff = _find_actor_exact_label("PA_D_SM_Cliff_LookoutFace")
    if cliff is None:
        cliff = _find_actor_exact_label("PA_D_SM_Cliff_CabinFace")
    meta: dict[str, Any] = {"pose_source": "cliff_actor_underside"}
    if cliff:
        origin, extent = cliff.get_actor_bounds(False)
        target = unreal.Vector(origin.x, origin.y, origin.z + extent.z * 0.4)
        loc = unreal.Vector(
            origin.x - CLIFF_UNDERSIDE_HORIZ_UU,
            origin.y,
            origin.z + CLIFF_UNDERSIDE_Z_OFFSET_UU,
        )
        meta["anchor_label"] = common.actor_label(cliff)
    else:
        bmin = dress_bounds.get("min") or [0.0, 0.0, 0.0]
        centroid = dress_bounds["centroid"]
        target = common._vector_from_list(centroid)
        loc = unreal.Vector(
            float(centroid[0]) - CLIFF_UNDERSIDE_HORIZ_UU,
            float(centroid[1]),
            float(bmin[2]) + CLIFF_UNDERSIDE_Z_OFFSET_UU,
        )
        meta["anchor_label"] = None
        meta["fallback"] = "dress_aabb_min_z"
    rot = common.look_at_rotation(loc, target)
    meta["camera_location"] = [loc.x, loc.y, loc.z]
    meta["target"] = [target.x, target.y, target.z]
    return loc, rot, meta


def _pose_path_corridor(dress_bounds: dict[str, Any]) -> tuple[Any, Any, dict[str, Any]]:
    stones = [
        a
        for a in _all_level_actors()
        if common.actor_label(a).startswith("PA_D_SM_PathStone")
    ]
    meta: dict[str, Any] = {"pose_source": "path_stone_midline"}
    if len(stones) >= 2:
        pts = [a.get_actor_location() for a in stones]
        mid = common._midpoint_xyz([[p.x, p.y, p.z] for p in pts])
        target = unreal.Vector(mid[0], mid[1], mid[2] + 80.0)
        loc = unreal.Vector(
            mid[0] + PATH_CORRIDOR_STANDOFF_UU,
            mid[1],
            mid[2] + PATH_CORRIDOR_HEIGHT_UU,
        )
        meta["path_stone_count"] = len(stones)
    else:
        centroid = dress_bounds["centroid"]
        target = common._vector_from_list(centroid)
        loc = unreal.Vector(
            float(centroid[0]) + PATH_CORRIDOR_STANDOFF_UU,
            float(centroid[1]),
            float(centroid[2]) + PATH_CORRIDOR_HEIGHT_UU,
        )
        meta["fallback"] = "dress_centroid"
    rot = common.look_at_rotation(loc, target)
    meta["camera_location"] = [loc.x, loc.y, loc.z]
    meta["target"] = [target.x, target.y, target.z]
    return loc, rot, meta


def _pose_garden_close(dress_bounds: dict[str, Any]) -> tuple[Any, Any, dict[str, Any]]:
    meta: dict[str, Any] = {"pose_source": "garden_close_standoff"}
    anchor = common.resolve_anchor_point(
        shot_id="shot2",
        primary_needles=common.SHOT2_CABIN_ANCHOR_NEEDLES,
        fallback_needles=common.SHOT2_CABIN_FOUNDATION_FALLBACK_NEEDLES,
        bounds_fallback=dress_bounds,
        meta=meta,
        prefer_single_actor=True,
    )
    if anchor is None:
        anchor = list(dress_bounds.get("centroid") or [0.0, 0.0, 0.0])
    ax, ay, az = anchor[0], anchor[1], anchor[2]
    ox, oy, oz = GARDEN_CLOSE_STANDOFF_UU
    target = unreal.Vector(ax + 90.0, ay + 60.0, az + 160.0)
    loc = unreal.Vector(ax + ox, ay + oy, az + oz)
    clamp_b = common._synthetic_anchor_bounds(anchor)
    loc = common._clamp_camera_pose_loc(loc, clamp_b, meta)
    rot = common.look_at_rotation(loc, target)
    meta["camera_location"] = [loc.x, loc.y, loc.z]
    meta["target"] = [target.x, target.y, target.z]
    return loc, rot, meta


def _pose_shrine_read(dress_bounds: dict[str, Any]) -> tuple[Any, Any, dict[str, Any]]:
    meta: dict[str, Any] = {"pose_source": "shrine_dress_anchor"}
    shrine = _find_actor_exact_label("DRESS_SM_Shrine_Homestead")
    if shrine is None:
        actors = common.find_actors_by_needles(("Shrine_Homestead", "SM_Shrine"), "shot2")
        shrine = actors[0] if actors else None
    if shrine:
        loc_s = shrine.get_actor_location()
        target = unreal.Vector(loc_s.x, loc_s.y, loc_s.z + 120.0)
        meta["anchor_label"] = common.actor_label(shrine)
    else:
        target = common._vector_from_list(dress_bounds["centroid"])
        meta["fallback"] = "dress_centroid"
    sx, sy, sz = SHRINE_STANDOFF_UU
    loc = unreal.Vector(target.x + sx, target.y + sy, target.z + sz)
    rot = common.look_at_rotation(loc, target)
    meta["camera_location"] = [loc.x, loc.y, loc.z]
    meta["target"] = [target.x, target.y, target.z]
    return loc, rot, meta


def _relocate_json_cameras(dress_bounds: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for shot in common.SHOTS:
        if shot.get("id") not in ("shot1", "shot2"):
            continue
        cam = common.find_camera(tuple(shot.get("camera_labels") or ()))
        loc, rot, pose_meta = common.resolve_camera_transform(shot, cam)
        entry: dict[str, Any] = {
            "shot_id": shot["id"],
            "camera_labels": list(shot.get("camera_labels") or []),
            "resolved_label": pose_meta.get("camera_label"),
            "pose_source": pose_meta.get("pose_source"),
        }
        if cam:
            err = common._apply_camera_transform(cam, loc, rot)
            entry["relocate"] = "updated" if not err else f"error:{err}"
            target = common._look_target_for_pose_meta(
                common._vector_from_list(dress_bounds["centroid"]), pose_meta
            )
            entry["aim"] = common.camera_forward_alignment(
                loc, rot, target, dress_bounds=dress_bounds, shot_id=shot["id"]
            )
        else:
            entry["relocate"] = "missing_in_level"
        results.append(entry)

        mrq_label = f"PA_E_MRQ_{shot['id']}"
        mrq = _find_actor_exact_label(mrq_label)
        if mrq:
            err = common._apply_camera_transform(mrq, loc, rot)
            results.append(
                {
                    "shot_id": shot["id"],
                    "camera_labels": [mrq_label],
                    "resolved_label": mrq_label,
                    "relocate": "updated" if not err else f"error:{err}",
                    "optional_mrq": True,
                }
            )
    return results


def _write_dress_bounds_json(dress_bounds: dict[str, Any], *, actor_count: int) -> str:
    payload: dict[str, Any] = {
        "version": 1,
        "level_path": common.LEVEL_PATH,
        "coordinate_space": "ue_world_uu",
        "dress_aabb": {
            "center": dress_bounds["centroid"],
            "extent": dress_bounds["extent"],
        },
        "dress_aabb_minmax": {
            "min": dress_bounds["min"],
            "max": dress_bounds["max"],
        },
        "margin_uu": DRESS_BOUNDS_MARGIN_UU,
        "anchors": {},
        "source": "arrange_ps_homestead",
        "generated_at_iso": datetime.now(timezone.utc).isoformat(),
        "dress_actor_count": actor_count,
        "actor_labels_sample": dress_bounds.get("actor_labels", [])[:20],
    }
    anchor = _find_actor_exact_label("ANCHOR_SM_Cabin")
    if anchor:
        loc = anchor.get_actor_location()
        payload["anchors"]["SM_Cabin"] = {
            "location_uu": [loc.x, loc.y, loc.z],
            "note": "ANCHOR_SM_Cabin in level",
        }
    path = _project_saved_path("ps_dress_bounds.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    _log("wrote ps_dress_bounds.json", {"path": path, "actor_count": actor_count})
    return path


def arrange_ps_homestead(*, include_shrine: bool = INCLUDE_PS_SHRINE_READ) -> dict[str, Any]:
    """Main PS-B Arrange entry — idempotent spawn/aim for PS_* + relocate CAM_Hero/CabinClose."""
    world = _assert_markers_world()
    dress_actors = _actors_for_dress_bounds(include_pa_d=True)
    dress_bounds = common.combined_bounds_from_actors(dress_actors)
    if not dress_bounds:
        raise RuntimeError("No DRESS_* / PA_D_* actors found — run dress + pa_d chain first.")

    dress_bounds_path = _write_dress_bounds_json(dress_bounds, actor_count=len(dress_actors))

    relocate_results = _relocate_json_cameras(dress_bounds)

    ps_cameras: list[dict[str, Any]] = []
    for direction in HIGH_ISO_DIRECTIONS:
        label = f"PS_{direction}_HighIso"
        loc, rot, pose_meta = _pose_high_iso(direction, dress_bounds)
        _actor, meta = _ensure_camera_actor(label, loc, rot)
        ps_cameras.append({**meta, **pose_meta})

    pose_fns = (
        ("PS_Cliff_Underside", _pose_cliff_underside),
        ("PS_Path_Corridor", _pose_path_corridor),
        ("PS_Garden_Close", _pose_garden_close),
    )
    for label, fn in pose_fns:
        loc, rot, pose_meta = fn(dress_bounds)
        _actor, meta = _ensure_camera_actor(label, loc, rot)
        ps_cameras.append({**meta, **pose_meta})

    if include_shrine:
        loc, rot, pose_meta = _pose_shrine_read(dress_bounds)
        _actor, meta = _ensure_camera_actor("PS_Shrine_Read", loc, rot)
        ps_cameras.append({**meta, **pose_meta})

    json_cam_present = {label: _find_actor_exact_label(label) is not None for label in JSON_CAM_LABELS}
    forbidden_present = [lbl for lbl in FORBIDDEN_ALIAS_LABELS if _find_actor_exact_label(lbl)]
    new_ps_present = {
        lbl: _find_actor_exact_label(lbl) is not None
        for lbl in NEW_PS_CAMERA_LABELS
        if lbl != "PS_Shrine_Read" or include_shrine
    }

    dress_count = _count_label_prefix(common.DRESS_LABEL_PREFIX)
    pa_d_count = _count_label_prefix("PA_D_")

    blocked: list[str] = []
    if forbidden_present:
        blocked.append("forbidden_alias_cameras_present")
    if not all(json_cam_present.values()):
        missing = [k for k, v in json_cam_present.items() if not v]
        blocked.append(f"missing_json_cams:{','.join(missing)}")
    if not all(new_ps_present.values()):
        missing = [k for k, v in new_ps_present.items() if not v]
        blocked.append(f"missing_ps_cams:{','.join(missing)}")
    if dress_count < 1:
        blocked.append("dress_count_zero")

    ready_for_ps_c = len(blocked) == 0

    gate: dict[str, Any] = {
        "version": 1,
        "track": "PS-B",
        "world_ok": True,
        "world": world,
        "level_path": common.LEVEL_PATH,
        "dress_aabb_summary": {
            "centroid": dress_bounds["centroid"],
            "extent": dress_bounds["extent"],
            "min": dress_bounds["min"],
            "max": dress_bounds["max"],
        },
        "counts": {
            "dress_prefix": dress_count,
            "pa_d_prefix": pa_d_count,
            "dress_bounds_source_actors": len(dress_actors),
        },
        "json_cameras_present": json_cam_present,
        "forbidden_alias_cameras": forbidden_present,
        "ps_cameras": ps_cameras,
        "relocate_cameras": relocate_results,
        "cam_labels_required": {
            "json": list(JSON_CAM_LABELS),
            "relocate": list(RELOCATE_CAM_LABELS),
            "new_ps": [lbl for lbl in NEW_PS_CAMERA_LABELS if lbl != "PS_Shrine_Read" or include_shrine],
            "optional_mrq": list(MRQ_OPTIONAL_LABELS),
        },
        "include_ps_shrine_read": include_shrine,
        "dress_bounds_json": dress_bounds_path,
        "ready_for_ps_c": ready_for_ps_c,
        "blocked_reasons": blocked,
        "generated_at_iso": datetime.now(timezone.utc).isoformat(),
        "note": (
            "Pose quality requires DESKTOP viewport eyeball before Lead APPROVE PS-B. "
            "PS-C: ps_placement_prove.py (not in this script)."
        ),
    }

    gate_path = _project_saved_path("ps_arrange_gate.json")
    with open(gate_path, "w", encoding="utf-8") as f:
        json.dump(gate, f, indent=2, default=str)
    gate["written_path"] = gate_path
    _log(
        "arrange complete",
        {
            "ready_for_ps_c": ready_for_ps_c,
            "dress": dress_count,
            "pa_d": pa_d_count,
            "blocked": blocked,
        },
    )
    return gate


def main() -> None:
    gate = arrange_ps_homestead()
    print(json.dumps({"ok": gate.get("ready_for_ps_c"), "gate_path": gate.get("written_path")}, indent=2))


if __name__ == "__main__":
    main()

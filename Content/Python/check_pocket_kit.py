"""Measure the L_SizeTest pocket kit, reopen the map, and measure it again.

Run inside the Unreal Editor. A row is closed_fail when its actor is missing
or location, scale, or bounds-bottom moves by more than 1 cm across the
reopen. A route gap that the room plan does not state, and the shrine taste
row, are soft_fail. Soft_fail does not excuse a missing actor.
"""

from __future__ import annotations

import os
import re

DRIFT_CM = 1.0
MAP_TOKEN = "L_SizeTest"
MAP_PATH = "/Game/HomeWorld/Maps/SizeTest/L_SizeTest"
MESH_DIR = "/Game/HomeWorld/Meshes/SizeTest"
ROOM_PLAN = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "Docs", "level", "L_SizeTest_ROOM_PLAN.md")
)
OUTPUT = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "Saved", "check_pocket_kit_output.txt")
)

PATH_START = (-950.0, -680.0)
PATH_END = (1400.0, -600.0)
PATH_SPACING_CM = 150.0
FENCE_Y = -1150.0
FENCE_X0 = -1500.0
FENCE_X1 = -400.0
SHRINE_XY = (-1620.0, -830.0)
SHRINE_HEIGHT_CM = 400.0
SHRINE_ROW = "Lead taste number"
SHRINE_ACTOR = "SM_Size_Shrine"
MOSS_ON_ROCK = (
    ("SM_Size_Moss", "SM_Size_Rock"),
    ("SM_Size_Moss_B", "SM_Size_Rock_B"),
    ("SM_Size_Moss_C", "SM_Size_Rock_C"),
)


def path_points() -> list[tuple[float, float]]:
    """Centers every 1.5 m from the porch entry toward the pine, on the segment."""
    x0, y0 = PATH_START
    x1, y1 = PATH_END
    span = x1 - x0
    if span <= 0.0 or PATH_SPACING_CM <= 0.0:
        raise ValueError("path does not advance along +X")
    points: list[tuple[float, float]] = []
    x = x0
    while x <= x1 + 0.01:
        t = (x - x0) / span
        points.append((x, y0 + t * (y1 - y0)))
        x += PATH_SPACING_CM
        if len(points) > 40:
            raise ValueError("path spacing did not advance")
    if len(points) not in (16, 17):
        raise ValueError("path stone count is %d" % len(points))
    return points


def path_labels() -> list[str]:
    return ["SM_Size_Path_%02d" % (index + 1) for index in range(len(path_points()))]


def fence_origins(segment_cm: float) -> list[float]:
    """Segment starts along X. Each start is still west of the named end."""
    if segment_cm <= 1.0:
        raise ValueError("fence segment is %.2f cm" % segment_cm)
    origins: list[float] = []
    x = FENCE_X0
    while x < FENCE_X1 - 0.01:
        origins.append(x)
        x += segment_cm
        if len(origins) > 24:
            raise ValueError("fence run did not advance")
    if not origins:
        raise ValueError("fence run is empty")
    return origins


def fence_labels(segment_cm: float) -> list[str]:
    return ["SM_Size_Fence_%02d" % (index + 1) for index in range(len(fence_origins(segment_cm)))]


def stated_route_gaps(text: str) -> dict[str, float]:
    """Centimeter gaps the room plan states on a route-gap line.

    A line counts only when it names a pad edge or a route gap and a length.
    Other meter values in the plan are not route gaps. A missing key stays
    missing so the caller can soft_fail it.
    """
    found: dict[str, float] = {}
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    for raw in normalized.split("\n"):
        line = raw.lower()
        if "pad edge" not in line and "route gap" not in line:
            continue
        match = re.search(r"(-?\d+(?:\.\d+)?)\s*(cm|m)\b", line)
        if match is None:
            continue
        value = float(match.group(1))
        if match.group(2) == "m":
            value *= 100.0
        if "path" in line or "+x" in line:
            found["path_pos_x"] = value
        if "fence" in line or "-y" in line:
            found["fence_neg_y"] = value
    return found


def gap_verdict(measured_cm: float | None, stated_cm: float | None) -> tuple[str, str]:
    if measured_cm is None:
        return "soft_fail", "route gap unmeasured"
    if stated_cm is None:
        return "soft_fail", "room plan states no route gap (measured %.2f cm)" % measured_cm
    delta = measured_cm - stated_cm
    if abs(delta) > DRIFT_CM:
        return "soft_fail", "route gap measured %.2f cm, room plan %.2f cm" % (measured_cm, stated_cm)
    return "ok", "route gap matches room plan %.2f cm" % stated_cm


def _over_cm(delta: float) -> bool:
    return abs(delta) > DRIFT_CM


def drift_verdict(before: dict | None, after: dict | None) -> tuple[str, str]:
    if before is None or after is None:
        return "closed_fail", "missing"
    reasons: list[str] = []
    for axis, left, right in zip("xyz", before["location"], after["location"]):
        if _over_cm(left - right):
            reasons.append("location %s drift %.2f cm" % (axis, left - right))
    for axis, left, right, size in zip("xyz", before["scale"], after["scale"], before["size"]):
        native = size / left if abs(left) > 1e-6 else size
        moved = (left - right) * native
        if _over_cm(moved):
            reasons.append("scale %s drift %.2f cm" % (axis, moved))
    if _over_cm(before["bottom"] - after["bottom"]):
        reasons.append("bounds-bottom drift %.2f cm" % (before["bottom"] - after["bottom"]))
    if reasons:
        return "closed_fail", "; ".join(reasons)
    return "closed_pass", ""


def row_verdict(
    before: dict | None,
    after: dict | None,
    gap_key: str | None,
    measured_gap: float | None,
    stated: dict[str, float],
    shrine: bool,
) -> tuple[str, str]:
    status, reason = drift_verdict(before, after)
    if status == "closed_fail":
        if shrine:
            return "closed_fail", reason + "; " + SHRINE_ROW
        return status, reason
    notes: list[str] = []
    if gap_key is not None:
        gap_status, gap_reason = gap_verdict(measured_gap, stated.get(gap_key))
        if gap_status == "soft_fail":
            notes.append(gap_reason)
    if shrine:
        notes.append("shrine taste row")
    if notes:
        return "soft_fail", "; ".join(notes)
    return "closed_pass", ""


def run_host_checks() -> None:
    points = path_points()
    if len(points) not in (16, 17):
        raise AssertionError(len(points))
    if abs(points[0][0] - PATH_START[0]) > 1e-6 or abs(points[0][1] - PATH_START[1]) > 1e-6:
        raise AssertionError(points[0])
    if points[-1][0] > PATH_END[0] + 1e-6:
        raise AssertionError(points[-1])
    origins = fence_origins(200.0)
    if origins[0] != FENCE_X0 or not (origins[-1] < FENCE_X1 <= origins[-1] + 200.0):
        raise AssertionError(origins)
    herb = "The player stands on that path at (-9.5 m, -9.5 m).\n"
    sample = herb + (
        "Path route gap to the +X pad edge is 600 cm.\n"
        "Fence route gap to the -Y pad edge is 2.5 m.\n"
    )
    stated = stated_route_gaps(sample)
    if stated.get("path_pos_x") != 600.0 or stated.get("fence_neg_y") != 250.0:
        raise AssertionError(stated)
    if stated_route_gaps(herb):
        raise AssertionError("herb line was read as a route gap")
    if gap_verdict(600.0, None)[0] != "soft_fail":
        raise AssertionError("missing plan gap must soft_fail")
    if gap_verdict(600.0, 600.0)[0] != "ok":
        raise AssertionError("matching gap must not soft_fail")
    if gap_verdict(600.0, 602.0)[0] != "soft_fail":
        raise AssertionError("gap off by more than 1 cm must soft_fail")
    if _over_cm(1.0) or not _over_cm(1.01):
        raise AssertionError("drift threshold is greater than 1 cm")
    same = {
        "location": (0.0, 0.0, 0.0),
        "scale": (1.0, 1.0, 1.0),
        "size": (100.0, 100.0, 100.0),
        "bottom": 10.0,
    }
    moved = dict(same)
    moved["bottom"] = 11.2
    if drift_verdict(same, same)[0] != "closed_pass":
        raise AssertionError("stable actor must closed_pass")
    if drift_verdict(same, None)[0] != "closed_fail":
        raise AssertionError("missing actor must closed_fail")
    if drift_verdict(same, moved)[0] != "closed_fail":
        raise AssertionError("bounds-bottom drift must closed_fail")
    shrine = row_verdict(same, same, None, None, {}, True)
    if shrine[0] != "soft_fail":
        raise AssertionError(shrine)
    print("check_pocket_kit host checks ok points=%d fences=%d" % (len(points), len(origins)))


def _fmt(value: float) -> str:
    return "%.2f" % value


def _fmt3(values: tuple[float, float, float]) -> str:
    return "(%s,%s,%s)" % tuple(_fmt(value) for value in values)


def _format_actor(
    phase: str,
    row_name: str,
    actor_name: str,
    measured: dict | None,
    surface: float | None,
    gap_key: str | None,
    gap_value: float | None,
) -> str:
    if measured is None:
        return "check_pocket_kit %s row=%s name=%s MISSING" % (phase, row_name, actor_name)
    if surface is None:
        versus = "unmeasured"
        surface_text = "unmeasured"
    else:
        versus = _fmt(measured["bottom"] - surface)
        surface_text = _fmt(surface)
    gap = ""
    if gap_key is not None and gap_value is not None:
        gap = " route_gap_%s_cm=%s" % (gap_key, _fmt(gap_value))
    elif gap_key is not None:
        gap = " route_gap_%s_cm=unmeasured" % gap_key
    return (
        "check_pocket_kit %s row=%s name=%s class=%s location=%s scale=%s "
        "bounds_min=%s bounds_max=%s bottom=%s surface=%s bottom_vs_surface=%s%s"
        % (
            phase,
            row_name,
            actor_name,
            measured["class"],
            _fmt3(measured["location"]),
            _fmt3(measured["scale"]),
            _fmt3(measured["bounds_min"]),
            _fmt3(measured["bounds_max"]),
            _fmt(measured["bottom"]),
            surface_text,
            versus,
            gap,
        )
    )


def main() -> int:
    import sys

    import unreal

    sys.path.insert(0, os.path.dirname(__file__))
    import scene_placement

    lines: list[str] = []

    def emit(text: str) -> None:
        lines.append(text)
        unreal.log(text)

    def load_map() -> str:
        unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(MAP_PATH)
        world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
        return world.get_path_name() if world is not None else ""

    def measure_all() -> dict[str, dict]:
        found: dict[str, dict] = {}
        for actor in scene_placement.actors():
            name = actor.get_actor_label()
            origin, extent = actor.get_actor_bounds(False)
            loc = actor.get_actor_location()
            scale = actor.get_actor_scale3d()
            found[name] = {
                "name": name,
                "class": actor.get_class().get_name(),
                "location": (float(loc.x), float(loc.y), float(loc.z)),
                "scale": (float(scale.x), float(scale.y), float(scale.z)),
                "bounds_min": (
                    float(origin.x - extent.x),
                    float(origin.y - extent.y),
                    float(origin.z - extent.z),
                ),
                "bounds_max": (
                    float(origin.x + extent.x),
                    float(origin.y + extent.y),
                    float(origin.z + extent.z),
                ),
                "bottom": float(origin.z - extent.z),
                "size": (float(extent.x * 2.0), float(extent.y * 2.0), float(extent.z * 2.0)),
            }
        return found

    world_path = load_map() if MAP_TOKEN not in _current_world_path(unreal) else _current_world_path(unreal)
    before = measure_all()
    pad = _pad(before.get("SM_Size_Island"))
    segment = _fence_segment_cm(unreal)
    catalog = _catalog(segment)
    stated = {}
    plan_error = ""
    try:
        stated = stated_route_gaps(open(ROOM_PLAN, encoding="utf-8").read())
    except OSError as exc:
        plan_error = str(exc)
    emit(
        "check_pocket_kit map=%s pad_top_z=%s edge_pos_x=%s edge_neg_x=%s edge_pos_y=%s edge_neg_y=%s"
        % (
            world_path,
            _fmt(pad["top"]) if pad else "unmeasured",
            _fmt(pad["pos_x"]) if pad else "unmeasured",
            _fmt(pad["neg_x"]) if pad else "unmeasured",
            _fmt(pad["pos_y"]) if pad else "unmeasured",
            _fmt(pad["neg_y"]) if pad else "unmeasured",
        )
    )
    if plan_error:
        emit("check_pocket_kit room_plan_unreadable %s" % plan_error)
    emit("check_pocket_kit room_plan_gaps %s" % (stated if stated else "none"))
    _emit_phase(emit, "before_reopen", before, pad, catalog)

    reopened = load_map()
    after = measure_all()
    pad_after = _pad(after.get("SM_Size_Island"))
    emit("check_pocket_kit reopened map=%s" % reopened)
    _emit_phase(emit, "after_reopen", after, pad_after, catalog)

    closed_fail = 0
    soft_fail = 0
    inspected = 0
    if pad is None or pad_after is None or MAP_TOKEN not in world_path or MAP_TOKEN not in reopened:
        closed_fail += 1
        emit("check_pocket_kit verdict map closed_fail unmeasured or wrong level")
    for entry in catalog:
        inspected += 1
        left = before.get(entry["actor"])
        right = after.get(entry["actor"])
        gap_key = entry["gap"]
        measured_gap = _gap_value(left, pad, gap_key)
        status, reason = row_verdict(
            left,
            right,
            gap_key,
            measured_gap,
            stated,
            entry["shrine"],
        )
        if status == "closed_fail":
            closed_fail += 1
        elif status == "soft_fail":
            soft_fail += 1
        suffix = (" " + reason) if reason else ""
        emit("check_pocket_kit verdict row=%s name=%s %s%s" % (entry["row"], entry["actor"], status, suffix))
    if inspected < 1:
        closed_fail += 1
        emit("check_pocket_kit verdict catalog closed_fail inspected nothing")
    emit(
        "check_pocket_kit RESULT inspected=%d closed_fail=%d soft_fail=%d"
        % (inspected, closed_fail, soft_fail)
    )
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")
    return 0 if closed_fail == 0 else 1


def _current_world_path(unreal_module: object) -> str:
    world = unreal_module.get_editor_subsystem(unreal_module.UnrealEditorSubsystem).get_editor_world()
    return world.get_path_name() if world is not None else ""


def _fence_segment_cm(unreal_module: object) -> float:
    mesh = unreal_module.EditorAssetLibrary.load_asset(MESH_DIR + "/SM_Size_Fence")
    if mesh is None:
        raise RuntimeError("SM_Size_Fence mesh is missing")
    bounds = mesh.get_bounds()
    return float(bounds.box_extent.x) * 2.0


def _pad(island: dict | None) -> dict | None:
    if island is None:
        return None
    return {
        "top": island["bounds_max"][2],
        "pos_x": island["bounds_max"][0],
        "neg_x": island["bounds_min"][0],
        "pos_y": island["bounds_max"][1],
        "neg_y": island["bounds_min"][1],
    }


def _catalog(segment_cm: float) -> list[dict]:
    last_path = path_labels()[-1]
    entries: list[dict] = []
    for label in path_labels():
        entries.append(
            {
                "actor": label,
                "row": label,
                "gap": "path_pos_x" if label == last_path else None,
                "shrine": False,
            }
        )
    for label in fence_labels(segment_cm):
        entries.append({"actor": label, "row": label, "gap": "fence_neg_y", "shrine": False})
    entries.append({"actor": SHRINE_ACTOR, "row": SHRINE_ROW, "gap": None, "shrine": True})
    for moss_label, _rock in MOSS_ON_ROCK:
        entries.append({"actor": moss_label, "row": moss_label, "gap": None, "shrine": False})
    return entries


def _gap_value(measured: dict | None, pad: dict | None, gap_key: str | None) -> float | None:
    if measured is None or pad is None or gap_key is None:
        return None
    if gap_key == "path_pos_x":
        return pad["pos_x"] - measured["bounds_max"][0]
    if gap_key == "fence_neg_y":
        return measured["bounds_min"][1] - pad["neg_y"]
    return None


def _surface(entry: dict, measured: dict[str, dict], pad: dict | None) -> float | None:
    actor_name = entry["actor"]
    if actor_name.startswith("SM_Size_Moss"):
        rock_name = dict(MOSS_ON_ROCK).get(actor_name)
        rock = measured.get(rock_name) if rock_name else None
        if rock is None:
            return None
        return rock["bounds_max"][2]
    if pad is None:
        return None
    return pad["top"]


def _emit_phase(emit, phase: str, measured: dict[str, dict], pad: dict | None, catalog: list[dict]) -> None:
    for entry in catalog:
        row = measured.get(entry["actor"])
        surface = _surface(entry, measured, pad)
        gap_value = _gap_value(row, pad, entry["gap"])
        emit(_format_actor(phase, entry["row"], entry["actor"], row, surface, entry["gap"], gap_value))


if __name__ == "__main__":
    try:
        import unreal  # noqa: F401
    except ImportError:
        run_host_checks()
    else:
        main()

"""Ease pad placer.

The pad and its focus belong on L_EasePad. They do not belong on L_SizeTest.
Host tests call ease_pad_report. An editor run places from
Docs/level/L_EasePad_METRICS.md and saves only after the measure passes.
"""

from __future__ import annotations

import os

PAD_MAP = "/Game/HomeWorld/Maps/EasePad/L_EasePad"
SIZE_TEST_MAP = "/Game/HomeWorld/Maps/SizeTest/L_SizeTest"
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
METRICS = os.path.join(ROOT, "Docs", "level", "L_EasePad_METRICS.md")
M = 100.0
SUN_LABEL = "EasePad_Sun"
SKY_LIGHT_LABEL = "EasePad_SkyLight"
SKY_ATMOSPHERE_LABEL = "EasePad_SkyAtmosphere"
SUN_PITCH = -45.0
SUN_YAW = 30.0
FLOOR_LABEL = "SM_EasePad_Floor"

INTENDED_PAD = (
    ("EasePad", ("HomeWorldEasePad", "Focus")),
    ("EasePad_Focus", ("SceneComponent",)),
)

SIZE_TEST_STAYS = (
    ("PlayerStart", ("PlayerStart",)),
    ("SM_Size_Cottage", ("StaticMeshActor",)),
)


def _blob(label, class_names):
    parts = [label or ""]
    for name in class_names or ():
        parts.append(name or "")
    return " ".join(parts)


def _has(entries, needle):
    for label, class_names in entries:
        if needle in _blob(label, class_names):
            return True
    return False


def ease_pad_report(pad_level, size_test_level):
    """Report the pad, the focus, and that the pad is absent from L_SizeTest."""
    pad = _has(pad_level, "EasePad") or _has(pad_level, "HomeWorldEasePad")
    focus = _has(pad_level, "Focus")
    on_size_test = _has(size_test_level, "EasePad") or _has(size_test_level, "HomeWorldEasePad") or _has(
        size_test_level, "StrokeReport"
    )
    return {
        "map": PAD_MAP,
        "pad": pad,
        "focus": focus,
        "absent_from_L_SizeTest": not on_size_test,
        "size_test_map": SIZE_TEST_MAP,
    }


def load_metrics():
    text = open(METRICS, encoding="utf-8").read()
    start = text.index("```json") + len("```json")
    end = text.index("```", start)
    import json

    return json.loads(text[start:end])


def _u():
    import unreal

    return unreal


def actors():
    return _u().get_editor_subsystem(_u().EditorActorSubsystem).get_all_level_actors()


def by_label():
    found = {}
    for actor in actors():
        found.setdefault(actor.get_actor_label(), actor)
    return found


def destroy(actor):
    _u().get_editor_subsystem(_u().EditorActorSubsystem).destroy_actor(actor)


def vec(x_m, y_m, z_m):
    return _u().Vector(x_m * M, y_m * M, z_m * M)


def yaw_rotator(yaw):
    rot = _u().Rotator()
    rot.yaw = float(yaw)
    return rot


def sun_rotator():
    return _u().Rotator(roll=0.0, pitch=SUN_PITCH, yaw=SUN_YAW)


def editor_world():
    return _u().get_editor_subsystem(_u().UnrealEditorSubsystem).get_editor_world()


def map_name():
    world = editor_world()
    if world is None:
        return ""
    return world.get_name() or ""


def level_editor():
    return _u().get_editor_subsystem(_u().LevelEditorSubsystem)


def load_map(path):
    level = level_editor()
    if not _u().EditorAssetLibrary.does_asset_exist(path):
        return False
    level.load_level(path)
    return True


def class_name(actor):
    if actor is None:
        return ""
    return actor.get_class().get_name() or ""


def is_ease_pad(actor):
    label = actor.get_actor_label() or ""
    return label == "EasePad" or "HomeWorldEasePad" in class_name(actor)


def has_focus(actor):
    for comp in actor.get_components_by_class(_u().SceneComponent):
        name = comp.get_name() or ""
        if name == "Focus" or name.startswith("Focus"):
            return True
    return False


def trace_hit(world, x_cm, y_cm):
    """One downward trace. Editor Python exposes the hit on to_dict()."""
    unreal = _u()
    start = unreal.Vector(x_cm, y_cm, 500.0)
    end = unreal.Vector(x_cm, y_cm, -500.0)
    draw = unreal.DrawDebugTrace.NONE
    try:
        hit = unreal.SystemLibrary.line_trace_single(
            world, start, end, unreal.TraceTypeQuery.TRACE_TYPE_QUERY1, False, [], draw, True
        )
    except TypeError:
        hit = unreal.SystemLibrary.line_trace_single(
            world,
            start,
            end,
            unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,
            False,
            [],
            draw,
            True,
            unreal.LinearColor(0, 0, 0, 0),
            unreal.LinearColor(0, 0, 0, 0),
            0.0,
        )
    if hit is None or not hasattr(hit, "to_dict"):
        return None
    data = hit.to_dict()
    if not data.get("blocking_hit"):
        return None
    actor = data.get("hit_actor")
    return {
        "z": float(data["location"].z),
        "label": actor.get_actor_label() if actor is not None else "none",
    }


def measure_current():
    """Measure the open L_EasePad. Does not move actors and does not save."""
    errors = []
    if "L_EasePad" not in map_name():
        errors.append("open map is %s, want L_EasePad" % map_name())
        return errors
    metrics = load_metrics()
    found = by_label()
    floor = found.get(FLOOR_LABEL)
    if floor is None:
        errors.append("no " + FLOOR_LABEL)
    else:
        world = editor_world()
        center = metrics["floor"]
        offsets = ((0, 0), (2, 0), (-2, 0), (0, 2), (0, -2))
        zs = []
        for dx, dy in offsets:
            hit = trace_hit(world, (center["x"] + dx) * M, (center["y"] + dy) * M)
            if hit is not None and hit["label"] == FLOOR_LABEL:
                zs.append(hit["z"])
        if len(zs) < 5:
            errors.append("%d floor traces hit %s, want 5" % (len(zs), FLOOR_LABEL))
        elif max(zs) - min(zs) > 50.0:
            errors.append("floor traces span %.0f cm" % (max(zs) - min(zs)))
    pad = found.get("EasePad")
    if pad is None or "HomeWorldEasePad" not in class_name(pad):
        errors.append("no HomeWorldEasePad labeled EasePad")
    elif not has_focus(pad):
        errors.append("EasePad has no Focus")
    if found.get("PlayerStart") is None and not any(class_name(actor) == "PlayerStart" for actor in actors()):
        errors.append("no player start")
    directional = [actor for actor in actors() if "DirectionalLight" in class_name(actor)]
    if len(directional) != 1:
        errors.append("%d directional lights, want 1" % len(directional))
    return errors


def size_test_has_ease_pad():
    """Load L_SizeTest, look for an ease pad, and do not save that map."""
    if not _u().EditorAssetLibrary.does_asset_exist(SIZE_TEST_MAP):
        return False
    load_map(SIZE_TEST_MAP)
    return any(is_ease_pad(actor) for actor in actors())


def place_cube(label, x, y, z, sx, sy, sz):
    unreal = _u()
    cube = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
    if cube is None:
        return "no engine cube"
    actor = by_label().get(label)
    if actor is None:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.StaticMeshActor, vec(x, y, z), yaw_rotator(0)
        )
        actor.set_actor_label(label)
    actor.set_actor_location(vec(x, y, z), False, False)
    actor.set_actor_rotation(yaw_rotator(0), False)
    actor.set_actor_scale3d(unreal.Vector(sx, sy, sz))
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    component.set_static_mesh(cube)
    component.set_collision_profile_name("BlockAll")
    component.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
    return None


def place_player(player):
    unreal = _u()
    actor = None
    for candidate in actors():
        if class_name(candidate) == "PlayerStart":
            actor = candidate
            break
    if actor is None:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.PlayerStart, vec(player["x"], player["y"], player["z"]), yaw_rotator(player["yaw"])
        )
    actor.set_actor_label("PlayerStart")
    actor.set_actor_location(vec(player["x"], player["y"], player["z"]), False, False)
    actor.set_actor_rotation(yaw_rotator(player["yaw"]), False)


def place_pad(pad):
    unreal = _u()
    cls = unreal.load_class(None, "/Script/HomeWorld.HomeWorldEasePad")
    if cls is None:
        return "HomeWorldEasePad class is not loaded"
    actor = by_label().get(pad["label"])
    if actor is not None and "HomeWorldEasePad" not in class_name(actor):
        destroy(actor)
        actor = None
    if actor is None:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            cls, vec(pad["x"], pad["y"], pad["z"]), yaw_rotator(0)
        )
        actor.set_actor_label(pad["label"])
    actor.set_actor_location(vec(pad["x"], pad["y"], pad["z"]), False, False)
    return None


def spawn_light(label, actor_class, location, rotation):
    unreal = _u()
    actor = by_label().get(label)
    if actor is None:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, location, rotation)
        actor.set_actor_label(label)
    actor.set_actor_location(location, False, False)
    actor.set_actor_rotation(rotation, False)


def place_lights():
    unreal = _u()
    zero = yaw_rotator(0)
    for actor in list(actors()):
        if "DirectionalLight" not in class_name(actor):
            continue
        if actor.get_actor_label() == SUN_LABEL:
            continue
        unreal.log("ease_pad: removed extra sun " + actor.get_actor_label())
        destroy(actor)
    spawn_light(SUN_LABEL, unreal.DirectionalLight, vec(0, 0, 5), sun_rotator())
    spawn_light(SKY_LIGHT_LABEL, unreal.SkyLight, vec(0, 0, 5), zero)
    spawn_light(SKY_ATMOSPHERE_LABEL, unreal.SkyAtmosphere, vec(0, 0, 0), zero)


def place_from_metrics():
    metrics = load_metrics()
    floor = metrics["floor"]
    error = place_cube(floor["label"], floor["x"], floor["y"], floor["z"], floor["sx"], floor["sy"], floor["sz"])
    if error:
        return [error]
    error = place_pad(metrics["pad"])
    if error:
        return [error]
    place_player(metrics["player"])
    place_lights()
    return []


def run_editor():
    """Place L_EasePad and save only when the measure passes and L_SizeTest has no pad."""
    unreal = _u()
    if not unreal.EditorAssetLibrary.does_asset_exist(SIZE_TEST_MAP):
        unreal.log("ease_pad: NOT SAVED, L_SizeTest is missing")
        return 1
    if size_test_has_ease_pad():
        unreal.log("ease_pad: NOT SAVED, an ease pad is on L_SizeTest")
        return 1
    level = level_editor()
    if unreal.EditorAssetLibrary.does_asset_exist(PAD_MAP):
        level.load_level(PAD_MAP)
    else:
        level.new_level(PAD_MAP)
    errors = place_from_metrics()
    errors.extend(measure_current())
    if errors:
        for error in errors:
            unreal.log("ease_pad: FAIL " + error)
        unreal.log("ease_pad: NOT SAVED")
        return 1
    level.save_current_level()
    unreal.log("ease_pad: saved")
    return 0


def main():
    try:
        import unreal  # noqa: F401
    except ImportError:
        report = ease_pad_report(INTENDED_PAD, SIZE_TEST_STAYS)
        print(
            "ease_pad: pad=%s focus=%s absent_from_L_SizeTest=%s map=%s"
            % (report["pad"], report["focus"], report["absent_from_L_SizeTest"], report["map"])
        )
        if not (report["pad"] and report["focus"] and report["absent_from_L_SizeTest"]):
            raise SystemExit(1)
        return
    raise SystemExit(run_editor())


if __name__ == "__main__":
    main()

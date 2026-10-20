"""Place a test scene from its metrics file and refuse to save a failed check.

The metrics file is the approved layout, in meters. This module snaps mesh
bottoms onto the measured floor, measures them again, and refuses to save if
any bottom is more than 2 cm off, or if two solids clip through each other.
See Docs/context/SCENE_SETUP.md practices
10-12: coat yaw offset 0, walk only while moving, pin before save.
"""

import json
import math
import os
import sys

import unreal

sys.path.insert(0, os.path.dirname(__file__))
import armory_shell
import cabin_shell
import size_test_guard

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
METRICS = os.path.join(ROOT, "Docs", "level", "L_SizeTest_METRICS.md")
MAP_PATH = "/Game/HomeWorld/Maps/SizeTest/L_SizeTest"
MESH_DIR = "/Game/HomeWorld/Meshes/SizeTest"
M = 100.0
CELL = 100.0
CAPSULE_RADIUS = 42.0
CAPSULE_HALF = 100.0
CLEARANCE = 200.0
PASSABLE_PREFIXES = ("SM_Size_HerbBed", "SM_Size_Lupine")
KEEP_EXACT = {
    "SM_Size_Island",
    "SM_Size_Cottage",
    "SM_Size_Field",
    "PlayerStart",
    "SizeTest_Sun",
    "SizeTest_SkyLight",
    "SizeTest_Sky",
    "SizeTest_Exposure",
}


def load_metrics():
    text = open(METRICS, encoding="utf-8").read()
    start = text.index("```json") + len("```json")
    end = text.index("```", start)
    return json.loads(text[start:end])


def actors():
    return unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()


def by_label():
    found = {}
    for actor in actors():
        found.setdefault(actor.get_actor_label(), actor)
    return found


def vec(x_m, y_m, z_m):
    return unreal.Vector(x_m * M, y_m * M, z_m * M)


def yaw_rotator(yaw):
    rot = unreal.Rotator()
    rot.yaw = float(yaw)
    return rot


def destroy(actor):
    unreal.get_editor_subsystem(unreal.EditorActorSubsystem).destroy_actor(actor)


def stand_like_player(actor):
    """Hold the wake pose. The mesh is the actor root, so the sheet yaw is the whole facing:
    SK_Player_Female faces mesh -Y, and the sheet turns that face where the beat wants it."""
    mesh = actor.get_component_by_class(unreal.SkeletalMeshComponent)
    if mesh is None:
        return
    mesh.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
    mesh.stop()


def place_skeletal(label, mesh_name, x_m, y_m, z_m, yaw, scale=1.0):
    mesh = unreal.EditorAssetLibrary.load_asset(MESH_DIR + "/" + mesh_name)
    if mesh is None:
        unreal.log("scene_placement: missing mesh " + mesh_name)
        return None
    location = vec(x_m, y_m, z_m)
    rotation = yaw_rotator(yaw)
    actor = by_label().get(label)
    if actor is not None and actor.get_component_by_class(unreal.SkeletalMeshComponent) is None:
        destroy(actor)
        actor = None
    if actor is None:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.SkeletalMeshActor, location, rotation
        )
        actor.set_actor_label(label)
    actor.set_actor_location(location, False, False)
    actor.set_actor_rotation(rotation, False)
    actor.set_actor_scale3d(unreal.Vector(float(scale), float(scale), float(scale)))
    component = actor.get_component_by_class(unreal.SkeletalMeshComponent)
    if component is None:
        unreal.log("scene_placement: no skeletal component " + label)
        return actor
    if hasattr(component, "set_skinned_asset_and_update"):
        component.set_skinned_asset_and_update(mesh)
    else:
        component.set_skeletal_mesh(mesh)
    component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    return actor


def place_static(label, mesh_name, x_m, y_m, z_m, yaw, scale=1.0, scale_z=1.0):
    mesh = unreal.EditorAssetLibrary.load_asset(MESH_DIR + "/" + mesh_name)
    if mesh is None:
        unreal.log("scene_placement: missing mesh " + mesh_name)
        return None
    location = vec(x_m, y_m, z_m)
    rotation = yaw_rotator(yaw)
    actor = by_label().get(label)
    if actor is not None and actor.get_component_by_class(unreal.StaticMeshComponent) is None:
        destroy(actor)
        actor = None
    if actor is None:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.StaticMeshActor, location, rotation
        )
        actor.set_actor_label(label)
    actor.set_actor_location(location, False, False)
    actor.set_actor_rotation(rotation, False)
    actor.set_actor_scale3d(unreal.Vector(scale, scale, scale_z))
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    if component is not None:
        component.set_static_mesh(mesh)
    return actor


def place_cube(label, x_m, y_m, z_m, yaw, size):
    """An engine cube, size in meters. The armor table uses this, like the walk pad."""
    cube = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
    if cube is None:
        unreal.log("scene_placement: FAIL no engine cube for " + label)
        return None
    location = vec(x_m, y_m, z_m)
    rotation = yaw_rotator(yaw)
    actor = by_label().get(label)
    if actor is not None and actor.get_component_by_class(unreal.StaticMeshComponent) is None:
        destroy(actor)
        actor = None
    if actor is None:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.StaticMeshActor, location, rotation
        )
        if actor is None:
            unreal.log("scene_placement: FAIL cube did not spawn " + label)
            return None
        actor.set_actor_label(label)
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    if component is not None:
        component.set_static_mesh(cube)
    actor.set_actor_location(location, False, False)
    actor.set_actor_rotation(rotation, False)
    actor.set_actor_scale3d(unreal.Vector(float(size[0]), float(size[1]), float(size[2])))
    return actor


def passable(label):
    return label.startswith(PASSABLE_PREFIXES)


def set_collision(actor):
    skeletal = actor.get_component_by_class(unreal.SkeletalMeshComponent)
    if skeletal is not None and actor.get_component_by_class(unreal.StaticMeshComponent) is None:
        skeletal.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        return
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    if component is None:
        return
    label = actor.get_actor_label()
    if label.startswith("SM_Size_HerbBed") or label == "SM_Size_Kettle":
        component.set_collision_enabled(unreal.CollisionEnabled.QUERY_ONLY)
        component.set_collision_response_to_all_channels(unreal.CollisionResponseType.ECR_IGNORE)
        component.set_collision_response_to_channel(
            unreal.CollisionChannel.ECC_VISIBILITY, unreal.CollisionResponseType.ECR_BLOCK
        )
        return
    if passable(label):
        component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        return
    component.set_collision_profile_name("BlockAll")
    component.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)


def tag_actor(actor, tag, extra=None):
    tags = [unreal.Name(tag)]
    if extra:
        tags.append(unreal.Name(extra))
    actor.set_editor_property("tags", tags)


def set_slab_collision():
    """One box for the pad in the metrics sheet. The cone does not block."""
    mesh = unreal.EditorAssetLibrary.load_asset(MESH_DIR + "/SM_Size_Island")
    if mesh is None:
        unreal.log("scene_placement: FAIL no island mesh")
        return False
    body = mesh.get_editor_property("body_setup")
    if body is None:
        unreal.log("scene_placement: FAIL island has no body setup")
        return False
    pad = load_metrics().get("pad", {"x": 40, "y": 30, "z": 1})
    body.set_editor_property("collision_trace_flag", unreal.CollisionTraceFlag.CTF_USE_SIMPLE_AS_COMPLEX)
    elem = unreal.KBoxElem()
    elem.set_editor_property("center", unreal.Vector(0.0, 0.0, -50.0))
    elem.set_editor_property("x", float(pad["x"]) * M)
    elem.set_editor_property("y", float(pad["y"]) * M)
    elem.set_editor_property("z", float(pad["z"]) * M)
    agg = body.get_editor_property("agg_geom")
    agg.set_editor_property("box_elems", [elem])
    agg.set_editor_property("sphere_elems", [])
    agg.set_editor_property("sphyl_elems", [])
    agg.set_editor_property("convex_elems", [])
    body.set_editor_property("agg_geom", agg)
    unreal.EditorAssetLibrary.save_loaded_asset(mesh)
    actor = by_label().get("SM_Size_Island")
    if actor is not None:
        component = actor.get_component_by_class(unreal.StaticMeshComponent)
        if component is not None:
            component.set_static_mesh(None)
            component.set_static_mesh(mesh)
            set_collision(actor)
    unreal.log("scene_placement: island slab %.0f by %.0f m" % (float(pad["x"]), float(pad["y"])))
    return True


def box_elem(cx, cy, cz, sx, sy, sz):
    elem = unreal.KBoxElem()
    elem.set_editor_property("center", unreal.Vector(cx, cy, cz))
    elem.set_editor_property("x", float(sx))
    elem.set_editor_property("y", float(sy))
    elem.set_editor_property("z", float(sz))
    return elem


def spawn_cabin_walls():
    """The hollow cabin is one cube mesh per wall. The old solid cottage does not block."""
    cottage = by_label().get("SM_Size_Cottage")
    if cottage is None:
        unreal.log("scene_placement: FAIL no cottage actor")
        return False
    component = cottage.get_component_by_class(unreal.StaticMeshComponent)
    if component is not None:
        component.set_visibility(False)
        component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    cottage.set_is_temporarily_hidden_in_editor(True)
    cube = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
    if cube is None:
        unreal.log("scene_placement: FAIL no engine cube")
        return False
    for actor in list(actors()):
        if actor.get_actor_label().startswith("CabinWall_") or actor.get_actor_label().startswith("PorchCrawl_") or actor.get_actor_label().startswith("CabinRoof_") or actor.get_actor_label().startswith("CabinRamp_"):
            destroy(actor)
    origin = cottage.get_actor_location()
    boxes = list(cabin_shell.BOXES) + list(cabin_shell.CRAWL_WALLS)
    labels = ["CabinWall_%02d" % index for index in range(len(cabin_shell.BOXES))]
    labels.append("PorchCrawl_West")
    labels.append("PorchCrawl_East")
    for index, box in enumerate(boxes):
        cx, cy, cz, sx, sy, sz = box
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.StaticMeshActor,
            unreal.Vector(origin.x + cx, origin.y + cy, origin.z + cz),
            yaw_rotator(0),
        )
        actor.set_actor_label(labels[index])
        actor.set_actor_scale3d(unreal.Vector(sx / 100.0, sy / 100.0, sz / 100.0))
        wall = actor.get_component_by_class(unreal.StaticMeshComponent)
        wall.set_static_mesh(cube)
        paint(actor, "MI_Greybox_Stone")
        wall.set_collision_profile_name("BlockAll")
        wall.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
    fx, fy, fz, fsx, fsy, fsz = cabin_shell.FILLER
    filler = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor,
        unreal.Vector(origin.x + fx, origin.y + fy, origin.z + fz),
        yaw_rotator(0),
    )
    filler.set_actor_label("PorchCrawl_Fill")
    filler.set_actor_scale3d(unreal.Vector(fsx / 100.0, fsy / 100.0, fsz / 100.0))
    fill_mesh = filler.get_component_by_class(unreal.StaticMeshComponent)
    fill_mesh.set_static_mesh(cube)
    paint(filler, "MI_Greybox_Stone")
    fill_mesh.set_collision_profile_name("BlockAll")
    fill_mesh.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
    tag_actor(filler, "NODE_PORCH_CRAWL")
    spawn_cabin_roof(origin, cube)
    spawn_cabin_ramp(origin, cube)
    unreal.log("scene_placement: cabin shell %d walls" % len(boxes))
    for actor in list(actors()):
        if actor.get_actor_label().startswith("CabinLight_"):
            destroy(actor)
    for index, (lx, ly, lz) in enumerate(cabin_shell.LIGHTS):
        light = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.PointLight,
            unreal.Vector(origin.x + lx, origin.y + ly, origin.z + lz),
            yaw_rotator(0),
        )
        if light is None:
            continue
        light.set_actor_label("CabinLight_%02d" % index)
        comp = light.get_component_by_class(unreal.PointLightComponent)
        if comp is not None:
            comp.set_editor_property("intensity", 4000.0)
            comp.set_editor_property("attenuation_radius", 1400.0)
            try:
                comp.set_editor_property("light_color", unreal.Color(255, 198, 140, 255))
            except Exception:
                pass
    unreal.log("scene_placement: cabin lights %d" % len(cabin_shell.LIGHTS))
    return True


def _sloped_cube(origin, name, start, end, width, thickness, material):
    """A cube whose length runs from start to end. start and end are local cm."""
    cube = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
    if cube is None:
        return None
    sx = end[0] - start[0]
    sy = end[1] - start[1]
    sz = end[2] - start[2]
    length = math.sqrt(sx * sx + sy * sy + sz * sz)
    if length < 1.0:
        return None
    uphill = unreal.Vector(sx / length, sy / length, sz / length)
    side = unreal.Vector(-sy, sx, 0.0)
    side_len = math.hypot(side.x, side.y)
    if side_len < 0.001:
        side = unreal.Vector(1.0, 0.0, 0.0)
    else:
        side = unreal.Vector(side.x / side_len, side.y / side_len, 0.0)
    normal = unreal.Vector(
        side.y * uphill.z - side.z * uphill.y,
        side.z * uphill.x - side.x * uphill.z,
        side.x * uphill.y - side.y * uphill.x,
    )
    if normal.z < 0.0:
        normal = unreal.Vector(-normal.x, -normal.y, -normal.z)
    mid = unreal.Vector(
        origin.x + (start[0] + end[0]) * 0.5 - normal.x * thickness * 0.5,
        origin.y + (start[1] + end[1]) * 0.5 - normal.y * thickness * 0.5,
        origin.z + (start[2] + end[2]) * 0.5 - normal.z * thickness * 0.5,
    )
    rot = unreal.MathLibrary.make_rot_from_xz(uphill, normal)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, mid, rot)
    if actor is None:
        return None
    actor.set_actor_label(name)
    actor.set_actor_scale3d(unreal.Vector(length / 100.0, width / 100.0, thickness / 100.0))
    mesh = actor.get_component_by_class(unreal.StaticMeshComponent)
    mesh.set_static_mesh(cube)
    paint(actor, material)
    mesh.set_collision_profile_name("BlockAll")
    mesh.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
    return actor


def spawn_cabin_roof(origin, cube):
    """Gable roof on the upstairs wall plate. The ridge runs east-west."""
    del cube
    for actor in list(actors()):
        if actor.get_actor_label().startswith("CabinRoof_"):
            destroy(actor)
    spawned = True
    for name, start, end in cabin_shell.ROOF:
        actor = _sloped_cube(
            origin, name, start, end, cabin_shell.ROOF_WIDTH, 20.0, "MI_Greybox_Slate"
        )
        spawned = spawned and actor is not None
    return spawned


def spawn_cabin_ramp(origin, cube):
    del cube
    for actor in list(actors()):
        if actor.get_actor_label().startswith("CabinRamp_"):
            destroy(actor)
    bottom, top, width = cabin_shell.RAMP
    actor = _sloped_cube(origin, "CabinRamp_0", bottom, top, width, 30.0, "MI_Greybox_Stone")
    return actor is not None


def spawn_armory_walls(top):
    """Greybox armory in front of the cottage. The door faces the courtyard, from the sheet."""
    armory = load_metrics().get("armory")
    if not armory:
        unreal.log("scene_placement: FAIL no armory in the sheet")
        return False
    cube = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
    if cube is None:
        unreal.log("scene_placement: FAIL no engine cube for the armory")
        return False
    for actor in list(actors()):
        if actor.get_actor_label().startswith("ArmoryWall_"):
            destroy(actor)
    ox = float(armory["x"]) * M
    oy = float(armory["y"]) * M
    for index, box in enumerate(armory_shell.BOXES):
        cx, cy, cz, sx, sy, sz = box
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.StaticMeshActor,
            unreal.Vector(ox + cx, oy + cy, top + cz),
            yaw_rotator(0),
        )
        actor.set_actor_label("ArmoryWall_%02d" % index)
        actor.set_actor_scale3d(unreal.Vector(sx / 100.0, sy / 100.0, sz / 100.0))
        wall = actor.get_component_by_class(unreal.StaticMeshComponent)
        wall.set_static_mesh(cube)
        paint(actor, "MI_Greybox_Stone")
        wall.set_collision_profile_name("BlockAll")
        wall.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
    unreal.log("scene_placement: armory shell %d walls" % len(armory_shell.BOXES))
    return True


def trace_floor_z(world, x, y, z_high, z_low, ignore):
    data = trace_hit(world, unreal.Vector(x, y, z_high), unreal.Vector(x, y, z_low), ignore)
    if data is None:
        return None
    if data.get("label") not in ("SM_Size_Island", "SM_Size_WalkPad"):
        unreal.log("scene_placement: floor hit %s" % data.get("label"))
        return None
    return data["z"]


def trace_hit(world, start, end, ignore):
    """One line trace. Editor Python exposes the hit on to_dict(), not as attributes."""
    draw = unreal.DrawDebugTrace.NONE
    hit = None
    try:
        hit = unreal.SystemLibrary.line_trace_single(
            world, start, end,
            unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,
            False, ignore, draw, True,
        )
    except TypeError:
        hit = unreal.SystemLibrary.line_trace_single(
            world, start, end,
            unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,
            False, ignore, draw, True,
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


def measure_floor():
    """Downward traces on the walk pad. Water and hill steps are not the floor."""
    pad = load_metrics().get("pad", {"x": 70, "y": 90})
    half_x = float(pad["x"]) * M * 0.25
    half_y = float(pad["y"]) * M * 0.25
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    ignore = [
        other for other in actors()
        if other.get_actor_label() not in ("SM_Size_Island", "SM_Size_WalkPad")
    ]
    z_high = 46000.0
    z_low = 44000.0
    samples = []
    for sx, sy in ((0.0, 0.0), (half_x, 0.0), (-half_x, 0.0), (0.0, half_y), (0.0, -half_y)):
        z = trace_floor_z(world, sx, sy, z_high, z_low, ignore)
        if z is not None:
            samples.append(z)
    if len(samples) < 5:
        unreal.log("scene_placement: floor traces hit %d" % len(samples))
        return None, ["floor trace missed the pad"]
    samples.sort()
    floor = samples[len(samples) // 2]
    spread = samples[-1] - samples[0]
    errors = []
    if spread > 50.0:
        errors.append("hill is %.0f cm above the pad" % spread)
    unreal.log("scene_placement: floor samples %s using %.0f" % (
        " ".join("%.0f" % z for z in samples), floor))
    return floor, errors


def snap_contacts(labels, top):
    for label in labels:
        if label == "SM_Size_Island" or label == "SM_Size_WalkPad" or label in ("SM_Size_Kettle", "SM_Size_Bed"):
            continue
        actor = by_label().get(label)
        if actor is None:
            continue
        origin, extent = actor.get_actor_bounds(False)
        delta = top - (origin.z - extent.z)
        loc = actor.get_actor_location()
        actor.set_actor_location(unreal.Vector(loc.x, loc.y, loc.z + delta), False, False)


def pin_to_floor(labels, top):
    """Move any mesh still off the floor, then fail if it is still more than 2 cm off."""
    errors = []
    for label in labels:
        if label == "SM_Size_Island" or label == "SM_Size_WalkPad" or label in ("SM_Size_Kettle", "SM_Size_Bed"):
            continue
        actor = by_label().get(label)
        if actor is None:
            errors.append(label + " missing")
            continue
        for _ in range(2):
            origin, extent = actor.get_actor_bounds(False)
            delta = top - (origin.z - extent.z)
            if abs(delta) <= 2.0:
                break
            loc = actor.get_actor_location()
            actor.set_actor_location(unreal.Vector(loc.x, loc.y, loc.z + delta), False, False)
        origin, extent = actor.get_actor_bounds(False)
        gap = (origin.z - extent.z) - top
        if abs(gap) > 2.0:
            errors.append("%s bottom off by %.1f cm" % (label, gap))
    return errors


def seat_props(top):
    """The kettle sits on the counter. The bed sits on the upper floor."""
    kettle = by_label().get("SM_Size_Kettle")
    if kettle is not None:
        _seat_bottom(kettle, top + 90.0)
    bed = by_label().get("SM_Size_Bed")
    if bed is not None:
        _seat_bottom(bed, top + 500.0)


def _seat_bottom(actor, bottom):
    origin, extent = actor.get_actor_bounds(False)
    delta = bottom - (origin.z - extent.z)
    loc = actor.get_actor_location()
    actor.set_actor_location(unreal.Vector(loc.x, loc.y, loc.z + delta), False, False)


def place_player(player, top):
    actor = None
    for candidate in actors():
        if candidate.get_class().get_name() == "PlayerStart":
            actor = candidate
            break
    if actor is None:
        unreal.log("scene_placement: no PlayerStart")
        return None
    location = unreal.Vector(player["x"] * M, player["y"] * M, top + CAPSULE_HALF + 10.0)
    actor.set_actor_location(location, False, False)
    actor.set_actor_rotation(yaw_rotator(player["yaw"]), False)
    return actor


def stroke_or_ease_errors():
    """A stroke or an ease pad must not be saved into this map."""
    entries = []
    for actor in actors():
        names = []
        try:
            names.append(actor.get_class().get_name())
        except Exception:
            pass
        try:
            for component in actor.get_components_by_class(unreal.ActorComponent):
                names.append(component.get_class().get_name())
        except Exception:
            pass
        entries.append((actor.get_actor_label(), names))
    return size_test_guard.size_test_stroke_errors(entries)


def remove_outside_homestead(keep):
    for actor in list(actors()):
        label = actor.get_actor_label()
        if label in keep or label in KEEP_EXACT:
            continue
        if label.startswith("SM_Size_") or label.startswith("SK_Size_") or label.startswith("NODE_") or label.startswith("CLOUD_") or label.startswith("PILE_"):
            destroy(actor)
            unreal.log("scene_placement: removed " + label)


def _bounds_box(actor):
    origin, extent = actor.get_actor_bounds(False)
    return (origin.x, origin.y, origin.z, extent.x, extent.y, extent.z)


def _boxes_overlap(a, b, pad=2.0):
    return (
        a[0] - a[3] < b[0] + b[3] - pad
        and b[0] - b[3] < a[0] + a[3] - pad
        and a[1] - a[4] < b[1] + b[4] - pad
        and b[1] - b[4] < a[1] + a[4] - pad
        and a[2] - a[5] < b[2] + b[5] - pad
        and b[2] - b[5] < a[2] + a[5] - pad
    )


def _resting(a, b):
    """True when one box only meets the top or bottom of the other."""
    a_bottom = a[2] - a[5]
    a_top = a[2] + a[5]
    b_bottom = b[2] - b[5]
    b_top = b[2] + b[5]
    return abs(a_bottom - b_top) <= 6.0 or abs(b_bottom - a_top) <= 6.0


def _is_structure(label):
    return (
        label.startswith("CabinWall_")
        or label.startswith("ArmoryWall_")
        or label.startswith("PorchCrawl_")
        or label.startswith("CabinRoof_")
        or label.startswith("CabinRamp_")
    )


def _grown_together(left, right):
    pair = tuple(sorted((left, right)))
    return pair in {
        ("SM_Size_HerbBed", "SM_Size_Lupine"),
        ("SM_Size_HerbBed_B", "SM_Size_Lupine_B"),
    }


def clip_errors():
    """Solids must not occupy the same volume. Touching a floor or a counter is not a clip.

    Cabin walls may meet each other. A lupine may occupy its herb bed. Everything else,
    including a new placement, fails the save when its bounds cut through another solid.
    """
    boxes = {}
    for actor in actors():
        label = actor.get_actor_label() or ""
        if not label or label in ("SM_Size_Island", "SM_Size_WalkPad", "SM_Size_Field", "SM_Size_Cottage"):
            continue
        if label.startswith("CabinLight_") or label.startswith("Water_") or label.startswith("Hill_") or label.startswith("CabinRoof_"):
            continue
        if not (
            label.startswith("SM_Size_")
            or label.startswith("SK_Size_")
            or label.startswith("CabinWall_")
            or label.startswith("ArmoryWall_")
            or         label.startswith("PorchCrawl_")
        or label.startswith("CabinRoof_")
        or label.startswith("CabinRamp_")
        or label == "OpeningDog"
        ):
            continue
        boxes[label] = _bounds_box(actor)
    errors = []
    labels = list(boxes)
    for i, left in enumerate(labels):
        for right in labels[i + 1 :]:
            if _is_structure(left) and _is_structure(right):
                continue
            if _grown_together(left, right):
                continue
            a = boxes[left]
            b = boxes[right]
            if not _boxes_overlap(a, b):
                continue
            if _resting(a, b):
                continue
            errors.append(left + " clips " + right)
    return errors


def cells_for(min_x, min_y, max_x, max_y):
    found = set()
    x = min_x
    while x <= max_x:
        y = min_y
        while y <= max_y:
            found.add((int(math.floor(x / CELL)), int(math.floor(y / CELL))))
            y += CELL
        x += CELL
    return found


def validate(player_actor, top):
    errors = []
    solids = {}
    for actor in actors():
        label = actor.get_actor_label()
        if not label.startswith("SM_Size_") or label == "SM_Size_Field" or passable(label):
            continue
        if label == "SM_Size_Island" or label == "SM_Size_WalkPad" or label in ("SM_Size_Kettle", "SM_Size_Bed"):
            continue
        origin, extent = actor.get_actor_bounds(False)
        solids[label] = (
            origin.x - extent.x,
            origin.y - extent.y,
            origin.x + extent.x,
            origin.y + extent.y,
            origin.z - extent.z,
        )
        if abs((origin.z - extent.z) - top) > 2.0:
            errors.append(label + " bottom is off the floor")
    labels = list(solids)
    for i, left in enumerate(labels):
        a = solids[left]
        for right in labels[i + 1 :]:
            b = solids[right]
            if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
                errors.append(left + " overlaps " + right)
    if player_actor is None:
        errors.append("no player start")
        return errors
    loc = player_actor.get_actor_location()
    yaw = player_actor.get_actor_rotation().yaw
    expected_yaw = float(load_metrics()["player"]["yaw"])
    yaw_delta = ((yaw - expected_yaw + 180.0) % 360.0) - 180.0
    if abs(yaw_delta) > 1.0:
        errors.append("player yaw is %.1f" % yaw)
    island = by_label().get("SM_Size_Island")
    pad = load_metrics().get("pad", {"x": 40, "y": 30})
    half_x = float(pad["x"]) * M * 0.5
    half_y = float(pad["y"]) * M * 0.5
    island_loc = island.get_actor_location()
    inset = 500.0
    if not (
        island_loc.x - half_x + inset < loc.x < island_loc.x + half_x - inset
        and island_loc.y - half_y + inset < loc.y < island_loc.y + half_y - inset
    ):
        errors.append("player start is inside the island edge margin")
    occupied = set()
    for label, box in solids.items():
        occupied |= cells_for(box[0], box[1], box[2], box[3])
    player_cells = cells_for(
        loc.x - CAPSULE_RADIUS - CLEARANCE,
        loc.y - CAPSULE_RADIUS - CLEARANCE,
        loc.x + CAPSULE_RADIUS + CLEARANCE,
        loc.y + CAPSULE_RADIUS + CLEARANCE,
    )
    shared = occupied & player_cells
    if shared:
        errors.append("player clearance shares %d grid cells with a solid" % len(shared))
    errors.extend(capsule_clearance(loc, top))
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    ignore = [other for other in actors() if other.get_actor_label() not in ("SM_Size_Island", "SM_Size_WalkPad")]
    hit_z = trace_floor_z(world, loc.x, loc.y, loc.z + 50.0, top - 500.0, ignore)
    if hit_z is None:
        errors.append("player start missed the island")
    elif abs(hit_z - top) > 20.0:
        errors.append("player start hit %.0f cm from the floor" % (hit_z - top))
    errors.extend(garden_and_door(top))
    errors.extend(armory_errors(top))
    errors.extend(clip_errors())
    errors.extend(zipline_ramp_errors(top))
    return errors


def garden_and_door(top):
    """Beds sit on the south apron, and a chest-high ray gets through the door."""
    cottage = by_label().get("SM_Size_Cottage")
    if cottage is None:
        return ["no cottage"]
    errors = []
    origin, extent = cottage.get_actor_bounds(False)
    south = origin.y - extent.y
    for actor in actors():
        label = actor.get_actor_label()
        if not (label.startswith("SM_Size_HerbBed") or label.startswith("SM_Size_Lupine")):
            continue
        loc = actor.get_actor_location()
        yaw = actor.get_actor_rotation().yaw
        if loc.y >= south - 10.0:
            errors.append(label + " is not in front of the south porch")
        if not (origin.x - extent.x - 50.0 < loc.x < origin.x + extent.x + 50.0):
            errors.append(label + " is outside the cottage front")
        if abs(((yaw + 180.0) % 360.0) - 180.0) > 15.0:
            errors.append("%s yaw %.0f does not face the cottage" % (label, yaw))
    loc = cottage.get_actor_location()
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    ignore = [other for other in actors() if not other.get_actor_label().startswith("CabinWall_")]
    chest = top + 150.0
    door = trace_hit(
        world,
        unreal.Vector(loc.x - 150.0, loc.y - 900.0, chest),
        unreal.Vector(loc.x - 150.0, loc.y - 50.0, chest),
        ignore,
    )
    if door is not None and is_cabin(door["label"]):
        errors.append("south door is blocked")
    wall = trace_hit(
        world,
        unreal.Vector(loc.x - 800.0, loc.y, chest),
        unreal.Vector(loc.x - 200.0, loc.y, chest),
        ignore,
    )
    if wall is None or not is_cabin(wall["label"]):
        errors.append("cottage wall does not block")
    errors.extend(room_path(top, loc, world))
    errors.extend(porch_gap_errors())
    errors.extend(sheet_errors())
    errors.extend(walk_cabin(top, loc))
    return errors


def is_cabin(label):
    return label == "SM_Size_Cottage" or (label or "").startswith("CabinWall_") or (label or "").startswith("PorchCrawl_")


def porch_gap_errors():
    """The porch gap fits an 84 cm body and refuses a 160 cm body."""
    west = by_label().get("PorchCrawl_West")
    east = by_label().get("PorchCrawl_East")
    fill = by_label().get("PorchCrawl_Fill")
    if west is None or east is None or fill is None:
        return ["porch crawl is missing"]
    west_face = west.get_actor_location().x + west.get_actor_scale3d().x * 50.0
    east_face = east.get_actor_location().x - east.get_actor_scale3d().x * 50.0
    gap = east_face - west_face
    if gap < 120.0 or gap > 140.0:
        return ["porch gap %.0f cm is not a fit" % gap]
    fill_x = fill.get_actor_location().x
    if not (west_face < fill_x < east_face):
        return ["porch filler is outside the gap"]
    return []


def sheet_errors():
    """Every placed actor must match the metrics sheet in X, Y, and yaw."""
    errors = []
    for item in load_metrics()["homestead"]:
        actor = by_label().get(item["label"])
        if actor is None:
            errors.append(item["label"] + " missing from the sheet")
            continue
        loc = actor.get_actor_location()
        yaw = actor.get_actor_rotation().yaw
        if abs(loc.x - item["x"] * M) > 2.0 or abs(loc.y - item["y"] * M) > 2.0:
            errors.append("%s is off the sheet" % item["label"])
        delta = ((yaw - float(item["yaw"]) + 180.0) % 360.0) - 180.0
        if abs(delta) > 1.0:
            errors.append("%s yaw %.0f is not %s" % (item["label"], yaw, item["yaw"]))
    return errors


def room_path(top, loc, world):
    """The kettle stays in the kitchen, the bed in the couple room, and the capsule fits both doors."""
    errors = []
    kettle = by_label().get("SM_Size_Kettle")
    bed = by_label().get("SM_Size_Bed")
    if kettle is None:
        return ["no kettle"]
    if bed is None:
        return ["no bed"]
    spot = kettle.get_actor_location()
    if not (loc.x + 1650.0 < spot.x < loc.x + 1780.0 and loc.y - 80.0 < spot.y < loc.y + 180.0):
        errors.append("kettle is outside the kitchen")
    bed_loc = bed.get_actor_location()
    if not (loc.x - 400.0 < bed_loc.x < loc.x - 100.0 and loc.y + 1000.0 < bed_loc.y < loc.y + 1300.0):
        errors.append("bed is outside the couple room")
    chest = top + 150.0
    ignore = [other for other in actors() if not other.get_actor_label().startswith("CabinWall_")]
    gap = trace_hit(
        world,
        unreal.Vector(loc.x - 150.0, loc.y - 110.0, chest),
        unreal.Vector(loc.x + 600.0, loc.y - 110.0, chest),
        ignore,
    )
    if gap is not None and is_cabin(gap["label"]):
        errors.append("kitchen door is blocked")
    center = top + CAPSULE_HALF
    for name, x, y in (
        ("south door", loc.x - 150.0, loc.y - 110.0),
        ("kitchen door", loc.x + 600.0, loc.y - 110.0),
    ):
        overlapped = unreal.SystemLibrary.sphere_overlap_actors(
            world,
            unreal.Vector(x, y, center),
            CAPSULE_RADIUS,
            [unreal.ObjectTypeQuery.OBJECT_TYPE_QUERY1],
            None,
            [],
        )
        for actor in overlapped or []:
            if is_cabin(actor.get_actor_label()):
                errors.append(name + " traps the capsule")
    return errors


def capsule_clearance(loc, top):
    """Overlap a sphere the size of the pawn plus 2 m. Ignore the island floor."""
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    center = unreal.Vector(loc.x, loc.y, top + CAPSULE_HALF)
    overlapped = unreal.SystemLibrary.sphere_overlap_actors(
        world,
        center,
        CAPSULE_RADIUS + CLEARANCE,
        [unreal.ObjectTypeQuery.OBJECT_TYPE_QUERY1],
        None,
        [],
    )
    errors = []
    for actor in overlapped or []:
        label = actor.get_actor_label()
        if label == "SM_Size_Island" or label == "SM_Size_WalkPad" or passable(label) or label == "SM_Size_Field" or label in ("SK_Size_Partner", "SK_Size_Child"):
            continue
        errors.append("capsule hits " + label)
    return errors


def walk_cabin(top, loc):
    """Sweep a 42 cm body in, through the rooms, and back out. A hit fails the save."""
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    z = top + CAPSULE_HALF
    points = [(loc.x + x, loc.y + y, z) for x, y in cabin_shell.WALK]
    errors = []
    for index in range(len(points) - 1):
        ax, ay, az = points[index]
        bx, by, bz = points[index + 1]
        label = body_hit(
            world,
            unreal.Vector(ax, ay, az),
            unreal.Vector(bx, by, bz),
        )
        if label is None or label in ("SM_Size_Island", "SM_Size_WalkPad", "SM_Size_Field", "SK_Size_Partner", "SK_Size_Child") or label.startswith("SM_Size_Herb") or label.startswith("SM_Size_Lupine"):
            continue
        errors.append(
            "walk blocked by %s from (%.0f, %.0f) to (%.0f, %.0f)"
            % (label, ax, ay, bx, by)
        )
        break
    if not errors:
        unreal.log("scene_placement: cabin walk enter cross exit clear")
    return errors


def body_hit(world, start, end):
    """A 42 cm sphere along the segment. None means the body fits."""
    hit = None
    try:
        hit = unreal.SystemLibrary.sphere_trace_single(
            world, start, end, CAPSULE_RADIUS,
            unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,
            False, [], unreal.DrawDebugTrace.NONE, True,
        )
    except TypeError:
        hit = unreal.SystemLibrary.sphere_trace_single(
            world, start, end, CAPSULE_RADIUS,
            unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,
            False, [], unreal.DrawDebugTrace.NONE, True,
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
    return actor.get_actor_label() if actor is not None else "unknown"


def armory_walk(ox, oy, top):
    """Sweep a 42 cm body through the armory door, past the table, and back out."""
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    z = top + CAPSULE_HALF
    points = [(ox + x, oy + y, z) for x, y in armory_shell.WALK]
    errors = []
    for index in range(len(points) - 1):
        ax, ay, az = points[index]
        bx, by, bz = points[index + 1]
        label = body_hit(
            world,
            unreal.Vector(ax, ay, az),
            unreal.Vector(bx, by, bz),
        )
        if label is None or label in ("SM_Size_Island", "SM_Size_WalkPad", "SM_Size_Field", "SK_Size_Partner", "SK_Size_Child"):
            continue
        errors.append(
            "armory walk blocked by %s from (%.0f, %.0f) to (%.0f, %.0f)"
            % (label, ax, ay, bx, by)
        )
        break
    if not errors:
        unreal.log("scene_placement: armory walk enter cross exit clear")
    return errors


def armory_errors(top):
    """The armory door opens, its walls block, it stands on the pad, and the armor table is placed."""
    armory = load_metrics().get("armory")
    if not armory:
        return ["no armory in the sheet"]
    if not [a for a in actors() if a.get_actor_label().startswith("ArmoryWall_")]:
        return ["armory walls are missing"]
    ox = float(armory["x"]) * M
    oy = float(armory["y"]) * M
    errors = []
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    only_walls = [other for other in actors() if not other.get_actor_label().startswith("ArmoryWall_")]
    chest = top + 150.0
    door = trace_hit(
        world,
        unreal.Vector(ox - 550.0, oy, chest),
        unreal.Vector(ox + 150.0, oy, chest),
        only_walls,
    )
    if door is not None:
        errors.append("armory door is blocked by " + str(door["label"]))
    wall = trace_hit(
        world,
        unreal.Vector(ox, oy + 500.0, chest),
        unreal.Vector(ox, oy + 100.0, chest),
        only_walls,
    )
    if wall is None or not str(wall["label"]).startswith("ArmoryWall_"):
        errors.append("armory wall does not block")
    only_floor = [other for other in actors() if other.get_actor_label() not in ("SM_Size_Island", "SM_Size_WalkPad")]
    z = trace_floor_z(world, ox, oy, top + 200.0, top - 500.0, only_floor)
    if z is None or abs(z - top) > 20.0:
        errors.append("armory floor is not the pad")
    errors.extend(armory_walk(ox, oy, top))
    for label in ("SM_Size_ArmorTable",):
        if by_label().get(label) is None:
            errors.append(label + " is not placed")
    return errors


def import_cabin_shell():
    filename = cabin_shell.write_obj(
        os.path.join(ROOT, "AssetCreation", "SizeTest", "SM_Size_CabinShell.obj")
    )
    task = unreal.AssetImportTask()
    task.filename = filename
    task.destination_path = MESH_DIR
    task.destination_name = "SM_Size_CabinShell"
    task.automated = True
    task.save = True
    task.replace_existing = True
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    unreal.log("scene_placement: imported cabin shell")


def import_island():
    filename = os.path.join(ROOT, "AssetCreation", "SizeTest", "SM_Size_Island.fbx")
    task = unreal.AssetImportTask()
    task.filename = filename
    task.destination_path = MESH_DIR
    task.destination_name = "SM_Size_Island"
    task.automated = True
    task.save = True
    task.replace_existing = True
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_as_skeletal", False)
    options.set_editor_property("import_animations", False)
    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_STATIC_MESH)
    task.options = options
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    unreal.log("scene_placement: imported island")


def place_walk_pad():
    """A flat cube the pawn stands on. The island mesh is the cone under it."""
    pad = load_metrics().get("pad", {"x": 70, "y": 90, "z": 1})
    cube = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
    if cube is None:
        unreal.log("scene_placement: FAIL no engine cube for the walk pad")
        return False
    actor = by_label().get("SM_Size_WalkPad")
    if actor is None:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.StaticMeshActor, unreal.Vector(0.0, 0.0, 0.0), yaw_rotator(0)
        )
        if actor is None:
            unreal.log("scene_placement: FAIL walk pad did not spawn")
            return False
        actor.set_actor_label("SM_Size_WalkPad")
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    component.set_static_mesh(cube)
    if not paint(actor, "MI_Greybox_Stone"):
        material = cube.get_material(0)
        if material is not None:
            component.set_material(0, material)
            unreal.log("scene_placement: walk pad material " + material.get_path_name())
    actor.set_actor_scale3d(unreal.Vector(float(pad["x"]), float(pad["y"]), float(pad.get("z", 1))))
    thickness = float(pad.get("z", 1)) * M
    actor.set_actor_location(unreal.Vector(0.0, 0.0, 45000.0 - thickness * 0.5), False, False)
    set_collision(actor)
    unreal.log("scene_placement: walk pad %.0f by %.0f m" % (float(pad["x"]), float(pad["y"])))
    return True


def place_opening_reveal(top):
    """Spirit halfway to the cottage. The crest is far enough south that the child, starting at the door, still arrives first at 585 cm/s."""
    for actor in list(actors()):
        if actor.get_actor_label() == "OpeningReveal":
            destroy(actor)
    reveal_class = unreal.load_class(None, "/Script/HomeWorld.HomeWorldOpeningReveal")
    if reveal_class is None:
        unreal.log("scene_placement: FAIL no opening reveal class")
        return False
    spirit_x = -7.0
    spirit_y = -29.0
    crest_x = -6.0
    crest_y = -53.0
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        reveal_class,
        unreal.Vector(spirit_x * M, spirit_y * M, top + 75.0),
        yaw_rotator(0),
    )
    if actor is None:
        unreal.log("scene_placement: FAIL opening reveal did not spawn")
        return False
    actor.set_actor_label("OpeningReveal")
    for component in actor.get_components_by_class(unreal.BoxComponent):
        component.set_relative_location(
            unreal.Vector((crest_x - spirit_x) * M, (crest_y - spirit_y) * M, 150.0),
            False,
            False,
        )
    unreal.log("scene_placement: opening reveal placed")
    return True


INSTANCES = "/Game/HomeWorld/Materials/Instances/"
_INSTANCE_CACHE = {}


def load_instance(name):
    if name in _INSTANCE_CACHE:
        return _INSTANCE_CACHE[name]
    asset = unreal.EditorAssetLibrary.load_asset(INSTANCES + name)
    if asset is None:
        unreal.log("scene_placement: missing material " + name)
    _INSTANCE_CACHE[name] = asset
    return asset


def paint(actor, name):
    """Greybox read. A missing instance is logged and the mesh is left as it is."""
    if actor is None or not name:
        return False
    material = load_instance(name)
    if material is None:
        return False
    painted = False
    for component in actor.get_components_by_class(unreal.StaticMeshComponent):
        count = component.get_num_materials()
        if count < 1:
            count = 1
        for index in range(count):
            component.set_material(index, material)
        painted = True
    return painted


def homestead_color(label):
    """Starting read for sheet props. Stations and the dog swap again at play."""
    if (
        label.startswith("SM_Size_HerbBed")
        or label.startswith("SM_Size_Lupine")
        or label == "SM_Size_Kettle"
        or label == "SM_Size_ArmorTable"
    ):
        return "MI_Greybox_Tan"
    if label == "SM_Size_Bed" or label.startswith("SM_Size_Pine") or label.startswith("SM_Size_Rock"):
        return "MI_Greybox_Stone"
    return None


def marker_instance(item):
    """Color key in Docs/level/L_SizeTest_CONTEXT.md. None leaves the mesh alone."""
    label = item["label"]
    tag = item.get("tag") or ""
    if label.startswith("Water_"):
        return "MI_Greybox_Cyan"
    if tag == "ObservatoryPath":
        return "MI_Greybox_Olive"
    if label.startswith("Hill_"):
        return "MI_Greybox_Purple" if item.get("gated") else "MI_Greybox_Olive"
    if label == "FarmPlot":
        return "MI_Greybox_Tan"
    if tag == "DogHouse" or label == "Observatory":
        return "MI_Greybox_Stone"
    if tag in ("CaveNotch", "FarmGate"):
        return "MI_Greybox_Purple"
    return None


GREYBOX_COLORS = (
    ("MI_Greybox_Stone", (0.62, 0.62, 0.66)),
    ("MI_Greybox_Slate", (0.16, 0.17, 0.20)),
    ("MI_Greybox_Olive", (0.22, 0.62, 0.18)),
    ("MI_Greybox_Tan", (0.92, 0.68, 0.12)),
    ("MI_Greybox_DangerRed", (0.75, 0.07, 0.05)),
    ("MI_Greybox_Cyan", (0.12, 0.72, 0.95)),
    ("MI_Greybox_Purple", (0.55, 0.22, 0.90)),
)


def _greybox_expr(material, expression_cls, x, y):
    return unreal.MaterialEditingLibrary.create_material_expression(material, expression_cls, x, y)


def _greybox_mask(material, x, y, channel):
    node = _greybox_expr(material, unreal.MaterialExpressionComponentMask, x, y)
    node.set_editor_property("r", channel == "r")
    node.set_editor_property("g", channel == "g")
    node.set_editor_property("b", channel == "b")
    node.set_editor_property("a", False)
    return node


def _greybox_has_param(material, name):
    try:
        expressions = unreal.MaterialEditingLibrary.get_material_expressions(material)
    except Exception:
        return False
    for expr in expressions:
        try:
            if str(expr.get_editor_property("parameter_name")) == name:
                return True
        except Exception:
            continue
    return False


def _greybox_checker2d(material, axis_a, axis_b, x, y):
    """0 or 1 from two axes. The face's own axis is left out, so a flat surface does not strobe."""
    floor_a = _greybox_expr(material, unreal.MaterialExpressionFloor, x, y)
    floor_b = _greybox_expr(material, unreal.MaterialExpressionFloor, x, y + 70)
    unreal.MaterialEditingLibrary.connect_material_expressions(axis_a, "", floor_a, "")
    unreal.MaterialEditingLibrary.connect_material_expressions(axis_b, "", floor_b, "")
    added = _greybox_expr(material, unreal.MaterialExpressionAdd, x + 160, y + 20)
    unreal.MaterialEditingLibrary.connect_material_expressions(floor_a, "", added, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(floor_b, "", added, "B")
    half = _greybox_expr(material, unreal.MaterialExpressionConstant, x + 160, y + 100)
    half.set_editor_property("r", 0.5)
    halved = _greybox_expr(material, unreal.MaterialExpressionMultiply, x + 320, y + 40)
    unreal.MaterialEditingLibrary.connect_material_expressions(added, "", halved, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(half, "", halved, "B")
    frac = _greybox_expr(material, unreal.MaterialExpressionFrac, x + 480, y + 40)
    unreal.MaterialEditingLibrary.connect_material_expressions(halved, "", frac, "")
    two = _greybox_expr(material, unreal.MaterialExpressionConstant, x + 480, y + 120)
    two.set_editor_property("r", 2.0)
    bit = _greybox_expr(material, unreal.MaterialExpressionMultiply, x + 640, y + 40)
    unreal.MaterialEditingLibrary.connect_material_expressions(frac, "", bit, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(two, "", bit, "B")
    return bit


def _build_greybox_read(material):
    """Lit grey mixed with the key color, then a 1 m checker across each face."""
    material.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_DEFAULT_LIT)
    unreal.MaterialEditingLibrary.delete_all_material_expressions(material)
    tint = _greybox_expr(material, unreal.MaterialExpressionVectorParameter, -980, 0)
    tint.set_editor_property("parameter_name", unreal.Name("BaseColor"))
    tint.set_editor_property("default_value", unreal.LinearColor(0.5, 0.5, 0.5, 1.0))
    grey = _greybox_expr(material, unreal.MaterialExpressionConstant3Vector, -980, 180)
    grey.set_editor_property("constant", unreal.LinearColor(0.22, 0.22, 0.22, 1.0))
    mix = _greybox_expr(material, unreal.MaterialExpressionLinearInterpolate, -620, 40)
    mix_amount = _greybox_expr(material, unreal.MaterialExpressionConstant, -820, 220)
    mix_amount.set_editor_property("r", 0.55)
    unreal.MaterialEditingLibrary.connect_material_expressions(grey, "", mix, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(tint, "", mix, "B")
    unreal.MaterialEditingLibrary.connect_material_expressions(mix_amount, "", mix, "Alpha")

    world = _greybox_expr(material, unreal.MaterialExpressionWorldPosition, -980, 420)
    grid = _greybox_expr(material, unreal.MaterialExpressionScalarParameter, -980, 560)
    grid.set_editor_property("parameter_name", unreal.Name("GreyboxGridSize"))
    grid.set_editor_property("default_value", 100.0)
    cell = _greybox_expr(material, unreal.MaterialExpressionDivide, -760, 460)
    unreal.MaterialEditingLibrary.connect_material_expressions(world, "", cell, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(grid, "", cell, "B")
    cell_x = _greybox_mask(material, -560, 400, "r")
    cell_y = _greybox_mask(material, -560, 470, "g")
    cell_z = _greybox_mask(material, -560, 540, "b")
    unreal.MaterialEditingLibrary.connect_material_expressions(cell, "", cell_x, "")
    unreal.MaterialEditingLibrary.connect_material_expressions(cell, "", cell_y, "")
    unreal.MaterialEditingLibrary.connect_material_expressions(cell, "", cell_z, "")
    check_yz = _greybox_checker2d(material, cell_y, cell_z, -360, 700)
    check_xz = _greybox_checker2d(material, cell_x, cell_z, -360, 900)
    check_xy = _greybox_checker2d(material, cell_x, cell_y, -360, 1100)
    normal = _greybox_expr(material, unreal.MaterialExpressionPixelNormalWS, -980, 760)
    normal_abs = _greybox_expr(material, unreal.MaterialExpressionAbs, -780, 760)
    unreal.MaterialEditingLibrary.connect_material_expressions(normal, "", normal_abs, "")
    weight_x = _greybox_mask(material, -600, 720, "r")
    weight_y = _greybox_mask(material, -600, 790, "g")
    weight_z = _greybox_mask(material, -600, 860, "b")
    unreal.MaterialEditingLibrary.connect_material_expressions(normal_abs, "", weight_x, "")
    unreal.MaterialEditingLibrary.connect_material_expressions(normal_abs, "", weight_y, "")
    unreal.MaterialEditingLibrary.connect_material_expressions(normal_abs, "", weight_z, "")
    weight_sum_xy = _greybox_expr(material, unreal.MaterialExpressionAdd, -420, 760)
    weight_sum = _greybox_expr(material, unreal.MaterialExpressionAdd, -250, 800)
    unreal.MaterialEditingLibrary.connect_material_expressions(weight_x, "", weight_sum_xy, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(weight_y, "", weight_sum_xy, "B")
    unreal.MaterialEditingLibrary.connect_material_expressions(weight_sum_xy, "", weight_sum, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(weight_z, "", weight_sum, "B")
    share_x = _greybox_expr(material, unreal.MaterialExpressionDivide, -60, 720)
    share_y = _greybox_expr(material, unreal.MaterialExpressionDivide, -60, 800)
    share_z = _greybox_expr(material, unreal.MaterialExpressionDivide, -60, 880)
    unreal.MaterialEditingLibrary.connect_material_expressions(weight_x, "", share_x, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(weight_sum, "", share_x, "B")
    unreal.MaterialEditingLibrary.connect_material_expressions(weight_y, "", share_y, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(weight_sum, "", share_y, "B")
    unreal.MaterialEditingLibrary.connect_material_expressions(weight_z, "", share_z, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(weight_sum, "", share_z, "B")
    part_x = _greybox_expr(material, unreal.MaterialExpressionMultiply, 140, 720)
    part_y = _greybox_expr(material, unreal.MaterialExpressionMultiply, 140, 800)
    part_z = _greybox_expr(material, unreal.MaterialExpressionMultiply, 140, 880)
    unreal.MaterialEditingLibrary.connect_material_expressions(check_yz, "", part_x, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(share_x, "", part_x, "B")
    unreal.MaterialEditingLibrary.connect_material_expressions(check_xz, "", part_y, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(share_y, "", part_y, "B")
    unreal.MaterialEditingLibrary.connect_material_expressions(check_xy, "", part_z, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(share_z, "", part_z, "B")
    part_xy = _greybox_expr(material, unreal.MaterialExpressionAdd, 320, 760)
    checker = _greybox_expr(material, unreal.MaterialExpressionAdd, 480, 800)
    unreal.MaterialEditingLibrary.connect_material_expressions(part_x, "", part_xy, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(part_y, "", part_xy, "B")
    unreal.MaterialEditingLibrary.connect_material_expressions(part_xy, "", checker, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(part_z, "", checker, "B")
    sentinel = _greybox_expr(material, unreal.MaterialExpressionScalarParameter, -980, 980)
    sentinel.set_editor_property("parameter_name", unreal.Name("GreyboxTriplanar"))
    sentinel.set_editor_property("default_value", 1.0)
    dark_amount = _greybox_expr(material, unreal.MaterialExpressionConstant, -620, 300)
    dark_amount.set_editor_property("r", 0.55)
    dark = _greybox_expr(material, unreal.MaterialExpressionMultiply, -400, 240)
    unreal.MaterialEditingLibrary.connect_material_expressions(mix, "", dark, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(dark_amount, "", dark, "B")
    checked = _greybox_expr(material, unreal.MaterialExpressionLinearInterpolate, 700, 80)
    unreal.MaterialEditingLibrary.connect_material_expressions(dark, "", checked, "A")
    unreal.MaterialEditingLibrary.connect_material_expressions(mix, "", checked, "B")
    unreal.MaterialEditingLibrary.connect_material_expressions(checker, "", checked, "Alpha")
    unreal.MaterialEditingLibrary.connect_material_property(
        checked, "", unreal.MaterialProperty.MP_BASE_COLOR
    )
    rough = _greybox_expr(material, unreal.MaterialExpressionConstant, 700, 260)
    rough.set_editor_property("r", 0.85)
    unreal.MaterialEditingLibrary.connect_material_property(
        rough, "", unreal.MaterialProperty.MP_ROUGHNESS
    )
    metal = _greybox_expr(material, unreal.MaterialExpressionConstant, 700, 380)
    metal.set_editor_property("r", 0.0)
    unreal.MaterialEditingLibrary.connect_material_property(
        metal, "", unreal.MaterialProperty.MP_METALLIC
    )
    unreal.MaterialEditingLibrary.recompile_material(material)
    unreal.EditorAssetLibrary.save_asset("/Game/HomeWorld/Materials/Masters/M_GreyboxRead")


def ensure_greybox_read_master():
    """One lit master. The key color is mixed into a grey base so the sun still models the mesh."""
    path = "/Game/HomeWorld/Materials/Masters/M_GreyboxRead"
    material = None
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        material = unreal.EditorAssetLibrary.load_asset(path)
    else:
        material = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            "M_GreyboxRead",
            "/Game/HomeWorld/Materials/Masters",
            unreal.Material,
            unreal.MaterialFactoryNew(),
        )
    if material is None:
        unreal.log("scene_placement: greybox read master was not created")
        return None
    if not _greybox_has_param(material, "GreyboxTriplanar"):
        _build_greybox_read(material)
        unreal.log("scene_placement: greybox checker uses the face, not the axis it sits on")
    return material


def ensure_greybox_palette():
    """Flat unlit reads. The lit cabin instances and the spirit master do not show a hue here."""
    master = ensure_greybox_read_master()
    if master is None:
        unreal.log("scene_placement: greybox palette skipped, no read master")
        return False
    for name, rgb in GREYBOX_COLORS:
        path = INSTANCES + name
        mi = None
        if unreal.EditorAssetLibrary.does_asset_exist(path):
            mi = unreal.EditorAssetLibrary.load_asset(path)
        else:
            factory = unreal.MaterialInstanceConstantFactoryNew()
            try:
                factory.set_editor_property("initial_parent", master)
            except Exception:
                pass
            mi = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
                name, "/Game/HomeWorld/Materials/Instances", unreal.MaterialInstanceConstant, factory
            )
        if mi is None:
            unreal.log("scene_placement: greybox palette missing " + name)
            continue
        color = unreal.LinearColor(rgb[0], rgb[1], rgb[2], 1.0)
        try:
            unreal.MaterialEditingLibrary.set_material_instance_parent(mi, master)
        except Exception as exc:
            unreal.log("scene_placement: greybox palette parent " + str(exc))
        for param in ("BaseColor", "Emissive"):
            try:
                unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(mi, param, color)
            except Exception as exc:
                unreal.log("scene_placement: greybox palette %s %s" % (param, exc))
        try:
            unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mi, "NightMix", 0.0)
        except Exception:
            pass
        try:
            unreal.MaterialEditingLibrary.update_material_instance(mi)
        except Exception:
            pass
        unreal.EditorAssetLibrary.save_asset(path)
        _INSTANCE_CACHE[name] = mi
    unreal.log("scene_placement: greybox palette ready")
    return True


def ensure_greybox_red():
    """One unlit red instance of M_SpiritUnlit. No new master. Runtime tint covers a failed create."""
    name = "MI_Greybox_DangerRed"
    path = INSTANCES + name
    master = unreal.EditorAssetLibrary.load_asset("/Game/HomeWorld/Materials/Masters/M_SpiritUnlit")
    if master is None:
        unreal.log("scene_placement: greybox red not created, no M_SpiritUnlit")
        return None
    mi = None
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        mi = unreal.EditorAssetLibrary.load_asset(path)
    else:
        factory = unreal.MaterialInstanceConstantFactoryNew()
        try:
            factory.set_editor_property("initial_parent", master)
        except Exception:
            pass
        mi = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            name, "/Game/HomeWorld/Materials/Instances", unreal.MaterialInstanceConstant, factory
        )
    if mi is None:
        unreal.log("scene_placement: greybox red not created, runtime tint will cover it")
        return None
    red = unreal.LinearColor(0.75, 0.07, 0.05, 1.0)
    try:
        unreal.MaterialEditingLibrary.set_material_instance_parent(mi, master)
    except Exception as exc:
        unreal.log("scene_placement: greybox red parent " + str(exc))
    for param in ("BaseColor", "Emissive"):
        try:
            unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(mi, param, red)
        except Exception as exc:
            unreal.log("scene_placement: greybox red %s %s" % (param, exc))
    try:
        unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mi, "NightMix", 0.0)
    except Exception as exc:
        unreal.log("scene_placement: greybox red NightMix " + str(exc))
    try:
        unreal.MaterialEditingLibrary.update_material_instance(mi)
    except Exception:
        pass
    unreal.EditorAssetLibrary.save_asset(path)
    unreal.log("scene_placement: greybox red " + mi.get_path_name())
    return mi


def sheet_collision(actor, mode):
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    if component is None:
        return
    if mode == "block":
        component.set_collision_profile_name("BlockAll")
        component.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
        return
    if mode == "overlap":
        component.set_collision_enabled(unreal.CollisionEnabled.QUERY_ONLY)
        component.set_collision_response_to_all_channels(unreal.CollisionResponseType.ECR_OVERLAP)
        return
    component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)


GRAPH_KINDS = ("peak", "spring", "hot_spring", "pond", "path_sample")
GRAPH_EDGES = ("river", "ridge", "walk")


def sheet_rows(metrics):
    rows = {}
    for key in ("water", "steps", "samples"):
        for item in metrics.get(key, []):
            rows[item["label"]] = (key, item)
    return rows


def graph_tag_names(metrics, label):
    graph = metrics.get("graph") or {}
    names = []
    for node in graph.get("nodes", []):
        if node.get("label") == label:
            names.append("GRAPH_" + str(node.get("kind")))
    for edge in graph.get("edges", []):
        if label in edge.get("labels", []):
            names.append("GRAPH_" + str(edge.get("id")))
    return names


def set_tags(actor, names):
    actor.set_editor_property("tags", [unreal.Name(name) for name in names])


def actor_tag_names(actor):
    return [str(tag) for tag in actor.get_editor_property("tags")]


def graph_errors(metrics):
    """Name the cubes the sheet already has. Do not add a height or a heightfield."""
    errors = []
    graph = metrics.get("graph")
    if not isinstance(graph, dict):
        return ["graph is missing"]
    rows = sheet_rows(metrics)
    nodes = graph.get("nodes")
    edges = graph.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        return ["graph has no nodes and edges"]
    kinds = {}
    for node in nodes:
        kind = node.get("kind")
        label = node.get("label")
        if kind not in GRAPH_KINDS:
            errors.append("graph node %s is not a kept kind" % node.get("id"))
            continue
        if label not in rows:
            errors.append("graph node %s has no sheet row" % label)
            continue
        kinds.setdefault(kind, []).append(label)
    for kind in GRAPH_KINDS:
        if kind not in kinds:
            errors.append("graph is missing " + kind)
    edge_ids = []
    edge_labels = {}
    for edge in edges:
        edge_id = edge.get("id")
        if edge_id in edge_labels:
            errors.append("graph edge %s is listed twice" % edge_id)
            continue
        edge_ids.append(edge_id)
        labels = edge.get("labels") or []
        edge_labels[edge_id] = labels
        if edge_id not in GRAPH_EDGES:
            errors.append("graph edge %s is not a kept edge" % edge_id)
            continue
        for label in labels:
            if label not in rows:
                errors.append("graph edge %s names %s, which is not on the sheet" % (edge_id, label))
                continue
            group, item = rows[label]
            if edge_id == "river" and group != "water":
                errors.append(label + " is on the river and is not water")
            if edge_id == "ridge" and group != "steps":
                errors.append(label + " is on the ridge and is not a hill step")
            if edge_id == "walk":
                if group != "samples" or float(item.get("bottom", 0)) != 0.0:
                    errors.append(label + " is on the walk and is not at pad height")
        if edge_id == "walk" and edge.get("flat") is not True:
            errors.append("walk edge is not flat")
    for edge_id in GRAPH_EDGES:
        if edge_id not in edge_ids:
            errors.append("graph is missing the " + edge_id)
    for label in kinds.get("path_sample", []):
        if label not in edge_labels.get("walk", []):
            errors.append(label + " is a path sample off the walk")
    for kind, edge_id in (("spring", "river"), ("hot_spring", "river"), ("pond", "river")):
        for label in kinds.get(kind, []):
            if label not in edge_labels.get(edge_id, []):
                errors.append(label + " is off the " + edge_id)
    found = by_label()
    if not errors:
        for label, (group, item) in rows.items():
            expected = graph_tag_names(metrics, label)
            if not expected and not (group == "steps" and item.get("gated")):
                continue
            actor = found.get(label)
            if group == "steps" and item.get("gated"):
                if actor is not None:
                    errors.append(label + " is gated and still placed")
                continue
            if not expected:
                continue
            if actor is None:
                errors.append(label + " is on the graph and not placed")
                continue
            present = actor_tag_names(actor)
            for name in expected:
                if name not in present:
                    errors.append(label + " is missing tag " + name)
    if not errors:
        for edge_id in GRAPH_EDGES:
            count = len(edge_labels.get(edge_id, []))
            unreal.log("scene_placement: graph edge %s %d" % (edge_id, count))
        unreal.log("scene_placement: graph heightfield skipped")
    return errors


def place_island_frames(metrics, top_cm):
    """Water, hill steps, and samples from the sheet. The top step stays unspawned until a glide."""
    labels = []
    floor_m = float(top_cm) / M
    wanted = {item["label"] for item in metrics.get("water", [])}
    for actor in list(actors()):
        label = actor.get_actor_label()
        if label.startswith("Water_") and label not in wanted:
            destroy(actor)
    for item in metrics.get("water", []):
        size = item["size"]
        bottom = float(item.get("bottom", 0))
        actor = place_cube(
            item["label"],
            item["x"],
            item["y"],
            floor_m + bottom + float(size[2]) * 0.5,
            0,
            size,
        )
        if actor is None:
            continue
        sheet_collision(actor, "none")
        set_tags(actor, ["WaterSheet"] + graph_tag_names(metrics, item["label"]))
        paint(actor, marker_instance(item))
        labels.append(item["label"])
    for item in metrics.get("steps", []):
        if item.get("gated"):
            existing = by_label().get(item["label"])
            if existing is not None:
                destroy(existing)
            continue
        size = item["size"]
        bottom = float(item.get("bottom", 0))
        actor = place_cube(
            item["label"],
            item["x"],
            item["y"],
            floor_m + bottom + float(size[2]) * 0.5,
            0,
            size,
        )
        if actor is None:
            continue
        sheet_collision(actor, "block")
        set_tags(actor, ["HillStep"] + graph_tag_names(metrics, item["label"]))
        paint(actor, marker_instance(item))
        labels.append(item["label"])
    for item in metrics.get("samples", []):
        size = item["size"]
        bottom = float(item.get("bottom", 0))
        actor = place_cube(
            item["label"],
            item["x"],
            item["y"],
            floor_m + bottom + float(size[2]) * 0.5,
            0,
            size,
        )
        if actor is None:
            continue
        sheet_collision(actor, item.get("collision", "none"))
        names = []
        if item.get("tag"):
            names.append(item["tag"])
        names.extend(graph_tag_names(metrics, item["label"]))
        if names:
            set_tags(actor, names)
        paint(actor, marker_instance(item))
        labels.append(item["label"])
    unreal.log("scene_placement: island frames %d" % len(labels))
    return labels


def _spawn_zipline(label, perch, landing, stair_a, stair_b, stairs_at_perch):
    for actor in list(actors()):
        if actor.get_actor_label() == label:
            destroy(actor)
    zipline_class = unreal.load_class(None, "/Script/HomeWorld.HomeWorldOpeningZipline")
    if zipline_class is None:
        unreal.log("scene_placement: FAIL no zipline class")
        return False
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(zipline_class, perch, yaw_rotator(0))
    if actor is None:
        unreal.log("scene_placement: FAIL zipline did not spawn")
        return False
    actor.set_actor_label(label)
    actor.set_line(perch, landing)
    actor.set_stairs(stair_a, stair_b, stairs_at_perch)
    tag_actor(actor, "NODE_ZIPLINE")
    return True


def place_opening_zipline(top):
    """Northwest corner down to the pond, and the research hill down to the northeast corner.

    The ramp meshes are 180 cm wide and the perch pad is 300 by 240. A perch
    sitting on the corner puts that width through the wall. The ride point is
    moved outside the shell by the perch half-size so the ramp's inner edge
    meets the wall instead of cutting it. Stair directions stay along the two
    outside faces. Widths match HomeWorldOpeningZipline.cpp.
    """
    floor_m = float(top) / M
    cottage = by_label().get("SM_Size_Cottage")
    if cottage is None:
        unreal.log("scene_placement: FAIL no cottage for the zipline")
        return False
    origin = cottage.get_actor_location()
    nw = _outside_corner(origin, "nw", 150.0, 120.0)
    ne = _outside_corner(origin, "ne", 120.0, 120.0)
    pond = _spawn_zipline(
        "OpeningZipline",
        unreal.Vector(nw[0], nw[1], top + 400.0),
        vec(-40.5, 2.0, floor_m + 1.5),
        unreal.Vector(0.0, -1.0, 0.0),
        unreal.Vector(1.0, 0.0, 0.0),
        True,
    )
    hill = _spawn_zipline(
        "OpeningZiplineHill",
        vec(32.0, 22.0, floor_m + 6.0),
        unreal.Vector(ne[0], ne[1], top + 150.0),
        unreal.Vector(-1.0, 0.0, 0.0),
        unreal.Vector(0.0, -1.0, 0.0),
        False,
    )
    if pond and hill:
        unreal.log("scene_placement: ziplines outside the shell corners")
    return pond and hill


# HomeWorldOpeningZipline.cpp: ramp width 180, perch 300 by 240, end perch 240.
RAMP_HALF = 90.0
RAMP_OFFSET = 160.0
RAMP_SLOPE_DEG = 22.0


def _outside_corner(origin, corner, half_x, half_y):
    """A pad of half_x by half_y must sit outside the shell, just clear of the wall."""
    wall = cabin_shell.WALL * 0.5 + 2.0
    if corner == "nw":
        x = origin.x + cabin_shell.SHELL_MIN_X - wall - half_x
        y = origin.y + cabin_shell.SHELL_MAX_Y + wall + half_y
    else:
        x = origin.x + cabin_shell.SHELL_MAX_X + wall + half_x
        y = origin.y + cabin_shell.SHELL_MAX_Y + wall + half_y
    return (x, y)


def _ramp_centerline(base, direction, pad_z):
    rise = max(base.z - pad_z, 40.0)
    run = rise / math.tan(math.radians(RAMP_SLOPE_DEG))
    top = unreal.Vector(base.x + direction.x * RAMP_OFFSET, base.y + direction.y * RAMP_OFFSET, base.z)
    bottom = unreal.Vector(top.x + direction.x * run, top.y + direction.y * run, pad_z)
    return top, bottom


def _dist_xy_to_box(px, py, box):
    min_x = box[0] - box[3]
    max_x = box[0] + box[3]
    min_y = box[1] - box[4]
    max_y = box[1] + box[4]
    dx = max(min_x - px, 0.0, px - max_x)
    dy = max(min_y - py, 0.0, py - max_y)
    return math.hypot(dx, dy)


def _z_hits_box(z, box):
    return (box[2] - box[5]) - 2.0 < z < (box[2] + box[5]) + 2.0


def zipline_ramp_errors(top):
    """A ramp clips a wall when its 90 cm half-width reaches that wall.

    The whole zipline actor is not tested: its cable span would overlap the
    yard on purpose. Only the two ramp centerlines are tested, against the
    cottage and armory shells.
    """
    cottage = by_label().get("SM_Size_Cottage")
    if cottage is None:
        return ["no cottage for the zipline ramps"]
    origin = cottage.get_actor_location()
    pad_z = top
    boxes = []
    for box in cabin_shell.BOXES:
        boxes.append((origin.x + box[0], origin.y + box[1], origin.z + box[2], box[3] * 0.5, box[4] * 0.5, box[5] * 0.5))
    armory = load_metrics().get("armory")
    if armory:
        ax = float(armory["x"]) * M
        ay = float(armory["y"]) * M
        for box in armory_shell.BOXES:
            boxes.append((ax + box[0], ay + box[1], top + box[2], box[3] * 0.5, box[4] * 0.5, box[5] * 0.5))
    nw = _outside_corner(origin, "nw", 150.0, 120.0)
    ne = _outside_corner(origin, "ne", 120.0, 120.0)
    lines = (
        ("OpeningZipline", unreal.Vector(nw[0], nw[1], top + 400.0), (unreal.Vector(0.0, -1.0, 0.0), unreal.Vector(1.0, 0.0, 0.0))),
        ("OpeningZiplineHill", unreal.Vector(ne[0], ne[1], top + 150.0), (unreal.Vector(-1.0, 0.0, 0.0), unreal.Vector(0.0, -1.0, 0.0))),
    )
    errors = []
    for label, base, directions in lines:
        segments = [_ramp_centerline(base, direction, pad_z) for direction in directions]
        for index, (start, end) in enumerate(segments):
            for step in range(9):
                t = step / 8.0
                px = start.x + (end.x - start.x) * t
                py = start.y + (end.y - start.y) * t
                pz = start.z + (end.z - start.z) * t
                for box in boxes:
                    if not _z_hits_box(pz, box):
                        continue
                    if _dist_xy_to_box(px, py, box) < RAMP_HALF - 2.0:
                        errors.append("%s ramp %d clips a wall" % (label, index + 1))
                        break
                else:
                    continue
                break
        gap = math.hypot(segments[0][0].x - segments[1][0].x, segments[0][0].y - segments[1][0].y)
        if gap < RAMP_HALF * 2.0:
            errors.append("%s ramps overlap each other (%.0f cm)" % (label, gap))
    return errors


def place_opening_dog(top):
    """Beat 4: the injured dog in the north backyard, from the sheet. Destroy and re-spawn, like the reveal."""
    dog = load_metrics().get("dog")
    if dog is None:
        unreal.log("scene_placement: no dog row, nothing to place")
        return True
    for actor in list(actors()):
        if actor.get_actor_label() == "OpeningDog":
            destroy(actor)
    dog_class = unreal.load_class(None, "/Script/HomeWorld.HomeWorldOpeningDog")
    if dog_class is None:
        unreal.log("scene_placement: FAIL no opening dog class")
        return False
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        dog_class,
        unreal.Vector(float(dog["x"]) * M, float(dog["y"]) * M, top),
        yaw_rotator(float(dog["yaw"])),
    )
    if actor is None:
        unreal.log("scene_placement: FAIL opening dog did not spawn")
        return False
    actor.set_actor_label("OpeningDog")
    unreal.log(
        "scene_placement: opening dog placed (%.1f, %.1f) yaw %.0f"
        % (float(dog["x"]), float(dog["y"]), float(dog["yaw"]))
    )
    return True


DOG_LANE_CM = 900.0
DOG_KNOCK_CM = 400.0


def dog_errors(top):
    """The dog stands on the pad with a clear nine-metre approach lane and 2.8 m of clearance."""
    dog = load_metrics().get("dog")
    if dog is None:
        return []
    actor = by_label().get("OpeningDog")
    if actor is None:
        return ["no OpeningDog at the sheet spot"]
    errors = []
    loc = actor.get_actor_location()
    if abs(loc.x - float(dog["x"]) * M) > 5.0 or abs(loc.y - float(dog["y"]) * M) > 5.0:
        errors.append("OpeningDog is off the sheet spot")
    if "OpeningDog" not in actor.get_class().get_name():
        errors.append("OpeningDog is not the dog class")
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    walkables = ("SM_Size_Island", "SM_Size_WalkPad")
    ignore = [other for other in actors() if other.get_actor_label() not in walkables]
    ground = trace_floor_z(world, loc.x, loc.y, loc.z + 100.0, top - 300.0, ignore)
    if ground is None or abs(ground - top) > 20.0:
        errors.append("OpeningDog is not standing on the walk pad")
    probe = unreal.Vector(loc.x, loc.y - DOG_LANE_CM, top + 160.0)
    body = unreal.Vector(loc.x, loc.y - DOG_KNOCK_CM, top + 160.0)
    blocked = trace_hit(world, probe, body, [])
    if blocked is not None:
        errors.append("dog approach lane is blocked by %s" % blocked.get("label"))
    for step in range(10):
        t = step / 9.0
        y = probe.y + (DOG_LANE_CM - DOG_KNOCK_CM) * t
        z = trace_floor_z(world, probe.x, y, top + 100.0, top - 300.0, ignore)
        if z is None or abs(z - top) > 20.0:
            errors.append("dog approach lane leaves the pad")
            break
    for other in actors():
        label = other.get_actor_label() or ""
        if not label or label in walkables or label == "SM_Size_Field":
            continue
        if label.startswith("Water_") or label.startswith("Hill_") or label in ("FarmPlot", "CaveNotch"):
            continue
        if not (
            label.startswith("SM_Size_")
            or label.startswith("SK_Size_")
            or label.startswith("CabinWall")
            or label.startswith("ArmoryWall")
        ):
            continue
        origin, extent = other.get_actor_bounds(False)
        dx = max(origin.x - extent.x - loc.x, 0.0, loc.x - (origin.x + extent.x))
        dy = max(origin.y - extent.y - loc.y, 0.0, loc.y - (origin.y + extent.y))
        if (dx * dx + dy * dy) ** 0.5 < 280.0:
            errors.append("OpeningDog shares 2.8 m with " + label)
            break
    if not errors:
        unreal.log("scene_placement: opening dog staged with a clear approach lane")
    return errors


def run(import_mesh=True):
    editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if editor.is_in_play_in_editor():
        unreal.log("scene_placement: end play before applying")
        editor.editor_request_end_play()
        return 1
    metrics = load_metrics()
    ensure_greybox_palette()
    if import_mesh:
        import_island()
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(MAP_PATH)
    labels = []
    for item in metrics["homestead"]:
        if str(item["mesh"]).startswith("SK_"):
            place_skeletal(
                item["label"],
                item["mesh"],
                item["x"],
                item["y"],
                item["z"],
                item["yaw"],
                float(item.get("scale", 1.0)),
            )
        elif str(item["mesh"]) == "Cube":
            place_cube(
                item["label"],
                item["x"],
                item["y"],
                item["z"],
                item["yaw"],
                item.get("size", [1.0, 1.0, 1.0]),
            )
        else:
            place_static(
                item["label"],
                item["mesh"],
                item["x"],
                item["y"],
                item["z"],
                item["yaw"],
                float(item.get("scale", 1.0)),
                float(item.get("scale_z", 1.0)),
            )
        labels.append(item["label"])
    for label in labels:
        actor = by_label().get(label)
        if actor is not None:
            set_collision(actor)
            if label == "SM_Size_HerbBed":
                tag_actor(actor, "NODE_GARDEN", "NODE_GARDEN_WEST")
            elif label.startswith("SM_Size_HerbBed"):
                tag_actor(actor, "NODE_GARDEN", "NODE_GARDEN_EAST")
            elif label == "SM_Size_Bed":
                tag_actor(actor, "NODE_BED")
            elif label == "SM_Size_Kettle":
                tag_actor(actor, "NODE_KETTLE")
            elif label == "SM_Size_ArmorTable":
                tag_actor(actor, "NODE_ARMOR_TABLE")
            color = homestead_color(label)
            if color:
                paint(actor, color)
            elif label == "SK_Size_Partner":
                tag_actor(actor, "NPC_PARTNER")
                stand_like_player(actor)
            elif label == "SK_Size_Child":
                tag_actor(actor, "NPC_CHILD")
                stand_like_player(actor)
    if not set_slab_collision():
        return 1
    if not place_walk_pad():
        return 1
    top, floor_errors = measure_floor()
    if top is None:
        for error in floor_errors:
            unreal.log("scene_placement: FAIL " + error)
        unreal.log("scene_placement: not saved")
        return 1
    snap_contacts(labels, top)
    frame_labels = place_island_frames(metrics, top)
    if not spawn_cabin_walls():
        unreal.log("scene_placement: not saved")
        return 1
    if not spawn_armory_walls(top):
        unreal.log("scene_placement: not saved")
        return 1
    plains = metrics["plains"]
    field = place_static(
        plains["label"], plains["mesh"], plains["x"], plains["y"], plains["z"], plains["yaw"], plains["scale"]
    )
    if field is not None:
        field.set_actor_scale3d(unreal.Vector(plains["scale"], plains["scale"], 1.0))
        set_collision(field)
    keep = set(labels)
    keep.add(plains["label"])
    keep.add("SM_Size_WalkPad")
    keep.update(frame_labels)
    remove_outside_homestead(keep)
    player = place_player(metrics["player"], top)
    if not place_opening_dog(top):
        unreal.log("scene_placement: not saved")
        return 1
    if not place_opening_zipline(top):
        unreal.log("scene_placement: not saved")
        return 1
    errors = pin_to_floor(labels, top)
    seat_props(top)
    errors.extend(floor_errors)
    errors.extend(validate(player, top))
    errors.extend(opening_sightline(top))
    errors.extend(dog_errors(top))
    errors.extend(stroke_or_ease_errors())
    errors.extend(graph_errors(metrics))
    for error in errors:
        unreal.log("scene_placement: FAIL " + error)
    if errors:
        unreal.log("scene_placement: not saved")
        return 1
    if not place_opening_reveal(top):
        unreal.log("scene_placement: not saved")
        return 1
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
    yaw = player.get_actor_rotation().yaw
    loc = player.get_actor_location()
    unreal.log(
        "scene_placement: saved top %.1f player (%.0f, %.0f, %.0f) yaw %.1f"
        % (top, loc.x, loc.y, loc.z, yaw)
    )
    return 0


def _is_copse(label):
    return (
        label.startswith("SM_Size_Copse")
        or label.startswith("SM_Size_Pine")
        or label.startswith("SM_Size_Rock")
    )


def opening_sightline(top):
    """Trees and rocks hide the cottage. The start stands on the walk pad."""
    player = None
    for candidate in actors():
        if candidate.get_class().get_name() == "PlayerStart":
            player = candidate
            break
    if player is None:
        return ["no player start for the sightline"]
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    loc = player.get_actor_location()
    ground = trace_floor_z(world, loc.x, loc.y, loc.z + 200.0, loc.z - 500.0, [player])
    errors = []
    if ground is None:
        errors.append("player start has no walk pad under it")
    eye = unreal.Vector(loc.x, loc.y, top + 160.0)
    cottage = by_label().get("SM_Size_Cottage")
    if cottage is None:
        return errors + ["no cottage"]
    door = cottage.get_actor_location()
    body_hit = trace_hit(world, eye, unreal.Vector(door.x, door.y - 280.0, top + 160.0), [])
    if body_hit is None or not _is_copse(str(body_hit.get("label", ""))):
        seen = "nothing" if body_hit is None else str(body_hit.get("label", ""))
        errors.append("cottage is already in sight, hit " + seen)
    if not errors:
        unreal.log("scene_placement: opening cottage hidden by trees and rocks")
    return errors


def check():
    """Measure the open map. Do not move actors and do not save."""
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(MAP_PATH)
    top, errors = measure_floor()
    if top is None:
        for error in errors:
            unreal.log("scene_placement: FAIL " + error)
        unreal.log("scene_placement: CHECK FAIL")
        return 1
    player = None
    for candidate in actors():
        if candidate.get_class().get_name() == "PlayerStart":
            player = candidate
            break
    errors.extend(validate(player, top))
    errors.extend(opening_sightline(top))
    errors.extend(dog_errors(top))
    errors.extend(space_mapping_errors())
    errors.extend(stroke_or_ease_errors())
    errors.extend(graph_errors(load_metrics()))
    for error in errors:
        unreal.log("scene_placement: FAIL " + error)
    if errors:
        unreal.log("scene_placement: CHECK FAIL")
        return 1
    unreal.log("scene_placement: CHECK PASS top %.1f" % top)
    watch_jump()
    return 0


_jump_watch = {"phase": "idle", "handle": None, "z0": 0.0, "peak": 0.0, "elapsed": 0.0}


def _jump_finish(message):
    unreal.log(message)
    handle = _jump_watch.get("handle")
    if handle is not None:
        unreal.unregister_slate_post_tick_callback(handle)
        _jump_watch["handle"] = None
    try:
        unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
    except Exception:
        pass
    _jump_watch["phase"] = "idle"


def _jump_tick(delta):
    if _jump_watch["phase"] == "idle":
        return
    try:
        world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
        if world is None:
            return
        pawn = unreal.GameplayStatics.get_player_pawn(world, 0)
        if pawn is None:
            return
        if _jump_watch["phase"] == "wait":
            z0 = pawn.get_actor_location().z
            _jump_watch["z0"] = z0
            _jump_watch["peak"] = z0
            pawn.jump()
            _jump_watch["phase"] = "watch"
            return
        z = pawn.get_actor_location().z
        if z > _jump_watch["peak"]:
            _jump_watch["peak"] = z
        _jump_watch["elapsed"] += float(delta)
        if _jump_watch["elapsed"] < 1.0:
            return
        rise = _jump_watch["peak"] - _jump_watch["z0"]
        if rise < 30.0:
            _jump_finish("scene_placement: FAIL jump rose %.1f cm" % rise)
        else:
            _jump_finish("scene_placement: jump rise %.1f cm within one second" % rise)
    except Exception as exc:
        _jump_finish("scene_placement: FAIL jump %s" % exc)


def space_mapping_errors():
    """UE 5.8 reads default_key_mappings. The deprecated mappings list does not count."""
    context = unreal.EditorAssetLibrary.load_asset("/Game/HomeWorld/Input/IMC_Default")
    if context is None:
        return ["no input mapping context"]
    text = context.get_editor_property("default_key_mappings").export_text()
    if "IA_Jump" not in text or "SpaceBar" not in text:
        return ["Space is not in default_key_mappings"]
    return []


def watch_jump():
    """Start play and require the jump Space calls to leave the ground within one second."""
    if _jump_watch["phase"] != "idle":
        return
    _jump_watch["phase"] = "wait"
    _jump_watch["elapsed"] = 0.0
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_begin_play()
    _jump_watch["handle"] = unreal.register_slate_post_tick_callback(_jump_tick)
    unreal.log("scene_placement: jump watch started")

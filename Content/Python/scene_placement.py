"""Place a test scene from its metrics file and refuse to save a failed check.

The metrics file is the approved layout, in meters. This module snaps mesh
bottoms onto the measured floor, measures them again, and refuses to save if
any bottom is more than 2 cm off. See Docs/context/SCENE_SETUP.md practices
10-12: coat yaw offset 0, walk only while moving, pin before save.
"""

import json
import math
import os
import sys

import unreal

sys.path.insert(0, os.path.dirname(__file__))
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
    """SK_Player_Female faces mesh -Y. A +90 component yaw turns that face onto actor +X."""
    mesh = actor.get_component_by_class(unreal.SkeletalMeshComponent)
    if mesh is None:
        return
    mesh.set_relative_rotation(yaw_rotator(90.0), False, False)
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
        if actor.get_actor_label().startswith("CabinWall_") or actor.get_actor_label().startswith("PorchCrawl_"):
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
        wall_material = cube.get_material(0)
        if wall_material is not None:
            wall.set_material(0, wall_material)
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
    fill_mesh.set_collision_profile_name("BlockAll")
    fill_mesh.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
    tag_actor(filler, "NODE_PORCH_CRAWL")
    unreal.log("scene_placement: cabin shell %d walls" % len(boxes))
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
    """Downward traces on the walk pad. Never use the mesh's highest point."""
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
        if label == "SM_Size_Island" or label == "SM_Size_WalkPad":
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
        if label == "SM_Size_Island" or label == "SM_Size_WalkPad":
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
    if not (loc.x + 900.0 < spot.x < loc.x + 1060.0 and loc.y - 120.0 < spot.y < loc.y + 120.0):
        errors.append("kettle is outside the kitchen")
    bed_loc = bed.get_actor_location()
    if not (loc.x - 280.0 < bed_loc.x < loc.x + 40.0 and loc.y + 750.0 < bed_loc.y < loc.y + 990.0):
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


def run(import_mesh=True):
    metrics = load_metrics()
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
            elif label == "SM_Size_Kettle":
                tag_actor(actor, "NODE_KETTLE")
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
    if not spawn_cabin_walls():
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
    remove_outside_homestead(keep)
    player = place_player(metrics["player"], top)
    errors = pin_to_floor(labels, top)
    errors.extend(floor_errors)
    errors.extend(validate(player, top))
    errors.extend(opening_sightline(top))
    errors.extend(stroke_or_ease_errors())
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
    errors.extend(space_mapping_errors())
    errors.extend(stroke_or_ease_errors())
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

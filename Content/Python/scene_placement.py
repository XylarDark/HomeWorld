"""Place a test scene from its metrics file and refuse to save a failed check.

The metrics file is the approved layout, in meters. This module snaps mesh
bottoms onto the measured floor, measures them again, and refuses to save if
any bottom is more than 2 cm off. See Docs/context/SCENE_SETUP.md practices
10-12: coat yaw offset 0, walk only while moving, pin before save.
"""

import json
import math
import os

import unreal

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


def place_static(label, mesh_name, x_m, y_m, z_m, yaw, scale=1.0):
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
    actor.set_actor_scale3d(unreal.Vector(scale, scale, 1.0 if scale != 1.0 else 1.0))
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    if component is not None:
        component.set_static_mesh(mesh)
    return actor


def passable(label):
    return label.startswith(PASSABLE_PREFIXES)


def set_collision(actor):
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    if component is None:
        return
    if passable(actor.get_actor_label()):
        component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        return
    component.set_collision_profile_name("BlockAll")
    component.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)


def set_slab_collision():
    """One box for the 40 m by 30 m by 1 m pad. The cone does not block."""
    mesh = unreal.EditorAssetLibrary.load_asset(MESH_DIR + "/SM_Size_Island")
    if mesh is None:
        unreal.log("scene_placement: FAIL no island mesh")
        return False
    body = mesh.get_editor_property("body_setup")
    if body is None:
        unreal.log("scene_placement: FAIL island has no body setup")
        return False
    body.set_editor_property("collision_trace_flag", unreal.CollisionTraceFlag.CTF_USE_SIMPLE_AS_COMPLEX)
    elem = unreal.KBoxElem()
    elem.set_editor_property("center", unreal.Vector(0.0, 0.0, -50.0))
    elem.set_editor_property("x", 4000.0)
    elem.set_editor_property("y", 3000.0)
    elem.set_editor_property("z", 100.0)
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
    unreal.log("scene_placement: island slab box collision")
    return True


def box_elem(cx, cy, cz, sx, sy, sz):
    elem = unreal.KBoxElem()
    elem.set_editor_property("center", unreal.Vector(cx, cy, cz))
    elem.set_editor_property("x", float(sx))
    elem.set_editor_property("y", float(sy))
    elem.set_editor_property("z", float(sz))
    return elem


def set_cottage_collision():
    """Walls and a south door. The porch stays open. The pad is the floor."""
    mesh = unreal.EditorAssetLibrary.load_asset(MESH_DIR + "/SM_Size_Cottage")
    if mesh is None:
        unreal.log("scene_placement: FAIL no cottage mesh")
        return False
    body = mesh.get_editor_property("body_setup")
    if body is None:
        unreal.log("scene_placement: FAIL cottage has no body setup")
        return False
    body.set_editor_property("collision_trace_flag", unreal.CollisionTraceFlag.CTF_USE_SIMPLE_AS_COMPLEX)
    # House front is 2 m north of the porch lip. Door gap is 1.4 m so the 84 cm capsule fits.
    door_half = 70.0
    wall_y = -395.0
    boxes = [
        box_elem(-280.0, wall_y, 250.0, 420.0, 40.0, 500.0),
        box_elem(280.0, wall_y, 250.0, 420.0, 40.0, 500.0),
        box_elem(0.0, wall_y, 400.0, door_half * 2.0, 40.0, 200.0),
        box_elem(0.0, 550.0, 250.0, 980.0, 40.0, 500.0),
        box_elem(-470.0, 87.5, 250.0, 40.0, 965.0, 500.0),
        box_elem(470.0, 87.5, 250.0, 40.0, 965.0, 500.0),
    ]
    agg = body.get_editor_property("agg_geom")
    agg.set_editor_property("box_elems", boxes)
    agg.set_editor_property("sphere_elems", [])
    agg.set_editor_property("sphyl_elems", [])
    agg.set_editor_property("convex_elems", [])
    body.set_editor_property("agg_geom", agg)
    unreal.EditorAssetLibrary.save_loaded_asset(mesh)
    actor = by_label().get("SM_Size_Cottage")
    if actor is not None:
        component = actor.get_component_by_class(unreal.StaticMeshComponent)
        if component is not None:
            component.set_static_mesh(None)
            component.set_static_mesh(mesh)
            set_collision(actor)
    unreal.log("scene_placement: cottage wall collision, south door open")
    return True


def trace_floor_z(world, x, y, z_high, z_low, ignore):
    data = trace_hit(world, unreal.Vector(x, y, z_high), unreal.Vector(x, y, z_low), ignore)
    if data is None:
        return None
    if data.get("label") != "SM_Size_Island":
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
    """Downward traces on the pad. Never use the mesh's highest point."""
    actor = by_label().get("SM_Size_Island")
    if actor is None:
        return None, ["no island"]
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    origin, extent = actor.get_actor_bounds(False)
    ignore = [other for other in actors() if other.get_actor_label() != "SM_Size_Island"]
    z_high = origin.z + extent.z + 300.0
    z_low = origin.z - extent.z - 300.0
    samples = []
    for sx, sy in ((0.0, 0.0), (0.75, 0.0), (-0.75, 0.0), (0.0, 0.75), (0.0, -0.75)):
        z = trace_floor_z(
            world,
            origin.x + extent.x * sx,
            origin.y + extent.y * sy,
            z_high,
            z_low,
            ignore,
        )
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
        if label == "SM_Size_Island":
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
        if label == "SM_Size_Island":
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
        if label == "SM_Size_Island":
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
    if abs(((yaw - 90.0 + 180.0) % 360.0) - 180.0) > 1.0:
        errors.append("player yaw is %.1f" % yaw)
    island = by_label().get("SM_Size_Island")
    origin, extent = island.get_actor_bounds(False)
    inset = 500.0
    if not (origin.x - extent.x + inset < loc.x < origin.x + extent.x - inset and origin.y - extent.y + inset < loc.y < origin.y + extent.y - inset):
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
    ignore = [other for other in actors() if other.get_actor_label() != "SM_Size_Island"]
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
    ignore = [other for other in actors() if other.get_actor_label() != "SM_Size_Cottage"]
    chest = top + 150.0
    door = trace_hit(
        world,
        unreal.Vector(loc.x, loc.y - 700.0, chest),
        unreal.Vector(loc.x, loc.y - 100.0, chest),
        ignore,
    )
    if door is not None and door["label"] == "SM_Size_Cottage":
        errors.append("south door is blocked")
    wall = trace_hit(
        world,
        unreal.Vector(loc.x - 800.0, loc.y - 300.0, chest),
        unreal.Vector(loc.x - 200.0, loc.y - 300.0, chest),
        ignore,
    )
    if wall is None or wall["label"] != "SM_Size_Cottage":
        errors.append("cottage wall does not block")
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
        if label == "SM_Size_Island" or passable(label) or label == "SM_Size_Field":
            continue
        errors.append("capsule hits " + label)
    return errors


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


def run(import_mesh=True):
    metrics = load_metrics()
    if import_mesh:
        import_island()
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(MAP_PATH)
    labels = []
    for item in metrics["homestead"]:
        place_static(item["label"], item["mesh"], item["x"], item["y"], item["z"], item["yaw"])
        labels.append(item["label"])
    for label in labels:
        actor = by_label().get(label)
        if actor is not None:
            set_collision(actor)
    if not set_slab_collision() or not set_cottage_collision():
        return 1
    top, floor_errors = measure_floor()
    if top is None:
        for error in floor_errors:
            unreal.log("scene_placement: FAIL " + error)
        unreal.log("scene_placement: not saved")
        return 1
    snap_contacts(labels, top)
    plains = metrics["plains"]
    field = place_static(
        plains["label"], plains["mesh"], plains["x"], plains["y"], plains["z"], plains["yaw"], plains["scale"]
    )
    if field is not None:
        field.set_actor_scale3d(unreal.Vector(plains["scale"], plains["scale"], 1.0))
        set_collision(field)
    keep = set(labels)
    keep.add(plains["label"])
    remove_outside_homestead(keep)
    player = place_player(metrics["player"], top)
    errors = pin_to_floor(labels, top)
    errors.extend(floor_errors)
    errors.extend(validate(player, top))
    for error in errors:
        unreal.log("scene_placement: FAIL " + error)
    if errors:
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
    for error in errors:
        unreal.log("scene_placement: FAIL " + error)
    if errors:
        unreal.log("scene_placement: CHECK FAIL")
        return 1
    unreal.log("scene_placement: CHECK PASS top %.1f" % top)
    return 0

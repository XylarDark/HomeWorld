"""Place the field greybox from Docs/level/L_Field_METRICS.md.

Texture-off mass only. No path, no landing ring, no camp. The two forest
edges share one pine sequence. Herb centres come from the sheet. The map is
built from an empty level, so this file also places the lighting set the kept
size test keeps: one sun, one sky light, one sky atmosphere
(Docs/context/SCENE_SETUP.md practice 4). A run with a missing mesh saves
nothing and exits non-zero.
"""

import json
import os
import sys

import unreal

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
METRICS = os.path.join(ROOT, "Docs", "level", "L_Field_METRICS.md")
MAP_PATH = "/Game/HomeWorld/Maps/Field/L_Field"
MESH_DIR = "/Game/HomeWorld/Meshes/SizeTest"
CUBE = "/Engine/BasicShapes/Cube"
M = 100.0

# The lighting set, named so a re-run finds its own actors and a stray sun is
# caught. Values match the kept size test (place_size_test.py) and the
# moonlight pose in vnp_night_tune_and_evidence.py: 45 degrees up, 30 azimuth.
SUN_LABEL = "Field_Sun"
SKY_LIGHT_LABEL = "Field_SkyLight"
SKY_ATMOSPHERE_LABEL = "Field_SkyAtmosphere"
SUN_PITCH = -45.0
SUN_YAW = 30.0

#: Labels cleared and rebuilt on every run. The lighting actors are kept and
#: re-posed instead, so a re-run repairs the map rather than stacking a second sun.
CLEARED_PREFIXES = ("SM_Field_", "SK_Field_")

#: Placements that did not happen. run() refuses to save with any entry here:
#: a miss is not a save (Docs/context/SCENE_SETUP.md practice 13).
FAILED = []


def fail(message):
    """Record a placement that did not happen and say so in the log."""
    FAILED.append(message)
    unreal.log("field_greybox: FAIL " + message)


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


def destroy(actor):
    unreal.get_editor_subsystem(unreal.EditorActorSubsystem).destroy_actor(actor)


def vec(x_m, y_m, z_m):
    return unreal.Vector(x_m * M, y_m * M, z_m * M)


def yaw_rotator(yaw):
    rot = unreal.Rotator()
    rot.yaw = float(yaw)
    return rot


def clear_field_actors():
    for actor in list(actors()):
        label = actor.get_actor_label()
        if label.startswith(CLEARED_PREFIXES):
            destroy(actor)


def spawn_static(label, location, rotation):
    actor = by_label().get(label)
    if actor is None:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.StaticMeshActor, location, rotation
        )
        actor.set_actor_label(label)
    actor.set_actor_location(location, False, False)
    actor.set_actor_rotation(rotation, False)
    return actor


def place_cube(label, x, y, z, sx, sy, sz, block):
    cube = unreal.EditorAssetLibrary.load_asset(CUBE)
    if cube is None:
        fail("no engine cube")
        return None
    actor = spawn_static(label, vec(x, y, z), yaw_rotator(0))
    actor.set_actor_scale3d(unreal.Vector(sx, sy, sz))
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    component.set_static_mesh(cube)
    if block:
        component.set_collision_profile_name("BlockAll")
        component.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
    else:
        component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    return actor


def place_pine(label, mesh_name, x, y):
    mesh = unreal.EditorAssetLibrary.load_asset(MESH_DIR + "/" + mesh_name)
    if mesh is None:
        fail("missing " + mesh_name)
        return None
    actor = spawn_static(label, vec(x, y, 0), yaw_rotator(0))
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    component.set_static_mesh(mesh)
    component.set_collision_profile_name("BlockAll")
    component.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
    origin, extent = actor.get_actor_bounds(False)
    loc = actor.get_actor_location()
    actor.set_actor_location(
        unreal.Vector(loc.x, loc.y, loc.z - (origin.z - extent.z)), False, False
    )
    return actor


def forest_stations(forest):
    stations = []
    along = forest["start"]
    while along <= forest["end"] + 0.01:
        stations.append(round(along, 1))
        along += forest["step"]
    return stations


def place_forests(forest):
    sequence = forest["sequence"]
    stations = forest_stations(forest)
    for index, along in enumerate(stations):
        mesh_name = sequence[index % len(sequence)]
        if index == 0:
            place_pine("SM_Field_Pine_Corner", mesh_name, forest["x_west"], forest["y_south"])
            continue
        place_pine(
            "SM_Field_Pine_S_%02d" % index,
            mesh_name,
            along,
            forest["y_south"],
        )
        place_pine(
            "SM_Field_Pine_W_%02d" % index,
            mesh_name,
            forest["x_west"],
            along,
        )


def herb_points(herb):
    points = [(herb["x"], herb["y"])]
    if herb["kind"] in ("dual", "triple"):
        points.append((herb["x"] + 1.0, herb["y"]))
    if herb["kind"] == "triple":
        points.append((herb["x"], herb["y"] + 1.0))
    return points


def place_herbs(herbs):
    index = 0
    for herb in herbs:
        for x, y in herb_points(herb):
            place_cube(
                "SM_Field_Herb_%03d" % index,
                x,
                y,
                0.25,
                0.7,
                0.7,
                0.5,
                False,
            )
            index += 1
    return index


def place_trees(trees):
    for tree in trees:
        place_pine(tree["label"], tree["mesh"], tree["x"], tree["y"])


def place_bull(label, x, y, yaw):
    mesh = unreal.EditorAssetLibrary.load_asset(MESH_DIR + "/SK_Size_Bull")
    if mesh is None:
        fail("missing SK_Size_Bull")
        return None
    location = vec(x, y, 0)
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
    component = actor.get_component_by_class(unreal.SkeletalMeshComponent)
    if hasattr(component, "set_skinned_asset_and_update"):
        component.set_skinned_asset_and_update(mesh)
    else:
        component.set_skeletal_mesh(mesh)
    component.set_collision_profile_name("BlockAll")
    component.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
    origin, extent = actor.get_actor_bounds(False)
    loc = actor.get_actor_location()
    actor.set_actor_location(
        unreal.Vector(loc.x, loc.y, loc.z - (origin.z - extent.z)), False, False
    )
    return actor


def place_bulls(bulls):
    for bull in bulls:
        place_bull(bull["label"], bull["x"], bull["y"], bull["yaw"])


def place_player(player):
    actor = None
    for candidate in actors():
        if candidate.get_class().get_name() == "PlayerStart":
            actor = candidate
            break
    if actor is None:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.PlayerStart, vec(player["x"], player["y"], player["z"]), yaw_rotator(player["yaw"])
        )
        actor.set_actor_label("PlayerStart")
    actor.set_actor_location(vec(player["x"], player["y"], player["z"]), False, False)
    actor.set_actor_rotation(yaw_rotator(player["yaw"]), False)
    return actor


def sun_rotator():
    """The one sun's pose, written with keyword args on purpose.

    A positional unreal.Rotator is (roll, pitch, yaw), not (pitch, yaw, roll), so
    Rotator(-45.0, 30.0, 0.0) puts the elevation in the inert roll slot and the
    azimuth into pitch - a sun that lights upward. See docs/KNOWN_ERRORS.md
    ("UE Python Rotator positional args").
    """
    return unreal.Rotator(roll=0.0, pitch=SUN_PITCH, yaw=SUN_YAW)


def spawn_light(label, actor_class, location, rotation):
    actor = by_label().get(label)
    if actor is None:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            actor_class, location, rotation
        )
        actor.set_actor_label(label)
    actor.set_actor_location(location, False, False)
    actor.set_actor_rotation(rotation, False)
    return actor


def place_lights():
    """One sun, one sky light, one sky atmosphere, matching the kept size test.

    Two directional lights leave the view black (SCENE_SETUP practice 4), so a
    directional light that is not Field_Sun is removed. The sun is re-posed even
    when its label already exists: a label guard alone would keep a wrong
    rotation from an earlier save.
    """
    zero = yaw_rotator(0)
    for actor in list(actors()):
        if "DirectionalLight" not in (actor.get_class().get_name() or ""):
            continue
        if actor.get_actor_label() == SUN_LABEL:
            continue
        unreal.log("field_greybox: removed extra sun " + actor.get_actor_label())
        destroy(actor)
    spawn_light(SUN_LABEL, unreal.DirectionalLight, vec(0, 0, 500), sun_rotator())
    spawn_light(SKY_LIGHT_LABEL, unreal.SkyLight, vec(0, 0, 500), zero)
    spawn_light(SKY_ATMOSPHERE_LABEL, unreal.SkyAtmosphere, vec(0, 0, 0), zero)


def run():
    metrics = load_metrics()
    del FAILED[:]
    level = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if unreal.EditorAssetLibrary.does_asset_exist(MAP_PATH):
        level.load_level(MAP_PATH)
    else:
        level.new_level(MAP_PATH)
    clear_field_actors()
    floor = metrics["floor"]
    place_cube(floor["label"], floor["x"], floor["y"], floor["z"], floor["sx"], floor["sy"], floor["sz"], True)
    for cliff in metrics["cliffs"]:
        place_cube(cliff["label"], cliff["x"], cliff["y"], cliff["z"], cliff["sx"], cliff["sy"], cliff["sz"], True)
    drop = metrics["drop"]
    place_cube(drop["label"], drop["x"], drop["y"], drop["z"], drop["sx"], drop["sy"], drop["sz"], True)
    river = metrics["river"]
    place_cube(river["label"], river["x"], river["y"], river["z"], river["sx"], river["sy"], river["sz"], True)
    bank = metrics["river_bank"]
    place_cube(bank["label"], bank["x"], bank["y"], bank["z"], bank["sx"], bank["sy"], bank["sz"], True)
    place_forests(metrics["forest"])
    place_trees(metrics.get("trees", []))
    herb_count = place_herbs(metrics["herbs"])
    bulls = metrics.get("bulls", [])
    place_bulls(bulls)
    place_player(metrics["player"])
    place_lights()
    if FAILED:
        unreal.log(
            "field_greybox: NOT SAVED, %d placement(s) failed" % len(FAILED)
        )
        return 1
    level.save_current_level()
    unreal.log(
        "field_greybox: saved herb nodes %d from %d centres, bulls %d"
        % (herb_count, len(metrics["herbs"]), len(bulls))
    )
    return 0


if __name__ == "__main__":
    sys.exit(run())

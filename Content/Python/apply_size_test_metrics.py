"""Move L_SizeTest actors to Docs/level/L_SizeTest_METRICS.md."""

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("apply_size_test_metrics: run inside Unreal Editor")
    sys.exit(1)

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
METRICS = os.path.join(ROOT, "Docs", "level", "L_SizeTest_METRICS.md")
MAP_PATH = "/Game/HomeWorld/Maps/SizeTest/L_SizeTest"
MESH_DIR = "/Game/HomeWorld/Meshes/SizeTest"
M = 100.0
HOMESTEAD_Z = 20000.0


def load_metrics():
    text = open(METRICS, encoding="utf-8").read()
    start = text.index("```json") + len("```json")
    end = text.index("```", start)
    return json.loads(text[start:end])


def vec(x_m, y_m, z_m):
    return unreal.Vector(x_m * M, y_m * M, z_m * M)


def actors():
    return unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()


def by_label():
    found = {}
    for actor in actors():
        found.setdefault(actor.get_actor_label(), actor)
    return found


def mesh_asset(name):
    return unreal.EditorAssetLibrary.load_asset(MESH_DIR + "/" + name)


def import_static(name):
    filename = os.path.join(ROOT, "AssetCreation", "SizeTest", name + ".fbx")
    if not os.path.isfile(filename):
        unreal.log("apply_size_test_metrics: missing fbx " + name)
        return
    task = unreal.AssetImportTask()
    task.filename = filename
    task.destination_path = MESH_DIR
    task.destination_name = name
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
    unreal.log("apply_size_test_metrics: imported " + name)


def place_static(label, mesh_name, x_m, y_m, z_m, yaw):
    mesh = mesh_asset(mesh_name)
    if mesh is None:
        unreal.log("apply_size_test_metrics: missing mesh " + mesh_name)
        return
    found = by_label()
    location = vec(x_m, y_m, z_m)
    rotation = unreal.Rotator(0.0, yaw, 0.0)
    actor = found.get(label)
    if actor is not None and actor.get_component_by_class(unreal.StaticMeshComponent) is None:
        unreal.EditorLevelLibrary.destroy_actor(actor)
        actor = None
    if actor is None:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.StaticMeshActor, location, rotation
        )
        actor.set_actor_label(label)
    else:
        actor.set_actor_location(location, False, False)
        actor.set_actor_rotation(rotation, False)
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    if component is not None:
        component.set_static_mesh(mesh)
        if mesh_name.startswith("SM_Size_Cloud"):
            component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)


def remove_unwanted(remove_labels):
    remove = set(remove_labels)
    for actor in list(actors()):
        label = actor.get_actor_label()
        drop = label in remove or label.startswith("SM_Size_Path")
        if label.startswith("SK_Size_Guard") and actor.get_actor_location().z > HOMESTEAD_Z:
            drop = True
        if drop:
            unreal.EditorLevelLibrary.destroy_actor(actor)
            unreal.log("apply_size_test_metrics: removed " + label)


def one_sun():
    for actor in list(actors()):
        cls = actor.get_class().get_name() if actor.get_class() else ""
        if "DirectionalLight" not in cls:
            continue
        if actor.get_actor_label() == "SizeTest_Sun":
            continue
        unreal.EditorLevelLibrary.destroy_actor(actor)
        unreal.log("apply_size_test_metrics: removed extra sun " + actor.get_actor_label())


def place_player(player):
    for actor in actors():
        if actor.get_class().get_name() != "PlayerStart":
            continue
        actor.set_actor_location(vec(player["x"], player["y"], player["z"]), False, False)
        actor.set_actor_rotation(unreal.Rotator(0.0, player["yaw"], 0.0), False)
        unreal.log("apply_size_test_metrics: player start moved")
        return
    unreal.log("apply_size_test_metrics: no PlayerStart")


def import_player():
    filename = os.path.join(ROOT, "AssetCreation", "SizeTest", "SK_Size_Player.fbx")
    if not os.path.isfile(filename):
        unreal.log("apply_size_test_metrics: no player fbx")
        return
    task = unreal.AssetImportTask()
    task.filename = filename
    task.destination_path = MESH_DIR
    task.destination_name = "SK_Size_Player"
    task.automated = True
    task.save = True
    task.replace_existing = True
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_as_skeletal", True)
    options.set_editor_property("import_animations", True)
    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
    task.options = options
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    unreal.log("apply_size_test_metrics: player import " + ", ".join(task.imported_object_paths))


STATIC_MESHES = [
    "SM_Size_Cottage",
    "SM_Size_HerbBed",
    "SM_Size_Rock",
    "SM_Size_Pine_S",
    "SM_Size_Pine_M",
    "SM_Size_Pine_L",
    "SM_Size_Lupine",
    "SM_Size_Herb",
    "SM_Size_Wood",
    "SM_Size_Berry",
    "SM_Size_BerryBush",
    "SM_Size_Bear",
    "SM_Size_Bull",
    "SM_Size_Kettle",
    "SM_Size_Shrine",
    "SM_Size_Cloud",
    "SM_Size_CloudAmbient",
]


def clear_prefix(prefix):
    subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for actor in list(actors()):
        if actor.get_actor_label().startswith(prefix):
            subsystem.destroy_actor(actor)


def snap_to_island(items):
    island_top = None
    for actor in actors():
        if actor.get_actor_label() != "SM_Size_Island":
            continue
        origin, extent = actor.get_actor_bounds(False)
        island_top = origin.z + extent.z
        break
    if island_top is None:
        unreal.log("apply_size_test_metrics: no island top")
        return None
    for item in items:
        if item["label"] == "SM_Size_Island":
            continue
        actor = by_label().get(item["label"])
        if actor is None:
            continue
        origin, extent = actor.get_actor_bounds(False)
        delta = island_top - (origin.z - extent.z)
        loc = actor.get_actor_location()
        actor.set_actor_location(unreal.Vector(loc.x, loc.y, loc.z + delta), False, False)
        unreal.log("apply_size_test_metrics: snap %s by %.1f" % (item["label"], delta))
    return island_top


def place_group(items):
    for item in items:
        place_static(item["label"], item["mesh"], item["x"], item["y"], item["z"], item.get("yaw", 0))


def main():
    metrics = load_metrics()
    for name in STATIC_MESHES:
        import_static(name)
    import_player()
    import scene_placement
    return scene_placement.run()


if __name__ == "__main__":
    sys.exit(main())

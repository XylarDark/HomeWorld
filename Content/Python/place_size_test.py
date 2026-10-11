"""Import the size-test FBX set and build the homestead-to-camp walk.

Run inside the Unreal Editor:
  execute_python_script with the absolute path, or Tools > Execute Python Script.

The island walk surface is 450 m up. A straight glide at the pawn's 30 m/s
forward and 15 m/s sink lands on the field 900 m ahead. Interact at the perch
starts that glide. Draft meshes stay under /Game/HomeWorld/Meshes/SizeTest.
"""

import os
import sys

try:
    import unreal
except ImportError:
    print("place_size_test: run inside Unreal Editor")
    sys.exit(1)

PREFIX = "place_size_test:"
MAP_PATH = "/Game/HomeWorld/Maps/SizeTest/L_SizeTest"
DEST = "/Game/HomeWorld/Meshes/SizeTest"
M = 100.0


def log(message):
    unreal.log(PREFIX + " " + str(message))
    print(PREFIX, message)


def project_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", ".."))


def import_one(asset_tools, path):
    name = os.path.splitext(os.path.basename(path))[0]
    task = unreal.AssetImportTask()
    task.filename = path
    task.destination_path = DEST
    task.destination_name = name
    task.automated = True
    task.save = True
    task.replace_existing = True
    if name.startswith("SK_"):
        options = unreal.FbxImportUI()
        options.set_editor_property("import_mesh", True)
        options.set_editor_property("import_as_skeletal", True)
        options.set_editor_property("import_animations", True)
        options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
        task.options = options
    asset_tools.import_asset_tasks([task])
    landed = list(task.imported_object_paths)
    log("import %s -> %s" % (name, ", ".join(landed) if landed else "nothing"))
    return landed


def load_imported(paths):
    static_mesh = None
    skeletal = None
    walk = None
    for path in paths:
        asset = unreal.load_asset(path)
        if asset is None:
            continue
        if isinstance(asset, unreal.StaticMesh):
            static_mesh = asset
        elif isinstance(asset, unreal.SkeletalMesh):
            skeletal = asset
        elif isinstance(asset, unreal.AnimSequence) and walk is None:
            walk = asset
    return static_mesh, skeletal, walk


def spawn_static(mesh, location, rotation=None):
    if rotation is None:
        rotation = unreal.Rotator(0.0, 0.0, 0.0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor, location, rotation
    )
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    component.set_static_mesh(mesh)
    actor.set_actor_label(mesh.get_name())
    return actor


def spawn_skeletal(skeletal, walk, location, yaw):
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SkeletalMeshActor, location, unreal.Rotator(0.0, yaw, 0.0)
    )
    component = actor.get_component_by_class(unreal.SkeletalMeshComponent)
    if hasattr(component, "set_skinned_asset_and_update"):
        component.set_skinned_asset_and_update(skeletal)
    else:
        component.set_skeletal_mesh(skeletal)
    if walk is not None:
        component.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
        component.play_animation(walk, True)
    actor.set_actor_label(skeletal.get_name())
    return actor


def vec(x_m, y_m, z_m):
    return unreal.Vector(x_m * M, y_m * M, z_m * M)


def main():
    folder = os.path.join(project_root(), "AssetCreation", "SizeTest")
    if not os.path.isdir(folder):
        log("missing " + folder)
        return 1
    files = sorted(
        os.path.join(folder, name)
        for name in os.listdir(folder)
        if name.lower().endswith(".fbx")
    )
    if not files:
        log("no fbx in " + folder)
        return 1

    unreal.EditorAssetLibrary.make_directory(DEST)
    unreal.EditorAssetLibrary.make_directory("/Game/HomeWorld/Maps/SizeTest")
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    assets = {}
    for path in files:
        name = os.path.splitext(os.path.basename(path))[0]
        assets[name] = load_imported(import_one(tools, path))

    level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_editor.new_level(MAP_PATH)

    island_z = 450.0
    spawn_static(assets["SM_Size_Island"][0], vec(0, 0, island_z))
    spawn_static(assets["SM_Size_Cottage"][0], vec(-8, 0, island_z + 1))
    spawn_static(assets["SM_Size_Pine_S"][0], vec(-12, 8, island_z))
    spawn_static(assets["SM_Size_Pine_M"][0], vec(-12, -8, island_z))
    spawn_static(assets["SM_Size_Pine_L"][0], vec(0, 10, island_z))
    spawn_static(assets["SM_Size_Lupine"][0], vec(-4, 6, island_z))
    spawn_static(assets["SM_Size_Rock"][0], vec(4, -8, island_z))
    for index, step in enumerate(range(-6, 12, 2)):
        spawn_static(assets["SM_Size_Path"][0], vec(step, -4, island_z))
    spawn_static(assets["SM_Size_Fence"][0], vec(-16, 6, island_z))
    spawn_static(assets["SM_Size_HerbBed"][0], vec(-6, 6, island_z))
    spawn_static(assets["SM_Size_Moss"][0], vec(4, -6, island_z))
    spawn_static(assets["SM_Size_Crystal"][0], vec(-2, -6, island_z))
    spawn_static(assets["SM_Size_Bed"][0], vec(-10, 2, island_z + 1))
    spawn_static(assets["SM_Size_Kettle"][0], vec(-9, 3, island_z + 1))
    spawn_static(assets["SM_Size_Stump"][0], vec(-8, -6, island_z))
    spawn_static(assets["SM_Size_Perch"][0], vec(16, 0, island_z))
    spawn_static(assets["SM_Size_Shrine"][0], vec(-16, -6, island_z))
    spawn_skeletal(*assets["SK_Size_Bear"][1:], vec(-2, 8, island_z), 180.0)
    spawn_skeletal(*assets["SK_Size_Partner"][1:], vec(-10, -2, island_z + 1), 90.0)
    spawn_skeletal(*assets["SK_Size_Child"][1:], vec(-6, 4, island_z), 0.0)

    spawn_static(assets["SM_Size_Field"][0], vec(900, 0, 0))
    spawn_skeletal(*assets["SK_Size_Bull"][1:], vec(880, 20, 0), 90.0)
    spawn_static(assets["SM_Size_Herb"][0], vec(860, -10, 0))
    spawn_static(assets["SM_Size_Wood"][0], vec(870, 10, 0))
    spawn_static(assets["SM_Size_Berry"][0], vec(890, -16, 0))
    spawn_static(assets["SM_Size_Fire"][0], vec(1060, 0, 0))
    for post in ((1052, -6), (1068, -6), (1060, 8)):
        spawn_static(assets["SM_Size_Post"][0], vec(post[0], post[1], 0))
    for guard, yaw in (((1054, 2), 0.0), ((1066, 2), 180.0), ((1060, -4), 90.0)):
        spawn_skeletal(*assets["SK_Size_Guard"][1:], vec(guard[0], guard[1], 0), yaw)
    for cloud in ((300, 0, 300), (500, 30, 200), (700, -20, 100)):
        actor = spawn_static(assets["SM_Size_Cloud"][0], vec(*cloud))
        actor.get_component_by_class(unreal.StaticMeshComponent).set_collision_enabled(
            unreal.CollisionEnabled.NO_COLLISION
        )
    wisp = spawn_static(assets["SM_Size_Wisp"][0], vec(500, 0, 220))
    wisp.get_component_by_class(unreal.StaticMeshComponent).set_collision_enabled(
        unreal.CollisionEnabled.NO_COLLISION
    )

    start = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PlayerStart, vec(-8, -6, island_z + 1), unreal.Rotator(0.0, 0.0, 0.0)
    )
    start.set_actor_label("PlayerStart")
    marker = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.TargetPoint, vec(16, 0, island_z + 1), unreal.Rotator(0.0, 0.0, 0.0)
    )
    marker.set_actor_label("GP_GlideStart")
    marker.tags = ["GlideStart"]

    sun = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.DirectionalLight, vec(0, 0, 500), unreal.Rotator(-45.0, 30.0, 0.0)
    )
    sun.set_actor_label("Sun")
    unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SkyLight, vec(0, 0, 500), unreal.Rotator(0.0, 0.0, 0.0)
    )
    unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SkyAtmosphere, vec(0, 0, 0), unreal.Rotator(0.0, 0.0, 0.0)
    )

    unreal.EditorLevelLibrary.save_current_level()
    log("saved " + MAP_PATH)
    return 0


if __name__ == "__main__":
    sys.exit(main())

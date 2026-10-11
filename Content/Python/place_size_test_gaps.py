"""Place the berry bush and ambient clouds on the size-test walk."""

import os
import sys

try:
    import unreal
except ImportError:
    print("place_size_test_gaps: run inside Unreal Editor")
    sys.exit(1)

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
MAP_PATH = "/Game/HomeWorld/Maps/SizeTest/L_SizeTest"
M = 100.0


def vec(x_m, y_m, z_m):
    return unreal.Vector(x_m * M, y_m * M, z_m * M)


def labels(actors):
    return {actor.get_actor_label(): actor for actor in actors}


def import_ambient():
    task = unreal.AssetImportTask()
    task.filename = os.path.join(ROOT, "AssetCreation", "SizeTest", "SM_Size_CloudAmbient.obj")
    task.destination_path = "/Game/HomeWorld/Meshes/SizeTest"
    task.destination_name = "SM_Size_CloudAmbient"
    task.automated = True
    task.save = True
    task.replace_existing = True
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    landed = list(task.imported_object_paths)
    unreal.log("place_size_test_gaps import: " + ", ".join(landed))
    if not landed:
        return None
    return unreal.EditorAssetLibrary.load_asset(landed[0])


def spawn_static(mesh, location, label):
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor, location, unreal.Rotator(0.0, 0.0, 0.0)
    )
    actor.get_component_by_class(unreal.StaticMeshComponent).set_static_mesh(mesh)
    actor.set_actor_label(label)
    return actor


def main():
    ambient = import_ambient()
    bush = unreal.EditorAssetLibrary.load_asset("/Game/HomeWorld/Meshes/SizeTest/SM_Size_BerryBush")
    level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_editor.load_level(MAP_PATH)
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
    have = labels(actors)
    if "SM_Size_BerryBush" not in have and bush is not None:
        spawn_static(bush, vec(890.0, -8.0, 0.0), "SM_Size_BerryBush")
        unreal.log("place_size_test_gaps: spawned berry bush")
    if ambient is not None:
        for label, place in (
            ("SM_Size_CloudAmbient", (350.0, -60.0, 260.0)),
            ("SM_Size_CloudAmbient_B", (640.0, 55.0, 140.0)),
        ):
            if label in have:
                continue
            actor = spawn_static(ambient, vec(*place), label)
            actor.get_component_by_class(unreal.StaticMeshComponent).set_collision_enabled(
                unreal.CollisionEnabled.NO_COLLISION
            )
            unreal.log("place_size_test_gaps: spawned " + label)
    level_editor.save_current_level()
    unreal.log("place_size_test_gaps: saved")
    return 0


if __name__ == "__main__":
    sys.exit(main())

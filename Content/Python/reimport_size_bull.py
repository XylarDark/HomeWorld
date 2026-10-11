"""Import the size-test bull and replace the box bull on the map."""

import os
import sys

try:
    import unreal
except ImportError:
    print("reimport_size_bull: run inside Unreal Editor")
    sys.exit(1)

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
MAP_PATH = "/Game/HomeWorld/Maps/SizeTest/L_SizeTest"


def main():
    task = unreal.AssetImportTask()
    task.filename = os.path.join(ROOT, "AssetCreation", "SizeTest", "SM_Size_Bull.obj")
    task.destination_path = "/Game/HomeWorld/Meshes/SizeTest"
    task.destination_name = "SM_Size_Bull"
    task.automated = True
    task.save = True
    task.replace_existing = True
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    landed = list(task.imported_object_paths)
    unreal.log("reimport_size_bull: " + ", ".join(landed))
    if not landed:
        return 1
    mesh = unreal.EditorAssetLibrary.load_asset(landed[0])
    size = mesh.get_bounds().box_extent * 2.0
    unreal.log("bounds bull extent_cm %.1f %.1f %.1f" % (size.x, size.y, size.z))
    level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_editor.load_level(MAP_PATH)
    old = None
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        if actor.get_actor_label() == "SK_Size_Bull":
            old = actor
            break
    if old is None:
        unreal.log("reimport_size_bull: no SK_Size_Bull actor")
        return 0
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor, old.get_actor_location(), old.get_actor_rotation()
    )
    actor.get_component_by_class(unreal.StaticMeshComponent).set_static_mesh(mesh)
    actor.set_actor_label("SM_Size_Bull")
    unreal.EditorLevelLibrary.destroy_actor(old)
    level_editor.save_current_level()
    unreal.log("reimport_size_bull: replaced SK_Size_Bull actor")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Import the size-test bull and replace the box bull on the map."""

import os
import sys

try:
    import unreal
except ImportError:
    print("reimport_size_bull: run inside Unreal Editor")
    sys.exit(1)

sys.path.insert(0, os.path.dirname(__file__))
import reimport_size_test

MAP_PATH = "/Game/HomeWorld/Maps/SizeTest/L_SizeTest"
MESH = "/Game/HomeWorld/Meshes/SizeTest/SM_Size_Bull"


def main():
    if reimport_size_test.import_names(["SM_Size_Bull"]) != 0:
        return 1
    mesh = unreal.EditorAssetLibrary.load_asset(MESH)
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

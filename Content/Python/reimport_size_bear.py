"""Import the size-test OBJ meshes and put the bear on the size-test map."""

import os
import sys

try:
    import unreal
except ImportError:
    print("reimport_size_bear: run inside Unreal Editor")
    sys.exit(1)

sys.path.insert(0, os.path.dirname(__file__))
import reimport_size_test

MAP_PATH = "/Game/HomeWorld/Maps/SizeTest/L_SizeTest"
MESH = "/Game/HomeWorld/Meshes/SizeTest/SM_Size_Bear"


def bounds(path):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if asset is None:
        unreal.log("missing " + path)
        return
    size = asset.get_bounds().box_extent * 2.0
    unreal.log("bounds %s extent_cm %.1f %.1f %.1f" % (path, size.x, size.y, size.z))


def replace_bear(mesh):
    level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_editor.load_level(MAP_PATH)
    old = None
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        if actor.get_actor_label() == "SK_Size_Bear":
            old = actor
            break
    if old is None:
        unreal.log("reimport_size_bear: no SK_Size_Bear actor")
        return
    location = old.get_actor_location()
    rotation = old.get_actor_rotation()
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor, location, rotation
    )
    actor.get_component_by_class(unreal.StaticMeshComponent).set_static_mesh(mesh)
    actor.set_actor_label("SM_Size_Bear")
    unreal.EditorLevelLibrary.destroy_actor(old)
    level_editor.save_current_level()
    unreal.log("reimport_size_bear: replaced SK_Size_Bear actor")


def main():
    if reimport_size_test.import_names(["SM_Size_Bear"]) != 0:
        return 1
    bounds(MESH)
    bear = unreal.EditorAssetLibrary.load_asset(MESH)
    if bear is not None:
        replace_bear(bear)
    return 0


if __name__ == "__main__":
    sys.exit(main())

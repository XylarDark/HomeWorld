"""Import the size-test OBJ meshes and put the bear on the size-test map."""

import os
import sys

try:
    import unreal
except ImportError:
    print("reimport_size_bear: run inside Unreal Editor")
    sys.exit(1)

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
NAMES = (
    "SM_Size_Bear",
    "SM_Size_Pine_S",
    "SM_Size_Pine_M",
    "SM_Size_Pine_L",
    "SM_Size_Kettle",
)
MAP_PATH = "/Game/HomeWorld/Maps/SizeTest/L_SizeTest"


def bounds(path):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if asset is None:
        unreal.log("missing " + path)
        return
    size = asset.get_bounds().box_extent * 2.0
    unreal.log("bounds %s extent_cm %.1f %.1f %.1f" % (path, size.x, size.y, size.z))


def import_one(tools, name):
    task = unreal.AssetImportTask()
    task.filename = os.path.join(ROOT, "AssetCreation", "SizeTest", name + ".obj")
    task.destination_path = "/Game/HomeWorld/Meshes/SizeTest"
    task.destination_name = name
    task.automated = True
    task.save = True
    task.replace_existing = True
    tools.import_asset_tasks([task])
    landed = list(task.imported_object_paths)
    unreal.log("reimport_size_bear: %s -> %s" % (name, ", ".join(landed)))
    return landed


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
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    bear = None
    failed = 0
    for name in NAMES:
        landed = import_one(tools, name)
        if not landed:
            failed += 1
            continue
        asset = unreal.EditorAssetLibrary.load_asset(landed[0])
        bounds(landed[0])
        if name == "SM_Size_Bear":
            bear = asset
    if bear is not None:
        replace_bear(bear)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

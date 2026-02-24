# test_pcg_forest.py
# PythonAutomationTest: validates PCG forest configuration.

import unreal


def test_pcg_graph_asset():
    """PCG graph asset exists and can be loaded."""
    path = "/Game/HomeWorld/PCG/ForestIsland_PCG"
    assert unreal.EditorAssetLibrary.does_asset_exist(path), "PCG graph not found"
    asset = unreal.load_asset(path)
    assert asset, "Could not load PCG graph"


def test_pcg_volume_in_level():
    """At least one PCG Volume exists in the current editor level."""
    world = unreal.EditorLevelLibrary.get_editor_world()
    assert world, "No editor world open"
    volumes = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.PCGVolume)
    assert volumes and len(volumes) > 0, "No PCG Volume actors in level"


def test_static_mesh_actors_generated():
    """PCG has generated a reasonable number of static mesh actors (trees/rocks)."""
    world = unreal.EditorLevelLibrary.get_editor_world()
    assert world, "No editor world open"
    actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.StaticMeshActor)
    count = len(actors) if actors else 0
    assert count > 100, \
        "Only %d StaticMeshActors in level; expected >100 from PCG forest" % count

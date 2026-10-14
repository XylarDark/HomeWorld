# test_place_field_greybox.py
# Guards the field placer's sheet contract and its save gate.
#
# place_field_greybox.py runs only inside the Editor, but four of its pieces do
# not need Unreal: the metrics reader, the forest station walk, the herb node
# rule, and the sun pose. The first version also saved the map and exited 0 when
# a mesh was missing, so a run with a hole in it looked like a pass - the save
# gate is guarded here too, against a stubbed Editor.
#
# The stub Rotator is keyword-only on purpose. A positional unreal.Rotator is
# (roll, pitch, yaw), so Rotator(-45.0, 30.0, 0.0) - the value this file used to
# carry - puts the elevation in the inert roll slot and the azimuth into pitch:
# a sun that lights upward. A positional call now raises here instead of
# becoming a wrong sun in the Editor. See docs/KNOWN_ERRORS.md.

import importlib.util
import os
import sys
import types

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_PYTHON = os.path.normpath(os.path.join(_HERE, ".."))
SCRIPT = os.path.join(_PYTHON, "place_field_greybox.py")

HERB_CENTRES = 104
BULL_COUNT = 104
TREE_COUNT = 8
HERB_NODES = 144
FOREST_STATIONS = 36


class _Rotator:
    """Rotator stub that refuses positional args (see the header)."""

    def __init__(self, *, roll=0.0, pitch=0.0, yaw=0.0):
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw


class _Vector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z


class _Component:
    def set_static_mesh(self, mesh):
        self.mesh = mesh

    def set_skeletal_mesh(self, mesh):
        self.mesh = mesh

    def set_collision_profile_name(self, name):
        self.profile = name

    def set_collision_enabled(self, enabled):
        self.collision = enabled


class _Actor:
    """Enough of an actor for the placer to place and pose it."""

    def __init__(self, actor_class):
        self.actor_class = actor_class
        self.label = ""
        self.component = _Component()
        self.location = _Vector()
        self.rotation = None

    def set_actor_label(self, label):
        self.label = label

    def get_actor_label(self):
        return self.label

    def get_class(self):
        return types.SimpleNamespace(get_name=lambda: "Actor")

    def get_component_by_class(self, component_class):
        return self.component

    def set_actor_location(self, location, sweep, teleport):
        self.location = location

    def get_actor_location(self):
        return self.location

    def set_actor_rotation(self, rotation, teleport):
        self.rotation = rotation

    def get_actor_rotation(self):
        return self.rotation

    def set_actor_scale3d(self, scale):
        self.scale = scale

    def get_actor_bounds(self, only_colliding):
        """A 1 m cube resting on the floor, so the bottom is at z = 0."""
        return _Vector(0.0, 0.0, 50.0), _Vector(50.0, 50.0, 50.0)


class _CollisionEnabled:
    QUERY_AND_PHYSICS = "query_and_physics"
    NO_COLLISION = "no_collision"


def _base_stub():
    stub = types.ModuleType("unreal")
    stub.log = lambda *args, **kwargs: None
    stub.Rotator = _Rotator
    stub.Vector = _Vector
    stub.CollisionEnabled = _CollisionEnabled
    stub.StaticMeshActor = "StaticMeshActor"
    stub.SkeletalMeshActor = "SkeletalMeshActor"
    stub.DirectionalLight = "DirectionalLight"
    stub.SkyLight = "SkyLight"
    stub.SkyAtmosphere = "SkyAtmosphere"
    stub.PlayerStart = "PlayerStart"
    stub.StaticMeshComponent = "StaticMeshComponent"
    stub.SkeletalMeshComponent = "SkeletalMeshComponent"
    stub.LevelEditorSubsystem = "LevelEditorSubsystem"
    stub.EditorActorSubsystem = "EditorActorSubsystem"
    stub.EditorLevelLibrary = types.SimpleNamespace(
        spawn_actor_from_class=lambda actor_class, location, rotation: _Actor(actor_class)
    )
    return stub


def _load(monkeypatch, stub):
    monkeypatch.setitem(sys.modules, "unreal", stub)
    spec = importlib.util.spec_from_file_location("place_field_greybox", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, "place_field_greybox", module)
    spec.loader.exec_module(module)
    return module


def _empty_level_stub():
    """A stub Editor on an empty level, with every mesh asset missing."""
    stub = _base_stub()

    class _Level:
        loaded = None

        def load_level(self, path):
            self.loaded = path

        def new_level(self, path):
            self.loaded = path

        def save_current_level(self):
            stub.saved.append(True)

    class _Actors:
        def get_all_level_actors(self):
            return []

        def destroy_actor(self, actor):
            raise AssertionError("nothing to destroy on an empty level")

    level = _Level()
    actors = _Actors()

    def _subsystem(subsystem_class):
        if subsystem_class == stub.LevelEditorSubsystem:
            return level
        return actors

    stub.saved = []
    stub.get_editor_subsystem = _subsystem
    stub.EditorAssetLibrary = types.SimpleNamespace(
        does_asset_exist=lambda path: True,
        load_asset=lambda path: None,
    )
    return stub


def _placed_asset_stub():
    """A stub Editor where every asset loads, so nothing has to fail."""
    stub = _empty_level_stub()
    stub.EditorAssetLibrary = types.SimpleNamespace(
        does_asset_exist=lambda path: True,
        load_asset=lambda path: object(),
    )
    return stub


@pytest.fixture()
def placer(monkeypatch):
    return _load(monkeypatch, _base_stub())


def test_metrics_sheet_matches_the_placer_contract(placer):
    metrics = placer.load_metrics()

    assert len(metrics["herbs"]) == HERB_CENTRES
    assert len(metrics["bulls"]) == BULL_COUNT
    assert len(metrics["trees"]) == TREE_COUNT
    assert metrics["player"]["x"] == 0 and metrics["player"]["y"] == 0


def test_forest_stations_start_at_the_shared_corner(placer):
    forest = placer.load_metrics()["forest"]
    stations = placer.forest_stations(forest)

    assert len(stations) == FOREST_STATIONS
    assert stations[0] == forest["start"] == -210.0
    assert stations[-1] == forest["end"] == 210.0
    assert stations[1] - stations[0] == forest["step"]


def test_herb_nodes_follow_the_scatter_rule(placer):
    assert placer.herb_points({"x": 1.0, "y": 2.0, "kind": "single"}) == [(1.0, 2.0)]
    assert placer.herb_points({"x": 1.0, "y": 2.0, "kind": "dual"}) == [
        (1.0, 2.0),
        (2.0, 2.0),
    ]
    assert placer.herb_points({"x": 1.0, "y": 2.0, "kind": "triple"}) == [
        (1.0, 2.0),
        (2.0, 2.0),
        (1.0, 3.0),
    ]

    nodes = sum(len(placer.herb_points(herb)) for herb in placer.load_metrics()["herbs"])
    assert nodes == HERB_NODES


def test_the_sun_is_posed_with_keyword_args(placer):
    sun = placer.sun_rotator()

    assert (sun.roll, sun.pitch, sun.yaw) == (0.0, placer.SUN_PITCH, placer.SUN_YAW)
    assert placer.SUN_PITCH == -45.0, "45 degrees up is the kept size-test pose"
    assert placer.SUN_YAW == 30.0
    assert placer.yaw_rotator(90.0).yaw == 90.0


def test_a_missing_mesh_saves_nothing(monkeypatch):
    module = _load(monkeypatch, _empty_level_stub())

    assert module.run() == 1, "a run with missing meshes has to fail"
    assert module.FAILED, "the failures have to be recorded, not swallowed"
    # 7 mass cubes (floor, three cliffs, drop, river, bank) plus one per herb node.
    assert module.FAILED.count("no engine cube") == 7 + HERB_NODES
    assert sys.modules["unreal"].saved == [], "a failed run must not save the map"


def test_a_complete_run_saves_once(monkeypatch):
    module = _load(monkeypatch, _placed_asset_stub())

    assert module.run() == 0
    assert module.FAILED == []
    assert sys.modules["unreal"].saved == [True]

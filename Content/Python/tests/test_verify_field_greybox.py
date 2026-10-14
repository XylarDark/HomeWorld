# test_verify_field_greybox.py
# Guards the field verifier: it has to fail when the map drifts from the sheet.
#
# verify_field_greybox.py runs only inside the Editor. Its first version read the
# sheet but only ever compared the sheet with itself - it never re-measured where
# the built actors sat - so a map whose pines had all wandered off their stations
# still reported CHECK PASS. sheet_spots() now states where every mass belongs,
# and the pseudo-level here is built from the sheet, so a pass means the verifier
# really compared the actors to the sheet. Each drift test then moves one thing
# and requires the matching failure, which is the mutation that proves the check
# measured its subject rather than always agreeing.
#
# The stub is deliberately small: only the Editor surface check() touches.

import importlib.util
import os
import sys
import types

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_PYTHON = os.path.normpath(os.path.join(_HERE, ".."))
PLACER = os.path.join(_PYTHON, "place_field_greybox.py")
VERIFIER = os.path.join(_PYTHON, "verify_field_greybox.py")

SPOT_COUNT = 230  # 7 mass cubes + 71 pines + 8 trees + 144 herb nodes
PINE_COUNT = 71
HERB_NODES = 144
TREE_COUNT = 8


class _Mesh:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name


class _Component:
    def __init__(self, mesh_name):
        self._mesh = _Mesh(mesh_name) if mesh_name else None

    def get_editor_property(self, name):
        if name == "static_mesh":
            return self._mesh
        raise KeyError(name)


class _Actor:
    """A placed actor: a label, a spot, a class name, and a mesh name."""

    def __init__(self, label, x, y, class_name="StaticMeshActor", mesh_name="", bottom=0.0):
        self.label = label
        self.x = x
        self.y = y
        self.class_name = class_name
        self.component = _Component(mesh_name)
        self.bottom = bottom
        self.rotation = types.SimpleNamespace(roll=0.0, pitch=0.0, yaw=0.0)
        self.scale = types.SimpleNamespace(x=1.0, y=1.0, z=1.0)

    def get_actor_label(self):
        return self.label

    def get_class(self):
        return types.SimpleNamespace(get_name=lambda: self.class_name)

    def get_component_by_class(self, component_class):
        return self.component

    def get_actor_location(self):
        return types.SimpleNamespace(x=self.x, y=self.y, z=0.0)

    def get_actor_rotation(self):
        return self.rotation

    def get_actor_scale3d(self):
        return self.scale

    def get_actor_bounds(self, only_colliding):
        """Origin sits `bottom` + 50 up, so actor_bottom_z() reads `bottom`."""
        origin = types.SimpleNamespace(x=self.x, y=self.y, z=self.bottom + 50.0)
        extent = types.SimpleNamespace(x=50.0, y=50.0, z=50.0)
        return origin, extent


class _Level:
    def __init__(self):
        self.loaded = None

    def load_level(self, path):
        self.loaded = path


class _ActorSystem:
    def __init__(self):
        self.actors = []

    def get_all_level_actors(self):
        return list(self.actors)


def _install(monkeypatch):
    """Stub unreal, load both field modules, and hand back a mutable level."""
    stub = types.ModuleType("unreal")
    stub.logs = []
    stub.log = lambda *args, **kwargs: stub.logs.append(" ".join(str(a) for a in args))
    stub.Rotator = lambda **kwargs: types.SimpleNamespace(**kwargs)
    stub.Vector = types.SimpleNamespace
    stub.StaticMeshComponent = "StaticMeshComponent"
    stub.SkeletalMeshComponent = "SkeletalMeshComponent"
    stub.LevelEditorSubsystem = "LevelEditorSubsystem"
    stub.EditorActorSubsystem = "EditorActorSubsystem"

    level = _Level()
    actor_system = _ActorSystem()

    def _subsystem(subsystem_class):
        if subsystem_class == stub.LevelEditorSubsystem:
            return level
        return actor_system

    stub.get_editor_subsystem = _subsystem
    monkeypatch.setitem(sys.modules, "unreal", stub)

    placer = _load(monkeypatch, "place_field_greybox", PLACER)
    verifier = _load(monkeypatch, "verify_field_greybox", VERIFIER)
    return stub, placer, verifier, actor_system


def _load(monkeypatch, name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, name, module)
    spec.loader.exec_module(module)
    return module


def _sheet_level(placer, verifier, metrics):
    """One actor per sheet spot, plus the lighting set and the player start."""
    sequence = metrics["forest"]["sequence"]
    actors = []
    for label, (x, y) in verifier.sheet_spots(metrics).items():
        mesh = ""
        if label.startswith("SM_Field_Pine_"):
            index = 0 if label.endswith("Corner") else int(label.rsplit("_", 1)[1])
            mesh = sequence[index % len(sequence)]
        actors.append(_Actor(label, x, y, mesh_name=mesh))
    for bull in metrics["bulls"]:
        actors.append(
            _Actor(
                bull["label"],
                bull["x"] * placer.M,
                bull["y"] * placer.M,
                class_name="SkeletalMeshActor",
            )
        )
    actors.append(
        _Actor(
            placer.SUN_LABEL,
            0.0,
            0.0,
            class_name="DirectionalLight",
        )
    )
    sun = actors[-1]
    sun.rotation = types.SimpleNamespace(
        roll=0.0, pitch=placer.SUN_PITCH, yaw=placer.SUN_YAW
    )
    actors.append(_Actor(placer.SKY_LIGHT_LABEL, 0.0, 0.0, class_name="SkyLight"))
    actors.append(
        _Actor(placer.SKY_ATMOSPHERE_LABEL, 0.0, 0.0, class_name="SkyAtmosphere")
    )
    actors.append(_Actor("PlayerStart", 0.0, 0.0, class_name="PlayerStart"))
    for actor in actors:
        if actor.label == metrics["river"]["label"]:
            actor.scale = types.SimpleNamespace(x=metrics["river"]["sx"], y=1.0, z=1.0)
    return actors, sun


@pytest.fixture()
def field(monkeypatch):
    stub, placer, verifier, actor_system = _install(monkeypatch)
    metrics = placer.load_metrics()
    actors, sun = _sheet_level(placer, verifier, metrics)
    actor_system.actors = actors
    return stub, placer, verifier, actor_system, metrics, sun


def test_the_sheet_pins_every_placed_mass(field):
    _, _, verifier, _, metrics, _ = field
    spots = verifier.sheet_spots(metrics)

    assert len(spots) == SPOT_COUNT
    assert sum(label.startswith("SM_Field_Pine_") for label in spots) == PINE_COUNT
    assert sum(label.startswith("SM_Field_Herb_") for label in spots) == HERB_NODES
    assert len([t for t in metrics["trees"]]) == TREE_COUNT
    assert spots["SM_Field_Pine_Corner"] == (
        metrics["forest"]["x_west"] * verifier.M,
        metrics["forest"]["y_south"] * verifier.M,
    )
    assert spots["SM_Field_Pine_S_35"] == (210.0 * verifier.M, -210.0 * verifier.M)
    assert "SM_Field_Herb_%03d" % (HERB_NODES - 1) in spots


def test_a_map_on_the_sheet_passes(field):
    _, _, verifier, _, _, _ = field

    assert verifier.check() == 0
    assert "field_greybox: placed actors on the sheet" in sys.modules["unreal"].logs


def test_a_pine_off_its_station_fails(field):
    _, _, verifier, _, _, _ = field
    actors = sys.modules["unreal"].get_editor_subsystem("EditorActorSubsystem").actors
    for actor in actors:
        if actor.label == "SM_Field_Pine_S_05":
            actor.x += 500.0

    assert verifier.check() == 1
    assert any(
        "SM_Field_Pine_S_05" in line and "off the sheet" in line
        for line in sys.modules["unreal"].logs
    )


def test_a_pine_with_the_wrong_mesh_fails(field):
    _, _, verifier, _, _, _ = field
    actors = sys.modules["unreal"].get_editor_subsystem("EditorActorSubsystem").actors
    for actor in actors:
        if actor.label == "SM_Field_Pine_W_04":
            actor.component = _Component("SM_Not_The_Sequence")

    assert verifier.check() == 1
    assert any("forest pair 4" in line for line in sys.modules["unreal"].logs)


def test_a_herb_off_the_floor_fails(field):
    _, _, verifier, _, _, _ = field
    actors = sys.modules["unreal"].get_editor_subsystem("EditorActorSubsystem").actors
    for actor in actors:
        if actor.label == "SM_Field_Herb_000":
            actor.bottom = 40.0

    assert verifier.check() == 1
    assert any("mesh bottom off the floor" in line for line in sys.modules["unreal"].logs)


def test_a_second_sun_fails(field):
    _, placer, verifier, actor_system, _, _ = field
    actor_system.actors.append(_Actor("Stray_Sun", 0.0, 0.0, class_name="DirectionalLight"))

    assert verifier.check() == 1
    assert any("2 directional lights" in line for line in sys.modules["unreal"].logs)


def test_a_missing_sun_fails(field):
    _, _, verifier, actor_system, _, sun = field
    actor_system.actors.remove(sun)

    assert verifier.check() == 1
    assert any("missing Field_Sun" in line for line in sys.modules["unreal"].logs)


def test_a_wrong_sun_pose_fails(field):
    _, _, verifier, _, _, sun = field
    sun.rotation = types.SimpleNamespace(roll=0.0, pitch=0.0, yaw=0.0)

    assert verifier.check() == 1
    assert any("sun pitch/yaw" in line for line in sys.modules["unreal"].logs)

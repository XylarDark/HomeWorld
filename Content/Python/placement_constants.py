"""Height, standoff, tag names, and light presets.

The cabin shell, the placer, and the reveal read placement_constants.json.
A placer asks for a preset by name: candle, lamplight, or night.
"""

import json
import os

_PATH = os.path.join(os.path.dirname(__file__), "placement_constants.json")


def load():
    with open(_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


DATA = load()


def counter():
    return DATA["counter"]


def standoff(name):
    return DATA["standoff_cm"][name]


def tag(name):
    return DATA["tags"][name]


def light(name):
    return DATA["lights"][name]


def apply_light(comp, name, local_z):
    """Write one preset onto a point-light component. unreal is the editor module."""
    import unreal

    preset = light(name)
    split = preset["split_z"]
    intensity = preset["intensity_below"] if local_z < split else preset["intensity_above"]
    comp.set_editor_property("intensity", intensity)
    comp.set_editor_property("attenuation_radius", preset["attenuation_radius"])
    comp.set_editor_property("source_radius", preset["source_radius"])
    comp.set_editor_property("use_temperature", True)
    comp.set_editor_property("temperature", preset["temperature"])
    comp.set_editor_property("cast_shadows", True)
    comp.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)

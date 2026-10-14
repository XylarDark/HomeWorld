"""Measure the field greybox. Do not move actors and do not save."""

import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import place_field_greybox

importlib.reload(place_field_greybox)

MAP_PATH = place_field_greybox.MAP_PATH
M = place_field_greybox.M


def mesh_name(actor):
    component = actor.get_component_by_class(__import__("unreal").StaticMeshComponent)
    if component is None:
        return ""
    mesh = component.get_editor_property("static_mesh")
    return mesh.get_name() if mesh is not None else ""


def check():
    import unreal

    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(MAP_PATH)
    metrics = place_field_greybox.load_metrics()
    found = place_field_greybox.by_label()
    errors = []
    banned = ("Path", "Landing", "Camp", "Shrine")
    for label in found:
        for word in banned:
            if word.lower() in label.lower():
                errors.append("banned actor " + label)

    required = [
        metrics["floor"]["label"],
        metrics["drop"]["label"],
        metrics["river"]["label"],
        metrics["river_bank"]["label"],
        "SM_Field_Pine_Corner",
        "PlayerStart",
    ]
    required.extend(cliff["label"] for cliff in metrics["cliffs"])
    for label in required:
        if label not in found:
            errors.append("missing " + label)

    river = found.get(metrics["river"]["label"])
    if river is not None:
        scale = river.get_actor_scale3d()
        if abs(scale.x - metrics["river"]["sx"]) > 0.05:
            errors.append("river width is %.2f" % scale.x)

    sequence = metrics["forest"]["sequence"]
    stations = place_field_greybox.forest_stations(metrics["forest"])
    south = []
    west = []
    for index in range(1, len(stations)):
        south_actor = found.get("SM_Field_Pine_S_%02d" % index)
        west_actor = found.get("SM_Field_Pine_W_%02d" % index)
        if south_actor is None or west_actor is None:
            errors.append("forest pair %d missing" % index)
            break
        south.append(mesh_name(south_actor))
        west.append(mesh_name(west_actor))
        expected = sequence[index % len(sequence)]
        if south[-1] != expected or west[-1] != expected:
            errors.append("forest pair %d is not %s" % (index, expected))
            break
    if south != west:
        errors.append("forest edges differ")
    else:
        unreal.log("field_greybox: forests identical")

    herb_centres = [(item["x"] * M, item["y"] * M) for item in metrics["herbs"]]
    for left in range(len(herb_centres)):
        for right in range(left + 1, len(herb_centres)):
            dx = herb_centres[left][0] - herb_centres[right][0]
            dy = herb_centres[left][1] - herb_centres[right][1]
            if (dx * dx + dy * dy) ** 0.5 < 30.0 * M - 5.0:
                errors.append("herb centres closer than 30 m")
                break
        else:
            continue
        break

    bulls = metrics.get("bulls", [])
    herbs = metrics["herbs"]
    if abs(len(bulls) - len(herbs)) > 1:
        errors.append("bull count %d is not the herb centre count" % len(bulls))
    beside = 0
    for bull in bulls:
        actor = found.get(bull["label"])
        if actor is None:
            errors.append("missing " + bull["label"])
            continue
        loc = actor.get_actor_location()
        if abs(loc.x - bull["x"] * M) > 50.0 or abs(loc.y - bull["y"] * M) > 50.0:
            errors.append(bull["label"] + " is off the sheet")
        nearest = min(
            ((bull["x"] - herb["x"]) ** 2 + (bull["y"] - herb["y"]) ** 2) ** 0.5
            for herb in herbs
        )
        if nearest <= 4.0:
            beside += 1
    if bulls and abs(beside - len(bulls) / 2.0) > 1.0:
        errors.append("bulls beside a herb %d is not half" % beside)
    else:
        unreal.log("field_greybox: bulls %d beside %d" % (len(bulls), beside))

    player = found.get("PlayerStart")
    if player is not None:
        loc = player.get_actor_location()
        if abs(loc.x) > 2.0 or abs(loc.y) > 2.0:
            errors.append("arrival is not the meadow centre")

    for error in errors:
        unreal.log("field_greybox: FAIL " + error)
    if errors:
        unreal.log("field_greybox: CHECK FAIL")
        return 1
    unreal.log("field_greybox: CHECK PASS")
    return 0


if __name__ == "__main__":
    sys.exit(check())

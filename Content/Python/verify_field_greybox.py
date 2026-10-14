"""Measure the field greybox. Do not move actors and do not save."""

import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import place_field_greybox

importlib.reload(place_field_greybox)

MAP_PATH = place_field_greybox.MAP_PATH
M = place_field_greybox.M
FLOOR_TOP_CM = 0.0
BOTTOM_TOLERANCE_CM = 2.0
#: The sheet carries metres to 0.1 m, so a placed actor should land on its
#: sheet spot to within that 10 cm. The first version never re-measured this.
POSITION_TOLERANCE_CM = 10.0
BOTTOM_PREFIXES = (
    "SM_Field_Pine_",
    "SM_Field_Tree_",
    "SM_Field_Herb_",
    "SK_Field_Bull_",
)
LIGHT_LABELS = (
    place_field_greybox.SUN_LABEL,
    place_field_greybox.SKY_LIGHT_LABEL,
    place_field_greybox.SKY_ATMOSPHERE_LABEL,
)


def mesh_name(actor):
    component = actor.get_component_by_class(__import__("unreal").StaticMeshComponent)
    if component is None:
        return ""
    mesh = component.get_editor_property("static_mesh")
    return mesh.get_name() if mesh is not None else ""


def actor_bottom_z(actor):
    origin, extent = actor.get_actor_bounds(False)
    return origin.z - extent.z


def sheet_spots(metrics):
    """label -> (x_cm, y_cm) for every mass the sheet pins, in sheet order.

    The first version read the sheet only to compare it with itself: a map whose
    pines had all wandered off their stations still passed, because nothing
    re-measured where the built actors actually sat. This walks the same sheet
    the placer reads, so check() can compare the built actor to the sheet. Bulls
    are pinned by the bull block instead, which also carries the beside rule.
    """
    spots = {}
    for key in ("floor", "drop", "river", "river_bank"):
        item = metrics[key]
        spots[item["label"]] = (item["x"] * M, item["y"] * M)
    for cliff in metrics["cliffs"]:
        spots[cliff["label"]] = (cliff["x"] * M, cliff["y"] * M)
    forest = metrics["forest"]
    for index, along in enumerate(place_field_greybox.forest_stations(forest)):
        if index == 0:
            spots["SM_Field_Pine_Corner"] = (
                forest["x_west"] * M,
                forest["y_south"] * M,
            )
            continue
        spots["SM_Field_Pine_S_%02d" % index] = (along * M, forest["y_south"] * M)
        spots["SM_Field_Pine_W_%02d" % index] = (forest["x_west"] * M, along * M)
    for tree in metrics.get("trees", []):
        spots[tree["label"]] = (tree["x"] * M, tree["y"] * M)
    index = 0
    for herb in metrics["herbs"]:
        for x, y in place_field_greybox.herb_points(herb):
            spots["SM_Field_Herb_%03d" % index] = (x * M, y * M)
            index += 1
    return spots


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
    required.extend(LIGHT_LABELS)
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

    off_sheet = []
    for label, (x, y) in sorted(sheet_spots(metrics).items()):
        actor = found.get(label)
        if actor is None:
            continue  # the missing-label check above already reports it
        loc = actor.get_actor_location()
        if (
            abs(loc.x - x) > POSITION_TOLERANCE_CM
            or abs(loc.y - y) > POSITION_TOLERANCE_CM
        ):
            off_sheet.append(
                "%s at %.0f,%.0f wants %.0f,%.0f" % (label, loc.x, loc.y, x, y)
            )
    if off_sheet:
        errors.append(
            "%d actor(s) off the sheet: %s"
            % (len(off_sheet), ", ".join(off_sheet[:4]))
        )
    else:
        unreal.log("field_greybox: placed actors on the sheet")

    directional = [
        actor
        for actor in place_field_greybox.actors()
        if "DirectionalLight" in (actor.get_class().get_name() or "")
    ]
    if len(directional) != 1:
        errors.append("%d directional lights, want 1" % len(directional))

    sun = found.get(place_field_greybox.SUN_LABEL)
    if sun is not None:
        rotation = sun.get_actor_rotation()
        if (
            abs(rotation.pitch - place_field_greybox.SUN_PITCH) > 1.0
            or abs(rotation.yaw - place_field_greybox.SUN_YAW) > 1.0
        ):
            errors.append(
                "sun pitch/yaw is %.1f/%.1f, want %.1f/%.1f"
                % (
                    rotation.pitch,
                    rotation.yaw,
                    place_field_greybox.SUN_PITCH,
                    place_field_greybox.SUN_YAW,
                )
            )

    off_floor = []
    for label, actor in found.items():
        if not label.startswith(BOTTOM_PREFIXES):
            continue
        bottom = actor_bottom_z(actor)
        if abs(bottom - FLOOR_TOP_CM) > BOTTOM_TOLERANCE_CM:
            off_floor.append("%s %.1f" % (label, bottom))
    if off_floor:
        errors.append(
            "mesh bottom off the floor on %d actor(s): %s"
            % (len(off_floor), ", ".join(sorted(off_floor)[:5]))
        )
    else:
        unreal.log("field_greybox: mesh bottoms on the floor")

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

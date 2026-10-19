"""Standard wisp hover for an interactable.

Same rule as HomeWorldWispPlacement.cpp. Static meshes only. Rune ribbons
are left out. If the mesh top reaches head height, the point stays at head height, 40 cm from center.
If the mesh top is below the head, the point floats 40 cm above that top and 36 cm past the right face.

This audit has no player, so the viewer stands 3 m south of the prop and
the head is one standing height above the walk pad (45000 + 176 cm).

Run in the open editor: execute_python_script Content/Python/wisp_place.py
"""

import unreal

HOVER_SIDE_CM = 40.0
HOVER_AWAY_CM = 36.0
HOVER_AWAY_MAX_CM = 160.0
HOVER_ABOVE_CM = 40.0
PAD_TOP_CM = 45000.0
HEAD_Z = PAD_TOP_CM + 176.0


def _mesh_box(actor):
    origin = None
    extent = None
    for component in actor.get_components_by_class(unreal.StaticMeshComponent):
        if component.get_editor_property("static_mesh") is None:
            continue
        if not component.get_editor_property("visible"):
            continue
        outer = component.get_outer()
        if outer is not None and outer.get_class().get_name() == "HomeWorldRuneShapeComponent":
            continue
        world_origin, world_extent, _radius = unreal.SystemLibrary.get_component_bounds(component)
        if origin is None:
            origin = unreal.Vector(
                world_origin.x - world_extent.x,
                world_origin.y - world_extent.y,
                world_origin.z - world_extent.z,
            )
            extent = unreal.Vector(
                world_origin.x + world_extent.x,
                world_origin.y + world_extent.y,
                world_origin.z + world_extent.z,
            )
        else:
            origin = unreal.Vector(
                min(origin.x, world_origin.x - world_extent.x),
                min(origin.y, world_origin.y - world_extent.y),
                min(origin.z, world_origin.z - world_extent.z),
            )
            extent = unreal.Vector(
                max(extent.x, world_origin.x + world_extent.x),
                max(extent.y, world_origin.y + world_extent.y),
                max(extent.z, world_origin.z + world_extent.z),
            )
    if origin is None:
        return None
    center = unreal.Vector(
        (origin.x + extent.x) * 0.5,
        (origin.y + extent.y) * 0.5,
        (origin.z + extent.z) * 0.5,
    )
    half = unreal.Vector(
        (extent.x - origin.x) * 0.5,
        (extent.y - origin.y) * 0.5,
        (extent.z - origin.z) * 0.5,
    )
    return center, half


def hover_point(actor):
    """Rest point, cm. Bob is not included.

    Viewer stands 3 m south and looks north. Their right is -X, matching
    Up cross Look in the game.
    """
    found = _mesh_box(actor)
    if found is None:
        return None
    center, half = found
    right = unreal.Vector(-1.0, 0.0, 0.0)
    top_z = center.z + half.z
    if top_z >= HEAD_Z:
        side = HOVER_SIDE_CM
        height = HEAD_Z
    else:
        side_reach = abs(half.x * right.x) + abs(half.y * right.y)
        side = min(side_reach + HOVER_AWAY_CM, HOVER_AWAY_MAX_CM)
        height = top_z + HOVER_ABOVE_CM
    return unreal.Vector(
        center.x + right.x * side,
        center.y + right.y * side,
        height,
    )


def log_opening_targets():
    world_actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
    names = ("HerbBed", "Lupine", "Kettle", "OpeningDog", "Armor", "Zipline")
    count = 0
    for actor in world_actors:
        label = actor.get_actor_label()
        if not any(name in label for name in names):
            continue
        point = hover_point(actor)
        if point is None:
            unreal.log("wisp_place: %s no mesh" % label)
            continue
        unreal.log("wisp_place: %s hover (%.0f, %.0f, %.0f)" % (label, point.x, point.y, point.z))
        count += 1
    unreal.log("wisp_place: %d targets" % count)
    return count


log_opening_targets()

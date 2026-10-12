"""Greybox masses at the locked meters. Mixar only. Texture off.

Measured: cottage, herb-bed planter, shrine.
Silhouette rebuilds: pines, lupine, herb, wood, berry, bush, rock, bear, bull, kettle, clouds.
Characters stay on their existing rigs.
"""

import math
import os

import bmesh
import bpy
from mathutils import Vector

OUT = r"C:\dev\HomeWorld\AssetCreation\SizeTest"
REVIEW = os.path.join(OUT, "review")
os.makedirs(REVIEW, exist_ok=True)


def shade_flat(obj):
    for poly in obj.data.polygons:
        poly.use_smooth = False


def box(name, x0, y0, z0, x1, y1, z1):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=((x0 + x1) * 0.5, (y0 + y1) * 0.5, (z0 + z1) * 0.5),
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (max(abs(x1 - x0), 0.02), max(abs(y1 - y0), 0.02), max(abs(z1 - z0), 0.02))
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    shade_flat(obj)
    return obj


def cone(name, radius, height, x, y, z, verts=6, tilt=0.0, yaw=0.0):
    bpy.ops.mesh.primitive_cone_add(
        vertices=verts,
        radius1=radius,
        radius2=max(radius * 0.15, 0.02),
        depth=height,
        location=(x, y, z + height * 0.5),
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_euler = (math.radians(tilt), 0.0, math.radians(yaw))
    bpy.ops.object.transform_apply(rotation=True, location=True)
    shade_flat(obj)
    return obj


def sphere(name, radius, x, y, z, smooth=False):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=radius, location=(x, y, z))
    obj = bpy.context.active_object
    obj.name = name
    if smooth:
        bpy.ops.object.shade_smooth()
    else:
        shade_flat(obj)
    return obj


def join(parts, name):
    bpy.ops.object.select_all(action="DESELECT")
    for part in parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    obj = bpy.context.active_object
    obj.name = name
    return obj


def bounds(obj):
    xs = [v.co.x for v in obj.data.vertices]
    ys = [v.co.y for v in obj.data.vertices]
    zs = [v.co.z for v in obj.data.vertices]
    return min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)


def apply_scale(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(scale=True)


def shift(obj, dx, dy, dz):
    obj.location = (dx, dy, dz)
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True)


def fit_z(obj, target):
    _, _, _, _, z0, z1 = bounds(obj)
    obj.scale = (target / max(z1 - z0, 0.001),) * 3
    apply_scale(obj)
    x0, x1, y0, y1, z0, _ = bounds(obj)
    shift(obj, -((x0 + x1) * 0.5), -((y0 + y1) * 0.5), -z0)


def fit_x(obj, target):
    x0, x1, _, _, _, _ = bounds(obj)
    span = max(x1 - x0, 0.001)
    obj.scale = (target / span, target / span, target / span)
    apply_scale(obj)
    x0, x1, y0, y1, z0, _ = bounds(obj)
    shift(obj, -((x0 + x1) * 0.5), -((y0 + y1) * 0.5), -z0)


def export_fbx(obj, filename):
    path = os.path.join(OUT, filename)
    temp = os.path.join(OUT, "_" + filename)
    if os.path.exists(temp):
        os.remove(temp)
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.fbx(
        filepath=temp,
        use_selection=True,
        object_types={"MESH"},
        apply_scale_options="FBX_SCALE_ALL",
        mesh_smooth_type="FACE",
        axis_forward="-Z",
        axis_up="Y",
    )
    if os.path.exists(path):
        os.remove(path)
    os.replace(temp, path)
    x0, x1, y0, y1, z0, z1 = bounds(obj)
    print(
        "mesh",
        filename,
        round(x1 - x0, 2),
        round(y1 - y0, 2),
        round(z1 - z0, 2),
    )


def look_at(camera, target):
    direction = target - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def render_obj(obj, filename):
    x0, x1, y0, y1, z0, z1 = bounds(obj)
    center = Vector(((x0 + x1) * 0.5, (y0 + y1) * 0.5, (z0 + z1) * 0.5))
    span = max(x1 - x0, y1 - y0, z1 - z0, 0.01)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = 8
    scene.render.resolution_x = 640
    scene.render.resolution_y = 640
    world = scene.world or bpy.data.worlds.new("ReviewWorld")
    scene.world = world
    world.use_nodes = True
    background = world.node_tree.nodes.get("Background")
    if background:
        background.inputs[0].default_value = (0.72, 0.72, 0.72, 1.0)
        background.inputs[1].default_value = 0.8
    if "ReviewSun" not in bpy.data.objects:
        light_data = bpy.data.lights.new("ReviewSun", "SUN")
        light_data.energy = 4.0
        light = bpy.data.objects.new("ReviewSun", light_data)
        scene.collection.objects.link(light)
        light.rotation_euler = (math.radians(55), 0.0, math.radians(30))
    if "ReviewCam" not in bpy.data.objects:
        camera_data = bpy.data.cameras.new("ReviewCam")
        camera_data.lens = 50
        camera = bpy.data.objects.new("ReviewCam", camera_data)
        scene.collection.objects.link(camera)
    camera = bpy.data.objects["ReviewCam"]
    scene.camera = camera
    camera.location = center + Vector((0.0, -span * 1.7, span * 0.25))
    look_at(camera, center)
    scene.render.filepath = os.path.join(REVIEW, os.path.splitext(filename)[0] + ".png")
    bpy.ops.render.render(write_still=True)


def finish(parts, name, filename, height=None, length=None):
    obj = join(parts, name)
    if height:
        fit_z(obj, height)
    if length:
        fit_x(obj, length)
    render_obj(obj, filename)
    export_fbx(obj, filename)
    bpy.data.objects.remove(obj, do_unlink=True)


def clear_meshes():
    for obj in list(bpy.context.scene.objects):
        if obj.type == "MESH":
            bpy.data.objects.remove(obj, do_unlink=True)


def cut_segments(span, holes):
    segments = [span]
    for hole in holes:
        nxt = []
        for left, right in segments:
            if hole[1] <= left or hole[0] >= right:
                nxt.append((left, right))
                continue
            if left < hole[0]:
                nxt.append((left, hole[0]))
            if hole[1] < right:
                nxt.append((hole[1], right))
        segments = nxt
    return [(left, right) for left, right in segments if right - left > 0.08]


def log_wall(parts, name, x0, x1, y0, y1, z0, z1, holes):
    count = 8
    gap = 0.06
    course = ((z1 - z0) - gap * (count - 1)) / count
    for index in range(count):
        cz0 = z0 + index * (course + gap)
        cz1 = cz0 + course
        active = [hole[2:] for hole in holes if not (cz1 <= hole[0] or cz0 >= hole[1])]
        for left, right in cut_segments((x0, x1), active):
            parts.append(box(f"{name}_{index}_{left:.2f}", left, y0, cz0, right, y1, cz1))


def build_cottage():
    parts = []
    parts.append(box("PorchDeck", 0.0, 0.0, 0.0, 9.0, 2.0, 0.25))
    log_wall(parts, "WallW", 0.0, 0.45, 2.0, 11.0, 0.0, 5.0, [])
    log_wall(parts, "WallE", 8.55, 9.0, 2.0, 11.0, 0.0, 5.0, [])
    log_wall(parts, "WallN", 0.45, 8.55, 10.55, 11.0, 0.0, 5.0, [])
    log_wall(
        parts,
        "WallS",
        0.45,
        8.55,
        2.0,
        2.45,
        0.0,
        5.0,
        [(0.0, 3.0, 5.0, 6.0), (2.1, 3.4, 1.2, 2.5), (2.1, 3.4, 6.7, 8.0)],
    )
    parts.append(box("Door", 5.15, 2.12, 0.08, 5.85, 2.28, 2.85))
    parts.append(box("SillL", 1.15, 2.05, 2.05, 2.55, 2.2, 2.18))
    parts.append(box("SillR", 6.65, 2.05, 2.05, 8.05, 2.2, 2.18))
    for index, z0 in enumerate((5.08, 5.75, 6.4, 7.05)):
        inset = (z0 - 5.0) / 3.0 * 4.5
        z1 = z0 + 0.38
        if index == 1:
            parts.append(box("GableL", inset, 1.95, z0, 3.8, 2.35, z1))
            parts.append(box("GableR", 5.2, 1.95, z0, 9.0 - inset, 2.35, z1))
        else:
            parts.append(box(f"Gable{index}", inset, 1.95, z0, 9.0 - inset, 2.35, z1))
    parts.append(box("GableWin", 4.05, 2.05, 5.9, 4.95, 2.22, 6.7))
    mesh = bpy.data.meshes.new("Roof")
    verts = [
        (-0.4, 1.65, 4.8),
        (9.4, 1.65, 4.8),
        (9.4, 11.3, 4.8),
        (-0.4, 11.3, 4.8),
        (4.5, 1.5, 8.1),
        (4.5, 11.45, 8.1),
    ]
    mesh.from_pydata(verts, [], [(0, 4, 5, 3), (1, 2, 5, 4), (0, 1, 4), (3, 5, 2)])
    mesh.update()
    roof = bpy.data.objects.new("Roof", mesh)
    bpy.context.scene.collection.objects.link(roof)
    shade_flat(roof)
    parts.append(roof)
    parts.append(box("PorchRoof", -0.2, -0.2, 3.1, 9.2, 2.2, 3.38))
    for index, x in enumerate((0.2, 3.5, 6.5, 8.5)):
        parts.append(box(f"Post{index}", x, 0.12, 0.25, x + 0.28, 0.42, 3.1))
    for side, x0, x1 in (("L", 0.7, 4.6), ("R", 6.4, 8.3)):
        parts.append(box(f"Rail{side}", x0, 0.2, 0.95, x1, 0.34, 1.08))
        cursor = x0
        baluster = 0
        while cursor < x1:
            parts.append(box(f"Bal{side}{baluster}", cursor, 0.22, 0.25, cursor + 0.08, 0.32, 0.95))
            cursor += 0.4
            baluster += 1
    parts.append(box("Chimney", 7.15, 3.2, 5.3, 8.45, 4.6, 8.7))
    parts.append(box("ChimneyCap", 7.0, 3.05, 8.7, 8.6, 4.75, 9.05))
    obj = join(parts, "SM_Size_Cottage")
    shift(obj, -4.5, -5.5, 0.0)
    render_obj(obj, "SM_Size_Cottage.fbx")
    export_fbx(obj, "SM_Size_Cottage.fbx")
    bpy.data.objects.remove(obj, do_unlink=True)


def build_herb_bed():
    parts = [box("Planter", 0, 0, 0, 2, 1, 0.65), box("Soil", 0.1, 0.1, 0.5, 1.9, 0.9, 0.72)]
    spots = ((0.35, 0.35), (0.7, 0.6), (1.05, 0.35), (1.45, 0.58), (1.6, 0.3))
    for index, (x, y) in enumerate(spots):
        for leaf_index, yaw in enumerate((20, 90, 160, 250, 320)):
            parts.append(cone(f"Leaf{index}_{leaf_index}", 0.08, 0.55, x, y, 0.6, verts=4, tilt=68, yaw=yaw))
        parts.append(cone(f"Spike{index}", 0.06, 0.7, x, y, 0.65, verts=4, tilt=8, yaw=index * 15))
    finish(parts, "SM_Size_HerbBed", "SM_Size_HerbBed.fbx", height=1.4)


def build_rock():
    parts = []
    slabs = (
        ("Base", -1.35, -0.95, 0.0, 1.25, 0.9, 0.55, 0.0, 0.0, 0.05),
        ("Mid", -0.7, -0.55, 0.25, 0.95, 0.65, 1.35, 0.15, 0.2, 0.1),
        ("Shoulder", -0.15, -0.3, 0.85, 0.7, 0.4, 1.9, -0.1, 0.05, 0.2),
        ("Nose", 0.55, -0.35, 0.15, 1.55, 0.4, 0.95, 0.0, 0.35, 0.15),
        ("Chip", -1.2, -0.2, 0.2, -0.45, 0.55, 1.05, 0.4, 0.0, -0.2),
    )
    for name, x0, y0, z0, x1, y1, z1, rx, ry, rz in slabs:
        part = box(name, x0, y0, z0, x1, y1, z1)
        part.rotation_euler = (rx, ry, rz)
        bpy.ops.object.select_all(action="DESELECT")
        part.select_set(True)
        bpy.context.view_layer.objects.active = part
        bpy.ops.object.transform_apply(rotation=True)
        parts.append(part)
    finish(parts, "SM_Size_Rock", "SM_Size_Rock.fbx", height=2.0)


def build_pine(total, trunk_height, filename):
    parts = [cone("Trunk", 0.45, trunk_height, 0, 0, 0, verts=6)]
    foliage = total - trunk_height
    tiers = 5
    for index in range(tiers):
        radius = 1.7 * (1.0 - index / tiers) + 0.2
        height = foliage / tiers * 1.35
        z = trunk_height * 0.92 + foliage * (index / tiers) * 0.82
        parts.append(cone(f"Tier{index}", radius, height, 0, 0, z, verts=7))
    finish(parts, filename.replace(".fbx", ""), filename, height=total)


def build_lupine():
    parts = [cone("Stem", 0.08, 1.7, 0, 0, 0, verts=5)]
    for index, yaw in enumerate(range(0, 360, 40)):
        parts.append(cone(f"Leaf{index}", 0.1, 0.85, 0, 0, 0.15, verts=4, tilt=72, yaw=yaw))
    for index in range(14):
        z = 1.15 + index * 0.12
        radius = 0.22 * (1.0 - index / 16.0)
        parts.append(cone(f"Floret{index}", radius, 0.28, 0, 0, z, verts=5))
        for yaw in (0, 72, 144, 216, 288):
            parts.append(
                cone(
                    f"Petal{index}_{yaw}",
                    radius * 0.55,
                    0.22,
                    0,
                    0,
                    z,
                    verts=4,
                    tilt=58,
                    yaw=yaw + index * 8,
                )
            )
    finish(parts, "SM_Size_Lupine", "SM_Size_Lupine.fbx", height=3.0)


def build_herb():
    parts = []
    for index, yaw in enumerate(range(0, 360, 30)):
        parts.append(cone(f"Herb{index}", 0.07, 0.7, 0, 0, 0.05, verts=4, tilt=60, yaw=yaw))
    for index, yaw in enumerate((15, 80, 150, 230, 300)):
        parts.append(cone(f"HerbUp{index}", 0.06, 0.9, 0, 0, 0.1, verts=4, tilt=25, yaw=yaw))
    finish(parts, "SM_Size_Herb", "SM_Size_Herb.fbx", height=1.0)


def build_wood():
    parts = [
        box("Log", -1.0, -0.16, 0.05, 0.7, 0.16, 0.38),
        box("ForkA", 0.45, -0.05, 0.12, 1.05, 0.18, 0.32),
        box("ForkB", 0.4, -0.22, 0.08, 0.95, -0.02, 0.28),
        box("Knot", -0.2, -0.05, 0.2, 0.05, 0.28, 0.36),
    ]
    finish(parts, "SM_Size_Wood", "SM_Size_Wood.fbx", length=2.0)


def berry_fruit(parts, name, x, y, z, radius):
    points = []
    for index in range(8):
        angle = index / 8 * math.tau
        points.append((x + radius * math.cos(angle), y + radius * 0.85 * math.sin(angle), z))
        points.append((x + radius * 0.7 * math.cos(angle), y + radius * 0.6 * math.sin(angle), z + radius * 0.8))
    points.append((x, y, z + radius * 0.95))
    points.append((x, y, z - radius * 0.2))
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    for point in points:
        bm.verts.new(point)
    bm.verts.ensure_lookup_table()
    bmesh.ops.convex_hull(bm, input=bm.verts)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    shade_flat(obj)
    parts.append(obj)


def build_berry():
    parts = [cone("Stem", 0.06, 0.45, 0, 0, 0, verts=5)]
    for name, x, y, z, radius in (
        ("A", 0.0, 0.0, 0.45, 0.18),
        ("B", 0.2, 0.08, 0.5, 0.16),
        ("C", -0.18, 0.06, 0.48, 0.16),
        ("D", 0.05, -0.18, 0.5, 0.15),
        ("E", 0.02, 0.02, 0.68, 0.17),
    ):
        berry_fruit(parts, name, x, y, z, radius)
    finish(parts, "SM_Size_Berry", "SM_Size_Berry.fbx", height=1.0)


def build_bush():
    parts = []
    for index, (x, y) in enumerate(((-0.35, 0.0), (0.05, 0.15), (0.4, -0.05))):
        parts.append(cone(f"Stem{index}", 0.1, 0.55, x, y, 0, verts=5))
    for index in range(16):
        yaw = index * 23
        radius = 0.7
        angle = math.radians(yaw)
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        parts.append(cone(f"BushLeaf{index}", 0.22, 0.7, x * 0.3, y * 0.3, 0.35, verts=4, tilt=62, yaw=yaw))
    for name, x, y, z in (("A", 0.45, 0.2, 0.7), ("B", -0.5, 0.1, 0.65), ("C", 0.1, -0.45, 0.75), ("D", 0.0, 0.15, 0.95)):
        berry_fruit(parts, name, x, y, z, 0.16)
    finish(parts, "SM_Size_BerryBush", "SM_Size_BerryBush.fbx", height=2.0)


def build_bear():
    parts = [
        box("Body", -1.8, -1.1, 2.2, 1.8, 2.5, 5.0),
        box("Chest", -1.55, -2.0, 2.4, 1.55, -0.5, 4.5),
        box("Head", -1.15, -3.4, 3.1, 1.15, -1.6, 5.2),
        box("Snout", -0.55, -4.2, 3.3, 0.55, -3.1, 4.2),
        box("EarL", -1.2, -2.6, 4.9, -0.45, -1.9, 5.8),
        box("EarR", 0.45, -2.6, 4.9, 1.2, -1.9, 5.8),
        box("LegFL", -1.6, -1.9, 0.0, -0.7, -0.8, 2.7),
        box("LegFR", 0.7, -1.9, 0.0, 1.6, -0.8, 2.7),
        box("LegBL", -1.55, 1.2, 0.0, -0.65, 2.3, 2.6),
        box("LegBR", 0.65, 1.2, 0.0, 1.55, 2.3, 2.6),
    ]
    finish(parts, "SM_Size_Bear", "SM_Size_Bear.fbx")


def build_bull():
    parts = [
        box("Body", -1.3, -1.2, 2.4, 1.3, 2.6, 5.0),
        box("Chest", -1.15, -2.2, 2.5, 1.15, -0.8, 4.7),
        box("Head", -0.9, -3.3, 3.4, 0.9, -1.8, 5.3),
        box("Snout", -0.45, -3.9, 3.3, 0.45, -3.1, 4.2),
        cone("HornL", 0.16, 2.2, -0.55, -2.5, 5.0, verts=5, tilt=-20, yaw=-30),
        cone("HornR", 0.16, 2.2, 0.55, -2.5, 5.0, verts=5, tilt=-20, yaw=30),
        box("LegFL", -1.15, -1.8, 0.0, -0.5, -1.0, 2.8),
        box("LegFR", 0.5, -1.8, 0.0, 1.15, -1.0, 2.8),
        box("LegBL", -1.15, 1.4, 0.0, -0.5, 2.2, 2.7),
        box("LegBR", 0.5, 1.4, 0.0, 1.15, 2.2, 2.7),
    ]
    finish(parts, "SM_Size_Bull", "SM_Size_Bull.fbx")


def build_kettle():
    parts = [
        cone("Pot", 0.38, 0.62, 0, 0, 0.05, verts=8),
        cone("Lid", 0.2, 0.16, 0, 0, 0.62, verts=8),
        box("Handle", -0.08, -0.42, 0.35, 0.08, -0.28, 0.95),
        box("Spout", 0.2, -0.08, 0.4, 0.55, 0.08, 0.55),
    ]
    finish(parts, "SM_Size_Kettle", "SM_Size_Kettle.fbx", height=1.0)


def build_shrine():
    parts = [
        box("Base", -0.9, -0.7, 0.0, 0.9, 0.7, 0.4),
        box("Stone", -0.55, -0.35, 0.35, 0.55, 0.35, 3.7),
        box("Cap", -0.4, -0.28, 3.55, 0.4, 0.28, 4.0),
    ]
    finish(parts, "SM_Size_Shrine", "SM_Size_Shrine.fbx", height=4.0)


def build_cloud(filename, diameter, lobes):
    parts = []
    for index, (x, y, z, radius) in enumerate(lobes):
        parts.append(sphere(f"Lobe{index}", radius, x, y, z, smooth=True))
    obj = join(parts, filename.replace(".fbx", ""))
    x0, x1, y0, y1, z0, z1 = bounds(obj)
    span = max(x1 - x0, y1 - y0, z1 - z0, 0.001)
    obj.scale = (diameter / span,) * 3
    apply_scale(obj)
    x0, x1, y0, y1, z0, _ = bounds(obj)
    shift(obj, -((x0 + x1) * 0.5), -((y0 + y1) * 0.5), -z0)
    for poly in obj.data.polygons:
        poly.use_smooth = True
    render_obj(obj, filename)
    export_fbx(obj, filename)
    bpy.data.objects.remove(obj, do_unlink=True)


def main():
    clear_meshes()
    build_cottage()
    clear_meshes()
    build_herb_bed()
    clear_meshes()
    build_rock()
    clear_meshes()
    build_pine(5.0, 1.0, "SM_Size_Pine_S.fbx")
    clear_meshes()
    build_pine(7.0, 2.0, "SM_Size_Pine_M.fbx")
    clear_meshes()
    build_pine(9.0, 3.0, "SM_Size_Pine_L.fbx")
    clear_meshes()
    build_lupine()
    clear_meshes()
    build_herb()
    clear_meshes()
    build_wood()
    clear_meshes()
    build_berry()
    clear_meshes()
    build_bush()
    clear_meshes()
    build_bear()
    clear_meshes()
    build_bull()
    clear_meshes()
    build_kettle()
    clear_meshes()
    build_shrine()
    clear_meshes()
    build_cloud(
        "SM_Size_Cloud.fbx",
        72.0,
        ((0, 0, 0, 1.2), (1.4, 0.2, 0.3, 1.0), (-1.3, 0.1, 0.2, 0.95), (0.2, 1.1, 0.4, 0.9), (0.3, -1.0, 0.25, 0.85), (0, 0.2, 1.0, 0.7)),
    )
    clear_meshes()
    build_cloud(
        "SM_Size_CloudAmbient.fbx",
        36.0,
        ((0, 0, 0, 1.0), (0.9, 0.2, 0.15, 0.75), (-0.8, -0.1, 0.1, 0.7), (0.1, 0.7, 0.2, 0.6)),
    )


if __name__ == "__main__":
    main()

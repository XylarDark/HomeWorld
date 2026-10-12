"""Rebuild the greybox masses whose review stills were boxes.

Cottage: 9 m by 11 m, walls 5 m, porch inside that footprint, door 1 m by 3 m.
Herb bed: the 2 m by 1 m measured bed, with the kept planter plants on top.
Rock: one 2 m boulder, flat bottom, large faces.

Run:
  "C:\\Program Files\\Mixar\\mixar.exe" --background --python Tools/Iterate-GreyboxSilhouette.py
"""

import os

import bmesh
import bpy

OUT = r"C:\dev\HomeWorld\AssetCreation\SizeTest"


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


def join(parts, name):
    bpy.ops.object.select_all(action="DESELECT")
    for part in parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    obj = bpy.context.active_object
    obj.name = name
    return obj


def shift(obj, dx, dy, dz):
    obj.location = (dx, dy, dz)
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True)


def export_fbx(obj, filename):
    path = os.path.join(OUT, filename)
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=True,
        object_types={"MESH"},
        apply_scale_options="FBX_SCALE_ALL",
        mesh_smooth_type="FACE",
        axis_forward="-Z",
        axis_up="Y",
    )
    print("wrote", filename)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


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
    gap = 0.05
    course = ((z1 - z0) - gap * (count - 1)) / count
    for index in range(count):
        cz0 = z0 + index * (course + gap)
        cz1 = cz0 + course
        active = [hole[2:] for hole in holes if not (cz1 <= hole[0] or cz0 >= hole[1])]
        for left, right in cut_segments((x0, x1), active):
            parts.append(box(f"{name}_{index}", left, y0, cz0, right, y1, cz1))


def build_cottage():
    # Footprint x 0..9, y 0..11. Porch is the south 2 m. Origin moves to center.
    parts = []
    parts.append(box("PorchDeck", 0.0, 0.0, 0.0, 9.0, 2.0, 0.25))
    parts.append(box("Step", 4.6, -0.35, 0.0, 6.4, 0.05, 0.12))
    log_wall(parts, "WallW", 0.0, 0.4, 2.0, 11.0, 0.0, 5.0, [])
    log_wall(parts, "WallE", 8.6, 9.0, 2.0, 11.0, 0.0, 5.0, [])
    log_wall(parts, "WallN", 0.4, 8.6, 10.6, 11.0, 0.0, 5.0, [])
    log_wall(
        parts,
        "WallS",
        0.4,
        8.6,
        2.0,
        2.4,
        0.0,
        5.0,
        [(0.0, 3.0, 5.0, 6.0), (2.15, 3.35, 1.15, 2.45), (2.15, 3.35, 6.7, 8.0)],
    )
    parts.append(box("Door", 5.08, 2.08, 0.05, 5.92, 2.2, 2.9))
    parts.append(box("WinL", 1.25, 2.08, 2.25, 2.35, 2.18, 3.25))
    parts.append(box("WinR", 6.8, 2.08, 2.25, 7.9, 2.18, 3.25))
    # Gable boards shorten toward the 8 m peak. Ridge runs north-south.
    for index, z0 in enumerate((5.05, 5.7, 6.35, 7.0)):
        inset = (z0 - 5.0) / 3.0 * 4.5
        z1 = z0 + 0.42
        if index == 1:
            parts.append(box("GableL", inset, 2.0, z0, 3.85, 2.35, z1))
            parts.append(box("GableR", 5.15, 2.0, z0, 9.0 - inset, 2.35, z1))
            parts.append(box("GableWin", 3.95, 2.08, 5.85, 5.05, 2.2, 6.85))
        else:
            parts.append(box(f"Gable{index}", inset, 2.0, z0, 9.0 - inset, 2.35, z1))
    mesh = bpy.data.meshes.new("Roof")
    mid = 4.5
    verts = [
        (-0.35, 1.7, 4.85),
        (9.35, 1.7, 4.85),
        (9.35, 11.25, 4.85),
        (-0.35, 11.25, 4.85),
        (mid, 1.55, 8.15),
        (mid, 11.4, 8.15),
    ]
    faces = [(0, 4, 5, 3), (1, 2, 5, 4), (0, 1, 4), (3, 5, 2)]
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    roof = bpy.data.objects.new("Roof", mesh)
    bpy.context.scene.collection.objects.link(roof)
    shade_flat(roof)
    parts.append(roof)
    parts.append(box("PorchRoof", -0.15, -0.15, 3.15, 9.15, 2.15, 3.4))
    for index, x in enumerate((0.25, 3.55, 6.55, 8.55)):
        parts.append(box(f"Post{index}", x, 0.15, 0.25, x + 0.28, 0.43, 3.15))
    for side, x0, x1 in (("L", 0.7, 4.7), ("R", 6.3, 8.3)):
        parts.append(box(f"Rail{side}", x0, 0.22, 0.95, x1, 0.36, 1.08))
        cursor = x0 + 0.15
        baluster = 0
        while cursor < x1 - 0.1:
            parts.append(box(f"Bal{side}{baluster}", cursor, 0.24, 0.25, cursor + 0.08, 0.34, 0.95))
            cursor += 0.38
            baluster += 1
    parts.append(box("Chimney", 7.15, 3.3, 5.4, 8.45, 4.7, 8.7))
    parts.append(box("ChimneyCap", 7.0, 3.15, 8.7, 8.6, 4.85, 9.05))
    cottage = join(parts, "SM_Size_Cottage")
    shift(cottage, -4.5, -5.5, 0.0)
    export_fbx(cottage, "SM_Size_Cottage.fbx")
    bpy.data.objects.remove(cottage, do_unlink=True)


def leaf_clump(parts, name, x, y, z, scale):
    tips = ((0.0, 0.0, 1.0), (0.45, 0.1, 0.7), (-0.4, 0.15, 0.62), (0.1, 0.4, 0.55), (-0.1, -0.35, 0.5))
    for index, (tx, ty, tz) in enumerate(tips):
        parts.append(
            box(
                f"{name}{index}",
                x + tx * scale - 0.06 * scale,
                y + ty * scale - 0.06 * scale,
                z + tz * scale * 0.15,
                x + tx * scale + 0.06 * scale,
                y + ty * scale + 0.06 * scale,
                z + tz * scale,
            )
        )


def build_herb_bed():
    parts = []
    parts.append(box("Bed", 0.0, 0.0, 0.0, 2.0, 1.0, 0.7))
    parts.append(box("Soil", 0.12, 0.12, 0.55, 1.88, 0.88, 0.78))
    spots = ((0.4, 0.35, 0.9), (1.0, 0.55, 0.75), (1.55, 0.4, 1.0), (0.7, 0.7, 0.7))
    for index, (x, y, scale) in enumerate(spots):
        leaf_clump(parts, f"Herb{index}", x, y, 0.7, scale)
    bed = join(parts, "SM_Size_HerbBed")
    shift(bed, -1.0, -0.5, 0.0)
    export_fbx(bed, "SM_Size_HerbBed.fbx")
    bpy.data.objects.remove(bed, do_unlink=True)


def build_rock():
    points = [
        (0.15, 0.2, 0.0),
        (1.35, 0.05, 0.0),
        (1.7, 1.15, 0.0),
        (0.2, 1.45, 0.05),
        (0.85, 0.7, 0.0),
        (0.05, 0.55, 0.7),
        (1.55, 0.25, 0.85),
        (1.65, 1.05, 1.15),
        (0.25, 1.2, 1.25),
        (0.9, 0.35, 1.85),
        (1.15, 0.95, 1.7),
        (0.45, 0.85, 1.55),
        (1.4, 0.6, 0.45),
        (0.3, 0.25, 0.4),
    ]
    mesh = bpy.data.meshes.new("SM_Size_Rock")
    bm = bmesh.new()
    for point in points:
        bm.verts.new(point)
    bm.verts.ensure_lookup_table()
    bmesh.ops.convex_hull(bm, input=bm.verts)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new("SM_Size_Rock", mesh)
    bpy.context.scene.collection.objects.link(obj)
    shade_flat(obj)
    zs = [vertex.co.z for vertex in obj.data.vertices]
    height = max(zs) - min(zs)
    scale = 2.0 / height
    obj.scale = (scale, scale, scale)
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(scale=True)
    xs = [vertex.co.x for vertex in obj.data.vertices]
    ys = [vertex.co.y for vertex in obj.data.vertices]
    zs = [vertex.co.z for vertex in obj.data.vertices]
    shift(obj, -((min(xs) + max(xs)) * 0.5), -((min(ys) + max(ys)) * 0.5), -min(zs))
    export_fbx(obj, "SM_Size_Rock.fbx")
    print(
        "rock",
        round(max(xs) - min(xs), 2),
        round(max(ys) - min(ys), 2),
        round(max(zs) - min(zs), 2),
    )


def main():
    clear_scene()
    build_cottage()
    clear_scene()
    build_herb_bed()
    clear_scene()
    build_rock()


if __name__ == "__main__":
    main()

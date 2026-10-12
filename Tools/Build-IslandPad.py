"""Island pad: flat top at the origin, cone hanging below. Mixar only."""

import os

import bpy

OUT = r"C:\dev\HomeWorld\AssetCreation\SizeTest\SM_Size_Island.fbx"


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
    obj.scale = (abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    shade_flat(obj)
    return obj


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()
# Top of the pad is z = 0. That is the walkable floor.
slab = box("Slab", -20, -15, -1, 20, 15, 0)
# Tip points down. The old cone sat with its tip 3 m above the pad.
bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=14, depth=8, location=(0, 0, -5))
cone = bpy.context.active_object
cone.rotation_euler[0] = 3.14159265
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
shade_flat(cone)
bpy.ops.object.select_all(action="DESELECT")
slab.select_set(True)
cone.select_set(True)
bpy.context.view_layer.objects.active = slab
bpy.ops.object.join()
island = bpy.context.active_object
zs = [v.co.z for v in island.data.vertices]
print("island z", round(min(zs), 2), round(max(zs), 2))
if max(zs) > 0.05:
    raise SystemExit("cone still rises above the pad")
bpy.ops.object.select_all(action="DESELECT")
island.select_set(True)
bpy.ops.export_scene.fbx(
    filepath=OUT,
    use_selection=True,
    object_types={"MESH"},
    apply_scale_options="FBX_SCALE_ALL",
    mesh_smooth_type="FACE",
    axis_forward="-Z",
    axis_up="Y",
)
print("wrote", OUT)

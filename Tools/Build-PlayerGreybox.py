"""Faceted player block. 2 m, head one sixth, origin at the feet.

Run:
  "C:\\Program Files\\Mixar\\mixar.exe" --background --python Tools/Build-PlayerGreybox.py
"""

import math
import os

import bpy

OUT = r"C:\dev\TripoSR\output\player\0\mesh_hand.obj"
HEIGHT = 2
HEAD = HEIGHT / 6.0


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def add_box(name, size, location, rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    return obj


def build():
    clear_scene()
    head_center = HEIGHT - HEAD * 0.5
    add_box("Head", (0.22, 0.24, HEAD), (0.0, 0.0, head_center))
    add_box("Neck", (0.08, 0.08, 0.06), (0.0, 0.0, head_center - HEAD * 0.5 - 0.03))
    add_box("Coat", (0.52, 0.26, 0.62), (0.0, 0.0, 1.16))
    add_box("Hip", (0.32, 0.18, 0.16), (0.0, 0.0, 0.78))
    for side, x in (("L", -0.11), ("R", 0.11)):
        add_box(f"Leg_{side}", (0.12, 0.12, 0.62), (x, 0.0, 0.40))
        add_box(f"Boot_{side}", (0.14, 0.22, 0.10), (x, 0.04, 0.05))
    arm = (0.50, 0.08, 0.08)
    pitch = math.radians(55.0)
    add_box("Arm_L", arm, (-0.48, 0.0, 1.22), (0.0, pitch, 0.0))
    add_box("Arm_R", arm, (0.48, 0.0, 1.22), (0.0, -pitch, 0.0))

    bpy.ops.object.select_all(action="SELECT")
    bpy.context.view_layer.objects.active = bpy.data.objects["Coat"]
    bpy.ops.object.join()
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    body = bpy.context.active_object
    body.name = "SM_Player_Greybox"
    min_z = min(vertex.co.z for vertex in body.data.vertices)
    for vertex in body.data.vertices:
        vertex.co.z -= min_z
    top = max(vertex.co.z for vertex in body.data.vertices)
    if top <= 0.0:
        raise RuntimeError("Player block has no height.")
    scale = HEIGHT / top
    for vertex in body.data.vertices:
        vertex.co *= scale

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    body.select_set(True)
    bpy.ops.wm.obj_export(filepath=OUT, export_selected_objects=True)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    build()

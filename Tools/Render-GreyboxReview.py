"""Render size-test meshes to review stills. Mixar only."""

import math
import os

import bpy
from mathutils import Vector

SRC = r"C:\dev\HomeWorld\AssetCreation\SizeTest"
OUT = os.path.join(SRC, "review")
os.makedirs(OUT, exist_ok=True)

FILES = [
    "SM_Size_Cottage.fbx",
    "SM_Size_HerbBed.fbx",
    "SM_Size_Rock.fbx",
    "SM_Size_Lupine.obj",
    "SM_Size_Pine_S.obj",
    "SM_Size_Berry.obj",
    "SM_Size_BerryBush.obj",
    "SM_Size_Bear.obj",
    "SM_Size_Herb.obj",
    "SM_Size_Wood.obj",
]


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.armatures):
        for item in list(block):
            if item.users == 0:
                block.remove(item)


def mesh_objects():
    return [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]


def world_bounds(objects):
    low = Vector((1e9, 1e9, 1e9))
    high = Vector((-1e9, -1e9, -1e9))
    for obj in objects:
        for corner in obj.bound_box:
            point = obj.matrix_world @ Vector(corner)
            low.x = min(low.x, point.x)
            low.y = min(low.y, point.y)
            low.z = min(low.z, point.z)
            high.x = max(high.x, point.x)
            high.y = max(high.y, point.y)
            high.z = max(high.z, point.z)
    return low, high


def look_at(camera, target):
    direction = target - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def render_file(filename):
    clear_scene()
    path = os.path.join(SRC, filename)
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".obj":
        bpy.ops.wm.obj_import(filepath=path, forward_axis="NEGATIVE_Z", up_axis="Z")
    else:
        bpy.ops.import_scene.fbx(filepath=path)
    objects = mesh_objects()
    if not objects:
        print("empty", filename)
        return
    low, high = world_bounds(objects)
    center = (low + high) * 0.5
    size = high - low
    span = max(size.x, size.y, size.z, 0.01)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = 8
    scene.render.resolution_x = 768
    scene.render.resolution_y = 768
    scene.render.film_transparent = False
    world = scene.world or bpy.data.worlds.new("ReviewWorld")
    scene.world = world
    world.use_nodes = True
    background = world.node_tree.nodes.get("Background")
    if background:
        background.inputs[0].default_value = (0.75, 0.75, 0.75, 1.0)
        background.inputs[1].default_value = 0.6
    light_data = bpy.data.lights.new("ReviewSun", "SUN")
    light_data.energy = 3.0
    light = bpy.data.objects.new("ReviewSun", light_data)
    scene.collection.objects.link(light)
    light.rotation_euler = (math.radians(50), 0.0, math.radians(35))
    camera_data = bpy.data.cameras.new("ReviewCam")
    camera_data.lens = 50
    camera = bpy.data.objects.new("ReviewCam", camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    camera.location = center + Vector((0.0, -span * 1.6, span * 0.35))
    look_at(camera, center)
    stem = os.path.splitext(filename)[0]
    scene.render.filepath = os.path.join(OUT, stem + ".png")
    bpy.ops.render.render(write_still=True)
    print(
        "rendered",
        stem,
        "span",
        round(size.x, 2),
        round(size.y, 2),
        round(size.z, 2),
    )


for name in FILES:
    render_file(name)

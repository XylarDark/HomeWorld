import bpy
import mathutils
import math

name = "SM_NODE_PLANT_SLOT_DAY_PLANTED"
out_close = r"C:\dev\HomeWorld\Docs\qa\stills\plant_slot_day_planted_close.png"
out_ctx = r"C:\dev\HomeWorld\Docs\qa\stills\plant_slot_day_planted_context.png"

obj = bpy.data.objects.get(name) or bpy.data.objects.get("SM_PlantSlot_Soil")
assert obj is not None, "plant slot object missing"

cam = bpy.data.objects.get("HW_STILL_CAM")
if cam is None:
    cam_data = bpy.data.cameras.new("HW_STILL_CAM")
    cam = bpy.data.objects.new("HW_STILL_CAM", cam_data)
    bpy.context.scene.collection.objects.link(cam)
bpy.context.scene.camera = cam

mw = obj.matrix_world
corners = [mw @ mathutils.Vector(c) for c in obj.bound_box]
center = sum(corners, mathutils.Vector()) / 8.0
dims = obj.dimensions
extent = max(float(dims.x), float(dims.y), float(dims.z), 0.2)

def look_at(cam_obj, target, distance, elev_deg, azim_deg):
    elev = math.radians(elev_deg)
    azim = math.radians(azim_deg)
    offset = mathutils.Vector((
        distance * math.cos(elev) * math.sin(azim),
        -distance * math.cos(elev) * math.cos(azim),
        distance * math.sin(elev),
    ))
    cam_obj.location = target + offset
    direction = target - cam_obj.location
    cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
scene.display.shading.light = 'STUDIO'
scene.display.shading.color_type = 'MATERIAL'
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'

look_at(cam, center, distance=max(1.8, extent * 4.5), elev_deg=35, azim_deg=40)
cam.data.lens = 50
scene.render.filepath = out_close
bpy.ops.render.render(write_still=True)

look_at(cam, center, distance=max(6.0, extent * 18.0), elev_deg=28, azim_deg=55)
cam.data.lens = 35
scene.render.filepath = out_ctx
bpy.ops.render.render(write_still=True)

print("HW_STILLS_OK", out_close, out_ctx, "obj", obj.name, "dims", [round(float(v),4) for v in dims])

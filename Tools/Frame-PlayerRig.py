"""Frame the rigged player and start playback. Used when Mixar opens the blend."""

import bpy

armature = bpy.data.objects.get("PlayerRig")
mesh = bpy.data.objects.get("SM_Player_Tripo")
if armature is not None:
    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)
if mesh is not None:
    mesh.select_set(True)

screen = getattr(bpy.context, "screen", None)
if screen is None:
    raise SystemExit(0)

for area in screen.areas:
    if area.type != "VIEW_3D":
        continue
    region = next(region for region in area.regions if region.type == "WINDOW")
    with bpy.context.temp_override(window=bpy.context.window, area=area, region=region):
        bpy.ops.view3d.view_selected(use_all_regions=False)
        if not bpy.context.screen.is_animation_playing:
            bpy.ops.screen.animation_play()
    break

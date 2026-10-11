"""Greybox masses for the homestead-to-camp walk. Whole meters. Texture off.

Run:
  "C:\\Program Files\\Mixar\\mixar.exe" --background --python Tools/Build-SizeTestWorld.py
"""

import math
import os

import bpy
from mathutils import Vector

OUT = r"C:\dev\HomeWorld\AssetCreation\SizeTest"
LOG = os.path.join(OUT, "build_log.txt")
WALK_FRAMES = 32


def log(message):
    print(message)
    os.makedirs(OUT, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as handle:
        handle.write(message + "\n")


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def shade_flat(obj):
    for poly in obj.data.polygons:
        poly.use_smooth = False


def box(name, x0, y0, z0, x1, y1, z1):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) * 0.5, (y0 + y1) * 0.5, (z0 + z1) * 0.5))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    shade_flat(obj)
    return obj


def cone(name, radius, height):
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=radius, depth=height, location=(0.0, 0.0, height * 0.5))
    obj = bpy.context.active_object
    obj.name = name
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    shade_flat(obj)
    return obj


def shift(objects, dx, dy, dz):
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.location = (dx, dy, dz)
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.transform_apply(location=True)


def export_fbx(objects, filename, animated):
    path = os.path.join(OUT, filename)
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=True,
        object_types={"ARMATURE", "MESH"},
        add_leaf_bones=False,
        bake_anim=animated,
        bake_anim_use_all_actions=False,
        bake_anim_use_nla_strips=False,
        bake_anim_force_startend_keying=True,
        axis_forward="-Z",
        axis_up="Y",
        apply_scale_options="FBX_SCALE_ALL",
        mesh_smooth_type="FACE",
    )
    log(f"wrote {filename}")
    for obj in objects:
        bpy.data.objects.remove(obj, do_unlink=True)


def join_selected(name):
    bpy.ops.object.join()
    obj = bpy.context.active_object
    obj.name = name
    shade_flat(obj)
    return obj


def add_bone(armature, name, head, tail, parent):
    bone = armature.data.edit_bones.new(name)
    bone.head = head
    bone.tail = tail
    bone.use_connect = False
    bone.envelope_distance = 0.2
    bone.head_radius = 0.08
    bone.tail_radius = 0.06
    if parent is not None:
        bone.parent = parent
    return bone


def bind_action(armature, name):
    action = bpy.data.actions.new(name)
    anim = armature.animation_data or armature.animation_data_create()
    anim.action = action
    if hasattr(action, "slots"):
        try:
            slot = action.slots.new(id_type="OBJECT", name=armature.name)
        except TypeError:
            slot = action.slots.new("OBJECT", armature.name)
        if hasattr(anim, "action_slot"):
            anim.action_slot = slot
    return action


def key_euler(pose_bone, axis, value, frame):
    euler = [0.0, 0.0, 0.0]
    euler[axis] = value
    pose_bone.rotation_euler = euler
    pose_bone.keyframe_insert(data_path="rotation_euler", frame=frame)


def discover_axis(armature, bone_name, target):
    pose_bone = armature.pose.bones[bone_name]
    pose_bone.rotation_mode = "XYZ"
    rest = pose_bone.tail.copy()
    best = None
    for axis in range(3):
        for sign in (1.0, -1.0):
            euler = [0.0, 0.0, 0.0]
            euler[axis] = sign * 0.5
            pose_bone.rotation_euler = euler
            bpy.context.view_layer.update()
            score = (pose_bone.tail - rest).dot(target)
            if best is None or score > best[0]:
                best = (score, axis, sign)
            pose_bone.rotation_euler = (0.0, 0.0, 0.0)
            bpy.context.view_layer.update()
    return best[1], best[2]


def walk_legs(armature, pairs, leg_amp, knee_amp):
    forward = Vector((0.0, 1.0, 0.0))
    backward = Vector((0.0, -1.0, 0.0))
    sample = pairs[0][0]
    leg_axis, leg_sign = discover_axis(armature, sample, forward)
    knee_name = sample.replace("Upper", "Lower")
    knee_axis, knee_sign = leg_axis, leg_sign
    if knee_name in armature.pose.bones:
        knee_axis, knee_sign = discover_axis(armature, knee_name, backward)
    frames = list(range(1, WALK_FRAMES + 2, 4))
    for frame in frames:
        phase = math.cos((frame - 1) / WALK_FRAMES * math.tau)
        for bone_name, side in pairs:
            swing = phase * side
            key_euler(armature.pose.bones[bone_name], leg_axis, leg_sign * leg_amp * swing, frame)
            lower = bone_name.replace("Upper", "Lower")
            if lower in armature.pose.bones:
                key_euler(
                    armature.pose.bones[lower],
                    knee_axis,
                    knee_sign * (0.15 + knee_amp * max(0.0, -swing)),
                    frame,
                )


def finish_walk(armature, mesh):
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    mesh.select_set(True)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    try:
        bpy.ops.object.parent_set(type="ARMATURE_AUTO")
    except RuntimeError as exc:
        log(f"envelope weights for {mesh.name}: {exc}")
        bpy.ops.object.parent_set(type="ARMATURE_ENVELOPE")
    bpy.ops.object.mode_set(mode="POSE")
    for pose_bone in armature.pose.bones:
        pose_bone.rotation_mode = "XYZ"
    scene = bpy.context.scene
    scene.render.fps = 30
    scene.frame_start = 1
    scene.frame_end = WALK_FRAMES
    bind_action(armature, "Walk")


def build_cottage():
    parts = []
    parts.append(box("Floor", 0, 0, -1, 9, 11, 0))
    parts.append(box("PorchFloor", 0, -2, -1, 9, 0, 0))
    parts.append(box("WallW", 0, 1, 0, 1, 10, 5))
    parts.append(box("WallE", 8, 1, 0, 9, 10, 5))
    parts.append(box("WallN", 0, 10, 0, 9, 11, 5))
    parts.append(box("WallS_L", 0, 0, 0, 5, 1, 5))
    parts.append(box("WallS_R", 6, 0, 0, 9, 1, 5))
    parts.append(box("DoorHead", 5, 0, 3, 6, 1, 5))
    parts.append(box("Hall_L", 1, 3, 0, 5, 4, 5))
    parts.append(box("Hall_R", 6, 3, 0, 8, 4, 5))
    parts.append(box("HallHead", 5, 3, 3, 6, 4, 5))
    parts.append(box("Roof", 0, 0, 5, 9, 11, 6))
    parts.append(box("Ridge", 0, 5, 6, 9, 6, 8))
    parts.append(box("PorchRoof", 0, -2, 3, 9, 0, 4))
    parts.append(box("PostSW", 0, -2, 0, 1, -1, 3))
    parts.append(box("PostSE", 8, -2, 0, 9, -1, 3))
    parts.append(box("Chimney", 8, 1, 5, 9, 2, 7))
    bpy.ops.object.select_all(action="DESELECT")
    for part in parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    cottage = join_selected("SM_Size_Cottage")
    shift([cottage], -4.5, -5.5, 0)
    export_fbx([cottage], "SM_Size_Cottage.fbx", False)


def build_static(name, obj):
    export_fbx([obj], f"{name}.fbx", False)


def build_island():
    slab = box("Slab", -20, -15, -1, 20, 15, 0)
    point = cone("Underside", 16, 8)
    point.location = (0, 0, -5)
    bpy.ops.object.transform_apply(location=True)
    bpy.ops.object.select_all(action="DESELECT")
    slab.select_set(True)
    point.select_set(True)
    bpy.context.view_layer.objects.active = slab
    island = join_selected("SM_Size_Island")
    export_fbx([island], "SM_Size_Island.fbx", False)


def build_pine(height, filename):
    trunk = box("Trunk", -0.5, -0.5, 0, 0.5, 0.5, 1)
    foliage = cone("Foliage", 2, height - 1)
    foliage.location = (0, 0, 1 + (height - 1) * 0.5)
    bpy.ops.object.transform_apply(location=True)
    scale = height / 5.0
    foliage.scale = (scale, scale, 1)
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.select_all(action="DESELECT")
    trunk.select_set(True)
    foliage.select_set(True)
    bpy.context.view_layer.objects.active = trunk
    pine = join_selected(filename.replace(".fbx", ""))
    export_fbx([pine], filename, False)


def biped(name, height):
    hip = height * 0.5
    chest = height * 0.7
    neck = height * 0.82
    arm_x = height * 0.28
    hip_x = height * 0.12
    parts = [
        box("Hips", -hip_x, -hip_x * 0.6, hip - height * 0.08, hip_x, hip_x * 0.6, hip + height * 0.06),
        box("Torso", -hip_x * 1.3, -hip_x * 0.7, hip, hip_x * 1.3, hip_x * 0.7, neck),
        box("Head", -height * 0.1, -height * 0.1, neck, height * 0.1, height * 0.1, height),
        box("ArmL", -arm_x - height * 0.08, -height * 0.05, chest - height * 0.28, -arm_x + height * 0.02, height * 0.05, chest),
        box("ArmR", arm_x - height * 0.02, -height * 0.05, chest - height * 0.28, arm_x + height * 0.08, height * 0.05, chest),
        box("LegL", -hip_x - height * 0.04, -height * 0.05, 0, -hip_x + height * 0.06, height * 0.05, hip),
        box("LegR", hip_x - height * 0.06, -height * 0.05, 0, hip_x + height * 0.04, height * 0.05, hip),
    ]
    bpy.ops.object.select_all(action="DESELECT")
    for part in parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    mesh = join_selected(name)
    arm_data = bpy.data.armatures.new(name + "_Rig")
    armature = bpy.data.objects.new(name + "_Rig", arm_data)
    bpy.context.collection.objects.link(armature)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode="EDIT")
    root = add_bone(armature, "Root", (0, 0, 0), (0, 0, height * 0.1), None)
    pelvis = add_bone(armature, "Pelvis", (0, 0, hip), (0, 0, hip + height * 0.08), root)
    chest_bone = add_bone(armature, "Chest", (0, 0, chest), (0, 0, neck), pelvis)
    add_bone(armature, "Head", (0, 0, neck), (0, 0, height), chest_bone)
    for side, x in (("L", -1), ("R", 1)):
        thigh = add_bone(armature, f"UpperLeg.{side}", (x * hip_x, 0, hip), (x * hip_x, 0, hip * 0.45), pelvis)
        add_bone(armature, f"LowerLeg.{side}", (x * hip_x, 0, hip * 0.45), (x * hip_x, 0, 0.02), thigh)
        upper = add_bone(armature, f"UpperArm.{side}", (x * arm_x * 0.7, 0, chest), (x * arm_x, 0, chest - height * 0.16), chest_bone)
        add_bone(armature, f"LowerArm.{side}", (x * arm_x, 0, chest - height * 0.16), (x * arm_x, 0, chest - height * 0.32), upper)
    bpy.ops.object.mode_set(mode="OBJECT")
    finish_walk(armature, mesh)
    walk_legs(
        armature,
        [("UpperLeg.L", 1), ("UpperLeg.R", -1)],
        0.6,
        0.7,
    )
    arm_axis, arm_sign = discover_axis(armature, "UpperArm.L", Vector((0, 1, 0)))
    for frame in range(1, WALK_FRAMES + 2, 4):
        phase = math.cos((frame - 1) / WALK_FRAMES * math.tau)
        for side, sign in (("L", 1), ("R", -1)):
            key_euler(armature.pose.bones[f"UpperArm.{side}"], arm_axis, arm_sign * -0.4 * phase * sign, frame)
    bpy.ops.object.mode_set(mode="OBJECT")
    export_fbx([mesh, armature], f"{name}.fbx", True)


def quadruped(name, shoulder, length, horn):
    hip = shoulder * 0.55
    parts = [
        box("Body", -length * 0.5, -shoulder * 0.22, hip, length * 0.5, shoulder * 0.22, shoulder),
        box("Head", length * 0.35, -shoulder * 0.16, shoulder * 0.72, length * 0.72, shoulder * 0.16, shoulder * 1.05),
    ]
    if horn:
        parts.append(box("HornL", length * 0.5, -shoulder * 0.2, shoulder, length * 0.62, -shoulder * 0.12, shoulder * 1.25))
        parts.append(box("HornR", length * 0.5, shoulder * 0.12, shoulder, length * 0.62, shoulder * 0.2, shoulder * 1.25))
    xs = (-length * 0.28, length * 0.28)
    ys = (-shoulder * 0.18, shoulder * 0.18)
    for ix, x in enumerate(xs):
        for iy, y in enumerate(ys):
            parts.append(box(f"Leg{ix}{iy}", x - 0.25, y - 0.25, 0, x + 0.25, y + 0.25, hip))
    bpy.ops.object.select_all(action="DESELECT")
    for part in parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    mesh = join_selected(name)
    arm_data = bpy.data.armatures.new(name + "_Rig")
    armature = bpy.data.objects.new(name + "_Rig", arm_data)
    bpy.context.collection.objects.link(armature)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode="EDIT")
    root = add_bone(armature, "Root", (0, 0, 0), (0, 0, 0.4), None)
    spine = add_bone(armature, "Spine", (0, 0, hip), (length * 0.2, 0, shoulder * 0.85), root)
    add_bone(armature, "Head", (length * 0.45, 0, shoulder * 0.9), (length * 0.7, 0, shoulder), spine)
    pairs = []
    for label, x, side in (
        ("FL", length * 0.28, 1),
        ("FR", length * 0.28, -1),
        ("BL", -length * 0.28, -1),
        ("BR", -length * 0.28, 1),
    ):
        y = shoulder * 0.18 * (1 if "R" in label else -1)
        thigh = add_bone(armature, f"UpperLeg.{label}", (x, y, hip), (x, y, hip * 0.45), spine)
        add_bone(armature, f"LowerLeg.{label}", (x, y, hip * 0.45), (x, y, 0.05), thigh)
        pairs.append((f"UpperLeg.{label}", side))
    bpy.ops.object.mode_set(mode="OBJECT")
    finish_walk(armature, mesh)
    walk_legs(armature, pairs, 0.45, 0.5)
    bpy.ops.object.mode_set(mode="OBJECT")
    export_fbx([mesh, armature], f"{name}.fbx", True)


def build():
    if os.path.exists(LOG):
        os.remove(LOG)
    os.makedirs(OUT, exist_ok=True)
    log(f"mixar {bpy.app.version_string}")
    clear_scene()
    bpy.context.scene.render.fps = 30
    build_island()
    build_cottage()
    build_pine(5, "SM_Size_Pine_S.fbx")
    build_pine(7, "SM_Size_Pine_M.fbx")
    build_pine(9, "SM_Size_Pine_L.fbx")
    build_static("SM_Size_Lupine", cone("SM_Size_Lupine", 1, 3))
    build_static("SM_Size_Rock", box("SM_Size_Rock", -1, -1, 0, 1, 1, 2))
    build_static("SM_Size_Path", box("SM_Size_Path", -1, -1, 0, 1, 1, 1))
    build_static("SM_Size_Fence", box("SM_Size_Fence", 0, 0, 0, 2, 1, 1))
    build_static("SM_Size_HerbBed", box("SM_Size_HerbBed", 0, 0, 0, 2, 1, 1))
    build_static("SM_Size_Moss", box("SM_Size_Moss", 0, 0, 0, 1, 1, 1))
    build_static("SM_Size_Crystal", cone("SM_Size_Crystal", 1, 1))
    build_static("SM_Size_Bed", box("SM_Size_Bed", 0, 0, 0, 2, 1, 1))
    build_static("SM_Size_Kettle", box("SM_Size_Kettle", 0, 0, 0, 1, 1, 1))
    build_static("SM_Size_Stump", box("SM_Size_Stump", 0, 0, 0, 1, 1, 1))
    build_static("SM_Size_Perch", box("SM_Size_Perch", -2, -2, 0, 2, 2, 1))
    build_static("SM_Size_Shrine", box("SM_Size_Shrine", -1, -1, 0, 1, 1, 4))
    build_static("SM_Size_Field", box("SM_Size_Field", -100, -100, -1, 100, 100, 0))
    build_static("SM_Size_Herb", cone("SM_Size_Herb", 1, 1))
    build_static("SM_Size_Wood", box("SM_Size_Wood", 0, 0, 0, 2, 1, 1))
    build_static("SM_Size_Berry", box("SM_Size_Berry", 0, 0, 0, 1, 1, 1))
    build_static("SM_Size_Fire", cone("SM_Size_Fire", 1, 1))
    build_static("SM_Size_Post", box("SM_Size_Post", -1, -1, 0, 1, 1, 2))
    build_static("SM_Size_Cloud", box("SM_Size_Cloud", -10, -4, -1, 10, 4, 1))
    build_static("SM_Size_Wisp", box("SM_Size_Wisp", -1, -1, 0, 1, 1, 1))
    biped("SK_Size_Partner", 2)
    biped("SK_Size_Child", 1)
    biped("SK_Size_Guard", 2)
    quadruped("SK_Size_Bear", 5, 6, False)
    quadruped("SK_Size_Bull", 5, 6, True)
    log("size test set complete")


if __name__ == "__main__":
    if os.environ.get("HOMEWORLD_SIZE_ONLY") == "cottage":
        if os.path.exists(LOG):
            os.remove(LOG)
        os.makedirs(OUT, exist_ok=True)
        clear_scene()
        build_cottage()
        log("cottage block complete")
    else:
        build()

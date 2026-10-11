"""Fit a skeleton to the stood Tripo player and store Idle and Walk.

Run:
  "C:\\Program Files\\Mixar\\mixar.exe" --background --python Tools/Rig-TripoPlayer.py
"""

import math
import os
import traceback

import bpy
from mathutils import Vector

OBJ = r"C:\dev\TripoSR\output\player\0\mesh_greybox.obj"
BLEND = r"C:\dev\TripoSR\output\player\0\SM_Player_Rig.blend"
LOG = r"C:\dev\TripoSR\output\player\0\rig_log.txt"
WALK_FRAMES = 32


def log(message):
    print(message)
    with open(LOG, "a", encoding="utf-8") as handle:
        handle.write(message + "\n")


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def activate(obj):
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def percentile(values, fraction):
    ordered = sorted(values)
    if not ordered:
        return 0.0
    position = (len(ordered) - 1) * fraction
    index = int(position)
    blend = position - index
    if index + 1 < len(ordered):
        return ordered[index] * (1.0 - blend) + ordered[index + 1] * blend
    return ordered[index]


def import_mesh():
    before = set(bpy.data.objects)
    try:
        bpy.ops.wm.obj_import(filepath=OBJ, up_axis="Z", forward_axis="Y")
    except TypeError:
        bpy.ops.wm.obj_import(filepath=OBJ)
    created = [obj for obj in bpy.data.objects if obj not in before and obj.type == "MESH"]
    if not created:
        raise RuntimeError("OBJ import created no mesh.")
    mesh = created[0]
    mesh.name = "SM_Player_Tripo"
    activate(mesh)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return mesh


def stand_on_feet(mesh):
    coords = [vertex.co.copy() for vertex in mesh.data.vertices]
    spans = []
    for axis in range(3):
        column = [coord[axis] for coord in coords]
        spans.append(max(column) - min(column))
    height_axis = max(range(3), key=lambda axis: spans[axis])
    if height_axis != 2:
        # Longest axis becomes Z. The other two stay in order.
        order = [axis for axis in range(3) if axis != height_axis] + [height_axis]
        for vertex in mesh.data.vertices:
            source = vertex.co.copy()
            vertex.co = Vector((source[order[0]], source[order[1]], source[order[2]]))
        coords = [vertex.co.copy() for vertex in mesh.data.vertices]

    low = percentile([coord.z for coord in coords], 0.1)
    high = percentile([coord.z for coord in coords], 0.9)

    def spread(sample):
        if not sample:
            return 0.0
        center_x = sum(coord.x for coord in sample) / len(sample)
        center_y = sum(coord.y for coord in sample) / len(sample)
        return sum(math.hypot(coord.x - center_x, coord.y - center_y) for coord in sample) / len(sample)

    low_sample = [coord for coord in coords if coord.z <= low]
    high_sample = [coord for coord in coords if coord.z >= high]
    if spread(high_sample) > spread(low_sample):
        for vertex in mesh.data.vertices:
            vertex.co.z *= -1.0

    zs = [vertex.co.z for vertex in mesh.data.vertices]
    floor = min(zs)
    center_x = (min(vertex.co.x for vertex in mesh.data.vertices) + max(vertex.co.x for vertex in mesh.data.vertices)) * 0.5
    center_y = (min(vertex.co.y for vertex in mesh.data.vertices) + max(vertex.co.y for vertex in mesh.data.vertices)) * 0.5
    for vertex in mesh.data.vertices:
        vertex.co.x -= center_x
        vertex.co.y -= center_y
        vertex.co.z -= floor
    mesh.data.update()
    height = max(vertex.co.z for vertex in mesh.data.vertices)
    log(f"stood height {height:.3f} m")
    return height


def add_bone(armature, name, head, tail, parent, deform):
    bone = armature.data.edit_bones.new(name)
    bone.head = head
    bone.tail = tail
    bone.use_connect = False
    bone.use_deform = deform
    bone.envelope_distance = 0.16
    bone.head_radius = 0.07
    bone.tail_radius = 0.05
    if parent is not None:
        bone.parent = parent
    return bone


def build_armature(mesh, height):
    coords = [vertex.co.copy() for vertex in mesh.data.vertices]
    hip_z = height * 0.52
    knee_z = height * 0.28
    ankle_z = height * 0.05
    chest_z = height * 0.74
    neck_z = height * 0.84
    lower = [coord for coord in coords if ankle_z < coord.z < hip_z] or coords
    upper = [coord for coord in coords if chest_z - 0.05 < coord.z < neck_z] or coords
    left_hip = min(percentile([coord.x for coord in lower], 0.22), -0.08)
    right_hip = max(percentile([coord.x for coord in lower], 0.78), 0.08)
    left_arm = min(percentile([coord.x for coord in upper], 0.08), -0.2)
    right_arm = max(percentile([coord.x for coord in upper], 0.92), 0.2)

    armature_data = bpy.data.armatures.new("PlayerRig")
    armature = bpy.data.objects.new("PlayerRig", armature_data)
    bpy.context.collection.objects.link(armature)
    activate(armature)
    bpy.ops.object.mode_set(mode="EDIT")

    root = add_bone(armature, "Root", (0.0, 0.0, 0.0), (0.0, 0.0, 0.12), None, False)
    pelvis = add_bone(armature, "Pelvis", (0.0, 0.0, hip_z), (0.0, 0.0, hip_z + 0.08), root, True)
    spine = add_bone(armature, "Spine", (0.0, 0.0, hip_z + 0.08), (0.0, 0.0, chest_z), pelvis, True)
    chest = add_bone(armature, "Chest", (0.0, 0.0, chest_z), (0.0, 0.0, neck_z), spine, True)
    add_bone(armature, "Head", (0.0, 0.0, neck_z), (0.0, 0.0, height * 0.98), chest, True)

    for side, hip_x, arm_x in (("L", left_hip, left_arm), ("R", right_hip, right_arm)):
        thigh = add_bone(
            armature,
            f"UpperLeg.{side}",
            (hip_x, 0.0, hip_z),
            (hip_x, 0.0, knee_z),
            pelvis,
            True,
        )
        shin = add_bone(
            armature,
            f"LowerLeg.{side}",
            (hip_x, 0.0, knee_z),
            (hip_x, 0.02, ankle_z),
            thigh,
            True,
        )
        add_bone(
            armature,
            f"Foot.{side}",
            (hip_x, 0.02, ankle_z),
            (hip_x, 0.12, 0.02),
            shin,
            True,
        )
        upper = add_bone(
            armature,
            f"UpperArm.{side}",
            (arm_x * 0.45, 0.0, chest_z),
            (arm_x * 0.85, 0.0, chest_z - 0.16),
            chest,
            True,
        )
        add_bone(
            armature,
            f"LowerArm.{side}",
            (arm_x * 0.85, 0.0, chest_z - 0.16),
            (arm_x, 0.02, chest_z - 0.38),
            upper,
            True,
        )

    bpy.ops.object.mode_set(mode="OBJECT")
    armature.show_in_front = True
    armature.data.display_type = "OCTAHEDRAL"
    log(f"bones {len(armature.data.bones)}")
    return armature


def parent_with_weights(mesh, armature):
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    mesh.select_set(True)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    try:
        bpy.ops.object.parent_set(type="ARMATURE_AUTO")
        weighted = any(vertex.groups for vertex in mesh.data.vertices)
        if not weighted:
            raise RuntimeError("Automatic weights wrote no groups.")
        log("weights automatic")
    except RuntimeError as exc:
        log(f"automatic weights failed: {exc}")
        bpy.ops.object.parent_set(type="ARMATURE_ENVELOPE")
        log("weights envelope")


def bind_action(armature, name):
    action = bpy.data.actions.new(name)
    anim = armature.animation_data or armature.animation_data_create()
    anim.action = action
    slot = None
    if hasattr(action, "slots"):
        try:
            slot = action.slots.new(id_type="OBJECT", name=armature.name)
        except TypeError:
            slot = action.slots.new("OBJECT", armature.name)
        if hasattr(anim, "action_slot"):
            anim.action_slot = slot
    return action, slot


def fcurve_count(action):
    count = 0
    if hasattr(action, "layers"):
        for layer in action.layers:
            for strip in layer.strips:
                bags = getattr(strip, "channelbags", [])
                count += sum(len(bag.fcurves) for bag in bags)
    if count == 0 and hasattr(action, "fcurves"):
        count = len(action.fcurves)
    return count


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
    log(f"swing {bone_name} axis {best[1]} sign {best[2]:+.0f} score {best[0]:.3f}")
    return best[1], best[2]


def key_euler(pose_bone, axis, value, frame):
    euler = [0.0, 0.0, 0.0]
    euler[axis] = value
    pose_bone.rotation_euler = euler
    pose_bone.keyframe_insert(data_path="rotation_euler", frame=frame)


def key_cycle(armature, bones):
    forward = Vector((0.0, 1.0, 0.0))
    backward = Vector((0.0, -1.0, 0.0))
    leg_axis, leg_sign = discover_axis(armature, "UpperLeg.L", forward)
    knee_axis, knee_sign = discover_axis(armature, "LowerLeg.L", backward)
    arm_axis, arm_sign = discover_axis(armature, "UpperArm.L", forward)
    frames = list(range(1, WALK_FRAMES + 2, 4))
    for frame in frames:
        phase = math.cos((frame - 1) / WALK_FRAMES * math.tau)
        back = max(0.0, -phase)
        for side, side_sign in (("L", 1.0), ("R", -1.0)):
            swing = phase * side_sign
            key_euler(
                armature.pose.bones[f"UpperLeg.{side}"],
                leg_axis,
                leg_sign * 0.55 * swing,
                frame,
            )
            key_euler(
                armature.pose.bones[f"LowerLeg.{side}"],
                knee_axis,
                knee_sign * (0.2 + 0.75 * max(0.0, -swing)),
                frame,
            )
            key_euler(
                armature.pose.bones[f"Foot.{side}"],
                leg_axis,
                leg_sign * 0.25 * swing,
                frame,
            )
            key_euler(
                armature.pose.bones[f"UpperArm.{side}"],
                arm_axis,
                arm_sign * -0.4 * swing,
                frame,
            )
            key_euler(
                armature.pose.bones[f"LowerArm.{side}"],
                arm_axis,
                arm_sign * -0.15 * swing,
                frame,
            )
        key_euler(armature.pose.bones["Chest"], leg_axis, leg_sign * 0.04 * phase, frame)
        key_euler(armature.pose.bones["Pelvis"], 2, 0.06 * phase, frame)
    return bones


def smooth_action(action):
    curves = []
    if hasattr(action, "layers"):
        for layer in action.layers:
            for strip in layer.strips:
                for bag in getattr(strip, "channelbags", []):
                    curves.extend(bag.fcurves)
    if not curves and hasattr(action, "fcurves"):
        curves.extend(action.fcurves)
    for curve in curves:
        for point in curve.keyframe_points:
            point.interpolation = "BEZIER"
            point.handle_left_type = "AUTO_CLAMPED"
            point.handle_right_type = "AUTO_CLAMPED"


def build():
    os.makedirs(os.path.dirname(BLEND), exist_ok=True)
    if os.path.exists(LOG):
        os.remove(LOG)
    log(f"mixar {bpy.app.version_string}")
    clear_scene()
    mesh = import_mesh()
    height = stand_on_feet(mesh)
    clay = bpy.data.materials.new("Clay")
    clay.diffuse_color = (0.45, 0.42, 0.38, 1.0)
    mesh.data.materials.append(clay)

    armature = build_armature(mesh, height)
    parent_with_weights(mesh, armature)
    activate(armature)
    bpy.ops.object.mode_set(mode="POSE")
    for pose_bone in armature.pose.bones:
        pose_bone.rotation_mode = "XYZ"

    scene = bpy.context.scene
    scene.render.fps = 30
    scene.frame_start = 1
    scene.frame_end = WALK_FRAMES

    idle, _slot = bind_action(armature, "Idle")
    for frame, sway in ((1, 0.0), (16, 0.04), (32, 0.0), (48, -0.04), (64, 0.0)):
        key_euler(armature.pose.bones["Chest"], 0, sway, frame)
        key_euler(armature.pose.bones["UpperArm.L"], 0, sway, frame)
        key_euler(armature.pose.bones["UpperArm.R"], 0, -sway, frame)
    if fcurve_count(idle) == 0:
        raise RuntimeError("Idle action received no keys.")
    smooth_action(idle)

    walk, _slot = bind_action(armature, "Walk")
    key_cycle(armature, armature.pose.bones)
    if fcurve_count(walk) == 0:
        raise RuntimeError("Walk action received no keys.")
    smooth_action(walk)

    scene.frame_set(1)
    bpy.context.view_layer.update()
    left = armature.pose.bones["UpperLeg.L"].tail.y
    scene.frame_set(int(WALK_FRAMES / 2) + 1)
    bpy.context.view_layer.update()
    left_back = armature.pose.bones["UpperLeg.L"].tail.y
    log(f"left leg tail Y frame1 {left:.3f} frame17 {left_back:.3f}")
    scene.frame_set(1)
    bpy.ops.object.mode_set(mode="OBJECT")
    armature.select_set(True)
    mesh.select_set(True)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    log(f"wrote {BLEND}")


if __name__ == "__main__":
    try:
        build()
    except Exception:
        log(traceback.format_exc())
        raise

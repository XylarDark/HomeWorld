# place_vs_mvp_markers.py
# Docs/05 first-pass: TargetPoints + cameras from MVP_CRUMB_SPLINE.json + NightMix MPC stub.
# Run in Unreal Editor (Execute Python Script) or -ExecutePythonScript=

from __future__ import annotations

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("place_vs_mvp_markers: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "place_vs_mvp_markers:"
JSON_REL = os.path.join("AssetCreation", "Exports", "MVP_CRUMB_SPLINE.json")
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
MPC_PATH = "/Game/HomeWorld/Materials/MPC_HomeWorld_Time"
MPC_NAME = "MPC_HomeWorld_Time"


def _log(msg):
    unreal.log(PREFIX + " " + str(msg))
    print(PREFIX, msg)


def _project_root():
    cwd = os.getcwd()
    if os.path.isdir(cwd) and "Content" in (os.listdir(cwd) or []):
        return cwd
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", ".."))


def blender_to_ue_cm(loc):
    """Blender meters Z-up -> UE centimeters. Flip Y (common Blender->UE)."""
    x, y, z = float(loc[0]), float(loc[1]), float(loc[2])
    return unreal.Vector(x * 100.0, -y * 100.0, z * 100.0)


def blender_euler_to_ue_rot(eulers):
    """Blender XYZ radians -> UE rotator degrees (best-effort; cameras may need polish)."""
    import math
    rx, ry, rz = eulers
    # Approximate: pitch/yaw/roll mapping with Y flip
    pitch = math.degrees(rx)
    yaw = math.degrees(-rz)
    roll = math.degrees(ry)
    return unreal.Rotator(pitch, yaw, roll)


def ensure_folder(content_path):
    if not unreal.EditorAssetLibrary.does_directory_exist(content_path):
        unreal.EditorAssetLibrary.make_directory(content_path)
        _log("Created folder %s" % content_path)


def destroy_existing_named(world, names):
    """Remove previously spawned markers with same labels if re-running."""
    name_set = set(names)
    to_destroy = []
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        try:
            label = actor.get_actor_label()
        except Exception:
            continue
        if label in name_set:
            to_destroy.append(actor)
    for actor in to_destroy:
        unreal.EditorLevelLibrary.destroy_actor(actor)
    if to_destroy:
        _log("Removed %d existing marker actors" % len(to_destroy))


def spawn_target_point(name, location, rotation=None):
    cls = unreal.TargetPoint
    loc = blender_to_ue_cm(location)
    rot = blender_euler_to_ue_rot(rotation) if rotation else unreal.Rotator(0, 0, 0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(cls, loc, rot)
    if actor:
        actor.set_actor_label(name)
        actor.set_folder_path("VS_MVP/Markers")
    return actor


def spawn_camera(name, location, rotation):
    cls = unreal.CameraActor
    loc = blender_to_ue_cm(location)
    rot = blender_euler_to_ue_rot(rotation)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(cls, loc, rot)
    if actor:
        actor.set_actor_label(name)
        actor.set_folder_path("VS_MVP/Cameras")
    return actor


def create_or_load_level():
    ensure_folder("/Game/HomeWorld/Maps")
    ensure_folder("/Game/HomeWorld/Maps/VS_MVP")
    ensure_folder("/Game/HomeWorld/Maps/VS_MVP/Transit")
    ensure_folder("/Game/HomeWorld/Maps/VS_MVP/Cameras")
    ensure_folder("/Game/HomeWorld/Maps/VS_MVP/Markers")
    if unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        ok = unreal.EditorLevelLibrary.load_level(LEVEL_PATH)
        _log("Loaded existing level %s ok=%s" % (LEVEL_PATH, ok))
    else:
        # new_level path without asset extension
        ok = unreal.EditorLevelLibrary.new_level(LEVEL_PATH)
        _log("Created new level %s ok=%s" % (LEVEL_PATH, ok))
    return True


def create_nightmix_mpc():
    ensure_folder("/Game/HomeWorld/Materials")
    if unreal.EditorAssetLibrary.does_asset_exist(MPC_PATH):
        mpc = unreal.EditorAssetLibrary.load_asset(MPC_PATH)
        _log("NightMix MPC already exists: %s" % MPC_PATH)
        return mpc

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.MaterialParameterCollectionFactoryNew()
    mpc = asset_tools.create_asset(
        MPC_NAME,
        "/Game/HomeWorld/Materials",
        unreal.MaterialParameterCollection,
        factory,
    )
    if not mpc:
        _log("Failed to create MPC_HomeWorld_Time")
        return None

    # Add scalar NightMix via EditorProperty if available
    try:
        scalars = unreal.Array(unreal.CollectionScalarParameter)
        param = unreal.CollectionScalarParameter()
        param.set_editor_property("parameter_name", "NightMix")
        param.set_editor_property("default_value", 0.85)
        scalars.append(param)
        mpc.set_editor_property("scalar_parameters", scalars)
        unreal.EditorAssetLibrary.save_asset(MPC_PATH)
        _log("Created MPC with NightMix default 0.85 (homestead night target)")
    except Exception as exc:
        unreal.EditorAssetLibrary.save_asset(MPC_PATH)
        _log("Created MPC shell; set NightMix scalar in editor if missing (%s)" % exc)
    return mpc


def main():
    root = _project_root()
    json_path = os.path.join(root, JSON_REL)
    if not os.path.isfile(json_path):
        _log("JSON not found: %s" % json_path)
        return 1

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    create_or_load_level()
    create_nightmix_mpc()

    names = []
    for item in data.get("CRUMB", []):
        names.append(item["name"])
    for item in data.get("VS_MARKER", []):
        names.append(item["name"])
    for item in data.get("CAM", []):
        names.append(item["name"])
    for name in (data.get("anchors") or {}).keys():
        names.append("ANCHOR_" + name)

    destroy_existing_named(None, names)

    spawned = 0
    for item in data.get("CRUMB", []):
        if spawn_target_point(item["name"], item["location"], item.get("rotation_euler_xyz")):
            spawned += 1
            _log("CRUMB %s @ %s" % (item["name"], item["location"]))

    for item in data.get("VS_MARKER", []):
        if spawn_target_point(item["name"], item["location"], item.get("rotation_euler_xyz")):
            spawned += 1
            _log("MARKER %s @ %s" % (item["name"], item["location"]))

    for name, item in (data.get("anchors") or {}).items():
        loc = item.get("location") if isinstance(item, dict) else None
        if not loc:
            continue
        label = "ANCHOR_" + name
        if spawn_target_point(label, loc, item.get("rotation_euler_xyz") if isinstance(item, dict) else None):
            spawned += 1
            _log("ANCHOR %s @ %s" % (label, loc))

    for item in data.get("CAM", []):
        if spawn_camera(item["name"], item["location"], item.get("rotation_euler_xyz") or [0, 0, 0]):
            spawned += 1
            _log("CAM %s @ %s" % (item["name"], item["location"]))

    order = data.get("CRUMB_order_suggested") or []
    _log("CRUMB_order_suggested: %s" % " -> ".join(order))
    _log("FALLBACK: scripted glide along CRUMB_* only; portal SM_Shrine_Homestead <-> SM_Shrine_Return")

    # Save current level
    try:
        unreal.EditorLevelLibrary.save_current_level()
        _log("Saved current level")
    except Exception as exc:
        _log("Save level warning: %s" % exc)

    _log("Done. Spawned %d actors. NightMix MPC: %s" % (spawned, MPC_PATH))
    return 0


if __name__ == "__main__":
    code = main()
    # Do not sys.exit hard — keep editor open for Lead
    if code != 0:
        unreal.log_error(PREFIX + " finished with code %s" % code)

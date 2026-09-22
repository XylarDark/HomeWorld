"""Harness P3 exempt: PL-D preview homestead spike — not canonical shotlist prove."""
import unreal, json, os, time

OUT_DIR = os.path.join(unreal.SystemLibrary.get_project_directory(), "Maps", "Preview_Homestead_Night")
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PNG = os.path.join(OUT_DIR, "shot1_lookout_ue_pl_d.png")
META = os.path.join(unreal.SystemLibrary.get_project_directory(), "Saved", "PL_D_shot1.json")

def find_cam(label):
    for a in unreal.EditorLevelLibrary.get_all_level_actors():
        try:
            if a.get_actor_label() == label:
                return a
        except Exception:
            continue
    return None

cam = find_cam("CAM_Hero")
marker = find_cam("VS_MARKER_Shot1_Lookout")
result = {"cam_hero": bool(cam), "marker": bool(marker), "path": OUT_PNG}

if cam:
    loc = cam.get_actor_location()
    rot = cam.get_actor_rotation()
    result["cam_loc"] = [loc.x, loc.y, loc.z]
    result["cam_rot"] = [rot.pitch, rot.yaw, rot.roll]
    # Set viewport to camera
    try:
        unreal.EditorLevelLibrary.set_level_viewport_camera_info(loc, rot)
        result["viewport_set"] = True
    except Exception as e:
        result["viewport_set"] = False
        result["viewport_err"] = str(e)
    # Prefer piloting camera actor if available
    try:
        unreal.EditorLevelLibrary.pilot_level_actor(cam)
        result["pilot"] = True
    except Exception as e:
        result["pilot"] = False
        result["pilot_err"] = str(e)

# High-res screenshot via AutomationLibrary if present
ok = False
try:
    # take_high_res_screenshot(ResolutionX, ResolutionY, Filename, Camera=None, ...)
    unreal.AutomationLibrary.take_high_res_screenshot(1600, 900, OUT_PNG, cam if cam else None)
    ok = True
    result["method"] = "AutomationLibrary.take_high_res_screenshot"
except Exception as e:
    result["auto_err"] = str(e)
    try:
        unreal.SystemLibrary.execute_console_command(
            unreal.EditorLevelLibrary.get_editor_world(),
            'HighResShot 1600x900 filename="' + OUT_PNG.replace("\\", "/") + '"'
        )
        ok = True
        result["method"] = "HighResShot console"
    except Exception as e2:
        result["console_err"] = str(e2)

# Fallback: EditorUtilityLibrary or Screenshot
if not ok:
    try:
        # delayed - write path for HighResShot relative to project
        rel = "Maps/Preview_Homestead_Night/shot1_lookout_ue_pl_d.png"
        unreal.SystemLibrary.execute_console_command(
            unreal.EditorLevelLibrary.get_editor_world(),
            "HighResShot 1600x900 filename=\"" + rel + "\""
        )
        result["method"] = "HighResShot relative"
        ok = True
    except Exception as e3:
        result["fallback_err"] = str(e3)

result["ok"] = ok
result["exists_after"] = os.path.isfile(OUT_PNG)
with open(META, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))

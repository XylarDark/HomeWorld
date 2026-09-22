"""Harness P3 exempt: PL-D one-off CAM_Hero spike — not canonical shotlist prove."""
import unreal, time, os, json
cam = None
for a in unreal.EditorLevelLibrary.get_all_level_actors():
    try:
        if a.get_actor_label() == "CAM_Hero":
            cam = a
            break
    except Exception:
        pass
if cam:
    unreal.EditorLevelLibrary.set_level_viewport_camera_info(cam.get_actor_location(), cam.get_actor_rotation())
    try:
        unreal.EditorLevelLibrary.pilot_level_actor(cam)
    except Exception:
        pass
# import capture_viewport helpers inline
proj = unreal.Paths.project_dir()
out_dir = os.path.join(proj, "Saved", "Screenshots")
os.makedirs(out_dir, exist_ok=True)
filename = "pl_d_shot1_cam_hero.png"
filepath = os.path.join(out_dir, filename)
try:
    unreal.AutomationLibrary.take_high_res_screenshot(1600, 900, filename)
except Exception as e:
    unreal.SystemLibrary.execute_console_command(None, 'HighResShot 1600x900 filename="%s"' % filepath.replace("\\","/"))
meta = {"requested": filepath, "cam": "CAM_Hero"}
open(os.path.join(proj, "Saved", "PL_D_shot1_capture2.json"), "w").write(json.dumps(meta, indent=2))
print("requested", filepath)

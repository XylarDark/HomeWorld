import unreal
import os
import math

def logf(m):
    path = os.path.join(unreal.Paths.project_saved_dir(), "vp2_b_probe.txt")
    with open(path, "a", encoding="utf-8") as f:
        f.write(m + "\n")
    unreal.log(m)

w = unreal.EditorLevelLibrary.get_pie_worlds(include_dedicated_server=False)[0]
pc = unreal.GameplayStatics.get_player_controller(w, 0)
p = pc.get_controlled_pawn()
store = None
for a in unreal.GameplayStatics.get_all_actors_of_class(w, unreal.Actor):
    try:
        if a.get_actor_label() == "GP_Store_STONE":
            store = a
            break
    except Exception:
        pass
pl = p.get_actor_location()
sl = store.get_actor_location()
d = math.sqrt((pl.x - sl.x) ** 2 + (pl.y - sl.y) ** 2 + (pl.z - sl.z) ** 2)
spirit = False
try:
    spirit = bool(p.is_spirit_form())
except Exception as e:
    spirit = "err:%s" % e
logf("pawn=%s store=%s dist=%.1f spirit=%s" % (pl, sl, d, spirit))
new = unreal.Vector(sl.x - 100.0, sl.y, sl.z + 30.0)
p.set_actor_location(new, False, True)
yaw = math.degrees(math.atan2(sl.y - new.y, sl.x - new.x))
p.set_actor_rotation(unreal.Rotator(0.0, yaw, 0.0), True)
# also set control rotation so line trace uses GetControlRotation
pc.set_control_rotation(unreal.Rotator(0.0, yaw, 0.0))
logf("after tele pawn=%s yaw=%.1f ctrl=%s" % (p.get_actor_location(), yaw, pc.get_control_rotation()))
unreal.SystemLibrary.execute_console_command(w, "hw.TimeOfDay.SetPhase 0", None)
unreal.SystemLibrary.execute_console_command(w, "hw.Gather.Ore 2", None)
r = p.try_store_transfer_in_front()
logf("try_store -> %s" % r)

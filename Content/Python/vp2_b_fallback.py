import unreal, os, math
def logf(m):
    open(os.path.join(unreal.Paths.project_saved_dir(),"vp2_b_probe.txt"),"a",encoding="utf-8").write(m+"\n"); unreal.log(m)
w = unreal.EditorLevelLibrary.get_pie_worlds(include_dedicated_server=False)[0]
pc = unreal.GameplayStatics.get_player_controller(w, 0)
p = pc.get_controlled_pawn()
unreal.SystemLibrary.execute_console_command(w, "hw.TimeOfDay.SetPhase 0", None)
target=None
for lab in ("GP_GlideStart","CRUMB_Depart_Lookout"):
    for a in unreal.GameplayStatics.get_all_actors_of_class(w, unreal.Actor):
        try:
            if a.get_actor_label()==lab: target=a; break
        except: pass
    if target: break
logf("glide target=%s" % target)
if target:
    sl=target.get_actor_location()
    new=unreal.Vector(sl.x-80.0, sl.y, sl.z+30.0)
    p.set_actor_location(new, False, True)
    yaw=math.degrees(math.atan2(sl.y-new.y, sl.x-new.x))
    rot=unreal.Rotator(0.0,yaw,0.0)
    p.set_actor_rotation(rot, True); pc.set_control_rotation(rot)
    r=p.try_start_fallback_glide()
    logf("fallback -> %s" % r)

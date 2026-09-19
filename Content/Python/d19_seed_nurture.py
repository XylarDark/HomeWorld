import unreal, os, math
def logf(m):
    open(os.path.join(unreal.Paths.project_saved_dir(),"d19_probe.txt"),"a",encoding="utf-8").write(m+"\n"); unreal.log(m)
w=unreal.EditorLevelLibrary.get_pie_worlds(include_dedicated_server=False)[0]
pc=unreal.GameplayStatics.get_player_controller(w,0); p=pc.get_controlled_pawn()
def find(lab):
  for a in unreal.GameplayStatics.get_all_actors_of_class(w, unreal.Actor):
    try:
      if a.get_actor_label()==lab: return a
    except: pass
  return None
def aim(t,dist=100.0):
  sl=t.get_actor_location(); new=unreal.Vector(sl.x-dist,sl.y,sl.z+30.0)
  p.set_actor_location(new,False,True)
  yaw=math.degrees(math.atan2(sl.y-new.y,sl.x-new.x)); rot=unreal.Rotator(0.0,yaw,0.0)
  p.set_actor_rotation(rot,True); pc.set_control_rotation(rot)
unreal.SystemLibrary.execute_console_command(w,"log LogTemp Log",None)
unreal.SystemLibrary.execute_console_command(w,"hw.Gather.Seed 2",None)
unreal.SystemLibrary.execute_console_command(w,"hw.TimeOfDay.SetPhase 2",None)
n1=find("GP_N1_Crop"); logf("n1=%s"%n1)
if n1:
  aim(n1); r=p.try_nurture_in_front(); logf("nurture->%s"%r)
unreal.SystemLibrary.execute_console_command(w,"hw.Inventory.Dump",None)
unreal.SystemLibrary.execute_console_command(w,"hw.TimeOfDay.SetPhase 3",None)
logf("done")

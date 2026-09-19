import unreal, os, math, time
p=r"C:\dev\HomeWorld\Saved\d19_probe.txt"
open(p,"w").close()
def w(m):
  open(p,"a",encoding="utf-8").write(str(m)+"\n"); unreal.log(str(m))
world=None
for i in range(30):
  worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
  if worlds:
    world=worlds[0]
    break
  time.sleep(0.5)
w("world="+str(world is not None))
pc=None; pawn=None
for i in range(40):
  pc=unreal.GameplayStatics.get_player_controller(world,0) if world else None
  pawn=pc.get_controlled_pawn() if pc else None
  if pawn: break
  time.sleep(0.5)
w("pawn="+str(pawn.get_class().get_name() if pawn else None)+" wait_i="+str(i))
if not pawn: raise SystemExit(0)
labels=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor):
  try:
    lab=a.get_actor_label()
    if lab and ("Gather" in lab or "GP_" in lab):
      labels.append(lab)
  except: pass
w("labels="+str(sorted(set(labels))[:40]))
def find(lab):
  for a in unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor):
    try:
      if a.get_actor_label()==lab: return a
    except: pass
  return None
def aim(t,dist=120.0):
  sl=t.get_actor_location(); new=unreal.Vector(sl.x-dist,sl.y,sl.z+40.0)
  pawn.set_actor_location(new,False,True)
  yaw=math.degrees(math.atan2(sl.y-new.y,sl.x-new.x)); rot=unreal.Rotator(0.0,yaw,0.0)
  pawn.set_actor_rotation(rot,True); pc.set_control_rotation(rot)
unreal.SystemLibrary.execute_console_command(world,"log LogTemp Log",None)
unreal.SystemLibrary.execute_console_command(world,"hw.TimeOfDay.SetPhase 0",None)
g=find("GP_Gather_WOOD")
w("wood="+str(g))
if g:
  aim(g); w("harvest="+str(pawn.try_harvest_in_front()))
unreal.SystemLibrary.execute_console_command(world,"hw.Gather.Seed 1",None)
unreal.SystemLibrary.execute_console_command(world,"hw.Inventory.Dump",None)
w("done")

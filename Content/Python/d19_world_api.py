import unreal, os
path=os.path.join(unreal.Paths.project_saved_dir(),"d19_probe.txt")
def w(m):
  with open(path,"a",encoding="utf-8") as f: f.write(m+"\n")
  unreal.log(m)
# try variants
for kwargs in ({}, {"include_dedicated_server":True}, {"include_dedicated_server":False}):
  try:
    worlds = unreal.EditorLevelLibrary.get_pie_worlds(**kwargs) if kwargs else unreal.EditorLevelLibrary.get_pie_worlds()
    w("get_pie_worlds%s -> %s"%(kwargs, len(worlds) if worlds is not None else None))
  except Exception as e:
    w("get_pie_worlds%s ERR %s"%(kwargs,e))
# GameplayStatics
try:
  ew = unreal.EditorLevelLibrary.get_editor_world()
  w("gs pc editor=%s"%unreal.GameplayStatics.get_player_controller(ew,0))
except Exception as e:
  w("gs ed err %s"%e)
# UnrealEditorSubsystem
try:
  ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
  gw = ues.get_game_world()
  w("ues game_world=%s"%gw)
  if gw:
    pc=unreal.GameplayStatics.get_player_controller(gw,0)
    w("ues pc=%s pawn=%s"%(pc, pc.get_controlled_pawn() if pc else None))
except Exception as e:
  w("ues err %s"%e)

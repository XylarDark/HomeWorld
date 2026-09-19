import unreal, time, os
p=r"C:\dev\HomeWorld\Saved\d19_probe.txt"
open(p,"w").close()
def w(m):
  open(p,"a",encoding="utf-8").write(str(m)+"\n"); unreal.log(str(m))
sub=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if sub.is_in_play_in_editor():
  sub.editor_request_end_play()
  time.sleep(4)
w("ended pie="+str(sub.is_in_play_in_editor()))
# kill sticky state: request end again
if sub.is_in_play_in_editor():
  sub.editor_request_end_play()
  time.sleep(2)
sub.editor_request_begin_play()
time.sleep(10)
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
ues=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
gw=ues.get_game_world()
w("pie="+str(sub.is_in_play_in_editor())+" worlds="+str(len(worlds) if worlds else 0)+" gw="+str(gw is not None))
if worlds:
  pc=unreal.GameplayStatics.get_player_controller(worlds[0],0)
  w("pawn="+str(pc.get_controlled_pawn() if pc else None))
elif gw:
  pc=unreal.GameplayStatics.get_player_controller(gw,0)
  w("gw pawn="+str(pc.get_controlled_pawn() if pc else None))

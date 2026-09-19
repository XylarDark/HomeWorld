import unreal
p=r"C:\dev\HomeWorld\Saved\d19_probe.txt"
open(p,"w").close()
def w(m):
  open(p,"a",encoding="utf-8").write(str(m)+"\n")
sub=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
w("in_pie="+str(sub.is_in_play_in_editor()))
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
w("worlds="+str(len(worlds) if worlds else 0))
ues=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
gw=ues.get_game_world()
w("gw="+str(gw))

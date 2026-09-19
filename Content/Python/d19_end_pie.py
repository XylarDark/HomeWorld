import unreal, time
p=r"C:\dev\HomeWorld\Saved\d19_probe.txt"
open(p,"w").write("end\n")
sub=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if sub.is_in_play_in_editor():
  sub.editor_request_end_play()
  time.sleep(5)
open(p,"a").write("pie="+str(sub.is_in_play_in_editor())+"\n")

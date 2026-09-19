import unreal, time
sub=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
unreal.log("before=%s"%sub.is_in_play_in_editor())
if not sub.is_in_play_in_editor():
  sub.editor_request_begin_play()
  time.sleep(12)
unreal.log("after=%s"%sub.is_in_play_in_editor())
open(unreal.Paths.project_saved_dir()+"/d19_probe.txt","a",encoding="utf-8").write("after=%s\n"%sub.is_in_play_in_editor())

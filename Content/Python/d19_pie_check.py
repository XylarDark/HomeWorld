import unreal, os
path=os.path.join(unreal.Paths.project_saved_dir(),"d19_probe.txt")
def w(m):
  open(path,"a",encoding="utf-8").write(m+"\n"); unreal.log(m)
sub=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
w("in_pie=%s"%sub.is_in_play_in_editor())
try:
  worlds=unreal.EditorLevelLibrary.get_pie_worlds(include_dedicated_server=False)
  w("worlds=%s"%len(worlds))
except Exception as e:
  w("get_pie_worlds err %s"%e)
try:
  worlds2=unreal.EditorLevelLibrary.get_editor_world()
  w("editor_world=%s"%worlds2)
except Exception as e:
  w("edworld err %s"%e)

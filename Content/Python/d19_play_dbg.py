import unreal
p=r"C:\dev\HomeWorld\Saved\d19_probe.txt"
open(p,"w").close()
def w(m):
  open(p,"a",encoding="utf-8").write(str(m)+"\n"); unreal.log(str(m))
try:
  ps = unreal.get_editor_subsystem(unreal.PlayLevelSettings)  # may not exist
  w("pls="+str(ps))
except Exception as e:
  w("pls err "+str(e))
# try console play
try:
  unreal.SystemLibrary.execute_console_command(None, "Py print('hi')", None)
except Exception as e:
  w("console "+str(e))
# EditorActorSubsystem?
w("modules ok")
# Force: LevelEditorPlaySettings
try:
  settings = unreal.LevelEditorPlaySettings.get_default_object() if hasattr(unreal,'LevelEditorPlaySettings') else None
  w("settings="+str(settings))
except Exception as e:
  w("settings err "+str(e))

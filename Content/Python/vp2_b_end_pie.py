import unreal
subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if subsys and subsys.is_in_play_in_editor():
    subsys.editor_request_end_play()
    unreal.log("ended PIE")

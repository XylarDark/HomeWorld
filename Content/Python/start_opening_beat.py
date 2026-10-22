# start_opening_beat.py
# Load L_SizeTest, begin one PIE, send hw.Playtest.FastForward once, and leave PIE running.
# The word is the first line of Saved/opening_beat.txt.

import os

import unreal

_HANDLE = None
_PHASE = "load"
LEVEL_PATH = "/Game/HomeWorld/Maps/SizeTest/L_SizeTest"
LEVEL_TOKEN = "L_SizeTest"


def _beat():
    saved = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_saved_dir())
    path = os.path.join(saved, "opening_beat.txt")
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read().strip()
    except Exception:
        return ""


def _tick(_delta):
    global _HANDLE, _PHASE
    subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if _PHASE == "load":
        world = unreal.EditorLevelLibrary.get_editor_world()
        if world is None or LEVEL_TOKEN not in world.get_path_name():
            return
        if subsys.is_in_play_in_editor():
            return
        subsys.editor_request_begin_play()
        _PHASE = "pie"
        unreal.log("playtest_start: PIE requested")
        return
    if _PHASE != "pie":
        return
    try:
        worlds = unreal.EditorLevelLibrary.get_pie_worlds(False)
    except Exception:
        return
    if not worlds:
        return
    world = worlds[0]
    try:
        pawn = unreal.GameplayStatics.get_player_pawn(world, 0)
    except Exception:
        return
    if pawn is None:
        return
    beat = _beat()
    if not beat:
        unreal.log("playtest_start: no beat")
    else:
        command = "hw.Playtest.FastForward " + beat
        unreal.SystemLibrary.execute_console_command(world, command)
        unreal.log("playtest_start: " + command)
    _PHASE = "done"
    if _HANDLE is not None:
        unreal.unregister_slate_post_tick_callback(_HANDLE)
        _HANDLE = None


def main():
    global _HANDLE, _PHASE
    _PHASE = "load"
    subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    world = unreal.EditorLevelLibrary.get_editor_world()
    if world is None or LEVEL_TOKEN not in world.get_path_name():
        subsys.load_level(LEVEL_PATH)
    _HANDLE = unreal.register_slate_post_tick_callback(_tick)
    unreal.log("playtest_start: armed")


main()

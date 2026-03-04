# start_pie_and_wait.py
# Start PIE if not running and wait for the game to be ready.
# Used before running pie_test_runner.py so PIE-dependent checks (Save/Load, TimeOfDay Phase 2) run.
# Idempotent: if PIE is already running, only waits.

import time

import unreal

def main():
    subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if not subsys:
        print("start_pie_and_wait: LevelEditorSubsystem not found")
        return
    was_running = subsys.is_in_play_in_editor()
    if not was_running:
        subsys.editor_request_begin_play()
        print("start_pie_and_wait: PIE requested, waiting 8s")
        time.sleep(8)
    else:
        print("start_pie_and_wait: PIE already running, waiting 5s")
        time.sleep(5)
    print("start_pie_and_wait: done")

if __name__ == "__main__":
    main()

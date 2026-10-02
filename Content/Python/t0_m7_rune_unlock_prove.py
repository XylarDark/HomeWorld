"""T0_M7 rune unlock prove - BeginPlay/Arrange helpers for Conductor DESKTOP."""
import unreal
import json
import os
from datetime import datetime, timezone

SAVED = unreal.Paths.project_saved_dir()


def _write(name, obj):
    path = os.path.join(SAVED, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    unreal.log("RUNE_PROVE: wrote %s" % path)
    return path


def request_begin_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.editor_request_begin_play()
    unreal.log("RUNE_PROVE: begin_play_requested")
    _write("t0_m7_begin_sidecar.json", {"begin_play_requested": True})


def request_end_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if hasattr(les, "editor_request_end_play"):
        les.editor_request_end_play()
        unreal.log("RUNE_PROVE: end_play_requested")
    else:
        unreal.log("RUNE_PROVE: no editor_request_end_play")


def act_rune_unlock():
    notes = []
    pie_worlds = []
    try:
        pie_worlds = list(unreal.EditorLevelLibrary.get_pie_worlds(False) or [])
    except Exception as e:
        notes.append("pie_worlds_err %s" % e)
    in_pie = len(pie_worlds) > 0
    notes.append("in_pie=%s" % in_pie)
    world = pie_worlds[0] if pie_worlds else unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        _write("t0_m7_rune_unlock_py_act.json", {"ok": False, "notes": notes + ["no world"]})
        return

    unreal.SystemLibrary.execute_console_command(world, "hw.TimeOfDay.SetPhase 0")
    notes.append("tod_setphase_0")
    notes.append("form_default_body_assumed")

    pc = unreal.GameplayStatics.get_player_controller(world, 0)
    pawn = pc.get_controlled_pawn() if pc else None
    notes.append("pawn=%s" % (pawn.get_class().get_name() if pawn else None))

    unlock_ok = False
    method = None
    if pawn and hasattr(pawn, "try_unlock_node_rune"):
        try:
            unlock_ok = bool(pawn.try_unlock_node_rune())
            method = "try_unlock_node_rune"
            notes.append("unlock_direct ok=%s" % unlock_ok)
        except Exception as e:
            notes.append("unlock_direct_err %s" % e)
    else:
        notes.append("no_try_unlock_attr")

    unreal.SystemLibrary.execute_console_command(world, "hw.Rune.Unlock")
    notes.append("console_hw.Rune.Unlock")

    latched = False
    if pawn and hasattr(pawn, "is_rune_gate_unlocked"):
        try:
            latched = bool(pawn.is_rune_gate_unlocked())
            notes.append("latched=%s" % latched)
        except Exception as e:
            notes.append("latched_err %s" % e)

    _write(
        "t0_m7_rune_unlock_py_act.json",
        {
            "ok": bool(unlock_ok or latched),
            "method": method,
            "unlock_ok": unlock_ok,
            "latched": latched,
            "notes": notes,
            "ts_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    unreal.log("RUNE_PROVE: act done unlock=%s latched=%s method=%s" % (unlock_ok, latched, method))


req_path = os.path.join(SAVED, "t0_m7_rune_unlock_request.json")
mode = "act"
if os.path.isfile(req_path):
    try:
        with open(req_path, "r", encoding="utf-8") as f:
            mode = json.load(f).get("mode", "act")
    except Exception:
        pass

if mode == "begin":
    request_begin_play()
elif mode == "end":
    request_end_play()
else:
    act_rune_unlock()
"""T0_M6 field gather prove - BeginPlay/Arrange helpers for Conductor DESKTOP."""
import unreal
import json
import os
from datetime import datetime, timezone

SAVED = unreal.Paths.project_saved_dir()


def _write(name, obj):
    path = os.path.join(SAVED, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    unreal.log("FIELD_GATHER_PROVE: wrote %s" % path)
    return path


def request_begin_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.editor_request_begin_play()
    unreal.log("FIELD_GATHER_PROVE: begin_play_requested")
    _write("t0_m6_begin_sidecar.json", {"begin_play_requested": True})


def request_end_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if hasattr(les, "editor_request_end_play"):
        les.editor_request_end_play()
        unreal.log("FIELD_GATHER_PROVE: end_play_requested")
    else:
        unreal.log("FIELD_GATHER_PROVE: no editor_request_end_play")


def act_field_gather():
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
        _write("t0_m6_field_gather_py_act.json", {"ok": False, "notes": notes + ["no world"]})
        return

    # Arrange: day + body form (match Plant/Backpack)
    unreal.SystemLibrary.execute_console_command(world, "hw.TimeOfDay.SetPhase 0")
    notes.append("tod_setphase_0")
    notes.append("form_default_body_assumed")

    pc = unreal.GameplayStatics.get_player_controller(world, 0)
    pawn = pc.get_controlled_pawn() if pc else None
    notes.append("pawn=%s" % (pawn.get_class().get_name() if pawn else None))

    collect_ok = False
    method = None
    if pawn and hasattr(pawn, "try_collect_node_field_gather"):
        try:
            collect_ok = bool(pawn.try_collect_node_field_gather())
            method = "try_collect_node_field_gather"
            notes.append("collect_direct ok=%s" % collect_ok)
        except Exception as e:
            notes.append("collect_direct_err %s" % e)
    else:
        notes.append("no_try_collect_attr")

    unreal.SystemLibrary.execute_console_command(world, "hw.FieldGather.Collect")
    notes.append("console_hw.FieldGather.Collect")

    _write(
        "t0_m6_field_gather_py_act.json",
        {
            "ok": bool(collect_ok),
            "method": method,
            "collect_ok": collect_ok,
            "notes": notes,
            "ts_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    unreal.log("FIELD_GATHER_PROVE: act done collect=%s method=%s" % (collect_ok, method))


req_path = os.path.join(SAVED, "t0_m6_field_gather_request.json")
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
    act_field_gather()
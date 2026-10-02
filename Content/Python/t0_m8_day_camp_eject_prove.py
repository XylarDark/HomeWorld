"""T0_M8 day camp eject prove - BeginPlay/Arrange helpers for Conductor DESKTOP."""
import unreal
import json
import os
from datetime import datetime, timezone

SAVED = unreal.Paths.project_saved_dir()


def _write(name, obj):
    path = os.path.join(SAVED, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    unreal.log("DAYCAMP_PROVE: wrote %s" % path)
    return path


def request_begin_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.editor_request_begin_play()
    unreal.log("DAYCAMP_PROVE: begin_play_requested")
    _write("t0_m8_begin_sidecar.json", {"begin_play_requested": True})


def request_end_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if hasattr(les, "editor_request_end_play"):
        les.editor_request_end_play()
        unreal.log("DAYCAMP_PROVE: end_play_requested")
    else:
        unreal.log("DAYCAMP_PROVE: no editor_request_end_play")


def act_day_camp_eject():
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
        _write("t0_m8_day_camp_eject_py_act.json", {"ok": False, "notes": notes + ["no world"]})
        return

    # Arrange: Day + body (FORM_BODY assumed default)
    unreal.SystemLibrary.execute_console_command(world, "hw.TimeOfDay.SetPhase 0")
    notes.append("tod_setphase_0")
    notes.append("form_default_body_assumed")

    pc = unreal.GameplayStatics.get_player_controller(world, 0)
    pawn = pc.get_controlled_pawn() if pc else None
    notes.append("pawn=%s" % (pawn.get_class().get_name() if pawn else None))

    eject_ok = False
    method = None
    if pawn and hasattr(pawn, "try_eject_node_day_camp"):
        try:
            eject_ok = bool(pawn.try_eject_node_day_camp())
            method = "try_eject_node_day_camp"
            notes.append("eject_direct ok=%s" % eject_ok)
        except Exception as e:
            notes.append("eject_direct_err %s" % e)
    else:
        notes.append("no_try_eject_attr")

    # Console path (primary greppable evidence)
    unreal.SystemLibrary.execute_console_command(world, "hw.DayCamp.Eject")
    notes.append("console_hw.DayCamp.Eject")

    latched = False
    if pawn and hasattr(pawn, "is_day_camp_eject_triggered"):
        try:
            latched = bool(pawn.is_day_camp_eject_triggered())
            notes.append("latched=%s" % latched)
        except Exception as e:
            notes.append("latched_err %s" % e)

    _write(
        "t0_m8_day_camp_eject_py_act.json",
        {
            "ok": bool(eject_ok or latched),
            "method": method,
            "eject_ok": eject_ok,
            "latched": latched,
            "notes": notes,
            "labels": ["NODE_DAY_CAMP", "EJECT_HOME", "TOD_DAY", "FORM_BODY", "CAM_T0_CAMP_DAY"],
            "anti": ["SM_ProxyDayCamp", "GP_RS_HumanoidCamp", "TryStartFallbackGlide", "StartGlide alone"],
            "ts_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    unreal.log("DAYCAMP_PROVE: act done eject=%s latched=%s method=%s" % (eject_ok, latched, method))


req_path = os.path.join(SAVED, "t0_m8_day_camp_eject_request.json")
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
    act_day_camp_eject()

"""T0_M11 bed→spirit prove - BeginPlay/Arrange helpers for Conductor DESKTOP."""
import unreal
import json
import os
from datetime import datetime, timezone

SAVED = unreal.Paths.project_saved_dir()


def _write(name, obj):
    path = os.path.join(SAVED, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    unreal.log("BED_SPIRIT_PROVE: wrote %s" % path)
    return path


def request_begin_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.editor_request_begin_play()
    unreal.log("BED_SPIRIT_PROVE: begin_play_requested")
    _write("t0_m11_begin_sidecar.json", {"begin_play_requested": True})


def request_end_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if hasattr(les, "editor_request_end_play"):
        les.editor_request_end_play()
        unreal.log("BED_SPIRIT_PROVE: end_play_requested")
    else:
        unreal.log("BED_SPIRIT_PROVE: no editor_request_end_play")


def act_bed_spirit():
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
        _write("t0_m11_bed_spirit_py_act.json", {"ok": False, "notes": notes + ["no world"]})
        return

    # Arrange: Day + body, then the bed. The rune is removed.
    unreal.SystemLibrary.execute_console_command(world, "hw.TimeOfDay.SetPhase 0")
    notes.append("tod_setphase_0_day")
    notes.append("form_default_body_assumed")
    notes.append("no_soft_kidnap")

    pc = unreal.GameplayStatics.get_player_controller(world, 0)
    pawn = pc.get_controlled_pawn() if pc else None
    notes.append("pawn=%s" % (pawn.get_class().get_name() if pawn else None))

    bed_ok = False
    method = None
    if pawn and hasattr(pawn, "try_bed_sleep_spirit"):
        try:
            bed_ok = bool(pawn.try_bed_sleep_spirit())
            method = "try_bed_sleep_spirit"
            notes.append("bed_direct ok=%s" % bed_ok)
        except Exception as e:
            notes.append("bed_direct_err %s" % e)
    else:
        notes.append("no_try_bed_attr")

    unreal.SystemLibrary.execute_console_command(world, "hw.Bed.SleepSpirit")
    notes.append("console_hw.Bed.SleepSpirit")

    latched = False
    sleep_gate = False
    spirit = False
    if pawn:
        if hasattr(pawn, "is_bed_spirit_granted"):
            try:
                latched = bool(pawn.is_bed_spirit_granted())
                notes.append("latched=%s" % latched)
            except Exception as e:
                notes.append("latched_err %s" % e)
        if hasattr(pawn, "is_spirit_sleep_gate_granted"):
            try:
                sleep_gate = bool(pawn.is_spirit_sleep_gate_granted())
                notes.append("sleep_gate=%s" % sleep_gate)
            except Exception as e:
                notes.append("sleep_gate_err %s" % e)
        if hasattr(pawn, "get_is_spirit_form"):
            try:
                spirit = bool(pawn.get_is_spirit_form())
                notes.append("spirit_form=%s" % spirit)
            except Exception as e:
                notes.append("spirit_form_err %s" % e)

    _write(
        "t0_m11_bed_spirit_py_act.json",
        {
            "ok": bool(bed_ok or latched or spirit),
            "method": method,
            "bed_ok": bed_ok,
            "latched": latched,
            "sleep_gate": sleep_gate,
            "spirit": spirit,
            "notes": notes,
            "labels": ["NODE_BED", "TOD_NIGHT_SPIRIT", "FORM_SPIRIT", "CAM_T0_BED"],
            "anti": ["phase-alone", "soft-kidnap", "spirit-w/o-bed", "SetPhase-alone-spirit"],
            "ts_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    unreal.log(
        "BED_SPIRIT_PROVE: act done bed=%s latched=%s spirit=%s method=%s"
        % (bed_ok, latched, spirit, method)
    )


req_path = os.path.join(SAVED, "t0_m11_bed_spirit_request.json")
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
    act_bed_spirit()

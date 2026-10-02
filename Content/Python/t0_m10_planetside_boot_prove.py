"""T0_M10 planetside night boot prove - BeginPlay/Arrange helpers for Conductor DESKTOP."""
import unreal
import json
import os
from datetime import datetime, timezone

SAVED = unreal.Paths.project_saved_dir()


def _write(name, obj):
    path = os.path.join(SAVED, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    unreal.log("PLANETSIDE_BOOT_PROVE: wrote %s" % path)
    return path


def request_begin_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.editor_request_begin_play()
    unreal.log("PLANETSIDE_BOOT_PROVE: begin_play_requested")
    _write("t0_m10_begin_sidecar.json", {"begin_play_requested": True})


def request_end_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if hasattr(les, "editor_request_end_play"):
        les.editor_request_end_play()
        unreal.log("PLANETSIDE_BOOT_PROVE: end_play_requested")
    else:
        unreal.log("PLANETSIDE_BOOT_PROVE: no editor_request_end_play")


def act_planetside_boot():
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
        _write("t0_m10_planetside_boot_py_act.json", {"ok": False, "notes": notes + ["no world"]})
        return

    # Arrange: Night + body (FORM_BODY assumed; no bed / no GoToBed)
    unreal.SystemLibrary.execute_console_command(world, "hw.TimeOfDay.SetPhase 2")
    notes.append("tod_setphase_2_night")
    notes.append("form_default_body_assumed")
    notes.append("no_bed_no_gotobed")

    pc = unreal.GameplayStatics.get_player_controller(world, 0)
    pawn = pc.get_controlled_pawn() if pc else None
    notes.append("pawn=%s" % (pawn.get_class().get_name() if pawn else None))

    boot_ok = False
    method = None
    if pawn and hasattr(pawn, "try_boot_planetside_night_home"):
        try:
            boot_ok = bool(pawn.try_boot_planetside_night_home())
            method = "try_boot_planetside_night_home"
            notes.append("boot_direct ok=%s" % boot_ok)
        except Exception as e:
            notes.append("boot_direct_err %s" % e)
    else:
        notes.append("no_try_boot_attr")

    # Console path (primary greppable evidence) — NOT hw.DayCamp.Eject
    unreal.SystemLibrary.execute_console_command(world, "hw.Planetside.BootHome")
    notes.append("console_hw.Planetside.BootHome")

    latched = False
    if pawn and hasattr(pawn, "is_planetside_night_boot_triggered"):
        try:
            latched = bool(pawn.is_planetside_night_boot_triggered())
            notes.append("latched=%s" % latched)
        except Exception as e:
            notes.append("latched_err %s" % e)

    _write(
        "t0_m10_planetside_boot_py_act.json",
        {
            "ok": bool(boot_ok or latched),
            "method": method,
            "boot_ok": boot_ok,
            "latched": latched,
            "notes": notes,
            "labels": ["EJECT_HOME", "TOD_NIGHT_HOME", "FORM_BODY", "NODE_GLIDER"],
            "anti": ["hw.DayCamp.Eject", "TryEjectNodeDayCamp", "TryStartFallbackGlide", "soft-kidnap"],
            "ts_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    unreal.log("PLANETSIDE_BOOT_PROVE: act done boot=%s latched=%s method=%s" % (boot_ok, latched, method))


req_path = os.path.join(SAVED, "t0_m10_planetside_boot_request.json")
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
    act_planetside_boot()

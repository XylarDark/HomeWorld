"""T0_M13 portal camp prove - BeginPlay/Arrange helpers for Conductor DESKTOP."""
import unreal
import json
import os
from datetime import datetime, timezone

SAVED = unreal.Paths.project_saved_dir()


def _write(name, obj):
    path = os.path.join(SAVED, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    unreal.log("PORTAL_CAMP_PROVE: wrote %s" % path)
    return path


def request_begin_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.editor_request_begin_play()
    unreal.log("PORTAL_CAMP_PROVE: begin_play_requested")
    _write("t0_m13_begin_sidecar.json", {"begin_play_requested": True})


def request_end_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if hasattr(les, "editor_request_end_play"):
        les.editor_request_end_play()
        unreal.log("PORTAL_CAMP_PROVE: end_play_requested")
    else:
        unreal.log("PORTAL_CAMP_PROVE: no editor_request_end_play")


def act_portal_camp():
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
        _write("t0_m13_portal_camp_py_act.json", {"ok": False, "notes": notes + ["no world"]})
        return

    pc = unreal.GameplayStatics.get_player_controller(world, 0)
    pawn = pc.get_controlled_pawn() if pc else None
    notes.append("pawn=%s" % (pawn.get_class().get_name() if pawn else None))

    # Arrange #11: rune + bed spirit
    unreal.SystemLibrary.execute_console_command(world, "hw.Rune.Unlock")
    notes.append("console_hw.Rune.Unlock")
    unreal.SystemLibrary.execute_console_command(world, "hw.Bed.SleepSpirit")
    notes.append("console_hw.Bed.SleepSpirit")

    spirit = False
    if pawn and hasattr(pawn, "get_is_spirit_form"):
        try:
            spirit = bool(pawn.get_is_spirit_form())
            notes.append("spirit_form=%s" % spirit)
        except Exception as e:
            notes.append("spirit_form_err %s" % e)

    portal_ok = False
    method = None
    if pawn and hasattr(pawn, "try_portal_home_to_camp"):
        try:
            portal_ok = bool(pawn.try_portal_home_to_camp())
            method = "try_portal_home_to_camp"
            notes.append("portal_direct ok=%s" % portal_ok)
        except Exception as e:
            notes.append("portal_direct_err %s" % e)
    else:
        notes.append("no_try_portal_attr")

    unreal.SystemLibrary.execute_console_command(world, "hw.Portal.Camp")
    notes.append("console_hw.Portal.Camp")

    # Soft second call
    unreal.SystemLibrary.execute_console_command(world, "hw.Portal.Camp")
    notes.append("console_hw.Portal.Camp_again")

    latched = False
    if pawn and hasattr(pawn, "is_portal_home_to_camp_granted"):
        try:
            latched = bool(pawn.is_portal_home_to_camp_granted())
            notes.append("latched=%s" % latched)
        except Exception as e:
            notes.append("latched_err %s" % e)

    _write(
        "t0_m13_portal_camp_py_act.json",
        {
            "ok": bool(portal_ok or latched),
            "method": method,
            "portal_ok": portal_ok,
            "latched": latched,
            "spirit": spirit,
            "notes": notes,
            "labels": ["NODE_PORTAL_HOME", "NODE_PORTAL_CAMP", "TOD_NIGHT_SPIRIT", "FORM_SPIRIT"],
            "anti": ["home-planet-alone", "body-form", "dress-as-camp"],
            "ts_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    unreal.log(
        "PORTAL_CAMP_PROVE: act done portal=%s latched=%s method=%s"
        % (portal_ok, latched, method)
    )


req_path = os.path.join(SAVED, "t0_m13_portal_camp_request.json")
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
    act_portal_camp()

"""T0_M14 camp night prove - BeginPlay/Arrange helpers for Conductor DESKTOP."""
import unreal
import json
import os
from datetime import datetime, timezone

SAVED = unreal.Paths.project_saved_dir()


def _write(name, obj):
    path = os.path.join(SAVED, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    unreal.log("CAMP_NIGHT_PROVE: wrote %s" % path)
    return path


def request_begin_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.editor_request_begin_play()
    unreal.log("CAMP_NIGHT_PROVE: begin_play_requested")
    _write("t0_m14_begin_sidecar.json", {"begin_play_requested": True})


def request_end_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if hasattr(les, "editor_request_end_play"):
        les.editor_request_end_play()
        unreal.log("CAMP_NIGHT_PROVE: end_play_requested")
    else:
        unreal.log("CAMP_NIGHT_PROVE: no editor_request_end_play")


def act_camp_night():
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
        _write("t0_m14_camp_night_py_act.json", {"ok": False, "notes": notes + ["no world"]})
        return

    pc = unreal.GameplayStatics.get_player_controller(world, 0)
    pawn = pc.get_controlled_pawn() if pc else None
    notes.append("pawn=%s" % (pawn.get_class().get_name() if pawn else None))

    # Arrange #11: rune + bed spirit -> FORM_SPIRIT / TOD_NIGHT_SPIRIT
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

    # Optional #13 camp route (soft OK)
    unreal.SystemLibrary.execute_console_command(world, "hw.Portal.Camp")
    notes.append("console_hw.Portal.Camp_optional")

    camp_ok = False
    method = None
    if pawn and hasattr(pawn, "try_camp_night"):
        try:
            camp_ok = bool(pawn.try_camp_night())
            method = "try_camp_night"
            notes.append("camp_direct ok=%s" % camp_ok)
        except Exception as e:
            notes.append("camp_direct_err %s" % e)
    else:
        notes.append("no_try_camp_night_attr")

    unreal.SystemLibrary.execute_console_command(world, "hw.CampNight")
    notes.append("console_hw.CampNight")

    # Soft second call (already granted)
    unreal.SystemLibrary.execute_console_command(world, "hw.CampNight")
    notes.append("console_hw.CampNight_again")

    latched = False
    if pawn and hasattr(pawn, "is_camp_night_granted"):
        try:
            latched = bool(pawn.is_camp_night_granted())
            notes.append("latched=%s" % latched)
        except Exception as e:
            notes.append("latched_err %s" % e)

    guards = None
    sleepers = None
    if pawn:
        try:
            stealth = pawn.get_component_by_class(unreal.load_class(None, "/Script/HomeWorld.HomeWorldSpiritStealthComponent"))
            if stealth:
                if hasattr(stealth, "get_guards_avoided_this_session"):
                    guards = int(stealth.get_guards_avoided_this_session())
                if hasattr(stealth, "get_sleepers_soothed_this_session"):
                    sleepers = int(stealth.get_sleepers_soothed_this_session())
                notes.append("guards=%s sleepers=%s" % (guards, sleepers))
        except Exception as e:
            notes.append("stealth_counts_err %s" % e)

    _write(
        "t0_m14_camp_night_py_act.json",
        {
            "ok": bool(camp_ok or latched),
            "method": method,
            "camp_ok": camp_ok,
            "latched": latched,
            "spirit": spirit,
            "guards_avoided": guards,
            "sleepers_soothed": sleepers,
            "notes": notes,
            "labels": [
                "NODE_GUARD",
                "NODE_SLEEPER",
                "TOD_NIGHT_SPIRIT",
                "FORM_SPIRIT",
                "CAM_T0_CAMP_NIGHT",
            ],
            "anti": ["GP_SS_Lit_alone", "stealth-alone", "convert-as-soothe", "body-form"],
            "ts_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    unreal.log(
        "CAMP_NIGHT_PROVE: act done camp=%s latched=%s method=%s"
        % (camp_ok, latched, method)
    )


req_path = os.path.join(SAVED, "t0_m14_camp_night_request.json")
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
    act_camp_night()

"""T0_M12 nurture slot prove - BeginPlay/Arrange helpers for Conductor DESKTOP."""
import unreal
import json
import os
from datetime import datetime, timezone

SAVED = unreal.Paths.project_saved_dir()


def _write(name, obj):
    path = os.path.join(SAVED, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    unreal.log("NURTURE_SLOT_PROVE: wrote %s" % path)
    return path


def request_begin_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.editor_request_begin_play()
    unreal.log("NURTURE_SLOT_PROVE: begin_play_requested")
    _write("t0_m12_begin_sidecar.json", {"begin_play_requested": True})


def request_end_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if hasattr(les, "editor_request_end_play"):
        les.editor_request_end_play()
        unreal.log("NURTURE_SLOT_PROVE: end_play_requested")
    else:
        unreal.log("NURTURE_SLOT_PROVE: no editor_request_end_play")


def _ensure_n1(world, notes):
    """KEEP-LOCAL Arrange: spawn AHomeWorldNurtureTarget N1 if map has none (no .uasset commit)."""
    n1_count = 0
    try:
        for a in unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor.static_class()) or []:
            try:
                # Find nurture component via python reflection if exposed
                comps = a.get_components_by_class(unreal.load_class(None, "/Script/HomeWorld.HomeWorldNurtureComponent"))
                if comps:
                    for c in comps:
                        tid = None
                        if hasattr(c, "get_target_id"):
                            tid = c.get_target_id()
                        # enum 0 = N1_Crop
                        if tid is None or int(tid) == 0 or str(tid).endswith("N1_CROP") or str(tid) == "N1_Crop":
                            n1_count += 1
            except Exception:
                pass
    except Exception as e:
        notes.append("scan_err %s" % e)
    notes.append("n1_found=%s" % n1_count)
    if n1_count > 0:
        return True

    cls = unreal.load_class(None, "/Script/HomeWorld.HomeWorldNurtureTarget")
    if not cls:
        notes.append("no_HomeWorldNurtureTarget_class")
        return False
    loc = unreal.Vector(0.0, 0.0, 100.0)
    rot = unreal.Rotator(0.0, 0.0, 0.0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(cls, loc, rot)
    if not actor:
        # PIE spawn fallback
        try:
            actor = world.spawn_actor(cls, loc, rot)
        except Exception as e:
            notes.append("spawn_err %s" % e)
            return False
    if not actor:
        notes.append("spawn_n1_failed")
        return False
    notes.append("spawned_KEEP_LOCAL_N1=%s" % actor.get_name())
    # Configure N1 + RES_SEED if component exposed
    try:
        comps = actor.get_components_by_class(unreal.load_class(None, "/Script/HomeWorld.HomeWorldNurtureComponent"))
        if comps and hasattr(comps[0], "configure_target"):
            # N1_Crop = 0, RES_SEED
            comps[0].configure_target(0, "RES_SEED")
            notes.append("configured_N1_RES_SEED")
    except Exception as e:
        notes.append("configure_err %s" % e)
    return True


def act_nurture_slot():
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
        _write("t0_m12_nurture_slot_py_act.json", {"ok": False, "notes": notes + ["no world"]})
        return

    pc = unreal.GameplayStatics.get_player_controller(world, 0)
    pawn = pc.get_controlled_pawn() if pc else None
    notes.append("pawn=%s" % (pawn.get_class().get_name() if pawn else None))

    # KEEP-LOCAL ensure N1 (map may lack GP_N1 instance this session)
    _ensure_n1(world, notes)

    # Arrange #3: Day + plant (must be body - so plant BEFORE spirit)
    unreal.SystemLibrary.execute_console_command(world, "hw.TimeOfDay.SetPhase 0")
    notes.append("tod_setphase_0_day")
    # If already spirit from prior act, plant may fail FORM_BODY — end/rebegin preferred;
    # try plant anyway; if spirit, note it.
    spirit_early = False
    if pawn and hasattr(pawn, "get_is_spirit_form"):
        try:
            spirit_early = bool(pawn.get_is_spirit_form())
            notes.append("spirit_before_plant=%s" % spirit_early)
        except Exception as e:
            notes.append("spirit_early_err %s" % e)

    unreal.SystemLibrary.execute_console_command(world, "hw.Gather.Flowers")
    notes.append("console_hw.Gather.Flowers")
    unreal.SystemLibrary.execute_console_command(world, "hw.Plant.Slot")
    notes.append("console_hw.Plant.Slot")

    planted = False
    if pawn and hasattr(pawn, "is_node_plant_slot_day_planted"):
        try:
            planted = bool(pawn.is_node_plant_slot_day_planted())
            notes.append("day_planted=%s" % planted)
        except Exception as e:
            notes.append("day_planted_err %s" % e)

    # Arrange #11: the bed grants spirit. The rune is removed.
    unreal.SystemLibrary.execute_console_command(world, "hw.Bed.SleepSpirit")
    notes.append("console_hw.Bed.SleepSpirit")

    spirit = False
    if pawn and hasattr(pawn, "get_is_spirit_form"):
        try:
            spirit = bool(pawn.get_is_spirit_form())
            notes.append("spirit_form=%s" % spirit)
        except Exception as e:
            notes.append("spirit_form_err %s" % e)

    unreal.SystemLibrary.execute_console_command(world, "hw.Gather.Seed")
    notes.append("console_hw.Gather.Seed")

    nurture_ok = False
    method = None
    if pawn and hasattr(pawn, "try_nurture_node_plant_slot"):
        try:
            nurture_ok = bool(pawn.try_nurture_node_plant_slot())
            method = "try_nurture_node_plant_slot"
            notes.append("nurture_direct ok=%s" % nurture_ok)
        except Exception as e:
            notes.append("nurture_direct_err %s" % e)
    else:
        notes.append("no_try_nurture_attr")

    unreal.SystemLibrary.execute_console_command(world, "hw.Nurture.Slot")
    notes.append("console_hw.Nurture.Slot")

    latched = False
    if pawn and hasattr(pawn, "is_node_plant_slot_spirit_nurtured"):
        try:
            latched = bool(pawn.is_node_plant_slot_spirit_nurtured())
            notes.append("latched=%s" % latched)
        except Exception as e:
            notes.append("latched_err %s" % e)

    _write(
        "t0_m12_nurture_slot_py_act.json",
        {
            "ok": bool(nurture_ok or latched),
            "method": method,
            "nurture_ok": nurture_ok,
            "latched": latched,
            "planted": planted,
            "spirit": spirit,
            "notes": notes,
            "labels": ["NODE_PLANT_SLOT", "TOD_NIGHT_SPIRIT", "FORM_SPIRIT"],
            "anti": ["N2", "body-form", "day-plant-alone", "unplanted"],
            "ts_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    unreal.log(
        "NURTURE_SLOT_PROVE: act done nurture=%s latched=%s method=%s"
        % (nurture_ok, latched, method)
    )


req_path = os.path.join(SAVED, "t0_m12_nurture_slot_request.json")
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
    act_nurture_slot()

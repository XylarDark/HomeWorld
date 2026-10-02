"""T0_M4 backpack prove - BeginPlay/Arrange helpers for Conductor DESKTOP."""
import unreal
import json
import os
from datetime import datetime, timezone

SAVED = unreal.Paths.project_saved_dir()


def _write(name, obj):
    path = os.path.join(SAVED, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    unreal.log("BACKPACK_PROVE: wrote %s" % path)
    return path


def request_begin_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.editor_request_begin_play()
    unreal.log("BACKPACK_PROVE: begin_play_requested")
    _write("t0_m4_begin_sidecar.json", {"begin_play_requested": True})


def request_end_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if hasattr(les, "editor_request_end_play"):
        les.editor_request_end_play()
        unreal.log("BACKPACK_PROVE: end_play_requested")
    else:
        unreal.log("BACKPACK_PROVE: no editor_request_end_play")


def act_backpack():
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
        _write("t0_m4_backpack_py_act.json", {"ok": False, "notes": notes + ["no world"]})
        return

    unreal.SystemLibrary.execute_console_command(world, "hw.TimeOfDay.SetPhase 0")
    notes.append("tod_setphase_0")

    unreal.SystemLibrary.execute_console_command(world, "hw.Inventory.Open")
    notes.append("inventory_open_pre_equip")

    pc = unreal.GameplayStatics.get_player_controller(world, 0)
    pawn = pc.get_controlled_pawn() if pc else None
    notes.append("pawn=%s" % (pawn.get_class().get_name() if pawn else None))

    equip_ok = False
    open_ok = False
    method = None
    if pawn and hasattr(pawn, "try_equip_node_backpack"):
        try:
            equip_ok = bool(pawn.try_equip_node_backpack())
            method = "try_equip_node_backpack"
            notes.append("equip_direct ok=%s" % equip_ok)
        except Exception as e:
            notes.append("equip_direct_err %s" % e)
    else:
        notes.append("no_try_equip_attr")

    unreal.SystemLibrary.execute_console_command(world, "hw.Backpack.Equip")
    notes.append("console_hw.Backpack.Equip")

    if pawn and hasattr(pawn, "try_open_inventory_gated"):
        try:
            open_ok = bool(pawn.try_open_inventory_gated())
            notes.append("open_direct ok=%s" % open_ok)
        except Exception as e:
            notes.append("open_direct_err %s" % e)
    else:
        notes.append("no_try_open_attr")

    unreal.SystemLibrary.execute_console_command(world, "hw.Inventory.Open")
    notes.append("console_hw.Inventory.Open_post")

    equipped = False
    if pawn and hasattr(pawn, "is_backpack_equipped"):
        try:
            equipped = bool(pawn.is_backpack_equipped())
            notes.append("equipped=%s" % equipped)
        except Exception as e:
            notes.append("equipped_err %s" % e)

    _write(
        "t0_m4_backpack_py_act.json",
        {
            "ok": bool((equip_ok or equipped) and (open_ok or equipped)),
            "method": method,
            "equip_ok": equip_ok,
            "open_ok": open_ok,
            "equipped": equipped,
            "notes": notes,
            "ts_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    unreal.log("BACKPACK_PROVE: act done equip=%s open=%s equipped=%s" % (equip_ok, open_ok, equipped))


req_path = os.path.join(SAVED, "t0_m4_backpack_request.json")
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
    act_backpack()
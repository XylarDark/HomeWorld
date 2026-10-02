"""T0_M3 plant prove — BeginPlay/Arrange helpers for Conductor DESKTOP."""
import unreal
import json
import os
from datetime import datetime, timezone

SAVED = unreal.Paths.project_saved_dir()


def _write(name, obj):
    path = os.path.join(SAVED, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    unreal.log(f"PLANT_PROVE: wrote {path}")
    return path


def request_begin_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.editor_request_begin_play()
    unreal.log("PLANT_PROVE: begin_play_requested")
    _write("t0_m3_begin_sidecar.json", {"begin_play_requested": True})


def request_end_play():
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    # editor_request_end_play if present
    if hasattr(les, "editor_request_end_play"):
        les.editor_request_end_play()
        unreal.log("PLANT_PROVE: end_play_requested")
    else:
        unreal.SystemLibrary.execute_console_command(None, "quit")  # bad — avoid
        unreal.log("PLANT_PROVE: no editor_request_end_play")


def act_plant():
    notes = []
    pie_worlds = []
    try:
        pie_worlds = list(unreal.EditorLevelLibrary.get_pie_worlds(False) or [])
    except Exception as e:
        notes.append(f"pie_worlds_err {e}")
    in_pie = len(pie_worlds) > 0
    notes.append(f"in_pie={in_pie}")
    notes.append(f"pie_worlds={len(pie_worlds)}")
    world = pie_worlds[0] if pie_worlds else unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        _write("t0_m3_plant_py_act.json", {"ok": False, "notes": notes + ["no world"]})
        return

    # Day via console (works in PIE)
    unreal.SystemLibrary.execute_console_command(world, "hw.TimeOfDay.SetPhase 0")
    notes.append("tod_setphase_0")

    # Grant herbs
    unreal.SystemLibrary.execute_console_command(world, "hw.Gather.Flowers")
    notes.append("gather_flowers")

    pc = unreal.GameplayStatics.get_player_controller(world, 0)
    pawn = pc.get_controlled_pawn() if pc else None
    notes.append(f"pawn={pawn.get_class().get_name() if pawn else None}")

    ok = False
    method = None
    if pawn and hasattr(pawn, "try_plant_node_plant_slot_herb"):
        try:
            ok = bool(pawn.try_plant_node_plant_slot_herb())
            method = "try_plant_node_plant_slot_herb"
            notes.append(f"direct_call ok={ok}")
        except Exception as e:
            notes.append(f"direct_call_err {e}")
    else:
        notes.append("no_try_plant_attr")

    # Console fallback (may be unregistered under LiveCoding without StartupModule)
    unreal.SystemLibrary.execute_console_command(world, "hw.Plant.Slot")
    notes.append("console_hw.Plant.Slot")

    marked = False
    if pawn and hasattr(pawn, "is_node_plant_slot_day_planted"):
        try:
            marked = bool(pawn.is_node_plant_slot_day_planted())
            notes.append(f"day_planted={marked}")
        except Exception as e:
            notes.append(f"day_planted_err {e}")

    _write(
        "t0_m3_plant_py_act.json",
        {
            "ok": ok or marked,
            "method": method,
            "marked": marked,
            "notes": notes,
            "ts_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    unreal.log(f"PLANT_PROVE: act done ok={ok} marked={marked}")


# Default when run via MCP: detect mode from sidecar request
req_path = os.path.join(SAVED, "t0_m3_plant_request.json")
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
    act_plant()

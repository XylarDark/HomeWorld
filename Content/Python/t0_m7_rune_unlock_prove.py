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
    """The rune is removed. The bed grants spirit. This prove does not unlock anything."""
    _write(
        "t0_m7_rune_unlock_py_act.json",
        {
            "ok": False,
            "removed": True,
            "notes": ["rune removed; the bed grants spirit"],
            "ts_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    unreal.log("RUNE_PROVE: removed; the bed grants spirit")


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
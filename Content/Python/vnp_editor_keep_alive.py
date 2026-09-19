"""Pattern helper: keep UnrealEditor-Cmd Python session alive for latent work.

UE 5.8: call ``unreal.EditorPythonScripting.set_keep_python_script_alive(True)``
before scheduling latent AutomationLibrary / screenshot / load_map work so the
Cmd process does not quit when the entry script returns.

Usage (inside Editor or -ExecutePythonScript):

    import vnp_editor_keep_alive as keep
    keep.arm()
    # ... AutomationLibrary.take_high_res_screenshot / load_map ...
    # call keep.disarm() when finished if you need a clean Cmd exit

See docs/Automation/FULL_AUTOMATION_RESEARCH.md § keep_python_script_alive.
"""
from __future__ import annotations

import unreal


def arm() -> bool:
    try:
        unreal.EditorPythonScripting.set_keep_python_script_alive(True)
        unreal.log("vnp_editor_keep_alive: keep_python_script_alive=True")
        return True
    except Exception as e:
        unreal.log_warning("vnp_editor_keep_alive: arm failed: %s" % e)
        return False


def disarm() -> bool:
    try:
        unreal.EditorPythonScripting.set_keep_python_script_alive(False)
        unreal.log("vnp_editor_keep_alive: keep_python_script_alive=False")
        return True
    except Exception as e:
        unreal.log_warning("vnp_editor_keep_alive: disarm failed: %s" % e)
        return False

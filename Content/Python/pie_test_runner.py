# pie_test_runner.py
# Reusable PIE test runner for HomeWorld.
# Provides start/stop/check utilities and predefined validation checks.
# Results are written to Saved/pie_test_results.json for agent consumption.
#
# Usage via MCP:
#   1. Write Saved/mcp_request.json with {"command":"run_pie_tests","args":{}}
#      then execute mcp_harness.py, OR
#   2. Execute this script directly: execute_python_script("pie_test_runner.py")
#
# All UE 5.7 API quirks are handled here so callers don't need to know them.

import json
import os
import sys
import traceback

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)


def _output_path():
    proj = unreal.Paths.project_dir()
    saved = os.path.join(proj, "Saved")
    os.makedirs(saved, exist_ok=True)
    return os.path.join(saved, "pie_test_results.json")


def is_pie_running():
    try:
        subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        return subsys.is_in_play_in_editor()
    except Exception:
        return False


def start_pie():
    subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if subsys.is_in_play_in_editor():
        return True
    subsys.editor_request_begin_play()
    return True


def stop_pie():
    subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if subsys.is_in_play_in_editor():
        subsys.editor_request_end_play()
    return True


def get_pie_world():
    """Return the first PIE world, or None."""
    try:
        worlds = unreal.EditorLevelLibrary.get_pie_worlds(include_dedicated_server=False)
        return worlds[0] if worlds else None
    except Exception:
        return None


def get_player_pawn(world=None):
    """Return the controlled pawn from PIE, or None."""
    if world is None:
        world = get_pie_world()
    if not world:
        return None
    pc = unreal.GameplayStatics.get_player_controller(world, 0)
    if not pc:
        return None
    try:
        return pc.get_controlled_pawn()
    except Exception:
        return getattr(pc, "pawn", None)


# ---------------------------------------------------------------------------
# Predefined checks — each returns {"name", "passed", "detail"}
# ---------------------------------------------------------------------------

def check_pie_active():
    active = is_pie_running()
    return {"name": "PIE active", "passed": active, "detail": "Running" if active else "Not running"}


def check_character_spawned():
    pawn = get_player_pawn()
    if not pawn:
        return {"name": "Character spawned", "passed": False, "detail": "No controlled pawn"}
    cls = pawn.get_class().get_name()
    expected = "BP_HomeWorldCharacter_C"
    return {
        "name": "Character spawned",
        "passed": expected in cls or "HomeWorldCharacter" in cls,
        "detail": cls,
    }


def check_on_ground():
    pawn = get_player_pawn()
    if not pawn:
        return {"name": "On ground", "passed": False, "detail": "No pawn"}
    try:
        move = pawn.character_movement
        falling = move.is_falling()
        mode = str(move.movement_mode)
        return {
            "name": "On ground",
            "passed": not falling,
            "detail": "Mode: " + mode + ", Falling: " + str(falling),
        }
    except Exception as e:
        return {"name": "On ground", "passed": False, "detail": str(e)}


def check_capsule():
    pawn = get_player_pawn()
    if not pawn:
        return {"name": "Capsule dimensions", "passed": False, "detail": "No pawn"}
    try:
        capsule = pawn.capsule_component
        hh = capsule.get_unscaled_capsule_half_height()
        r = capsule.get_unscaled_capsule_radius()
        return {
            "name": "Capsule dimensions",
            "passed": hh > 0 and r > 0,
            "detail": "Half-height: %.1f, Radius: %.1f" % (hh, r),
        }
    except Exception as e:
        return {"name": "Capsule dimensions", "passed": False, "detail": str(e)}


def check_skeletal_mesh():
    pawn = get_player_pawn()
    if not pawn:
        return {"name": "Skeletal mesh", "passed": False, "detail": "No pawn"}
    try:
        mesh = pawn.mesh
        sk = None
        try:
            sk = mesh.get_editor_property("skeletal_mesh_asset")
        except Exception:
            sk = getattr(mesh, "skeletal_mesh", None)
        name = sk.get_name() if sk else "None"
        return {"name": "Skeletal mesh", "passed": sk is not None, "detail": name}
    except Exception as e:
        return {"name": "Skeletal mesh", "passed": False, "detail": str(e)}


def check_anim_instance():
    pawn = get_player_pawn()
    if not pawn:
        return {"name": "AnimInstance", "passed": False, "detail": "No pawn"}
    try:
        mesh = pawn.mesh
        anim = mesh.get_anim_instance()
        if anim:
            cls = anim.get_class().get_name()
            return {"name": "AnimInstance", "passed": True, "detail": cls}
        return {"name": "AnimInstance", "passed": False, "detail": "No AnimInstance active"}
    except Exception as e:
        return {"name": "AnimInstance", "passed": False, "detail": str(e)}


def check_pcg_actors():
    world = get_pie_world()
    if not world:
        world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        return {"name": "PCG actors", "passed": False, "detail": "No world"}
    try:
        actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.StaticMeshActor)
        count = len(actors) if actors else 0
        return {
            "name": "PCG actors",
            "passed": count > 100,
            "detail": "%d static mesh actors" % count,
        }
    except Exception as e:
        return {"name": "PCG actors", "passed": False, "detail": str(e)}


ALL_CHECKS = [
    check_pie_active,
    check_character_spawned,
    check_on_ground,
    check_capsule,
    check_skeletal_mesh,
    check_anim_instance,
    check_pcg_actors,
]


def run_checks(checks=None):
    """Run a list of check functions and return results."""
    if checks is None:
        checks = ALL_CHECKS
    results = []
    for check_fn in checks:
        try:
            results.append(check_fn())
        except Exception as e:
            results.append({
                "name": check_fn.__name__,
                "passed": False,
                "detail": "Exception: " + str(e),
            })
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    return {
        "summary": "%d/%d passed" % (passed, total),
        "all_passed": passed == total,
        "checks": results,
    }


def main():
    """Run all PIE checks and write results to Saved/pie_test_results.json."""
    output = {"pie_was_running": is_pie_running()}

    if not is_pie_running():
        output["note"] = "PIE not running. Start PIE first for full validation."

    results = run_checks()
    output.update(results)

    out_path = _output_path()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)


if __name__ == "__main__":
    main()

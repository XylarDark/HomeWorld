# mcp_harness.py
# Reusable command-response bridge for MCP agent communication.
# Instead of creating one-off scripts, the agent writes a request JSON,
# runs this harness via execute_python_script, then reads the response JSON.
#
# Request: Saved/mcp_request.json  -> {"command": "func_name", "args": {...}}
# Response: Saved/mcp_response.json -> {"status": "ok"|"error", "result": ..., "error": ...}
#
# Built-in commands: ping, eval_asset_exists, get_actor_list, get_world_info,
# get_pawn_info, get_blueprint_defaults, run_function.
# Extensible: import and register additional command modules.

import json
import os
import sys
import traceback

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)


def _paths():
    proj = unreal.Paths.project_dir()
    saved = os.path.join(proj, "Saved")
    os.makedirs(saved, exist_ok=True)
    return (
        os.path.join(saved, "mcp_request.json"),
        os.path.join(saved, "mcp_response.json"),
    )


def _write_response(data):
    _, resp_path = _paths()
    with open(resp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)


# ---------------------------------------------------------------------------
# Built-in commands
# ---------------------------------------------------------------------------

def cmd_ping(args):
    return {"message": "pong", "editor_version": str(unreal.SystemLibrary.get_engine_version())}


def cmd_asset_exists(args):
    path = args.get("path", "")
    return {"path": path, "exists": unreal.EditorAssetLibrary.does_asset_exist(path)}


def cmd_get_actors(args):
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        return {"error": "No editor world"}
    class_name = args.get("class", "Actor")
    cls = getattr(unreal, class_name, unreal.Actor)
    actors = unreal.GameplayStatics.get_all_actors_of_class(world, cls)
    result = []
    for a in (actors or []):
        loc = a.get_actor_location()
        result.append({
            "name": a.get_name(),
            "class": a.get_class().get_name(),
            "location": {"x": round(loc.x, 1), "y": round(loc.y, 1), "z": round(loc.z, 1)},
        })
    return {"count": len(result), "actors": result}


def cmd_world_info(args):
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        return {"error": "No editor world"}
    path = world.get_path_name() if hasattr(world, "get_path_name") else "unknown"
    actor_count = len(unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor) or [])
    return {"world_path": path, "actor_count": actor_count}


def cmd_pawn_info(args):
    """Get info about the player pawn in PIE or editor world."""
    source = args.get("source", "pie")
    world = None
    if source == "pie":
        try:
            worlds = unreal.EditorLevelLibrary.get_pie_worlds(include_dedicated_server=False)
            world = worlds[0] if worlds else None
        except Exception:
            pass
    if not world:
        world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        return {"error": "No world available"}

    pc = unreal.GameplayStatics.get_player_controller(world, 0)
    if not pc:
        return {"error": "No PlayerController"}

    pawn = pc.get_controlled_pawn() if hasattr(pc, "get_controlled_pawn") else None
    if not pawn:
        return {"pawn": None, "message": "No controlled pawn"}

    loc = pawn.get_actor_location()
    vel = pawn.get_velocity()
    info = {
        "class": pawn.get_class().get_name(),
        "location": {"x": round(loc.x, 1), "y": round(loc.y, 1), "z": round(loc.z, 1)},
        "velocity": {"x": round(vel.x, 1), "y": round(vel.y, 1), "z": round(vel.z, 1)},
    }

    try:
        move = pawn.character_movement
        if move:
            info["movement_mode"] = str(move.movement_mode)
            info["is_falling"] = move.is_falling()
    except Exception:
        pass

    try:
        mesh = pawn.mesh
        if mesh:
            anim = mesh.get_anim_instance()
            if anim:
                info["anim_instance_class"] = anim.get_class().get_name()
    except Exception:
        pass

    return {"pawn": info}


def cmd_blueprint_defaults(args):
    """Read Class Default Object properties for a Blueprint."""
    bp_path = args.get("path", "")
    if not bp_path or not unreal.EditorAssetLibrary.does_asset_exist(bp_path):
        return {"error": "Blueprint not found: " + bp_path}
    bp = unreal.load_asset(bp_path)
    if not bp:
        return {"error": "Could not load: " + bp_path}

    gen_class = None
    try:
        gen_class = bp.generated_class()
    except Exception:
        try:
            gen_class = bp.get_editor_property("generated_class")
        except Exception:
            pass
    if not gen_class:
        return {"error": "No generated class"}

    cdo = None
    try:
        cdo = unreal.get_default_object(gen_class)
    except Exception:
        pass
    if not cdo:
        return {"error": "No CDO"}

    props = args.get("properties", [])
    result = {"class": gen_class.get_name(), "properties": {}}
    for prop in props:
        try:
            val = cdo.get_editor_property(prop)
            result["properties"][prop] = str(val)
        except Exception as e:
            result["properties"][prop] = "ERROR: " + str(e)
    return result


def cmd_pie_status(args):
    """Check if PIE is running."""
    try:
        subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        return {"is_in_pie": subsys.is_in_play_in_editor()}
    except Exception as e:
        return {"error": str(e)}


def cmd_start_pie(args):
    try:
        subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        if subsys.is_in_play_in_editor():
            return {"already_running": True}
        subsys.editor_request_begin_play()
        return {"requested": True}
    except Exception as e:
        return {"error": str(e)}


def cmd_stop_pie(args):
    try:
        subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        if not subsys.is_in_play_in_editor():
            return {"already_stopped": True}
        subsys.editor_request_end_play()
        return {"stopped": True}
    except Exception as e:
        return {"error": str(e)}


COMMANDS = {
    "ping": cmd_ping,
    "asset_exists": cmd_asset_exists,
    "get_actors": cmd_get_actors,
    "world_info": cmd_world_info,
    "pawn_info": cmd_pawn_info,
    "blueprint_defaults": cmd_blueprint_defaults,
    "pie_status": cmd_pie_status,
    "start_pie": cmd_start_pie,
    "stop_pie": cmd_stop_pie,
}


def main():
    req_path, _ = _paths()
    if not os.path.exists(req_path):
        _write_response({"status": "error", "error": "No request file at " + req_path})
        return

    try:
        with open(req_path, "r", encoding="utf-8") as f:
            request = json.load(f)
    except Exception as e:
        _write_response({"status": "error", "error": "Invalid request JSON: " + str(e)})
        return

    command = request.get("command", "")
    args = request.get("args", {})

    if command not in COMMANDS:
        _write_response({
            "status": "error",
            "error": "Unknown command: " + command,
            "available": list(COMMANDS.keys()),
        })
        return

    try:
        result = COMMANDS[command](args)
        _write_response({"status": "ok", "command": command, "result": result})
    except Exception as e:
        _write_response({
            "status": "error",
            "command": command,
            "error": str(e),
            "traceback": traceback.format_exc(),
        })

    # Clean up request file after processing
    try:
        os.remove(req_path)
    except Exception:
        pass


if __name__ == "__main__":
    main()

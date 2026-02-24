# setup_level.py
# Run from Unreal Editor: Tools -> Execute Python Script.
# Level preparation for the demo:
#   - Ensures a PlayerStart exists (spawns one above the landscape if missing)
#   - Optionally triggers the PCG demo map script

import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)


def _log(msg):
    unreal.log("LevelSetup: " + str(msg))
    print("LevelSetup: " + str(msg))


def _get_landscape_center_z():
    """Return (center_xy Vector, top_z float) from the first Landscape, or None."""
    try:
        world = unreal.EditorLevelLibrary.get_editor_world()
        if not world:
            return None
        landscapes = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Landscape)
        if not landscapes:
            return None
        origin, extent = landscapes[0].get_actor_bounds(False)
        return (origin, origin.z + extent.z)
    except Exception:
        return None


def _ensure_player_start():
    """Spawn a PlayerStart actor if one doesn't already exist in the level."""
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        _log("No editor world open. Open a level first.")
        return

    existing = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.PlayerStart)
    if existing and len(existing) > 0:
        loc = existing[0].get_actor_location()
        _log("PlayerStart already exists at (%.0f, %.0f, %.0f)" % (loc.x, loc.y, loc.z))
        return

    spawn_location = unreal.Vector(0.0, 0.0, 300.0)
    landscape_info = _get_landscape_center_z()
    if landscape_info:
        center, top_z = landscape_info
        spawn_location = unreal.Vector(center.x, center.y, top_z + 200.0)

    rotation = unreal.Rotator(0.0, 0.0, 0.0)
    ps = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PlayerStart, spawn_location, rotation)
    if ps:
        _log("Spawned PlayerStart at (%.0f, %.0f, %.0f)" % (spawn_location.x, spawn_location.y, spawn_location.z))
    else:
        _log("Failed to spawn PlayerStart; add one manually via Place Actors > Basic > Player Start.")


def _run_pcg_demo(run_pcg=True):
    """Optionally run create_demo_map to generate the PCG forest."""
    if not run_pcg:
        return
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
        import create_demo_map
        _log("Running PCG demo map generation...")
        create_demo_map.main()
    except ImportError:
        _log("create_demo_map.py not found; skip PCG generation. Run it separately if needed.")
    except Exception as e:
        _log("PCG demo map error: " + str(e))


def main(run_pcg=False):
    _log("Setting up level...")
    _ensure_player_start()
    if run_pcg:
        _run_pcg_demo(run_pcg=True)
    unreal.EditorLevelLibrary.save_current_level()
    _log("Done. Level saved.")


if __name__ == "__main__":
    main(run_pcg=False)

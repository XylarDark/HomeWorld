# setup_level.py
# Run from Unreal Editor: Tools -> Execute Python Script.
# Level preparation for the demo:
#   - Ensures a PlayerStart exists (spawns one above the landscape if missing)
#   - Ensures basic lighting (Directional Light + Sky Light) so PIE is not black
#   - Optionally triggers the PCG demo map script

import importlib
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


def _ensure_basic_lighting():
    """Spawn a Directional Light and Sky Light if none exist, so PIE is not black."""
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        return

    # Directional Light (sun)
    directional_class = getattr(unreal, "DirectionalLight", None)
    if directional_class:
        existing = unreal.GameplayStatics.get_all_actors_of_class(world, directional_class)
        if not existing or len(existing) == 0:
            loc = unreal.Vector(0.0, 0.0, 0.0)
            rot = unreal.Rotator(-45.0, 0.0, 0.0)  # typical sun angle
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(directional_class, loc, rot)
            if actor:
                _log("Spawned Directional Light.")
            else:
                _log("Could not spawn Directional Light; add one manually (Place Actors > Lights > Directional Light).")
        else:
            _log("Directional Light already exists.")
    else:
        _log("DirectionalLight class not found; add a Directional Light manually (Place Actors > Lights).")

    # Sky Light (ambient)
    sky_class = getattr(unreal, "SkyLight", None)
    if sky_class:
        existing = unreal.GameplayStatics.get_all_actors_of_class(world, sky_class)
        if not existing or len(existing) == 0:
            loc = unreal.Vector(0.0, 0.0, 0.0)
            rot = unreal.Rotator(0.0, 0.0, 0.0)
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(sky_class, loc, rot)
            if actor:
                _log("Spawned Sky Light.")
            else:
                _log("Could not spawn Sky Light; add one manually (Place Actors > Lights > Sky Light).")
        else:
            _log("Sky Light already exists.")
    else:
        _log("SkyLight class not found; add a Sky Light manually (Place Actors > Lights).")


def _run_pcg_demo(run_pcg=True):
    """Optionally run create_demo_from_scratch: ensures DemoMap exists, opens it, sets up PCG volume and graph. See docs/DEMO_MAP.md and docs/PCG_SETUP.md."""
    if not run_pcg:
        return
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
        import create_demo_from_scratch
        importlib.reload(create_demo_from_scratch)
        _log("Running demo map PCG setup...")
        create_demo_from_scratch.main()
    except ImportError:
        _log("create_demo_from_scratch.py not found; skip PCG. Run it separately if needed.")
    except Exception as e:
        _log("PCG demo map setup error: " + str(e))


def main(run_pcg=False):
    _log("Setting up level...")
    _ensure_player_start()
    _ensure_basic_lighting()
    if run_pcg:
        _run_pcg_demo(run_pcg=True)
    unreal.EditorLevelLibrary.save_current_level()
    _log("Done. Level saved.")


if __name__ == "__main__":
    main(run_pcg=False)

# create_pcg_forest.py
# Run from Unreal Editor: Tools -> Execute Python Script.
#
# PCG Fundamental Redo (Option A): Script does NOT create or modify the PCG graph.
# Script only: (1) tags the Landscape with PCG_Landscape so Get Landscape Data (By Tag) can find it,
# (2) creates and scales one PCG Volume to landscape bounds (or config), (3) saves the level.
# You must: create the PCG graph in the Editor (or copy from a reference project), set Get Landscape
# Data to By Tag + PCG_Landscape, assign the graph to the volume, and click Generate.
# See docs/PCG_SETUP.md (or docs/tasks/PCG_MANUAL_SETUP.md) for the full checklist.

import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

# Tag added to the level's Landscape so Get Landscape Data (Actor By Tag) can find it
PCG_LANDSCAPE_TAG = "PCG_Landscape"
VOLUME_HALF_EXTENT_X = 5000.0
VOLUME_HALF_EXTENT_Y = 5000.0
VOLUME_HALF_EXTENT_Z = 500.0


def _log(msg):
    unreal.log("PCG Forest: " + str(msg))
    print("PCG Forest: " + str(msg))


def ensure_landscape_has_pcg_tag():
    """Ensure the level's first Landscape actor has PCG_LANDSCAPE_TAG so Get Landscape Data (Actor By Tag) can find it. Idempotent."""
    try:
        world = unreal.EditorLevelLibrary.get_editor_world()
        if not world:
            return
        landscapes = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Landscape)
        if not landscapes:
            return
        land = landscapes[0]
        tags = land.get_editor_property("tags") if hasattr(land, "get_editor_property") else getattr(land, "tags", None)
        if tags is not None:
            tag_strs = [str(t) for t in tags]
            if PCG_LANDSCAPE_TAG in tag_strs:
                return
            try:
                if hasattr(land, "add_tag"):
                    land.add_tag(PCG_LANDSCAPE_TAG)
                else:
                    tags.append(unreal.Name(PCG_LANDSCAPE_TAG))
                    if hasattr(land, "set_editor_property"):
                        land.set_editor_property("tags", tags)
                _log("Tagged Landscape with '%s' for Get Landscape Data (By Tag)." % PCG_LANDSCAPE_TAG)
            except Exception as e:
                _log("Could not add tag to Landscape: %s" % e)
    except Exception:
        pass


def _find_existing_pcg_volume(world):
    """Return the first non-exclusion PCGVolume in the level, or None."""
    try:
        volumes = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.PCGVolume)
        for vol in (volumes or []):
            try:
                tags = vol.get_editor_property("tags") if hasattr(vol, "get_editor_property") else getattr(vol, "tags", [])
                tag_strs = [str(t) for t in tags] if tags else []
                if "PCG_Exclusion" not in tag_strs:
                    return vol
            except Exception:
                return vol
    except Exception:
        pass
    return None


def place_pcg_volume(location=None, extent=None):
    """Place a PCG Volume in the current level (or reuse existing), size it to extent, save level.
    Does NOT create a graph or assign a graph. You assign the graph in the Editor and click Generate.
    location: unreal.Vector for volume center (default 0,0,0).
    extent: unreal.Vector for half-extents in cm (default VOLUME_HALF_EXTENT_*)."""
    editor_subsystem = unreal.EditorLevelLibrary
    world = editor_subsystem.get_editor_world()
    if not world:
        _log("No editor world. Open a level (e.g. Main) first.")
        return

    if location is None:
        location = unreal.Vector(0.0, 0.0, 0.0)
    if extent is None:
        extent = unreal.Vector(VOLUME_HALF_EXTENT_X, VOLUME_HALF_EXTENT_Y, VOLUME_HALF_EXTENT_Z)

    volume = _find_existing_pcg_volume(world)
    if volume:
        _log("Reusing existing PCG Volume.")
        volume.set_actor_location(location, False, False)
    else:
        rotation = unreal.Rotator(0.0, 0.0, 0.0)
        volume = editor_subsystem.spawn_actor_from_class(unreal.PCGVolume, location, rotation)
        if not volume:
            _log("Failed to spawn PCG Volume.")
            return

    try:
        if hasattr(volume, "set_actor_label"):
            volume.set_actor_label("PCG_Forest")
    except Exception:
        pass

    try:
        volume.set_actor_scale3d(unreal.Vector(1.0, 1.0, 1.0))
        _, base_ext = volume.get_actor_bounds(False)
        if base_ext.x > 0 and base_ext.y > 0 and base_ext.z > 0:
            scale_x = abs(extent.x) / base_ext.x
            scale_y = abs(extent.y) / base_ext.y
            scale_z = abs(extent.z) / base_ext.z
            volume.set_actor_scale3d(unreal.Vector(scale_x, scale_y, scale_z))
            _log("Scaled PCG Volume to extent (%.0f, %.0f, %.0f) cm." % (extent.x, extent.y, extent.z))
        else:
            _log("Default volume extent is zero; set volume bounds manually in Editor.")
    except Exception as e:
        _log("Could not scale volume: %s. Set bounds manually in Details." % str(e))

    editor_subsystem.save_current_level()
    _log("PCG Volume placed and level saved. Assign your PCG graph to the volume in Details and click Generate.")


def try_world_partition():
    """No-op; document manual step if needed."""
    pass

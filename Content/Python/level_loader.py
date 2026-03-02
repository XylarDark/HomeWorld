# level_loader.py
# Shared level loading and "ready" helpers for scripts and Python automation tests.
# Use open_level + wait_for_condition for synchronous scripts; use latent_load_level_and_wait
# inside AutomationScheduler.add_latent_command for tests that need the Editor to tick during load.
# See docs/LEVEL_TESTING_PLAN.md.

import os
import time

try:
    import unreal
except ImportError:
    unreal = None

_diagnostic_logged = False


def _log(msg):
    if unreal:
        unreal.log("Level loader: " + str(msg))


def get_editor_world():
    """Return the editor world; prefer UnrealEditorSubsystem, fallback to EditorLevelLibrary."""
    if not unreal:
        return None
    try:
        subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem) if hasattr(unreal, "get_editor_subsystem") else None
        if subsystem and hasattr(subsystem, "get_editor_world"):
            return subsystem.get_editor_world()
    except Exception:
        pass
    return unreal.EditorLevelLibrary.get_editor_world()


def get_current_level_path():
    """Return the asset path of the current editor level, or None."""
    try:
        world = get_editor_world()
        if not world:
            return None
        path = world.get_path_name() if hasattr(world, "get_path_name") else ""
        if not path or "." not in path:
            return None
        path = path.split(".")[0]
        if ":" in path:
            path = path.split(":")[0]
        out = path if path.startswith("/") else None
        return out
    except Exception as e:
        return None


def _normalize_level_path(level_path):
    """Return a comparable path (strip trailing slash, take last segment for flexible match)."""
    if not level_path:
        return "", ""
    p = level_path.rstrip("/")
    segments = [s for s in p.split("/") if s]
    base = segments[-1].split(".")[0] if segments else ""
    return p, base


def is_level_loaded(level_path):
    """True if the current editor level path matches level_path (normalized comparison)."""
    current = get_current_level_path()
    if not current:
        return False
    _, current_base = _normalize_level_path(current)
    full, target_base = _normalize_level_path(level_path)
    if full and current == full:
        return True
    return current_base == target_base


def open_level(level_path):
    """Open the given level in the Editor. Return True if it is open or was opened successfully."""
    current = get_current_level_path()
    if current and is_level_loaded(level_path):
        return True
    try:
        level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem) if hasattr(unreal, "get_editor_subsystem") else None
        if level_editor and hasattr(level_editor, "load_level"):
            level_editor.load_level(level_path)
            return True
    except Exception as e:
        _log("LevelEditorSubsystem load_level: " + str(e))
    try:
        if hasattr(unreal.EditorLevelLibrary, "load_level"):
            unreal.EditorLevelLibrary.load_level(level_path)
            return True
    except Exception as e:
        _log("Open level failed: " + str(e))
    return False


def wait_for_condition(condition_fn, max_attempts, delay_sec):
    """Poll condition_fn() every delay_sec; return True when it returns True, False after max_attempts."""
    for attempt in range(max_attempts):
        if condition_fn():
            return True
        if attempt < max_attempts - 1:
            time.sleep(delay_sec)
    return False


def _parse_wp_box_to_origin_extent(box):
    """Convert WP bounds box (min/max or center/extent) to (origin, extent) Vectors, or None."""
    if box is None:
        return None
    if hasattr(box, "min") and hasattr(box, "max"):
        min_v, max_v = box.min, box.max
        origin = unreal.Vector(
            (min_v.x + max_v.x) * 0.5,
            (min_v.y + max_v.y) * 0.5,
            (min_v.z + max_v.z) * 0.5,
        )
        extent = unreal.Vector(
            abs(max_v.x - min_v.x) * 0.5,
            abs(max_v.y - min_v.y) * 0.5,
            abs(max_v.z - min_v.z) * 0.5,
        )
        return (origin, extent)
    if hasattr(box, "center") and hasattr(box, "extent"):
        origin = box.center if hasattr(box.center, "x") else unreal.Vector(box.center[0], box.center[1], box.center[2])
        e = box.extent
        extent = e if hasattr(e, "x") else unreal.Vector(e[0], e[1], e[2])
        return (origin, extent)
    return None


def _get_world_partition_bounds(world):
    """Return (origin Vector, box_extent Vector) from World Partition runtime bounds, or None.
    UE 5.7 Python does not expose get_world_partition on World; try Blueprint library first."""
    try:
        if not world:
            _log("WP bounds: world is None.")
            return None
        box = None
        # Try Blueprint library. UE 5.7 Python: get_runtime_world_bounds() takes no args (uses context/current world).
        lib = getattr(unreal, "WorldPartitionBlueprintLibrary", None)
        if lib and hasattr(lib, "get_runtime_world_bounds"):
            try:
                box = lib.get_runtime_world_bounds()
            except Exception as e:
                _log("WP bounds: WorldPartitionBlueprintLibrary.get_runtime_world_bounds failed: %s" % (e,))
        if box is None and lib and hasattr(lib, "get_editor_world_bounds"):
            try:
                box = lib.get_editor_world_bounds()
            except Exception:
                pass
        if box is not None:
            result = _parse_wp_box_to_origin_extent(box)
            if result is not None:
                origin, extent = result
                if extent.x > 0 or extent.y > 0 or extent.z > 0:
                    return result
                _log("WP bounds: extent zero (%.0f, %.0f, %.0f)." % (extent.x, extent.y, extent.z))
            else:
                _log("WP bounds: box format not supported (type=%s)." % type(box).__name__)
            return None
        # Fallback: get WP from world if Python exposes it (e.g. future engine version).
        wp = None
        if hasattr(world, "get_world_partition"):
            try:
                wp = world.get_world_partition()
            except Exception as e:
                _log("WP bounds: get_world_partition() failed: %s" % (e,))
        if wp is None and hasattr(world, "get_editor_property"):
            try:
                wp = world.get_editor_property("world_partition")
            except Exception:
                pass
        if wp is not None and wp:
            if hasattr(wp, "get_runtime_world_bounds"):
                box = wp.get_runtime_world_bounds()
            if box is None and hasattr(wp, "get_editor_world_bounds"):
                try:
                    box = wp.get_editor_world_bounds()
                except Exception:
                    pass
            if box is not None:
                result = _parse_wp_box_to_origin_extent(box)
                if result is not None:
                    origin, extent = result
                    if extent.x > 0 or extent.y > 0 or extent.z > 0:
                        return result
        if box is None:
            _log("WP bounds: could not get bounds (world type=%s, has get_world_partition=%s)." % (type(world).__name__, hasattr(world, "get_world_partition")))
        return None
    except Exception as e:
        _log("World Partition bounds: " + str(e))
        return None


def _get_landscape_bounds_from_components(land):
    """Compute bounds from LandscapeComponent aggregation. Return (origin, box_extent) or None."""
    try:
        comp_class = getattr(unreal, "LandscapeComponent", None)
        if not comp_class:
            return None
        components = land.get_components_by_class(comp_class)
        if not components:
            return None
        min_x = min_y = min_z = float("inf")
        max_x = max_y = max_z = float("-inf")
        for comp in components:
            try:
                if not hasattr(comp, "get_bounds"):
                    continue
                try:
                    bounds = comp.get_bounds(False)
                except TypeError:
                    bounds = comp.get_bounds(False, False)
                if isinstance(bounds, (list, tuple)) and len(bounds) >= 2:
                    o, e = bounds[0], bounds[1]
                elif hasattr(bounds, "origin") and hasattr(bounds, "box_extent"):
                    o, e = bounds.origin, bounds.box_extent
                else:
                    continue
                min_x = min(min_x, o.x - abs(e.x))
                max_x = max(max_x, o.x + abs(e.x))
                min_y = min(min_y, o.y - abs(e.y))
                max_y = max(max_y, o.y + abs(e.y))
                min_z = min(min_z, o.z - abs(e.z))
                max_z = max(max_z, o.z + abs(e.z))
            except Exception:
                continue
        if min_x == float("inf"):
            return None
        origin = unreal.Vector((min_x + max_x) * 0.5, (min_y + max_y) * 0.5, (min_z + max_z) * 0.5)
        box_extent = unreal.Vector((max_x - min_x) * 0.5, (max_y - min_y) * 0.5, (max_z - min_z) * 0.5)
        _log("Landscape bounds from %d LandscapeComponent(s)." % len(components))
        return (origin, box_extent)
    except Exception as e:
        _log("Landscape component bounds: " + str(e))
        return None


def get_landscape_bounds():
    """Return (origin Vector, box_extent Vector) from the first Landscape, or None.
    Uses only landscape data: actor bounds, then LandscapeComponent aggregation. Does not use World Partition
    bounds (so the PCG volume stays landscape-sized when available; when landscape is not loaded we return
    None and callers use config bounds). See docs/PCG_SETUP.md for rationale."""
    global _diagnostic_logged
    if not unreal:
        return None
    try:
        world = get_editor_world()
        if not world:
            if not _diagnostic_logged:
                _log("No editor world.")
                _diagnostic_logged = True
            return None
        landscapes = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Landscape)
        if not landscapes:
            if not _diagnostic_logged:
                _log("No Landscape actors in level.")
                _diagnostic_logged = True
            return None
        land = landscapes[0]
        origin, box_extent = land.get_actor_bounds(False)
        if box_extent.x != 0 or box_extent.y != 0 or box_extent.z != 0:
            return (origin, box_extent)
        bounds = _get_landscape_bounds_from_components(land)
        if bounds is not None:
            return bounds
        comp_class = getattr(unreal, "LandscapeComponent", None)
        comp_count = len(land.get_components_by_class(comp_class)) if comp_class and hasattr(land, "get_components_by_class") else 0
        if not _diagnostic_logged:
            _log("Landscape actor extent (0,0,0), %d LandscapeComponent(s), component_bounds=none. Use Window -> World Partition -> Load All, then re-run to fit volume to landscape." % comp_count)
            _diagnostic_logged = True
        # Diagnostic: what Python sees (helps when WP shows "everything loaded" but we still get 0 components)
        try:
            level_path = get_current_level_path() or ""
            land_path = land.get_path_name() if hasattr(land, "get_path_name") else str(land)
            _log("Landscape diagnostic: level=%s, landscape=%s, origin=(%.0f,%.0f,%.0f), extent=(%.0f,%.0f,%.0f), components=%d" % (
                level_path[:60], land_path[:80] if len(land_path) > 80 else land_path,
                origin.x, origin.y, origin.z, box_extent.x, box_extent.y, box_extent.z, comp_count))
        except Exception:
            pass
        return None
    except Exception as e:
        if not _diagnostic_logged:
            _log("Exception: " + str(e))
            _diagnostic_logged = True
        return None


def get_world_partition_bounds():
    """Return (origin Vector, box_extent Vector) from the current world's World Partition, or None.
    Use when the level uses World Partition and landscape bounds are not yet available (cells not loaded).
    Sizing the PCG volume to WP bounds is a reasonable fallback so the volume covers the level without requiring Load All."""
    if not unreal:
        return None
    world = get_editor_world()
    if not world:
        return None
    return _get_world_partition_bounds(world)


def landscape_has_bounds():
    """True if get_landscape_bounds() returns non-None (used as ready condition)."""
    return get_landscape_bounds() is not None


def level_has_actor_of_class(actor_class):
    """True if the editor world has at least one actor of the given class."""
    if not unreal:
        return False
    world = get_editor_world()
    if not world:
        return False
    actors = unreal.GameplayStatics.get_all_actors_of_class(world, actor_class)
    return bool(actors and len(actors) > 0)


def latent_load_level_and_wait(level_path, ready_condition, max_wait_sec):
    """Generator for use with unreal.AutomationScheduler.add_latent_command.
    Opens the level, then yields each frame until ready_condition() is True or timeout.
    Callers should set latent command timeout (e.g. unreal.PyAutomationTestLibrary.set_latent_command_timeout(max_wait_sec + 15))
    before registering this generator so the test does not hang."""
    open_level(level_path)
    max_attempts = max(1, int(max_wait_sec / 2.0))
    for _ in range(max_attempts):
        if ready_condition():
            return
        yield

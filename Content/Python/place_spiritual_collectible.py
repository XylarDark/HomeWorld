# place_spiritual_collectible.py
# Run from Unreal Editor with target level open (e.g. DemoMap): Tools -> Execute Python Script or via MCP.
# Idempotent: places one AHomeWorldSpiritualCollectible (power) and one AHomeWorldSpiritualArtefact if none present.
# In PIE: set hw.TimeOfDay.Phase 2 (night), walk into each actor to collect; run hw.SpiritualPower or hw.Goods to see both counters.
# See docs/workflow/VISION.md (spiritual artefacts at night); T2 second type + power counter.

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

SPIRITUAL_TAG = "SpiritualCollectible"
ARTEFACT_TAG = "SpiritualArtefact"
DEFAULT_POSITION = [300.0, 0.0, 100.0]
ARTEFACT_POSITION = [450.0, 0.0, 100.0]


def _log(msg):
    unreal.log("Spiritual collectible: " + str(msg))
    print("Spiritual collectible: " + str(msg))


def _get_editor_world():
    if hasattr(unreal, "EditorLevelLibrary"):
        return unreal.EditorLevelLibrary.get_editor_world()
    return None


def _save_current_level():
    try:
        subsys = getattr(unreal, "get_editor_subsystem", None) and unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        if subsys and hasattr(subsys, "save_current_level"):
            subsys.save_current_level()
            return True
    except Exception:
        pass
    if hasattr(unreal, "EditorLevelLibrary") and hasattr(unreal.EditorLevelLibrary, "save_current_level"):
        unreal.EditorLevelLibrary.save_current_level()
        return True
    return False


def _find_existing_by_tag_or_class(world, tag, class_substring):
    """Return True if an actor with tag or class name containing class_substring exists."""
    if not world:
        return False
    try:
        for actor in unreal.EditorLevelLibrary.get_all_level_actors():
            if not actor:
                continue
            tags = getattr(actor, "tags", None) or (actor.get_editor_property("tags") if hasattr(actor, "get_editor_property") else None)
            if tags and tag in [str(t) for t in tags]:
                return True
            try:
                cls_name = actor.get_class().get_name() if hasattr(actor, "get_class") else ""
                if class_substring in cls_name:
                    return True
            except Exception:
                continue
    except Exception as e:
        _log("Could not enumerate actors: " + str(e))
    return False


def _place_and_tag(world, class_path, position, tag, class_substring):
    if _find_existing_by_tag_or_class(world, tag, class_substring):
        _log(class_substring + " already present.")
        return True
    location = unreal.Vector(position[0], position[1], position[2])
    rotation = unreal.Rotator(0, 0, 0)
    try:
        cls = unreal.load_class(None, class_path)
        if not cls:
            _log("Could not load class " + class_path)
            return False
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(cls, location, rotation)
        if not actor:
            return False
        _log("Placed " + class_substring + " at " + str(position))
        tags = getattr(actor, "tags", None) or (actor.get_editor_property("tags") if hasattr(actor, "get_editor_property") else [])
        if tags is None:
            tags = []
        if tag not in [str(t) for t in tags]:
            tags.append(unreal.Name(tag))
            if hasattr(actor, "set_editor_property"):
                actor.set_editor_property("tags", tags)
        return True
    except Exception as e:
        _log("Could not spawn " + class_substring + ": " + str(e))
        return False


def main():
    world = _get_editor_world()
    if not world:
        _log("No editor world. Open a level and run again.")
        return

    placed_power = _place_and_tag(
        world,
        "/Script/HomeWorld.HomeWorldSpiritualCollectible",
        DEFAULT_POSITION,
        SPIRITUAL_TAG,
        "HomeWorldSpiritualCollectible",
    )
    placed_artefact = _place_and_tag(
        world,
        "/Script/HomeWorld.HomeWorldSpiritualArtefact",
        ARTEFACT_POSITION,
        ARTEFACT_TAG,
        "HomeWorldSpiritualArtefact",
    )

    if placed_power or placed_artefact:
        try:
            _save_current_level()
        except Exception as e:
            _log("Failed to save level: " + str(e))

    _log("In PIE: hw.TimeOfDay.Phase 2, overlap each collectible; hw.SpiritualPower or hw.Goods for both counters.")


if __name__ == "__main__":
    main()

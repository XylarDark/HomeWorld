# place_vs_mvp_beast_tame.py
# Idempotent: attach UHomeWorldBeastTameComponent to beast pad actor on L_VS_MVP_Markers.
# Run via MCP execute_python_script or Tools > Execute Python Script.

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
BEAST_PAD_TAGS = ("BeastPad", "SM_BeastPad_01")
TAME_COMPONENT_CLASS = "/Script/HomeWorld.HomeWorldBeastTameComponent"


def _log(msg: str) -> None:
    unreal.log("BeastTame: " + msg)
    print("BeastTame: " + msg)


def _load_level() -> bool:
    if unreal.EditorLoadingAndSavingUtils.load_map(LEVEL_PATH):
        _log("Level loaded: " + LEVEL_PATH)
        return True
    _log("Could not load level: " + LEVEL_PATH)
    return False


def _find_beast_pad_actor(world):
    actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)
    for actor in actors:
        label = actor.get_actor_label() if hasattr(actor, "get_actor_label") else ""
        tags = list(actor.tags) if hasattr(actor, "tags") else []
        tag_names = {str(t) for t in tags}
        if tag_names.intersection(BEAST_PAD_TAGS):
            return actor
        if "BeastPad" in label or "Beast_Pad" in label or "SM_BeastPad" in label:
            return actor
    return None


def _has_tame_component(actor) -> bool:
    tame_class = unreal.load_class(None, TAME_COMPONENT_CLASS)
    if not tame_class:
        return False
    if hasattr(actor, "get_component_by_class"):
        return actor.get_component_by_class(tame_class) is not None
    return False


def main() -> None:
    if not _load_level():
        return
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        _log("No editor world")
        return

    pad = _find_beast_pad_actor(world)
    if not pad:
        _log("No beast pad actor found — spawn SM_BeastPad_01 or tag actor BeastPad")
        return

    if _has_tame_component(pad):
        _log("Reused existing tame component on '" + pad.get_name() + "'")
        return

    tame_class = unreal.load_class(None, TAME_COMPONENT_CLASS)
    if not tame_class:
        _log("HomeWorldBeastTameComponent not found — run Safe-Build first")
        return

    try:
        comp = pad.add_component_by_class(tame_class, False, unreal.Transform(), False)
        if comp:
            pad.modify()
            unreal.EditorLevelLibrary.save_current_level()
            _log("TAME: placed component on '" + pad.get_name() + "'")
        else:
            _log("add_component_by_class returned None")
    except Exception as exc:
        _log("Failed to add component: " + str(exc))


if __name__ == "__main__":
    main()

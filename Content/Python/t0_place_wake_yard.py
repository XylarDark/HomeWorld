"""Place the wake-yard markers in L_VS_MVP_Markers.

Positions are taken from the actor scan in
Docs/level/L_VS_MVP_Markers_manifest.json. Nothing here is a new site.

- NODE_BED sits on GP_PlayerStart. Wake already starts there.
- NPC_PARTNER stands 80 cm beside that bed.
- NODE_GARDEN sits on GP_N1_Crop.
- NPC_CHILD stands 80 cm beside that crop, in the garden.
- NODE_WOUND sits just north of PROTO_SM_Cabin_Prototype's scanned bounds,
  at the yard height of GP_PlayerStart. The valley wisps are not this wound.
- NODE_SHRINE sits on GP_PortalA, the homestead shrine already in the level.

No meshes. The rune is not placed. Re-running updates; it does not duplicate.

After save, rewrite the level manifest so the scan names these actors.
"""

import os
import sys

import unreal

LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"

# Scanned locations, centimetres. Sources are the manifest labels named above.
_PLACEMENTS = (
    ("NODE_BED", unreal.Vector(-240.0, -120.0, 100.0)),
    ("NPC_PARTNER", unreal.Vector(-160.0, -120.0, 100.0)),
    ("NODE_GARDEN", unreal.Vector(-200.0, -350.0, 100.0)),
    ("NPC_CHILD", unreal.Vector(-200.0, -270.0, 100.0)),
    ("NODE_WOUND", unreal.Vector(-200.0, 400.0, 100.0)),
    ("NODE_SHRINE", unreal.Vector(-200.0, -350.0, 0.0)),
)


def _log(message):
    unreal.log("WAKE_YARD: %s" % message)


def _actors():
    return unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


def _level():
    return unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)


def _find(label):
    for actor in _actors().get_all_level_actors():
        try:
            if actor.get_actor_label() == label:
                return actor
        except Exception:
            continue
    return None


def main():
    if not unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        _log("FATAL: %s does not exist" % LEVEL_PATH)
        return 1
    _level().load_level(LEVEL_PATH)

    for label, location in _PLACEMENTS:
        actor = _find(label)
        if actor is None:
            actor = _actors().spawn_actor_from_class(
                unreal.TargetPoint, location, unreal.Rotator()
            )
            if actor is None:
                _log("FATAL: could not spawn %s" % label)
                return 1
            _log("CREATED %s" % label)
        else:
            actor.set_actor_location(location, False, None)
            _log("UPDATED %s" % label)
        actor.set_actor_label(label)
        # Read back. A placeable that does not keep its transform is not placed.
        got = actor.get_actor_location()
        if abs(got.x - location.x) > 1.0 or abs(got.y - location.y) > 1.0 or abs(got.z - location.z) > 1.0:
            _log("FATAL: %s did not keep its transform" % label)
            return 1

    if not _level().save_current_level():
        _log("FATAL: save failed")
        return 1

    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    import level_manifest
    level_manifest.main()
    _log("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

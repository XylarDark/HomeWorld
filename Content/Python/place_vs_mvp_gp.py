# place_vs_mvp_gp.py
# NP-C: GP_PlayerStart TargetPoint + PlayerStart at homestead cabin hub on L_VS_MVP_Markers.
# Idempotent — re-run safe. Run after place_vs_mvp_markers.py.
#
# Docs/03_GAMEPLAY_MVP §8: GP_PlayerStart at cabin path / homestead hub (verb=V1, form=body).

from __future__ import annotations

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("place_vs_mvp_gp: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "place_vs_mvp_gp:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
JSON_REL = os.path.join("AssetCreation", "Exports", "MVP_CRUMB_SPLINE.json")
GP_LABEL = "GP_PlayerStart"
FOLDER = "VS_MVP/Markers"


def _log(msg):
    unreal.log(PREFIX + " " + str(msg))
    print(PREFIX, msg)


def _project_root():
    cwd = os.getcwd()
    if os.path.isdir(cwd) and "Content" in (os.listdir(cwd) or []):
        return cwd
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", ".."))


def blender_to_ue_cm(loc):
    x, y, z = float(loc[0]), float(loc[1]), float(loc[2])
    return unreal.Vector(x * 100.0, -y * 100.0, z * 100.0)


def find_actor_by_label(label):
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        try:
            if actor.get_actor_label() == label:
                return actor
        except Exception:
            continue
    return None


def destroy_labeled(labels):
    label_set = set(labels)
    removed = 0
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        try:
            lbl = actor.get_actor_label()
        except Exception:
            continue
        if lbl in label_set:
            unreal.EditorLevelLibrary.destroy_actor(actor)
            removed += 1
    if removed:
        _log("Removed %d existing GP_PlayerStart marker(s)" % removed)


def compute_spawn_location(data):
    """Homestead hub: between SM_Cabin and path center (Docs/03 §8)."""
    anchors = data.get("anchors") or {}
    cabin = anchors.get("SM_Cabin") or {}
    cabin_loc = cabin.get("location")
    if cabin_loc:
        cabin_ue = blender_to_ue_cm(cabin_loc)
        # Offset toward path center (+X from cabin per graybox)
        return unreal.Vector(cabin_ue.x + 200.0, cabin_ue.y - 50.0, cabin_ue.z + 100.0)

    anchor_actor = find_actor_by_label("ANCHOR_SM_Cabin")
    if anchor_actor:
        loc = anchor_actor.get_actor_location()
        return unreal.Vector(loc.x + 200.0, loc.y - 50.0, loc.z + 100.0)

    _log("Fallback spawn at island hub default (-400, -50, 100)")
    return unreal.Vector(-400.0, -50.0, 100.0)


def spawn_gp_player_start(location):
    rot = unreal.Rotator(0, 90.0, 0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.TargetPoint, location, rot)
    if actor:
        actor.set_actor_label(GP_LABEL)
        actor.set_folder_path(FOLDER)
        actor.tags = [unreal.Name("PlayerStart"), unreal.Name("verb=V1"), unreal.Name("form=body")]
        _log("TargetPoint %s @ %s" % (GP_LABEL, location))
    return actor


def ensure_player_start(location):
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        _log("No editor world")
        return None

    existing = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.PlayerStart)
    rot = unreal.Rotator(0, 90.0, 0)
    if existing:
        ps = existing[0]
        ps.set_actor_location(location, False, True)
        ps.set_actor_rotation(rot, True)
        try:
            ps.set_actor_label("PlayerStart_VS_MVP")
        except Exception:
            pass
        _log("Moved existing PlayerStart to GP_PlayerStart @ %s" % location)
        return ps

    ps = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PlayerStart, location, rot)
    if ps:
        try:
            ps.set_actor_label("PlayerStart_VS_MVP")
        except Exception:
            pass
        _log("Spawned PlayerStart @ %s" % location)
    else:
        _log("Failed to spawn PlayerStart")
    return ps


def main():
    root = _project_root()
    json_path = os.path.join(root, JSON_REL)
    data = {}
    if os.path.isfile(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        _log("JSON not found — using anchor defaults only")

    if unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        unreal.EditorLevelLibrary.load_level(LEVEL_PATH)
        _log("Loaded %s" % LEVEL_PATH)
    else:
        _log("Level missing — run place_vs_mvp_markers.py first")
        return 1

    destroy_labeled([GP_LABEL])
    location = compute_spawn_location(data)
    spawn_gp_player_start(location)
    ensure_player_start(location)

    try:
        unreal.EditorLevelLibrary.save_current_level()
        _log("Saved level")
    except Exception as exc:
        _log("Save warning: %s" % exc)

    _log("Done. PIE spawns at homestead hub; walk toward lookout for V1.")
    return 0


if __name__ == "__main__":
    code = main()
    if code != 0:
        unreal.log_error(PREFIX + " finished with code %s" % code)

# place_fallback_glide_markers.py
# FALLBACK V2: GP_GlideStart + dual shrine portal triggers on L_VS_MVP_Markers (idempotent).
# Run in Unreal Editor (Execute Python Script) or via MCP execute_python_script.
#
# Prerequisite: place_vs_mvp_markers.py (CRUMB_* + ANCHOR_SM_Shrine_* TargetPoints).

from __future__ import annotations

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("place_fallback_glide_markers: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "place_fallback_glide_markers:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
JSON_REL = os.path.join("AssetCreation", "Exports", "MVP_CRUMB_SPLINE.json")

PORTAL_PAIRS = (
    {
        "trigger_label": "GP_PortalA",
        "anchor": "SM_Shrine_Homestead",
        "destination": "ANCHOR_SM_Shrine_Return",
        "folder": "VS_MVP/Portal",
    },
    {
        "trigger_label": "GP_PortalB",
        "anchor": "SM_Shrine_Return",
        "destination": "ANCHOR_SM_Shrine_Homestead",
        "folder": "VS_MVP/Portal",
    },
)

GLIDE_START = {
    "label": "GP_GlideStart",
    "fallback_crumb": "CRUMB_Depart_Lookout",
    "folder": "VS_MVP/Markers",
}


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
        _log("Removed %d existing actors for re-run" % removed)


def spawn_target_point(label, location, folder):
    rot = unreal.Rotator(0, 0, 0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.TargetPoint, location, rot)
    if actor:
        actor.set_actor_label(label)
        actor.set_folder_path(folder)
        _log("TargetPoint %s @ %s" % (label, location))
    return actor


def spawn_portal_trigger(label, location, destination_label, folder):
    portal_class = None
    try:
        portal_class = unreal.load_class(None, "/Script/HomeWorld.HomeWorldShrinePortalTrigger")
    except Exception:
        portal_class = getattr(unreal, "HomeWorldShrinePortalTrigger", None)

    if not portal_class:
        _log("HomeWorldShrinePortalTrigger C++ not loaded — build Safe-Build first; skipped %s" % label)
        return spawn_target_point(label, location, folder)

    rot = unreal.Rotator(0, 0, 0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(portal_class, location, rot)
    if not actor:
        _log("Failed to spawn portal trigger %s" % label)
        return None

    actor.set_actor_label(label)
    actor.set_folder_path(folder)

    portal_comp = actor.get_component_by_class(unreal.HomeWorldShrinePortalComponent)
    if portal_comp:
        portal_comp.set_editor_property("DestinationLabel", unreal.Name(destination_label))
        portal_comp.set_editor_property("bRequireNight", False)
        _log("Portal trigger %s -> %s (bRequireNight=false)" % (label, destination_label))
    else:
        _log("Portal trigger %s spawned without component reference" % label)
    return actor


def load_anchor_locations(data):
    anchors = data.get("anchors") or {}
    out = {}
    for name, item in anchors.items():
        if isinstance(item, dict) and item.get("location"):
            out[name] = item["location"]
    return out


def main():
    root = _project_root()
    json_path = os.path.join(root, JSON_REL)
    if not os.path.isfile(json_path):
        _log("JSON not found: %s" % json_path)
        return 1

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        unreal.EditorLevelLibrary.load_level(LEVEL_PATH)
        _log("Loaded %s" % LEVEL_PATH)
    else:
        _log("Level missing — run place_vs_mvp_markers.py first")
        return 1

    labels = [GLIDE_START["label"]] + [p["trigger_label"] for p in PORTAL_PAIRS]
    destroy_labeled(labels)

    anchors = load_anchor_locations(data)

    # GP_GlideStart at glider perch / depart crumb
    glide_loc = None
    depart = find_actor_by_label(GLIDE_START["fallback_crumb"])
    if depart:
        glide_loc = depart.get_actor_location()
        _log("GP_GlideStart using existing %s location" % GLIDE_START["fallback_crumb"])
    elif "SM_Glider_Perch" in anchors:
        glide_loc = blender_to_ue_cm(anchors["SM_Glider_Perch"])
        glide_loc.z += 150.0
    if glide_loc:
        spawn_target_point(GLIDE_START["label"], glide_loc, GLIDE_START["folder"])
    else:
        _log("Skipped GP_GlideStart — no CRUMB_Depart_Lookout or SM_Glider_Perch anchor")

    for pair in PORTAL_PAIRS:
        anchor_name = pair["anchor"]
        loc = None
        anchor_actor = find_actor_by_label("ANCHOR_" + anchor_name)
        if anchor_actor:
            loc = anchor_actor.get_actor_location()
        elif anchor_name in anchors:
            loc = blender_to_ue_cm(anchors[anchor_name])
        if loc:
            spawn_portal_trigger(
                pair["trigger_label"],
                loc,
                pair["destination"],
                pair["folder"],
            )
        else:
            _log("Skipped %s — anchor %s not found" % (pair["trigger_label"], anchor_name))

    try:
        unreal.EditorLevelLibrary.save_current_level()
        _log("Saved level")
    except Exception as exc:
        _log("Save warning: %s" % exc)

    _log("Done. FALLBACK: Interact (E) near GP_GlideStart starts CRUMB glide; walk into GP_Portal* for shrine transit.")
    return 0


if __name__ == "__main__":
    code = main()
    if code != 0:
        unreal.log_error(PREFIX + " finished with code %s" % code)

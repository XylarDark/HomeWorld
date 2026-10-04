# measure_ue_island.py
# Writes Docs/qa/UE_ISLAND_MEASUREMENT.json: how big the island actually is inside
# Unreal, in the units Unreal uses.
#
# WHY THIS EXISTS. On 2026-10-04 the island plate was applied and verified in
# blender/floating_island_homestead_LIB.blend - 180.0 x 100.0 x 0.45 m - and the
# readiness gate went green on env.island_sized. The FBX Unreal consumes still
# measured 19.3 x 10.7, exported on 2026-09-16, and the .uasset imported from it
# on 2026-09-28. Every gate row was reading the Blender source of truth and none
# read the artefact the game is built from. A player would have stood on a 19 m
# island while the report said 180 m.
#
# That is a measurement gap, not a discipline problem, so this closes it by
# measuring the far end. The gate's env.ue_island_measured row reads what this
# writes and compares it against the Blender side.
#
# RUN: inside the Unreal Editor, with the target level open.
#   Scripting workspace -> open this file -> Run Script
#   or via MCP: execute_python_script("measure_ue_island.py")
#
# It only reads. It spawns nothing, moves nothing and saves no level. Re-running
# it after a re-import is the intended workflow:
#
#   1. blender --background blender/floating_island_homestead_LIB.blend \
#           --python AssetCreation/Blender/apply_island_plate.py
#   2. export SM_IslandTop -> AssetCreation/Exports/Homestead/SM_IslandTop.fbx
#   3. in-editor: re-import the FBX over the existing SM_IslandTop asset
#   4. in-editor: re-place the island actor if its transform changed
#   5. in-editor: run this script, then commit the JSON it writes
#
# Step 5 is the one that used to be skipped, and skipping it is how the plate went
# missing for a day without anything going red.

from __future__ import annotations

import datetime
import json
import os
import sys

try:
    import unreal
except ImportError:
    print("measure_ue_island: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "measure_ue_island:"
ASSET_NAME = "SM_IslandTop"
OUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "Docs", "qa", "UE_ISLAND_MEASUREMENT.json")

#: How many actors to report before truncating. A misnamed asset can match a lot
#: of things and a truncated list is better than a silent one.
MAX_REPORTED = 12


def _log(message, data=None):
    line = PREFIX + " " + str(message)
    if data is not None:
        line += " " + str(data)
    unreal.log(line)
    print(line)


def find_mesh_actors():
    """Every actor whose mesh is the island asset, with its world bounds in cm.

    Uses get_actor_bounds rather than reading the StaticMesh's own Bounds, because
    the question is how big the island is *in the level*, which includes any
    actor-level scale. In UE 5.8 this returns a tuple.
    """
    found = []
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        try:
            mesh = actor.static_mesh
        except Exception:
            continue
        if mesh is None:
            continue
        if mesh.get_name() != ASSET_NAME:
            continue
        try:
            origin, extent = actor.get_actor_bounds(False)
        except Exception as exc:                      # noqa: BLE001
            _log("get_actor_bounds failed", "%s: %s" % (actor.get_name(), exc))
            continue
        xs = (float(origin.x) - float(extent.x),
              float(origin.x) + float(extent.x))
        ys = (float(origin.y) - float(extent.y),
              float(origin.y) + float(extent.y))
        zs = (float(origin.z) - float(extent.z),
              float(origin.z) + float(extent.z))
        found.append({
            "actor": actor.get_name(),
            "label": actor.get_actor_label(),
            "bbox_cm": [xs[1] - xs[0], ys[1] - ys[0], zs[1] - zs[0]],
            "origin_cm": [float(origin.x), float(origin.y), float(origin.z)],
            "scale": [float(v) for v in actor.get_actor_scale3d()],
        })
    return found


def main():
    level = unreal.EditorLevelLibrary.get_editor_world().get_name()
    _log("level", level)

    hits = find_mesh_actors()
    if not hits:
        # Writing the file with no bbox_cm is deliberate. The gate then reads
        # MISSING and names the asset, instead of the row quietly disappearing
        # because there was nothing to report.
        _log("no actor uses %s - writing an empty record so the gate says so"
             % ASSET_NAME)
        payload = {
            "measured_at": datetime.datetime.now(datetime.timezone.utc)
                           .isoformat(timespec="seconds"),
            "level": level,
            "asset": ASSET_NAME,
            "actors_found": 0,
            "bbox_cm": None,
            "note": "No level actor uses a mesh named %s. Either the asset is not "
                    "imported, or the island is placed under a different mesh." % ASSET_NAME,
        }
    else:
        hits.sort(key=lambda h: -(h["bbox_cm"][0] * h["bbox_cm"][1]))
        largest = hits[0]
        _log("actors found", len(hits))
        for hit in hits[:MAX_REPORTED]:
            _log("  %-40s bbox_cm=[%.1f %.1f %.1f]"
                 % (hit["label"], hit["bbox_cm"][0], hit["bbox_cm"][1], hit["bbox_cm"][2]))
        if len(hits) > MAX_REPORTED:
            _log("  ... and %d more" % (len(hits) - MAX_REPORTED))
        if len(hits) > 1:
            _log("WARNING more than one actor uses this mesh. The gate compares "
                 "the largest. Two islands in one level is probably not intended; "
                 "if it is, say so in the record's note.")
        payload = {
            "measured_at": datetime.datetime.now(datetime.timezone.utc)
                           .isoformat(timespec="seconds"),
            "level": level,
            "asset": ASSET_NAME,
            "actors_found": len(hits),
            "bbox_cm": largest["bbox_cm"],
            "largest_actor": largest["label"],
            "actors": hits[:MAX_REPORTED],
        }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    _log("wrote %s" % OUT_PATH)
    _log("bbox_cm=%s" % (payload.get("bbox_cm"),))
    _log("Commit this file. It is the only evidence the engine has the plate.")


main()

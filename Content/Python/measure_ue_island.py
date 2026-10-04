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
#
# TWO THINGS THIS FILE GETS RIGHT THAT THE FIRST DRAFT DID NOT. Both were caught
# reviewing it before it ever ran, which is the only reason they were cheap:
#
#   * It measures the MESH's local bounds, not the actor's world AABB. Blender
#     reports object-space dimensions; `get_actor_bounds` returns a world-space
#     box. Comparing those two means the row fails on any rotated island - the
#     check would have been wrong by construction rather than by tolerance. The
#     world box is still recorded, but as information, and actor scale is
#     checked separately and exactly.
#   * It never destroys the skeleton. The first draft opened the output with "w"
#     and wrote only its own keys, so the first person who did everything right
#     deleted the explanation of what the file is - including the 19.3 x 10.7
#     diagnosis. Keys starting with "_" are documentation and are preserved.

from __future__ import annotations

import datetime
import json
import os
import sys
import traceback

try:
    import unreal
except ImportError:
    print("measure_ue_island: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "measure_ue_island:"
ASSET_NAME = "SM_IslandTop"

#: The level a player actually stands in. A measurement taken in any other level
#: - a blockout sandbox, an empty test map - describes a scene nobody ships, and
#: the gate row rejects it rather than reporting on it.
SHIPPING_LEVEL = "L_VS_MVP_Markers"

#: How many actors to report before truncating. A misnamed asset can match a lot
#: of things and a truncated list is better than a silent one. `actors_found`
#: always carries the true count, so truncation cannot hide a total.
MAX_REPORTED = 12


def _project_dir():
    """Repo root, without assuming `__file__` exists.

    Via MCP `execute_python_script` there may be no `__file__`, and the first
    draft built its output path from it. Falling back to the project directory
    keeps the script runnable by every route it documents.
    """
    try:
        return os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
    except NameError:
        return unreal.Paths.convert_relative_path_to_full(
            unreal.Paths.project_dir())


OUT_PATH = os.path.join(_project_dir(), "Docs", "qa",
                        "UE_ISLAND_MEASUREMENT.json")


def _log(message, data=None):
    line = PREFIX + " " + str(message)
    if data is not None:
        line += " " + str(data)
    unreal.log(line)
    print(line)


def _actor_subsystem():
    """EditorActorSubsystem, falling back to the deprecated LevelLibrary.

    `EditorLevelLibrary` is deprecated in UE5 and slated for removal; using it
    is the kind of thing that works today and fails on an engine upgrade. The
    fallback stays because a 5.8 install can still be missing the subsystem on a
    headless commandlet, and a read-only measurement should never be the thing
    that breaks.
    """
    try:
        return unreal.get_editor_subsystem(unreal.EditorActorSubsystem), True
    except Exception:                                      # noqa: BLE001
        return unreal.EditorLevelLibrary, False


def _all_level_actors():
    subsystem, modern = _actor_subsystem()
    if modern:
        return list(subsystem.get_all_level_actors())
    return list(subsystem.get_all_level_actors())


def _editor_level_name():
    """The open level's name, or None rather than an exception.

    `get_editor_world()` returns None outside a normal world context - during
    startup, in a blueprint macro context, with no map open. The first draft
    called `.get_name()` on it unguarded, so it raised before the file was ever
    written. The gate then kept reading MISSING with no record that an attempt
    had even happened, which is the worst possible outcome: a silent failure
    that looks exactly like nobody having tried.
    """
    subsystem, modern = _actor_subsystem()
    try:
        if modern:
            world = subsystem.get_editor_world()
        else:
            world = subsystem.get_editor_world()
    except Exception as exc:                              # noqa: BLE001
        _log("could not read the editor world", exc)
        return None
    if world is None:
        return None
    try:
        return world.get_name()
    except Exception as exc:                              # noqa: BLE001
        _log("editor world has no name", exc)
        return None


def _mesh_local_bbox_cm(mesh):
    """(x, y, z) dimensions of the mesh itself, in cm.

    This is the quantity comparable to Blender's object-space `bbox`. For a
    rotated or non-uniformly scaled actor it differs from the world AABB, which
    is exactly why it is the thing the gate compares.
    """
    bounds = mesh.get_bounds()
    extent = bounds.box_extent
    return [abs(float(extent.x)) * 2.0,
            abs(float(extent.y)) * 2.0,
            abs(float(extent.z)) * 2.0]


def find_mesh_actors():
    """Every actor whose mesh is the island asset, with local and world bounds.

    Three things are recorded per hit because each answers a different failure:

    `local_bbox_cm`  the mesh itself - catches the wrong asset being imported.
                    This is what the gate compares against Blender.
    `bbox_cm`        the world AABB - reported for context only.
    `scale`          actor scale - checked exactly, because a correct mesh at
                    0.1 scale is still a 19 m island to a player.

    Actors without a `static_mesh` attribute are counted, not silently skipped:
    the first draft swallowed the AttributeError in a bare `except: continue`,
    so a blueprint-wrapped island vanished from the report and the gate read
    MISSING with nothing in the log to say why.
    """
    found = []
    skipped = 0
    for actor in _all_level_actors():
        try:
            mesh = actor.static_mesh
        except AttributeError:
            skipped += 1
            continue
        except Exception as exc:                          # noqa: BLE001
            _log("skipping actor we could not query", "%s: %s"
                 % (actor.get_name(), exc))
            skipped += 1
            continue
        if mesh is None:
            continue
        # Accept a re-import that produced a numbered duplicate (SM_IslandTop_2).
        # Exact-match-only meant the most likely post-re-import state produced an
        # empty report rather than an obviously duplicated one.
        mesh_name = mesh.get_name()
        if mesh_name != ASSET_NAME and not mesh_name.startswith(ASSET_NAME + "_"):
            continue
        try:
            origin, extent = actor.get_actor_bounds(False)
        except Exception as exc:                          # noqa: BLE001
            _log("get_actor_bounds failed", "%s: %s" % (actor.get_name(), exc))
            continue
        try:
            local = _mesh_local_bbox_cm(mesh)
        except Exception as exc:                          # noqa: BLE001
            _log("could not read mesh bounds", "%s: %s" % (actor.get_name(), exc))
            continue
        world = [float(extent.x) * 2.0, float(extent.y) * 2.0,
                 float(extent.z) * 2.0]
        found.append({
            "actor": actor.get_name(),
            "label": actor.get_actor_label(),
            "mesh": mesh_name,
            "local_bbox_cm": local,
            "bbox_cm": world,
            "origin_cm": [float(origin.x), float(origin.y), float(origin.z)],
            "scale": [float(v) for v in actor.get_actor_scale3d()],
        })
    if skipped:
        _log("%d actor(s) skipped: no static_mesh property" % skipped)
    return found


def _write(payload):
    """Write the record, preserving any `_`-prefixed documentation keys.

    The skeleton in the repo explains what the file is and what a 19.3 x 10.7
    reading means. The first draft overwrote it with mode "w" and its own keys,
    so following the documented workflow destroyed the documentation.
    """
    existing = {}
    if os.path.isfile(OUT_PATH):
        try:
            with open(OUT_PATH, "r", encoding="utf-8") as handle:
                loaded = json.load(handle)
            if isinstance(loaded, dict):
                existing = loaded
        except (OSError, ValueError):
            existing = {}

    merged = {k: v for k, v in existing.items() if k.startswith("_")}
    merged.update(payload)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    tmp = OUT_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(merged, handle, indent=2, sort_keys=False,
                  allow_nan=False)
        handle.write("\n")
    os.replace(tmp, OUT_PATH)
    return merged


def _now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(
        timespec="seconds")


def main():
    level = _editor_level_name()
    if level is None:
        # Write the failure. An absent record and a record saying "I tried and
        # could not" are different facts and only one of them is diagnosable.
        _log("no editor world - recording the failure rather than raising")
        _write({
            "measured_at": _now(),
            "level": None,
            "asset": ASSET_NAME,
            "actors_found": 0,
            "local_bbox_cm": None,
            "bbox_cm": None,
            "_status": "FAILED",
            "note": "get_editor_world() returned None. Open a level in the "
                    "editor and run this again - typically means no map is "
                    "open, or this ran outside a normal editor world context.",
        })
        return 1

    _log("level", level)
    if level != SHIPPING_LEVEL:
        _log("WARNING this is not the shipping level (%s). The gate row rejects "
             "a measurement from any other level, so the record will read "
             "MISSING until you run it in %s." % (SHIPPING_LEVEL,
                                                   SHIPPING_LEVEL))

    hits = find_mesh_actors()
    common = {"measured_at": _now(), "level": level, "asset": ASSET_NAME}

    if not hits:
        # Writing the file with no measurement is deliberate. The gate then
        # reads MISSING and names the asset, instead of the row quietly
        # disappearing because there was nothing to report.
        _log("no actor uses %s - writing an empty record so the gate says so"
             % ASSET_NAME)
        _write(dict(common, actors_found=0, local_bbox_cm=None, bbox_cm=None,
                    note="No level actor uses a mesh named %s. Either the asset "
                         "is not imported, or the island is placed under a "
                         "different mesh." % ASSET_NAME))
        return 0

    # Largest by mesh footprint, not by world AABB. Ranking on the world box
    # would let a stray scaled-up actor outrank the real island.
    hits.sort(key=lambda h: -(h["local_bbox_cm"][0] * h["local_bbox_cm"][1]))
    largest = hits[0]
    _log("actors found", len(hits))
    for hit in hits[:MAX_REPORTED]:
        _log("  %-40s local_cm=[%.1f %.1f %.1f] world_cm=[%.1f %.1f %.1f]"
             % (hit["label"], hit["local_bbox_cm"][0], hit["local_bbox_cm"][1],
                hit["local_bbox_cm"][2], hit["bbox_cm"][0], hit["bbox_cm"][1],
                hit["bbox_cm"][2]))
    if len(hits) > MAX_REPORTED:
        _log("  ... and %d more" % (len(hits) - MAX_REPORTED))
    if len(hits) > 1:
        _log("WARNING more than one actor uses this mesh. The gate compares "
             "the largest by mesh footprint. Two islands in one level is "
             "probably not intended; if it is, say so in the record's note.")

    scaled = [h for h in hits
              if any(abs(v - 1.0) > 1e-4 for v in h["scale"])]
    if scaled:
        _log("WARNING %d actor(s) have non-unit scale: %s. The mesh may be "
             "correct while the island in the level is not."
             % (len(scaled), ", ".join(h["label"] for h in scaled)))

    meshes = sorted({h["mesh"] for h in hits})
    if len(meshes) > 1 or meshes[0] != ASSET_NAME:
        _log("WARNING mesh name(s) matched: %s. A re-import that created a "
             "numbered duplicate leaves two assets in the project." % meshes)

    _write(dict(
        common,
        actors_found=len(hits),
        local_bbox_cm=largest["local_bbox_cm"],
        bbox_cm=largest["bbox_cm"],
        largest_actor=largest["label"],
        matched_meshes=meshes,
        non_unit_scale_actors=[h["label"] for h in scaled],
        actors=hits[:MAX_REPORTED],
        _status="MEASURED",
    ))
    _log("wrote %s" % OUT_PATH)
    _log("local_bbox_cm=%s  world_bbox_cm=%s"
         % (largest["local_bbox_cm"], largest["bbox_cm"]))
    _log("Commit this file. It is the only evidence the engine has the plate.")
    return 0


try:
    main()
except Exception:                                         # noqa: BLE001
    # Any unexpected failure still leaves a record. A script that dies before
    # writing is indistinguishable from one nobody ran.
    _log("FAILED", traceback.format_exc())
    try:
        _write({
            "measured_at": _now(),
            "level": None,
            "asset": ASSET_NAME,
            "actors_found": 0,
            "local_bbox_cm": None,
            "bbox_cm": None,
            "_status": "FAILED",
            "note": "Unhandled exception; see the editor log for "
                    "measure_ue_island. Full traceback: " +
                    traceback.format_exc().replace("\n", " | "),
        })
    except Exception:                                     # noqa: BLE001
        _log("could not even write the failure record",
             traceback.format_exc())
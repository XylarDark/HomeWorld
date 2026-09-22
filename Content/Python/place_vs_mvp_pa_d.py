# place_vs_mvp_pa_d.py
# PA-D: Idempotent Homestead kit dress (cliffs, garden, path) + refresh core DRESS_* anchors.
# Run in Unreal Editor or via MCP execute_python_script("place_vs_mvp_pa_d.py").
# Prerequisites: batch_import_asset_creation.py, place_vs_mvp_markers.py on Windows host.

from __future__ import annotations

import importlib
import os
import sys

try:
    import unreal
except ImportError:
    print("place_vs_mvp_pa_d: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "place_vs_mvp_pa_d:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
PA_D_FOLDER = "VS_MVP/PA_D"
PA_D_LABEL_PREFIX = "PA_D_"

# Graybox cliff faces (Blender m) — Lib/01_Homestead/SM_Cliff.json
CLIFF_SPECS = (
    ("SM_Cliff_LookoutFace", (7.5, -5.5, -4.0)),
    ("SM_Cliff_CabinFace", (-7.0, -4.5, -3.0)),
    ("SM_Cliff_Rear", (0.0, 5.0, -2.5)),
)

# Garden center — Lib/01_Homestead/GARDEN_BLOCKING.md
GARDEN_CENTER_BL = (-3.5, 0.5, 0.0)
PLANTER_SPECS = (
    ("SM_Planter_A", (-4.1, 0.5, 0.0)),
    ("SM_Planter_B", (-3.5, 0.5, 0.0)),
    ("SM_Planter_C", (-2.9, 0.5, 0.0)),
)

# Low rail segments around ~4 × 2.5 m garden envelope (Blender m)
FENCE_SEGMENTS_BL = (
    (-5.5, 0.5, 0.0),
    (-3.5, 1.75, 0.0),
    (-1.5, 0.5, 0.0),
    (-3.5, -0.75, 0.0),
    (-4.5, 1.25, 0.0),
)

PATH_START_BL = (-6.0, 1.0, 0.0)
PATH_END_BL = (7.0, -3.5, 0.0)
PATH_STONE_NAMES = ("SM_PathStone_A", "SM_PathStone_B", "SM_PathStone_C")


def _log(msg, data=None):
    line = PREFIX + " " + str(msg)
    if data is not None:
        line += " " + str(data)
    unreal.log(line)
    print(line)


def blender_to_ue_cm(loc):
    x, y, z = float(loc[0]), float(loc[1]), float(loc[2])
    return unreal.Vector(x * 100.0, -y * 100.0, z * 100.0)


def destroy_existing_pa_d():
    to_destroy = []
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        try:
            label = actor.get_actor_label()
        except Exception:
            label = ""
        folder = ""
        try:
            folder = str(actor.get_folder_path())
        except Exception:
            pass
        if label.startswith(PA_D_LABEL_PREFIX) or folder.replace("\\", "/") == PA_D_FOLDER:
            to_destroy.append(actor)
    for actor in to_destroy:
        unreal.EditorLevelLibrary.destroy_actor(actor)
    if to_destroy:
        _log("Removed existing PA-D actors", {"count": len(to_destroy)})
    return len(to_destroy)


def spawn_pa_d_actor(mesh_name, static_mesh, location_blender):
    loc = blender_to_ue_cm(location_blender)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc, unreal.Rotator(0, 0, 0))
    if not actor:
        _log("Spawn failed", {"mesh": mesh_name})
        return None
    sm_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
    if sm_comp and static_mesh:
        sm_comp.set_static_mesh(static_mesh)
    actor.set_actor_label(PA_D_LABEL_PREFIX + mesh_name)
    actor.set_folder_path(PA_D_FOLDER)
    return actor


def _lerp_bl(a, b, t):
    return (
        a[0] + (b[0] - a[0]) * t,
        a[1] + (b[1] - a[1]) * t,
        a[2] + (b[2] - a[2]) * t,
    )


def sample_path_points(count=5):
    count = max(2, int(count))
    points = []
    for i in range(count):
        t = i / float(count - 1)
        points.append(_lerp_bl(PATH_START_BL, PATH_END_BL, t))
    return points


def place_exact_mesh(mesh_index, mesh_name, location_blender, counts, optional=False):
    entry = mesh_index.get(mesh_name)
    if not entry:
        if optional:
            _log("Optional mesh missing (skip)", {"mesh": mesh_name})
        else:
            _log("Mesh missing", {"mesh": mesh_name})
        return 0
    _path, mesh = entry
    if spawn_pa_d_actor(mesh_name, mesh, location_blender):
        counts["spawned"] = counts.get("spawned", 0) + 1
        if mesh_name.startswith("SM_Cliff"):
            counts["cliffs"] = counts.get("cliffs", 0) + 1
        elif mesh_name.startswith("SM_Planter"):
            counts["planters"] = counts.get("planters", 0) + 1
        elif mesh_name.startswith("SM_Garden_Fence"):
            counts["fence"] = counts.get("fence", 0) + 1
        elif mesh_name.startswith("SM_PathStone"):
            counts["path_stones"] = counts.get("path_stones", 0) + 1
        return 1
    return 0


def ensure_level():
    import place_vs_mvp_markers

    importlib.reload(place_vs_mvp_markers)
    place_vs_mvp_markers.create_or_load_level()
    return True


def run_dress_refresh():
    import place_vs_mvp_dress as dress

    importlib.reload(dress)
    _log("Refreshing DRESS_* kit via place_vs_mvp_dress")
    dress.main()


def main():
    _log("Start PA-D Homestead place")
    ensure_level()
    removed = destroy_existing_pa_d()

    import place_vs_mvp_dress as dress

    importlib.reload(dress)
    mesh_index = dress.build_mesh_index()
    counts = {"removed_pa_d": removed, "spawned": 0, "cliffs": 0, "planters": 0, "fence": 0, "path_stones": 0}

    for mesh_name, loc in CLIFF_SPECS:
        place_exact_mesh(mesh_index, mesh_name, loc, counts, optional=False)

    for mesh_name, loc in PLANTER_SPECS:
        place_exact_mesh(mesh_index, mesh_name, loc, counts, optional=True)

    fence_mesh = "SM_Garden_Fence_Seg"
    if mesh_index.get(fence_mesh):
        for idx, loc in enumerate(FENCE_SEGMENTS_BL):
            label = fence_mesh if idx == 0 else fence_mesh + "_" + str(idx + 1)
            entry = mesh_index.get(fence_mesh)
            if entry and spawn_pa_d_actor(label, entry[1], loc):
                counts["spawned"] = counts.get("spawned", 0) + 1
                counts["fence"] = counts.get("fence", 0) + 1
    else:
        _log("Optional mesh missing (skip)", {"mesh": fence_mesh})

    path_points = sample_path_points(5)
    for i, loc in enumerate(path_points):
        stone_name = PATH_STONE_NAMES[i % len(PATH_STONE_NAMES)]
        place_exact_mesh(mesh_index, stone_name, loc, counts, optional=True)

    run_dress_refresh()

    try:
        unreal.EditorLevelLibrary.save_current_level()
        _log("Saved current level", {"path": LEVEL_PATH})
    except Exception as exc:
        _log("Save level warning", {"error": str(exc)})

    _log("Done", counts)
    return 0


if __name__ == "__main__":
    code = main()
    if code != 0:
        unreal.log_error(PREFIX + " finished with code %s" % code)

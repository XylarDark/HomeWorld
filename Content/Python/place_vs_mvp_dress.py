# place_vs_mvp_dress.py
# Docs/06: Idempotent kit dress for L_VS_MVP_Markers from imported StaticMeshes + MVP_CRUMB_SPLINE.json.
# Run in Unreal Editor (Execute Python Script) or via MCP execute_python_script("place_vs_mvp_dress.py").
# Prerequisites: batch_import_asset_creation.py + place_vs_mvp_markers.py on Windows host.

from __future__ import annotations

import importlib
import json
import os
import sys

try:
    import unreal
except ImportError:
    print("place_vs_mvp_dress: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "place_vs_mvp_dress:"
JSON_REL = os.path.join("AssetCreation", "Exports", "MVP_CRUMB_SPLINE.json")
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
DRESS_FOLDER = "VS_MVP/Dress"
DRESS_LABEL_PREFIX = "DRESS_"

MESH_ROOTS = (
    "/Game/HomeWorld/Meshes/Homestead",
    "/Game/HomeWorld/Meshes/Forest",
    "/Game/HomeWorld/Meshes/Gatherables",
    "/Game/HomeWorld/Meshes/Transit",
)

# anchor_key -> mesh prefix (spawn all matching StaticMeshes except UCX_/M_)
ANCHOR_MESH_RULES = (
    ("SM_IslandTop", "SM_IslandTop"),
    ("SM_Cabin", "SM_Cabin_"),
    ("SM_Lookout_Pad", "SM_Lookout_Pad"),
    ("SM_Glider_Perch", "SM_Glider_Perch"),
    ("SM_Shrine_Homestead", "SM_Shrine_Homestead_"),
    ("SM_LandingCircle", "SM_LandingCircle_"),
    ("SM_Shrine_Return", "SM_Shrine_Return_"),
)

# crumb name -> islet mesh prefix
ISLET_RULES = (
    ("CRUMB_Islet_01", "SM_Islet_01_"),
    ("CRUMB_Islet_02", "SM_Islet_02_"),
    ("CRUMB_Islet_03", "SM_Islet_03_"),
)

# (anchor_key, mesh_prefix, blender_offset_xyz, optional)
EXTRA_RULES = (
    ("SM_LandingCircle", "SM_Planet_GroundPlate", (0.0, 0.0, 0.0), False),
    ("SM_LandingCircle", "SM_Gather_FirstHarvest_Bush_", (2.0, 0.0, 0.0), False),
    ("SM_Shrine_Return", "SM_Roof_Hamlet_01", (0.0, 0.0, 0.0), False),
    ("SM_Shrine_Return", "SM_Roof_Hamlet_02", (2.0, 0.0, 0.0), False),
    ("SM_Shrine_Return", "SM_Roof_Hamlet_03", (-2.0, 0.0, 0.0), False),
    ("SM_Cabin", "SM_Pine_Homestead_M_", (0.0, 3.0, 0.0), True),
)


def _log(msg, data=None):
    line = PREFIX + " " + str(msg)
    if data is not None:
        line += " " + str(data)
    unreal.log(line)
    print(line)


def _project_root():
    cwd = os.getcwd()
    if os.path.isdir(cwd) and "Content" in (os.listdir(cwd) or []):
        return cwd
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", ".."))


def blender_to_ue_cm(loc):
    """Blender meters Z-up -> UE centimeters. Flip Y (same as place_vs_mvp_markers)."""
    x, y, z = float(loc[0]), float(loc[1]), float(loc[2])
    return unreal.Vector(x * 100.0, -y * 100.0, z * 100.0)


def blender_offset_to_ue_cm(offset):
    return blender_to_ue_cm(offset)


def _asset_basename(asset_path):
    """Return StaticMesh asset name without UE path or ObjectPath duplicate suffix."""
    tail = asset_path.rsplit("/", 1)[-1]
    return tail.split(".", 1)[0]


def _should_skip_mesh_name(name):
    return name.startswith("UCX_") or name.startswith("M_")


def _is_static_mesh_asset(asset_path):
    if not unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        return False
    try:
        asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    except Exception:
        return False
    return asset is not None and isinstance(asset, unreal.StaticMesh)


def _mesh_matches_prefix(name, prefix, exact=False):
    """Match mesh basename: exact (SM_IslandTop), family (SM_Cabin_*), or prefix+underscore."""
    if _should_skip_mesh_name(name):
        return False
    if name == prefix:
        return True
    if exact:
        return False
    if prefix.endswith("_"):
        return name.startswith(prefix)
    return name.startswith(prefix + "_")


def build_mesh_index():
    """Map mesh basename -> (asset_path, StaticMesh) under MESH_ROOTS."""
    index = {}
    for root in MESH_ROOTS:
        if not unreal.EditorAssetLibrary.does_directory_exist(root):
            _log("Mesh root missing (skip)", {"path": root})
            continue
        for asset_path in unreal.EditorAssetLibrary.list_assets(root, recursive=True):
            name = _asset_basename(asset_path)
            if _should_skip_mesh_name(name):
                continue
            if name in index:
                continue
            if _is_static_mesh_asset(asset_path):
                mesh = unreal.EditorAssetLibrary.load_asset(asset_path)
                index[name] = (asset_path, mesh)
    _log("Mesh index built", {"count": len(index)})
    return index


def find_meshes_for_prefix(mesh_index, prefix, exact=False):
    hits = []
    for name, pair in sorted(mesh_index.items()):
        if _mesh_matches_prefix(name, prefix, exact=exact):
            hits.append((name, pair[0], pair[1]))
    return hits


def destroy_existing_dress():
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
        if label.startswith(DRESS_LABEL_PREFIX) or folder.replace("\\", "/") == DRESS_FOLDER:
            to_destroy.append(actor)
    for actor in to_destroy:
        unreal.EditorLevelLibrary.destroy_actor(actor)
    if to_destroy:
        _log("Removed existing dress actors", {"count": len(to_destroy)})


def spawn_dress_actor(mesh_name, static_mesh, location_blender, rotation_euler=None):
    loc = blender_to_ue_cm(location_blender)
    rot = unreal.Rotator(0, 0, 0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc, rot)
    if not actor:
        _log("Spawn failed", {"mesh": mesh_name})
        return None
    sm_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
    if sm_comp and static_mesh:
        sm_comp.set_static_mesh(static_mesh)
    actor.set_actor_label(DRESS_LABEL_PREFIX + mesh_name)
    actor.set_folder_path(DRESS_FOLDER)
    _log("Spawned dress", {"label": DRESS_LABEL_PREFIX + mesh_name, "loc_blender": location_blender})
    return actor


def _anchor_location(anchors, key):
    item = anchors.get(key)
    if not item:
        return None
    loc = item.get("location") if isinstance(item, dict) else None
    return loc


def _crumb_location(data, crumb_name):
    for item in data.get("CRUMB", []):
        if item.get("name") == crumb_name:
            return item.get("location")
    return None


def _add_blender_offset(base_loc, offset):
    bx, by, bz = base_loc
    ox, oy, oz = offset
    return [bx + ox, by + oy, bz + oz]


def place_at_anchor(mesh_index, anchors, anchor_key, mesh_prefix, missing, optional=False, exact=False):
    base = _anchor_location(anchors, anchor_key)
    if not base:
        _log("Anchor missing in JSON", {"anchor": anchor_key})
        missing.append("anchor:" + anchor_key)
        return 0
    meshes = find_meshes_for_prefix(mesh_index, mesh_prefix, exact=exact)
    if not meshes:
        msg = "mesh_prefix:" + mesh_prefix + " (anchor " + anchor_key + ")"
        if optional:
            _log("Optional meshes not found (skip)", {"prefix": mesh_prefix})
        else:
            _log("Meshes not found", {"prefix": mesh_prefix, "anchor": anchor_key})
            missing.append(msg)
        return 0
    spawned = 0
    for name, _path, mesh in meshes:
        if spawn_dress_actor(name, mesh, base):
            spawned += 1
    return spawned


def place_at_location(mesh_index, location_blender, mesh_prefix, missing, optional=False, exact=False):
    meshes = find_meshes_for_prefix(mesh_index, mesh_prefix, exact=exact)
    if not meshes:
        msg = "mesh_prefix:" + mesh_prefix
        if optional:
            _log("Optional meshes not found (skip)", {"prefix": mesh_prefix})
        else:
            _log("Meshes not found", {"prefix": mesh_prefix})
            missing.append(msg)
        return 0
    spawned = 0
    for name, _path, mesh in meshes:
        if spawn_dress_actor(name, mesh, location_blender):
            spawned += 1
    return spawned


def load_json_data(root):
    json_path = os.path.join(root, JSON_REL)
    if not os.path.isfile(json_path):
        _log("JSON not found", {"path": json_path})
        return None
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_level():
    import place_vs_mvp_markers

    importlib.reload(place_vs_mvp_markers)
    place_vs_mvp_markers.create_or_load_level()
    return True


def main():
    _log("Start VS_MVP dress")
    root = _project_root()
    data = load_json_data(root)
    if not data:
        return 1

    ensure_level()
    destroy_existing_dress()

    anchors = data.get("anchors") or {}
    mesh_index = build_mesh_index()
    missing = []
    spawned = 0

    EXACT_MESH_PREFIXES = frozenset(
        ("SM_IslandTop", "SM_Lookout_Pad", "SM_Glider_Perch", "SM_Planet_GroundPlate")
    )

    for anchor_key, mesh_prefix in ANCHOR_MESH_RULES:
        exact = mesh_prefix in EXACT_MESH_PREFIXES
        spawned += place_at_anchor(
            mesh_index, anchors, anchor_key, mesh_prefix, missing, exact=exact
        )

    for crumb_name, mesh_prefix in ISLET_RULES:
        loc = _crumb_location(data, crumb_name)
        if not loc:
            _log("CRUMB missing in JSON", {"crumb": crumb_name})
            missing.append("crumb:" + crumb_name)
            continue
        spawned += place_at_location(mesh_index, loc, mesh_prefix, missing)

    for anchor_key, mesh_prefix, offset, optional in EXTRA_RULES:
        base = _anchor_location(anchors, anchor_key)
        if not base:
            _log("Anchor missing for extra rule", {"anchor": anchor_key, "prefix": mesh_prefix})
            if not optional:
                missing.append("anchor:" + anchor_key)
            continue
        loc = _add_blender_offset(base, offset)
        exact = mesh_prefix in EXACT_MESH_PREFIXES
        spawned += place_at_location(
            mesh_index, loc, mesh_prefix, missing, optional=optional, exact=exact
        )

    try:
        unreal.EditorLevelLibrary.save_current_level()
        _log("Saved current level", {"path": LEVEL_PATH})
    except Exception as exc:
        _log("Save level warning", {"error": str(exc)})

    if missing:
        _log("Missing meshes or anchors (non-fatal where optional)", {"items": missing})
    else:
        _log("All requested mesh prefixes resolved")

    _log(
        "FALLBACK: scripted glide along CRUMB_* only; portal SM_Shrine_Homestead <-> SM_Shrine_Return (no free-flight)"
    )
    _log("Done", {"spawned": spawned, "missing_count": len(missing)})
    return 0


if __name__ == "__main__":
    code = main()
    if code != 0:
        unreal.log_error(PREFIX + " finished with code %s" % code)

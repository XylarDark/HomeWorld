# place_prototype_import_cleanup.py
# Lead-locked import cleanup: spawn new prototype meshes at old actors'
# transforms on L_VS_MVP_Markers; REMOVE (delete) old dress actors — not hide.
# Copy tags / collision / relevant component flags for functional parity.
# Materials assigned separately by assign_prototype_material_map.py.

from __future__ import annotations

import json
import os
import sys
from datetime import datetime

try:
    import unreal
except ImportError:
    print("place_prototype_import_cleanup: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "place_prototype_import_cleanup:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
PROTO_FOLDER = "VS_MVP/PrototypeImport"
PROTO_LABEL_PREFIX = "PROTO_"
REPORT_REL = os.path.join("Saved", "prototype_import_place_report.json")

CABIN_MESH = "/Game/HomeWorld/Meshes/Homestead/SM_Cabin_Prototype"
CABIN_CORNER = "/Game/HomeWorld/Meshes/Homestead/SM_Cabin_CornerPosts"
PORTAL_MESH = "/Game/HomeWorld/Meshes/Gatherables/SM_Portal_Prototype"
FLOWERS_MESH = "/Game/HomeWorld/Meshes/Gatherables/SM_Flowers_Prototype"

OLD_CABIN_PREFIXES = ("DRESS_SM_Cabin_",)
OLD_PORTAL_PREFIXES = ("DRESS_SM_Shrine_Homestead_",)
OLD_FLOWER_LABELS = ("GP_RS_Flower",)
OLD_FLOWER_PREFIXES = ("DRESS_SM_Gather_FirstHarvest_Bush_",)

FALLBACK_BLENDER = {
    "cabin": [-6.0, 1.0, 0.0],
    "portal": [-2.0, 3.5, 0.0],
    "flowers": [-3.5, 0.5, 0.0],
}


def _log(msg, data=None):
    line = PREFIX + " " + str(msg)
    if data is not None:
        line += " " + str(data)
    unreal.log(line)
    print(line)


def blender_to_ue_cm(loc):
    x, y, z = float(loc[0]), float(loc[1]), float(loc[2])
    return unreal.Vector(x * 100.0, -y * 100.0, z * 100.0)


def _project_root():
    cwd = os.getcwd()
    if os.path.isdir(os.path.join(cwd, "Content")):
        return cwd
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", ".."))


def _ensure_level():
    try:
        unreal.EditorLoadingAndSavingUtils.load_map(LEVEL_PATH)
        _log("Loaded level", {"path": LEVEL_PATH})
    except Exception as exc:
        _log("load_map note (may already be open)", {"err": str(exc)})


def _all_actors():
    try:
        return list(unreal.EditorLevelLibrary.get_all_level_actors())
    except Exception:
        return []


def _label(actor):
    try:
        return actor.get_actor_label() or ""
    except Exception:
        return ""


def _find_by_prefixes(prefixes):
    hits = []
    for actor in _all_actors():
        lab = _label(actor)
        for p in prefixes:
            if lab.startswith(p):
                hits.append(actor)
                break
    return hits


def _find_by_exact_labels(labels):
    wanted = set(labels)
    hits = []
    for actor in _all_actors():
        if _label(actor) in wanted:
            hits.append(actor)
    return hits


def _actor_transform(actor):
    loc = actor.get_actor_location()
    rot = actor.get_actor_rotation()
    scale = None
    try:
        scale = actor.get_actor_scale3d()
    except Exception:
        try:
            t = actor.get_actor_transform()
            scale = t.scale3d
        except Exception:
            scale = unreal.Vector(1, 1, 1)
    return loc, rot, scale


def _is_blueprint_actor(actor) -> bool:
    try:
        cls = actor.get_class()
        path = str(cls.get_path_name()) if cls else ""
        # Generated BP classes live under /Game/... and class name often ends with _C
        if "/Game/" in path and path.endswith("_C"):
            return True
        name = str(cls.get_name()) if cls else ""
        if name.endswith("_C") and not name.startswith("StaticMeshActor"):
            return True
    except Exception:
        pass
    return False


def _copy_parity(src_actor, dst_actor):
    """Copy tags, collision, mobility, hidden flags from src to dst for functional parity."""
    notes = []
    # Tags
    try:
        tags = list(src_actor.tags) if src_actor.tags else []
        if tags:
            dst_actor.tags = tags
            notes.append("tags:" + ",".join(str(t) for t in tags))
        else:
            # DRESS_* sources are bare StaticMeshActors (place_vs_mvp_dress.py) - nothing to copy.
            notes.append("tags:none_on_source")
    except Exception as exc:
        notes.append("tags_fail:" + str(exc))

    src_sm = None
    dst_sm = None
    try:
        src_sm = src_actor.get_component_by_class(unreal.StaticMeshComponent)
    except Exception:
        pass
    try:
        dst_sm = dst_actor.static_mesh_component
        if dst_sm is None:
            dst_sm = dst_actor.get_component_by_class(unreal.StaticMeshComponent)
    except Exception:
        pass

    if src_sm and dst_sm:
        # Collision
        try:
            enabled = src_sm.get_collision_enabled()
            dst_sm.set_collision_enabled(enabled)
            notes.append("collision_enabled:" + str(enabled))
        except Exception:
            try:
                dst_actor.set_actor_enable_collision(src_actor.get_actor_enable_collision())
                notes.append("actor_collision_copied")
            except Exception as exc:
                notes.append("collision_fail:" + str(exc))
        try:
            profile = src_sm.get_collision_profile_name()
            dst_sm.set_collision_profile_name(profile)
            notes.append("collision_profile:" + str(profile))
        except Exception:
            pass
        try:
            dst_sm.set_generate_overlap_events(src_sm.get_generate_overlap_events())
            notes.append("overlap_events_copied")
        except Exception:
            pass
        try:
            dst_sm.set_mobility(src_sm.mobility)
            notes.append("mobility_copied")
        except Exception:
            pass
        try:
            dst_sm.set_cast_shadow(src_sm.get_cast_shadow())
        except Exception:
            pass
    else:
        try:
            dst_actor.set_actor_enable_collision(True)
            notes.append("default_collision_on")
        except Exception:
            pass

    # Visibility
    try:
        dst_actor.set_actor_hidden_in_game(False)
        dst_actor.set_is_temporarily_hidden_in_editor(False)
    except Exception:
        pass

    return notes


def _remove_actors(actors, report_list, skipped_list):
    """DELETE old actors (Lead lock). Skip Blueprint gameplay actors; log skips."""
    for actor in actors:
        lab = _label(actor)
        if _is_blueprint_actor(actor) and not isinstance(actor, unreal.StaticMeshActor):
            skipped_list.append({"label": lab, "reason": "blueprint_gameplay_preserve"})
            _log("Skip remove BP actor (preserve interact)", {"label": lab})
            continue
        # Also skip if class name suggests BP harvestable / GP_
        try:
            cls_name = actor.get_class().get_name()
        except Exception:
            cls_name = ""
        if lab.startswith("GP_") and "StaticMeshActor" not in cls_name:
            skipped_list.append({"label": lab, "reason": "gp_prefix_non_sma", "class": cls_name})
            _log("Skip remove GP_* non-SMA", {"label": lab, "class": cls_name})
            continue
        try:
            ok = unreal.EditorLevelLibrary.destroy_actor(actor)
            report_list.append({"label": lab, "destroyed": bool(ok), "class": cls_name})
            _log("Removed old actor", {"label": lab, "ok": ok})
        except Exception as exc:
            report_list.append({"label": lab, "destroyed": False, "err": str(exc)})
            _log("Remove failed", {"label": lab, "err": str(exc)})


def _destroy_existing_proto(prefix_match):
    to_destroy = []
    for actor in _all_actors():
        lab = _label(actor)
        if lab.startswith(PROTO_LABEL_PREFIX) and any(s in lab for s in prefix_match):
            to_destroy.append(actor)
    for actor in to_destroy:
        unreal.EditorLevelLibrary.destroy_actor(actor)
    if to_destroy:
        _log("Removed prior PROTO actors", {"count": len(to_destroy), "match": list(prefix_match)})


def _load_mesh(path):
    if not unreal.EditorAssetLibrary.does_asset_exist(path):
        _log("Mesh missing", {"path": path})
        return None
    mesh = unreal.EditorAssetLibrary.load_asset(path)
    if mesh is None or not isinstance(mesh, unreal.StaticMesh):
        _log("Not a StaticMesh", {"path": path})
        return None
    return mesh


def _spawn_proto(mesh_path, label_suffix, location, rotation=None, scale=None, parity_src=None):
    mesh = _load_mesh(mesh_path)
    if mesh is None:
        return None, []
    rot = rotation if rotation is not None else unreal.Rotator(0, 0, 0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor, location, rot
    )
    if not actor:
        _log("Spawn failed", {"mesh": mesh_path})
        return None, []
    if scale is not None:
        try:
            actor.set_actor_scale3d(scale)
        except Exception:
            pass
    sm_comp = actor.static_mesh_component
    if sm_comp is None:
        sm_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
    if sm_comp and mesh:
        sm_comp.set_static_mesh(mesh)
    label = PROTO_LABEL_PREFIX + label_suffix
    actor.set_actor_label(label)
    actor.set_folder_path(PROTO_FOLDER)
    actor.set_actor_hidden_in_game(False)
    try:
        actor.set_is_temporarily_hidden_in_editor(False)
    except Exception:
        pass
    parity_notes = []
    if parity_src is not None:
        parity_notes = _copy_parity(parity_src, actor)
    _log("Spawned proto", {"label": label, "loc": [location.x, location.y, location.z], "parity": parity_notes})
    return actor, parity_notes


def _resolve_transform(old_actors, fallback_blender_key):
    if old_actors:
        preferred = None
        for a in old_actors:
            lab = _label(a)
            if any(s in lab for s in ("Foundation", "Base", "Wall_Front", "Lintel")):
                preferred = a
                break
        src = preferred or old_actors[0]
        loc, rot, scale = _actor_transform(src)
        return loc, rot, scale, src, "old_actor:" + _label(src)
    loc = blender_to_ue_cm(FALLBACK_BLENDER[fallback_blender_key])
    return loc, unreal.Rotator(0, 0, 0), unreal.Vector(1, 1, 1), None, "fallback_blender:" + fallback_blender_key


def main():
    _log("BEGIN (REMOVE old actors, not hide)")
    _ensure_level()

    report = {
        "started": datetime.now().isoformat(timespec="seconds"),
        "level": LEVEL_PATH,
        "placed": [],
        "removed": [],
        "remove_skipped": [],
        "notes": [],
        "materials_assigned": False,
        "mode": "remove_not_hide",
    }

    # --- Cabin ---
    old_cabin = _find_by_prefixes(OLD_CABIN_PREFIXES)
    loc, rot, scale, src, origin = _resolve_transform(old_cabin, "cabin")
    _destroy_existing_proto(("SM_Cabin_Prototype", "SM_Cabin_CornerPosts"))
    a1, p1 = _spawn_proto(CABIN_MESH, "SM_Cabin_Prototype", loc, rot, scale, src)
    a2, p2 = _spawn_proto(CABIN_CORNER, "SM_Cabin_CornerPosts", loc, rot, scale, src)
    if a1:
        report["placed"].append({"label": _label(a1), "src": origin, "mesh": CABIN_MESH, "parity": p1})
    if a2:
        report["placed"].append({"label": _label(a2), "src": origin, "mesh": CABIN_CORNER, "parity": p2})
    _remove_actors(old_cabin, report["removed"], report["remove_skipped"])
    if not old_cabin:
        report["notes"].append("No DRESS_SM_Cabin_* found; used fallback cabin anchor")

    # --- Portal ---
    old_portal = _find_by_prefixes(OLD_PORTAL_PREFIXES)
    loc, rot, scale, src, origin = _resolve_transform(old_portal, "portal")
    _destroy_existing_proto(("SM_Portal_Prototype",))
    a3, p3 = _spawn_proto(PORTAL_MESH, "SM_Portal_Prototype", loc, rot, scale, src)
    if a3:
        report["placed"].append({"label": _label(a3), "src": origin, "mesh": PORTAL_MESH, "parity": p3})
    _remove_actors(old_portal, report["removed"], report["remove_skipped"])
    if not old_portal:
        report["notes"].append("No DRESS_SM_Shrine_Homestead_* found; used fallback shrine anchor")

    # --- Flowers ---
    old_flowers = _find_by_exact_labels(OLD_FLOWER_LABELS) + _find_by_prefixes(OLD_FLOWER_PREFIXES)
    loc, rot, scale, src, origin = _resolve_transform(old_flowers, "flowers")
    _destroy_existing_proto(("SM_Flowers_Prototype",))
    # Prefer a StaticMeshActor as parity source if GP_ is BP
    parity_src = src
    if src is not None and _is_blueprint_actor(src):
        for a in old_flowers:
            if isinstance(a, unreal.StaticMeshActor):
                parity_src = a
                break
    a4, p4 = _spawn_proto(FLOWERS_MESH, "SM_Flowers_Prototype", loc, rot, scale, parity_src)
    if a4:
        report["placed"].append({"label": _label(a4), "src": origin, "mesh": FLOWERS_MESH, "parity": p4})
    _remove_actors(old_flowers, report["removed"], report["remove_skipped"])
    if not old_flowers:
        report["notes"].append("No flower/bush old actors; used garden-centre fallback")

    # Functional parity beyond tags/collision copy: PROTO pivots are centred on the anchors
    # (old DRESS meshes were world-baked), so clear gameplay actors the new hulls encroach.
    try:
        import importlib
        import prototype_import_parity

        importlib.reload(prototype_import_parity)
        parity = prototype_import_parity.apply(save=False)
        report["parity_fix"] = {
            "portal_pawn_clearance": parity.get("portal_pawn_clearance"),
            "player_start": parity.get("player_start"),
            "gameplay_encroached_after": parity.get("audit_after", {}).get("gameplay_encroached_by_proto"),
        }
    except Exception as exc:
        report["notes"].append("prototype_import_parity failed: " + str(exc))
        _log("Parity fix failed", {"err": str(exc)})

    try:
        ok = unreal.EditorLevelLibrary.save_current_level()
        report["level_saved"] = bool(ok)
        _log("Saved current level", {"ok": ok})
    except Exception as exc:
        report["level_saved"] = False
        report["notes"].append("save_current_level failed: " + str(exc))
        _log("Save failed", {"err": str(exc)})

    report["finished"] = datetime.now().isoformat(timespec="seconds")
    report["placed_count"] = len(report["placed"])
    report["removed_count"] = len(report["removed"])
    report["remove_skipped_count"] = len(report["remove_skipped"])

    out_path = os.path.join(_project_root(), REPORT_REL)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    _log(
        "Wrote report",
        {
            "path": out_path,
            "placed": report["placed_count"],
            "removed": report["removed_count"],
            "skipped": report["remove_skipped_count"],
        },
    )
    _log("DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)

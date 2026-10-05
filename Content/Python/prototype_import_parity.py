# prototype_import_parity.py
# Lead lock (prototype import): PROTO_* actors must be as functional as the DRESS_* actors
# they replaced. Called at the end of place_prototype_import_cleanup.py; also runnable alone
# (Execute Python Script / MCP execute_python_script("prototype_import_parity.py")).
#
# Facts this encodes (DESKTOP inventory 2026-10-05):
# - Old DRESS_SM_Cabin_* / DRESS_SM_Shrine_Homestead_* / DRESS_SM_Gather_FirstHarvest_Bush_*
#   were plain StaticMeshActors from place_vs_mvp_dress.py: NO tags, NO extra components,
#   one convex hull per piece, BlockAll. Interact never lived on them; it lives on separate
#   actors that the cleanup did not touch: GP_PortalA/B (HomeWorldShrinePortalTrigger),
#   GP_Store_* (StoreProp), GP_N1_Crop / GP_N2_Stored (NurtureTarget).
# - Old meshes had world-baked pivots, so the old dress rendered at 2x its anchor offset and
#   never overlapped those gameplay actors. PROTO meshes have centred pivots and sit ON the
#   anchors, so their single-hull collision now encroaches gameplay actors:
#     * PlayerStart_VS_MVP (-400,-150,100) inside PROTO cabin hull -> PIE log
#       "FindPlayerStart: ... NO PLAYERSTART with positive rating", pawn spawned at (0,0,90).
#     * Home portal arrival point (ANCHOR_SM_Shrine_Homestead + 80 fwd) inside PROTO portal hull.
# Fix (smallest, keeps PROTO collision otherwise identical to the copied BlockAll):
#   1. PROTO_SM_Portal_Prototype ignores Pawn only (trigger volume + arrival walkable as before).
#   2. If PlayerStart_VS_MVP / GP_PlayerStart are encroached, move them to the cabin hub
#      offset used by place_vs_mvp_gp.py (ANCHOR_SM_Cabin + (360, -20, 100)).
# Tags: none copied because the sources had none (see report "tags_old").

from __future__ import annotations

import json
import os
import sys
from datetime import datetime

try:
    import unreal
except ImportError:
    print("prototype_import_parity: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "prototype_import_parity:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
REPORT_REL = os.path.join("Saved", "prototype_import_parity_report.json")

PROTO_PREFIX = "PROTO_"
PORTAL_PROTO_LABEL = "PROTO_SM_Portal_Prototype"
PLAYER_START_LABELS = ("PlayerStart_VS_MVP", "GP_PlayerStart")
CABIN_ANCHOR_LABEL = "ANCHOR_SM_Cabin"
# Keep in sync with place_vs_mvp_gp.compute_spawn_location.
PLAYER_START_CABIN_OFFSET = (360.0, -20.0, 100.0)
PLAYER_CAPSULE = (40.0, 92.0)  # PlayerStart capsule radius / half-height (cm)
INTERACT_LABEL_PREFIXES = ("GP_", "NODE_", "PlayerStart_VS_MVP")
PORTAL_ARRIVE_ANCHORS = ("ANCHOR_SM_Shrine_Homestead", "ANCHOR_SM_Shrine_Return")


def _log(msg, data=None):
    line = PREFIX + " " + str(msg)
    if data is not None:
        line += " " + str(data)
    unreal.log(line)
    print(line)


def _project_root():
    cwd = os.getcwd()
    if os.path.isdir(os.path.join(cwd, "Content")):
        return cwd
    return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def _actors():
    try:
        return list(unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors())
    except Exception:
        return list(unreal.EditorLevelLibrary.get_all_level_actors())


def _label(actor):
    try:
        return actor.get_actor_label() or ""
    except Exception:
        return ""


def _by_label():
    return {_label(a): a for a in _actors()}


def _world():
    try:
        return unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    except Exception:
        return unreal.EditorLevelLibrary.get_editor_world()


def _object_types():
    out = []
    for new, old in (("ECC_WORLD_STATIC", "OBJECT_TYPE_QUERY1"), ("ECC_WORLD_DYNAMIC", "OBJECT_TYPE_QUERY2")):
        val = getattr(unreal.ObjectTypeQuery, new, None) or getattr(unreal.ObjectTypeQuery, old)
        out.append(val)
    return out


def _vec(v):
    return [round(v.x, 1), round(v.y, 1), round(v.z, 1)]


def capsule_blockers(location, radius, half_height, ignore=None):
    """PROTO_* actors whose collision overlaps a capsule at location."""
    res = unreal.SystemLibrary.capsule_overlap_actors(
        _world(), location, radius, half_height, _object_types(), None, list(ignore or [])
    )
    if isinstance(res, tuple):
        res = res[-1]
    hits = res if isinstance(res, (list, unreal.Array)) else ([res] if res else [])
    return sorted({_label(h) for h in hits if _label(h).startswith(PROTO_PREFIX)})


def apply_portal_pawn_clearance(actors):
    actor = actors.get(PORTAL_PROTO_LABEL)
    if not actor:
        return {"applied": False, "reason": "missing " + PORTAL_PROTO_LABEL}
    comp = actor.get_component_by_class(unreal.StaticMeshComponent)
    actor.modify()
    comp.modify()
    comp.set_collision_response_to_channel(unreal.CollisionChannel.ECC_PAWN, unreal.CollisionResponseType.ECR_IGNORE)
    return {
        "applied": True,
        "collision_enabled": str(comp.get_collision_enabled()),
        "profile": str(comp.get_collision_profile_name()),
        "pawn": str(comp.get_collision_response_to_channel(unreal.CollisionChannel.ECC_PAWN)),
        "visibility": str(comp.get_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY)),
    }


def relocate_player_start_if_encroached(actors):
    ps = actors.get(PLAYER_START_LABELS[0])
    if not ps:
        return {"moved": False, "reason": "missing PlayerStart_VS_MVP"}
    radius, half = PLAYER_CAPSULE
    before = ps.get_actor_location()
    blockers = capsule_blockers(before, radius, half, [ps])
    result = {"before": _vec(before), "blockers_before": blockers, "moved": False}
    if not blockers:
        return result
    anchor = actors.get(CABIN_ANCHOR_LABEL)
    if not anchor:
        result["reason"] = "missing " + CABIN_ANCHOR_LABEL
        return result
    base = anchor.get_actor_location()
    ox, oy, oz = PLAYER_START_CABIN_OFFSET
    target = unreal.Vector(base.x + ox, base.y + oy, base.z + oz)
    for lab in PLAYER_START_LABELS:
        a = actors.get(lab)
        if a:
            a.modify()
            a.set_actor_location(target, False, True)
    result.update({"moved": True, "after": _vec(target), "blockers_after": capsule_blockers(target, radius, half, [ps])})
    return result


def audit(actors):
    out = {"proto": {}, "gameplay_encroached_by_proto": {}, "portal_arrive": {}}
    for lab, a in sorted(actors.items()):
        if lab.startswith(PROTO_PREFIX):
            comp = a.get_component_by_class(unreal.StaticMeshComponent)
            out["proto"][lab] = {
                "loc": _vec(a.get_actor_location()),
                "tags": [str(t) for t in a.tags],
                "collision_enabled": str(comp.get_collision_enabled()) if comp else None,
                "profile": str(comp.get_collision_profile_name()) if comp else None,
                "pawn": str(comp.get_collision_response_to_channel(unreal.CollisionChannel.ECC_PAWN)) if comp else None,
                "mesh": comp.static_mesh.get_path_name() if comp and comp.static_mesh else None,
            }
        elif lab.startswith(INTERACT_LABEL_PREFIXES):
            blockers = capsule_blockers(a.get_actor_location(), 20.0, 20.0, [a])
            if blockers:
                out["gameplay_encroached_by_proto"][lab] = blockers
    radius, half = 34.0, 88.0
    for lab in PORTAL_ARRIVE_ANCHORS:
        a = actors.get(lab)
        if not a:
            continue
        loc = a.get_actor_location()
        fwd = a.get_actor_forward_vector()
        arrive = unreal.Vector(loc.x + fwd.x * 80.0, loc.y + fwd.y * 80.0, loc.z + fwd.z * 80.0 + half)
        # Pawn-blocking only: a PROTO actor that ignores Pawn cannot trap the player.
        blockers = []
        for b in capsule_blockers(arrive, radius, half):
            comp = actors[b].get_component_by_class(unreal.StaticMeshComponent)
            if comp and comp.get_collision_response_to_channel(unreal.CollisionChannel.ECC_PAWN) == unreal.CollisionResponseType.ECR_BLOCK:
                blockers.append(b)
        out["portal_arrive"][lab] = {"arrive": _vec(arrive), "pawn_blockers": blockers}
    return out


def apply(save=True, load_level=False):
    world = _world()
    on_level = bool(world) and world.get_path_name().startswith(LEVEL_PATH + ".")
    if load_level and not on_level:
        # Overlap queries return nothing in the same tick as load_map; run again after load.
        unreal.EditorLoadingAndSavingUtils.load_map(LEVEL_PATH)
        _log("Loaded level - re-run this script so collision queries see the new world")
        return {"loaded_only": True}
    actors = _by_label()
    report = {
        "started": datetime.now().isoformat(timespec="seconds"),
        "level": LEVEL_PATH,
        "tags_old": "none - DRESS_* were bare StaticMeshActors (place_vs_mvp_dress.py; umap name-table diff 4920c90 vs 33bb37f)",
        "interact_lives_on": ["GP_PortalA", "GP_PortalB", "GP_Store_*", "GP_N1_Crop", "GP_N2_Stored"],
        "interact_actors_present": sorted(l for l in actors if l.startswith(("GP_Portal", "GP_Store_", "GP_N1_", "GP_N2_"))),
        "audit_before": audit(actors),
    }
    report["portal_pawn_clearance"] = apply_portal_pawn_clearance(actors)
    report["player_start"] = relocate_player_start_if_encroached(actors)
    report["audit_after"] = audit(_by_label())
    if save:
        # Python edits do not always dirty the map package, so force the write.
        report["level_saved"] = bool(unreal.EditorAssetLibrary.save_asset(LEVEL_PATH, only_if_is_dirty=False))
    report["finished"] = datetime.now().isoformat(timespec="seconds")
    out_path = os.path.join(_project_root(), REPORT_REL)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    _log("Wrote report", {"path": out_path})
    return report


if __name__ == "__main__":
    apply(save=True, load_level=True)

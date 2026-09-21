# homeworld_gc_site_setup.py — GC-A site→RES tags + optional GatherSiteKind on resource piles.
# Used by place_vs_mvp_* scripts; C++ infers from GC_Site_* tags and GP_RS_* labels when enum unset.

from __future__ import annotations

try:
    import unreal
except ImportError:
    unreal = None  # type: ignore

GC_SITE_TAG_BY_KIND = {
    "trees": "GC_Site_Trees",
    "rocks": "GC_Site_Rocks",
    "flowers": "GC_Site_Flowers",
    "berry": "GC_Site_Berry",
    "seed": "GC_Site_Seed",
}


def _gather_site_enum_type():
    if unreal is None:
        return None, None
    for type_name in ("EHomeWorldGatherSiteKind", "HomeWorldGatherSiteKind"):
        enum_type = getattr(unreal, type_name, None)
        if enum_type is not None:
            return type_name, enum_type
    for name in sorted(dir(unreal)):
        if "GatherSiteKind" in name and not name.startswith("_"):
            enum_type = getattr(unreal, name, None)
            if enum_type is not None:
                return name, enum_type
    return None, None


def _enum_member(enum_type, site_kind: str):
    if enum_type is None:
        return None
    candidates = [
        site_kind,
        site_kind.upper(),
        site_kind.capitalize(),
        site_kind.replace("_", "").upper(),
    ]
    if site_kind == "berry":
        candidates.extend(["BERRY_NODE", "BerryNode", "berry_node"])
    if site_kind == "seed":
        candidates.extend(["SEED_POD", "SeedPod", "seed_pod"])
    for cand in candidates:
        member = getattr(enum_type, cand, None)
        if member is not None:
            return member
    return None


def apply_gc_site(actor, site_kind: str | None, fallback_resource_id: str | None = None) -> None:
    """Tag pile for GC-A mapping; set gather_site_kind when UE exposes the enum."""
    if unreal is None or not actor or not site_kind:
        return
    tag = GC_SITE_TAG_BY_KIND.get(site_kind)
    if tag:
        try:
            tags = list(actor.tags)
            tag_name = unreal.Name(tag)
            if tag_name not in tags:
                tags.append(tag_name)
                actor.tags = tags
        except Exception:
            pass
    _, enum_type = _gather_site_enum_type()
    member = _enum_member(enum_type, site_kind)
    if member is not None:
        try:
            actor.set_editor_property("gather_site_kind", member)
        except Exception:
            pass
    if fallback_resource_id:
        try:
            actor.set_editor_property("resource_type", unreal.Name(fallback_resource_id))
        except Exception:
            pass

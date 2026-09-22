# place_vs_mvp_gc_placeholders.py — GC-C shop + cottage room placeholder volumes on L_VS_MVP_Markers.
# DS-A: GP_Demo_Cottage blockout (hidden until unlock) + readable room markers at PIE.
# Run after Safe-Build; idempotent GP_PH_* actors.

from __future__ import annotations

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "DS-PlaceholderPlace:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
TARGET_CLASS = "/Script/HomeWorld.HomeWorldGcPlaceholderVolume"
FOLDER = "VS_MVP/Markers/GC_Placeholders"

# EHomeWorldGcPlaceholderKind (C++ enum order)
KIND_WOODSHOP = 0
KIND_TEXTILE = 1
KIND_RESEARCH = 2
KIND_KITCHEN = 3
KIND_BEDROOM = 4
KIND_CAULDRON = 5

# (label, kind, offset from cabin hub)
PLACEHOLDERS = [
    ("GP_PH_Woodshop", KIND_WOODSHOP, unreal.Vector(450.0, 550.0, 0.0)),
    ("GP_PH_Textile", KIND_TEXTILE, unreal.Vector(550.0, 450.0, 0.0)),
    ("GP_PH_Research", KIND_RESEARCH, unreal.Vector(650.0, 350.0, 0.0)),
    ("GP_PH_CottageKitchen", KIND_KITCHEN, unreal.Vector(120.0, -180.0, 0.0)),
    ("GP_PH_CottageBedroom", KIND_BEDROOM, unreal.Vector(-120.0, -180.0, 0.0)),
    ("GP_PH_Cauldron", KIND_CAULDRON, unreal.Vector(0.0, -280.0, 0.0)),
]


def _log(msg: str) -> None:
    unreal.log(PREFIX + " " + str(msg))
    print(PREFIX, msg)


def find_actor_by_label(label: str):
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        try:
            if actor.get_actor_label() == label:
                return actor
        except Exception:
            continue
    return None


def _cabin_base():
    for label in ("SM_Cabin", "GP_PlayerStart", "GP_N2_Stored"):
        a = find_actor_by_label(label)
        if a:
            return a.get_actor_location()
    return unreal.Vector(0.0, 0.0, 0.0)


def _load_level() -> bool:
    if not unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        _log("Level missing")
        return False
    return bool(unreal.EditorLoadingAndSavingUtils.load_map(LEVEL_PATH))


def _ensure_placeholder(cls, label: str, kind: int, loc: unreal.Vector):
    existing = find_actor_by_label(label)
    if existing:
        actor = existing
        actor.set_actor_location(loc, False, True)
        _log("reuse " + label)
    else:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(cls, loc)
        if not actor:
            _log("FAIL spawn " + label)
            return None
        try:
            actor.set_actor_label(label)
        except Exception:
            pass
        try:
            actor.set_folder_path(FOLDER)
        except Exception:
            pass
        _log("spawn " + label)
    try:
        actor.set_editor_property("placeholder_kind", kind)
    except Exception as e:
        _log("placeholder_kind warn " + label + ": " + str(e))
    try:
        tags = list(actor.get_editor_property("tags") or [])
        tag_name = unreal.Name(label)
        if tag_name not in tags:
            tags.append(tag_name)
            actor.set_editor_property("tags", tags)
    except Exception:
        pass
    return actor


def main() -> int:
    if not _load_level():
        return 1
    cls = unreal.load_class(None, TARGET_CLASS)
    if not cls:
        _log("FAIL load class — Safe-Build first")
        return 2
    base = _cabin_base()
    ok = 0
    for label, kind, offset in PLACEHOLDERS:
        loc = base + offset
        if _ensure_placeholder(cls, label, kind, loc):
            ok += 1
    try:
        import vs_mvp_ds_visual_helpers as ds_vis

        ds_vis.ensure_cottage_blockout(base, unreal.Vector(0.0, -120.0, 0.0))
    except Exception as e:
        _log("DS-A cottage blockout warn: " + str(e))
    unreal.EditorLevelLibrary.save_current_level()
    _log("DONE placeholders placed=%d/%d (GP_Demo_Cottage hidden until unlock)" % (ok, len(PLACEHOLDERS)))
    return 0 if ok == len(PLACEHOLDERS) else 4


if __name__ == "__main__":
    raise SystemExit(main())

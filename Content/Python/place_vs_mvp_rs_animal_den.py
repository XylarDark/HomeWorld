# place_vs_mvp_rs_animal_den.py
# RS-C: idempotent animal den on L_VS_MVP_Markers — day BeastPad + night dream marker.
# Day claim/tame → existing UHomeWorldBeastTameComponent (TAME: logs).
# Night dream → TargetPoint stub (placeholder convert; full dream combat deferred).
# Run after place_vs_mvp_markers.py; Safe-Build for HomeWorldBeastPad.
# Script-only — KEEP-LOCAL level save; no .uasset/.umap commits.

from __future__ import annotations

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "RSDen:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
BEAST_PAD_CLASS = "/Script/HomeWorld.HomeWorldBeastPad"
FOLDER = "VS_MVP/Markers/RS_C"
DEN_LABEL = "GP_RS_AnimalDen"
DREAM_LABEL = "GP_RS_AnimalDen_Dream"
# Offset from CRUMB_Landing / landing circle (cm)
DEN_OFFSET = unreal.Vector(300.0, -200.0, 0.0)
DREAM_OFFSET = unreal.Vector(300.0, -200.0, 80.0)


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


def _load_level() -> bool:
    if not unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        _log("Level missing — run place_vs_mvp_markers.py first")
        return False
    return bool(unreal.EditorLoadingAndSavingUtils.load_map(LEVEL_PATH))


def _planet_base() -> unreal.Vector:
    for label in (
        "CRUMB_Landing",
        "SM_LandingCircle",
        "SM_Landing_Circle",
        "GP_Landing",
        "SM_Shrine_Return",
        "GP_BeastPad",
    ):
        actor = find_actor_by_label(label)
        if actor:
            _log("den base from " + label)
            return actor.get_actor_location()
    _log("den base fallback")
    return unreal.Vector(2200.0, -200.0, 0.0)


def _add_tag(actor, tag_name: str) -> None:
    try:
        tags = list(actor.tags)
        tag = unreal.Name(tag_name)
        if tag not in tags:
            tags.append(tag)
            actor.tags = tags
    except Exception:
        try:
            actor.tags.add(unreal.Name(tag_name))
        except Exception:
            pass


def _apply_label(actor, label: str) -> None:
    try:
        actor.set_actor_label(label, True)
    except TypeError:
        try:
            actor.set_actor_label(label)
        except Exception as exc:
            _log("label warn " + label + ": " + str(exc))


def _is_beast_pad(actor, beast_cls) -> bool:
    if not actor or not beast_cls:
        return False
    try:
        cls = actor.get_class()
        while cls:
            if cls == beast_cls:
                return True
            get_super = getattr(cls, "get_super_class", None)
            cls = get_super() if get_super else None
    except Exception:
        pass
    try:
        return "BeastPad" in actor.get_class().get_name()
    except Exception:
        return False


def _ensure_den_pad(location: unreal.Vector):
    beast_cls = unreal.load_class(None, BEAST_PAD_CLASS)
    if not beast_cls:
        _log("FAIL HomeWorldBeastPad missing — Safe-Build")
        return None

    existing = find_actor_by_label(DEN_LABEL)
    if existing and _is_beast_pad(existing, beast_cls):
        existing.set_actor_location(location, False, True)
        _add_tag(existing, DEN_LABEL)
        _add_tag(existing, "BeastPad")
        _log("updated " + DEN_LABEL)
        unreal.log("HomeWorld: RSDen day site ready " + DEN_LABEL)
        return existing
    if existing:
        try:
            unreal.EditorLevelLibrary.destroy_actor(existing)
        except Exception:
            pass

    # Reuse GP_BeastPad if present and den absent — also stamp den label alias via tag
    legacy = find_actor_by_label("GP_BeastPad")
    if legacy and _is_beast_pad(legacy, beast_cls) and not find_actor_by_label(DEN_LABEL):
        # Place a second pad for RS den so NP beast pad stays; spawn new
        pass

    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        beast_cls, location, unreal.Rotator(0, 0, 0)
    )
    if not actor:
        _log("FAIL spawn " + DEN_LABEL)
        return None
    _apply_label(actor, DEN_LABEL)
    _add_tag(actor, DEN_LABEL)
    _add_tag(actor, "BeastPad")
    try:
        actor.set_folder_path(FOLDER)
    except Exception:
        pass
    _log("spawned " + DEN_LABEL + " @ " + str(location))
    unreal.log("HomeWorld: RSDen day site ready " + DEN_LABEL)
    return actor


def _ensure_dream_marker(location: unreal.Vector):
    target_cls = unreal.load_class(None, "/Script/Engine.TargetPoint")
    if not target_cls:
        _log("FAIL TargetPoint class missing")
        return None
    existing = find_actor_by_label(DREAM_LABEL)
    if existing:
        existing.set_actor_location(location, False, True)
        _add_tag(existing, DREAM_LABEL)
        _log("updated " + DREAM_LABEL)
        unreal.log("HomeWorld: RSDen dream stub ready " + DREAM_LABEL)
        return existing
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(target_cls, location)
    if not actor:
        _log("FAIL spawn " + DREAM_LABEL)
        return None
    _apply_label(actor, DREAM_LABEL)
    _add_tag(actor, DREAM_LABEL)
    try:
        actor.set_folder_path(FOLDER)
    except Exception:
        pass
    _log("spawned " + DREAM_LABEL)
    unreal.log("HomeWorld: RSDen dream stub ready " + DREAM_LABEL)
    unreal.log(
        "HomeWorld: DREAM: stub marker "
        + DREAM_LABEL
        + " — night placeholder; use hw.Conversion.Test for recruit hook"
    )
    return actor


def main() -> None:
    _log("start RS-C animal den")
    if not _load_level():
        return
    base = _planet_base()
    den_loc = unreal.Vector(base.x + DEN_OFFSET.x, base.y + DEN_OFFSET.y, base.z + DEN_OFFSET.z)
    dream_loc = unreal.Vector(
        base.x + DREAM_OFFSET.x, base.y + DREAM_OFFSET.y, base.z + DREAM_OFFSET.z
    )
    den = _ensure_den_pad(den_loc)
    dream = _ensure_dream_marker(dream_loc)
    _log(
        "Done den=%s dream=%s. PIE day: face GP_RS_AnimalDen Interact → TAME:. "
        "Night: dream marker + hw.Conversion.Test → convert/recruit stub. Save KEEP-LOCAL."
        % ("ok" if den else "FAIL", "ok" if dream else "FAIL")
    )


if __name__ == "__main__":
    main()

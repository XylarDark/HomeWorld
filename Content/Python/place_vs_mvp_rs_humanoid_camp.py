# place_vs_mvp_rs_humanoid_camp.py
# RS-D: idempotent humanoid camp on L_VS_MVP_Markers — day visit/collect + night dream convert stub.
# Night recruit uses hw.Conversion.Test (ReportFoeConverted); placeholder GA deferred.
# Run after place_vs_mvp_markers.py. Script-only — KEEP-LOCAL level save.

from __future__ import annotations

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "RSCamp:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
FOLDER = "VS_MVP/Markers/RS_D"
CAMP_LABEL = "GP_RS_HumanoidCamp"
DREAM_LABEL = "GP_RS_HumanoidCamp_Dream"
COLLECT_LABEL = "GP_RS_HumanoidCamp_Collect"
# Offset from landing / return shrine (cm)
CAMP_OFFSET = unreal.Vector(-350.0, 280.0, 0.0)
DREAM_OFFSET = unreal.Vector(-350.0, 280.0, 80.0)
COLLECT_OFFSET = unreal.Vector(-280.0, 320.0, 0.0)


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
        "SM_Shrine_Return",
        "GP_RS_AnimalDen",
        "GP_BeastPad",
    ):
        actor = find_actor_by_label(label)
        if actor:
            _log("camp base from " + label)
            return actor.get_actor_location()
    _log("camp base fallback")
    return unreal.Vector(2400.0, 300.0, 0.0)


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


def _ensure_target(label: str, location: unreal.Vector, extra_tag=None):
    target_cls = unreal.load_class(None, "/Script/Engine.TargetPoint")
    if not target_cls:
        _log("FAIL TargetPoint class missing")
        return None
    existing = find_actor_by_label(label)
    if existing:
        existing.set_actor_location(location, False, True)
        _add_tag(existing, label)
        if extra_tag:
            _add_tag(existing, extra_tag)
        _log("updated " + label)
        return existing
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(target_cls, location)
    if not actor:
        _log("FAIL spawn " + label)
        return None
    _apply_label(actor, label)
    _add_tag(actor, label)
    if extra_tag:
        _add_tag(actor, extra_tag)
    try:
        actor.set_folder_path(FOLDER)
    except Exception:
        pass
    _log("spawned " + label + " @ " + str(location))
    return actor


def main() -> None:
    _log("start RS-D humanoid camp")
    if not _load_level():
        return
    base = _planet_base()
    camp_loc = unreal.Vector(base.x + CAMP_OFFSET.x, base.y + CAMP_OFFSET.y, base.z + CAMP_OFFSET.z)
    dream_loc = unreal.Vector(base.x + DREAM_OFFSET.x, base.y + DREAM_OFFSET.y, base.z + DREAM_OFFSET.z)
    collect_loc = unreal.Vector(
        base.x + COLLECT_OFFSET.x, base.y + COLLECT_OFFSET.y, base.z + COLLECT_OFFSET.z
    )
    camp = _ensure_target(CAMP_LABEL, camp_loc, "HumanoidCamp")
    dream = _ensure_target(DREAM_LABEL, dream_loc, "DreamConvert")
    collect = _ensure_target(COLLECT_LABEL, collect_loc, "CampCollect")
    if camp:
        unreal.log("HomeWorld: RSCamp day site ready " + CAMP_LABEL)
    if dream:
        unreal.log("HomeWorld: RSCamp dream stub ready " + DREAM_LABEL)
        unreal.log(
            "HomeWorld: DREAM: stub marker "
            + DREAM_LABEL
            + " — night placeholder convert; hw.Conversion.Test → recruit"
        )
    if collect:
        unreal.log("HomeWorld: RSCamp day collect marker ready " + COLLECT_LABEL)
    _log(
        "Done camp=%s dream=%s collect=%s. PIE night: hw.Conversion.Test at dream. "
        "Day: visit camp / collect markers (stub). Save KEEP-LOCAL."
        % (
            "ok" if camp else "FAIL",
            "ok" if dream else "FAIL",
            "ok" if collect else "FAIL",
        )
    )


if __name__ == "__main__":
    main()

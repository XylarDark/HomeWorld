# place_vs_mvp_rs_special_site.py
# RS-E: idempotent special cross-bonus hinge site on L_VS_MVP_Markers.
# Same landmark: GP_RS_SpecialSite + day/night collect markers.
# Prove: hw.RS.CollectDayBonus / hw.RS.CollectNightBonus / hw.RS.CrossBonusStatus (Safe-Build).
# Script-only — KEEP-LOCAL level save.

from __future__ import annotations

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "RSSpecial:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
FOLDER = "VS_MVP/Markers/RS_E"
SITE_LABEL = "GP_RS_SpecialSite"
DAY_LABEL = "GP_RS_Special_DayBonus"
NIGHT_LABEL = "GP_RS_Special_NightBonus"
SITE_OFFSET = unreal.Vector(0.0, 450.0, 0.0)
DAY_OFFSET = unreal.Vector(-60.0, 450.0, 40.0)
NIGHT_OFFSET = unreal.Vector(60.0, 450.0, 40.0)


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
        "GP_RS_HumanoidCamp",
        "GP_RS_AnimalDen",
    ):
        actor = find_actor_by_label(label)
        if actor:
            _log("special base from " + label)
            return actor.get_actor_location()
    return unreal.Vector(2600.0, 0.0, 0.0)


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
    _log("spawned " + label)
    return actor


def main() -> None:
    _log("start RS-E special cross-bonus site")
    if not _load_level():
        return
    base = _planet_base()
    site = _ensure_target(
        SITE_LABEL,
        unreal.Vector(base.x + SITE_OFFSET.x, base.y + SITE_OFFSET.y, base.z + SITE_OFFSET.z),
        "SpecialSite",
    )
    day_m = _ensure_target(
        DAY_LABEL,
        unreal.Vector(base.x + DAY_OFFSET.x, base.y + DAY_OFFSET.y, base.z + DAY_OFFSET.z),
        "DayBonus",
    )
    night_m = _ensure_target(
        NIGHT_LABEL,
        unreal.Vector(base.x + NIGHT_OFFSET.x, base.y + NIGHT_OFFSET.y, base.z + NIGHT_OFFSET.z),
        "NightBonus",
    )
    if site:
        unreal.log("HomeWorld: RSSpecial hinge site ready " + SITE_LABEL)
    if day_m:
        unreal.log("HomeWorld: RSSpecial day marker " + DAY_LABEL + " — hw.RS.CollectDayBonus")
    if night_m:
        unreal.log("HomeWorld: RSSpecial night marker " + NIGHT_LABEL + " — hw.RS.CollectNightBonus")
    _log(
        "Done site=%s day=%s night=%s. PIE: hw.RS.CollectDayBonus then hw.RS.CrossBonusStatus; "
        "hw.TimeOfDay.Phase 2; hw.RS.CollectNightBonus; hw.RS.CrossBonusStatus. Save KEEP-LOCAL."
        % ("ok" if site else "FAIL", "ok" if day_m else "FAIL", "ok" if night_m else "FAIL")
    )


if __name__ == "__main__":
    main()

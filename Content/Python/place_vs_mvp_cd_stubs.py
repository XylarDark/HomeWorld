# place_vs_mvp_cd_stubs.py — CD-A minigame markers + boss placeholder volume on L_VS_MVP_Markers.
# Planet / tutorial path only — never homestead. Run after Safe-Build.

from __future__ import annotations

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "CD-StubPlace:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
MINIGAME_CLASS = "/Script/HomeWorld.HomeWorldMinigameStubMarker"
BOSS_CLASS = "/Script/HomeWorld.HomeWorldBossPlaceholderVolume"
FOLDER = "VS_MVP/Markers/CD_A"

# EHomeWorldMinigameKind order: Heal=0, Nurture=1, Grow=2, Possess=3
MINIGAMES = (
    ("GP_CD_Minigame_Heal", 0, unreal.Vector(200.0, -400.0, 0.0)),
    ("GP_CD_Minigame_Nurture", 1, unreal.Vector(320.0, -400.0, 0.0)),
    ("GP_CD_Minigame_Grow", 2, unreal.Vector(440.0, -400.0, 0.0)),
    ("GP_CD_Minigame_Possess", 3, unreal.Vector(560.0, -400.0, 0.0)),
)
BOSS_LABEL = "GP_CD_BossPlaceholder"
BOSS_OFFSET = unreal.Vector(900.0, -550.0, 0.0)


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


def _planet_path_base() -> unreal.Vector:
    for label in (
        "CRUMB_Depart_Lookout",
        "CRUMB_Landing",
        "GP_RS_AnimalDen",
        "SM_Shrine_Return",
    ):
        actor = find_actor_by_label(label)
        if actor:
            _log("base from " + label)
            return actor.get_actor_location()
    _log("base fallback")
    return unreal.Vector(2800.0, 0.0, 0.0)


def _load_level() -> bool:
    if not unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        _log("Level missing — run place_vs_mvp_markers.py first")
        return False
    return bool(unreal.EditorLoadingAndSavingUtils.load_map(LEVEL_PATH))


def _ensure_minigame(cls, label: str, kind: int, loc: unreal.Vector):
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
            actor.set_folder_path(FOLDER)
        except Exception:
            pass
        _log("spawn " + label)
    try:
        actor.set_editor_property("minigame_kind", kind)
    except Exception as e:
        _log("minigame_kind warn " + label + ": " + str(e))
    return actor


def _ensure_boss(cls, label: str, loc: unreal.Vector):
    existing = find_actor_by_label(label)
    if existing:
        actor = existing
        actor.set_actor_location(loc, False, True)
        _log("reuse " + label)
        return actor
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(cls, loc)
    if not actor:
        _log("FAIL spawn boss volume")
        return None
    try:
        actor.set_actor_label(label)
        actor.set_folder_path(FOLDER)
    except Exception:
        pass
    _log("spawn " + label)
    return actor


def main() -> int:
    if not _load_level():
        return 1
    minigame_cls = unreal.load_class(None, MINIGAME_CLASS)
    boss_cls = unreal.load_class(None, BOSS_CLASS)
    if not minigame_cls or not boss_cls:
        _log("FAIL load C++ classes — run Safe-Build first")
        return 2

    base = _planet_path_base()
    ok = 0
    for label, kind, offset in MINIGAMES:
        if _ensure_minigame(minigame_cls, label, kind, base + offset):
            ok += 1

    if _ensure_boss(boss_cls, BOSS_LABEL, base + BOSS_OFFSET):
        ok += 1

    unreal.EditorLevelLibrary.save_current_level()
    _log(
        "DONE minigames=%d/4 boss=%s — PIE greps MINIGAME:* BOSS:PHASE_* BOSS:SEAL"
        % (min(4, ok), "ok" if ok >= 5 else "missing")
    )
    return 0 if ok >= 5 else 4


if __name__ == "__main__":
    raise SystemExit(main())

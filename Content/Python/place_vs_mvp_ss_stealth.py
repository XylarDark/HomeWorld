# place_vs_mvp_ss_stealth.py — SS-A spirit lit volumes on L_VS_MVP_Markers (planet path).
# Never homestead. Run after Safe-Build.

from __future__ import annotations

import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "SS-StubPlace:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
LIT_CLASS = "/Script/HomeWorld.HomeWorldSpiritLitVolume"
FOLDER = "VS_MVP/Markers/SS_A"

# EHomeWorldSpiritLitSourceKind: Campfire=0, NpcTorch=1, SpiritTorch=2, BodyMundaneTorch=3
VOLUMES = (
    ("GP_SS_Lit_Campfire", 0, unreal.Vector(120.0, -200.0, 0.0)),
    ("GP_SS_Lit_NpcTorch", 1, unreal.Vector(240.0, -200.0, 0.0)),
    ("GP_SS_Lit_SpiritTorch", 2, unreal.Vector(360.0, -200.0, 0.0)),
    ("GP_SS_Lit_BodyMundane", 3, unreal.Vector(480.0, -200.0, 0.0)),
)


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
        "GP_RS_AnimalDen",
        "GP_RS_HumanoidCamp",
        "GP_CD_BossPlaceholder",
        "CRUMB_Depart_Lookout",
    ):
        actor = find_actor_by_label(label)
        if actor:
            _log("base from " + label)
            return actor.get_actor_location()
    _log("base fallback")
    return unreal.Vector(3000.0, -150.0, 0.0)


def _load_level() -> bool:
    if not unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        _log("Level missing — run place_vs_mvp_markers.py first")
        return False
    return bool(unreal.EditorLoadingAndSavingUtils.load_map(LEVEL_PATH))


def _ensure_volume(cls, label: str, kind: int, loc: unreal.Vector):
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
        actor.set_editor_property("lit_source_kind", kind)
    except Exception as e:
        _log("lit_source_kind warn " + label + ": " + str(e))
    return actor


def main() -> int:
    if not _load_level():
        return 1
    lit_cls = unreal.load_class(None, LIT_CLASS)
    if not lit_cls:
        _log("FAIL load HomeWorldSpiritLitVolume — run Safe-Build first")
        return 2

    base = _planet_path_base()
    ok = 0
    for label, kind, offset in VOLUMES:
        if _ensure_volume(lit_cls, label, kind, base + offset):
            ok += 1

    unreal.EditorLevelLibrary.save_current_level()
    _log(
        "DONE volumes=%d/4 — PIE spirit: hw.TimeOfDay.Phase 2, walk GP_SS_Lit_* "
        "(grep STEALTH: LIT enter / ALERT / CLEAR; body ignores reveal volumes)"
        % ok
    )
    return 0 if ok >= 4 else 4


if __name__ == "__main__":
    raise SystemExit(main())

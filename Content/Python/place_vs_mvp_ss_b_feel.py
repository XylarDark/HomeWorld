# place_vs_mvp_ss_b_feel.py — SS-B NPC torch carriers + SS-A volume refresh on L_VS_MVP_Markers.
# Idempotent. Run after Safe-Build. Never homestead.

from __future__ import annotations

import importlib
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "SS-B-Feel:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
CARRIER_CLASS = "/Script/HomeWorld.HomeWorldSpiritNpcTorchCarrier"
FOLDER = "VS_MVP/Markers/SS_B"

# (label, patrol_enabled, offset from camp/den path base)
CARRIERS = (
    ("GP_SS_NpcTorch_CampPath", True, unreal.Vector(180.0, 120.0, 0.0)),
    ("GP_SS_NpcTorch_DenSit", False, unreal.Vector(-90.0, 220.0, 0.0)),
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


def _path_base() -> unreal.Vector:
    for label in ("GP_RS_HumanoidCamp", "GP_RS_AnimalDen", "CRUMB_Depart_Lookout"):
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


def _ensure_carrier(cls, label: str, patrol: bool, loc: unreal.Vector):
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
        actor.set_editor_property("b_patrol_enabled", patrol)
        actor.set_editor_property("lit_source_kind", 1)  # NpcTorch
    except Exception as exc:
        _log("prop warn " + label + ": " + str(exc))
    return actor


def main() -> int:
    if not _load_level():
        return 1

    # Refresh SS-A volumes (campfire / torch kinds) without duplicating.
    try:
        import place_vs_mvp_ss_stealth as ss_a

        importlib.reload(ss_a)
        ss_a.main()
    except Exception as exc:
        _log("SS-A refresh warn: " + str(exc))

    carrier_cls = unreal.load_class(None, CARRIER_CLASS)
    if not carrier_cls:
        _log("FAIL load HomeWorldSpiritNpcTorchCarrier — run Safe-Build first")
        return 2

    base = _path_base()
    ok = 0
    for label, patrol, offset in CARRIERS:
        if _ensure_carrier(carrier_cls, label, patrol, base + offset):
            ok += 1

    unreal.EditorLevelLibrary.save_current_level()
    _log(
        "DONE carriers=%d/2 — PIE spirit: hw.TimeOfDay.Phase 2; "
        "walk GP_SS_NpcTorch_* → STEALTH: LIT enter (NpcTorch); HUD alert bar; "
        "hw.Stealth.Status shows alert 0-1"
        % ok
    )
    return 0 if ok >= 1 else 3


if __name__ == "__main__":
    raise SystemExit(main())

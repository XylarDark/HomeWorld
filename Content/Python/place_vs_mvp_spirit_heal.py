# place_vs_mvp_spirit_heal.py
# NP-E V6: idempotent three AHomeWorldSpiritWisp actors at SM_SpiritWound (planet slice).
# Run after place_vs_mvp_markers.py; Safe-Build required for C++ actor class.

from __future__ import annotations

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "SpiritHeal:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
JSON_REL = os.path.join("AssetCreation", "Exports", "MVP_CRUMB_SPLINE.json")
WISP_CLASS = "/Script/HomeWorld.HomeWorldSpiritWisp"
HEAL_COMPONENT_CLASS = "/Script/HomeWorld.HomeWorldSpiritHealComponent"
FOLDER = "VS_MVP/Markers"

# Blender m offsets from spirit-wound site (Docs/03 §6 — three wisps around SM_SpiritWound_01)
DEFAULT_WOUND_BL = (-4.0, -115.0, -95.0)
WISP_SPECS = (
    ("GP_SpiritWisp_A", "Spirit_A", unreal.Vector(0.0, 0.0, 0.0)),
    ("GP_SpiritWisp_B", "Spirit_B", unreal.Vector(100.0, 50.0, 0.0)),
    ("GP_SpiritWisp_C", "Spirit_C", unreal.Vector(-100.0, 80.0, 0.0)),
)


def _log(msg: str) -> None:
    unreal.log(PREFIX + " " + str(msg))
    print(PREFIX, msg)


def _project_root():
    cwd = os.getcwd()
    if os.path.isdir(cwd) and "Content" in (os.listdir(cwd) or []):
        return cwd
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", ".."))


def blender_to_ue_cm(loc):
    x, y, z = float(loc[0]), float(loc[1]), float(loc[2])
    return unreal.Vector(x * 100.0, -y * 100.0, z * 100.0)


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


def _spirit_wound_base():
    wound = find_actor_by_label("SM_SpiritWound_01")
    if wound:
        return wound.get_actor_location()
    root = _project_root()
    json_path = os.path.join(root, JSON_REL)
    if os.path.isfile(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            anchors = data.get("anchors") or {}
            for key in ("SM_SpiritWound_01", "SM_SpiritWound"):
                entry = anchors.get(key)
                if isinstance(entry, dict) and entry.get("location"):
                    return blender_to_ue_cm(entry["location"])
        except Exception:
            pass
    return blender_to_ue_cm(DEFAULT_WOUND_BL)


def _configure_spirit_id(actor, spirit_id: str) -> None:
    comp_class = unreal.load_class(None, HEAL_COMPONENT_CLASS)
    if not comp_class or not hasattr(actor, "get_component_by_class"):
        return
    comp = actor.get_component_by_class(comp_class)
    if comp and hasattr(comp, "configure_spirit"):
        comp.configure_spirit(unreal.Name(spirit_id))


def _ensure_wisp(label: str, spirit_id: str, offset: unreal.Vector):
    existing = find_actor_by_label(label)
    if existing:
        _log("Reused %s" % label)
        _configure_spirit_id(existing, spirit_id)
        return existing

    wisp_class = unreal.load_class(None, WISP_CLASS)
    if not wisp_class:
        _log("HomeWorldSpiritWisp not found — run Safe-Build first")
        return None

    base = _spirit_wound_base()
    loc = base + offset
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(wisp_class, loc, unreal.Rotator(0, 0, 0))
    if not actor:
        _log("Failed to spawn %s" % label)
        return None
    actor.set_actor_label(label)
    actor.set_folder_path(FOLDER)
    _configure_spirit_id(actor, spirit_id)
    _log("Spawned %s @ %s (id=%s)" % (label, loc, spirit_id))
    return actor


def main() -> int:
    if not _load_level():
        return 1

    created = 0
    for label, spirit_id, offset in WISP_SPECS:
        if _ensure_wisp(label, spirit_id, offset):
            created += 1

    if created < len(WISP_SPECS):
        return 1

    try:
        unreal.EditorLevelLibrary.save_current_level()
        _log("Saved level")
    except Exception as exc:
        _log("Save warning: " + str(exc))

    _log("Done. PIE night: hw.Gather.Flowers 1, hw.TimeOfDay.Phase 2, Interact (E) at wisps for HEAL: logs.")
    return 0


if __name__ == "__main__":
    code = main()
    if code != 0:
        unreal.log_error(PREFIX + " finished with code %s" % code)

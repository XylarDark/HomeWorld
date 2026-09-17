# place_vs_mvp_nurture.py
# NP-E V7: idempotent N1_Crop + N2_Stored AHomeWorldNurtureTarget on homestead (L_VS_MVP_Markers).
# Run after place_vs_mvp_gp.py; Safe-Build required.

from __future__ import annotations

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "Nurture:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
JSON_REL = os.path.join("AssetCreation", "Exports", "MVP_CRUMB_SPLINE.json")
TARGET_CLASS = "/Script/HomeWorld.HomeWorldNurtureTarget"
NURTURE_COMPONENT_CLASS = "/Script/HomeWorld.HomeWorldNurtureComponent"
FOLDER = "VS_MVP/Markers"

# Offsets from SM_Cabin anchor (Blender m -> UE cm applied in blender_to_ue)
NURTURE_SPECS = (
    ("GP_N1_Crop", "N1_Crop", "RES_SEED", unreal.Vector(200.0, -200.0, 0.0)),
    ("GP_N2_Stored", "N2_Stored", "RES_WOOD", unreal.Vector(-250.0, 300.0, 0.0)),
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


def _homestead_cabin_base():
    cabin = find_actor_by_label("SM_Cabin")
    if cabin:
        return cabin.get_actor_location()
    gp = find_actor_by_label("GP_PlayerStart")
    if gp:
        return gp.get_actor_location()
    root = _project_root()
    json_path = os.path.join(root, JSON_REL)
    if os.path.isfile(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            entry = (data.get("anchors") or {}).get("SM_Cabin")
            if isinstance(entry, dict) and entry.get("location"):
                return blender_to_ue_cm(entry["location"])
        except Exception:
            pass
    return blender_to_ue_cm((-6.0, 1.0, 0.0))


def _member_name_variants(enum_name: str):
    """Candidate UE Python enum member names for EHomeWorldNurtureTargetId."""
    variants = [enum_name]
    if enum_name.upper().startswith("N1"):
        variants.extend(
            [
                "N1_Crop",
                "N1_CROP",
                "N1_crop",
                "NEWENUMERATOR0",
                "NEW_ENUMERATOR0",
            ]
        )
    elif enum_name.upper().startswith("N2"):
        variants.extend(
            [
                "N2_Stored",
                "N2_STORED",
                "N2_stored",
                "NEWENUMERATOR1",
                "NEW_ENUMERATOR1",
            ]
        )
    seen = set()
    ordered = []
    for name in variants:
        if name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered


def _find_nurture_target_enum_type():
    """Resolve enum type: EHomeWorldNurtureTargetId, scan dir(unreal), or component CDO."""
    for type_name in ("EHomeWorldNurtureTargetId", "HomeWorldNurtureTargetId"):
        enum_type = getattr(unreal, type_name, None)
        if enum_type is not None:
            return type_name, enum_type

    for name in sorted(dir(unreal)):
        if "NurtureTarget" in name and "Id" in name and not name.startswith("_"):
            enum_type = getattr(unreal, name, None)
            if enum_type is not None:
                return name, enum_type

    comp_class = unreal.load_class(None, NURTURE_COMPONENT_CLASS)
    if comp_class:
        try:
            cdo = unreal.get_default_object(comp_class)
            if cdo and hasattr(cdo, "get_editor_property"):
                sample = cdo.get_editor_property("target_id")
                if sample is not None:
                    enum_type = type(sample)
                    return getattr(enum_type, "__name__", "target_id_enum"), enum_type
        except Exception:
            pass

    return None, None


def _resolve_nurture_target_id(enum_name: str):
    type_name, enum_type = _find_nurture_target_enum_type()
    if enum_type is None:
        _log("Nurture target enum missing — run Safe-Build first")
        return None

    for member in _member_name_variants(enum_name):
        target_id = getattr(enum_type, member, None)
        if target_id is not None:
            if member != enum_name:
                _log("Resolved %s via %s.%s" % (enum_name, type_name, member))
            return target_id

    # Last resort: match dir(enum_type) for N1/N2 substring (handles odd exporter names).
    needle = "N1" if enum_name.upper().startswith("N1") else "N2"
    for member in dir(enum_type):
        if member.startswith("_") or needle not in member:
            continue
        target_id = getattr(enum_type, member, None)
        if target_id is not None:
            _log("Resolved %s via %s.%s (dir scan)" % (enum_name, type_name, member))
            return target_id

    _log("%s.%s not found (tried %s)" % (type_name, enum_name, ", ".join(_member_name_variants(enum_name))))
    return None


def _configure_target(actor, target_id, res_id: str) -> None:
    comp_class = unreal.load_class(None, NURTURE_COMPONENT_CLASS)
    if not comp_class or not hasattr(actor, "get_component_by_class"):
        return
    comp = actor.get_component_by_class(comp_class)
    if not comp or target_id is None:
        return

    res_name = unreal.Name(res_id)

    if hasattr(comp, "configure_target"):
        try:
            comp.configure_target(target_id, res_name)
            return
        except TypeError as exc:
            _log("configure_target failed (%s); trying set_editor_property" % exc)

    for target_prop, res_prop in (
        ("target_id", "required_resource_id"),
        ("TargetId", "RequiredResourceId"),
    ):
        try:
            comp.set_editor_property(target_prop, target_id)
            comp.set_editor_property(res_prop, res_name)
            _log("Configured via set_editor_property(%s)" % target_prop)
            return
        except Exception:
            continue

    _log("Could not configure nurture target on %s" % actor.get_name())


def _ensure_target(label: str, enum_name: str, res_id: str, offset: unreal.Vector):
    target_id = _resolve_nurture_target_id(enum_name)
    if target_id is None:
        return None

    existing = find_actor_by_label(label)
    if existing:
        _log("Reused %s" % label)
        _configure_target(existing, target_id, res_id)
        return existing

    target_class = unreal.load_class(None, TARGET_CLASS)
    if not target_class:
        _log("HomeWorldNurtureTarget not found — run Safe-Build first")
        return None

    base = _homestead_cabin_base()
    loc = base + offset
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(target_class, loc, unreal.Rotator(0, 0, 0))
    if not actor:
        _log("Failed to spawn %s" % label)
        return None
    actor.set_actor_label(label)
    actor.set_folder_path(FOLDER)
    _configure_target(actor, target_id, res_id)
    _log("Spawned %s @ %s (target=%s res=%s)" % (label, loc, enum_name, res_id))
    return actor


def main() -> int:
    if not _load_level():
        return 1

    ok = 0
    for label, enum_name, res_id, offset in NURTURE_SPECS:
        if _ensure_target(label, enum_name, res_id, offset):
            ok += 1

    if ok < len(NURTURE_SPECS):
        return 1

    try:
        unreal.EditorLevelLibrary.save_current_level()
        _log("Saved level")
    except Exception as exc:
        _log("Save warning: " + str(exc))

    _log("Done. PIE night at homestead: hw.Gather with seed/herb/wood, Phase 2, Interact (E) for NURTURE: logs.")
    return 0


if __name__ == "__main__":
    code = main()
    if code != 0:
        unreal.log_error(PREFIX + " finished with code %s" % code)

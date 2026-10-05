# assign_prototype_material_map.py
# Lead-locked APPROVE MATERIAL MAP: create MI_* from Docs/handoffs proposal,
# bind onto prototype SM_* slots, retarget mesh-folder master cites to
# /Game/HomeWorld/Materials/Masters/, then delete Homestead M_GatherHerb + M_Nurtured dups.
# No 11th master. Do not touch sound plugins.

from __future__ import annotations

import json
import os
import sys
from datetime import datetime

try:
    import unreal
except ImportError:
    print("assign_prototype_material_map: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "assign_prototype_material_map:"
MASTERS_DIR = "/Game/HomeWorld/Materials/Masters"
INSTANCES_DIR = "/Game/HomeWorld/Materials/Instances"
REPORT_REL = os.path.join("Saved", "prototype_material_assign_report.json")

# Flat mat path -> (MI name, master name) per approved proposal table.
FLAT_TO_MI = {
    "/Game/HomeWorld/Meshes/Homestead/Cabin_BrownTimber": ("MI_Cabin_BrownTimber", "M_WoodCabin"),
    "/Game/HomeWorld/Meshes/Homestead/Cabin_LightWood": ("MI_Cabin_LightWood", "M_WoodCabin"),
    "/Game/HomeWorld/Meshes/Homestead/Cabin_DoorBrown": ("MI_Cabin_DoorBrown", "M_WoodCabin"),
    "/Game/HomeWorld/Meshes/Homestead/Cabin_BandBrown": ("MI_Cabin_BandBrown", "M_WoodCabin"),
    "/Game/HomeWorld/Meshes/Homestead/Cabin_DarkSlate": ("MI_Cabin_DarkSlate", "M_WoodCabin"),
    "/Game/HomeWorld/Meshes/Homestead/Cabin_WarmAmber": ("MI_Cabin_WindowWarm", "M_WoodCabin"),
    "/Game/HomeWorld/Meshes/Homestead/Cabin_StoneGray": ("MI_Cabin_StoneGray", "M_CliffRock"),
    "/Game/HomeWorld/Meshes/Homestead/Cabin_StoneCapGray": ("MI_Cabin_StoneCapGray", "M_CliffRock"),
    "/Game/HomeWorld/Meshes/Homestead/Cabin_BlackIron": ("MI_Cabin_BlackIron", "M_CliffRock"),
    "/Game/HomeWorld/Meshes/Homestead/Cabin_TanCeramic": ("MI_Cabin_TanCeramic", "M_CliffRock"),
    "/Game/HomeWorld/Meshes/Homestead/Cabin_OliveHerb": ("MI_Cabin_OliveHerb", "M_GatherHerb"),
    "/Game/HomeWorld/Meshes/Gatherables/Portal_Crystal_Cyan": ("MI_Portal_Crystal_Cyan", "M_SpiritUnlit"),
    "/Game/HomeWorld/Meshes/Gatherables/Portal_Crystal_LightCyan": ("MI_Portal_Crystal_LightCyan", "M_SpiritUnlit"),
    "/Game/HomeWorld/Meshes/Gatherables/Portal_Stone_Gray": ("MI_Portal_Stone_Gray", "M_CliffRock"),
    "/Game/HomeWorld/Meshes/Gatherables/Portal_Stone_Midgray": ("MI_Portal_Stone_Midgray", "M_CliffRock"),
    "/Game/HomeWorld/Meshes/Gatherables/Portal_Stone_Lightgray": ("MI_Portal_Stone_Lightgray", "M_CliffRock"),
    "/Game/HomeWorld/Meshes/Gatherables/Flowers_DarkGreen": ("MI_Flowers_DarkGreen", "M_GatherHerb"),
    "/Game/HomeWorld/Meshes/Gatherables/Flowers_Olive": ("MI_Flowers_Olive", "M_GatherHerb"),
    "/Game/HomeWorld/Meshes/Gatherables/Flowers_Lilac": ("MI_Flowers_Lilac", "M_GatherHerb"),
    "/Game/HomeWorld/Meshes/Gatherables/Flowers_Purple": ("MI_Flowers_Purple", "M_GatherHerb"),
}

# Slot-name / current-mat basename -> MI or master path to bind.
# Used after MI creation; keys are slot_name strings on the mesh.
SLOT_NAME_TO_MI = {
    "Cabin_WarmAmber": "MI_Cabin_WindowWarm",
    "Cabin_LightWood": "MI_Cabin_LightWood",
    "Cabin_DoorBrown": "MI_Cabin_DoorBrown",
    "Cabin_StoneGray": "MI_Cabin_StoneGray",
    "Cabin_StoneCapGray": "MI_Cabin_StoneCapGray",
    "Cabin_BlackIron": "MI_Cabin_BlackIron",
    "Cabin_BandBrown": "MI_Cabin_BandBrown",
    "Cabin_OliveHerb": "MI_Cabin_OliveHerb",
    "Cabin_TanCeramic": "MI_Cabin_TanCeramic",
    "Cabin_DarkSlate": "MI_Cabin_DarkSlate",
    "Cabin_BrownTimber": "MI_Cabin_BrownTimber",
    "Portal_Stone_Gray": "MI_Portal_Stone_Gray",
    "Portal_Stone_Midgray": "MI_Portal_Stone_Midgray",
    "Portal_Stone_Lightgray": "MI_Portal_Stone_Lightgray",
    "Portal_Crystal_Cyan": "MI_Portal_Crystal_Cyan",
    "Portal_Crystal_LightCyan": "MI_Portal_Crystal_LightCyan",
    "Flowers_Olive": "MI_Flowers_Olive",
    "Flowers_Purple": "MI_Flowers_Purple",
    "Flowers_Lilac": "MI_Flowers_Lilac",
    "Flowers_DarkGreen": "MI_Flowers_DarkGreen",
}

# Mesh-folder master basename -> real Masters path (retarget).
MESH_FOLDER_MASTER_RETARGET = {
    "M_WoodCabin": f"{MASTERS_DIR}/M_WoodCabin",
    "M_CliffRock": f"{MASTERS_DIR}/M_CliffRock",
    "M_PathStone": f"{MASTERS_DIR}/M_PathStone",
    "M_GatherHerb": f"{MASTERS_DIR}/M_GatherHerb",
    "M_Nurtured": f"{MASTERS_DIR}/M_Nurtured",
    "M_StylizedGrass": f"{MASTERS_DIR}/M_StylizedGrass",
    "M_WoodWild": f"{MASTERS_DIR}/M_WoodWild",
    "M_SpiritUnlit": f"{MASTERS_DIR}/M_SpiritUnlit",
    "M_FoliageCard": f"{MASTERS_DIR}/M_FoliageCard",
    "M_BeastStylized": f"{MASTERS_DIR}/M_BeastStylized",
}

PROTOTYPE_MESHES = [
    "/Game/HomeWorld/Meshes/Homestead/SM_Cabin_Prototype",
    "/Game/HomeWorld/Meshes/Homestead/SM_Cabin_CornerPosts",
    "/Game/HomeWorld/Meshes/Homestead/SM_Cliff_CabinFace",
    "/Game/HomeWorld/Meshes/Homestead/SM_Cliff_LookoutFace",
    "/Game/HomeWorld/Meshes/Homestead/SM_Cliff_Rear",
    "/Game/HomeWorld/Meshes/Homestead/SM_PathStone_A",
    "/Game/HomeWorld/Meshes/Homestead/SM_PathStone_B",
    "/Game/HomeWorld/Meshes/Homestead/SM_PathStone_C",
    "/Game/HomeWorld/Meshes/Homestead/SM_Planter_A",
    "/Game/HomeWorld/Meshes/Homestead/SM_Planter_B",
    "/Game/HomeWorld/Meshes/Homestead/SM_Planter_C",
    "/Game/HomeWorld/Meshes/Homestead/SM_Garden_Fence_Seg",
    "/Game/HomeWorld/Meshes/Gatherables/SM_Portal_Prototype",
    "/Game/HomeWorld/Meshes/Gatherables/SM_Flowers_Prototype",
]

DUP_DELETE = [
    "/Game/HomeWorld/Meshes/Homestead/M_GatherHerb",
    "/Game/HomeWorld/Meshes/Homestead/M_Nurtured",
]


def _log(msg, data=None):
    line = PREFIX + " " + str(msg)
    if data is not None:
        line += " " + str(data)
    unreal.log(line)
    print(line)


def _norm(path: str) -> str:
    if not path:
        return ""
    p = str(path)
    if "." in p.rsplit("/", 1)[-1]:
        return p.rsplit(".", 1)[0]
    return p


def _project_root():
    cwd = os.getcwd()
    if os.path.isdir(os.path.join(cwd, "Content")):
        return cwd
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", ".."))


def _ensure_dir(path: str) -> None:
    if not unreal.EditorAssetLibrary.does_directory_exist(path):
        unreal.EditorAssetLibrary.make_directory(path)
        _log("Created folder", {"path": path})


def _load(path: str):
    if not unreal.EditorAssetLibrary.does_asset_exist(path):
        return None
    return unreal.EditorAssetLibrary.load_asset(path)


def _try_read_basecolor(mat_asset):
    """Best-effort BaseColor from a material or MIC."""
    if mat_asset is None:
        return None
    try:
        # MIC path
        if isinstance(mat_asset, unreal.MaterialInstanceConstant):
            val = unreal.MaterialEditingLibrary.get_material_instance_vector_parameter_value(
                mat_asset, "BaseColor"
            )
            if val is not None:
                return val
    except Exception:
        pass
    try:
        val = unreal.MaterialEditingLibrary.get_material_default_vector_parameter_value(
            mat_asset, "BaseColor"
        )
        if val is not None:
            return val
    except Exception:
        pass
    # Some imports use "Color" / "Tint"
    for pname in ("Color", "Tint", "Base_Color", "albedo"):
        try:
            if isinstance(mat_asset, unreal.MaterialInstanceConstant):
                val = unreal.MaterialEditingLibrary.get_material_instance_vector_parameter_value(
                    mat_asset, pname
                )
            else:
                val = unreal.MaterialEditingLibrary.get_material_default_vector_parameter_value(
                    mat_asset, pname
                )
            if val is not None:
                return val
        except Exception:
            continue
    return None


def ensure_mi(mi_name: str, master_name: str, flat_path: str, report: dict):
    mi_path = f"{INSTANCES_DIR}/{mi_name}"
    master_path = f"{MASTERS_DIR}/{master_name}"
    parent = _load(master_path)
    if parent is None:
        report["mi_failed"].append({"mi": mi_name, "reason": "master_missing", "master": master_path})
        _log("Master missing", {"master": master_path})
        return None

    created = False
    if unreal.EditorAssetLibrary.does_asset_exist(mi_path):
        mi = _load(mi_path)
        _log("MI exists", {"path": mi_path})
        # Ensure parent is correct
        try:
            if mi and isinstance(mi, unreal.MaterialInstanceConstant):
                cur_parent = mi.get_editor_property("parent")
                if cur_parent is None or _norm(cur_parent.get_path_name()) != master_path:
                    unreal.MaterialEditingLibrary.set_material_instance_parent(mi, parent)
                    _log("Reparented MI", {"mi": mi_path, "parent": master_path})
        except Exception as exc:
            _log("Reparent note", {"mi": mi_path, "err": str(exc)})
    else:
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        factory = unreal.MaterialInstanceConstantFactoryNew()
        try:
            factory.set_editor_property("initial_parent", parent)
        except Exception:
            pass
        mi = asset_tools.create_asset(
            mi_name, INSTANCES_DIR, unreal.MaterialInstanceConstant, factory
        )
        if mi is None:
            report["mi_failed"].append({"mi": mi_name, "reason": "create_failed"})
            _log("MI create failed", {"mi": mi_name})
            return None
        created = True
        try:
            unreal.MaterialEditingLibrary.set_material_instance_parent(mi, parent)
        except Exception:
            pass
        _log("Created MI", {"path": mi_path, "parent": master_path})

    # Copy BaseColor from flat when possible
    flat = _load(flat_path)
    color = _try_read_basecolor(flat)
    color_copied = False
    if color is not None and mi is not None:
        try:
            unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(
                mi, "BaseColor", color
            )
            color_copied = True
        except Exception as exc:
            _log("BaseColor copy failed", {"mi": mi_name, "err": str(exc)})

    try:
        unreal.MaterialEditingLibrary.update_material_instance(mi)
    except Exception:
        pass
    unreal.EditorAssetLibrary.save_asset(mi_path)

    entry = {
        "mi": mi_path,
        "master": master_path,
        "flat": flat_path,
        "created": created,
        "basecolor_copied": color_copied,
    }
    report["mi_created_or_ensured"].append(entry)
    return mi_path


def _resolve_bind_target(slot_name: str, current_mat_path: str, mi_cache: dict) -> str | None:
    """Return asset path to bind onto this slot."""
    if slot_name in SLOT_NAME_TO_MI:
        mi_name = SLOT_NAME_TO_MI[slot_name]
        return f"{INSTANCES_DIR}/{mi_name}"

    # Retarget mesh-folder masters to Materials/Masters
    basename = (current_mat_path or "").rsplit("/", 1)[-1]
    if basename in MESH_FOLDER_MASTER_RETARGET:
        # Prefer MI if we somehow keyed it; else master
        return MESH_FOLDER_MASTER_RETARGET[basename]

    if slot_name in MESH_FOLDER_MASTER_RETARGET:
        return MESH_FOLDER_MASTER_RETARGET[slot_name]

    # Already on Masters?
    if current_mat_path.startswith(MASTERS_DIR) or current_mat_path.startswith(INSTANCES_DIR):
        return current_mat_path

    return None


def bind_mesh(mesh_path: str, report: dict) -> None:
    mesh = _load(mesh_path)
    if mesh is None or not isinstance(mesh, unreal.StaticMesh):
        report["mesh_bind_failed"].append({"mesh": mesh_path, "reason": "missing"})
        _log("Mesh missing", {"path": mesh_path})
        return

    try:
        static_mats = list(mesh.get_editor_property("static_materials"))
    except Exception as exc:
        report["mesh_bind_failed"].append({"mesh": mesh_path, "reason": str(exc)})
        return

    new_list = []
    changed = 0
    slot_report = []
    for i, sm in enumerate(static_mats):
        try:
            slot_name = str(sm.material_slot_name)
        except Exception:
            slot_name = ""
        try:
            cur = sm.material_interface
            cur_path = _norm(cur.get_path_name()) if cur else ""
        except Exception:
            cur_path = ""

        target_path = _resolve_bind_target(slot_name, cur_path, {})
        if not target_path:
            new_list.append(sm)
            slot_report.append({"index": i, "slot": slot_name, "action": "unmapped", "from": cur_path})
            continue

        if _norm(cur_path) == _norm(target_path):
            new_list.append(sm)
            slot_report.append({"index": i, "slot": slot_name, "action": "skip", "path": target_path})
            continue

        target = _load(target_path)
        if target is None:
            new_list.append(sm)
            slot_report.append({"index": i, "slot": slot_name, "action": "target_missing", "path": target_path})
            continue

        try:
            sm.set_editor_property("material_interface", target)
        except Exception:
            try:
                # Rebuild StaticMaterial
                sm = unreal.StaticMaterial(
                    material_interface=target,
                    material_slot_name=slot_name or sm.material_slot_name,
                    imported_material_slot_name=getattr(sm, "imported_material_slot_name", ""),
                )
            except Exception as exc2:
                slot_report.append({"index": i, "slot": slot_name, "action": "set_failed", "err": str(exc2)})
                new_list.append(sm)
                continue
        new_list.append(sm)
        changed += 1
        slot_report.append({"index": i, "slot": slot_name, "action": "bound", "from": cur_path, "to": target_path})

    if changed:
        try:
            mesh.set_editor_property("static_materials", new_list)
            unreal.EditorAssetLibrary.save_asset(mesh_path)
            _log("Bound mesh", {"mesh": mesh_path, "changed": changed})
        except Exception as exc:
            report["mesh_bind_failed"].append({"mesh": mesh_path, "reason": "save:" + str(exc)})
            _log("Bind save failed", {"mesh": mesh_path, "err": str(exc)})
            return

    report["meshes_bound"].append({"mesh": mesh_path, "changed": changed, "slots": slot_report})


def retarget_and_verify_dups(report: dict) -> bool:
    """Ensure no prototype mesh still cites Homestead M_GatherHerb / M_Nurtured."""
    ok = True
    remaining = []
    for mesh_path in PROTOTYPE_MESHES:
        mesh = _load(mesh_path)
        if mesh is None:
            continue
        try:
            static_mats = list(mesh.get_editor_property("static_materials"))
        except Exception:
            continue
        for i, sm in enumerate(static_mats):
            try:
                cur = sm.material_interface
                cur_path = _norm(cur.get_path_name()) if cur else ""
            except Exception:
                cur_path = ""
            for dup in DUP_DELETE:
                if cur_path == dup:
                    remaining.append({"mesh": mesh_path, "slot": i, "mat": cur_path})
                    ok = False
    report["dup_refs_after_retarget"] = remaining
    report["dup_retarget_clean"] = ok
    _log("Dup retarget verify", {"clean": ok, "remaining": remaining})
    return ok


def delete_dups(report: dict) -> None:
    for dup in DUP_DELETE:
        if not unreal.EditorAssetLibrary.does_asset_exist(dup):
            report["dups_deleted"].append({"path": dup, "status": "already_absent"})
            continue
        # Final referencer check
        try:
            refs = list(unreal.EditorAssetLibrary.find_package_referencers_for_asset(dup, False) or [])
        except Exception as exc:
            refs = ["error:" + str(exc)]
        # Filter self
        refs = [r for r in refs if _norm(str(r)) != dup]
        report["dup_refs_at_delete"] = report.get("dup_refs_at_delete", {})
        report["dup_refs_at_delete"][dup] = [str(r) for r in refs]
        if refs:
            # Still referenced — do not delete
            report["dups_deleted"].append({"path": dup, "status": "blocked_refs", "refs": [str(r) for r in refs]})
            _log("Dup delete blocked", {"path": dup, "refs": [str(r) for r in refs]})
            continue
        ok = unreal.EditorAssetLibrary.delete_asset(dup)
        report["dups_deleted"].append({"path": dup, "status": "deleted" if ok else "delete_failed"})
        _log("Deleted dup", {"path": dup, "ok": ok})


def main():
    _log("BEGIN Lead-approved material map assign")
    report = {
        "started": datetime.now().isoformat(timespec="seconds"),
        "mi_created_or_ensured": [],
        "mi_failed": [],
        "meshes_bound": [],
        "mesh_bind_failed": [],
        "dups_deleted": [],
        "notes": [],
    }

    _ensure_dir("/Game/HomeWorld/Materials")
    _ensure_dir(INSTANCES_DIR)

    # A1: create MI_*
    for flat_path, (mi_name, master_name) in FLAT_TO_MI.items():
        ensure_mi(mi_name, master_name, flat_path, report)

    # A2: bind meshes (MI slots + retarget mesh-folder masters)
    for mesh_path in PROTOTYPE_MESHES:
        bind_mesh(mesh_path, report)

    # C: retarget verify then delete the two dups only
    clean = retarget_and_verify_dups(report)
    if clean:
        delete_dups(report)
    else:
        # Force retarget on remaining then retry delete
        report["notes"].append("First verify dirty; rebinding planters then re-verify")
        for mesh_path in (
            "/Game/HomeWorld/Meshes/Homestead/SM_Planter_A",
            "/Game/HomeWorld/Meshes/Homestead/SM_Planter_B",
            "/Game/HomeWorld/Meshes/Homestead/SM_Planter_C",
        ):
            bind_mesh(mesh_path, report)
        clean2 = retarget_and_verify_dups(report)
        if clean2:
            delete_dups(report)
        else:
            report["notes"].append("Dup delete skipped — refs remain after retarget")

    report["finished"] = datetime.now().isoformat(timespec="seconds")
    out = os.path.join(_project_root(), REPORT_REL)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    _log("Wrote report", {"path": out})
    _log("DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)

# assign_vs_mvp_materials.py
# NP-B: Assign Docs/02 ten masters onto DRESS_* StaticMesh actors in L_VS_MVP_Markers.
# Run in Unreal Editor (Tools > Execute Python Script) or MCP execute_python_script.
# Prerequisites: place_vs_mvp_markers.py, place_vs_mvp_dress.py, create_master_materials.py on Windows host.
# Idempotent: skips slots already using the resolved material; saves level locally (no .uasset commit).

from __future__ import annotations

import importlib
import sys

try:
    import unreal
except ImportError:
    print("assign_vs_mvp_materials: Run inside Unreal Editor.")
    sys.exit(1)

import homeworld_vs_mvp_material_rules as rules_mod

PREFIX = "assign_vs_mvp_materials:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"


def _log(msg, data=None):
    line = PREFIX + " " + str(msg)
    if data is not None:
        line += " " + str(data)
    unreal.log(line)
    print(line)


def _normalize_asset_path(path: str) -> str:
    if not path:
        return ""
    # /Game/.../M_Foo.M_Foo -> /Game/.../M_Foo
    if "." in path.rsplit("/", 1)[-1]:
        return path.rsplit(".", 1)[0]
    return path


def _material_path(material_interface) -> str:
    if not material_interface:
        return ""
    try:
        return _normalize_asset_path(str(material_interface.get_path_name()))
    except Exception:
        return ""


def _load_material_interface(asset_path: str):
    if not unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        return None
    asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    if asset is None:
        return None
    return asset


def resolve_material_for_master(master_name: str):
    """Load MI if present, else master material."""
    for candidate in rules_mod.material_asset_candidates(master_name):
        mat = _load_material_interface(candidate)
        if mat is not None:
            _log("Resolved material", {"master": master_name, "path": candidate})
            return mat, candidate
    _log("Material missing for master", {"master": master_name})
    return None, None


def _is_dress_actor(actor) -> bool:
    try:
        label = actor.get_actor_label()
    except Exception:
        label = ""
    if label.startswith(rules_mod.DRESS_LABEL_PREFIX):
        return True
    try:
        folder = str(actor.get_folder_path()).replace("\\", "/")
    except Exception:
        folder = ""
    return folder == rules_mod.DRESS_FOLDER


def _collect_dress_actors():
    actors = []
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        if not isinstance(actor, unreal.StaticMeshActor):
            continue
        if _is_dress_actor(actor):
            actors.append(actor)
    return actors


def _assign_materials_on_actor(actor, material_cache: dict) -> dict:
    """Return stats dict: assigned, skipped, missing_master, unmapped."""
    stats = {"assigned": 0, "skipped": 0, "missing_master": 0, "unmapped": 0}
    label = actor.get_actor_label()
    mesh_name = rules_mod.mesh_basename_from_actor_label(label)
    if not mesh_name:
        mesh_name = label

    master = rules_mod.resolve_master_for_mesh(mesh_name)
    if not master:
        _log("No master rule for mesh", {"label": label, "mesh": mesh_name})
        stats["unmapped"] += 1
        return stats

    if master not in material_cache:
        mat, path = resolve_material_for_master(master)
        material_cache[master] = (mat, path)
    else:
        mat, path = material_cache[master]

    if mat is None:
        stats["missing_master"] += 1
        return stats

    sm_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
    if not sm_comp:
        _log("No StaticMeshComponent", {"label": label})
        return stats

    try:
        slot_count = int(sm_comp.get_num_materials())
    except Exception:
        slot_count = 0
    if slot_count < 1:
        static_mesh = sm_comp.get_static_mesh()
        if static_mesh:
            try:
                slot_count = len(static_mesh.static_materials)
            except Exception:
                slot_count = 1
        else:
            slot_count = 1

    target_path = _normalize_asset_path(path)
    for slot in range(slot_count):
        current_path = _normalize_asset_path(_material_path(sm_comp.get_material(slot)))
        if current_path == target_path:
            stats["skipped"] += 1
            continue
        sm_comp.set_material(slot, mat)
        stats["assigned"] += 1

    if stats["assigned"]:
        _log(
            "Assigned master",
            {"label": label, "mesh": mesh_name, "master": master, "material": target_path, "slots": slot_count},
        )
    elif stats["skipped"]:
        _log("Already assigned (skip)", {"label": label, "master": master, "material": target_path})

    return stats


def ensure_level_loaded():
    import place_vs_mvp_markers

    importlib.reload(place_vs_mvp_markers)
    if not unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        _log("Level missing — run place_vs_mvp_markers.py first", {"path": LEVEL_PATH})
        return False
    ok = unreal.EditorLevelLibrary.load_level(LEVEL_PATH)
    _log("Loaded level", {"path": LEVEL_PATH, "ok": ok})
    return bool(ok)


def smoke_nightmix_mpc():
    """Optional: set NightMix 0 then 0.85 on MPC for visual smoke."""
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        _log("NightMix smoke skipped — no editor world")
        return

    import place_vs_mvp_markers

    importlib.reload(place_vs_mvp_markers)
    mpc_asset = place_vs_mvp_markers.create_nightmix_mpc()
    if not mpc_asset:
        _log("NightMix smoke skipped — MPC missing")
        return

    for value in (0.0, 0.85):
        try:
            unreal.KismetMaterialLibrary.set_scalar_parameter_value(
                world, mpc_asset, rules_mod.MPC_SCALAR_NAME, value
            )
            _log("NightMix smoke set", {"NightMix": value, "mpc": rules_mod.MPC_PATH})
        except Exception as exc:
            _log("NightMix smoke failed", {"NightMix": value, "error": str(exc)})
            break


def main(smoke_nightmix: bool = True) -> int:
    _log("Start VS_MVP material assign (NP-B)")
    _log(
        "FALLBACK: scripted glide CRUMB_* only; portal SM_Shrine_Homestead <-> SM_Shrine_Return (no free-flight)"
    )

    if not ensure_level_loaded():
        return 1

    dress_actors = _collect_dress_actors()
    _log("Dress actors found", {"count": len(dress_actors)})

    if not dress_actors:
        _log("No DRESS_* actors — run place_vs_mvp_dress.py first")
        return 1

    material_cache: dict = {}
    totals = {"assigned": 0, "skipped": 0, "missing_master": 0, "unmapped": 0, "actors": 0}

    for actor in dress_actors:
        stats = _assign_materials_on_actor(actor, material_cache)
        totals["actors"] += 1
        for key in ("assigned", "skipped", "missing_master", "unmapped"):
            totals[key] += stats[key]

    if smoke_nightmix:
        smoke_nightmix_mpc()

    try:
        unreal.EditorLevelLibrary.save_current_level()
        _log("Saved current level (local only — do not commit .umap)", {"path": LEVEL_PATH})
    except Exception as exc:
        _log("Save level warning", {"error": str(exc)})

    _log(
        "Done",
        {
            "actors": totals["actors"],
            "slots_assigned": totals["assigned"],
            "slots_skipped": totals["skipped"],
            "missing_master": totals["missing_master"],
            "unmapped": totals["unmapped"],
            "masters_used": sorted(material_cache.keys()),
        },
    )
    return 0 if totals["missing_master"] == 0 and totals["unmapped"] == 0 else 1


if __name__ == "__main__":
    smoke = "--no-nightmix-smoke" not in sys.argv
    code = main(smoke_nightmix=smoke)
    if code != 0:
        unreal.log_error(PREFIX + " finished with code %s" % code)

# create_master_materials.py
# Post-audit wrap: create or upgrade ten Docs/02 master materials with NightMix MPC graphs.
# Idempotent: skips materials that already contain HomeWorldGraphVersion marker unless --force.
# Run inside Unreal Editor (Tools > Execute Python Script) or via MCP execute_python_script.

from __future__ import annotations

import importlib
import os
import sys

try:
    import unreal
except ImportError:
    print("create_master_materials: Run inside Unreal Editor.")
    sys.exit(1)

import homeworld_master_material_defs as defs_mod
import homeworld_material_graph as graph_mod

PREFIX = "create_master_materials:"
MASTERS_DIR = "/Game/HomeWorld/Materials/Masters"
MATERIALS_DIR = "/Game/HomeWorld/Materials"


def _log(msg: str) -> None:
    unreal.log(PREFIX + " " + str(msg))
    print(PREFIX, msg)


def ensure_folder(path: str) -> None:
    if not unreal.EditorAssetLibrary.does_directory_exist(path):
        unreal.EditorAssetLibrary.make_directory(path)
        _log("Created folder %s" % path)


def _load_mpc():
    import place_vs_mvp_markers

    importlib.reload(place_vs_mvp_markers)
    mpc = place_vs_mvp_markers.create_nightmix_mpc()
    if mpc:
        _log("MPC ensure OK: %s (scalar NightMix)" % graph_mod.MPC_PATH)
    else:
        mpc = unreal.EditorAssetLibrary.load_asset(graph_mod.MPC_PATH)
        if mpc:
            _log("Loaded existing MPC: %s" % graph_mod.MPC_PATH)
        else:
            _log("WARNING: MPC missing — CollectionParameter may fail until place_vs_mvp_markers runs")
    return mpc


def _create_material_shell(name: str) -> unreal.Material | None:
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.MaterialFactoryNew()
    mat = asset_tools.create_asset(name, MASTERS_DIR, unreal.Material, factory)
    if not mat:
        _log("Failed to create material shell %s/%s" % (MASTERS_DIR, name))
        return None
    return mat


def ensure_master_material(name: str, force: bool = False) -> str:
    asset_path = "%s/%s" % (MASTERS_DIR, name)
    created = False
    if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        material = unreal.EditorAssetLibrary.load_asset(asset_path)
        _log("Found existing material %s" % asset_path)
    else:
        material = _create_material_shell(name)
        if not material:
            return "failed"
        created = True
        _log("Created material shell %s" % asset_path)

    if graph_mod.material_has_homeworld_graph(material) and not force:
        _log("Skip graph rebuild (HomeWorldGraphVersion present): %s" % name)
        return "skipped"

    try:
        raw = defs_mod.load_master_json(name)
        master = defs_mod.parse_master_def(raw)
    except Exception as exc:
        _log("Failed to load JSON for %s: %s" % (name, exc))
        return "failed"

    mpc = _load_mpc()
    try:
        graph_mod.apply_material_settings(material, master)
        graph_mod.build_master_graph(material, master, mpc)
        unreal.EditorAssetLibrary.save_asset(asset_path)
        action = "upgraded" if not created else "created"
        _log(
            "%s %s — params BaseColor/Roughness/Variation/NightMix/Emissive; NightMix from MPC %s"
            % (action, name, graph_mod.MPC_SCALAR_NAME)
        )
        return action
    except Exception as exc:
        _log("Graph build failed for %s: %s" % (name, exc))
        return "failed"


def main(force: bool = False) -> int:
    _log("Building ten master materials per Docs/02 + Lib/06_Materials_Master/*.json")
    _log("NightMix driver: CollectionParameter on %s scalar %s" % (graph_mod.MPC_PATH, graph_mod.MPC_SCALAR_NAME))
    ensure_folder(MATERIALS_DIR)
    ensure_folder(MASTERS_DIR)

    stats: dict[str, int] = {"created": 0, "upgraded": 0, "skipped": 0, "failed": 0}
    for name in defs_mod.MASTER_NAMES:
        result = ensure_master_material(name, force=force)
        stats[result] = stats.get(result, 0) + 1

    _log(
        "Done. created=%d upgraded=%d skipped=%d failed=%d"
        % (stats.get("created", 0), stats.get("upgraded", 0), stats.get("skipped", 0), stats.get("failed", 0))
    )
    if stats.get("failed", 0):
        _log("M_FoliageCard uses BLEND_MASKED with opaque opacity stub (no card texture yet)")
    else:
        _log("M_FoliageCard: masked blend + constant opacity=1 (card texture alpha deferred)")
    return 0 if stats.get("failed", 0) == 0 else 1


if __name__ == "__main__":
    force_flag = "--force" in sys.argv
    code = main(force=force_flag)
    if code != 0:
        unreal.log_error(PREFIX + " finished with code %s" % code)

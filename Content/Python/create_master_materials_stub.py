# create_master_materials_stub.py
# WAVE E: create empty Material assets for the ten Docs/02 masters (script-only, no binary commit).
# Idempotent: skips existing assets. Node graphs remain Editor/TA work.

from __future__ import annotations

import sys

try:
    import unreal
except ImportError:
    print("create_master_materials_stub: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "create_master_materials_stub:"
MASTERS_DIR = "/Game/HomeWorld/Materials/Masters"

# Docs/02_MATERIAL_SHEET.md §2 — ten masters only
MASTER_NAMES = (
    "M_StylizedGrass",
    "M_CliffRock",
    "M_WoodCabin",
    "M_WoodWild",
    "M_FoliageCard",
    "M_PathStone",
    "M_GatherHerb",
    "M_BeastStylized",
    "M_SpiritUnlit",
    "M_Nurtured",
)


def _log(msg):
    unreal.log(PREFIX + " " + str(msg))
    print(PREFIX, msg)


def ensure_folder(path):
    if not unreal.EditorAssetLibrary.does_directory_exist(path):
        unreal.EditorAssetLibrary.make_directory(path)
        _log("Created folder %s" % path)


def create_or_skip_master(name):
    asset_path = "%s/%s" % (MASTERS_DIR, name)
    if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        _log("Reuse existing %s" % asset_path)
        return "skipped"
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.MaterialFactoryNew()
    mat = asset_tools.create_asset(name, MASTERS_DIR, unreal.Material, factory)
    if not mat:
        _log("Failed to create %s" % asset_path)
        return "failed"
    unreal.EditorAssetLibrary.save_asset(asset_path)
    _log("Created empty material %s (assign NG_M_* / NightMix in Editor)" % asset_path)
    return "created"


def main():
    _log("Creating master material stubs per Docs/02 (ten masters)")
    ensure_folder("/Game/HomeWorld/Materials")
    ensure_folder(MASTERS_DIR)
    stats = {"created": 0, "skipped": 0, "failed": 0}
    for name in MASTER_NAMES:
        result = create_or_skip_master(name)
        stats[result] = stats.get(result, 0) + 1
    _log(
        "Done. created=%d skipped=%d failed=%d — wire NightMix via MPC_HomeWorld_Time + material instances"
        % (stats.get("created", 0), stats.get("skipped", 0), stats.get("failed", 0))
    )
    return 0 if stats.get("failed", 0) == 0 else 1


if __name__ == "__main__":
    code = main()
    if code != 0:
        unreal.log_error(PREFIX + " finished with code %s" % code)

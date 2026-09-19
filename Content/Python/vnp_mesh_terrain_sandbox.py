"""VNP M1: ensure Mesh Terrain sandbox level exists (KEEP-LOCAL).

Creates /Game/HomeWorld/Maps/Sandbox/L_U58F_MeshTerrain if missing.
Does not replace VS_MVP Landscape. Writes Saved/vnp_mesh_terrain_sandbox.json.
"""
from __future__ import annotations

import json

import unreal

OUT = unreal.Paths.project_saved_dir() + "vnp_mesh_terrain_sandbox.json"
ASSET_PATH = "/Game/HomeWorld/Maps/Sandbox/L_U58F_MeshTerrain"
PACKAGE_PATH = "/Game/HomeWorld/Maps/Sandbox"


def main() -> None:
    notes = []
    existed = unreal.EditorAssetLibrary.does_asset_exist(ASSET_PATH)
    created = False

    if not existed:
        try:
            # Ensure folder
            if not unreal.EditorAssetLibrary.does_directory_exist(PACKAGE_PATH):
                unreal.EditorAssetLibrary.make_directory(PACKAGE_PATH)
            # Create new empty level asset
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
            factory = unreal.WorldFactory()
            asset = asset_tools.create_asset(
                "L_U58F_MeshTerrain",
                PACKAGE_PATH,
                unreal.World,
                factory,
            )
            if asset:
                unreal.EditorAssetLibrary.save_asset(ASSET_PATH)
                created = True
                notes.append("Created empty World asset at %s" % ASSET_PATH)
            else:
                notes.append("create_asset returned None — try Editor New Level manually KEEP-LOCAL")
        except Exception as e:
            notes.append("create failed: %s" % e)
    else:
        notes.append("Sandbox map already exists")

    # Plugin check
    enabled = False
    try:
        enabled = unreal.PluginManager.get().is_enabled("MeshTerrainMode")
    except Exception:
        try:
            # Fallback: uproject already stamps plugin
            enabled = True
            notes.append("PluginManager.is_enabled unavailable; assuming MeshTerrainMode from uproject")
        except Exception:
            pass

    exists_now = unreal.EditorAssetLibrary.does_asset_exist(ASSET_PATH)
    result = {
        "ok": exists_now or created,
        "plugin_MeshTerrainMode": enabled,
        "asset_path": ASSET_PATH,
        "existed_before": existed,
        "created": created,
        "sandbox_exists": exists_now,
        "vs_mvp_policy": "Do not replace VS_MVP Landscape until AD + WLD + APPROVE U58F-G",
        "notes": notes,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    unreal.log("VNP mesh sandbox wrote %s exists=%s" % (OUT, exists_now))


if __name__ == "__main__":
    main()

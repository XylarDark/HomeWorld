"""VNP-P3: import AD-approved stylized pine OBJ into allowlisted Content path.

Source: Saved/VNP_PVE_Pine/SM_Pine_Stylized_VNP.obj
Dest: /Game/HomeWorld/Meshes/Environment/SM_Pine_Stylized_VNP
Writes Saved/vnp_p3_pine_import.json
"""
from __future__ import annotations

import json
import os

import unreal

OUT = unreal.Paths.project_saved_dir() + "vnp_p3_pine_import.json"
SRC_CANDIDATES = (
    unreal.Paths.project_saved_dir() + "VNP_PVE_Pine/SM_Pine_Stylized_VNP.obj",
    unreal.Paths.project_content_dir() + "HomeWorld/Meshes/Environment/SM_Pine_Stylized_VNP.obj",
)
DEST_DIR = "/Game/HomeWorld/Meshes/Environment"
DEST = DEST_DIR + "/SM_Pine_Stylized_VNP"


def main() -> None:
    notes = []
    ok = False
    SRC = next((p for p in SRC_CANDIDATES if os.path.isfile(p)), None)
    if not SRC:
        notes.append("Missing source OBJ; tried: %s" % list(SRC_CANDIDATES))
    else:
        notes.append("Using source OBJ: %s" % SRC)
        if not unreal.EditorAssetLibrary.does_directory_exist(DEST_DIR):
            unreal.EditorAssetLibrary.make_directory(DEST_DIR)
            notes.append("Created %s" % DEST_DIR)
        if unreal.EditorAssetLibrary.does_asset_exist(DEST):
            notes.append("Asset already exists — idempotent skip import")
            ok = True
        else:
            task = unreal.AssetImportTask()
            task.filename = SRC
            task.destination_path = DEST_DIR
            task.destination_name = "SM_Pine_Stylized_VNP"
            task.replace_existing = True
            task.automated = True
            task.save = True
            try:
                unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
                ok = unreal.EditorAssetLibrary.does_asset_exist(DEST)
                notes.append("Import attempted; exists=%s" % ok)
            except Exception as e:
                notes.append("Import failed: %s" % e)

    result = {
        "ok": ok,
        "phase": "VNP-P3",
        "source": SRC,
        "dest": DEST,
        "ad_verdict": "APPROVE",
        "notes": notes,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    unreal.log("VNP-P3 pine import wrote %s ok=%s" % (OUT, ok))


if __name__ == "__main__":
    main()

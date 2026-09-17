"""
HomeWorld Blender export helper — STYLE_GUIDE-aligned FBX export into AssetCreation/Exports.

Run inside Blender (Scripting workspace, or via blender-mcp execute_blender_code / run script):

    # Default: export selected objects as FBX into Exports/Homestead/
    exec(open(r"C:/dev/HomeWorld/AssetCreation/Blender/export_to_asset_creation.py").read())

Or call the API from MCP / another script:

    from export_to_asset_creation import export_fbx
    export_fbx(category="Harvestables", filename="tree_01.fbx", selected_only=True)

Categories (Docs/04 mesh roots + legacy):
  Homestead, Forest, Gatherables, Transit, Beasts, Spirits,
  Characters, Harvestables, Dungeon, Biomes.

Preset (UE5 / STYLE_GUIDE): Forward X, Up Z, FBX Unit Scale, Apply Modifiers,
Face smoothing, FBX 2020.2. See AssetCreation/STYLE_GUIDE.md.
Docs/04 axis note (-Y Forward) is deferred to UE import preset; helper keeps STYLE_GUIDE.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

try:
    import bpy
except ImportError as exc:  # pragma: no cover - Blender-only
    raise SystemExit("export_to_asset_creation.py must run inside Blender") from exc

# #region agent log
def _debug_log(message: str, data: Optional[dict] = None) -> None:
    payload = data or {}
    print(f"HomeWorld Blender export: {message} {payload}")


# #endregion

# Docs/04 content roots (mesh) + legacy AssetCreation folders
VALID_CATEGORIES = (
    "Homestead",
    "Forest",
    "Gatherables",
    "Transit",
    "Beasts",
    "Spirits",
    "Characters",
    "Harvestables",
    "Dungeon",
    "Biomes",
)

# Categories that land under /Game/HomeWorld/Meshes/<Category>/ (Docs/04)
MESH_CATEGORIES = (
    "Homestead",
    "Forest",
    "Gatherables",
    "Transit",
    "Beasts",
    "Spirits",
)


def _repo_root() -> Path:
    """AssetCreation/Blender/ -> AssetCreation/ -> repo root."""
    try:
        return Path(__file__).resolve().parents[2]
    except NameError:
        # exec()'d without __file__ (MCP / paste) — fall back to known repo layout
        return Path("/workspace/repos/HomeWorld")


def exports_dir(category: str) -> Path:
    if category not in VALID_CATEGORIES:
        raise ValueError(f"category must be one of {VALID_CATEGORIES}, got {category!r}")
    out = _repo_root() / "AssetCreation" / "Exports" / category
    out.mkdir(parents=True, exist_ok=True)
    return out


def apply_transforms_selected() -> int:
    """Apply location/rotation/scale to selected mesh objects. Returns count applied."""
    meshes = [obj for obj in bpy.context.selected_objects if obj.type == "MESH"]
    if not meshes:
        _debug_log("apply_transforms_selected: no mesh selection", {"selected": len(bpy.context.selected_objects)})
        return 0
    bpy.ops.object.select_all(action="DESELECT")
    for obj in meshes:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    _debug_log("apply_transforms_selected: done", {"count": len(meshes)})
    return len(meshes)


def export_fbx(
    category: str = "Homestead",
    filename: str = "export.fbx",
    selected_only: bool = True,
    apply_transforms: bool = True,
) -> str:
    """
    Export FBX using HomeWorld STYLE_GUIDE settings.

    Returns the absolute path written.
    """
    _debug_log(
        "export_fbx: start",
        {
            "category": category,
            "filename": filename,
            "selected_only": selected_only,
            "apply_transforms": apply_transforms,
        },
    )

    if apply_transforms and selected_only:
        apply_transforms_selected()

    dest_dir = exports_dir(category)
    if not filename.lower().endswith(".fbx"):
        filename = f"{filename}.fbx"
    dest = dest_dir / filename
    abs_path = str(dest.resolve())

    # UE5-oriented FBX (Blender 3.x / 4.x bpy.ops.export_scene.fbx)
    # STYLE_GUIDE: Forward X, Up Z (keep helper preset; Docs/04 -Y deferred to UE)
    bpy.ops.export_scene.fbx(
        filepath=abs_path,
        use_selection=selected_only,
        apply_scale_options="FBX_SCALE_UNITS",
        axis_forward="X",
        axis_up="Z",
        apply_unit_scale=True,
        use_mesh_modifiers=True,
        mesh_smooth_type="FACE",
        use_triangles=False,
        bake_space_transform=False,
        object_types={"MESH", "ARMATURE", "EMPTY"},
        path_mode="AUTO",
    )

    _debug_log("export_fbx: done", {"path": abs_path, "exists": os.path.isfile(abs_path)})
    return abs_path


def export_glb(
    category: str = "Homestead",
    filename: str = "export.glb",
    selected_only: bool = True,
) -> str:
    """Export glTF binary (.glb) into Exports/<category>/."""
    _debug_log("export_glb: start", {"category": category, "filename": filename})
    dest_dir = exports_dir(category)
    if not filename.lower().endswith(".glb"):
        filename = f"{filename}.glb"
    dest = dest_dir / filename
    abs_path = str(dest.resolve())
    bpy.ops.export_scene.gltf(
        filepath=abs_path,
        export_format="GLB",
        use_selection=selected_only,
    )
    _debug_log("export_glb: done", {"path": abs_path, "exists": os.path.isfile(abs_path)})
    return abs_path


# When run via Blender Text Editor ("Run Script"), __name__ is "__main__".
if __name__ == "__main__":
    try:
        path = export_fbx(category="Homestead", filename="export.fbx", selected_only=True)
        print(f"Exported: {path}")
    except Exception as err:  # pragma: no cover
        _debug_log("export_fbx: failed", {"error": str(err)})
        raise

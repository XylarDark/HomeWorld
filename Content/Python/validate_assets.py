# validate_assets.py
# Editor script: validate key assets (exist, loadable), optional missing refs and PCG-related checks.
# Run in Editor: Tools > Execute Python Script, or -ExecutePythonScript=Content/Python/validate_assets.py
# Outputs: Saved/asset_validation_result.json (success, errors, missing_refs, pcg_checks).

import json
import os

PREFIX = "validate_assets:"

# Key paths to validate (existence + loadable)
KEY_PATHS = [
    "/Game/HomeWorld/Maps/DemoMap",
    "/Game/HomeWorld/PCG/ForestIsland_PCG",
    "/Game/HomeWorld/Characters/BP_HomeWorldCharacter",
    "/Game/HomeWorld/Input/IA_Move",
    "/Game/HomeWorld/Input/IA_Look",
    "/Game/HomeWorld/Input/IMC_Default",
]


def _log(msg: str, data: dict | None = None) -> None:
    parts = [PREFIX, msg]
    if data is not None:
        parts.append(json.dumps(data))
    print(" ".join(parts))


def main() -> None:
    try:
        import unreal
    except ImportError:
        _log("abort: unreal module not available (run in Editor)")
        return

    errors = []
    missing_refs = []
    pcg_checks = {"ForestIsland_PCG_exists": False, "ForestIsland_PCG_loadable": False}

    for path in KEY_PATHS:
        if not unreal.EditorAssetLibrary.does_asset_exist(path):
            errors.append(f"missing:{path}")
            if "ForestIsland_PCG" in path:
                pcg_checks["ForestIsland_PCG_exists"] = False
            continue
        if "ForestIsland_PCG" in path:
            pcg_checks["ForestIsland_PCG_exists"] = True
        try:
            asset = unreal.EditorAssetLibrary.load_asset(path)
            if asset is None:
                errors.append(f"load_failed:{path}")
                if "ForestIsland_PCG" in path:
                    pcg_checks["ForestIsland_PCG_loadable"] = False
            else:
                if "ForestIsland_PCG" in path:
                    pcg_checks["ForestIsland_PCG_loadable"] = True
        except Exception as e:
            errors.append(f"load_error:{path}:{e!s}")
            if "ForestIsland_PCG" in path:
                pcg_checks["ForestIsland_PCG_loadable"] = False

    # Optional: AssetRegistry for referencers (if available)
    if hasattr(unreal, "AssetRegistryHelpers"):
        try:
            registry = unreal.AssetRegistryHelpers.get_asset_registry()
            if registry:
                for path in KEY_PATHS[:2]:  # sample
                    if unreal.EditorAssetLibrary.does_asset_exist(path):
                        data = registry.get_asset_by_object_path(path)
                        if data and not data.is_valid():
                            missing_refs.append(path)
        except Exception as e:
            _log("AssetRegistry check skipped", {"error": str(e)})

    success = len(errors) == 0
    # Project Saved dir: from Content/Python go up to project root then Saved
    script_dir = os.path.dirname(os.path.abspath(__file__))
    saved_dir = os.path.normpath(os.path.join(script_dir, "..", "..", "Saved"))
    if hasattr(unreal, "Paths") and hasattr(unreal.Paths, "project_saved_dir"):
        try:
            saved_dir = unreal.Paths.project_saved_dir()
        except Exception:
            pass
    os.makedirs(saved_dir, exist_ok=True)
    result_path = os.path.join(saved_dir, "asset_validation_result.json")
    result = {
        "success": success,
        "errors": errors,
        "missing_refs": missing_refs,
        "pcg_checks": pcg_checks,
        "key_paths_checked": len(KEY_PATHS),
    }
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    _log("completed", {"success": success, "errors_count": len(errors), "result_path": result_path})


if __name__ == "__main__":
    main()

# preflight_ue_editor.py
# HR3-B: Editor-side deep checks for UE preflight (run via MCP on DESKTOP).
# Writes Saved/preflight_ue_editor.json for scripts/preflight-ue.js to consume.
#
# MCP: execute_python_script("preflight_ue_editor.py")
# Then: npm run preflight:ue -- --skip-mcp --require-editor

import json
import os
import sys
import traceback

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)

PREFIX = "PreflightUE"
CONFIG_REL = "config/preflight-ue.json"
OUT_REL = "Saved/preflight_ue_editor.json"


def _log(msg, data=None):
    line = f"{PREFIX}: {msg}"
    unreal.log(line)
    print(line)
    if data is not None:
        unreal.log(f"{PREFIX}: {json.dumps(data, default=str)}")


def _project_root():
    return unreal.SystemLibrary.get_project_directory()


def _load_config():
    cfg_path = os.path.join(_project_root(), CONFIG_REL.replace("/", os.sep))
    if not os.path.exists(cfg_path):
        return {}
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _blocker(code, message, detail=None, asset=None):
    b = {"code": code, "message": message}
    if detail:
        b["detail"] = detail
    if asset:
        b["asset"] = asset
    return b


def _check_asset_exists(game_path, code, label):
    if not game_path:
        return _blocker("CONFIG_EMPTY_PATH", f"{label} path not configured", detail=label)
    if not unreal.EditorAssetLibrary.does_asset_exist(game_path):
        return _blocker(
            "EDITOR_MAP_MISSING" if "/Maps/" in game_path else "ASSET_MISSING_ON_DISK",
            f"{label} missing or unloadable in Editor",
            detail=game_path,
            asset=game_path,
        )
    asset = unreal.load_asset(game_path)
    if not asset:
        return _blocker(
            "ASSET_MISSING_ON_DISK",
            f"{label} failed to load",
            detail=game_path,
            asset=game_path,
        )
    return None


def _check_abp_skeleton(abp_path):
    blockers = []
    b = _check_asset_exists(abp_path, "EDITOR_ABP_SKELETON", "Character AnimBP")
    if b:
        return [b]

    abp = unreal.load_asset(abp_path)
    skeleton = None
    try:
        skeleton = abp.get_editor_property("target_skeleton")
    except Exception:
        pass
    if not skeleton:
        try:
            skeleton = abp.get_editor_property("skeleton")
        except Exception:
            pass

    if not skeleton:
        blockers.append(
            _blocker(
                "EDITOR_ABP_SKELETON",
                "ABP skeleton asset missing — AnimBP cannot compile (VP-A class failure)",
                detail=abp_path,
                asset=abp_path,
            )
        )
        return blockers

    sk_name = skeleton.get_path_name() if hasattr(skeleton, "get_path_name") else str(skeleton)
    if not unreal.EditorAssetLibrary.does_asset_exist(sk_name.split(".")[0] if "." in sk_name else sk_name):
        # Skeleton object may be embedded; verify compile status below
        pass

    try:
        unreal.BlueprintEditorLibrary.compile_blueprint(abp)
    except Exception as e:
        _log("compile_blueprint warning", {"error": str(e)})

    status = None
    try:
        status = unreal.BlueprintEditorLibrary.get_blueprint_compile_status(abp)
    except Exception:
        pass

    if status is not None:
        status_str = str(status)
        if "Error" in status_str or "BS_Error" in status_str:
            blockers.append(
                _blocker(
                    "EDITOR_ABP_SKELETON",
                    "ABP failed to compile — check skeleton and animation dependencies",
                    detail=f"{abp_path} status={status_str}",
                    asset=abp_path,
                )
            )

    return blockers


def _check_bp_mesh_and_anim(bp_path):
    blockers = []
    b = _check_asset_exists(bp_path, "EDITOR_BP_MESH_EMPTY", "Character Blueprint")
    if b:
        return [b]

    bp = unreal.load_asset(bp_path)
    gen_class = None
    try:
        gen_class = bp.generated_class()
    except Exception:
        try:
            gen_class = bp.get_editor_property("generated_class")
        except Exception:
            pass

    cdo = unreal.get_default_object(gen_class) if gen_class else None
    mesh = None
    anim_class = None

    if cdo:
        try:
            mesh = cdo.get_editor_property("mesh")
        except Exception:
            pass
        if mesh:
            try:
                sk = mesh.get_editor_property("skeletal_mesh_asset")
                if not sk:
                    blockers.append(
                        _blocker(
                            "EDITOR_BP_MESH_EMPTY",
                            "Character BP skeletal mesh component has no skeletal_mesh_asset",
                            detail=bp_path,
                            asset=bp_path,
                        )
                    )
                try:
                    anim_class = mesh.get_editor_property("anim_class")
                except Exception:
                    pass
            except Exception as e:
                blockers.append(
                    _blocker(
                        "EDITOR_BP_MESH_EMPTY",
                        "Could not read mesh component on character BP",
                        detail=str(e),
                        asset=bp_path,
                    )
                )
        else:
            blockers.append(
                _blocker(
                    "EDITOR_BP_MESH_EMPTY",
                    "Character BP CDO has no mesh component",
                    detail=bp_path,
                    asset=bp_path,
                )
            )

        if anim_class is None:
            blockers.append(
                _blocker(
                    "EDITOR_BP_MESH_EMPTY",
                    "Character BP anim_class unset — PIE spawn will fail verb greps",
                    detail=bp_path,
                    asset=bp_path,
                )
            )

    return blockers


def run_checks():
    config = _load_config()
    content = config.get("content", {})
    checks = []
    blockers = []

    map_path = content.get("vsMvpMap")
    bp_path = content.get("characterBlueprint")
    abp_path = content.get("characterAnimBlueprint")

    for name, path, fn in (
        ("map", map_path, lambda p: _check_asset_exists(p, "EDITOR_MAP_MISSING", "VS_MVP map")),
        ("character_bp", bp_path, lambda p: _check_asset_exists(p, "EDITOR_BP_MESH_EMPTY", "Character BP")),
    ):
        result = fn(path)
        checks.append({"name": name, "path": path, "ok": result is None})
        if result:
            blockers.append(result)

    abp_blockers = _check_abp_skeleton(abp_path)
    checks.append({"name": "character_abp", "path": abp_path, "ok": len(abp_blockers) == 0})
    blockers.extend(abp_blockers)

    bp_blockers = _check_bp_mesh_and_anim(bp_path)
    checks.append({"name": "bp_mesh_anim", "path": bp_path, "ok": len(bp_blockers) == 0})
    blockers.extend(bp_blockers)

    return {
        "ok": len(blockers) == 0,
        "prefix": PREFIX,
        "checks": checks,
        "blockers": blockers,
    }


def main():
    _log("entry")
    out_path = os.path.join(_project_root(), OUT_REL.replace("/", os.sep))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    try:
        payload = run_checks()
    except Exception as e:
        payload = {
            "ok": False,
            "prefix": PREFIX,
            "message": str(e),
            "traceback": traceback.format_exc(),
            "blockers": [
                _blocker("EDITOR_RESULTS_MISSING", "preflight_ue_editor.py crashed", detail=str(e))
            ],
        }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)

    _log("exit", {"ok": payload.get("ok"), "blockers": len(payload.get("blockers", [])), "out": out_path})

    if not payload.get("ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()

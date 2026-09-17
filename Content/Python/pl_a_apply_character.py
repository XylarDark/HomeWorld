# pl_a_apply_character.py — PL-A: Lead-accepted Manny substitute + compiling ABP_Unarmed
# Run via MCP: execute_python_script / hw_unreal_mcp_client.py script pl_a_apply_character.py
import json
import os
import unreal

BP = "/Game/HomeWorld/Characters/BP_HomeWorldCharacter"
OUT = os.path.join(unreal.SystemLibrary.get_project_directory(), "Saved", "PL_A_apply.json")


def _log(msg):
    unreal.log("PL_A: " + str(msg))
    print("PL_A: " + str(msg))


def _load_cfg():
    path = os.path.join(
        unreal.SystemLibrary.get_project_directory(),
        "Content",
        "Python",
        "character_blueprint_config.json",
    )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write(result):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    _log("wrote " + OUT)


def main():
    cfg = _load_cfg()
    mesh_path = cfg.get("skeletal_mesh") or ""
    anim_path = cfg.get("anim_blueprint") or ""
    result = {"mesh_path": mesh_path, "anim_path": anim_path, "ok": False, "errors": []}

    if not mesh_path or mesh_path.startswith("/Engine/"):
        result["errors"].append("config still Engine/mesh-only: " + mesh_path)
        _write(result)
        return 1

    for p in (mesh_path, anim_path):
        if p and not unreal.EditorAssetLibrary.does_asset_exist(p):
            result["errors"].append("missing asset: " + p)

    mesh = unreal.EditorAssetLibrary.load_asset(mesh_path) if mesh_path else None
    anim = unreal.EditorAssetLibrary.load_asset(anim_path) if anim_path else None
    bp = unreal.EditorAssetLibrary.load_asset(BP)
    if not mesh or not bp:
        result["errors"].append("FAIL load mesh/bp")
        _write(result)
        return 1

    cdo = unreal.get_default_object(bp.generated_class())
    sk = cdo.mesh
    sk.set_editor_property("skeletal_mesh_asset", mesh)

    anim_class = None
    if anim:
        try:
            anim_class = (
                anim.generated_class()
                if hasattr(anim, "generated_class")
                else anim.get_editor_property("generated_class")
            )
        except Exception as e:
            result["errors"].append("anim generated_class: " + str(e))
        if anim_class:
            try:
                sk.set_editor_property(
                    "animation_mode", unreal.AnimationMode.ANIMATION_BLUEPRINT
                )
            except Exception as e:
                result["errors"].append("animation_mode: " + str(e))
            sk.set_editor_property("anim_class", anim_class)
        else:
            result["errors"].append("no anim_class from " + anim_path)
    else:
        sk.set_editor_property("anim_class", None)

    try:
        unreal.BlueprintEditorLibrary.compile_blueprint(bp)
        result["bp_compile"] = "ok"
    except Exception as e:
        result["bp_compile"] = str(e)
        result["errors"].append("bp compile: " + str(e))

    if anim:
        try:
            unreal.BlueprintEditorLibrary.compile_blueprint(anim)
            result["abp_compile"] = "ok"
        except Exception as e:
            result["abp_compile"] = str(e)
            result["errors"].append("abp compile: " + str(e))

    unreal.EditorAssetLibrary.save_asset(BP)

    mesh_now = None
    anim_now = None
    try:
        mesh_now = sk.get_editor_property("skeletal_mesh_asset")
    except Exception:
        pass
    try:
        anim_now = sk.get_editor_property("anim_class")
    except Exception:
        pass
    result["mesh_now"] = str(mesh_now)
    result["anim_now"] = str(anim_now)
    result["ok"] = (
        mesh_now is not None
        and (not str(mesh_now).startswith("/Engine/"))
        and anim_now is not None
        and (not result["errors"])
    )
    _log("mesh_now=" + result["mesh_now"])
    _log("anim_now=" + result["anim_now"])
    _log("ok=" + str(result["ok"]))
    _write(result)
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

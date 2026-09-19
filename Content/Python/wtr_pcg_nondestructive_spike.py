"""WTR-D: duplicate a PCG forest/VS graph and apply one nondestructive comment edit.

Creates /Game/HomeWorld/PCG/WTR_ForestIsland_PCG_Dup from ForestIsland_PCG (or
first available forest graph), adds/updates a graph comment box via Python when
exposed, writes Saved/wtr_pcg_nondestructive_spike.json + optional screenshot path.

Idempotent: re-run skips recreate if dup exists; still stamps evidence.
"""
from __future__ import annotations

import json
import os
import time

import unreal

OUT = unreal.Paths.project_saved_dir() + "wtr_pcg_nondestructive_spike.json"
SHOT = unreal.Paths.project_saved_dir() + "VNP_Evidence/wtr_pcg_dup_spike.png"
SRC_CANDIDATES = (
    "/Game/HomeWorld/PCG/ForestIsland_PCG",
    "/Game/PCG/ForestIsland_PCG",
    "/Game/HomeWorld/PCG/VS_MVP_Forest_PCG",
)
DUP_DIR = "/Game/HomeWorld/PCG"
DUP_NAME = "WTR_ForestIsland_PCG_Dup"
DUP_PATH = DUP_DIR + "/" + DUP_NAME
COMMENT = "WTR-D nondestructive spike 2026-09-19 — do not use in production Generate"


def _ensure_dir(path: str) -> None:
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)


def _find_src() -> str | None:
    for p in SRC_CANDIDATES:
        if unreal.EditorAssetLibrary.does_asset_exist(p):
            return p
    # Soft search
    try:
        assets = unreal.EditorAssetLibrary.list_assets("/Game/HomeWorld", recursive=True)
        for a in assets:
            if "Forest" in a and "PCG" in a and not a.endswith("_Dup"):
                return a.split(".")[0]
    except Exception:
        pass
    return None


def main() -> None:
    notes = []
    ok = False
    src = _find_src()
    if not unreal.EditorAssetLibrary.does_directory_exist(DUP_DIR):
        unreal.EditorAssetLibrary.make_directory(DUP_DIR)

    if unreal.EditorAssetLibrary.does_asset_exist(DUP_PATH):
        notes.append("Dup already exists — idempotent reuse %s" % DUP_PATH)
        dup = unreal.EditorAssetLibrary.load_asset(DUP_PATH)
    elif src:
        dup = unreal.EditorAssetLibrary.duplicate_asset(src, DUP_PATH)
        notes.append("Duplicated %s -> %s" % (src, DUP_PATH))
    else:
        # No production forest graph in Content yet — create sandbox graph only
        notes.append("No ForestIsland_PCG source — creating sandbox PCGGraph %s" % DUP_PATH)
        try:
            factory = unreal.PCGGraphFactory()
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
            dup = asset_tools.create_asset(DUP_NAME, DUP_DIR, unreal.PCGGraph, factory)
            if not dup:
                # Fallback factory name variants
                for fname in ("PCGGraphFactory",):
                    try:
                        factory = getattr(unreal, fname)()
                        dup = asset_tools.create_asset(
                            DUP_NAME, DUP_DIR, unreal.PCGGraph, factory
                        )
                        if dup:
                            break
                    except Exception:
                        continue
            notes.append("Created sandbox graph exists=%s" % bool(dup))
        except Exception as e:
            notes.append("Sandbox create failed: %s" % e)
            dup = None
        src = "(sandbox-new)"

    edit = {"comment": COMMENT, "applied": False}
    if dup:
        # Best-effort: set asset metadata / graph description if exposed
        for prop, val in (
            ("graph_description", COMMENT),
            ("description", COMMENT),
        ):
            try:
                dup.set_editor_property(prop, val)
                edit["applied"] = True
                edit["via"] = prop
                break
            except Exception:
                continue
        try:
            # Some PCG assets expose SetGraphDescription-like editor props
            if hasattr(dup, "set_editor_property"):
                pass
        except Exception:
            pass
        try:
            unreal.EditorAssetLibrary.save_asset(DUP_PATH)
            notes.append("Saved dup asset")
            ok = True
        except Exception as e:
            notes.append("Save failed: %s" % e)
            ok = bool(dup)
    else:
        notes.append("duplicate_asset returned None")

    # Evidence screenshot of content browser / viewport (best-effort)
    shot_ok = False
    try:
        _ensure_dir(SHOT)
        unreal.AutomationLibrary.take_high_res_screenshot(1280, 720, SHOT)
        shot_ok = True
        time.sleep(0.2)
    except Exception as e:
        notes.append("Screenshot skipped: %s" % e)

    result = {
        "ok": ok,
        "phase": "WTR-D",
        "source": src,
        "dup": DUP_PATH,
        "edit": edit,
        "screenshot": SHOT if shot_ok else None,
        "notes": notes,
        "policy": "Duplicate only — production ForestIsland_PCG untouched",
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    unreal.log("WTR-D PCG spike wrote %s ok=%s" % (OUT, ok))


if __name__ == "__main__":
    main()

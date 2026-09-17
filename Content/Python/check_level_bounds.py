# check_level_bounds.py
# Optional Phase 4 (LEVEL_TESTING_PLAN): check current editor level for Landscape bounds.
# NP-C: also logs VS_MVP soft walk bounds config (vs_mvp_walk_bounds.json) when level is L_VS_MVP_Markers.
# Run from Editor: Tools -> Execute Python Script, or via MCP execute_python_script("check_level_bounds.py").
# If the level uses World Partition and the Landscape has zero bounds (cells not loaded), logs a warning
# suggesting Window -> World Partition -> Load All. Use this to remind designers before running
# scripts that depend on landscape size (e.g. create_demo_from_scratch).

import json
import os
import sys

try:
    import unreal
except ImportError:
    unreal = None

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)
import level_loader
import importlib
importlib.reload(level_loader)


def _log_vs_mvp_walk_bounds():
    config_path = os.path.join(_script_dir, "vs_mvp_walk_bounds.json")
    if not os.path.isfile(config_path):
        return
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception:
        return
    unreal.log(
        "Check level bounds: VS_MVP soft walk bounds (C++ SoftBoundsComponent) — "
        "center=(%.0f,%.0f,%.0f) radius=%.0f cm min_z=%.0f max_z=%.0f"
        % (
            float(cfg.get("center_x_cm", -400)),
            float(cfg.get("center_y_cm", -50)),
            float(cfg.get("center_z_cm", 100)),
            float(cfg.get("radius_xy_cm", 1050)),
            float(cfg.get("min_z_cm", -400)),
            float(cfg.get("max_z_cm", 600)),
        )
    )
    unreal.log(
        "Check level bounds: Navmesh deferred — soft pushback only per Docs/12c NP-C runbook."
    )


def main():
    if not unreal:
        return
    path = level_loader.get_current_level_path()
    if not path:
        unreal.log("Check level bounds: No editor level open.")
        return
    if path and "L_VS_MVP_Markers" in path:
        _log_vs_mvp_walk_bounds()
    has_bounds = level_loader.landscape_has_bounds()
    if not has_bounds:
        if level_loader.level_has_actor_of_class(unreal.Landscape):
            unreal.log_warning(
                "Check level bounds: Landscape has zero bounds (World Partition may not have loaded cells). "
                "Use Window -> World Partition -> Load All for full bounds, then re-run scripts that size the PCG volume."
            )
        else:
            unreal.log("Check level bounds: No Landscape in level (or no editor world).")
    else:
        bounds = level_loader.get_landscape_bounds()
        if bounds:
            o, e = bounds
            unreal.log("Check level bounds: OK — landscape bounds available (center Z=%.0f, extent Z=%.0f cm)." % (o.z, e.z))


if __name__ == "__main__":
    if not unreal:
        print("Run this script inside Unreal Editor.")
        sys.exit(1)
    main()

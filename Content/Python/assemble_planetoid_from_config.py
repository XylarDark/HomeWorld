# assemble_planetoid_from_config.py
# Run from Unreal Editor: Tools -> Execute Python Script or via MCP execute_python_script.
# Single entry point: ensures planetoid level, portal on DemoMap, opens planetoid, runs PCG setup.
# Idempotent; safe to run multiple times. After this, do manual steps (Get Landscape Data By Tag,
# Actor Spawner Template, terrain, homestead plateau) per docs/PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md.
# Config: Content/Python/planetoid_map_config.json.
# See docs/PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md, docs/tasks/DAYS_16_TO_30.md.

import sys
import os

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(1)

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

import level_loader
import ensure_demo_portal
import setup_planetoid_pcg
import importlib
importlib.reload(level_loader)
importlib.reload(ensure_demo_portal)
importlib.reload(setup_planetoid_pcg)


def _log(msg):
    unreal.log("Assemble planetoid: " + str(msg))
    print("Assemble planetoid: " + str(msg))


def main():
    _log("Start: assemble planetoid from config (idempotent).")
    # 1) Portal on DemoMap (opens DemoMap, places BP_PortalToPlanetoid at config position)
    _log("Step 1/2: Ensure demo portal (DemoMap + portal actor).")
    ensure_demo_portal.main()
    # 2) Planetoid level + PCG (ensures level exists, opens it, tags Landscape, volume, graph, Generate)
    _log("Step 2/2: Setup planetoid level and PCG (open planetoid, POI PCG, Generate).")
    setup_planetoid_pcg.main()
    _log("Assembly done. Planetoid level is open.")
    _log("Manual follow-up: In Planetoid_POI_PCG set Get Landscape Data -> By Tag = PCG_Landscape, Actor Spawner -> Template = BP_Shrine_POI (or chosen POI). Terrain: Sculpt/Erosion/Noise + spires per PLANETOID_PRIDE_MVP. Homestead plateau: place spawn/homestead. See docs/PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md.")
    _log("Optional: With planetoid open, run place_dungeon_entrance.py to place a dungeon entrance; with DemoMap open, run place_resource_nodes.py for resource nodes on DemoMap.")


if __name__ == "__main__":
    main()

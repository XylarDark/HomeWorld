---
name: homestead-setup
description: Set up or refresh the Homestead map and PCG (volume, graph, exclusion). Use when the user wants to create/regenerate Homestead, fix "no ground" or "volume not sized to landscape," or run the one-shot Homestead + PCG script.
---

# Homestead setup

Run the Homestead-from-scratch workflow so the map and PCG volume are ready for play or iteration.

## When to use

- User asks to "set up Homestead," "recreate Homestead," "fix Homestead PCG," or "run the Homestead script."
- User reports no ground, PCG volume wrong size, or wants a clean Homestead + forest setup.
- Task involves Homestead map, PCG volume, or ForestIsland_PCG graph.

## Instructions

1. **Ensure Homestead map exists.** If missing, the user must duplicate Main to `/Game/HomeWorld/Maps/Homestead` or run `ensure_homestead_map.py` (if present). If the map was converted to World Partition, there may be Homestead_WP; prefer one map named Homestead (see [docs/HOMESTEAD_MAP.md](../../docs/HOMESTEAD_MAP.md)).

2. **Fast path (recommended):** Tell the user to open Homestead in the Editor, then **Window → World Partition → Load All** so landscape bounds are available. Then run the script so the volume is sized to the landscape in one pass.

3. **Run the script:** Execute `Content/Python/create_homestead_from_scratch.py` via Editor (Tools → Execute Python Script or `py "Content/Python/create_homestead_from_scratch.py"`) or MCP `execute_python_script("create_homestead_from_scratch.py")`. The script will open Homestead if needed, wait for landscape bounds (or use config after timeout), destroy/recreate or reuse PCG volume and graph per config, size the volume, and attempt to assign the graph and Generate.

4. **After the script:** Remind the user of manual steps from [docs/PCG_SETUP.md](../../docs/PCG_SETUP.md): set Get Landscape Data to By Tag + PCG_Landscape, set mesh lists on Static Mesh Spawner nodes, assign the graph to the volume if the script could not, and click Generate from the level (select PCG_Forest → Details → Generate).

5. **Fast iteration:** For repeated runs without full recreation, suggest setting in `Content/Python/homestead_map_config.json`: `recreate_volume_and_graph: false`, and optionally `landscape_wait_attempts: 3`, `landscape_wait_delay_sec: 0.5`. See [docs/PCG_SETUP.md](../../docs/PCG_SETUP.md) (Fast iteration).

## References

- [docs/HOMESTEAD_MAP.md](../../docs/HOMESTEAD_MAP.md) — layout, content paths, World Partition, no ground
- [docs/PCG_SETUP.md](../../docs/PCG_SETUP.md) — what the script does, manual steps, fast iteration
- [Content/Python/homestead_map_config.json](../../Content/Python/homestead_map_config.json) — volume bounds, exclusion zones, recreate_volume_and_graph, timeouts

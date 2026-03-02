---
name: demo-map-setup
description: Set up or refresh the Demo map (primary demo/playable) and PCG. Use when the user wants to create DemoMap from scratch, run the demo PCG script, or fix DemoMap + PCG.
---

# Demo map setup

Run the DemoMap-from-scratch workflow so the primary demo map and PCG volume are ready for play or MVP build-out.

## When to use

- User asks to "set up the demo map," "create DemoMap," "run the demo script," or "set up PCG on DemoMap."
- Task involves the **primary demo/playable map** (DemoMap). For Homestead (legacy/campaign), use **homestead-setup** instead.

## Instructions

1. **Ensure DemoMap exists.** The map is **not** duplicated from another level. If missing, the user must create it once: **File → New Level → Empty Open World → Create**, then **File → Save As** → save to `Content/HomeWorld/Maps/` as **DemoMap** (path `/Game/HomeWorld/Maps/DemoMap`). Run `ensure_demo_map.py` to check; it logs these steps if the map is missing. See [docs/DEMO_MAP.md](../../docs/DEMO_MAP.md).

2. **Add a minimal landscape (one-time).** In DemoMap: **Mode → Landscape → Create New**, small landscape, **Component Subsection = 1 x 1**, add tag **PCG_Landscape** to the Landscape actor.

3. **Run the script:** Execute `Content/Python/create_demo_from_scratch.py` via Editor (Tools → Execute Python Script) or MCP `execute_python_script("create_demo_from_scratch.py")`. The script opens DemoMap if needed, creates/reuses PCG volume and graph (default non-destructive), tags landscape, and attempts to assign the graph and trigger Generate.

4. **After the script:** Remind the user of the 3 manual steps from [docs/PCG_QUICK_SETUP.md](../../docs/PCG_QUICK_SETUP.md) Option B: set Get Landscape Data (By Tag PCG_Landscape, Component By Class Landscape Component), set mesh lists on Static Mesh Spawner nodes, assign graph to PCG_Forest and click Generate. Volume sizing: if needed, set `use_landscape_bounds: false` and `volume_center_*` / `volume_extent_*` in **demo_map_config.json**.

## References

- [docs/DEMO_MAP.md](../../docs/DEMO_MAP.md) — create map, config, script flow
- [docs/PCG_QUICK_SETUP.md](../../docs/PCG_QUICK_SETUP.md) — Option B (script + 3 steps), volume sizing
- [Content/Python/demo_map_config.json](../../Content/Python/demo_map_config.json) — demo_level_path, volume bounds, exclusion_zones

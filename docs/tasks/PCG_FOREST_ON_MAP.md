# Task 4: PCG forest on map

**Goal:** Procedural trees/rocks on the landscape (e.g. around the village).

**Status:** Script creates the PCG graph (**ForestIsland_PCG**) if missing, tags the Landscape, and creates/sizes one PCG Volume (**PCG_Forest**). Generation is manual: set Get Landscape Data to By Tag + `PCG_Landscape`, assign the graph to the volume, click Generate.

**Setup and troubleshooting:** **[docs/PCG_SETUP.md](../PCG_SETUP.md)** — prerequisites, what the script does vs what you do, references, and "if nothing generates."

**Step-by-step from scratch:** **[PCG_MANUAL_SETUP.md](PCG_MANUAL_SETUP.md)** — tag Landscape, create graph, wire nodes, add volume, Generate.

**Config (DemoMap):** `Content/Python/demo_map_config.json` (level path, volume bounds, exclusion zones); `Content/Python/pcg_forest_config.json` (density, transform, mesh paths).

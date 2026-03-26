# Demo Map – Setup Guide

DemoMap is the **primary demo and playable map** for HomeWorld. This guide shows how to create it, add a landscape, run the setup scripts, and finish PCG in the Editor.

**You will:** Create an Empty Open World map (or use a template), add a small landscape, run `create_demo_from_scratch.py`, then do a few one-time steps in the Editor so trees and rocks appear.

---

## When to use this guide

- You need a playable demo level and don’t have DemoMap yet.
- You’re following the MVP or tutorial flow and DemoMap is the target level.
- Scripts like `create_demo_from_scratch.py` or `ensure_demo_map.py` are failing and you want the manual fallback.

---

## Tutorial 1: Create the map

**Option A – Let the script create it (recommended)**  
1. Create one Empty Open World level and save it (e.g. **File → New Level → Empty Open World → Save As** → `/Game/HomeWorld/Maps/Templates/EmptyOpenWorld`).  
2. In [demo_map_config.json](../../Content/Python/demo_map_config.json), set **`template_level_path`** to that asset path.  
3. Run **ensure_demo_map.py** or **create_demo_from_scratch.py**. If DemoMap is missing, the script creates it from the template. No manual “File → New Level” for DemoMap needed.

**Option B – Create DemoMap by hand**  
If `template_level_path` is not set:  
1. In the Editor: **File → New Level** → **Empty Open World** → **Create**.  
2. **File → Save As** → save under **Content/HomeWorld/Maps/** as **DemoMap** (path `/Game/HomeWorld/Maps/DemoMap`).  
3. Confirm **World Settings → World Partition** is enabled (it is by default for Empty Open World).

---

## Tutorial 2: Add a minimal landscape

Do this once with DemoMap open:

1. Open the **Mode** panel → **Landscape** → **Create New**.
2. Create a small landscape (e.g. 1–2 sections for speed).
3. In **Details**, set **Component Subsection** to **1 x 1** (required for PCG in UE 5.x).
4. Select the **Landscape** actor → **Details → Actor → Tags** → add **`PCG_Landscape`**.

---

## Tutorial 3: Run the setup scripts

**Config file:** [Content/Python/demo_map_config.json](../../Content/Python/demo_map_config.json) — defines `demo_level_path`, `template_level_path`, `volume_center_*`, `volume_extent_*`, `exclusion_zones`, and `use_landscape_bounds`. For a small playable area, set `use_landscape_bounds: false` and set the volume center/extent to match your landscape (see [PCG/PCG_QUICK_SETUP.md](../PCG/PCG_QUICK_SETUP.md)).

**Run in this order:**

1. **ensure_demo_map.py** (optional) — Ensures DemoMap exists; if you set `template_level_path`, the script can create DemoMap from that template. Run from **Tools → Execute Python Script** or via MCP.
2. **create_demo_from_scratch.py** — Opens DemoMap, tags the landscape, creates/reuses the PCG volume and ForestIsland_PCG graph. Run with DemoMap open (or let the script open it). The script cannot set some PCG options in UE 5.7; you’ll finish those in Tutorial 4.
3. **setup_level.py** — Adds **PlayerStart**, **Directional Light**, and **Sky Light** so you can press Play and see the level. Run with DemoMap open, then save and press Play to test.

**Homestead spawn:** On DemoMap, `setup_level.py` places PlayerStart at the first exclusion zone (homestead compound). After running it, start PIE and confirm the character spawns at the compound.

**Build orders and family agents (optional):** To add one build order and family agents for agentic-building tests, run **create_bp_build_order_wall.py**, then **place_build_order_wall.py**, then **place_mass_spawner_demomap.py**. See task docs for DAY10 / AGENTIC_BUILDING if needed.

---

## Tutorial 4: Finish PCG in the Editor (one-time)

After **create_demo_from_scratch.py**, the engine does not let scripts set some PCG options. Do these steps **once** in the Editor, then save the graph and level.

1. **Get Landscape Data**  
   Open **ForestIsland_PCG** (Content → HomeWorld → PCG). Select the **Get Landscape Data** node. In **Details**: **Actor** → **By Tag**, tag **`PCG_Landscape`**; **Component** → **By Class** → **Landscape Component**.

2. **Set mesh lists**  
   Select the tree (and rocks) **Static Mesh Spawner** node(s). In **Details → Mesh Selector**, add the meshes listed in [pcg_forest_config.json](../../Content/Python/pcg_forest_config.json) (`static_mesh_spawner_meshes`, `static_mesh_spawner_meshes_rocks`). **Save the graph** (Ctrl+S).

3. **Load the landscape region (World Partition)**  
   In a World Partition level the root Landscape can show 0 components; geometry is in **LandscapeStreamingProxy** actors. **Window → World Partition** → select the cell(s) that contain your landscape → **Load region from selection**. You can run **create_demo_from_scratch.py** again (or **pcg_generate_nothing_diagnostic.py** once) so the script tags loaded proxies with **PCG_Landscape**. Without loading the region, Generate often produces nothing.

4. **Assign graph and generate**  
   In the level, select **PCG_Forest** in the Outliner. In **Details → Graph** assign **ForestIsland_PCG** (if not already). Click **Generate** (or Ctrl+Click for full regenerate). **Save the level** (Ctrl+S).

Full flow and troubleshooting: [PCG/PCG_QUICK_SETUP.md](../PCG/PCG_QUICK_SETUP.md) Option B.

---

## Default map (optional)

To open DemoMap by default when starting the Editor or PIE: set in **Config/DefaultEngine.ini**:

- `GameDefaultMap=/Game/HomeWorld/Maps/DemoMap.DemoMap`
- `EditorStartupMap=/Game/HomeWorld/Maps/DemoMap.DemoMap`

---

## Legacy maps

- **Main** and **Homestead** remain in the project. Homestead is used for narrative/campaign content when needed; scripts **ensure_homestead_map.py** and **create_homestead_from_scratch.py** still target Homestead. The **primary demo and MVP build-out** use **DemoMap** and **create_demo_from_scratch.py**.

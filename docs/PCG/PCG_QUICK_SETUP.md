# PCG Quick Setup – Tutorial (UE 5.7)

This guide gets PCG (trees, rocks, etc.) working on a landscape in one sitting. Choose **Option A** if you want to build the graph by hand; choose **Option B** if you prefer running a script and then doing a short manual pass.

**You will need:** A level open in the Editor with a **Landscape** that has **Component Subsection = 1×1** and the tag **`PCG_Landscape`**. For DemoMap, start with [Maps/DEMO_MAP.md](../Maps/DEMO_MAP.md).

---

## Option A: Manual setup (no script)

Use this when you want full control or the script path is failing.

### 1. Prerequisites

- Level open with a **Landscape**.
- **Landscape** → Details → **Component Subsection** = **1x1**.

### 2. Tag the Landscape

- Outliner → select **Landscape** (root, e.g. Landscape1).
- Details → **Actor** → **Tags** → add **`PCG_Landscape`**.

### 3. Create the PCG graph

1. Content Browser → **Content/HomeWorld/PCG** → Right‑click → **PCG** → **PCG Graph** → name it (e.g. **ForestIsland_PCG**). Open it.
2. Add **Get Landscape Data**. Details: **Actor** → **By Tag**, tag **`PCG_Landscape`**; **Component** → **By Class** → **Landscape Component**.
3. Add **Surface Sampler**. Connect **Get Landscape Data (Out)** → **Surface Sampler (Surface)**; **Input** → **Surface Sampler (Bounding Shape)**. Set **Points Per Squared Meter** (e.g. 0.02–0.05).
4. Add **Static Mesh Spawner**. Connect **Surface Sampler (Out)** → **Static Mesh Spawner (In)** → **Output**. In Details → **Mesh Selector**, add your meshes (e.g. trees from `/Game/StylizedProvencal/Meshes/SM_Tree_01`, etc.).
5. (Optional) Add **Transform Points** between Surface Sampler and Spawner for rotation/scale variation.
6. **Save** the graph (Ctrl+S).

### 4. Add PCG Volume and Generate

1. In the **level**: **Place Actors** → search **PCG Volume** → drag into level.
2. **Position and scale** the volume so it **covers the landscape** where you want trees (use the transform gizmo; the volume is the sampling bounds).
3. Select the **PCG Volume** → Details → **Graph** → set to your graph (e.g. **ForestIsland_PCG**).
4. Click **Generate** (or Ctrl+Click for full regenerate).

**World Partition (e.g. DemoMap, Homestead):** Load the region that contains the landscape (Window → World Partition → select all cells or the right region → Load region from selection). Then do step 4. The root Landscape has Component Count 0 in Details; the geometry is in **LandscapeStreamingProxy** children — Get Landscape Data uses the tag on the root and works with loaded proxies.

---

## Option B: Script + 3 manual steps

Use this when you want the script to create/size the volume and graph, then do a short manual pass once.

### 1. Size the volume correctly (important for World Partition)

When the level uses **World Partition**, the script often **cannot** read landscape bounds (root Landscape reports 0 components). It then falls back to **World Partition bounds**, which are huge and can make the volume wrong.

**Fix:** Set the volume in **config** so it matches your playable area:

- For **DemoMap:** Edit **`Content/Python/demo_map_config.json`**. For Homestead (legacy): **`Content/Python/homestead_map_config.json`**.
- Set **`use_landscape_bounds`** to **`false`**.
- Set **`volume_center_x`**, **`volume_center_y`**, **`volume_center_z`** to the **center** of your terrain (in cm). Example: if terrain is around the origin, use `0, 0, 0`.
- Set **`volume_extent_x`**, **`volume_extent_y`**, **`volume_extent_z`** to the **half-size** of the area you want to cover (in cm). Example: for a 2 km × 2 km area use `100000, 100000, 5000`.

You can read the approximate center and size from the **World Partition** window (loaded region) or the viewport (Landscape or known actor transform).

### 2. Run the script

- Open **DemoMap** in the Editor (or let the script open it).
- Run **create_demo_from_scratch.py** (Tools → Execute Python Script or MCP).
- The script creates/reuses the graph and volume, tags the Landscape, and tries to assign the graph and trigger Generate. Many of these steps **fail** in UE 5.7 from Python (protected properties); that’s expected.

### 3. Three manual steps (one-time)

Do these **once**; then save the graph and level so future runs don’t need them.

1. **Get Landscape Data:** Open **ForestIsland_PCG** → select **Get Landscape Data** → Details: **Actor** → **By Tag**, tag **`PCG_Landscape`**; **Component** → **By Class** → **Landscape Component**.
2. **Meshes:** Select the **tree** (and if present **rocks**) **Static Mesh Spawner** → Details → **Mesh Selector** → add meshes from **`Content/Python/pcg_forest_config.json`** (`static_mesh_spawner_meshes`, `static_mesh_spawner_meshes_rocks`). Save the graph.
3. **Assign and Generate:** In the level, select **PCG_Forest** → Details → **Graph** → **ForestIsland_PCG** (if not already). Click **Generate** (or Ctrl+Click).

**World Partition:** Ensure the region containing the landscape is loaded (Window → World Partition → load the right region) before step 3.

**Harvestable trees:** Default config (`pcg_forest_config.json`) has **`spawn_harvestable_trees`** true and **50% density** (0.01 pts/m²). When the script **creates** the graph, the tree branch is an **Actor Spawner** (BP_HarvestableTree). If your graph already existed, delete ForestIsland_PCG and re-run the script, or set **Template Actor** to BP_HarvestableTree on the tree spawner manually. See [Day 7 — Make all PCG trees harvestable](tasks/DAY7_RESOURCE_NODES.md#6-make-all-pcg-trees-harvestable).

---

## If nothing spawns

- **Output Log** (Window → Developer Tools → Output Log): search **LogPCG** and **"No surfaces found"**.  
  If you see "No surfaces found": tag on Landscape, Get Landscape Data (By Tag + Component), and loaded region are the usual causes; see [PCG_SETUP.md](PCG_SETUP.md) “Generate produces nothing”.
- **Volume must overlap the landscape:** In the viewport the PCG Volume (box) should clearly contain the terrain. If you used script with WP fallback, the volume may be huge or off-center; set **use_landscape_bounds: false** and config **volume_center_*** / **volume_extent_*** to your island, then re-run the script.

---

## References

- [PCG_SETUP.md](PCG_SETUP.md) — Full script behavior, checklist, and troubleshooting.
- [PCG_MANUAL_SETUP.md](tasks/PCG_MANUAL_SETUP.md) — Build the graph from zero in the Editor.
- Epic: [PCG Tutorial Series](https://dev.epicgames.com/community/learning/tutorials/1wro/unreal-engine-pcg-tutorial-series), [Landscape in UE5.4 PCG](https://dev.epicgames.com/community/learning/tutorials/m38k/unreal-engine-fab-landscape-creation-in-ue5-4-procedural-content-generation-framework-pcg).

# Day 7 [1.2]: Resource nodes (trees as resource gathering object)

**Goal:** Place resource nodes on DemoMap using **trees as the resource gathering object**: a harvestable tree Blueprint (same mesh as PCG trees, based on `AHomeWorldResourcePile`) with Wood resource type. Day 8 will add the player harvest interaction (Interact key → GAS/inventory). See [30_DAY_SCHEDULE.md](../30_DAY_SCHEDULE.md) Day 7 and [AGENTIC_BUILDING.md](AGENTIC_BUILDING.md) section 2.3 (BP_WoodPile) for Week 2 Smart Object / HarvestWood.

**Status:** Ready. Create the Blueprint (manual), then run the placement script or place manually.

---

## 1. Prerequisites

- [ ] Day 6 done: DemoMap layout and PCG set up (see [DAY6_HOMESTEAD_LAYOUT.md](DAY6_HOMESTEAD_LAYOUT.md)).
- [ ] Editor open; C++ built (so `AHomeWorldResourcePile` is available).
- [ ] **Building folder:** Run `Content/Python/ensure_week2_folders.py` once (Tools → Execute Python Script or MCP) to create `/Game/HomeWorld/Building/`. Or run `place_resource_nodes.py` once—it will call ensure_week2_folders so the folder exists before you create the Blueprint.

---

## 2. Create the harvestable tree Blueprint

**Option A — Script (recommended):** Run **`Content/Python/create_bp_harvestable_tree.py`** (Tools → Execute Python Script or MCP). This creates **BP_HarvestableTree** in `/Game/HomeWorld/Building/` with ResourceType=Wood and AmountPerHarvest=10. Add a Static Mesh component with a tree mesh in the Editor if desired (see Option B step 4).

**Option B — Manual:**

1. **Content Browser:** Navigate to **Content → HomeWorld → Building**. If the **Building** folder is missing, run **`Content/Python/ensure_week2_folders.py`** (Tools → Execute Python Script or MCP) once to create it; then refresh the Content Browser or navigate again.
2. **Right-click** → **Blueprint Class**. Search for **HomeWorldResourcePile** ([AHomeWorldResourcePile](../../Source/HomeWorld/HomeWorldResourcePile.h)). Create a child Blueprint.
3. **Name it** `BP_HarvestableTree` (or `BP_WoodPile`; AGENTIC_BUILDING uses BP_WoodPile for Week 2).
4. **Open** the Blueprint. In **Components:**
   - Root is the C++ **OverlapVolume** (box). Add a **Static Mesh** component as a child.
   - **Static Mesh:** Assign one of the PCG tree meshes, e.g. `/Game/StylizedProvencal/Meshes/SM_Tree_01` (see [pcg_forest_config.json](../../Content/Python/pcg_forest_config.json) `static_mesh_spawner_meshes`). Ensures the resource object looks like a tree.
   - Optionally set mesh collision to **No Collision** so only the OverlapVolume is used for interaction.
5. **Details (Blueprint defaults):** Under **Resource**, set **Resource Type** to `Wood`, **Amount Per Harvest** to `10` (or as desired).
6. **Save.** The actor already has tag **ResourcePile** from C++.

---

## 3. Place resource nodes on DemoMap

**Option A — Script (recommended):**

1. Open **DemoMap** in the Editor.
2. Ensure **Content/Python/demo_map_config.json** has a **`resource_node_positions`** array (list of `{x, y, z}` in cm). Add or edit positions as needed.
3. Run **`Content/Python/place_resource_nodes.py`** (Tools → Execute Python Script or MCP `execute_python_script("place_resource_nodes.py")`). The script spawns `BP_HarvestableTree` at each position; idempotent (re-run does not duplicate if nodes already exist at those locations).
4. Save the level (Ctrl+S).

**Option B — Manual:**

1. With DemoMap open, drag **BP_HarvestableTree** from the Content Browser into the level 5–10 times.
2. Place instances near or among PCG trees so they read as harvestable trees. Save the level.

---

## 4. Validation

- [ ] Blueprint exists: `BP_HarvestableTree` (or `BP_WoodPile`) child of `AHomeWorldResourcePile` with tree mesh and Resource Type = Wood.
- [ ] Multiple instances placed on DemoMap (script or manual).
- [ ] No regression: DemoMap opens, PCG trees unchanged; new actors have tag **ResourcePile** (from C++).
- [ ] Day 8-ready: Resource Type and Amount Per Harvest are set so Day 8 can implement "Interact on resource node → grant wood."

---

## 5. After Day 7 [1.2]

- [ ] 30_DAY_SCHEDULE: Day 7 [1.2] item marked [x].
- [ ] DAILY_STATE: Yesterday = Day 7 resource nodes; Today = Day 8 (1.3 Resource collection loop); Current day = 8.
- [ ] SESSION_LOG: Short entry for Day 7 (Blueprint created, nodes placed, script used if any).

---

## 6. Make all PCG trees harvestable

**Project default:** In **`Content/Python/pcg_forest_config.json`**, **`spawn_harvestable_trees`** is **true** and density is **50%** of the previous default (`points_per_squared_meter`: 0.01, `density_lower_bound`/`density_upper_bound` halved). When the script **creates a new** ForestIsland_PCG graph, the tree branch uses an **Actor Spawner** (BP_HarvestableTree) instead of a Static Mesh Spawner, so every PCG-placed tree is harvestable. **Existing graphs** are not changed to Actor Spawner automatically: either **delete ForestIsland_PCG** in the Content Browser and run **create_demo_from_scratch.py** again (script recreates the graph with harvestable trees), or follow the manual steps below.

**Option A — Replace tree Static Mesh Spawner with Actor Spawner (all PCG trees harvestable):**

1. Open **ForestIsland_PCG** in the Editor (Content → HomeWorld → PCG).
2. **Remove** or bypass the **tree** Static Mesh Spawner (the one that places tree meshes). Optionally keep a separate Static Mesh Spawner for rocks only.
3. Add a **Spawn Actor** (Actor Spawner) node: right-click in graph → search **Spawn Actor** or **PCG Spawn Actor** → add it.
4. Connect the same points that fed the tree spawner into the **Actor Spawner**: e.g. **Transform Points** (or Surface Sampler) **Out** → **Actor Spawner In**; **Actor Spawner Out** → **Output** (or merge with rocks output).
5. Select the **Actor Spawner** node. In **Details** set **Template Actor** (or **Actor Class**) to **BP_HarvestableTree** (`/Game/HomeWorld/Building/BP_HarvestableTree`). Save the graph.
6. In the level, select **PCG_Forest** → **Generate**. All PCG-placed “trees” will now be harvestable actors. Save the level.

**Option B — Keep both (decoration + harvestable):** Keep the Static Mesh Spawner for visual trees and add a **second** branch: same points → **Actor Spawner** (BP_HarvestableTree). You will get two objects per point (one static mesh, one harvestable actor); consider lowering density or using the Actor Spawner only in a sub-region if that’s too heavy.

**Notes:** Actor Spawner spawns one Blueprint actor per point (heavier than instanced static meshes). For World Partition, ensure BP_HarvestableTree and PCG Volume partitioning/streaming are acceptable. See [PCG_BEST_PRACTICES.md](../PCG_BEST_PRACTICES.md) (“Actor Spawner (PCG-driven collectibles)”).

---

## References

- [AGENTIC_BUILDING.md](AGENTIC_BUILDING.md) — Section 2.3 (BP_WoodPile, HarvestWood SO) for Week 2 agent harvesting.
- [DEMO_MAP.md](../DEMO_MAP.md) — Primary demo map and config path.
- [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md) — Building folder and script index.

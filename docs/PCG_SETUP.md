# PCG Setup — HomeWorld (UE 5.7)

Single reference for procedural trees/rocks on the landscape: what the script does, what you must do in the Editor, and where to look for help.

**Quick path:** [**PCG_QUICK_SETUP.md**](PCG_QUICK_SETUP.md) — one-page, tutorial-aligned flow (manual-only or script + 3 steps) and volume sizing (config when landscape bounds unavailable). **Primary demo map:** DemoMap and **create_demo_from_scratch.py**; see [DEMO_MAP.md](DEMO_MAP.md).

For **elegant, research-backed approaches** (one-time "golden" graph so you don’t repeat manual steps), see **[PCG_ELEGANT_SOLUTIONS.md](PCG_ELEGANT_SOLUTIONS.md)**.

---

## Prerequisites

- Level open (e.g. **Main**) with a **Landscape** in it.
- **Landscape** → Details → **Component Subsection** = **1x1** (required for PCG in UE 5.x).
- The Landscape must be findable by **Get Landscape Data** via the tag **`PCG_Landscape`** (the script can add this tag).

---

## What the script does

The **primary demo** script **create_demo_from_scratch.py** ensures DemoMap exists (you create it manually: File → New Level → Empty Open World → Save As), opens it, then sets up PCG. It **does** the following on DemoMap:

1. **Open the level** (DemoMap).
2. **Creates or reuses a PCG graph** at **`/Game/HomeWorld/PCG/ForestIsland_PCG`**: **default is reuse** — the existing graph is reused and only Transform Points (and exclusion) are updated from config. Set **`recreate_volume_and_graph`** to **true** in config only when you explicitly want to force-recreate the graph (escape hatch). Graph contains Get Landscape Data, Surface Sampler (bounds + surface), Density Filter, Transform Points (trees **upright**, yaw-only rotation), Static Mesh Spawner (trees); optional rocks branch and Merge; optional **Difference** for exclusion zones from config (**`exclusion_zones`**) so trees spawn outside exclusion areas.
3. **Tree density** is driven by **`Content/Python/pcg_forest_config.json`**: `points_per_squared_meter` (default 0.01 = 50% of previous density), `density_lower_bound` / `density_upper_bound` (Density Filter). Lower values = fewer trees. When **`spawn_harvestable_trees`** is **true** (default), the script uses an **Actor Spawner** for the tree branch (BP_HarvestableTree) so all PCG trees are harvestable; existing graphs must be recreated (delete ForestIsland_PCG and re-run script) or updated manually (see [DAY7_RESOURCE_NODES.md](tasks/DAY7_RESOURCE_NODES.md#6-make-all-pcg-trees-harvestable)).
4. **Exclusion zones** come from the level config (**demo_map_config.json**) → **`exclusion_zones`** (center + half-extents in cm). Set **`skip_exclusion_zones`** to true to disable.
5. **Tags the Landscape** with **`PCG_Landscape`** if missing (`ensure_landscape_has_pcg_tag()`).
6. **PCG Volume:** **Default is reuse** — the existing volume is reused and resized from config. Set **`recreate_volume_and_graph`** to **true** in config only to destroy and create a new volume (escape hatch). Volume **bounds** (center and half-extents) come from **config** (`volume_center_*`, `volume_extent_*` in **demo_map_config.json**); if **`use_landscape_bounds`** is true, landscape bounds override when available, else World Partition bounds when available, else config. See **PCG volume size** below. Volume is labeled **PCG_Forest** in the Outliner. **One volume is enough** for the playable region. For World Partition levels, enable **Is Partitioned** on the PCG component and set **Partition Grid Size** on the **PCG World Actor** (see same section).
7. Saves the level.
8. **Attempts automation:** When the graph is created/loaded, the script tries to **assign the graph to the volume** (`try_assign_graph_to_volume`), **set Get Landscape Data to By Tag + PCG_Landscape** (`try_set_get_landscape_selector`), and **trigger Generate** (`trigger_pcg_generate`). In UE 5.7 many of these properties are protected or not exposed in Python, so these attempts often fail; the script logs what worked and what did not.

The script **cannot** (engine/Python limits):

- Reliably **assign the graph** to the PCG Volume — the graph property is often protected; if assignment fails, assign ForestIsland_PCG in Details.
- Reliably **set Get Landscape Data** (Actor By Tag, tag name, Component By Class) — you may need to set **By Tag** + **`PCG_Landscape`** and **Component → By Class → Landscape Component** in Details.
- Set **meshes on the Static Mesh Spawner nodes** — UE 5.7 Python does not expose `PCGStaticMeshSpawnerEntry` or `PCGMeshSelectorSingleMesh`, so you must assign the mesh list in the graph Details (see step 2b below).

So **after running the script**, if PCG did not generate, do the remaining steps: set Get Landscape Data (and Component), **set the mesh list on each Static Mesh Spawner**, assign the graph to the volume if needed, and click **Generate**.

---

## Steps only you do (in the Editor)

1. **Open the PCG graph** **ForestIsland_PCG** (Content → HomeWorld → PCG). The script creates it with Get Landscape Data, Surface Sampler, Density, Transform, Spawner (and optional rocks + Merge). If you prefer to build from scratch, see [PCG_MANUAL_SETUP.md](tasks/PCG_MANUAL_SETUP.md).
2. In the graph:
   - **2a.** Select **Get Landscape Data** and in **Details** set: **Actor** → **By Tag**, tag **`PCG_Landscape`**; **Component** → **By Class** → **Landscape Component** (if available).
   - **2b.** **Tree branch:** If the tree branch is an **Actor Spawner** (default when `spawn_harvestable_trees` is true in config), select it and in **Details** set **Template Actor** (or **Actor Class**) to **BP_HarvestableTree** (`/Game/HomeWorld/Building/BP_HarvestableTree`). If the tree branch is a **Static Mesh Spawner**, set **Mesh Selector** to the mesh list from `pcg_forest_config.json` → `static_mesh_spawner_meshes`. **Rocks:** If there is a **rocks** Static Mesh Spawner, set its mesh list from `static_mesh_spawner_meshes_rocks`. **Without mesh list or template, Generate produces no instances.**
3. **Assign the graph** to the **PCG Volume** (Outliner → select PCG_Forest → Details → **Graph** → ForestIsland_PCG).
4. **Generate from the level:** Close or minimize the graph editor. In the **level** (e.g. Main), select **PCG_Forest** in the Outliner. In the **Details** panel (right side), scroll to the **PCG** section and click the **Generate** button there. Use this Details-panel button only — not the green Play button or Simulate on the main toolbar, and not a Generate/Run button inside the graph asset editor. **If nothing appears after a normal click, try Ctrl+Click on Generate** to force a full regeneration. **For World Partition:** If you enabled **Is Partitioned** or changed **Partition Grid Size**, run **Cleanup** on the volume first, then **Generate** (or Ctrl+Click). After clicking Generate, **Output Log** (Window → Developer Tools → Output Log) should show lines containing `LogPCG`. If there are no LogPCG lines, the correct Generate was not used or the PCG log category may be filtered out.

If the script’s automation could not assign the graph or set Get Landscape Data (common in UE 5.7), you still need to set Get Landscape Data (and Component), **set the mesh list on each Static Mesh Spawner**, assign the graph to the volume if needed, and Generate from the level as above.

**Elegant approach (one-time setup):** Do the steps above **once** on ForestIsland_PCG, then save the graph. The **default is reuse**; on future runs the script reuses that graph, assigns it via `set_graph()`, and triggers Generate. Set `recreate_volume_and_graph: true` in config only to force full recreation. You then avoid re-entering Get Landscape Data and mesh lists every time. See [PCG_ELEGANT_SOLUTIONS.md](PCG_ELEGANT_SOLUTIONS.md) for the full flow and checklist.

---

## Demo setup: what the script does programmatically

When you run **create_demo_from_scratch.py** with the Editor open and DemoMap loaded, the script attempts to do **everything** so that opening the map is demo-ready:

| Step | Done by script? | If it fails |
|------|------------------|-------------|
| Ensure DemoMap exists | Yes when `template_level_path` in demo_map_config.json is set (creates from template); else logs manual steps | File → New Level → Empty Open World → Save As DemoMap, or set template_level_path and run ensure_demo_map |
| Open DemoMap level | Yes | Open the level in Editor |
| Tag Landscape with `PCG_Landscape` | Yes (`ensure_landscape_has_pcg_tag`) | Add tag in Details on Landscape actor |
| Create/reuse PCG graph (ForestIsland_PCG) | Yes | Create graph per [PCG_MANUAL_SETUP.md](tasks/PCG_MANUAL_SETUP.md) |
| Create/size PCG Volume (PCG_Forest) | Yes | Place and scale volume manually |
| Apply density (Surface Sampler, Density Filter) and transform/rotation from config | Yes (`update_forest_island_graph_from_config`) | Edit graph nodes in Details |
| Set Get Landscape Data to By Tag + `PCG_Landscape` | **Tried** (`try_set_get_landscape_selector`: multiple property names + `unreal.Name`) | Set in graph: Get Landscape Data → Details → Actor By Tag, tag `PCG_Landscape`; Component By Class → Landscape Component |
| Set mesh list on tree/rocks Static Mesh Spawner nodes | **Tried** (`try_set_spawner_mesh_lists`: uses `PCGStaticMeshSpawnerEntry` if present in Python) | Set in graph: each Static Mesh Spawner → Details → Mesh Selector → mesh list from `pcg_forest_config.json` |
| Assign graph to PCG Volume | **Tried** (`try_assign_graph_to_volume`: `set_graph()` on PCGComponent). **Or** run C++ commandlet: `UnrealEditor.exe HomeWorld.uproject <MapPath> -run=HomeWorldEditor.ApplyPCGSetup [GraphPath=/Game/HomeWorld/PCG/ForestIsland_PCG] [Tag=PCG_Landscape] [MeshList=/Game/Path1,...]` (level must be loaded). The commandlet assigns the graph; Tag and MeshList are accepted and logged—setting them on graph nodes requires one-time manual setup or Editor + auto-clicker (see [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md)). | In level: select PCG_Forest → Details → Graph → ForestIsland_PCG |
| Trigger Generate | Yes (`trigger_pcg_generate`) | In level: select PCG_Forest → Details → Generate (or Ctrl+Click) |
| Save level after Generate | Yes | Save level (Ctrl+S) so instances persist |

**After a successful run:** The level is saved with the volume, assigned graph, and generated instances. Re-opening the map should show trees/rocks. If any "Tried" step fails (see Output Log for "Could not set..." or "set in Editor"), do that step manually once; then re-run the script or save the level so the result is persisted.

---

## Fast iteration (minimize delay)

To run **create_demo_from_scratch.py** with the least delay when iterating:

1. **Open DemoMap** in the Editor.
2. Run **create_demo_from_scratch.py** (Tools → Execute Python Script or MCP).
3. **Default is reuse:** The script reuses the existing volume and graph and only updates location/extent and Transform Points from config. Set **`recreate_volume_and_graph`** to **true** in **`Content/Python/demo_map_config.json`** only when you explicitly want to force full recreation.
4. Set **`use_landscape_bounds`** to **false** to always use config bounds (no one-shot landscape query).
5. When using **Partitioned Generation:** after enabling Is Partitioned or changing Partition Grid Size, run **Cleanup** then **Generate** on the PCG Volume.

See comments in `demo_map_config.json` for a short summary of these keys.

---

## PCG volume size

**What "location" and "volume" mean:** The script places **one PCG Volume** (actor **PCG_Forest**). Its **location** is the volume center in world space; its **volume** (size) is given by **half-extents** in cm. There is no separate "location volume" asset. **Where bounds come from:** **Config** is the source of truth (`volume_center_*`, `volume_extent_*` in `demo_map_config.json`). If **`use_landscape_bounds`** is true, the script tries **landscape bounds** first; if not available (e.g. World Partition cells not loaded), it tries **World Partition bounds** so the volume is still sized to the level; otherwise it uses config. No retries or Load All.

**World Partition - Partitioned Generation (recommended):** For levels using World Partition (e.g. DemoMap), use **Partitioned Generation** so PCG streams with the world:

1. Select the **PCG Volume** (PCG_Forest) in the Outliner -> Details -> **PCG** component -> enable **Is Partitioned**.
2. Find the **PCG World Actor** in the level (Outliner or search) -> set **Partition Grid Size** to match your needs (e.g. **51200**-**102400** cm for DemoMap-style regions).
3. **Cleanup then Generate:** After enabling Is Partitioned or changing Partition Grid Size, run **Cleanup** on the PCG Volume (Details -> PCG section), then **Generate** (or Ctrl+Click for full regenerate). Re-run Cleanup then Generate whenever you change the grid size or toggle Is Partitioned.

The volume only needs to **overlap** the area you want to generate; the **partition grid** defines how work is split and streamed. **Get Landscape Data** remains the source for the **surface** (where to place instances); at Generate time each partition cell samples the landscape within its bounds.

---

## Detailed manual steps (from scratch)

If you prefer to build the graph from zero in the Editor, see **[docs/tasks/PCG_MANUAL_SETUP.md](tasks/PCG_MANUAL_SETUP.md)** for step-by-step (tag Landscape, create graph, add Get Landscape Data / Surface Sampler / Static Mesh Spawner, set By Tag + `PCG_Landscape`, add PCG Volume, assign graph, Generate).

---

## References

- **Elegant solutions (one-time setup, introspection):** [docs/PCG_ELEGANT_SOLUTIONS.md](PCG_ELEGANT_SOLUTIONS.md) — Research-backed approaches so you do manual steps once and reuse the graph; optional introspection to discover settable properties.
- **Required settings automation cannot set:** See [docs/PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md) for a list of variables/settings that are necessary but not (reliably) settable from Python/MCP.
- **[freetimecoder/unreal-pcg-examples](https://github.com/freetimecoder/unreal-pcg-examples)** — Full project with PCG graphs and maps; works in UE 5.7. Open a level with a PCG Volume + graph, hit Generate, then inspect the graph (Get Landscape Data settings, node order).
- **[PacktPublishing/Procedural-Content-Generation-with-Unreal-Engine-5](https://github.com/PacktPublishing/Procedural-Content-Generation-with-Unreal-Engine-5)** — Book repo, UE 5.4+; **Chapter_2** is “Craft your first lush, procedurally generated forest.” Open the Chapter_2 project in 5.7 and mirror its graph layout and Details settings in HomeWorld.
- **Epic docs:** [PCG Framework Node Reference (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-node-reference-in-unreal-engine), [Get Landscape Data (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/PCG/UPCGGetLandscapeSettings). In 5.4+, landscape is provided only via **Get Landscape Data**; the graph Input provides bounds.

---

## Generate produces nothing (checklist)

When clicking **Generate** on the PCG Volume shows **no instances**, work through in order:

1. **Get Landscape Data:** In ForestIsland_PCG, select **Get Landscape Data** → Details: **Actor** → **By Tag**, tag **`PCG_Landscape`**; **Component** → **By Class** → **Landscape Component**. Without this, the Surface Sampler gets no surface and logs "No surfaces found".
2. **Mesh list on spawners:** Tree (and rocks) **Static Mesh Spawner** nodes must have meshes assigned in Details (Mesh Selector / mesh list). Use paths from `Content/Python/pcg_forest_config.json` or assign in the graph. Without meshes, Generate produces no instances.
3. **Graph on volume:** In the level, select **PCG_Forest** → Details → **Graph** → **ForestIsland_PCG**. If the script could not assign it, assign manually.
4. **Landscape:** Landscape must have tag **`PCG_Landscape`** and **Component Subsection = 1x1** (Details). **Empty Open World:** The root Landscape can have **0 components** (they live on **LandscapeStreamingProxy**). Load the WP region containing the landscape (step 5), then run **create_demo_from_scratch.py** or **pcg_generate_nothing_diagnostic.py** so the script tags a proxy with `PCG_Landscape`; then Generate.
5. **World Partition:** If the level uses World Partition (e.g. **DemoMap**), the Landscape may be in an unloaded cell. Use **Window → World Partition** and load the landscape cells before Generate so Get Landscape Data can find the Landscape. In the World Partition window: use **Load All** / **Load All Cells** if available, or **box-select all cells** (drag a selection around the full grid) then **Load region from selection** (or right‑click → **Load Selected Cells**). "Load region from selection" alone only loads the current selection — select the whole world first to match "Load All".
6. **Partitioned / grid size:** If you changed **Partition Grid Size** or enabled **Is Partitioned** on the PCG component, run **Cleanup** on the volume then **Generate** (or Ctrl+Click). See the canonical flow in [PCG_BEST_PRACTICES.md](PCG_BEST_PRACTICES.md).

**Output Log:** Open **Window → Developer Tools → Output Log**. Click Generate (or **Ctrl+Click**). Search for **LogPCG** and **"No surfaces found"**; capture that output for diagnosis.

**Surface Sampler Debug:** In the graph, select **Surface Sampler** → Details → **Debug** → enable **Debug**, set **Point Mesh** to a small mesh (e.g. PCG_Cube). Generate again: if debug cubes appear, the problem is **downstream** (spawner/mesh list); if no cubes, the problem is **Get Landscape Data or bounds**.

**Minimal PCG test (troubleshooting):** Build a graph with **only** the canonical flow: **Input** → **Surface Sampler** (Bounding); **Get Landscape Data** → **Surface Sampler** (Surface); **Surface Sampler** → **Static Mesh Spawner** (one mesh) → **Output**. No Density, Transform, or Difference. Set Get Landscape Data to By Tag `PCG_Landscape` and Component By Class Landscape Component; assign one mesh to the spawner. Assign this graph to the volume and Generate. If this produces instances, the issue is in our extensions (Density, Transform, exclusion, rocks). If it also produces nothing, the issue is Get Landscape Data, bounds, or level/plugin. See [PCG_BEST_PRACTICES.md](PCG_BEST_PRACTICES.md) (Canonical flow).

**DemoMap:** World Partition is used; volume bounds come from config (and optionally landscape in one shot). **Load all World Partition cells (or the region containing the landscape) before Generate** so the Landscape is present when Get Landscape Data runs; see step 5 above for Load All vs Load region from selection. Enable **Is Partitioned** on the PCG component and set **Partition Grid Size** on the PCG World Actor for streaming. See **PCG volume size** above.

**Assets:** `Content/Python/pcg_forest_config.json` references `/Game/StylizedProvencal/Meshes/...`. Verify in the Content Browser that these paths exist; if the pack is missing or paths differ, the mesh list in the graph would be empty or invalid and Generate would produce nothing even if points are generated.

For more detail, see **If nothing generates** below.

---

## If nothing generates

0. **Force full regeneration:** Try **Ctrl+Click** on the Generate button in the PCG Volume’s Details panel; a normal click may not run a full generate in some cases.
1. **Landscape:** Component Subsection = **1x1**; actor has tag **`PCG_Landscape`**.
2. **Get Landscape Data (critical in UE 5.7):** Select the node → Details:
   - **Actor** → **By Tag**, tag **`PCG_Landscape`**.
   - **Component** → **By Class** → **Landscape Component**. (If you only set Actor and leave Component default, the node often outputs nothing. Set both.)
3. **Wiring:** Get Landscape Data **Out** → Surface Sampler **Surface**; Input → Surface Sampler **Bounding Shape**; chain to spawner → Output.
4. **Output Log:** Generate from the level (select PCG Volume → Details → Generate). Then open **Window → Developer Tools → Output Log** and search for `PCG`. You should see at least some lines starting with `LogPCG`. If there are **no** LogPCG lines, you are not generating from the volume in the level (go back to step 4 in "Steps only you do"). If you see "No surfaces found", Get Landscape Data is not providing surface (fix step 2). Note any red errors.
5. **Debug points:** In the graph, select the **Surface Sampler** node → Details → **Debug** section → enable **Debug** and set **Point Mesh** to a small mesh (e.g. PCG_Cube). Generate again: if coloured cubes appear on the landscape, points are fine and the issue is downstream (spawner/mesh list); if no cubes, no points are generated (fix Get Landscape Data / bounds).
6. **Volume bounds:** The script uses **config** (`volume_center_*`, `volume_extent_*` in **`demo_map_config.json`**) as the source of truth. If **`use_landscape_bounds`** is true, it tries landscape bounds first, then World Partition bounds (so the volume can be sized to the level without Load All), then config. Set the config values to match your playable region. Optional: run **check_level_bounds.py** (Tools -> Execute Python Script) to see if landscape bounds are available.
**Trees at weird angles or poking out of the volume:**

- **Weird angles / trees lying down:** The graph’s **Transform Points** node is set to **Yaw only** (0–359°); pitch and roll are 0 so trees stay upright. In UE 5.7 the **Static Mesh Spawner** has **no align-to-surface option** in Details. If trees still lie down, the rotation may be coming from the **Surface Sampler** (points inherit surface normals). Try in the graph: ensure **Transform Points** runs after the Surface Sampler and that its **Absolute Rotation** is checked so it overwrites point rotation. Tree meshes should have their pivot at the base.
- **Poking out the bottom:** Spawn Z is controlled by **transform_offset_z** in `pcg_forest_config.json` and mesh pivot, not by volume size. **volume_extent_z_padding** only enlarges the PCG Volume’s Z extent (bounds for sampling); it does not move spawn points. If meshes poke out the bottom, fix pivot and offset (see Debug below).

**Debug: trees tilted or meshes out of the bottom**

- **Mesh pivot:** In the Static Mesh editor, check whether tree/rock pivots are at the **base** or **center**. If pivot is at base, use **transform_offset_z: 0**. If pivot is at center, use a **positive** value (e.g. **250** to **400** cm) so world-space Z offset lifts the instance and the base sits on the surface. Re-run **create_demo_from_scratch.py** so the graph is updated from config, then Generate again.
- **Rotation (trees not upright):** Open **ForestIsland_PCG** in the PCG Graph editor. Confirm **Transform Points** is after Surface Sampler and before Static Mesh Spawner. Select each Transform Points node → Details: **Rotation** min/max with **Pitch = 0**, **Roll = 0** (script sets roll=0, pitch=0, yaw=0–359° via Rotator(roll, pitch, yaw)). **Absolute Rotation** = true. If still tilted, ensure there is no “Align to Normal” (or similar) that would re-apply surface rotation; rely on Transform Points for rotation. Re-running the script that places the volume will re-apply rotation/offset from `pcg_forest_config.json`.
- **volume_extent_z_padding:** Only affects the volume’s vertical bounds; it does not change spawn height. Default is 1000 cm so the volume fits around the landscape without extending far below; increase (e.g. 10000) only if sampling fails at terrain edges.

**If Generate still does nothing (Details → Generate is correct):**

- **Trigger Generate from script:** If clicking Generate in Details produces **no lines at all** in the Output Log, run generation from Python: **Tools → Execute Python Script**, then run: `import create_pcg_forest; create_pcg_forest.trigger_pcg_generate()`. Check the Output Log for lines like "PCG Forest: trigger_pcg_generate: ..." and any **LogPCG** lines; copy and share them so we can see if the graph runs when triggered from script.
- **Capture the log:** Open **Window → Developer Tools → Output Log**. In the log window, open the **Filters** dropdown and ensure **Log** (and if present, **PCG**) is enabled so messages aren’t hidden. Clear the log or note the time, then click **Generate** on the PCG Volume in Details. Wait a few seconds. Copy the **last 30–50 lines** of the Output Log (or everything that appeared) and share them — that shows whether the graph ran and any "No surfaces found" or errors.
- **Graph errors:** Open **ForestIsland_PCG** in the graph editor. Check for red error icons on any node or broken links. Confirm **Get Landscape Data** has **Out** connected to **Surface Sampler**’s **Surface** pin, and **Input** is connected to **Surface Sampler**’s **Bounding Shape** pin. Save the graph (Ctrl+S) and try Generate again.
- **Minimal test:** Create a new PCG Graph with only **Input** → **Point from Mesh** (or **Static Mesh Spawner** with one mesh). Assign it to the same volume and Generate. If that produces something, the issue is specific to ForestIsland_PCG (e.g. Get Landscape Data or wiring). If that also produces nothing, the issue may be project/engine (e.g. PCG plugin or volume execution).

See **docs/KNOWN_ERRORS.md** entries for *PCG Generate does nothing* and *PCG Surface Sampler: No surfaces found*.

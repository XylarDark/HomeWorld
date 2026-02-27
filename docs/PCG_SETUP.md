# PCG Setup — HomeWorld (UE 5.7)

Single reference for procedural trees/rocks on the landscape: what the script does, what you must do in the Editor, and where to look for help.

---

## Prerequisites

- Level open (e.g. **Main**) with a **Landscape** in it.
- **Landscape** → Details → **Component Subsection** = **1x1** (required for PCG in UE 5.x).
- The Landscape must be findable by **Get Landscape Data** via the tag **`PCG_Landscape`** (the script can add this tag).

---

## What the script does

The script (**create_demo_map.py**, or **create_pcg_forest.py** directly) **does**:

1. **Creates a PCG graph** at **`/Game/HomeWorld/PCG/ForestIsland_PCG`** if it does not exist: Get Landscape Data, Surface Sampler (bounds + surface), Density Filter, Transform Points (trees **upright**, yaw-only rotation), Static Mesh Spawner (trees); optional rocks branch and Merge; optional **Difference** for exclusion zones so trees spawn **around the village**, not inside it.
2. **Tree density** is driven by **`Content/Python/pcg_forest_config.json`**: `points_per_squared_meter` (default 0.02 = sparser), `density_lower_bound` / `density_upper_bound` (Density Filter). Lower values = fewer trees.
3. **Exclusion zones** (when **`skip_exclusion_zones`** is false in **`demo_map_config.json`**): the script auto-detects building-tagged actors and StylizedProvencal structures and builds **two** exclusion zones via simple clustering — one around the **village** (center) and one around the **castle** (top-left) — so trees spawn around them, not inside. You can also set **`exclusion_zones`** manually in config.
4. **Tags the Landscape** with **`PCG_Landscape`** if missing (`ensure_landscape_has_pcg_tag()`).
5. **Creates and sizes one PCG Volume** to the landscape bounds (or config), labeled **PCG_Forest** in the Outliner.
6. Saves the level.
7. **Attempts automation:** When the graph is created/loaded, the script tries to **assign the graph to the volume** (`try_assign_graph_to_volume`), **set Get Landscape Data to By Tag + PCG_Landscape** (`try_set_get_landscape_selector`), and **trigger Generate** (`trigger_pcg_generate`). In UE 5.7 many of these properties are protected or not exposed in Python, so these attempts often fail; the script logs what worked and what did not.

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
   - **2b.** Select the **tree Static Mesh Spawner** node — in Details under **Mesh Selector** set the mesh list (e.g. the paths from `Content/Python/pcg_forest_config.json` → `static_mesh_spawner_meshes`). If there is a **rocks** Static Mesh Spawner, select it and set its mesh list from `static_mesh_spawner_meshes_rocks`. **Without this step, Generate produces no instances.**
3. **Assign the graph** to the **PCG Volume** (Outliner → select PCG_Forest → Details → **Graph** → ForestIsland_PCG).
4. **Generate from the level:** Close or minimize the graph editor. In the **level** (e.g. Main), select **PCG_Forest** in the Outliner. In the **Details** panel (right side), scroll to the **PCG** section and click the **Generate** button there. Use this Details-panel button only — not the green Play button or Simulate on the main toolbar, and not a Generate/Run button inside the graph asset editor. **If nothing appears after a normal click, try Ctrl+Click on Generate** to force a full regeneration. After clicking Generate, **Output Log** (Window → Developer Tools → Output Log) should show lines containing `LogPCG`. If there are no LogPCG lines, the correct Generate was not used or the PCG log category may be filtered out.

If the script’s automation could not assign the graph or set Get Landscape Data (common in UE 5.7), you still need to set Get Landscape Data (and Component), **set the mesh list on each Static Mesh Spawner**, assign the graph to the volume if needed, and Generate from the level as above.

---

## Detailed manual steps (from scratch)

If you prefer to build the graph from zero in the Editor, see **[docs/tasks/PCG_MANUAL_SETUP.md](tasks/PCG_MANUAL_SETUP.md)** for step-by-step (tag Landscape, create graph, add Get Landscape Data / Surface Sampler / Static Mesh Spawner, set By Tag + `PCG_Landscape`, add PCG Volume, assign graph, Generate).

---

## References

- **Required settings automation cannot set:** See [docs/PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md) for a list of variables/settings that are necessary but not (reliably) settable from Python/MCP.
- **[freetimecoder/unreal-pcg-examples](https://github.com/freetimecoder/unreal-pcg-examples)** — Full project with PCG graphs and maps; works in UE 5.7. Open a level with a PCG Volume + graph, hit Generate, then inspect the graph (Get Landscape Data settings, node order).
- **[PacktPublishing/Procedural-Content-Generation-with-Unreal-Engine-5](https://github.com/PacktPublishing/Procedural-Content-Generation-with-Unreal-Engine-5)** — Book repo, UE 5.4+; **Chapter_2** is “Craft your first lush, procedurally generated forest.” Open the Chapter_2 project in 5.7 and mirror its graph layout and Details settings in HomeWorld.
- **Epic docs:** [PCG Framework Node Reference (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-node-reference-in-unreal-engine), [Get Landscape Data (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/PCG/UPCGGetLandscapeSettings). In 5.4+, landscape is provided only via **Get Landscape Data**; the graph Input provides bounds.

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
6. **Volume bounds:** Ensure the PCG Volume overlaps the landscape (the script sizes it to landscape bounds; if you moved the volume or landscape, resize the volume so it covers the terrain).

**Trees at weird angles or poking out of the volume:**

- **Weird angles / trees lying down:** The graph’s **Transform Points** node is set to **Yaw only** (0–359°); pitch and roll are 0 so trees stay upright. In UE 5.7 the **Static Mesh Spawner** has **no align-to-surface option** in Details. If trees still lie down, the rotation may be coming from the **Surface Sampler** (points inherit surface normals). Try in the graph: ensure **Transform Points** runs after the Surface Sampler and that its **Absolute Rotation** is checked so it overwrites point rotation. Tree meshes should have their pivot at the base.
- **Poking out the bottom:** Spawn Z is controlled by **transform_offset_z** in `pcg_forest_config.json` and mesh pivot, not by volume size. **volume_extent_z_padding** only enlarges the PCG Volume’s Z extent (bounds for sampling); it does not move spawn points. If meshes poke out the bottom, fix pivot and offset (see Debug below).

**Debug: trees tilted or meshes out of the bottom**

- **Mesh pivot:** In the Static Mesh editor, check whether tree/rock pivots are at the **base** or **center**. If pivot is at base, use **transform_offset_z: 0** in `Content/Python/pcg_forest_config.json`. If pivot is at center, use a negative value (e.g. **-250** for ~5 m height, **-400** to **-500** for taller trees). Re-run the PCG script (e.g. `create_homestead_pcg.py` or the script that places the volume) so the graph is updated from config, then Generate again.
- **Rotation (trees not upright):** Open **ForestIsland_PCG** in the PCG Graph editor. Confirm **Transform Points** is after Surface Sampler and before Static Mesh Spawner. Select each Transform Points node → Details: **Rotation** min/max should be **Yaw only** (e.g. 0–359°), **Pitch = 0**, **Roll = 0**; **Absolute Rotation** = true. In the Static Mesh Spawner, ensure there is no “Align to Normal” (or similar) that would re-apply surface rotation; rely on Transform Points for rotation. Re-running the script that places the volume will re-apply rotation/offset from `pcg_forest_config.json`.
- **volume_extent_z_padding:** Only affects the volume’s vertical bounds; it does not change spawn height. Keep it (e.g. 10000) so the volume fully contains the landscape.

**If Generate still does nothing (Details → Generate is correct):**

- **Trigger Generate from script:** If clicking Generate in Details produces **no lines at all** in the Output Log, run generation from Python: **Tools → Execute Python Script**, then run: `import create_pcg_forest; create_pcg_forest.trigger_pcg_generate()`. Check the Output Log for lines like "PCG Forest: trigger_pcg_generate: ..." and any **LogPCG** lines; copy and share them so we can see if the graph runs when triggered from script.
- **Capture the log:** Open **Window → Developer Tools → Output Log**. In the log window, open the **Filters** dropdown and ensure **Log** (and if present, **PCG**) is enabled so messages aren’t hidden. Clear the log or note the time, then click **Generate** on the PCG Volume in Details. Wait a few seconds. Copy the **last 30–50 lines** of the Output Log (or everything that appeared) and share them — that shows whether the graph ran and any "No surfaces found" or errors.
- **Graph errors:** Open **ForestIsland_PCG** in the graph editor. Check for red error icons on any node or broken links. Confirm **Get Landscape Data** has **Out** connected to **Surface Sampler**’s **Surface** pin, and **Input** is connected to **Surface Sampler**’s **Bounding Shape** pin. Save the graph (Ctrl+S) and try Generate again.
- **Minimal test:** Create a new PCG Graph with only **Input** → **Point from Mesh** (or **Static Mesh Spawner** with one mesh). Assign it to the same volume and Generate. If that produces something, the issue is specific to ForestIsland_PCG (e.g. Get Landscape Data or wiring). If that also produces nothing, the issue may be project/engine (e.g. PCG plugin or volume execution).

See **docs/KNOWN_ERRORS.md** entries for *PCG Generate does nothing* and *PCG Surface Sampler: No surfaces found*.

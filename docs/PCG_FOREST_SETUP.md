# PCG Forest Island – Programmatic Setup

This doc describes how to create the forest island (PCG graph + volume + generate) and enable World Partition using the provided Python script and, if needed, one manual step.

## Prerequisites

- **Plugins:** In `HomeWorld.uproject`, **PythonScriptPlugin** and **PCGPythonInterop** must be enabled (already added by the plan). Restart the Editor after first enable.
- **Level (required):** The script places the PCG Volume in the *current* level. The default map is `/Game/HomeWorld/Maps/Main` (see `Config/DefaultEngine.ini`). **You must create and save the Main map once if it does not exist:** in the Editor, **File → New Level** (e.g. Basic or Empty), then **File → Save Current Level As** and save as `Content/HomeWorld/Maps/Main`. Open that level before running the script; otherwise the script will log "No editor world. Open a level (e.g. Main) first." If the repo already includes `Main.umap` in `Content/HomeWorld/Maps/`, open that map and skip the create step. **Optional for maintainers:** To let new clones skip creating the map, create a minimal level in the Editor (File → New Level → Empty), save as `Content/HomeWorld/Maps/Main`, and commit the resulting `Main.umap` (tracked with Git LFS).
- **Quixel (optional):** For trees/rocks, add Quixel assets to the project (e.g. via Quixel Bridge), then list their asset paths in the config file (see below). If you skip this, the script uses engine placeholder meshes.

## Node setup (script defaults)

- **Surface Sampler:** Bounds = PCG Volume, Density = **0.05** (trees not overlapping).
- **Density Filter:** Min **0.3**, Max **1.0** (natural gaps).
- **Transform Points:** Random rotation (Yaw 0–360°), Scale **0.8–1.2** (variety).
- **Static Mesh Spawner:** Meshes from config (see below). Tree count is driven by surface density; adjust `points_per_squared_meter` in the script or in the graph if you want fewer/more trees (e.g. 0.02 for ~50 trees).

## Config file (mesh list)

- **Path:** `Content/Python/pcg_forest_config.json`
- **Trees:** `static_mesh_spawner_meshes` — add Megascans tree paths. Megascans/Quixel trees typically live under **Content/Environments/** (e.g. `/Game/Environments/Forest/SM_Tree_01`). In Content Browser, right‑click the asset → **Copy Reference**, then paste into the JSON array. Leave empty to use engine placeholder meshes.
- **Rocks (optional):** `static_mesh_spawner_meshes_rocks` — add rock mesh paths for the optional second spawner. Leave empty to skip.
- **Height filter (optional):** `height_filter_min` and `height_filter_max` — world Z in cm (e.g. `-5000` and `5000`) so instances spawn only on terrain. Set both to numbers to enable; leave `null` to skip. You may need to set the filter’s target attribute to **Position.Z** in the graph in the Editor.

## How to run the script

1. Open the project in Unreal Editor.
2. Open the level you want (e.g. **Main**).
3. **Tools → Execute Python Script** (or equivalent), then choose:
   `Content/Python/create_pcg_forest.py`
4. The script will:
   - Create a PCG graph at `/Game/HomeWorld/PCG/ForestIsland_PCG` with nodes: **Surface Sampler (0.05) → Density Filter (0.3–1.0) → Transform Points (random rotation/scale 0.8–1.2) → Static Mesh Spawner**.
   - Place a **PCG Volume** (100 m × 100 m box) at the origin, assign the graph, and **Generate** so the forest island appears.
   - Save the graph asset and the current level.
   - **Re-run:** If the graph already exists, the script removes it and creates a fresh one, so you can re-run the script after changing config without manually deleting the asset.

## Execute

- **From script:** The script calls Generate automatically after creating the graph and volume.
- **From Editor:** Open the PCG graph asset, then click **Execute Graph** (Play button top-left). Generation takes about **5–10 seconds**.

## Success

- **Target:** Roughly **50–100 trees** (and rocks if the optional second spawner is added) on the island.
- **Inspect:** Fly around with **Hold E + WASD** to check placement.

## World Partition

The script does **not** enable World Partition automatically. After running the script:

- Open **World Settings** (Window → World Settings).
- Enable **World Partition** (e.g. **Use External Actors** / streaming) and confirm conversion if prompted.
- Save the level.

This is the recommended manual step; conversion can also be done via **Tools → Convert Level** if your engine build exposes it.

## Optional: run script at Editor startup

You can launch the Editor and run the script in one go (if your engine supports it):

- **Batch file:** Edit `Run-PCGForestScript.bat` in the project root: **set `UE_EDITOR`** to your `UnrealEditor.exe` path (required; the batch exits with a message if unset). If your engine is not in the default location, you may also need to edit the hardcoded path in `Build-HomeWorld.bat` when building from the command line. Then run the batch; it will open the project and execute the Python script.
- **Manual command:** Use the path to `HomeWorld.uproject` in the project root (clone root). Example:  
  `"path/to/UnrealEditor.exe" "path/to/HomeWorld.uproject" -ExecutePythonScript="Content/Python/create_pcg_forest.py"`

Ensure the default map is already created; otherwise open the correct level first and run the script from **Tools → Execute Python Script**.

## Validation

- **Plugins:** Edit → Plugins shows PythonScriptPlugin and PCGPythonInterop enabled.
- **After script:** A PCG Graph asset exists at `/Game/HomeWorld/PCG/ForestIsland_PCG` with Surface Sampler 0.05, Density Filter 0.3–1.0, Transform Points (scale 0.8–1.2); the current level contains one PCG Volume (100×100 m) with that graph; after Generate, instances (placeholder or Megascans) appear.
- **World Partition:** In World Settings, World Partition is enabled, or you have performed the manual step above.

## Optional: polish (5 min)

- **Second spawner (rocks):** Add a second Static Mesh Spawner branch with **Density 0.01** (e.g. a second Surface Sampler with `points_per_squared_meter=0.01`, same Density Filter and Transform Points, then a second Spawner for rock meshes). Populate `static_mesh_spawner_meshes_rocks` in the config if the script supports the rocks branch; otherwise add the second spawner and meshes manually in the PCG graph in the Editor.
- **Height filter (terrain only):** Set `height_filter_min` and `height_filter_max` in `pcg_forest_config.json` (world Z in cm) and re-run the script to add a height filter node; then in the graph set the filter’s target attribute to **Position.Z** if needed. Alternatively add a **Height Filter** or **Attribute Filter** node manually in the Editor after Surface Sampler or Density Filter, set the height range to match your terrain, and connect the chain.

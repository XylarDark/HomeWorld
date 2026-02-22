# PCG Forest Island – Programmatic Setup

This doc describes how to create the forest island (PCG graph + volume + generate) and enable World Partition using the provided Python script and, if needed, one manual step.

## Prerequisites

- **Plugins:** In `HomeWorld.uproject`, **PythonScriptPlugin** and **PCGPythonInterop** must be enabled (already added by the plan). Restart the Editor after first enable.
- **Level:** The default map is `/Game/HomeWorld/Maps/Main` (see `Config/DefaultEngine.ini`). Ensure this map exists (create and save it in the Editor once if missing) before running the script, so the script can place the PCG Volume there.
- **Quixel (optional):** For trees/rocks, add Quixel assets to the project (e.g. via Quixel Bridge), then list their asset paths in the config file (see below). If you skip this, the script uses engine placeholder meshes.

## Config file (mesh list)

- **Path:** `Content/Python/pcg_forest_config.json`
- **Format:**  
  `"static_mesh_spawner_meshes": ["/Game/Path/To/QuixelTree", "/Game/Path/To/QuixelRock", ...]`
- Leave the array empty to use engine placeholder meshes. After adding Quixel content, search in the Content Browser for your trees/rocks, copy their paths (e.g. right‑click → Copy Reference), add them to this array, save the JSON, and re-run the script if you want to regenerate with the new meshes.

## How to run the script

1. Open the project in Unreal Editor.
2. Open the level you want (e.g. **Main**).
3. **Tools → Execute Python Script** (or equivalent), then choose:
   `Content/Python/create_pcg_forest.py`
4. The script will:
   - Create a PCG graph at `/Game/HomeWorld/PCG/ForestIsland_PCG` with nodes: **Surface Sampler → Density Filter → Static Mesh Spawner**.
   - Place a **PCG Volume** (100 m × 100 m box) at the origin, assign the graph, and **Generate** so the forest island appears.
   - Save the graph asset and the current level.

## World Partition

The script does **not** enable World Partition automatically. After running the script:

- Open **World Settings** (Window → World Settings).
- Enable **World Partition** (e.g. **Use External Actors** / streaming) and confirm conversion if prompted.
- Save the level.

This is the recommended manual step; conversion can also be done via **Tools → Convert Level** if your engine build exposes it.

## Optional: run script at Editor startup

You can launch the Editor and run the script in one go (if your engine supports it):

- **Batch file:** Edit `Run-PCGForestScript.bat` in the project root: set `UE_EDITOR` to your `UnrealEditor.exe` path, then run the batch. It will open the project and execute the Python script.
- **Manual command:**  
  `"path\to\UnrealEditor.exe" "path\to\HomeWorld\HomeWorld.uproject" -ExecutePythonScript="Content/Python/create_pcg_forest.py"`

Ensure the default map is already created; otherwise open the correct level first and run the script from **Tools → Execute Python Script**.

## Validation

- **Plugins:** Edit → Plugins shows PythonScriptPlugin and PCGPythonInterop enabled.
- **After script:** A PCG Graph asset exists at `/Game/HomeWorld/PCG/ForestIsland_PCG`; the current level contains one PCG Volume (100×100 m) with that graph; after Generate, instances (placeholder or Quixel) appear.
- **World Partition:** In World Settings, World Partition is enabled, or you have performed the manual step above.

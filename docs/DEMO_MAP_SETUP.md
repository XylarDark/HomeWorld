# Demo map: medieval village + PCG forest

The demo level combines the **Stylized Provencal medieval village** with a **PCG-generated forest** around it. One script run sets up the level: ensures Main exists (from the village template), opens it, creates the forest graph, places the PCG volume, and generates.

## Goal

- **Level:** `/Game/HomeWorld/Maps/Main` (Content/HomeWorld/Maps/Main).
- **Content:** Village (from StylizedProvencal) + PCG forest. Missing assets (e.g. Megascans trees) can be added later via [pcg_forest_config.json](../Content/Python/pcg_forest_config.json) or manual placement.

## How to run

1. Open the project in Unreal Editor. Ensure **PythonScriptPlugin** and **PCGPythonInterop** are enabled (see [PCG_FOREST_SETUP.md](PCG_FOREST_SETUP.md)).
2. Run the demo map script in either way:
   - **From the command line (programmatic):** Set `UE_EDITOR` in `Run-DemoMapScript.bat` to your UnrealEditor.exe path, then run the batch file. The Editor will open and execute `Content/Python/create_demo_map.py` automatically.
   - **From the Editor:** **Tools → Execute Python Script**, then choose `Content/Python/create_demo_map.py` (in the project root).
3. The script will:
   - Ensure the Main level exists. If it does not, it tries to duplicate `/Game/StylizedProvencal/Maps/Main` to `/Game/HomeWorld/Maps/Main`. If level duplication is not supported in your engine, it logs a one-time step: copy **StylizedProvencal/Maps/Main** to **HomeWorld/Maps/Main** in the Content Browser (right‑click the level → Duplicate, then move/save to Content/HomeWorld/Maps/Main).
   - Open Main if it is not already the current level (or ask you to open it if the API cannot open by path).
   - Create the PCG graph (same as [create_pcg_forest.py](Content/Python/create_pcg_forest.py)), place the PCG volume at the position/size from config, generate, and save the level.

## Config

- **Path:** `Content/Python/demo_map_config.json`
- **demo_level_path:** Target level (default `/Game/HomeWorld/Maps/Main`).
- **template_level_path:** Source level to duplicate if Main is missing (default `/Game/StylizedProvencal/Maps/Main`).
- **volume_center_x/y/z**, **volume_extent_x/y/z:** PCG volume center and half-extents in cm (default: center 0,0,0; extent 5000,5000,500 ⇒ 100×100×10 m box). Adjust to surround or avoid the village as needed.

Forest meshes (trees, rocks) are still driven by [pcg_forest_config.json](../Content/Python/pcg_forest_config.json); add paths there and re-run the script or run [create_pcg_forest.py](../Content/Python/create_pcg_forest.py) to refresh the graph.

## One-time copy (if duplication fails)

If the script reports that level duplication is not supported:

1. In the Content Browser, go to **Content/StylizedProvencal/Maps/**.
2. Right‑click **Main** → **Duplicate** (or Copy, then paste in Content/HomeWorld/Maps/).
3. Ensure the duplicate is saved as **Content/HomeWorld/Maps/Main**.
4. Open that Main level and run `create_demo_map.py` again.

After that, the script will find Main and only open it (if needed), create the graph, place the volume, and generate.

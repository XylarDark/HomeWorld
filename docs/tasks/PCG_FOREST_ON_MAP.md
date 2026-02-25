# Task: Apply PCG forest to the map

**Goal:** Procedural forest around the village.

**Status:** The script **only** tags the Landscape with `PCG_Landscape` and creates/sizes one PCG Volume. It does **not** create the PCG graph, set Get Landscape Data (Actor By Tag, etc.), or assign the graph to the volume. PCG generation **requires manual steps**: create (or copy) a PCG graph, set Get Landscape Data to By Tag + `PCG_Landscape`, assign the graph to the volume, and click Generate.

**Single reference:** **[docs/PCG_SETUP.md](../PCG_SETUP.md)** — prerequisites, what the script does vs what you do, and references (freetimecoder/unreal-pcg-examples, Packt Chapter_2, Epic 5.7 PCG docs).

**If nothing generates:** Follow **[PCG_MANUAL_SETUP.md](PCG_MANUAL_SETUP.md)** for step-by-step manual setup, or use the checklist in docs/PCG_SETUP.md.

---

## Optional: In-depth verification

1. **Open Main:** Content → HomeWorld → Maps → Main.
2. **Viewport:** Use the 3D view to confirm trees (or proxy meshes) cover the intended landscape area and the village/clearing is relatively clear.
3. **Re-run if needed:** With Editor open, run `execute_python_script("create_demo_map.py")` via MCP, or **Tools → Execute Python Script** → `Content/Python/create_demo_map.py`. This uses [demo_map_config.json](../../Content/Python/demo_map_config.json) and [pcg_forest_config.json](../../Content/Python/pcg_forest_config.json).

---

## Behavior

- **One PCG volume:** The script creates a single PCG Volume, labeled **PCG_Forest** in the Outliner. It does not create a graph or assign one.
- **Full landscape:** When the level has a Landscape actor, the volume is centered and scaled to that landscape’s bounds. With no landscape, bounds come from `demo_map_config.json` (volume_center_*, volume_extent_*).
- **You:** Create (or copy) a PCG graph, set Get Landscape Data to By Tag + `PCG_Landscape`, assign the graph to **PCG_Forest** in Details, and click **Generate**. See docs/PCG_SETUP.md.

## UE 5.7 graph flow

- **Input** (volume bounds) → Surface Sampler **Bounding Shape**
- **Get Landscape Data** (landscape surface) → Surface Sampler **Surface**
- **Surface Sampler Out** → Density Filter → [Difference] → Transform Points → Static Mesh Spawner → **Output**
- Rocks branch (same chain) → Merge → Output

Get Landscape Data in UE 5.7 has **Actor selector: By Tag only**. The script tags the Landscape with **`PCG_Landscape`**; it does **not** set the node’s Actor/Component selectors (Python API does not expose them reliably). You must set **By Tag** + `PCG_Landscape` and **Component By Class** (Landscape Component) in the Editor.

## If Generate does nothing

1. **Landscape subsections:** Select the level's **Landscape** → Details → **Component Subsection** = **1x1** (2x2 can cause no output).
2. **Get Landscape Data:** Open **ForestIsland_PCG** → select **Get Landscape Data**. The script tags the level's Landscape with **`PCG_Landscape`** and tries to set **Actor By Tag** to that tag and **Component By Class** to **LandscapeComponent**. If generation still fails: in **Details** → **Actor Selector Settings** set **Actor** to **By Tag** and the tag to **`PCG_Landscape`** (ensure your Landscape actor has that tag in Outliner → Details → Tags). Under **Component** set **By Class** to **Landscape Component** if available.
3. **Wiring:** **Get Landscape Data Out** → **Surface Sampler Surface** only. **Surface Sampler Out** → **Density Filter In**. Do not connect Get Landscape Data to Density Filter.
4. **Output Log:** After Generate, search for `PCG` or `No surfaces found`; fix 1–2 if the Surface Sampler reports no surface.
5. See `docs/KNOWN_ERRORS.md` entry *PCG Generate does nothing: landscape subsections and Get Landscape Data Actor Filter*.

## Config

- **Demo map:** `Content/Python/demo_map_config.json` (level path, volume center/extent, exclusion zones).
- **PCG forest:** `Content/Python/pcg_forest_config.json` (graph path, density, mesh references).

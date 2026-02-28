# PCG Tutorial Alignment — Manual vs Programmatic

This doc splits the PCG re-approach (research and tutorials first) into **manual** (you do in the Editor) and **programmatic** (done in code/docs) steps. Complete all programmatic steps first; then follow the manual plan.

---

## Programmatic (completed)

The following have been done in code and docs:

- **Canonical flow (from Epic)** added to [PCG_BEST_PRACTICES.md](PCG_BEST_PRACTICES.md): minimal 3-node flow (Get Landscape Data → Surface; Input → Bounding; Surface Sampler → Static Mesh Spawner → Output), Landscape 1x1 and tag; our graph extends this with Density, Transform Points, optional Difference/Merge. Links to Epic Foundation tutorial and PCG Tutorial Series.
- **Cleanup then Generate** documented in [PCG_SETUP.md](PCG_SETUP.md): for World Partition, after enabling Is Partitioned or changing Partition Grid Size, run **Cleanup** on the PCG Volume then **Generate** (Ctrl+Click for full regenerate). Added to "Generate produces nothing" checklist and to "Steps only you do" / "PCG volume size."
- **Generate produces nothing checklist** updated to include: "If you changed Partition Grid Size or enabled Is Partitioned, run **Cleanup** then **Generate**." Checklist references the canonical flow in PCG_BEST_PRACTICES.
- **Fast iteration** in PCG_SETUP.md updated to mention Cleanup then Generate when using Partitioned.
- **Minimal PCG test** procedure added as a troubleshooting step: build a graph with only Input + Get Landscape Data + Surface Sampler + one Static Mesh Spawner (no Density, Transform, exclusion); assign to volume and Generate to verify the pipeline; if that works, the issue is in our extensions (Density, Transform, Difference, rocks). See [PCG_SETUP.md](PCG_SETUP.md) and [PCG_BEST_PRACTICES.md](PCG_BEST_PRACTICES.md).
- **Script alignment:** [create_pcg_forest.py](Content/Python/create_pcg_forest.py) builds the **tutorial-minimal flow** (Input→Bounding, Get Landscape Data→Surface, Surface Sampler→…→Spawner→Output) **plus** Density Filter, Transform Points, optional Difference (exclusion zones), and optional rocks branch + Merge. Documented in PCG_BEST_PRACTICES and in a comment in the script.

---

## Manual (you do in the Editor)

Do these after the programmatic work is in place.

### 1. Follow one Epic tutorial end-to-end (recommended first)

- Open **Procedural Content Generation in Unreal Engine 5.7 - Foundation** or the first lesson of **PCG Tutorial Series** (Epic Learning / Community).
- In a **minimal test level** (e.g. Main or a duplicate with one Landscape), **without** using Homestead or the script:
  - Create a PCG Graph manually.
  - Add **Get Landscape Data** + **Surface Sampler** + **Static Mesh Spawner**.
  - Set **Get Landscape Data**: Actor → **By Tag**, tag **`PCG_Landscape`**; Component → **By Class** → **Landscape Component**.
  - Connect: **Input** → Surface Sampler **Bounding Shape**; **Get Landscape Data** → Surface Sampler **Surface**; Surface Sampler → Static Mesh Spawner → **Output**.
  - Assign a mesh to the Static Mesh Spawner. Assign the graph to a PCG Volume. Click **Generate**.
- **Record** (for your own reference or to add to this doc): exact node order, pin names that worked in 5.7, and any Surface Sampler settings you used. Confirm that **Input → Bounding** and **Get Landscape Data → Surface** is the required minimum.

### 2. Optional: Reference project verification

- Open **freetimecoder/unreal-pcg-examples** or **Packt Chapter_2** (Procedural-Content-Generation-with-Unreal-Engine-5) in UE 5.7.
- Open a level that has PCG trees/forest. Inspect the graph: Get Landscape Data settings, Surface Sampler, spawner mesh list, node order.
- Mirror those settings in HomeWorld’s ForestIsland_PCG if anything differs from our script or docs.

### 3. World Partition: Is Partitioned and Cleanup then Generate

- In **Homestead** (or any World Partition level): select **PCG_Forest** → Details → **PCG** component → enable **Is Partitioned**.
- Find the **PCG World Actor** in the level (Outliner or search) → set **Partition Grid Size** (e.g. 51200–102400 cm).
- Run **Cleanup** on the PCG Volume (Details → PCG section), then **Generate** (or Ctrl+Click for full regenerate).
- If you change Partition Grid Size or toggle Is Partitioned again, run **Cleanup** then **Generate** each time.

### 4. Homestead: Load All before Generate

- Before clicking Generate, use **Window → World Partition → Load All** (or load the region) so the Landscape is present. Get Landscape Data needs the Landscape loaded to find surfaces.

### 5. Manual steps after running the script (unchanged)

- Set **Get Landscape Data** in ForestIsland_PCG: By Tag **`PCG_Landscape`**, Component By Class **Landscape Component**.
- Set the **mesh list** on the tree (and rocks) Static Mesh Spawner in the graph Details.
- Assign **ForestIsland_PCG** to the PCG Volume in the level if the script could not.
- Click **Generate** (or Ctrl+Click) from the volume’s Details panel.

---

## Canonical flow (quick reference)

From Epic docs and tutorials; our script implements this plus extensions:

- **Get Landscape Data** (By Tag + Component By Class) → **Surface Sampler** (Surface pin).
- **Input** → **Surface Sampler** (Bounding Shape pin). Volume bounds define the sampling domain when no bounds input is connected.
- **Surface Sampler** → [optional filters] → **Static Mesh Spawner** → **Output**.
- **Landscape:** Component Subsection **1x1**; actor tag **`PCG_Landscape`**.

**Our extensions:** Density Filter, Transform Points (yaw-only, offset from config), optional Difference (exclusion zones), optional rocks branch + Merge. See [PCG_BEST_PRACTICES.md](PCG_BEST_PRACTICES.md) and [PCG_SETUP.md](PCG_SETUP.md).

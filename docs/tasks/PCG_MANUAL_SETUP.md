# PCG Manual Setup (Square One) — UE 5.7

Build the PCG graph **from zero in the Editor without using the script**. For script-based setup (ForestIsland_PCG + volume created by script), see [PCG_SETUP.md](../PCG_SETUP.md).

This doc is for when you want to create the graph entirely by hand (e.g. a minimal test graph or a different layout). The **script** (`create_homestead_from_scratch` → `create_pcg_forest`) **does** create the graph (ForestIsland_PCG), tag the Landscape, and place/size the PCG Volume; you still set Get Landscape Data (By Tag + `PCG_Landscape`), assign the graph to the volume, and click Generate. See [PCG_SETUP.md](../PCG_SETUP.md) for that workflow.

---

## Prerequisites

- Level open (e.g. **Main**) with a **Landscape** in it.
- **Landscape** → Details → **Component Subsection** = **1x1** (required for PCG sampling in UE5).

---

## Part 1: Tag the Landscape (so Get Landscape Data can find it)

1. In the **Outliner**, select your **Landscape** actor.
2. In **Details**, find **Tags** (under Actor).
3. Add a tag: **`PCG_Landscape`** (exact spelling).  
   - If there’s an **Add** or **+** next to Tags, use it and type `PCG_Landscape`.

---

## Part 2: Create a new PCG Graph from scratch

1. **Content Browser** → navigate to a folder (e.g. **Content/HomeWorld/PCG**). Create the folder if needed.
2. **Right‑click** in the folder → **PCG** → **PCG Graph**.
3. Name it (e.g. **PCG_ManualTest**). Double‑click to open the **PCG Graph Editor**.

---

## Part 3: Build the minimal graph (Input → Get Landscape Data → Surface Sampler → Spawner → Output)

In the PCG Graph Editor you should see the default **Input** and **Output** nodes.

### 3.1 Add Get Landscape Data

1. **Right‑click** in the graph → search **Get Landscape Data** → add it.
2. Select the **Get Landscape Data** node.
3. In **Details**:
   - **Actor Selector Settings** → **Actor** → set to **By Tag**.
   - Set the **tag** to **`PCG_Landscape`** (same as on the Landscape).
   - If there is a **Component** section, set it to **By Class** and choose **Landscape Component** (or leave default if that’s the only option).
   - Find **Unbounded** (or similar) and **check** it so the node uses the full landscape intersection.

### 3.2 Add Surface Sampler

1. **Right‑click** → search **Surface Sampler** → add it.
2. **Connect:**
   - **Get Landscape Data** → **Out** to **Surface Sampler** → **Surface** (the surface input).
   - **Input** → **In** (or main output) to **Surface Sampler** → **Bounding Shape** (so sampling is limited to the volume).
3. Select **Surface Sampler**. In Details set **Points Per Squared Meter** to something like **0.05** (sparse) or **0.1** (denser).

### 3.3 Add Static Mesh Spawner

1. **Right‑click** → search **Static Mesh Spawner** → add it.
2. **Connect:** **Surface Sampler** → **Out** to **Static Mesh Spawner** → **In**.
3. **Connect:** **Static Mesh Spawner** → **Out** to **Output** → **In** (or main input).
4. Select **Static Mesh Spawner**. In Details under **Mesh Selector** (or **Static Mesh**), assign **one** static mesh (e.g. a tree from your content: **StylizedProvencal/Meshes/SM_Tree_01** or any mesh).

### 3.4 (Optional) Add variation

- **Transform Points** between Surface Sampler and Static Mesh Spawner: add **Transform Points**, connect Surface Sampler → Transform Points → Static Mesh Spawner. Set random rotation (e.g. Yaw 0–360) and scale (e.g. 0.8–1.2) so instances don’t look identical.

---

## Part 4: Save the graph and add a PCG Volume

1. **Save** the PCG graph (Ctrl+S or File → Save).
2. In the **Level** viewport, **Place Actors** → search **PCG Volume** → drag it into the level.
3. **Scale/position** the volume so it **overlaps your Landscape** (e.g. cover the area where you want trees). You can use the scale tool to make it large enough to cover the landscape.
4. Select the **PCG Volume** in the Outliner.
5. In **Details**, find **Graph** (under PCG) and set it to your new graph (**PCG_ManualTest** or whatever you named it).
6. Click **Generate**.

---

## What you should see

- **Outliner:** New generated actors (e.g. under the PCG Volume or in the level) — static mesh instances.
- **Viewport:** Trees (or your chosen mesh) on the landscape inside the volume.

---

## If nothing generates

1. **Output Log** (Window → Developer Tools → Output Log): search for **PCG** or **Surface**. If you see **"No surfaces found"**, Get Landscape Data is not providing surface:
   - Confirm the **Landscape** has tag **`PCG_Landscape`**.
   - Confirm **Get Landscape Data** is set to **By Tag** and tag **`PCG_Landscape`**.
   - Confirm **Landscape** → **Component Subsection** = **1x1**.
2. Confirm **Get Landscape Data** → **Out** is connected **only** to **Surface Sampler** → **Surface** (not to the spawner or output).
3. Confirm **Surface Sampler** → **Out** goes to **Static Mesh Spawner** → **In**, and the spawner has a mesh set.
4. Confirm the **PCG Volume** overlaps the Landscape in the viewport.

---

## After it works

- You can add more nodes (Density Filter, second branch for rocks, Merge, etc.) using the same pattern: **Get Landscape Data** → **Surface**; **Input** → **Bounding Shape**; sampler → filters/transform → spawner → **Output**.
- For script-based flow (graph + volume created by script): see [PCG_SETUP.md](../PCG_SETUP.md) for prerequisites, what the script does vs what you do, and the Generate checklist.

# PCG Best Practices — HomeWorld (UE 5.7)

Summary of PCG setup and graph design aligned with Epic tutorials and reference projects. **Before changing the PCG graph or adding nodes, read this doc and [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md).**

---

## Minimal working graph

The minimal graph that produces instances on the landscape is:

**Input** → **Get Landscape Data** → **Surface Sampler** (Surface + Bounding) → [optional **Transform Points**] → **Static Mesh Spawner** → **Output**

- **Get Landscape Data** provides landscape spatial data; its **Out** goes to the Surface Sampler **Surface** pin; the graph **Input** provides bounds to the Surface Sampler **Bounding Shape** pin.
- **Surface Sampler** generates points on the landscape; configure **Points per square meter** (and optionally **Point extents**) for density.
- **Static Mesh Spawner** places meshes at those points. You must assign the **mesh list** in Details (Mesh Selector); automation cannot set it in UE 5.7.

Enhancements used in HomeWorld: **Density Filter** (density bounds), **Transform Points** (yaw-only rotation so trees stay upright, Z offset from config), optional **Difference** for exclusion zones. Optional: **Density Noise**, **Slope Filter**, **Randomize Transform** for variety.

---

## Canonical flow (from Epic)

Epic’s tutorials use this minimal flow; our script and graph extend it without changing the core:

- **Get Landscape Data** (Actor **By Tag** + tag `PCG_Landscape`; Component **By Class** → **Landscape Component**) → **Surface Sampler** (**Surface** pin).
- **Graph Input** → **Surface Sampler** (**Bounding Shape** pin). If no bounds are connected, the PCG Volume actor bounds limit the sampling domain.
- **Surface Sampler** → [optional filters] → **Static Mesh Spawner** → **Output**.

**Landscape:** Component Subsection **1x1** (UE 5.x); actor tag **`PCG_Landscape`**. In UE 5.7 landscape is provided **only** via Get Landscape Data; the graph Input provides bounds.

**Our graph** ([create_pcg_forest.py](Content/Python/create_pcg_forest.py)) builds this **tutorial-minimal flow plus**: Density Filter, Transform Points (yaw-only, Z offset), optional Difference (exclusion zones), and optional rocks branch + Merge. No structural change to the core wiring (Input→Bounding, Get Landscape Data→Surface, Surface Sampler→…→Spawner→Output).

**References:** [Procedural Content Generation in Unreal Engine 5.7 - Foundation](https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-in-unreal-engine-5) (Epic Learning), [PCG Tutorial Series](https://dev.epicgames.com/community/learning/tutorials/1wro/unreal-engine-pcg-tutorial-series).

---

## Mandatory manual steps (UE 5.7)

These cannot be set reliably from Python/MCP; they must be done in the Editor:

1. **Get Landscape Data:** **Actor** → **By Tag**, tag **`PCG_Landscape`**; **Component** → **By Class** → **Landscape Component**. Both must be set; leaving Component default often yields no output.
2. **Mesh list on Static Mesh Spawner(s):** Assign meshes in the node Details (Mesh Selector / mesh list). Use paths from `Content/Python/pcg_forest_config.json` or assign manually. Without meshes, Generate produces no instances.
3. **Graph on volume:** Assign the PCG graph to the PCG Volume in the level (Details → Graph). Script may not be able to set this.
4. **Landscape:** Tag **`PCG_Landscape`**; **Component Subsection = 1x1**.
5. **World Partition:** If the level uses World Partition, **Load All** (or load the region) before Generate so Get Landscape Data can find the Landscape.

See [PCG_SETUP.md](PCG_SETUP.md) and [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md) for the full list and troubleshooting.

---

## When to use Partitioned or Hierarchical Generation

- **Default generation:** Single-shot generation for the whole volume. Use for small/medium areas or when streaming is not critical.
- **Partitioned Generation:** Splits the PCG domain into a grid; each cell generates locally. Use when:
  - Assets cover large areas and default generation has performance issues
  - You need streaming integration with World Partition / Level Instancing
  - You want different grid sizes for different detail levels (e.g. large trees on a coarse grid, grass on a fine grid)
  Enable via **Is Partitioned** on the PCG component; configure **Partition Grid Size** on the PCG World Actor.
- **Hierarchical Generation:** Multiple grid sizes in the same graph. Use when:
  - You need fine-tuned control over generation at different scales
  - You want to speed up local updates by distributing work across grid sizes
  - Outputs should be split into separate actors that stream individually
  Enable in **Graph Settings** → **Use Hierarchical Generation** and set **HiGen Default Grid Size**. Requires Partitioned to be enabled.

Reference: [Using PCG Generation Modes (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-pcg-generation-modes-in-unreal-engine), [Using PCG with World Partition](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-pcg-with-world-partition-in-unreal-engine).

---

## World Partition: volume and partition grid

For levels using **World Partition** (e.g. Homestead):

- **Volume bounds:** Use **config** (or a fixed region) for the PCG Volume bounds. In script, `volume_center_*` and `volume_extent_*` in `homestead_map_config.json` are the source of truth; optional one-shot landscape override when available. Do **not** depend on landscape bounds for volume sizing in automation — in WP the landscape actor often has zero extent until cells stream, so script cannot reliably get landscape size.
- **Partitioned Generation:** Enable **Is Partitioned** on the PCG component and set **Partition Grid Size** on the **PCG World Actor**. The volume then only needs to **overlap** the area you want to generate; the **partition grid** defines how work is split and streamed.
- **Get Landscape Data:** Use for the **surface** only (where to place instances). At Generate time, each partition cell samples the landscape within its bounds. Landscape is the right source for surface, not for volume bounds in script.

See [PCG_SETUP.md](PCG_SETUP.md) **PCG volume size** for step-by-step (Is Partitioned, PCG World Actor grid).

---

## Reference projects and tutorials

- **Epic:** [PCG Tutorial Series](https://dev.epicgames.com/community/learning/tutorials/1wro/unreal-engine-pcg-tutorial-series), [PCG Framework Node Reference (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-node-reference-in-unreal-engine).
- **freetimecoder/unreal-pcg-examples:** UE 5.7; open a level with a PCG Volume + graph, hit Generate, then inspect the graph (Get Landscape Data settings, node order, mesh list).
- **Packt Chapter_2 (Procedural-Content-Generation-with-Unreal-Engine-5):** "Craft your first lush, procedurally generated forest"; mirror its graph layout and Details settings in HomeWorld.

Reference projects set **Get Landscape Data** to **By Tag** with the landscape tag (e.g. `PCG_Landscape`) and **Component By Class → Landscape Component**, and assign the mesh list on each Static Mesh Spawner in the graph Details. Homestead should mirror that; script creates the graph but these settings are manual.

---

## From decoration to collectible resources

PCG can place **decoration** (trees, rocks as instanced static meshes) or **resources the player can collect** (interaction, overlap, harvest, inventory). Design options:

- **Static Mesh Spawner only (decoration):** Use PCG to place trees/rocks as visual decoration. Implement collectibles via a **separate** system: place harvestable actors manually in set locations, or spawn Blueprint actors at runtime at positions derived from PCG (e.g. same density/regions). PCG defines where things *look*; interaction is elsewhere.
- **Actor Spawner (PCG-driven collectibles):** Use the **Actor Spawner** node in the PCG graph to spawn **Blueprint** actors (e.g. `BP_Resource_Tree`, `BP_Collectible`) that have collision and interaction logic. PCG defines *where* they spawn; the Blueprint defines *how* they are collected. Heavier than Static Mesh Spawner (one actor per instance); consider **Partitioned** or **Hierarchical** generation and streaming implications (class assignment, grid size). Document how to assign the spawner class in Details and any World Partition/streaming notes.
- **Hybrid:** PCG generates points and (optionally) writes attributes; a **runtime** system reads those points (e.g. PCG element reader, or saved point data) and spawns or registers collectible actors only where needed. Keeps PCG for placement and density; collectibles are a separate layer. No implementation in HomeWorld yet; document as an option when scaling to many collectibles.

When the user wants "resources in set locations for collection," recommend the option that fits: visual-only → Static Mesh + separate collectibles; PCG-placed interactives → Actor Spawner; large-scale + runtime logic → hybrid. See Epic’s **Actor Spawner** and tutorials that spawn interactive actors via PCG.

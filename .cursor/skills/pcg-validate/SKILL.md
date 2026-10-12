---
name: pcg-validate
description: Validate or troubleshoot PCG setup (ForestIsland_PCG, volume, landscape tag, spawner meshes). Use when the user reports no trees/rocks, wrong placement, or "what do I set in the graph?"
---

# PCG validate

Check that the PCG graph, volume, and landscape are correctly configured so Generate produces instances.

**Short path:** For a one-page, tutorial-aligned setup (manual-only or script + 3 steps) and **volume sizing for DemoMap**, use [docs/PCG_QUICK_SETUP.md](../../docs/PCG/PCG_QUICK_SETUP.md).

## When to use

- User says trees/rocks don't spawn, PCG "does nothing," or assets spawn wrong (below ground, tilted).
- User asks what to set in the graph or volume (Get Landscape Data, mesh list, etc.).
- Debugging "volume not sized to landscape" or "no ground" after running create_demo_from_scratch.

## Generate produces nothing — ordered checklist

When the user reports that **Generate produces no instances**, follow this order:

1. **Get Landscape Data:** In ForestIsland_PCG, select **Get Landscape Data** → Details: **Actor** → **By Tag**, tag **PCG_Landscape**; **Component** → **By Class** → **Landscape Component**. Without this, Surface Sampler gets no surface and logs "No surfaces found".
2. **Mesh list on spawners:** Tree (and rocks) **Static Mesh Spawner** nodes must have meshes in Details (Mesh Selector / mesh list). Use paths from `Content/Python/pcg_forest_config.json` or assign in the graph. Without meshes, Generate produces no instances.
3. **Graph on volume:** Select **PCG_Forest** in the level → Details → **Graph** → ForestIsland_PCG. Assign manually if the script could not.
4. **Landscape:** Tag **PCG_Landscape**; **Component Subsection = 1x1**.
5. **World Partition:** If the level uses WP (e.g. DemoMap), use **Window → World Partition → Load All** (or load the region) before Generate so Get Landscape Data can find the Landscape.

**Output Log:** After Generate, read `Saved/Logs/HomeWorld.log` for **LogPCG** and **"No surfaces found"**. Do not ask the user to open the Output Log.

**Surface Sampler Debug:** In the graph, **Surface Sampler** → Details → **Debug** → enable **Debug**, set **Point Mesh** to a small mesh (e.g. PCG_Cube). Generate again: if debug cubes appear, the problem is **downstream** (spawner/mesh list); if no cubes, the problem is **Get Landscape Data or bounds**.

**Minimal test (optional):** Create a second, minimal graph (Input → Point from Mesh or one Static Mesh Spawner with one mesh), assign to the same volume, Generate. If minimal produces output, the issue is ForestIsland_PCG; if not, the issue may be volume/level or PCG plugin.

**DemoMap:** Load All (or load region) before Generate is required. **Assets:** Verify `/Game/StylizedProvencal/Meshes/...` paths exist in Content Browser; see `pcg_forest_config.json`.

## Minimal working graph

Input → **Get Landscape Data** → **Surface Sampler** (Surface + Bounding) → [optional Transform Points] → **Static Mesh Spawner** → Output. Get Landscape Data **Out** → Surface Sampler **Surface**; graph **Input** → Surface Sampler **Bounding Shape**. When Python cannot set By Tag or the mesh list, the script logs `editor_ui: NEED_SLATE panel=pcg-details`. Open [.cursor/skills/ue-editor-ui/SKILL.md](../ue-editor-ui/SKILL.md).

## When Python cannot write the panel

Before changing the graph, try the script. If By Tag or the Static Mesh Spawner mesh list cannot be set, the log contains `editor_ui: NEED_SLATE panel=pcg-details`. Open the editor-UI skill and snapshot that Details field. Do not ask the user to click it. Graph assignment, the landscape tag, and World Partition load stay on the script when it can set them. See [docs/PCG/PCG_BEST_PRACTICES.md](../../docs/PCG/PCG_BEST_PRACTICES.md).

## General validation (when to use)

1. **Landscape tag:** The Landscape in the level must have the tag **PCG_Landscape**. The script `create_demo_from_scratch.py` calls `ensure_landscape_has_pcg_tag()`. If unsure, select the Landscape in the Outliner → Details → Actor → Tags → add PCG_Landscape. Landscape Component Subsection should be **1x1** (Details) for PCG in UE 5.x.

2. **Get Landscape Data (in graph):** Open ForestIsland_PCG → select **Get Landscape Data** node → Details: **Actor** → **By Tag**, tag **PCG_Landscape**; **Component** → **By Class** → **Landscape Component** if available. When the script cannot set this, it logs `editor_ui: NEED_SLATE panel=pcg-details`. Open the editor-UI skill.

3. **Mesh lists on spawners:** Tree and rocks Static Mesh Spawner nodes need meshes assigned in Details (Mesh Selector / mesh list). When the script cannot set these, it logs the same `pcg-details` token. Paths live in `Content/Python/pcg_forest_config.json`.

4. **Graph assigned to volume:** In the level, select **PCG_Forest** (or the PCG Volume) → Details → **Graph** → ForestIsland_PCG. If the script could not assign it (protected in UE 5.7), assign manually.

5. **Generate from level:** Generate must be triggered from the **level**: select PCG_Forest in Outliner → Details → PCG section → **Generate**. Not from inside the graph editor. If nothing appears, try Ctrl+Click on Generate.

6. **Placement (below ground / tilted):** Check [docs/PCG/PCG_SETUP.md](../../docs/PCG/PCG_SETUP.md) "Trees at weird angles" and "Poking out the bottom": mesh pivot (base vs center), `transform_offset_z` in pcg_forest_config.json (0 for base-pivot; negative for center-pivot). Transform Points node should have **Absolute Rotation** and **Yaw-only** rotation so trees stay upright; script sets these when creating/updating the graph.

## From decoration to collectible resources

When the user wants **resources in set locations for the player to collect**, recommend one of:

- **Static Mesh Spawner only:** PCG for decoration (trees/rocks); collectibles implemented separately (manual placement or runtime spawn at PCG-like positions).
- **Actor Spawner:** Use **Actor Spawner** in the graph to spawn Blueprint actors (e.g. BP_Resource_Tree) with collision and interaction; PCG defines where, Blueprint defines how they are collected. Heavier; document class assignment and partition/streaming.
- **Hybrid:** PCG generates points; a runtime system reads them and spawns/registers collectible actors. Option for large-scale or when collectibles are a separate layer.

See [docs/PCG/PCG_BEST_PRACTICES.md](../../docs/PCG/PCG_BEST_PRACTICES.md) section "From decoration to collectible resources" for details.

## References

- [docs/PCG/PCG_SETUP.md](../../docs/PCG/PCG_SETUP.md) — full steps, what script can/cannot do
- [docs/PCG/PCG_BEST_PRACTICES.md](../../docs/PCG/PCG_BEST_PRACTICES.md) — minimal graph, manual steps, Partitioned/Hierarchical, decoration vs collectibles
- [docs/PCG/PCG_VARIABLES_NO_ACCESS.md](../../docs/PCG/PCG_VARIABLES_NO_ACCESS.md) — settings that require manual Editor steps
- [docs/KNOWN_ERRORS.md](../../docs/KNOWN_ERRORS.md) — PCG and MCP pitfalls

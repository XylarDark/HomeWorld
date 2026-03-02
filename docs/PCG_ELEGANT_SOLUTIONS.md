# PCG Elegant Solutions — Research-Backed

This doc summarizes the **recurring issues** with PCG setup in HomeWorld (UE 5.7) and **elegant, research-backed approaches** so you can follow the Day 1 steps once and then rely on automation or a one-time setup.

**Context:** [PCG_SETUP.md](PCG_SETUP.md), [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md), [KNOWN_ERRORS.md](KNOWN_ERRORS.md) (PCG entries). The script creates the graph and volume and tags the landscape, but several settings cannot be set reliably from Python and have caused "no surfaces found", "nothing generated", wrong pin wiring, and tilted/misplaced instances.

---

## Problem summary (from known errors and docs)

| Issue | Cause | Current workaround |
|-------|--------|---------------------|
| **Get Landscape Data** not targeting landscape | Actor (By Tag) and tag name not settable from Python; property names not exposed or differ in 5.7 | Manual: Details → By Tag, tag `PCG_Landscape`; Component → By Class → Landscape Component |
| **Static Mesh Spawner** empty mesh list | `PCGStaticMeshSpawnerEntry` / mesh list not exposed in UE 5.7 Python (or differs from 5.3/5.4) | Manual: assign mesh list in graph Details from `pcg_forest_config.json` |
| **Graph not assigned to volume** | `graph` property on PCGComponent is protected for get/set_editor_property; `set_graph()` exists and works in 5.7 Python | Script uses `comp.set_graph(graph_asset)`; if that fails, assign in Details |
| **Surface Sampler "No surfaces found"** | Surface pin must receive data from Get Landscape Data; Bounding from Input; pin labels version-dependent | Correct wiring: Get Landscape Data → Surface; Input → Bounding; use introspection for pin names |
| **Execution Dependency pin** | Connecting data to execution pin causes "does not have the Execution Dependency label" | Wire only **data** pins for data edges; use `_first_data_input_pin_label()` etc. in script |
| **Nothing generated after Generate** | Landscape 1x1 subsections; World Partition cells unloaded; mesh list empty; or normal click not full regenerate | Checklist: 1x1, tag, mesh list, Load All, Ctrl+Click Generate |
| **Trees tilted / poking out of bottom** | Transform Points not overwriting rotation; wrong transform_offset_z vs mesh pivot | Transform Points with Absolute Rotation, Yaw only; transform_offset_z in config; see PCG_SETUP Debug |

**Sources:** Epic PCG Node Reference (UE 5.7), Tech Artist's Guide to PCG, Epic Python API (PCGComponent has `set_graph(graph)` and `generate(force)`), KNOWN_ERRORS.md, PCG_VARIABLES_NO_ACCESS.md, community (freetimecoder/unreal-pcg-examples, Packt PCG with UE 5).

---

## Recommended approach: one-time “golden” graph + automation

**Idea:** Do the **manual steps once** on a single graph asset. After that, the script only ensures the map, tags the landscape, creates/sizes the PCG Volume, **assigns the pre-configured graph** via `set_graph()`, and can trigger Generate. No graph recreation from code after the first time.

### One-time setup (you do once)

1. **Create or open the graph**  
   Run `create_demo_from_scratch.py` once (or create the graph manually per [PCG_MANUAL_SETUP.md](tasks/PCG_MANUAL_SETUP.md)).

2. **In ForestIsland_PCG, set what automation cannot:**
   - **Get Landscape Data:** Actor → **By Tag**, tag **`PCG_Landscape`**; Component → **By Class** → **Landscape Component**.
   - **Tree Static Mesh Spawner:** Mesh Selector → set the mesh list (paths from `Content/Python/pcg_forest_config.json` → `static_mesh_spawner_meshes`).
   - **Rocks Static Mesh Spawner** (if present): same from `static_mesh_spawner_meshes_rocks`.

3. **Save the graph asset** (Ctrl+S in graph editor or Save All). The graph is now your **golden template**: it already has the correct Get Landscape Data selector and mesh lists.

4. **Optional:** In the level, assign this graph to the PCG Volume (Details → Graph) and click **Generate** once to confirm trees/rocks appear. Then save the level.

### After one-time setup (automation)

- **Script behavior:** When the graph asset **already exists**, the script can **reuse it** (no force recreate). It will:
  - Ensure DemoMap and Landscape tag.
  - Create or update the PCG Volume (bounds from config).
  - Call **set_graph(graph_asset)** to assign the graph to the volume.
  - Optionally call **generate(True)** to trigger generation.
- **You no longer need to** re-enter Get Landscape Data or mesh lists each run; they are stored in the saved graph asset.
- **If you ever change density, extent, or exclusion:** Use config (`pcg_forest_config.json`, `demo_map_config.json`). The default is reuse — the script only updates volume/Transform Points and does not overwrite the graph. Set `recreate_volume_and_graph: true` only to force full recreation; if you do, you must repeat the one-time setup for Get Landscape Data and mesh lists.

**Benefit:** One-time manual setup; all future runs are script-driven (volume, assign, generate). No repeated “no surfaces found” or “no instances” from missing selector/mesh list.

---

## Alternative: introspection-driven automation

If you prefer to **avoid any manual step** and are willing to maintain engine-version-specific code:

1. **Run the introspection script** on the **actual graph** (not just default settings).  
   Extend `Content/Python/pcg_settings_introspect.py` to:
   - Load the asset at `/Game/HomeWorld/PCG/ForestIsland_PCG`.
   - For each node, get `get_settings()` and dump every `get_editor_property`-able property name and type.
   - Write results to `Saved/pcg_settings_introspect_5.7.txt` (and optionally a JSON keyed by node type).

2. **Inspect the output** for:
   - **Get Landscape Data:** The real property path for “actor by tag” and “tag name” (e.g. `actor_selector.tag` or a nested struct). Update `try_set_get_landscape_selector()` in `create_pcg_forest.py` to use those names.
   - **Static Mesh Spawner:** Whether `mesh_entries`, `mesh_selector_parameters`, or another property is writable and what type the entries use (e.g. `PCGStaticMeshSpawnerEntry` in 5.7 or a different struct). Update the mesh list code to use the discovered API.

3. **Re-run the script** after engine upgrades; Epic may expose or rename properties.

**Benefit:** Potential to set Get Landscape Data and mesh list from Python. **Cost:** Introspection and code updates per engine version; some properties may remain inaccessible.

---

## Alternative: Editor Utility Widget / C++ tool

For maximum reliability and minimal dependence on Python API gaps:

- Implement an **Editor Utility Widget** or **Editor-only C++ tool** that:
  - Finds the level’s PCG Volume and its PCGComponent.
  - Assigns the graph (C++ has full access to component and graph).
  - Optionally finds the Get Landscape Data and Static Mesh Spawner nodes in the graph and sets selector/mesh list via Editor APIs.
- Expose a single button, e.g. **“Apply PCG Setup”**, that runs this logic. The Python script can then focus on map/volume/landscape tag; the widget handles graph assignment and, if feasible, node settings.

**Benefit:** Uses Editor/C++ APIs that are stable and complete. **Cost:** More implementation and maintenance.

---

## Checklist: first-time manual setup (so the golden graph is correct)

Use this when creating or recreating ForestIsland_PCG so you don’t hit the known issues again:

- [ ] **Landscape:** Component Subsection = **1x1**; actor has tag **`PCG_Landscape`** (script can add tag).
- [ ] **Get Landscape Data:** Actor → **By Tag**, tag **`PCG_Landscape`**; Component → **By Class** → **Landscape Component**.
- [ ] **Wiring:** Get Landscape Data **Out** → Surface Sampler **Surface**; **Input** → Surface Sampler **Bounding Shape**; chain to spawner(s) → **Output**; if two branches (trees + rocks), both → **Merge** → Output.
- [ ] **Tree spawner:** Mesh list set from `pcg_forest_config.json` → `static_mesh_spawner_meshes`.
- [ ] **Rocks spawner** (if any): Mesh list from `static_mesh_spawner_meshes_rocks`.
- [ ] **Transform Points:** Absolute Rotation, **Yaw only** (pitch/roll 0); **transform_offset_z** in config matches mesh pivot (0 for base-pivot).
- [ ] **Volume:** Graph assigned in Details to **ForestIsland_PCG** (or script will set via `set_graph()`).
- [ ] **World Partition:** If the level uses WP, **Load All** (or load region) before Generate; after changing **Is Partitioned** or **Partition Grid Size**, run **Cleanup** then **Generate** (or Ctrl+Click).
- [ ] **Generate:** From level, select PCG Volume → Details → **Generate** (or **Ctrl+Click**). Confirm **LogPCG** in Output Log and instances in viewport.
- [ ] **Save:** Save the graph asset and the level.

---

## References

- [PCG_SETUP.md](PCG_SETUP.md) — Steps only you do, Generate produces nothing checklist, debug (tilted / out of bottom).
- [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md) — Full list of no-access variables and manual steps.
- [KNOWN_ERRORS.md](KNOWN_ERRORS.md) — PCG entries (graph protected, mesh entries missing, no surfaces, execution dependency, nothing generated, tilted/out of bottom).
- Epic: [PCG Framework Node Reference (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-node-reference-in-unreal-engine), [PCGComponent Python 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/PCGComponent?application_version=5.7) (`set_graph`, `generate(force)`).
- [freetimecoder/unreal-pcg-examples](https://github.com/freetimecoder/unreal-pcg-examples) — Reference project (UE 5.7); inspect Get Landscape Data and spawner in a working level.
- [PCG_BEST_PRACTICES.md](PCG_BEST_PRACTICES.md) — Minimal graph, canonical flow, mandatory manual steps.

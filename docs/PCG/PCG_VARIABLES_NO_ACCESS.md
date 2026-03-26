# PCG Variables With No (or Unreliable) Automation Access

Settings that are **necessary** for PCG to work (per tutorials and docs) but **not settable** (or not reliably settable) from Python/MCP/scripts. This explains why certain manual steps cannot be removed. See [docs/PCG_SETUP.md](PCG_SETUP.md) for the full setup checklist. To automate the one-time PCG steps without manual clicks, run the optional GUI script `py Content/Python/gui_automation/pcg_apply_manual_steps.py` with the Editor open and focused (requires PyAutoGUI and reference images in `Content/Python/gui_automation/refs/`). **Capture refs once:** Run `py Content/Python/gui_automation/capture_pcg_refs.py` with the Editor in the correct state for each prompt; refs are saved to `gui_automation/refs/`. **When to use:** If introspection and the C++ commandlet (ApplyPCGSetup) are not enough—e.g. you need to set Get Landscape Data By Tag or mesh list and have no C++ tool for it—add reference PNGs per `gui_automation/refs/README.md` (or use capture_pcg_refs.py) and run the script. See [docs/FULL_AUTOMATION_RESEARCH.md](FULL_AUTOMATION_RESEARCH.md) §10.

**Version note:** UE 5.2–5.7. In UE 5.7 the Get Landscape Data **actor selector** offers **By Tag** only (no By Class for actor).

---

## Summary table

| Node / component | Setting (UI / Details) | Necessary for | Python/automation access | Manual step |
|------------------|-----------------------|---------------|---------------------------|-------------|
| **Get Landscape Data** | Actor → By Tag; tag name (e.g. `PCG_Landscape`) | Node must find the level's Landscape | **No** — property names not exposed or differ; attempts fail silently | In graph: Get Landscape Data → Details → Actor Selector Settings → **By Tag**, tag **`PCG_Landscape`** |
| **Get Landscape Data** | Component → By Class → Landscape Component | When multiple component types exist | **No** — component selector not reliably settable | Details → Component → **By Class** → **Landscape Component** |
| **Get Landscape Data** | bUnbounded (optional) | Control landscape cache bounds vs grid bounds | Unknown — may or may not be exposed as `b_unbounded` | If needed: check Details for Unbounded and set |
| **PCG Volume (PCGComponent)** | Graph (asset reference) | Which graph runs when user clicks Generate | **Partial** — in 5.7 Python `set_graph()` often works; if not, assign in Details | Script tries `comp.set_graph(graph_asset)`; else Outliner → Details → **Graph** |
| **Static Mesh Spawner** | Mesh selector / mesh entries | Which static meshes to spawn (trees, rocks) | **No / partial** — `PCGStaticMeshSpawnerEntry` missing in Python 5.7; mesh list not settable like in Editor | In graph: Static Mesh Spawner → Details → assign static mesh(s) |
| **Actor Spawner (PCGSpawnActorSettings)** | Template Actor / Actor Class | Which Blueprint to spawn (e.g. BP_HarvestableTree) | **Tried** — script tries `template_actor`, `actor_class`, `template`; if not exposed in 5.7 Python, set manually | In graph: Actor Spawner node → Details → **Template Actor** (or **Actor Class**) → BP_HarvestableTree |
| **Surface Sampler** | Points Per Squared Meter, Unbounded, Point Extents, etc. | Density and sampling behavior | **Yes** — exposed in 5.7: `points_per_squared_meter`, `unbounded`, `point_extents`, `point_steepness`, `looseness`, etc. | Not required manually if script sets them |
| **Wiring (all nodes)** | Pin labels (Out, Surface, Bounding Shape, Execution Dependency) | Correct graph connections | **Version-dependent** — pin names vary by engine (e.g. "Out" vs "Output"); must introspect at runtime if building graph from code | When building graph manually: connect Get Landscape Data **Out** → Surface Sampler **Surface**; **Input** → Surface Sampler **Bounding Shape** |

---

## Per-node details

### Get Landscape Data (UPCGGetLandscapeSettings)

- **Actor Filter (By Tag + tag name):** Tutorials and Epic Node Reference state the node must target the level's Landscape; in UE 5.7 the actor selector is **By Tag** only. The script tags the Landscape with `PCG_Landscape` but cannot set the node's Actor selector or tag name from Python — property names are not exposed or differ. **Source:** Epic PCG Node Reference (Get Actor Data / Get Landscape Data), Tech Artist's Guide to PCG, Epic Forums (PCG with multiple Landscape actors), docs/tasks/PCG_MANUAL_SETUP.md.
- **World Partition (Empty Open World):** The root Landscape actor can have **0 components**; components live on **LandscapeStreamingProxy** actors. Get Landscape Data (By Tag) finds all actors with the tag; if only one proxy is tagged, instances spawn only in that cell. Scripts tag **all** loaded LandscapeStreamingProxy actors with `PCG_Landscape` so By Tag returns the full surface. **Manual:** Load the World Partition region(s) containing the landscape (select all cells or the full grid → Load region from selection), then run the script (or diagnostic) so all proxies are tagged; then Generate.
- **Component selector (By Class, Landscape Component):** Same; not reliably settable from Python.
- **bUnbounded / SamplingProperties:** Documented in Epic API summary; Python exposure unknown. Re-check with introspection script if needed.

### PCG Volume (PCGComponent)

- **Graph assignment:** All tutorials say "assign the graph in Details." Python: `graph` is protected for get/set_editor_property; **`set_graph(graph_asset)`** exists and often works in UE 5.7. The script tries it; if it fails, assign in Details. **Source:** All PCG setup tutorials; docs/KNOWN_ERRORS.md; [PCG_ELEGANT_SOLUTIONS.md](PCG_ELEGANT_SOLUTIONS.md).

### Static Mesh Spawner

- **Mesh selector / mesh entries:** Tutorials say "assign one static mesh in Details." Python: `PCGStaticMeshSpawnerEntry` is missing in UE 5.7; mesh entries may be partially or fully inaccessible from script. **Source:** docs/KNOWN_ERRORS.md (PCG script: PCGStaticMeshSpawnerEntry missing).

### Actor Spawner (PCGSpawnActorSettings)

- **Template Actor / Actor Class:** When `spawn_harvestable_trees` is true in pcg_forest_config.json, the script creates an Actor Spawner for the tree branch and tries to set the template (properties `template_actor`, `actor_class`, or `template`). If none are exposed or settable in UE 5.7 Python, the script logs that you must set **Template Actor** to BP_HarvestableTree in the graph Details. **Manual:** Open ForestIsland_PCG → select the Actor Spawner node → Details → **Template Actor** (or **Actor Class**) → assign `/Game/HomeWorld/Building/BP_HarvestableTree`.

### Surface Sampler (PCGSurfaceSamplerSettings)

- **Points Per Squared Meter, Unbounded, Point Extents, etc.:** Required for density/sampling. **Python 5.7:** Exposed as `points_per_squared_meter`, `unbounded`, `point_extents`, `point_steepness`, `looseness`, `apply_density_to_points`, `keep_zero_density_points`, `use_legacy_grid_creation_method`. No need for manual steps for these if automation sets them. **Source:** Epic Python API (PCGSurfaceSamplerSettings, UE 5.7).
- **Seed / use_seed:** When the graph has two Surface Samplers (trees + rocks), both must use **different seeds** or they generate the same point set and rocks spawn on top of trees. The script sets seed 12345 on the first (tree) and 54321 on the second (rocks); `update_forest_island_graph_from_config` applies the same when updating an existing graph.

### Wiring (pin labels)

- **Out, Surface, Bounding Shape, Execution Dependency:** Required for correct edges when building the graph. Pin labels can vary by engine version (e.g. "Out" vs "Output"); automation must introspect at runtime. **Source:** docs/KNOWN_ERRORS.md (pin name errors, Execution Dependency label).

### Homestead map

- **Same no-access items** as above apply when running PCG on the Homestead map (`/Game/HomeWorld/Maps/Homestead`). Script `Content/Python/create_homestead_from_scratch.py` places/sizes the PCG Volume and tags the Landscape; it cannot set Get Landscape Data, graph assignment, or mesh list.
- **Compound exclusion:** `homestead_map_config.json` defines `exclusion_zones` (compound bounds). To keep trees out of the compound, either duplicate **ForestIsland_PCG** to **Homestead_PCG**, add or configure a **Difference** node with a **Points from Bounds** (or similar) source using those bounds, or set the exclusion box in the graph to match the config. See [docs/HOMESTEAD_MAP.md](HOMESTEAD_MAP.md).
- **Trees tilted or meshes out of bottom:** Check Transform Points (Absolute Rotation, Yaw only) and **transform_offset_z** in `pcg_forest_config.json` vs mesh pivot. See [docs/KNOWN_ERRORS.md](KNOWN_ERRORS.md) (PCG: trees tilted or meshes poking out of the bottom) and [docs/PCG_SETUP.md](PCG_SETUP.md) (Debug: trees tilted or meshes out of the bottom).

---

## Introspection and script-driven updates

**Run introspection in Editor:** Execute `Content/Python/pcg_settings_introspect.py` (Tools → Execute Python Script or MCP). Output is written to `Saved/pcg_settings_introspect_5.7.txt`. The script dumps all properties for **PCGGetLandscapeSettings**, **PCGStaticMeshSpawnerSettings**, **PCGComponent**, and the nodes in `ForestIsland_PCG`.

**Use the output:** Check the introspect file for property names that are readable (and, if you try `set_editor_property`, writable). Update `try_set_get_landscape_selector()` and `try_set_spawner_mesh_lists()` in [Content/Python/create_pcg_forest.py](../Content/Python/create_pcg_forest.py) with any exact property paths that work (e.g. a nested `actor_selector_settings.tag_name`). Re-run introspection after engine upgrades; Epic may expose or rename properties.

**Set via script in 5.7 (when available):** Graph assignment often works via `comp.set_graph(graph_asset)`. Get Landscape Data (By Tag + tag name) and Static Mesh Spawner mesh list are usually **still no access** from Python in 5.7; the script tries multiple property names. If introspection reveals writable paths, add them to the try_set_* functions and note here. Otherwise use the **C++ commandlet** or the one-time "golden" graph manual setup.

**C++ commandlet (ApplyPCGSetup):** When Python cannot assign the graph, run the Editor with a level loaded and execute: `UnrealEditor.exe HomeWorld.uproject <MapPath> -run=HomeWorldEditor.ApplyPCGSetup [GraphPath=/Game/HomeWorld/PCG/ForestIsland_PCG] [Tag=PCG_Landscape] [MeshList=/Game/Path1,/Game/Path2,...]`. The commandlet finds the first actor with a PCGComponent in the level, loads the graph asset, and calls `SetGraph()`. Tag and MeshList are accepted and logged; applying them to graph nodes (Get Landscape Data By Tag, Static Mesh Spawner mesh entries) is not yet implemented in the commandlet—use one-time manual setup or Editor + auto-clicker (`pcg_apply_manual_steps.py` with refs). Then use Details > Generate in the Editor to run the graph. See [PCG_SETUP.md](PCG_SETUP.md) and [PCG_ELEGANT_SOLUTIONS.md](PCG_ELEGANT_SOLUTIONS.md).

---

## References

- [Epic: PCG Framework Node Reference (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-node-reference-in-unreal-engine)
- [Epic: Get Landscape Data API (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/PCG/UPCGGetLandscapeSettings)
- [Epic: Tech Artist's Guide to PCG](https://dev.epicgames.com/community/learning/knowledge-base/KP2D/unreal-engine-a-tech-artists-guide-to-pcg)
- [Epic: Managing Actor Tags for PCG](https://dev.epicgames.com/community/learning/tutorials/WDBK/unreal-engine-managing-actor-tags-for-pcg-with-enumerators)
- [Epic Forums: PCG with multiple Landscape actors](https://forums.unrealengine.com/t/pcg-with-multiple-landscape-actors/2455967)
- [freetimecoder/unreal-pcg-examples](https://github.com/freetimecoder/unreal-pcg-examples) (UE 5.5; inspect Get Landscape Data Details in a level)
- [Packt: Procedural Content Generation with Unreal Engine 5](https://github.com/PacktPublishing/Procedural-Content-Generation-with-Unreal-Engine-5) — Chapter_2 "Craft your first lush, procedurally generated forest" (UE 5.4+)
- [Epic Python API: PCGSurfaceSamplerSettings (5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/PCGSurfaceSamplerSettings?application_version=5.7)
- **HomeWorld:** [docs/PCG_SETUP.md](PCG_SETUP.md), [docs/KNOWN_ERRORS.md](KNOWN_ERRORS.md), [docs/tasks/PCG_MANUAL_SETUP.md](tasks/PCG_MANUAL_SETUP.md)

---

## Introspection (optional)

To see what Python actually exposes for Get Landscape Data, Static Mesh Spawner, and **actual graph node settings**, run the Editor script `Content/Python/pcg_settings_introspect.py`. Output is written to `Saved/pcg_settings_introspect_5.7.txt`. The script also loads `ForestIsland_PCG` (if it exists) and dumps properties from each node’s settings so you can add any writable tag/selector/mesh_entries names to `try_set_get_landscape_selector()` or mesh list code. Re-run after engine upgrades. See [PCG_ELEGANT_SOLUTIONS.md](PCG_ELEGANT_SOLUTIONS.md) for the one-time “golden” graph approach and introspection-driven automation.

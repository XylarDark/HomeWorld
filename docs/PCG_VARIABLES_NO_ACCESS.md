# PCG Variables With No (or Unreliable) Automation Access

Settings that are **necessary** for PCG to work (per tutorials and docs) but **not settable** (or not reliably settable) from Python/MCP/scripts. This explains why certain manual steps cannot be removed. See [docs/PCG_SETUP.md](PCG_SETUP.md) for the full setup checklist.

**Version note:** UE 5.2–5.7. In UE 5.7 the Get Landscape Data **actor selector** offers **By Tag** only (no By Class for actor).

---

## Summary table

| Node / component | Setting (UI / Details) | Necessary for | Python/automation access | Manual step |
|------------------|-----------------------|---------------|---------------------------|-------------|
| **Get Landscape Data** | Actor → By Tag; tag name (e.g. `PCG_Landscape`) | Node must find the level's Landscape | **No** — property names not exposed or differ; attempts fail silently | In graph: Get Landscape Data → Details → Actor Selector Settings → **By Tag**, tag **`PCG_Landscape`** |
| **Get Landscape Data** | Component → By Class → Landscape Component | When multiple component types exist | **No** — component selector not reliably settable | Details → Component → **By Class** → **Landscape Component** |
| **Get Landscape Data** | bUnbounded (optional) | Control landscape cache bounds vs grid bounds | Unknown — may or may not be exposed as `b_unbounded` | If needed: check Details for Unbounded and set |
| **PCG Volume (PCGComponent)** | Graph (asset reference) | Which graph runs when user clicks Generate | **No** — `graph` is protected; `set_graph()` unreliable across builds | Outliner → select PCG Volume → Details → **Graph** → assign your graph |
| **Static Mesh Spawner** | Mesh selector / mesh entries | Which static meshes to spawn (trees, rocks) | **No / partial** — `PCGStaticMeshSpawnerEntry` missing in Python 5.7; mesh list not settable like in Editor | In graph: Static Mesh Spawner → Details → assign static mesh(s) |
| **Surface Sampler** | Points Per Squared Meter, Unbounded, Point Extents, etc. | Density and sampling behavior | **Yes** — exposed in 5.7: `points_per_squared_meter`, `unbounded`, `point_extents`, `point_steepness`, `looseness`, etc. | Not required manually if script sets them |
| **Wiring (all nodes)** | Pin labels (Out, Surface, Bounding Shape, Execution Dependency) | Correct graph connections | **Version-dependent** — pin names vary by engine (e.g. "Out" vs "Output"); must introspect at runtime if building graph from code | When building graph manually: connect Get Landscape Data **Out** → Surface Sampler **Surface**; **Input** → Surface Sampler **Bounding Shape** |

---

## Per-node details

### Get Landscape Data (UPCGGetLandscapeSettings)

- **Actor Filter (By Tag + tag name):** Tutorials and Epic Node Reference state the node must target the level's Landscape; in UE 5.7 the actor selector is **By Tag** only. The script tags the Landscape with `PCG_Landscape` but cannot set the node's Actor selector or tag name from Python — property names are not exposed or differ. **Source:** Epic PCG Node Reference (Get Actor Data / Get Landscape Data), Tech Artist's Guide to PCG, Epic Forums (PCG with multiple Landscape actors), docs/tasks/PCG_MANUAL_SETUP.md.
- **Component selector (By Class, Landscape Component):** Same; not reliably settable from Python.
- **bUnbounded / SamplingProperties:** Documented in Epic API summary; Python exposure unknown. Re-check with introspection script if needed.

### PCG Volume (PCGComponent)

- **Graph assignment:** All tutorials say "assign the graph in Details." Python: `graph` is protected; `set_graph()` exists but is not reliable across builds. **Source:** All PCG setup tutorials; docs/KNOWN_ERRORS.md.

### Static Mesh Spawner

- **Mesh selector / mesh entries:** Tutorials say "assign one static mesh in Details." Python: `PCGStaticMeshSpawnerEntry` is missing in UE 5.7; mesh entries may be partially or fully inaccessible from script. **Source:** docs/KNOWN_ERRORS.md (PCG script: PCGStaticMeshSpawnerEntry missing).

### Surface Sampler (PCGSurfaceSamplerSettings)

- **Points Per Squared Meter, Unbounded, Point Extents, etc.:** Required for density/sampling. **Python 5.7:** Exposed as `points_per_squared_meter`, `unbounded`, `point_extents`, `point_steepness`, `looseness`, `apply_density_to_points`, `keep_zero_density_points`, `use_legacy_grid_creation_method`. No need for manual steps for these if automation sets them. **Source:** Epic Python API (PCGSurfaceSamplerSettings, UE 5.7).

### Wiring (pin labels)

- **Out, Surface, Bounding Shape, Execution Dependency:** Required for correct edges when building the graph. Pin labels can vary by engine version (e.g. "Out" vs "Output"); automation must introspect at runtime. **Source:** docs/KNOWN_ERRORS.md (pin name errors, Execution Dependency label).

### Homestead map

- **Same no-access items** as above apply when running PCG on the Homestead map (`/Game/HomeWorld/Maps/Homestead`). Script `Content/Python/create_homestead_from_scratch.py` places/sizes the PCG Volume and tags the Landscape; it cannot set Get Landscape Data, graph assignment, or mesh list.
- **Compound exclusion:** `homestead_map_config.json` defines `exclusion_zones` (compound bounds). To keep trees out of the compound, either duplicate **ForestIsland_PCG** to **Homestead_PCG**, add or configure a **Difference** node with a **Points from Bounds** (or similar) source using those bounds, or set the exclusion box in the graph to match the config. See [docs/HOMESTEAD_MAP.md](HOMESTEAD_MAP.md).
- **Trees tilted or meshes out of bottom:** Check Transform Points (Absolute Rotation, Yaw only) and **transform_offset_z** in `pcg_forest_config.json` vs mesh pivot. See [docs/KNOWN_ERRORS.md](KNOWN_ERRORS.md) (PCG: trees tilted or meshes poking out of the bottom) and [docs/PCG_SETUP.md](PCG_SETUP.md) (Debug: trees tilted or meshes out of the bottom).

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

To see what Python actually exposes for Get Landscape Data on your engine build, run the Editor script `Content/Python/pcg_settings_introspect.py` (if present). Output is written to `Saved/pcg_settings_introspect_5.7.txt` (or similar). Re-run after engine upgrades and update this doc if new properties become available.

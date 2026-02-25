# Known Errors

Record errors and their fixes here so they are not repeated. See `.cursor/rules/07-ai-agent-behavior.mdc` (Error recurrence prevention) and `05-error-handling.mdc` (Learning from errors).

## Entry format

For each entry use:

- **Error** – What failed (command, file, or step).
- **Cause** – Likely reason.
- **Fix** – What was done to resolve it.
- **Context** – Optional: area (e.g. build, API, refactor) or date.

---

## Entries

### UnrealMCP plugin: ANY_PACKAGE removed in UE 5.7
- **Error:** `error C2065: 'ANY_PACKAGE': undeclared identifier` in UnrealMCPBlueprintCommands.cpp and UnrealMCPBlueprintNodeCommands.cpp (9 occurrences).
- **Cause:** `ANY_PACKAGE` macro was deprecated in UE 5.1 and fully removed in UE 5.7. The unreal-mcp plugin (chongdashu/unreal-mcp) targets UE 5.5.
- **Fix:** Replace all `ANY_PACKAGE` with `nullptr` in `FindObject<UClass>()` calls.
- **Context:** 2026-02, UnrealMCP plugin build, UE 5.7 migration.

### UnrealMCP plugin: CompressImageArray deprecated in UE 5.7
- **Error:** `error C2664: cannot convert argument 4 from 'TArray<uint8>' to 'TArray<uint8, FDefaultAllocator64>&'` in UnrealMCPEditorCommands.cpp.
- **Cause:** `FImageUtils::CompressImageArray` deprecated; replaced by `PNGCompressImageArray` which requires `TArray64<uint8>`.
- **Fix:** Replace `CompressImageArray` with `PNGCompressImageArray` and change `TArray<uint8>` to `TArray64<uint8>`.
- **Context:** 2026-02, UnrealMCP plugin build, UE 5.7 migration.

### UnrealMCP plugin: BufferSize name collision in UE 5.7
- **Error:** `error C4459: declaration of 'BufferSize' hides global declaration` in MCPServerRunnable.cpp (treated as error in UE 5.7).
- **Cause:** Global `const int32 BufferSize = 8192` in plugin code shadows a local in UE's `StringConv.h` header.
- **Fix:** Rename to `static constexpr int32 MCPRecvBufferSize = 8192`.
- **Context:** 2026-02, UnrealMCP plugin build, UE 5.7 migration.

### UnrealMCP plugin: FPaths::IsRelativePath removed in UE 5.7
- **Error:** `error C2039: 'IsRelativePath': is not a member of 'FPaths'` in UnrealMCPEditorCommands.cpp.
- **Cause:** `FPaths::IsRelativePath` was renamed to `FPaths::IsRelative` in UE 5.7.
- **Fix:** Replace `FPaths::IsRelativePath(...)` with `FPaths::IsRelative(...)`.
- **Context:** 2026-02, UnrealMCP plugin build, UE 5.7 migration.

### MCP set_blueprint_property: full asset path causes Editor crash
- **Error:** Fatal error: `Attempted to create a package with name containing double slashes. PackageName: /Game/Blueprints//Game/HomeWorld/GameMode/BP_GameMode` — Editor crashes.
- **Cause:** `FindBlueprintByName` in UnrealMCPCommonUtils.cpp prepends `/Game/Blueprints/` to the blueprint_name argument. Passing a full path like `/Game/HomeWorld/GameMode/BP_GameMode` creates the invalid double-slash path.
- **Fix:** Always pass only the short Blueprint name (e.g. `BP_GameMode`) to MCP tools like `set_blueprint_property`, `compile_blueprint`, etc. Never pass a full `/Game/...` asset path as the blueprint name.
- **Context:** 2026-02, MCP runtime, Editor crash.

### MCP set_blueprint_property: cannot set inherited C++ UPROPERTY values
- **Error:** `Property not found: MeshForwardYawOffset` (and similar for `Mesh Forward Yaw Offset`, `mesh_forward_yaw_offset`) when calling `set_blueprint_property` on a Blueprint child of a C++ class.
- **Cause:** The MCP plugin's property lookup does not resolve C++ `UPROPERTY` names inherited from the parent class. It likely only finds properties defined directly in the Blueprint.
- **Fix:** Use Python Editor scripts (`setup_character_blueprint.py`) to set inherited properties via `set_editor_property()` on the Blueprint's default object. MCP cannot be used for this.
- **Context:** 2026-02, MCP runtime, BP_HomeWorldCharacter.

### MCP set_component_property: cannot find inherited C++ components
- **Error:** `Component not found: CharacterMesh0` and `Component not found: Mesh` when calling `set_component_property` on a Blueprint child of ACharacter.
- **Cause:** Components created in the C++ constructor (like `CharacterMesh0`) are not visible to the MCP plugin's component lookup on the Blueprint asset.
- **Fix:** Use Python Editor scripts to access the component via `get_editor_property()` or the SubobjectDataSubsystem. MCP cannot set properties on inherited components.
- **Context:** 2026-02, MCP runtime, BP_HomeWorldCharacter.

### Python InputMappingContext.map_key: Key struct from string
- **Error:** `TypeError: NativizeProperty: Cannot nativize 'str' as 'ToKey' (StructProperty)` / `Key: Struct has 0 initialization parameters, but the given sequence had 1 elements` when calling `imc.map_key(action, "W")` in setup_enhanced_input.py.
- **Cause:** UE Python API expects `to_key` to be a `Key` struct. Passing a string fails because `unreal.Key` has no string constructor; it has a single editor property `key_name` (Name).
- **Fix:** Construct the key with `key_obj = unreal.Key()` then `key_obj.set_editor_property("key_name", unreal.Name(key_name))`. Use that key object in `map_key(action, key_obj)`.
- **Context:** 2026-02, Content/Python/setup_enhanced_input.py, UE 5.7.

### AnimBlueprint: no get_editor_property("parent_class") in Python
- **Error:** `Reparent failed: AnimBlueprint: Failed to find property 'parent_class' for attribute 'parent_class' on 'AnimBlueprint'` when running `setup_animation_blueprint.py`.
- **Cause:** `UAnimBlueprint` does not expose a `parent_class` editor property in the Python API (unlike regular `UBlueprint`). The effective parent is the super class of the Blueprint's generated class.
- **Fix:** In Python, get the current parent via the generated class: load the ABP, get `abp.generated_class()` (or `BlueprintEditorLibrary.generated_class(abp)`), then get the super class with `gen_class.get_super_class()` or `gen_class.get_editor_property("super_class")`. Use that to decide whether to call `BlueprintEditorLibrary.reparent_blueprint(abp, target_parent_class)`.
- **Context:** 2026-02, setup_animation_blueprint.py, Animation Blueprint reparenting.

### GameplayAbilities: GameplayAbilitySpec.h include path
- **Error:** `fatal error C1083: Cannot open include file: 'Abilities/GameplayAbilitySpec.h': No such file or directory` in HomeWorldCharacter.cpp.
- **Cause:** The GameplayAbilities plugin exposes the header as `GameplayAbilitySpec.h` (under the module's Public folder), not `Abilities/GameplayAbilitySpec.h`.
- **Fix:** Use `#include "GameplayAbilitySpec.h"` instead of `#include "Abilities/GameplayAbilitySpec.h"`.
- **Context:** 2026-02, GAS default ability granting, UE 5.7.

### UCollisionProfile::OverlapAllDynamic_ProfileName not in UE 5.7
- **Error:** `error C2039: 'OverlapAllDynamic_ProfileName': is not a member of 'UCollisionProfile'` in HomeWorldBuildOrder.cpp and HomeWorldResourcePile.cpp.
- **Cause:** The constant was removed or renamed in UE 5.7; the engine collision profile list is name-based.
- **Fix:** Use `SetCollisionProfileName(FName("OverlapAllDynamic"))` instead of `UCollisionProfile::OverlapAllDynamic_ProfileName`.
- **Context:** 2026-02, agentic building C++ (AHomeWorldBuildOrder, AHomeWorldResourcePile), UE 5.7.

### UE 5.7 Python API: get_actor_bounds() signature changed
- **Error:** `get_actor_bounds() takes at most 2 arguments (4 given)` when calling `actor.get_actor_bounds(False, origin, extent, False)`.
- **Cause:** In UE 5.7, `get_actor_bounds(bOnlyCollidingComponents)` returns a `(origin, box_extent)` tuple instead of accepting out-parameters.
- **Fix:** Replace `actor.get_actor_bounds(False, origin, extent, False)` with `origin, extent = actor.get_actor_bounds(False)`.
- **Context:** 2026-02, Python Editor scripting, affects landscape bounds and actor bounds queries.

### Unreal Python: module caching prevents picking up script changes
- **Error:** Changes to Python scripts (e.g. `create_pcg_forest.py`) are not reflected when re-running `create_demo_map.py` or `bootstrap_project.py` because Python caches imported modules in `sys.modules`.
- **Cause:** The Unreal Editor Python session persists across script executions. `import module` reuses the cached version instead of re-reading from disk.
- **Fix:** Add `importlib.reload(module)` after each import in orchestrator scripts. Applied to `create_demo_map.py` and `bootstrap_project.py`.
- **Context:** 2026-02, Python Editor scripting, module caching.

### UE 5.7 Python: AnimBP factory class named differently
- **Error:** `AnimationBlueprintFactory` not found in `unreal` module when trying to create an Animation Blueprint programmatically.
- **Cause:** In UE 5.7, the factory class is `AnimBlueprintFactory`, not `AnimationBlueprintFactory`.
- **Fix:** Try multiple names: `AnimBlueprintFactory`, `AnimationBlueprintFactory`, `AnimBlueprint_Factory`.
- **Context:** 2026-02, Python Editor scripting, AnimBP creation.

### MCP set_blueprint_property: cannot find GameMode Blueprints
- **Error:** `Blueprint not found: BP_GameMode` when calling `set_blueprint_property` with the short name.
- **Cause:** The MCP plugin searches specific asset paths (likely `/Game/Blueprints/`) and does not find Blueprints stored in other directories (e.g. `/Game/HomeWorld/GameMode/`).
- **Fix:** Unknown — the MCP plugin's asset search is limited. Use Python Editor scripts or manual Editor steps to configure GameMode properties.
- **Context:** 2026-02, MCP runtime, BP_GameMode.

### Family/swarm agents: use UE 5.7 recommended Mass Entity + Mass AI
- **Error:** N/A (policy).
- **Cause:** Project previously avoided Mass; Epic's current (non-deprecated) stack for crowds and lightweight AI is Mass Entity + Mass AI.
- **Fix:** Use UE 5.7 recommended Mass Entity + Mass AI for family/swarm agents. Enable: MassEntity, MassGameplay, MassAI, StateTree, ZoneGraph, SmartObjects (and MassNavigation, MassRepresentation as required). See STACK_PLAN Layer 5 and docs/tasks/FAMILY_AGENTS_MASS_STATETREE.md.
- **Context:** 2026-02, stack plan, Week 2 family agents.

### Build HomeWorldEditor (CreateMEC commandlet) fails: Live Coding active
- **Error:** `Unable to build while Live Coding is active. Exit the editor and game...`
- **Cause:** Building the Editor target (HomeWorldEditor module) while the Unreal Editor is running triggers Live Coding checks and blocks the build.
- **Fix:** Close the Unreal Editor (and any PIE session), then run `Build-HomeWorld.bat`. To run the CreateMEC commandlet, use the engine executable with `-run=HomeWorldEditor.CreateMEC` (Editor must not be running for that too). See docs/ALTERNATIVE_AUTOMATION_OPTIONS.md.
- **Context:** 2026-02, HomeWorldEditor module, CreateMEC commandlet.

### FAssetRegistryModule::Get() is not static in UE 5.7
- **Error:** `error C2352: 'FAssetRegistryModule::Get': a call of a non-static member function requires an object`
- **Cause:** In UE 5.7, `FAssetRegistryModule::Get()` is an instance method, not a static one.
- **Fix:** Use `FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry").Get()` to obtain the registry, then call `AssetCreated()` etc. Include `Modules/ModuleManager.h`.
- **Context:** 2026-02, CreateMECCommandlet, asset registration.

### PCG create_demo_map: Graph protected, PCGStaticMeshSpawnerEntry missing, pin names
- **Error:** (1) `PCGComponent: Property 'Graph' for attribute 'graph' on 'PCGComponent' is protected and cannot be set` when using set_editor_property("graph", ...); (2) same property `cannot be read` when calling get_editor_property("graph") in trigger_pcg_generate. (3) `module 'unreal' has no attribute 'PCGStaticMeshSpawnerEntry'` so tree/rock mesh entries are not set. (4) `LogPCG: Error: From node DefaultInputNode does not have the Out label` (pin names vary by engine version).
- **Cause:** UE 5.7: PCGComponent graph is protected for both set (via set_editor_property) and get; **set_graph(graph_asset) does work** for assignment. PCGStaticMeshSpawnerEntry/PCGMeshSelectorSingleMesh not in Python API; default/Difference node pin labels are internal.
- **Fix:** (1) Assign graph via comp.set_graph(graph_asset), not set_editor_property. (2) In trigger_pcg_generate do not read the graph property; wrap any read in try/except and call comp.generate(True) — UE 5.7 requires the force argument. (3) Meshes: user sets mesh list in graph Details (PCG_SETUP.md step 2b). (4) Introspect pin labels at runtime. (5) PCGVolume: use only BoxComponent for exclusion extent.
- **Context:** 2026-02, Content/Python/create_pcg_forest.py, create_demo_map.py, PCG forest trees/rocks.

### PCG Surface Sampler: "No surfaces found from which to generate"
- **Error:** `LogPCG: Warning: [PCGVolume_7 - SurfaceSampler_0/1]: No surfaces found from which to generate` and `Could not initialize per-execution timeslice state data`.
- **Cause:** The Surface Sampler needs **surface** data (e.g. landscape geometry), not just bounds. Connecting only the graph Input node provides bounds; in UE 5.7 that does not supply the actual surface, so the sampler reports no surfaces.
- **Fix:** Add a **Get Landscape Data** node (`PCGGetLandscapeSettings`) to the graph, connect its output to the Surface Sampler's **Surface** input pin, and connect the graph Input to the Surface Sampler's **Bounding** input (if present). Introspect pin labels via `_get_node_all_input_pin_labels()` so "Surface" and "Bounding" are wired correctly. If `PCGGetLandscapeSettings` is not available in Python, the script skips the node and logs "Get Landscape Data node skipped"; user must assign the graph and Generate, or add the node manually in the PCG Editor.
- **Context:** 2026-02, Content/Python/create_pcg_forest.py, PCG forest.

### PCG: "From node GetLandscapeData_0 does not have the Execution Dependency label"
- **Error:** `LogPCG: Error: From node GetLandscapeData_0 does not have the Execution Dependency label` when the graph includes a Get Landscape Data node connected to the Surface Sampler.
- **Cause:** PCG nodes have both data pins (e.g. "Surface", "Bounding", "Out") and execution pins ("Execution Dependency"). Connecting a data output (e.g. from Get Landscape Data) to an "Execution Dependency" input fails because the engine expects the source to have an output named "Execution Dependency". Using the first input pin when "Surface" was missing picked "Execution Dependency" for the landscape→Surface Sampler edge.
- **Fix:** (1) Use only data pins for data edges: introduce `_first_data_input_pin_label()` to choose the first input label that is not "Execution Dependency". Use that for surface_pin when "Surface" is not in the list. (2) Connect execution separately: if the Input node has an "Execution Dependency" output, connect it to the Surface Sampler's and Get Landscape Data's "Execution Dependency" inputs via `_get_output_pin_label_by_name()`. Only add execution edges when the source has that output.
- **Context:** 2026-02, Content/Python/create_pcg_forest.py, PCG graph wiring.

### PCG nothing generated (trees/rocks) after assigning graph and Generate
- **Error:** User assigns ForestIsland_PCG to the PCG Volume and clicks Generate but no trees or rocks appear; no useful log output.
- **Cause:** (1) Using a separate Get Landscape Data node changed execution/data flow so the Surface Sampler did not receive the right input in some engine/context. (2) Both tree and rock branches connected directly to the Output node; some PCG versions only use one input, so one branch overwrote the other or only one stream was used.
- **Fix:** (1) Use the **canonical SimpleForest flow**: feed the Surface Sampler from the graph **Input** node only (no Get Landscape Data). When the graph is run by a PCG Volume, the Input provides the landscape surface within the volume. (2) Add a **Merge** node: connect both the tree spawner and rock spawner to the Merge node, then Merge → Output, so both branches contribute. (3) Keep Get Landscape Data optional (`use_get_landscape = False`); when enabled, set `b_unbounded` on its settings.
- **Context:** 2026-02, Content/Python/create_pcg_forest.py, PCG forest generation.

### PCG Generate does nothing: landscape subsections and Get Landscape Data (UE 5.7 By Tag / Component By Class)
- **Error:** After assigning ForestIsland_PCG and clicking Generate, no trees or rocks appear (Surface Sampler may log "No surfaces found" or nothing at all).
- **Cause:** (1) **Landscape component subsections:** Use **1x1** (2x2 can cause no output). (2) **Get Landscape Data (UE 5.7):** Actor selector offers **By Tag** only (no By Class); Component selector offers **By Class** and **By Tag**. The node must find the level's Landscape (e.g. Actor By Tag = `PCG_Landscape` with that tag on the Landscape actor, and/or Component By Class = Landscape Component). (3) **Normal click on Generate** may not run a full regeneration in some cases.
- **Fix:** (1) Landscape → Details → **Component Subsection** = **1x1**. (2) Ensure the level's **Landscape** actor has tag **`PCG_Landscape`** (script adds it via `ensure_landscape_has_pcg_tag()`). (3) In the PCG graph → **Get Landscape Data** → Details: set **Actor** to **By Tag** and tag **`PCG_Landscape`**; set **Component** to **By Class** and **Landscape Component** if needed. (4) Wiring: **Get Landscape Data Out** → **Surface Sampler Surface** only; **Surface Sampler Out** → spawner/filter chain → **Output**. (5) **If setup is correct but nothing appears:** try **Ctrl+Click** on the Generate button in the PCG Volume Details to force a full regeneration.
- **Context:** 2026-02, Content/Python/create_pcg_forest.py, UE 5.7 PCG. See also **docs/PCG_VARIABLES_NO_ACCESS.md** for all variables with no (or unreliable) access.

### PCG Static Mesh Spawner: no align-to-surface option (UE 5.7)
- **Error:** Trees spawn lying down or tilted; docs suggested turning off "align to surface" on the spawner.
- **Cause:** In UE 5.7 the **Static Mesh Spawner** node has **no align-to-surface or orient-to-normal option** in Details. Rotation may come from the Surface Sampler (point normals).
- **Fix:** Rely on **Transform Points** (Absolute Rotation, yaw-only) to overwrite point rotation. If trees still lie down, the Surface Sampler may be setting point rotation before Transform Points; ensure Transform Points is in the chain and Absolute Rotation is enabled. See **docs/PCG_SETUP.md** (trees lying down).
- **Context:** 2026-02, PCG forest; do not suggest "turn off align on spawner" — the option does not exist.

### PCG: script does not create graph or assign graph; manual steps required
- **Error:** N/A (policy). Running create_demo_map.py or setup_level with run_pcg=True does not result in trees/rocks.
- **Cause:** The Python API does not expose Get Landscape Data's Actor/Component selector (By Tag, tag name, By Class) or the PCG Volume's graph assignment in a way that can be set reliably. The script therefore only tags the Landscape and creates/sizes the PCG Volume.
- **Fix:** Create (or copy from a reference project) a PCG graph, set Get Landscape Data to **By Tag** + **`PCG_Landscape`**, assign the graph to the PCG Volume in Details, and click **Generate**. See **docs/PCG_SETUP.md** for the full checklist and references.
- **Context:** 2026-02, PCG Fundamental Redo; script reduced to tag + volume only. See also **docs/PCG_VARIABLES_NO_ACCESS.md** for all variables with no (or unreliable) access.

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

### Duplicated level: World Partition shows None and is not editable
- **Error:** After duplicating Main to create the Homestead map (or any level), **World Settings → World Partition** shows **None** and the field cannot be edited (grayed out or read-only).
- **Cause:** Duplicated levels do not get a World Partition asset assigned; the level is still a non–World Partition level until it is explicitly converted.
- **Fix:** With the duplicated level (e.g. Homestead) open, use **Tools → Convert Level** from the main menu. This converts the current level to World Partition and assigns the asset. After conversion, World Settings will show the World Partition asset and streaming will be enabled. Save the level.
- **Context:** 2026-02, Homestead map creation; applies to any level duplicated from another. See [HOMESTEAD_MAP.md](HOMESTEAD_MAP.md), [SETUP.md](SETUP.md).

### World Partition conversion creates a second map (Homestead_WP)
- **What happens:** After **Tools → Convert Level**, the Editor has two level assets: the original (e.g. **Homestead**) and the converted one (e.g. **Homestead_WP**). The converted one has World Partition and streaming; the original does not.
- **Which to use:** Use **Homestead_WP** (the one with World Partition). Do all homestead layout, PCG, and placeholders in that map.
- **To keep only one:** Delete the old **Homestead** in Content Browser, then rename **Homestead_WP** to **Homestead** so config/scripts that reference `/Game/HomeWorld/Maps/Homestead` still work. See [HOMESTEAD_MAP.md](HOMESTEAD_MAP.md) (“Why two maps”).

### Homestead: no ground visible after World Partition conversion
- **Error:** Placeholders and PCG trees are visible but there is no landscape/ground; everything appears to float.
- **Cause:** After **Tools → Convert Level**, the Landscape is in a World Partition **streaming cell**. Only cells that are loaded appear in the Editor; if the cell containing the Landscape is not loaded, the ground is not visible.
- **Fix:** **Window → World Partition** → use **Load All** (or **Load All Streamed Levels** / **Load All Cells**) so all cells load and the Landscape appears. Alternatively, load only the region around the origin (where the homestead is). If no Landscape actor exists in the Outliner at all, add one via **Mode → Landscape → Create New**. See [HOMESTEAD_MAP.md](HOMESTEAD_MAP.md) (“No ground visible”).

### World Partition bounds from Python (UE 5.7): World has no get_world_partition; Blueprint library takes no args
- **Error:** Script needs landscape or World Partition bounds for PCG volume sizing. `world.get_world_partition()` does not exist; `WorldPartitionBlueprintLibrary.get_runtime_world_bounds(world)` fails with `takes no arguments (1 given)`.
- **Cause:** UE 5.7 Python does not expose `get_world_partition` on `unreal.World`. The Blueprint library’s `get_runtime_world_bounds` / `get_editor_world_bounds` are exposed as **no-argument** methods (they use the current/context world internally).
- **Fix:** In `level_loader._get_world_partition_bounds`: call `lib.get_runtime_world_bounds()` and `lib.get_editor_world_bounds()` with **no arguments**. Do not pass `world`. If the current editor level is the one with World Partition, the library returns that world’s bounds. See [level_loader.py](Content/Python/level_loader.py).
- **Context:** 2026-02, Homestead from scratch / PCG volume sizing; landscape has 0 components until Load All, so we fall back to WP bounds when available.

### PCG diagnostic: landscape_components=0 even when region is loaded
- **Error:** `pcg_generate_nothing_diagnostic.py` reports `landscape_components=0` and `extent=(0,0,0)` even after the World Partition loaded region includes the landscape and the viewport shows the ground.
- **Cause:** In World Partition, the **root** Landscape actor (e.g. Landscape1) has **Component Count: 0** in Details; the actual components (143 total) live on **LandscapeStreamingProxy** child actors. Python’s `land.get_components_by_class(LandscapeComponent)` on the root therefore returns 0. This matches the Editor UI (Details → Information → Component Count: 0, Total Component Count: 143).
- **Fix:** Do not rely on the diagnostic’s component count. Ensure **Landscape1** (the root) has tag **PCG_Landscape**; Get Landscape Data finds by tag and should use loaded proxies. Click **Generate** on the PCG Volume and check **Output Log** (LogPCG, “No surfaces found”). If instances appear, PCG is working. See [PCG_SETUP.md](PCG_SETUP.md) “Generate produces nothing”.
- **Context:** 2026-02, PCG debug; Homestead uses LandscapeStreamingProxy; root Landscape shows 0 components, proxies hold the geometry.

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

### PowerShell: Get-Content -Tail and -Raw cannot be used together
- **Error:** `The 'Raw' and 'Tail' parameters cannot be specified in the same command` when running Run-RefinerAgent.ps1.
- **Cause:** Get-Content does not allow -Raw (return whole file as one string) and -Tail (return last N lines) in the same call.
- **Fix:** Use Get-Content -Tail N only, then join lines: `$lines = Get-Content -Path $Path -Tail 60; $text = $lines -join "`n"`.
- **Context:** 2026-03-03, Tools/Run-RefinerAgent.ps1.

### C++: GameplayStatics include path (UE 5.7)
- **Error:** `fatal error C1083: Cannot open include file: 'GameFramework/GameplayStatics.h': No such file or directory` when building HomeWorldDungeonEntrance.cpp.
- **Cause:** UGameplayStatics lives in the Kismet module; the correct include is Kismet/GameplayStatics.h, not GameFramework/GameplayStatics.h.
- **Fix:** Use `#include "Kismet/GameplayStatics.h"`.
- **Context:** 2026-03-03, T5 Dungeon entrance (OpenLevel).

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

### RunAutomationLoop: prompt becomes "---" when NEXT_SESSION_PROMPT has only one fence
- **Error:** Developer agent exits in 0m with exit code 1; automation_loop.log shows `prompt preview: ---`.
- **Cause:** Get-PromptText in RunAutomationLoop.ps1 expected content *between* two "---" fences. When NEXT_SESSION_PROMPT.md has only one "---", `-split "---", 3` yields two parts, so the "middle block" branch was skipped. The fallback then took the first line that doesn't start with `#` or `**`, which is the line "---" itself, so the agent received the prompt "---" and exited immediately.
- **Fix:** In Get-PromptText: (1) Use content after the first "---" (parts[1]) when parts.Count -ge 2 and parts[1] is non-empty and not literally "---". (2) In the fallback, exclude the line "---" so it is never returned as the prompt.
- **Context:** 2026-03-03, Watch-AutomationAndFix; Fixer round. Tools/RunAutomationLoop.ps1.

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

### SO_WallBuilder: Slot at index N needs to provide a behavior definition
- **Error:** Content validation reports: `/Game/HomeWorld/Building/SO_WallBuilder Slot at index 0 needs to provide a behavior definition since there is no default one in the SmartObject definition` (and index 1).
- **Cause:** The Smart Object definition has slots but no **Default Behavior Definitions**. Each slot must have a behavior (either from the slot or from the definition’s default).
- **Fix (non-experimental, no Gameplay Behavior Smart Objects plugin):** Run `Content/Python/create_so_wall_builder.py` in the Editor (Tools → Execute Python Script or MCP). The script creates **DA_SO_WallBuilder_Behavior** and assigns it to SO_WallBuilder’s **Default Behavior Definitions**, so validation passes. You do not need to create the behavior asset manually: **USmartObjectBehaviorDefinition** inherits from **UObject** (not UDataAsset), so the class does not appear in the Editor’s “Data Asset” creation menu; the script creates it via the asset tools API. If the script reports “HomeWorldSmartObjectBehaviorDefinition not found”, build the project and restart the Editor. For full build behavior later, extend the C++ class or add logic that uses the Smart Object.
- **Context:** Day 10 SO_WallBuilder. We avoid the experimental “Gameplay Behavior Smart Objects” plugin by using a minimal C++ subclass of `USmartObjectBehaviorDefinition` in the HomeWorld module.

### PCG: rocks spawn on top of trees (same positions)
- **Error:** In ForestIsland_PCG with both tree and rocks branches, rocks appear only at the base of each tree; no rocks elsewhere on the ground.
- **Cause:** Both Surface Sampler nodes (tree and rocks) had no seed set, so they used the same default and generated identical point sets. Rocks and trees therefore shared the same XY positions.
- **Fix:** Set different seeds on each Surface Sampler: tree branch 12345, rocks branch 54321. In [create_pcg_forest.py](Content/Python/create_pcg_forest.py), set `use_seed` and `seed` on both Surface Samplers in `create_pcg_graph`, and in `update_forest_island_graph_from_config` set seed on each Surface Sampler when updating an existing graph (first = 12345, second = 54321). Run the demo script then Generate so the graph uses the new seeds.
- **Context:** 2026-03, PCG ForestIsland_PCG; two branches + Merge. See [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md) (Surface Sampler seed).

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

### GAS: NonInstanced ability instancing policy deprecated
- **Error:** Asset validation log: "Gameplay Ability Instancing Policy is NonInstanced which is deprecated. Use InstancedPerActor."
- **Cause:** UE has deprecated `NonInstanced` in favor of `InstancedPerActor` for ability instances.
- **Fix:** In `UHomeWorldGameplayAbility` constructor (HomeWorldGameplayAbility.cpp), set `InstancingPolicy = EGameplayAbilityInstancingPolicy::InstancedPerActor`. Rebuild; Blueprint abilities inheriting from this class will use the new default.
- **Context:** 2026-02, GA_PrimaryAttack, GA_Dodge, GA_Interact validation.

### PIE: AttachTo "cannot be attached to itself" (BP_RiverSpline, BP_Walls)
- **Error:** `AttachTo: '...DefaultSceneRoot' cannot be attached to itself. Aborting.` spams the log when playing in Homestead (PIE).
- **Cause:** In StylizedProvencal Blueprints (e.g. BP_RiverSpline, BP_Walls), the root component’s **Attach Parent** is set to itself, or Blueprint/construction logic calls AttachToComponent on the root with itself.
- **Fix:** Open each Blueprint (Content → StylizedProvencal/Blueprints): in the Components tree, select the root (DefaultSceneRoot). In Details, set **Attach Parent** to None (or the intended parent). If attachment is done in Event Graph/Construction Script, ensure the target is not the same component. Save the Blueprint.
- **Context:** 2026-02, Homestead map PIE; assets from StylizedProvencal pack.

### DaySequence M_24HrSky depends on Landmass plugin (not mounted)
- **Error:** `While trying to load package /DaySequence/M_24HrSky, a dependent package /Landmass/Landscape/OldPrototype_BP/... was not available`; "plugin Landmass is not mounted."
- **Cause:** Day Sequence or a level uses M_24HrSky material that references Landmass plugin content; Landmass is not enabled in the project.
- **Fix:** Either enable the **Landmass** plugin (Edit → Plugins → search Landmass) and restart, or remove/replace the M_24HrSky (or dependent) usage so the project does not reference Landmass content.
- **Context:** 2026-02, Editor startup / Day Sequence.

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
- **Error:** Changes to Python scripts (e.g. `create_pcg_forest.py`) are not reflected when re-running `create_homestead_from_scratch.py` or `bootstrap_project.py` because Python caches imported modules in `sys.modules`.
- **Cause:** The Unreal Editor Python session persists across script executions. `import module` reuses the cached version instead of re-reading from disk.
- **Fix:** Add `importlib.reload(module)` after each import in orchestrator scripts. Applied to `create_homestead_from_scratch.py`, `setup_level.py`, and `bootstrap_project.py`.
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
- **Error:** `Unable to build while Live Coding is active. Exit the editor and game...` (or Exit code: 6 in Build-HomeWorld.log)
- **Cause:** Building the Editor target (HomeWorldEditor module) while the Unreal Editor is running triggers Live Coding checks and blocks the build.
- **Fix (automatic):** Use **`.\Tools\Safe-Build.ps1`** instead of `Build-HomeWorld.bat`; it closes the Editor if running and retries once on Editor-related failure. Or run `py Content/Python/run_automation_cycle.py` (without `--no-build`), which applies the same protocol. See docs/EDITOR_BUILD_PROTOCOL.md.
- **Context:** 2026-02, HomeWorldEditor module, CreateMEC commandlet.

### FAssetRegistryModule::Get() is not static in UE 5.7
- **Error:** `error C2352: 'FAssetRegistryModule::Get': a call of a non-static member function requires an object`
- **Cause:** In UE 5.7, `FAssetRegistryModule::Get()` is an instance method, not a static one.
- **Fix:** Use `FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry").Get()` to obtain the registry, then call `AssetCreated()` etc. Include `Modules/ModuleManager.h`.
- **Context:** 2026-02, CreateMECCommandlet, asset registration.

### PCG script (create_homestead_from_scratch): Graph protected, PCGStaticMeshSpawnerEntry missing, pin names
- **Error:** (1) `PCGComponent: Property 'Graph' for attribute 'graph' on 'PCGComponent' is protected and cannot be set` when using set_editor_property("graph", ...); (2) same property `cannot be read` when calling get_editor_property("graph") in trigger_pcg_generate. (3) `module 'unreal' has no attribute 'PCGStaticMeshSpawnerEntry'` so tree/rock mesh entries are not set. (4) `LogPCG: Error: From node DefaultInputNode does not have the Out label` (pin names vary by engine version).
- **Cause:** UE 5.7: PCGComponent graph is protected for both set (via set_editor_property) and get; **set_graph(graph_asset) does work** for assignment. PCGStaticMeshSpawnerEntry/PCGMeshSelectorSingleMesh not in Python API; default/Difference node pin labels are internal.
- **Fix:** (1) Assign graph via comp.set_graph(graph_asset), not set_editor_property. (2) In trigger_pcg_generate do not read the graph property; wrap any read in try/except and call comp.generate(True) — UE 5.7 requires the force argument. (3) Meshes: user sets mesh list in graph Details (PCG_SETUP.md step 2b). (4) Introspect pin labels at runtime. (5) PCGVolume: use only BoxComponent for exclusion extent.
- **Context:** 2026-02, Content/Python/create_pcg_forest.py, create_homestead_from_scratch.py, PCG forest trees/rocks.

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

### PCG: trees tilted or meshes poking out of the bottom of the landscape
- **Error:** (1) Trees/rocks not all upright (some tilted). (2) Trees/rocks appear to spawn out of the bottom of the landscape.
- **Cause:** (1) **Tilted:** Transform Points rotation or Absolute Rotation not applied in the graph, or spawner re-applying surface normal rotation. (2) **Out of bottom:** Mesh pivot (base vs center) does not match **transform_offset_z** in config (negative offset with base-pivot pushes mesh into ground; wrong offset for center-pivot causes clipping).
- **Fix:** (1) **Tilted:** In ForestIsland_PCG, ensure **Transform Points** runs after Surface Sampler with **Absolute Rotation** checked and **Yaw only** (Pitch = 0, Roll = 0). Disable any “Align to Normal” on the Static Mesh Spawner if present. Re-run the script that places the PCG volume so config is re-applied. (2) **Out of bottom:** Check mesh pivot in Static Mesh editor; set **transform_offset_z** in `pcg_forest_config.json`: **0** for base-pivot meshes, **negative** (e.g. -250 for ~5 m height) for center-pivot. Re-run the PCG script so the graph is updated from config. See **docs/PCG_SETUP.md** (Debug: trees tilted or meshes out of the bottom).
- **Context:** 2026-02, PCG forest/Homestead.

### PCG: script does not create graph or assign graph; manual steps required
- **Error:** N/A (policy). Running create_homestead_from_scratch.py or setup_level with run_pcg=True does not result in trees/rocks (manual mesh list and Generate required).
- **Cause:** The Python API does not expose Get Landscape Data's Actor/Component selector (By Tag, tag name, By Class) or the PCG Volume's graph assignment in a way that can be set reliably. The script therefore only tags the Landscape and creates/sizes the PCG Volume.
- **Fix:** Create (or copy from a reference project) a PCG graph, set Get Landscape Data to **By Tag** + **`PCG_Landscape`**, assign the graph to the PCG Volume in Details, and click **Generate**. See **docs/PCG_SETUP.md** for the full checklist and references.
- **Context:** 2026-02, PCG Fundamental Redo; script reduced to tag + volume only. See also **docs/PCG_VARIABLES_NO_ACCESS.md** for all variables with no (or unreliable) access.

### MEC (Mass Entity Config): no trait in dropdown exposes Static Mesh
- **Error:** The MEC Traits **Add** dropdown does not show a trait that has **Static Mesh** or **Mesh**; family agents spawn with no visible mesh.
- **Cause:** The representation trait lives in the **MassRepresentation** module (part of MassGameplay). The HomeWorldEditor module did not depend on MassRepresentation, so `StaticLoadClass` for `MassRepresentationFragmentTrait` failed and the commandlet could not add the trait. The Editor MEC trait picker may also not list it if the module was not loaded.
- **Fix:** Add **MassRepresentation** to `PrivateDependencyModuleNames` in [Source/HomeWorldEditor/HomeWorldEditor.Build.cs](Source/HomeWorldEditor/HomeWorldEditor.Build.cs). Rebuild with `Build-HomeWorld.bat` (Editor closed). Run the CreateMEC commandlet: `UnrealEditor.exe HomeWorld.uproject -run=HomeWorldEditor.CreateMEC [Path=/Game/HomeWorld/Mass/MEC_FamilyGatherer]`. Open **MEC_FamilyGatherer** in the Editor; the representation trait should now be present. Set **Static Mesh** and **Scale** (1.0) in Details. For finding a cube/placeholder mesh in UE 5.7, use **only** Epic 5.7–sourced steps: see [UE57_EDITOR_UI.md](UE57_EDITOR_UI.md) (Show Engine Content, then browse or search). Save. See [DAY11_FAMILY_SPAWN.md](tasks/DAY11_FAMILY_SPAWN.md) Step 2.
- **Context:** 2026-03, MEC_FamilyGatherer, family agent visualization.

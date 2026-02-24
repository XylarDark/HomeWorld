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

### GameplayAbilities: GameplayAbilitySpec.h include path
- **Error:** `fatal error C1083: Cannot open include file: 'Abilities/GameplayAbilitySpec.h': No such file or directory` in HomeWorldCharacter.cpp.
- **Cause:** The GameplayAbilities plugin exposes the header as `GameplayAbilitySpec.h` (under the module's Public folder), not `Abilities/GameplayAbilitySpec.h`.
- **Fix:** Use `#include "GameplayAbilitySpec.h"` instead of `#include "Abilities/GameplayAbilitySpec.h"`.
- **Context:** 2026-02, GAS default ability granting, UE 5.7.

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

### Night swarms: do not use Mass Entity; use Epic's replacement when documented
- **Error:** N/A (policy).
- **Cause:** Mass Entity is deprecated in UE 5.5+ and has been removed from this project. Epic will document a replacement for swarms.
- **Fix:** Do not add Mass Entity or Mass C++ to the project. When implementing night swarms (Weeks 3–4), use whatever Mass-related plugin or API Epic documents as the replacement. See STACK_PLAN Layer 5 (AI and Simulation).
- **Context:** 2026-02, stack plan, swarms.

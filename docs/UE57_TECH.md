# UE 5.7 tech stack and checklist

Single entry point for Unreal Engine 5.7 development in HomeWorld: when to plan first, where decisions live, and what to check before or after engine/plugin work.

## When to use this doc

- Starting **UE 5.7 API, plugin, or engine-related work** (C++, Blueprint, PCG, Python Editor scripts).
- Before adding or changing code that touches **FindObject**, **FPaths**, image utils, collision profiles, PCG graph, or Python Unreal APIs (e.g. `get_actor_bounds`, AnimBP factory).
- After an **engine or plugin upgrade** (e.g. 5.7 → 5.8) to know what to re-verify.
- Planning **multi-system UE work** (e.g. Mass migration, PCG graph v2) — save plans under [.cursor/plans/](../.cursor/plans/) (see [SPEC_AND_PLAN.md](SPEC_AND_PLAN.md)).

## Key links

| Topic | Where |
|-------|--------|
| C++ conventions and UE 5.7 API pitfalls | [.cursor/rules/unreal-cpp.mdc](../.cursor/rules/unreal-cpp.mdc) |
| Recorded errors and fixes | [KNOWN_ERRORS.md](KNOWN_ERRORS.md) |
| PCG settings automation cannot set | [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md) |
| C++ vs Blueprint, code-first checklist | [CONVENTIONS.md](CONVENTIONS.md) |
| Plugins, layers, stack | [STACK_PLAN.md](STACK_PLAN.md) |
| Plan before code (complex work) | [SPEC_AND_PLAN.md](SPEC_AND_PLAN.md), [.cursor/rules/17-plan-first.mdc](../.cursor/rules/17-plan-first.mdc) |
| Automation “no access” procedure | [.cursor/rules/automation-standards.mdc](../.cursor/rules/automation-standards.mdc) |

## Canonical examples

- **C++ pawn and basics:** [Source/HomeWorld/HomeWorldCharacter.h](../Source/HomeWorld/HomeWorldCharacter.h), `HomeWorldCharacter.cpp` — includes, naming, UPROPERTY/UFUNCTION.
- **GAS (abilities and attributes):** [Source/HomeWorld/HomeWorldGameplayAbility.h](../Source/HomeWorld/HomeWorldGameplayAbility.h), [HomeWorldAttributeSet.h](../Source/HomeWorld/HomeWorldAttributeSet.h) — base ability and attribute set for UE 5.7.
- **Python Editor (level/landscape):** [Content/Python/level_loader.py](../Content/Python/level_loader.py) — idempotent helpers, check-before-create, UE 5.7 Python API (e.g. `get_actor_bounds` tuple return).
- **Python PCG automation:** [Content/Python/create_pcg_forest.py](../Content/Python/create_pcg_forest.py) — graph creation, pin wiring, and documented limits (see PCG_VARIABLES_NO_ACCESS.md).

## UE 5.7 audit (game code)

- **C++ (Source/HomeWorld):** Grep for `FindObject`, `ANY_PACKAGE`, `FPaths::IsRelativePath`, `UCollisionProfile::`, `FImageUtils::`, `SCENE_QUERY_STAT` — **no matches**. Game module is clean; known pitfalls were in the UnrealMCP plugin (documented in KNOWN_ERRORS.md).
- **Python (Content/Python):** `get_actor_bounds` uses the UE 5.7 tuple-return signature in `level_loader.py`, `create_pcg_forest.py`, `setup_level.py`. AnimBP factory uses try-multiple-names in `setup_animation_blueprint.py`. No remaining deprecated usage in repo; plugin/build fixes are in KNOWN_ERRORS.md.

## Plugins and 5.7 status

| Plugin | 5.7 status |
|--------|------------|
| PCG, GameplayAbilities, EnhancedInput, SteamSockets, DaySequence | In use; no known 5.7 issues in game code. |
| PythonScriptPlugin, PCGPythonInterop, PythonAutomationTest | In use; see KNOWN_ERRORS for Python API changes (get_actor_bounds, AnimBP factory). |
| UnrealMCP | Patched for 5.7 (ANY_PACKAGE, CompressImageArray, BufferSize, FPaths::IsRelative); see KNOWN_ERRORS. |
| MassEntity, MassGameplay, MassAI, StateTree, ZoneGraph, SmartObjects | UE 5.7 recommended stack for family/swarm agents; see [tasks/FAMILY_AGENTS_MASS_STATETREE.md](tasks/FAMILY_AGENTS_MASS_STATETREE.md). |
| ModelingToolsEditorMode | Enabled; no special 5.7 notes. |

## When upgrading the engine (e.g. to 5.8)

1. **Re-run automation access checks** — PCG (Get Landscape Data, graph assignment, mesh lists), MCP (property/component resolution), Python (get_actor_bounds, factories, AssetRegistry). See [.cursor/rules/automation-standards.mdc](../.cursor/rules/automation-standards.mdc).
2. **Update pitfalls and known errors** — Refresh the table in [unreal-cpp.mdc](../.cursor/rules/unreal-cpp.mdc) and add or update entries in [KNOWN_ERRORS.md](KNOWN_ERRORS.md) for any new deprecations or API renames.
3. **Verify build and tests** — Run `Build-HomeWorld.bat`, check `Build-HomeWorld.log`; run Python automation tests and PIE validation (e.g. `pie_test_runner.py`).
4. **Update this doc** — Adjust plugin status and audit notes if needed.

## Plan first for UE work

For **multi-file or multi-system** UE work (e.g. new GAS abilities, Mass setup, PCG graph changes), follow [17-plan-first.mdc](../.cursor/rules/17-plan-first.mdc): propose a short plan and get approval before editing. Save plans under `.cursor/plans/` when the task is large enough to benefit from resume or future reference.

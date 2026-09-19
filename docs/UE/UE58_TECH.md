# UE 5.8 tech stack and checklist

Single entry point for Unreal Engine **5.8** development in HomeWorld: when to plan first, where decisions live, and what to check before or after engine/plugin work.

**Upgrade track:** [Docs/22_UE58_UPGRADE.md](../../Docs/22_UE58_UPGRADE.md). Historical 5.7 entry: [UE57_TECH.md](UE57_TECH.md).

## When to use this doc

- **Policy:** For any Unreal Engine API, UI, plugin, or documentation, use **only UE 5.8–specific sources** (Epic 5.8 docs, this doc, docs/UE/UE58_EDITOR_UI.md when present, KNOWN_ERRORS). Do not rely on training data or other engine versions. See [.cursor/rules/ue58-sources.mdc](../../.cursor/rules/ue58-sources.mdc).
- Starting **UE 5.8 API, plugin, or engine-related work** (C++, Blueprint, PCG, Python Editor scripts).
- Before adding or changing code that touches **FindObject**, **FPaths**, image utils, collision profiles, PCG graph, or Python Unreal APIs (e.g. `get_actor_bounds`, AnimBP factory).
- After an **engine or plugin upgrade** to know what to re-verify.
- Planning **multi-system UE work** (e.g. Mass migration, PCG graph v2) — propose the plan in the agent chat (see [SPEC_AND_PLAN.md](../SPEC_AND_PLAN.md)).

## Key links

| Topic | Where |
|-------|--------|
| C++ conventions and UE API pitfalls | [.cursor/rules/unreal-cpp.mdc](../../.cursor/rules/unreal-cpp.mdc) |
| Recorded errors and fixes | [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) |
| PCG settings automation cannot set | [PCG/PCG_VARIABLES_NO_ACCESS.md](../PCG/PCG_VARIABLES_NO_ACCESS.md) |
| C++ vs Blueprint, code-first checklist | [CONVENTIONS.md](../CONVENTIONS.md) |
| Plugins, layers, stack | [VisionBoard/Core/STACK_PLAN.md](../../VisionBoard/Core/STACK_PLAN.md) |
| Plan before code (complex work) | [SPEC_AND_PLAN.md](../SPEC_AND_PLAN.md), [.cursor/rules/17-plan-first.mdc](../../.cursor/rules/17-plan-first.mdc) |
| Automation “no access” procedure | [.cursor/rules/automation-standards.mdc](../../.cursor/rules/automation-standards.mdc) |
| Editor UI (menus, panels, options) | [UE58_EDITOR_UI.md](UE58_EDITOR_UI.md) (stub → Epic 5.8); legacy [UE57_EDITOR_UI.md](UE57_EDITOR_UI.md) |
| Full automation stack | [FULL_AUTOMATION_RESEARCH.md](../Automation/FULL_AUTOMATION_RESEARCH.md) |
| Host env | `UE_ENGINE` / `UE_EDITOR` → `C:\Program Files\Epic Games\UE_5.8\...` — [DEV_ENV_MATRIX.md](../Setup/DEV_ENV_MATRIX.md) |

## Canonical examples

- **C++ pawn and basics:** [Source/HomeWorld/HomeWorldCharacter.h](../../Source/HomeWorld/HomeWorldCharacter.h), `HomeWorldCharacter.cpp`
- **GAS:** [HomeWorldGameplayAbility.h](../../Source/HomeWorld/HomeWorldGameplayAbility.h), [HomeWorldAttributeSet.h](../../Source/HomeWorld/HomeWorldAttributeSet.h)
- **Python Editor:** [Content/Python/level_loader.py](../../Content/Python/level_loader.py)
- **Python PCG:** [Content/Python/create_pcg_forest.py](../../Content/Python/create_pcg_forest.py)

## Plugins and 5.8 status

| Plugin | 5.8 status |
|--------|------------|
| PCG, GameplayAbilities, EnhancedInput, SteamSockets, DaySequence | In use; rebuild verified under Docs/22 U58-C. |
| PythonScriptPlugin, PCGPythonInterop, PythonAutomationTest | In use; re-check Python signatures after upgrade. |
| UnrealMCP | Local plugin (gitignored); rebuild with Safe-Build; 5.7 patches still apply — verify on open. |
| **MassEntity** | **Removed from uproject** — stub gone in Launcher 5.8 (was deprecated/engine-moved). See KNOWN_ERRORS. |
| MassGameplay, MassAI, StateTree, ZoneGraph, SmartObjects | Enabled; MassEntity no longer listed. |
| ModelingToolsEditorMode | Enabled. |

## Docs/23 — 5.8 capabilities we use / reject

Track: [Docs/23_UE58_FEATURE_ADOPTION.md](../../Docs/23_UE58_FEATURE_ADOPTION.md).

| Capability | HomeWorld decision |
|------------|-------------------|
| PCG + `PCGBiomeCore` / `PCGPrimitives` | **Enabled** — nondestructive edit on graph **duplicates** only |
| Procedural Vegetation Editor | **Enabled** — stylized pine only; AD gate ([U58F_C_PVE_PINE.md](../../Docs/handoffs/U58F_C_PVE_PINE.md)) |
| MegaLights | **On** — `r.MegaLights.EnableForProject=True` in DefaultEngine.ini |
| Fog Screen Space Scattering | **On** — `r.Fog.ScreenSpaceScattering=1`; enable on height fog actors |
| Lumen Lite | **Low path** — Medium GI + Medium Reflections (`sg.GlobalIlluminationQuality 1`, `sg.ReflectionQuality 1`); hero stays High/Epic |
| UnrealMCP | **Primary** — Epic `ModelContextProtocol` stays **disabled** ([U58F_F_MCP_DECISION.md](../../Docs/handoffs/U58F_F_MCP_DECISION.md)) |
| Mesh Terrain | **Spike only** — sandbox; do not replace VS_MVP Landscape ([U58F_G_MESH_TERRAIN.md](../../Docs/handoffs/U58F_G_MESH_TERRAIN.md)) |
| MetaHuman / MH Crowds | **Reject** for hero/family |
| Mobile tooling | **Reject** (PC + Steam EA lock) |
| Mover / MassCrowd / Chaos Cloth | **Defer** |

### Lumen Lite (Steam EA min-spec)

```text
; Runtime / settings UI — Medium GI + Reflections
sg.GlobalIlluminationQuality 1
sg.ReflectionQuality 1
```

Hero lookdev cameras: keep `sg.GlobalIlluminationQuality` at 2 (High) or 3 (Epic). See [Config/DefaultScalability.ini](../../Config/DefaultScalability.ini).

## U58 cutover checklist (completed / re-run)

1. `EngineAssociation` → `"5.8"` in `HomeWorld.uproject`
2. Tools/CI defaults → `UE_5.8`; runner label `ue58`
3. Safe-Build green on DESKTOP-21CT3H0
4. Re-run automation access checks (PCG / MCP / Python)
5. VS_MVP content + PIE smoke
6. Docs/rules → `ue58-sources` + this file

## Plan first for UE work

For **multi-file or multi-system** UE work, follow [17-plan-first.mdc](../../.cursor/rules/17-plan-first.mdc).

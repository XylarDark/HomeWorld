---
last_mapped_commit: 94158e9416cc44954f4fdb11e0de696e31836276
last_mapped_at: 2026-09-28
---
﻿# Technology Stack

**Analysis Date:** 2026-09-28

## Languages

**Primary:**
- C++ (UE 5.8 / UnrealBuildTool) — all gameplay systems under `Source/HomeWorld/`
- Unreal Blueprints — content/data only (meshes, materials, level placement, GA_* asset shells reparented to C++)

**Secondary:**
- Python 3 (Editor `Content/Python/`) — bootstrap, PCG, PIE helpers, automation tests
- Node.js ≥20 — root harness scripts (`package.json`, `scripts/*.js`)
- PowerShell / batch — `Build-HomeWorld.bat`, `Tools/*.ps1`, Windows bridge

## Runtime

**Environment:**
- Unreal Engine **5.8** only (`HomeWorld.uproject` → `EngineAssociation: "5.8"`)
- Editor + packaged Win64 client (PC + Steam Early Access lock per `AGENTS.md`)
- Node.js ≥20 for doctor / preflight / evidence scripts

**Package Manager:**
- npm (root `package.json`; no app lockfile required beyond DET submodule)
- UE modules via `Source/HomeWorld/HomeWorld.Build.cs` / `HomeWorldEditor.Build.cs`

## Frameworks

**Core:**
- Unreal Engine 5.8 — game client, World Partition / open world
- Gameplay Ability System (GAS) — `UHomeWorldGameplayAbility`, `UHomeWorldAttributeSet`, ASC on character
- Enhanced Input — `IA_Move` / `IA_Look` / `IMC_Default` via bootstrap
- PCG + PCGPythonInterop — procedural forest / planetoid kit
- Mass Entity + Mass AI, StateTree, ZoneGraph, SmartObjects — Week-2 family stack (enabled in `.uproject`)
- UMG / Slate — HUD, menus, customize widgets

**Testing:**
- Node `node --test` — `scripts/preflight-ue.test.js`, `scripts/evidence-grep.test.js`
- UE Python automation — `Content/Python/tests/*.py`
- Optional UE automation via `Tools/RunTests.ps1` (CI)

**Build/Dev:**
- UnrealBuildTool / `Build-HomeWorld.bat` / `Tools/RunFullBuild.ps1`
- GitHub Actions self-hosted Win64 UE 5.8 runner (`.github/workflows/ci.yml`)
- Docs-only path: `.github/workflows/validate.yml`

## Key Dependencies

**Critical (Build.cs PublicDependencyModuleNames):**
- `EnhancedInput`, `GameplayAbilities`, `GameplayTags`, `GameplayTasks`
- `SmartObjectsModule`, `AIModule`, `UMG`, `HTTP`, `Json`

**Enabled plugins (`.uproject`):**
- `PCG`, `GameplayAbilities`, `EnhancedInput`, `SteamSockets`, `DaySequence`
- `PythonScriptPlugin`, `PCGPythonInterop`, `UnrealMCP`, `PythonAutomationTest`
- `MassGameplay`, `MassAI`, `StateTree`, `ZoneGraph`

**Infrastructure / harness:**
- `UserHarness/` (DevHarness gitlink) — doctor / sync layers
- `Plugins/UnrealMCP/` — gitignored external MCP plugin (Editor live tools)

## Configuration

**Environment:**
- `Config/` UE ini defaults
- `Config/preflight-ue.json`, `Config/userharness-pin.json`
- Secrets: `.env*` gitignored; `.cursor/mcp.json` gitignored (use `.example`)

**Build:**
- `HomeWorld.uproject`, `Source/**/*.Build.cs`, `global.json` (bundled .NET pin)

## Platform Requirements

**Development:**
- Windows DESKTOP with UE 5.8 (Conductor parent / DESKTOP-21CT3H0 for Shell/MCP/PIE)
- Cloud Linux agents: docs/C++/CI only — no MCP/PIE (`swarm/CLOUD_AGENT_PACKET.md`)

**Production:**
- PC + Steam Early Access; engine 5.8 lock — no engine/platform variants without Lead decision

---
*Stack analysis: 2026-09-28*
*Update after major dependency or engine changes*

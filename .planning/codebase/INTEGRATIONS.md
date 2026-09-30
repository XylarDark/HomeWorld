---
last_mapped_commit: 94158e9416cc44954f4fdb11e0de696e31836276
last_mapped_at: 2026-09-28
---
﻿# Integrations

**Analysis Date:** 2026-09-28

## External Systems

**Unreal Editor MCP (`UnrealMCP` plugin):**
- Live Editor manipulation when Editor + MCP connected
- Setup: `docs/Setup/MCP_SETUP.md`, `.cursor/rules/09-mcp-workflow.mdc`
- Plugin path `Plugins/UnrealMCP/` is gitignored (installed via tools)

**Steam:**
- `SteamSockets` plugin enabled in `HomeWorld.uproject`
- Early Access / PC platform lock (product constraint, not implemented here as GSD phase)

**HTTP / JSON:**
- `HTTP`, `Json`, `JsonUtilities` in `HomeWorld.Build.cs`
- Used by subsystems such as leaderboard / session / NFT stubs (`HomeWorldLeaderboardSubsystem`, `HomeWorldNFTSubsystem`, `HomeWorldSessionSubsystem`) — treat as optional remote surfaces; do not invent new SaaS in GSD host phases

**DevHarness / UserHarness:**
- Vendored gitlink `UserHarness/` pinned via `config/userharness-pin.json`
- npm scripts: `doctor`, `sync`, `sync:apply`

**GitHub Actions:**
- `.github/workflows/ci.yml` — Win64 build on self-hosted `ue58` runner when `Source/**` changes
- `.github/workflows/validate.yml` — docs/policy path

**Blender / AssetCreation:**
- `blender/`, `AssetCreation/`, `Lib/` — kit export into UE Content (swarm art pipeline)
- Canon vs engineering docs split: `Docs/` (capital) vs `docs/` (lowercase)

## Auth / Secrets

- No first-party auth product in MVP slice
- Local secrets via `.env` / MCP config — never commit (see `.gitignore`)

## Webhooks / Callbacks

- None required for GSD host scaffolding
- Night encounter / day-night driven in-process via `UHomeWorldTimeOfDaySubsystem` + `AHomeWorldGameMode`

## Data Stores

- `UHomeWorldSaveGame` / `UHomeWorldSaveGameSubsystem` — local save
- Inventory / craft / wallet / spirit roster — in-memory + save subsystems under `Source/HomeWorld/`

---
*Integrations analysis: 2026-09-28*

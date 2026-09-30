---
last_mapped_commit: 94158e9416cc44954f4fdb11e0de696e31836276
last_mapped_at: 2026-09-28
---
﻿# Architecture

**Analysis Date:** 2026-09-28

## Pattern Overview

**Overall:** Monolithic Unreal game client (C++ module + content) with a separate Conductor/swarm ops harness and DevHarness tooling — not a service mesh.

**Key Characteristics:**
- Single Win64 client; C++ is the single writer of gameplay behavior
- Blueprint assigns content/assets only (`docs/CONVENTIONS.md`)
- Swarm (Conductor / Design / Implement / Test / Fix) coordinates product Acts via `swarm/PHASE_BOARD.md`
- GSD `.planning/` is **host scaffolding** — does not own Co product phase graph

## Layers

**Gameplay runtime (`Source/HomeWorld/`):**
- Purpose: Characters, GAS abilities, gather/craft/build, spirits, day/night, save, UI widgets
- Contains: `AHomeWorldCharacter`, `AHomeWorldGameMode`, subsystems, components, abilities
- Depends on: UE Engine, Enhanced Input, GAS, SmartObjects, UMG
- Used by: Maps under `Maps/`, Blueprints under `Content/`

**Editor automation (`Source/HomeWorldEditor/`, `Content/Python/`):**
- Purpose: Commandlets (PCG setup, MEC), bootstrap, material/PCG scripts, PIE helpers
- Depends on: Editor modules + Python plugin
- Used by: DESKTOP Conductor parent for evidence / kit dress

**Harness / ops (repo root + `swarm/` + `DevEnvTemplate/`):**
- Purpose: Doctor, preflight, evidence greps, CI, swarm PHASE_BOARD
- Does not implement gameplay; gates and routes work

**Canon docs:**
- `Docs/` — signed MVP product canon (GDD, art, audit WAVEs)
- `docs/` — UE 5.8 engineering (setup, automation, known errors)
- Do not merge trees (`Docs/README.md`)

## Data Flow

**PIE / play session:**
1. Editor or packaged client loads map (`Maps/VS_MVP`, preview maps)
2. `AHomeWorldGameMode` sets `DefaultPawnClass = AHomeWorldCharacter`
3. Enhanced Input drives move/look; GAS abilities handle interact/place/heal/spirit verbs
4. Subsystems (inventory, craft, time-of-day, spirit roster, save) hold session state
5. Day/night + night encounters tick via GameMode + `UHomeWorldTimeOfDaySubsystem`
6. Fallback glide / shrine portal: `UHomeWorldFallbackGlideComponent`, `UHomeWorldShrinePortal*`

**Swarm Act flow (product — Co-owned):**
1. Lead names bite or PHASE_BOARD row opens
2. Conductor assigns seat; Implement/Test/Fix post evidence
3. Lead `APPROVE` / `SIGN OFF` — agents never invent approval

**State Management:**
- Game: UObject subsystems + SaveGame
- Swarm: `swarm/PHASE_BOARD.md`, `docs/SESSION_SUMMARY.md`, `Docs/handoffs/`

## Key Abstractions

**Character + GAS:**
- `AHomeWorldCharacter` owns ASC + `UHomeWorldAttributeSet`
- Abilities subclass `UHomeWorldGameplayAbility` (e.g. `UHomeWorldInteractAbility`, place/heal/spirit*)

**World verbs:**
- Gather/craft/build: yield nodes, craft station/subsystem, build order / place ability
- Spirits: roster, assignment, stealth, heal, lit volumes, wisps
- Transit: soft bounds, fallback glide, shrine portals

**Family / life (Mass-adjacent):**
- `UHomeWorldFamilySubsystem`, nurture, meal triggers, beast tame — Mass/StateTree plugins enabled for Week-2 agents

## Entry Points

**Runtime:**
- Module: `Source/HomeWorld/HomeWorld.cpp`
- Default classes: `AHomeWorldGameMode`, `AHomeWorldCharacter`

**Editor:**
- `Source/HomeWorldEditor/` commandlets
- `Content/Python/bootstrap_project.py` and related scripts

**Agent/Conductor:**
- `START_HERE.md`, `HOMEWORLD_MASTER_PROMPT.md`, `swarm/PHASE_BOARD.md`, `AGENTS.md`

## Error Handling

- Feature debug instrumentation + log-driven validation (`.cursor/rules/16-feature-debug-instrumentation.mdc`)
- `docs/KNOWN_ERRORS.md`, `docs/Automation/AUTOMATION_GAPS.md`
- `npm run preflight:ue` / `evidence:grep` before polish unlocks (HS-D)

---
*Architecture analysis: 2026-09-28*

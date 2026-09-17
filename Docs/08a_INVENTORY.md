# Docs/08a_INVENTORY.md — WAVE A Inventory

| Field | Value |
|-------|-------|
| **Board status** | WAVE A — INVENTORY COMPLETE (awaiting Lead gate) |
| **Date** | 2026-09-16 (ET) |
| **Author** | Conductor / audit executor (HomeWorld) |
| **Parent plan** | [08_AUDIT_UPGRADE_STRATEGY.md](08_AUDIT_UPGRADE_STRATEGY.md) |
| **Scope** | Classify pre-swarm / parallel harness vs new `Docs/` swarm path |
| **Hard rules honored** | Docs/07 CLOSED not reopened; FALLBACK FLIGHT stays armed; no C++ edits; no deletes |

**Gate:** stop for Lead **`APPROVE WAVE A`**

---

## Disposition legend

| Tag | Meaning |
|-----|---------|
| **KEEP** | Canonical or still required as-is; do not duplicate elsewhere |
| **UPGRADE** | Keep path; align to swarm canon / harness / Docs/04–05 in later WAVEs |
| **QUARANTINE** | Do not extend; freeze references; resolve in WAVE D/F before delete |
| **DELETE** | Candidate for WAVE F removal after Lead SIGN OFF AUDIT (no deletes in WAVE A) |

Owner tracks (when known): **CND** Conductor · **UE** Unreal/automation · **INT** Integration · **AD** Art Director · **ENV** Env kits · **Lead** Human Lead

---

## Summary table

| Area | Disposition | One-line why | Owner track |
|------|-------------|--------------|-------------|
| `Docs/` (capital) | **KEEP** | MVP swarm canon (P0–P7 CLOSED + audit strategy) | CND / Lead |
| `Docs/handoffs/`, `Docs/qa/` | **KEEP** | Durable evidence for signed slice | CND / QA |
| `Docs/08*` | **KEEP** | Audit WAVE plan + this inventory | CND / Lead |
| `swarm/` | **KEEP** | Conductor runtime; PHASE_BOARD CLOSED slice + FALLBACK armed | CND |
| `START_HERE.md`, `HOMEWORLD_MVP_SWARM_BRIEF.md`, `HOMEWORLD_MASTER_PROMPT.md` | **KEEP** | Swarm entry + Lead-owned game brief | Lead / CND |
| `Lib/` | **KEEP** | Kit specs + 10 master materials JSON (slice library) | AD / ENV / TA |
| `Maps/Preview_*`, `Maps/VS_MVP/` | **KEEP** | Signed lookdev stills + camera reel (not UE `/Game` maps) | AD / INT |
| `blender/` | **KEEP** | Homestead LIB blend for kit continuity | ENV-H / BLENDER |
| `AssetCreation/Exports/` MVP FBX + manifest + crumb JSON | **KEEP** | Docs/04–05 import staging | INT / ENV |
| `AssetCreation/Blender/export_to_asset_creation.py` | **UPGRADE** | Align categories/paths with Docs/04 mesh roots | INT |
| `AssetCreation/STYLE_GUIDE.md`, `README.md` | **UPGRADE** | Still cite pre-swarm style/workflow; point at Docs/02 + Docs/04 | AD / INT |
| `AssetCreation/AI_Sources/`, `RefImages/` | **KEEP** | Empty placeholders for pipeline inputs | AD |
| `refs/keyart_homestead_night.jpg` | **KEEP** | Key-art north star for night look | AD / Lead |
| `Source/HomeWorld/` (core character, GM, input, interact, TOD, inventory) | **UPGRADE** | Boot + MVP verbs substrate; align to Docs/03 / FALLBACK glide | UE / GP |
| `Source/HomeWorld/` (NFT, Milady, Leaderboard, Wallet, Family/Mass-heavy) | **QUARANTINE** | Off signed 8-verb slice; defer polish systems (WAVE E) | UE |
| `Source/HomeWorldEditor/` commandlets | **UPGRADE** | Keep for PCG/MEC tooling; verify UE 5.7.x boot (WAVE C) | UE |
| `Content/HomeWorld/` (structure) | **UPGRADE** | Product content root; Meshes/* per Docs/04; old Demo/Homestead layout TBD WAVE D | INT / UE |
| `Content/StylizedProvencal/`, `Content/Man/` | **QUARANTINE** | Third-party / sample look packs; not swarm kit canon | UE / AD |
| `Content/Python/batch_import_asset_creation.py` | **KEEP** | Docs/05 first-pass importer (Meshes categories) | INT |
| `Content/Python/` place_*/create_bp_*/PCG/Mass/automation suite | **UPGRADE** / **QUARANTINE** | Useful harness scripts vs obsolete map builders — split in WAVE D/E | UE |
| `Content/Python/gui_automation/` | **QUARANTINE** | Pre-swarm GUI click paths; prefer MCP; freeze until WAVE B/F | UE |
| `Tools/Safe-Build.ps1`, `Common-Automation.ps1`, `Check-AutomationPrereqs.ps1` | **KEEP** | Canonical autonomous build protocol | UE |
| `Build-HomeWorld.bat` | **KEEP** | Low-level engine Build.bat wrapper (called by Safe-Build) | UE |
| `Tools/RunAutomationLoop.ps1`, `Start-AllAgents*.ps1`, `Watch-*.ps1`, agent runners | **QUARANTINE** | Old agent-company loop; conflicts with `swarm/` Conductor model | UE / CND |
| `Start-AllAgents.bat`, `Run-DemoMapScript.bat`, `Run-PCGForestScript.bat` | **QUARANTINE** | Entrypoints into obsolete automation/demo maps | UE |
| `Package-HomeWorld.bat`, `Open-HomeWorld-In-VS.bat`, DotNet env bats | **KEEP** | Packaging / IDE helpers still useful | UE |
| `Setup-MCP.bat` | **UPGRADE** | Still needed; align paths with current MCP docs (WAVE B) | UE |
| `docs/` (lowercase) UE/session/automation tree | **KEEP** | Intentional split from `Docs/`; no merge | UE |
| `docs/MVP/`, `docs/Maps/DEMO_MAP.md`, `docs/Maps/HOMESTEAD_MAP.md` | **QUARANTINE** | Pre-swarm MVP/map truth vs `Docs/` + root `Maps/` | UE / CND |
| `docs/TaskLists/`, `docs/workflow/`, `docs/SESSION_LOG.md`, `DAILY_STATE.md` | **UPGRADE** | Session ops stay; stop treating 30-day lists as game canon | UE / Lead |
| `docs/Automation/AGENT_COMPANY.md` + automation loop docs | **QUARANTINE** | Parallel harness vs `swarm/SWARM_OPS.md` | UE / CND |
| `docs/PCG/`, `docs/Editor/`, `docs/Setup/`, `docs/UE/`, `KNOWN_ERRORS.md` | **KEEP** / **UPGRADE** | UE engineering truth; upgrade where they fight Docs/04 paths | UE |
| `VisionBoard/Core/`, `VisionBoard/Prompts/` | **KEEP** | Long-horizon vision (theme, stack) — not day-to-day MVP canon | Lead / DES |
| `VisionBoard/MVP/*` (gap lists, VERTICAL_SLICE_SIGNOFF, 30-day) | **QUARANTINE** | Duplicate / stale vs Docs/01–07 signed slice | CND / Lead |
| `VisionBoard/Planetoid/`, `Character/` | **QUARANTINE** | Broader design than 8-verb slice; defer | DES |
| `DevEnvTemplate/` (git submodule, currently empty checkout) | **UPGRADE** | Companion harness — init/pin + gap vs AGENTS/Safe-Build (WAVE B) | UE / CND |
| `package.json` doctor/sync scripts | **UPGRADE** | Depend on populated `DevEnvTemplate/dist` | UE |
| `AGENTS.md`, `.cursor/`, `.agents/` | **UPGRADE** | Still cite VisionBoard/TaskLists as primary; add Docs/swarm pointers | CND / UE |
| `Config/` | **KEEP** | Project defaults; touch only for boot health (WAVE C) | UE |
| `HomeWorld.uproject` | **KEEP** | Plugin set for UE 5.7; no audit churn | UE |
| `.github/workflows/` | **KEEP** | CI/validate | UE |
| `README-Automation.md` (root) | **QUARANTINE** | Documents old loop; supersede via docs + swarm pointers | UE |
| `README.md`, `CONTRIBUTING.md`, `LICENSE` | **KEEP** / **UPGRADE** | README should surface Docs/ + START_HERE | Lead |
| `SylizedProvencal.png` (root) | **QUARANTINE** | Loose ref image; prefer `refs/` | AD |
| `Plugins/` | — | Absent in-tree (plugins via `.uproject`) | — |

---

## Detailed sections

### 1. Capital `Docs/` — KEEP (canon)

Signed MVP operating system: `00_CANON` → `07_VERTICAL_SLICE_SIGN OFF` (CLOSED), handoffs, QA, and `08_AUDIT_UPGRADE_STRATEGY`.

| Item | Disposition | Why |
|------|-------------|-----|
| `00`–`07`, handoffs, qa | **KEEP** | Closed slice evidence; do not reopen as unfinished |
| `08_AUDIT_UPGRADE_STRATEGY.md` | **KEEP** | WAVE A–F plan |
| `08a_INVENTORY.md` (this file) | **KEEP** | WAVE A deliverable |
| `README.md` | **KEEP** | Docs vs docs split policy |

**Conflict call-out:** Any other tree claiming “vertical slice signed” or alternate GDD is subordinate to `Docs/`.

---

### 2. `swarm/` — KEEP

| Item | Disposition | Why |
|------|-------------|-----|
| `PHASE_BOARD.md` | **KEEP** | P0–P7 CLOSED; FALLBACK FLIGHT = YES |
| `SWARM_OPS.md`, role cards, packets, templates | **KEEP** | Conductor model for lookdev / audit WAVEs |
| `.cursor/agents/` copies | **KEEP** | Runtime mirrors of `swarm/agents/` |

**Conflict:** `docs/Automation/AGENT_COMPANY.md` + `Tools/Start-AllAgents*` describe a different “agent company” (Developer/Fixer/Guardian loop). Treat swarm Conductor as product-direction OPS; quarantine the parallel loop from driving game canon.

---

### 3. Lowercase `docs/` — KEEP tree, QUARANTINE conflicting truth

Intentional UE/session/automation docs (`DOCS_LAYOUT.md` already documents the split).

| Subtree | Disposition | Why |
|---------|-------------|-----|
| `Setup/`, `Editor/`, `UE/`, `PCG/`, `Testing/`, `Assets/`, `human-use/`, `KNOWN_ERRORS.md`, `SESSION_LOG.md` | **KEEP** / **UPGRADE** | Engineering + Human Use; upgrade path refs to Docs/04–05 where needed |
| `Maps/DEMO_MAP.md`, `Maps/HOMESTEAD_MAP.md` | **QUARANTINE** | Pre-swarm UE map guides vs root `Maps/Preview_*` + Docs/04 dress path |
| `MVP/*` | **QUARANTINE** | Vision/gap docs that predate Docs/01–07 |
| `Automation/*` agent-company + loop-until-done | **QUARANTINE** | Dual harness with `swarm/` |
| `TaskLists/*`, `workflow/` | **UPGRADE** | Keep as session task board; stop using as GDD |

---

### 4. `Source/` — UPGRADE core / QUARANTINE off-slice

~97 C++/header units. No deletions in WAVE A.

**UPGRADE (slice-adjacent substrate):** Character, GameMode, PlayerController/State, Enhanced Input stack, Interact/Heal (and related GAS bases), TimeOfDay, Inventory, SaveGame, GoToBed/Meal triggers (boot-health class — WAVE C), Yield/Resource, Spiritual collectible/artefact stubs, NightEncounter placeholder, Build placement (if still used for homestead verbs).

**QUARANTINE (defer WAVE E polish):** NFT, Milady import, Leaderboard, Wallet, Family/Spirit roster/assignment heavy paths, ProtectorAttack combat emphasis, DungeonEntrance sprawl beyond slice, SmartObject/Mass-oriented controller wiring that is not required for the signed 8 verbs + FALLBACK glide.

**Editor module:** Keep commandlets; verify compile/boot under UE 5.7.x in WAVE C.

---

### 5. `Content/` (structure only) — UPGRADE product / QUARANTINE samples

| Path | Disposition | Why |
|------|-------------|-----|
| `Content/HomeWorld/` (Input, GameMode, Abilities, Building, Characters, UI, PCG, Maps, AI, Mass, Milady, …) | **UPGRADE** | Live product content; WAVE D decides homestead/PCG/Mass vs Docs/04 `/Game/HomeWorld/Meshes/...` |
| `Content/HomeWorld/Meshes/` (expected post Docs/05) | **KEEP** target | Canonical import destination per Docs/04 |
| `Content/Python/batch_import_asset_creation.py` | **KEEP** | First-pass importer already Docs/04-aware |
| `Content/Python/` demo/homestead/planetoid assemblers, Mass spawners, GA creators | **UPGRADE** or **QUARANTINE** | Split: keep PIE/test helpers; quarantine map-builders that fight Preview_* / VS_MVP |
| `Content/Python/gui_automation/` | **QUARANTINE** | Fragile UI automation; MCP-first policy |
| `Content/StylizedProvencal/`, `Content/Man/` | **QUARANTINE** | Sample/third-party packs — not Lib kit |
| `__ExternalActors__` / `__ExternalObjects__` | **KEEP** | UE World Partition bookkeeping |

---

### 6. `Tools/` + root build bats — KEEP Safe-Build stack / QUARANTINE agent loop

| Item | Disposition | Why |
|------|-------------|-----|
| `Tools/Safe-Build.ps1` | **KEEP** | Autonomous build; closes Editor first |
| `Build-HomeWorld.bat` | **KEEP** | Underlying engine build; **not** a rival to Safe-Build — Safe-Build *calls* it |
| `Tools/Common-Automation.ps1`, `Check-AutomationPrereqs.ps1`, `CleanProject.ps1`, `RunTests.ps1`, `RunFullBuild.ps1` | **KEEP** / **UPGRADE** | Shared automation primitives |
| `Tools/RunAutomationLoop.ps1`, `Watch-AutomationAndFix.ps1`, `Run-*-Agent.ps1`, `Start-AllAgents*.ps1`, `Guard-AutomationLoop.ps1`, Horde JSON | **QUARANTINE** | Pre-swarm parallel harness; WAVE F candidates after Lead sign-off |
| `Package-HomeWorld.bat`, VS/DotNet helper bats | **KEEP** | Ship/IDE |
| `Start-AllAgents.bat`, `Run-DemoMapScript.bat`, `Run-PCGForestScript.bat` | **QUARANTINE** | Entrypoints into quarantined loops/maps |
| `Setup-MCP.bat` | **UPGRADE** | Align with `docs/Setup/MCP_SETUP.md` in WAVE B |

**Conflict call-out (Safe-Build vs Build-HomeWorld.bat):** Not mutually exclusive. Policy: agents use **Safe-Build**; humans may call `Build-HomeWorld.bat` directly. Do not delete either in WAVE A.

---

### 7. `AssetCreation/`, `blender/`, `Lib/`, `Maps/`, `refs/` — KEEP swarm art pipeline

| Item | Disposition | Why |
|------|-------------|-----|
| MVP FBX under Exports Homestead/Forest/Gatherables/Transit | **KEEP** | Signed kit exports |
| `MVP_EXPORT_MANIFEST.md`, `MVP_CRUMB_SPLINE.json` | **KEEP** | Import + FALLBACK glide data |
| Khronos/placeholder GLBs in legacy categories | **QUARANTINE** | Pre-swarm placeholders |
| `blender/floating_island_homestead_LIB.blend` | **KEEP** | Authoring source |
| `Lib/00`–`08` | **KEEP** | Kit + NightMix masters |
| `Maps/Preview_*` stills + `Maps/VS_MVP` | **KEEP** | P6/P7 evidence |
| `AssetCreation` STYLE/README | **UPGRADE** | Rewrite pointers from old STYLE_GUIDE tone to Docs/02 + Docs/04 |

---

### 8. `VisionBoard/` — KEEP core vision / QUARANTINE MVP duplicates

| Item | Disposition | Why |
|------|-------------|-----|
| `Core/VISION.md`, `STACK_PLAN.md`, `PROTOTYPE_SCOPE.md` | **KEEP** | Long-term creative/stack north star |
| `Prompts/` | **KEEP** | Ideation prompts |
| `MVP/VERTICAL_SLICE_SIGNOFF.md`, gap/30-day/checklist docs | **QUARANTINE** | **Duplicate GDD/sign-off** vs `Docs/07` (2026-09-16 CLOSED) |
| `Planetoid/`, `Character/` deep designs | **QUARANTINE** | Beyond 8-verb slice |

---

### 9. `DevEnvTemplate/`, `package.json`, `AGENTS.md` — UPGRADE (WAVE B inputs)

| Item | Disposition | Why |
|------|-------------|-----|
| `DevEnvTemplate/` submodule (empty on this clone) | **UPGRADE** | Must init/update; doctor/sync currently broken without `dist/` |
| `package.json` doctor/sync | **UPGRADE** | WAVE B harness align |
| `AGENTS.md` | **UPGRADE** | Still leads with VisionBoard + TaskLists; should privilege `Docs/` + `START_HERE` for MVP truth |
| `.agents/skills*` | **KEEP** / **UPGRADE** | Template agent-context layer |

---

### 10. `Config/`, project meta — KEEP

`Default*.ini`, `HomeWorld.uproject`, `.github/`, `LICENSE`, `CONTRIBUTING.md`, `global.json`, editorconfig — **KEEP**. Touch Config only for WAVE C boot health.

---

## Conflicts with swarm `Docs/` (explicit)

1. **Duplicate vertical-slice sign-off:** `VisionBoard/MVP/VERTICAL_SLICE_SIGNOFF.md` (2026-03 task-list era) vs **`Docs/07` CLOSED 2026-09-16** — swarm wins.
2. **Duplicate / competing GDD & gap truth:** `VisionBoard/MVP/*`, `docs/MVP/*`, old TaskLists vs **`Docs/00`–`03`**.
3. **Two map canons:** `docs/Maps/DEMO_MAP.md` + `HOMESTEAD_MAP.md` + `Content/Python/ensure_*_map.py` vs root **`Maps/Preview_*` / `Maps/VS_MVP`** + Docs/04 UE dress.
4. **Two agent operating systems:** `docs/Automation/AGENT_COMPANY.md` + `Tools/RunAutomationLoop.ps1` vs **`swarm/SWARM_OPS.md`** + Conductor.
5. **Style / export docs drift:** `AssetCreation/STYLE_GUIDE.md` (Mario Galaxy–like) vs **`Docs/02_ART_BIBLE` / `Docs/00_CANON`** tone and ten masters.
6. **Build entry confusion:** docs/agents sometimes say “use Build-HomeWorld.bat” without Safe-Build — clarify in WAVE B (both stay; Safe-Build preferred for autonomy).
7. **AGENTS.md / README gravity:** Point newcomers at TaskLists/VisionBoard MVP instead of **`START_HERE` + `Docs/`**.
8. **Obsolete Python:** GUI automation + DemoMap/PCG-forest one-shots vs **`batch_import_asset_creation.py`** + Docs/05.
9. **Empty `DevEnvTemplate/`:** package doctor/sync assume populated submodule — WAVE B.
10. **FALLBACK FLIGHT:** Armed on PHASE_BOARD / Docs/07 — any free-flight / full-sim docs or code paths are **QUARANTINE**, not reopen.

---

## Recommended next — WAVE B inputs

Per [08_AUDIT_UPGRADE_STRATEGY.md](08_AUDIT_UPGRADE_STRATEGY.md) WAVE B (Harness align):

1. **Init/pin `DevEnvTemplate` submodule** and record SHA; make `npm run doctor` runnable or document accepted skip.
2. **Diff AGENTS.md, Safe-Build, MCP setup, SESSION_LOG, swarm ops** vs current template; produce `Docs/08b_HARNESS_GAP.md`.
3. **Doc pointer PRs (no gameplay):** README / AGENTS lead with `START_HERE` + `Docs/`; mark VisionBoard/MVP + Automation agent-company as historical/quarantine.
4. **Clarify build policy in one place:** Safe-Build → Build-HomeWorld.bat relationship.
5. **Do not start WAVE C/D** until Lead **`APPROVE WAVE A`** (and later B).

Parallel (not a WAVE): Docs/05 UE first-pass import may continue when editor boots.

---

## Gate

```
STOP — Lead approval required
Type: APPROVE WAVE A
```

On approval, Conductor opens WAVE B (`Docs/08b_HARNESS_GAP.md`). Until then: no archive deletes, no dual-canon gameplay rewrites, Docs/07 remains CLOSED, FALLBACK FLIGHT remains armed.

# Docs directory structure

**Purpose:** Single source of truth for where documentation lives. All new docs must be placed in the appropriate subdirectory per this layout. Do not add new top-level files under `docs/` unless this layout is updated first.

**Policy:** When generating documentation or any content under `docs/`, follow this structure so everything stays organized. See `.cursor/rules/19-docs-directory-structure.mdc`.

**Actionable docs:** For docs that outline what to do next or have step-by-step instructions (setup, maps, PCG, manual Editor steps, automation readiness, pre-demo verification), make them easy to follow: add a short "What you'll do" or "When to use this" at the top, use numbered steps or clear section headings, and link to the next doc in the flow. Vision and ideas docs (e.g. VisionBoard) do not need a tutorial style.

---

## Repo roots outside `docs/` (MVP swarm vs UE)

These paths are **intentionally outside** lowercase `docs/`. Do not merge `Docs/` into `docs/` or move swarm kit files into UE subdirs without updating this table.

| Path | Purpose |
|------|---------|
| **`Docs/`** (capital D) | MVP swarm canon — GDD slices, art bible, material sheet, WAVE handoffs (`Docs/handoffs/`), QA placeholders. See [Docs/README.md](../Docs/README.md). |
| **`swarm/`** | Conductor runtime — [SWARM_OPS.md](../swarm/SWARM_OPS.md), [PHASE_BOARD.md](../swarm/PHASE_BOARD.md), wave packets, role cards (source for `.cursor/agents/`). |
| **`Lib/`** | Kit specs and master-material JSON for Blender-first pipeline (homestead, gatherables, night layer, transit). |
| **`Maps/`** (repo root) | Preview map READMEs for swarm lookdev (`Preview_Homestead_Night`, etc.) — not UE `/Game/` maps under `Content/`. |
| **`START_HERE.md`** | Human Lead entry for MVP lookdev swarm; gates and on-demand specialist spawn. |
| **`HOMEWORLD_MVP_SWARM_BRIEF.md`** | Game canon brief for the swarm (Human Lead owns changes after P0). |

**UE project docs** stay in **`docs/`** (this tree). **MVP swarm docs** stay in **`Docs/`**. On case-insensitive filesystems, Git may only expose one casing locally — see [Docs/README.md](../Docs/README.md).

---

## Root (docs/) — entry points and single-source-of-truth only

| File | Purpose |
|------|--------|
| [README.md](README.md) | Documentation index; links to VisionBoard, TaskLists, workflow, and subdirs. |
| [DOCS_LAYOUT.md](DOCS_LAYOUT.md) | This file — canonical directory structure and placement rules. |
| [CONVENTIONS.md](CONVENTIONS.md) | Code and project conventions (C++ vs Blueprint, naming). |
| [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md) | Content paths (`/Game/HomeWorld/`), script index, Python/config paths. |
| [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md) | `hw.*` commands; pre-demo verification entry point. |
| [KNOWN_ERRORS.md](KNOWN_ERRORS.md) | Recorded errors and fixes; check before similar work. |
| [SETUP.md](SETUP.md) | Developer onboarding; install, build, MCP, first run. |
| [SPEC_AND_PLAN.md](SPEC_AND_PLAN.md) | Plan-first discipline; when to save plans to `.cursor/plans/`. |
| [SESSION_LOG.md](SESSION_LOG.md) | Full session history (large); append at end for legacy UE track. |
| [SESSION_SUMMARY.md](SESSION_SUMMARY.md) | Rolling last-30-days summary; **default read at start** for swarm/Conductor. |

---

## Setup/

Setup and environment: MCP, CI, local tools, ref images, Cursor dev.

| File | Purpose |
|------|--------|
| [Setup/MCP_SETUP.md](Setup/MCP_SETUP.md) | MCP bridge install and troubleshooting. |
| [Setup/DEV_ENV_MATRIX.md](Setup/DEV_ENV_MATRIX.md) | Pinned toolchain, env vars, C++/Python/Cursor/MCP checklist. |
| [Setup/CI_SETUP.md](Setup/CI_SETUP.md) | CI (GitHub Actions) configuration. |
| [Setup/HORDE_LOCAL_SETUP.md](Setup/HORDE_LOCAL_SETUP.md) | Horde local setup (if used). |
| [Setup/REF_IMAGES_SETUP_TUTORIAL.md](Setup/REF_IMAGES_SETUP_TUTORIAL.md) | Reference images for GUI automation. |
| [Setup/CURSOR_DEV.md](Setup/CURSOR_DEV.md) | Cursor and dev environment; DevEnvTemplate init runbook. |
| [Setup/DOCTOR_POLICY.md](Setup/DOCTOR_POLICY.md) | DevEnvTemplate doctor accepted declines for UE game host (HR-B2). |
| [Setup/CI_POLICY.md](Setup/CI_POLICY.md) | When validate.yml vs ci.yml; docs-only PRs; `[skip ci]`. |
| [Setup/WINDOWS_BRIDGE.md](Setup/WINDOWS_BRIDGE.md) | Cloud agent → self-hosted CI → DESKTOP Editor/MCP. |
| [Setup/BUILD_POLICY.md](Setup/BUILD_POLICY.md) | Safe-Build vs Build-HomeWorld.bat for agents vs humans. |
| [Setup/UE_PREFLIGHT.md](Setup/UE_PREFLIGHT.md) | UE preflight (`preflight:ue`) — fail loud before PIE; cloud vs DESKTOP modes (HR3-B). |

### guides/

Template MCP hygiene and plan-integration (layer sync). HomeWorld MCP install stays in Setup/.

| File | Purpose |
|------|--------|
| [guides/mcp-hygiene.md](guides/mcp-hygiene.md) | Treat `.cursor/mcp.json` as a production change. |
| [guides/cursor-plan-integration.md](guides/cursor-plan-integration.md) | Plan mode with Human Use ownership. |
| [guides/automation-harness.md](guides/automation-harness.md) | Portable prove/capture harness (DevHarness PR #33; host UE policy in `.cursor/rules/automation-standards.mdc`). |

### operational/

Template operational-memory entry shapes (layer sync). HomeWorld canonical automation gaps stay under Automation/.

| File | Purpose |
|------|--------|
| [operational/automation-gaps.md](operational/automation-gaps.md) | Pointer to [Automation/AUTOMATION_GAPS.md](Automation/AUTOMATION_GAPS.md). |

### human-use/

Human jobs: steer, taste, test (DevEnvTemplate operational layer). Agents name the
job and stop when a decision you own is missing. Applies anywhere in the tree.

| File | Purpose |
|------|--------|
| [human-use/README.md](human-use/README.md) | Index for ownership docs. |
| [human-use/OWNERSHIP.md](human-use/OWNERSHIP.md) | Who owns the next step; alert shape. |
| [human-use/SWARM_MODE_ROUTING.md](human-use/SWARM_MODE_ROUTING.md) | Detect SWARM / NON-SWARM / HYBRID at task start (token efficiency). |
| [human-use/CYCLE.md](human-use/CYCLE.md) | When a decision is due for this task. |
| [human-use/outcome.md](human-use/outcome.md) | Gradeable rubric; verifier scores, not the implementer. |
| [human-use/cursor-cannot/](human-use/cursor-cannot/README.md) | Week 1 PDF slices Cursor does not enforce. |

---

## PCG/

Procedural Content Generation: setup, quick path, best practices, no-access variables.

| File | Purpose |
|------|--------|
| [PCG/PCG_SETUP.md](PCG/PCG_SETUP.md) | Full PCG setup; script + manual steps. |
| [PCG/PCG_QUICK_SETUP.md](PCG/PCG_QUICK_SETUP.md) | One-page tutorial-aligned flow. |
| [PCG/PCG_BEST_PRACTICES.md](PCG/PCG_BEST_PRACTICES.md) | Best practices; check before changing graphs. |
| [PCG/PCG_VARIABLES_NO_ACCESS.md](PCG/PCG_VARIABLES_NO_ACCESS.md) | Variables automation cannot set; manual steps. |
| [PCG/PCG_TUTORIAL_ALIGNMENT.md](PCG/PCG_TUTORIAL_ALIGNMENT.md) | Alignment with Epic PCG tutorials. |
| [PCG/PCG_ELEGANT_SOLUTIONS.md](PCG/PCG_ELEGANT_SOLUTIONS.md) | Research-backed approaches; one-time graph. |

---

## Maps/

Level and map guides: DemoMap, Homestead.

| File | Purpose |
|------|--------|
| [Maps/DEMO_MAP.md](Maps/DEMO_MAP.md) | Primary demo map; create_demo_from_scratch. |
| [Maps/HOMESTEAD_MAP.md](Maps/HOMESTEAD_MAP.md) | Homestead map; legacy/campaign. |

---

## Automation/

Agent company, automation loop, gaps, refinement, logs, research.

| File | Purpose |
|------|--------|
| [Automation/AGENT_COMPANY.md](Automation/AGENT_COMPANY.md) | Developer, Fixer, Guardian, Refiner, Gap-Solver roles. |
| [Automation/AUTOMATION_GAPS.md](Automation/AUTOMATION_GAPS.md) | Logged gaps; steps automation cannot do. |
| [Automation/AUTOMATION_LOOP_UNTIL_DONE.md](Automation/AUTOMATION_LOOP_UNTIL_DONE.md) | Loop until 30 days done; thresholds. |
| [Automation/AUTOMATION_REFINEMENT.md](Automation/AUTOMATION_REFINEMENT.md) | Refine rules from run history. |
| [Automation/AUTOMATION_EDITOR_LOG.md](Automation/AUTOMATION_EDITOR_LOG.md) | Editor Output Log capture for Fixer/Guardian. |
| [Automation/AUTOMATION_COST_TRACKING.md](Automation/AUTOMATION_COST_TRACKING.md) | Cost/token tracking. |
| [Automation/AUTOMATION_UPDATE_OVERVIEW.md](Automation/AUTOMATION_UPDATE_OVERVIEW.md) | What automation accomplished; tools used. |
| [Automation/AUTOMATION_READINESS.md](Automation/AUTOMATION_READINESS.md) | Prerequisites; what's ready to run. |
| [Automation/AUTOMATION_CAPABILITIES_VERIFICATION.md](Automation/AUTOMATION_CAPABILITIES_VERIFICATION.md) | Verification of automation capabilities. |
| [Automation/FULL_AUTOMATION_RESEARCH.md](Automation/FULL_AUTOMATION_RESEARCH.md) | Full automation stack; tool catalog. |
| [Automation/CAPTURE_REDUNDANCY.md](Automation/CAPTURE_REDUNDANCY.md) | **Universal** tooling redundancy + practice (Lead-gated): docs-first, proven-results, dead-end research, rung ladder; shotlist/PA-E instance; ImageGrab ban. |
| [Automation/ONE_SHOT_BITES.md](Automation/ONE_SHOT_BITES.md) | **Design schema:** slice UE/env/capture scope into Conductor one-shots (bot-company Design→Implement→Test→Fix); inherits evidence protocol from CAPTURE_REDUNDANCY. |
| [Automation/SWARM_ROUTING_RESEARCH.md](Automation/SWARM_ROUTING_RESEARCH.md) | Studio + model research for SWARM/NON-SWARM mode and ModelClass routing. |
| [Automation/GUI_AUTOMATION_WHY_AND_WHEN.md](Automation/GUI_AUTOMATION_WHY_AND_WHEN.md) | When to use GUI automation vs manual. |
| [Automation/ALTERNATIVE_AUTOMATION_OPTIONS.md](Automation/ALTERNATIVE_AUTOMATION_OPTIONS.md) | Alternative automation approaches. |
| [Automation/GAP_SOLUTIONS_RESEARCH.md](Automation/GAP_SOLUTIONS_RESEARCH.md) | Research for closing automation gaps. |
| [Automation/EXTERNAL_AI_AUTOMATION.md](Automation/EXTERNAL_AI_AUTOMATION.md) | Using external LLMs for Editor scripts. |

---

## Editor/

Editor launch, build protocol, polish, manual steps.

| File | Purpose |
|------|--------|
| [Editor/EDITOR_BUILD_PROTOCOL.md](Editor/EDITOR_BUILD_PROTOCOL.md) | Safe build; when to close Editor. |
| [Editor/EDITOR_LAUNCH_DEEP_DIVE.md](Editor/EDITOR_LAUNCH_DEEP_DIVE.md) | Debug Editor launch failures. |
| [Editor/EDITOR_POLISH_TUTORIAL.md](Editor/EDITOR_POLISH_TUTORIAL.md) | Get to polished MVP in Editor. |
| [Editor/MANUAL_EDITOR_TUTORIAL.md](Editor/MANUAL_EDITOR_TUTORIAL.md) | Manual steps when tools cannot do it. |

---

## UE/

Unreal Engine 5.7 tech and Editor UI.

| File | Purpose |
|------|--------|
| [UE/UE57_TECH.md](UE/UE57_TECH.md) | UE 5.7 tech entry point; API pitfalls. |
| [UE/UE57_EDITOR_UI.md](UE/UE57_EDITOR_UI.md) | Editor UI reference. |

---

## Assets/

Asset pipeline, image-to-3D, Milady.

| File | Purpose |
|------|--------|
| [Assets/ASSET_WORKFLOW_AND_STEAM_DEMO.md](Assets/ASSET_WORKFLOW_AND_STEAM_DEMO.md) | Asset workflow; image-to-3D; Steam demo. |
| [Assets/EXTERNAL_ASSET_MANIFEST.md](Assets/EXTERNAL_ASSET_MANIFEST.md) | Free-tier source ladder, bundle inventory, MVP vs automation tracks, cast checklist. |
| [Assets/MILADY_IMPORT_SETUP.md](Assets/MILADY_IMPORT_SETUP.md) | Milady import pipeline setup. |

---

## Testing/

Testing plans and validation.

| File | Purpose |
|------|--------|
| [Testing/LEVEL_TESTING_PLAN.md](Testing/LEVEL_TESTING_PLAN.md) | Level loading and test strategy. |
| [Testing/MVP_PIE_AND_TUTORIAL_VERIFICATION.md](Testing/MVP_PIE_AND_TUTORIAL_VERIFICATION.md) | After asset/PCG changes: batch import, PCG lock, pie_test_runner, tutorial console checklist. |
| [Testing/MOVEMENT_INPUT_VALIDATION.md](Testing/MOVEMENT_INPUT_VALIDATION.md) | Movement input validation. |

---

## MVP/

MVP scope, gap analysis, and feasibility.

| File | Purpose |
|------|--------|
| [MVP/MVP_GAP_ANALYSIS_VISION.md](MVP/MVP_GAP_ANALYSIS_VISION.md) | Vision vs implemented; gaps to solid MVP. |
| [MVP/MOBILE_FEASIBILITY.md](MVP/MOBILE_FEASIBILITY.md) | Mobile platform feasibility. |

---

## IndustryStandards/

Industry-standard approaches for MVP (world, character, monsters).

| File | Purpose |
|------|--------|
| [IndustryStandards/INDUSTRY_STANDARDS_FOR_MVP_WORLD_AND_CHARACTERS.md](IndustryStandards/INDUSTRY_STANDARDS_FOR_MVP_WORLD_AND_CHARACTERS.md) | Game world, 2D→character, characters/monsters. |

---

## TaskLists/

Task generation, current list, schedule, daily state, accomplishments. **TaskSpecs/** = per-task specs (DAY3_, AGENTIC_BUILDING, etc.). Do not move; already structured.

---

## workflow/

Workflow index; daily flow. Do not move; already structured.

---

## Redundancy and single source of truth

- **PCG:** Use [PCG/PCG_SETUP.md](PCG/PCG_SETUP.md) as the full reference; [PCG/PCG_QUICK_SETUP.md](PCG/PCG_QUICK_SETUP.md) for the short path. Both link to each other.
- **Automation:** [Automation/AUTOMATION_GAPS.md](Automation/AUTOMATION_GAPS.md) is the single place to log gaps; other automation docs link to it.
- **Setup:** [SETUP.md](SETUP.md) is the main onboarding entry; Setup/ holds detailed subs (MCP, CI, etc.).
- **Errors:** [KNOWN_ERRORS.md](KNOWN_ERRORS.md) is the single place for recorded errors; check before similar work.

When adding a new doc, place it in the subdirectory above that matches its topic. If the topic is new, add a new subdirectory and update this file and docs/README.md.

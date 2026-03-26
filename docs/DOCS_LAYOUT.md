# Docs directory structure

**Purpose:** Single source of truth for where documentation lives. All new docs must be placed in the appropriate subdirectory per this layout. Do not add new top-level files under `docs/` unless this layout is updated first.

**Policy:** When generating documentation or any content under `docs/`, follow this structure so everything stays organized. See `.cursor/rules/19-docs-directory-structure.mdc`.

**Actionable docs:** For docs that outline what to do next or have step-by-step instructions (setup, maps, PCG, manual Editor steps, automation readiness, pre-demo verification), make them easy to follow: add a short "What you'll do" or "When to use this" at the top, use numbered steps or clear section headings, and link to the next doc in the flow. Vision and ideas docs (e.g. VisionBoard) do not need a tutorial style.

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
| [SESSION_LOG.md](SESSION_LOG.md) | Session summaries; read at start, append at end. |

---

## Setup/

Setup and environment: MCP, CI, local tools, ref images, Cursor dev.

| File | Purpose |
|------|--------|
| [Setup/MCP_SETUP.md](Setup/MCP_SETUP.md) | MCP bridge install and troubleshooting. |
| [Setup/CI_SETUP.md](Setup/CI_SETUP.md) | CI (GitHub Actions) configuration. |
| [Setup/HORDE_LOCAL_SETUP.md](Setup/HORDE_LOCAL_SETUP.md) | Horde local setup (if used). |
| [Setup/REF_IMAGES_SETUP_TUTORIAL.md](Setup/REF_IMAGES_SETUP_TUTORIAL.md) | Reference images for GUI automation. |
| [Setup/CURSOR_DEV.md](Setup/CURSOR_DEV.md) | Cursor and dev environment. |

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
| [Assets/MILADY_IMPORT_SETUP.md](Assets/MILADY_IMPORT_SETUP.md) | Milady import pipeline setup. |

---

## Testing/

Testing plans and validation.

| File | Purpose |
|------|--------|
| [Testing/LEVEL_TESTING_PLAN.md](Testing/LEVEL_TESTING_PLAN.md) | Level loading and test strategy. |
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

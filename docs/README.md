# HomeWorld – Documentation

Setup, conventions, content layout, automation, and operational guides live here. **Vision and task-list content** are in dedicated directories.

**New here?**  
1. **Get running** — Follow [SETUP.md](SETUP.md) to install the engine, open the project, and set up the MCP bridge.  
2. **See what to work on** — Open [workflow/README.md](workflow/README.md) and [workflow/30_DAY_SCHEDULE.md](workflow/30_DAY_SCHEDULE.md) (or [TaskLists/CURRENT_TASK_LIST.md](TaskLists/CURRENT_TASK_LIST.md)).  
3. **Find a guide** — Use the table below to jump to setup, PCG, maps, automation, or Editor steps.

**Directory structure:** All docs are organized into subdirectories. **Canonical layout:** [DOCS_LAYOUT.md](DOCS_LAYOUT.md). When adding or generating docs, place them in the correct subdirectory per DOCS_LAYOUT. See `.cursor/rules/19-docs-directory-structure.mdc`.

---

## Layout

| Location | Contents |
|----------|----------|
| **[VisionBoard/](../VisionBoard/)** | **MVP and vision:** Theme (VISION.md), campaign, moral system, scope, planetoid design, STACK_PLAN, MVP and tutorial plans, vertical slice, character generation. Plus vision-board prompt files (Aesthetics, Gameplay Mechanics, World Lore, etc.). |
| **[TaskLists/](TaskLists/)** | **Task generation and lists:** Current task list (T1–T10), how to generate lists, 30-day schedule, daily state, accomplishments, project state. **TaskSpecs/** = per-task specs (DAY3_, DAY7_, AGENTIC_BUILDING, CONVERSION_NOT_KILL, etc.). |
| **[workflow/](workflow/)** | **Workflow index** — entry point; points to VisionBoard and TaskLists. Daily flow, automation loop, key links. |
| **docs/ root** | Entry points only: README, DOCS_LAYOUT, CONVENTIONS, CONTENT_LAYOUT, CONSOLE_COMMANDS, KNOWN_ERRORS, SETUP, SPEC_AND_PLAN, SESSION_LOG. |
| **[Setup/](Setup/)** | MCP, CI, Horde, ref images, Cursor dev. |
| **[PCG/](PCG/)** | PCG setup, quick setup, best practices, variables no access. |
| **[Maps/](Maps/)** | DemoMap, Homestead. |
| **[Automation/](Automation/)** | Agent company, automation gaps, loop, refinement, research. |
| **[Editor/](Editor/)** | Build protocol, launch deep dive, polish, manual tutorial. |
| **[UE/](UE/)** | UE 5.7 tech, Editor UI. |
| **[Assets/](Assets/)** | Asset workflow, Milady import. |
| **[Testing/](Testing/)** | Level testing, movement validation. |
| **[MVP/](MVP/)** | MVP gap analysis, mobile feasibility. |
| **[IndustryStandards/](IndustryStandards/)** | Industry-standard approaches for MVP (world, character, monsters). |

---

## Entry points

- **Directory structure (where to put new docs):** [DOCS_LAYOUT.md](DOCS_LAYOUT.md)
- **Workflow and daily state:** [workflow/README.md](workflow/README.md)
- **Vision and scope:** [VisionBoard/Core/VISION.md](../VisionBoard/Core/VISION.md), [VisionBoard/Core/STACK_PLAN.md](../VisionBoard/Core/STACK_PLAN.md)
- **Current tasks:** [TaskLists/PROJECT_STATE_AND_TASK_LIST.md](TaskLists/PROJECT_STATE_AND_TASK_LIST.md), [TaskLists/CURRENT_TASK_LIST.md](TaskLists/CURRENT_TASK_LIST.md)
- **Setup:** [SETUP.md](SETUP.md)
- **Content paths:** [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md)
- **Pre-demo verification:** [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md) §3
- **PCG:** [PCG/PCG_SETUP.md](PCG/PCG_SETUP.md), [PCG/PCG_QUICK_SETUP.md](PCG/PCG_QUICK_SETUP.md)
- **Automation gaps:** [Automation/AUTOMATION_GAPS.md](Automation/AUTOMATION_GAPS.md)
- **Known errors:** [KNOWN_ERRORS.md](KNOWN_ERRORS.md)

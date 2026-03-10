# HomeWorld – Workflow index

This folder is the **entry point** for project workflow. Vision, MVP, and task-list content have been reorganized:

---

## Documentation layout

| Location | Contents |
|----------|----------|
| **[VisionBoard/](../../VisionBoard/)** | **MVP and vision:** Theme, campaign, moral system, scope. VISION.md, PROTOTYPE_SCOPE, MVP_* and tutorial plan, vertical slice, planetoid design/biomes, STACK_PLAN, CHARACTER_GENERATION_AND_CUSTOMIZATION, assets/Steam phased approach, Steam checklist. Plus vision-board prompt files (Aesthetics, Gameplay Mechanics, World Lore, etc.). See [VisionBoard/README.md](../../VisionBoard/README.md). |
| **[docs/TaskLists/](../TaskLists/)** | **Task generation and lists:** Current task list (T1–T10), how to generate lists, 30-day schedule, daily state, accomplishments, project state, cycle/agent task list. **TaskSpecs/** holds the per-task specs (DAY3_, DAY7_, CONVERSION_NOT_KILL, AGENTIC_BUILDING, etc.). See [TaskLists/README.md](../TaskLists/README.md). |
| **docs/** | Setup, conventions, content layout, PCG, automation, known errors, console commands, and other operational docs. |

---

## Daily flow (yesterday / today / tomorrow)

**Start a day:** Ask e.g. "What did we do yesterday and what do we need to do today?" The agent reads [TaskLists/DAILY_STATE.md](../TaskLists/DAILY_STATE.md) (and [SESSION_LOG.md](../SESSION_LOG.md)) and answers from **Yesterday** and **Today**.

**End a session:** The agent updates [TaskLists/DAILY_STATE.md](../TaskLists/DAILY_STATE.md) and appends [SESSION_LOG.md](../SESSION_LOG.md). See `.cursor/rules/07-ai-agent-behavior.mdc`.

---

## Automation loop

**Active driver:** [TaskLists/CURRENT_TASK_LIST.md](../TaskLists/CURRENT_TASK_LIST.md) (10 tasks T1–T10). Run `.\Tools\Start-AllAgents-InNewWindow.ps1` to start the loop. Generate new lists per [TaskLists/HOW_TO_GENERATE_TASK_LIST.md](../TaskLists/HOW_TO_GENERATE_TASK_LIST.md).

---

## Key links

- **Vision and scope:** [VisionBoard/Core/VISION.md](../../VisionBoard/Core/VISION.md), [VisionBoard/Core/STACK_PLAN.md](../../VisionBoard/Core/STACK_PLAN.md)
- **Project state and task list:** [TaskLists/PROJECT_STATE_AND_TASK_LIST.md](../TaskLists/PROJECT_STATE_AND_TASK_LIST.md)
- **Pre-demo verification:** [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) §3 and [VisionBoard/VERTICAL_SLICE_CHECKLIST.md](../../VisionBoard/VERTICAL_SLICE_CHECKLIST.md)
- **Setup and conventions:** [SETUP.md](../SETUP.md), [CONVENTIONS.md](../CONVENTIONS.md), [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md), [KNOWN_ERRORS.md](../KNOWN_ERRORS.md)

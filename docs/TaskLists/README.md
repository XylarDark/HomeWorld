# HomeWorld – Task lists and task specs

This directory holds **task generation and list workflow** and the **per-task specification docs**.

---

## Task list and generation

| Document | Purpose |
|----------|---------|
| [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md) | **Active 10-task list** (T1–T10). Run `.\Tools\Start-AllAgents-InNewWindow.ps1` to execute. |
| [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md) | How to generate the next task list; task list composition by phase. |
| [CURRENT_TASK_LIST_TEMPLATE.md](CURRENT_TASK_LIST_TEMPLATE.md) | Template for new task lists. |
| [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md) | Day-by-day schedule (Act 1 → Homestead → Family → Planetoid → Spirits → Dungeon → buffer). |
| [30_DAY_IMPLEMENTATION_STATUS.md](30_DAY_IMPLEMENTATION_STATUS.md) | Which days are implementation-complete vs pending/blocked. |
| [DAILY_STATE.md](DAILY_STATE.md) | **Yesterday** (last session), **Today** (this day's tasks), **Tomorrow** (preview). Read at session start; updated at session end. |
| [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) | Project overview and task list — work done, work not yet completed (T1–T10). |
| [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md) | Master high-level record of all work accomplished. |
| [AGENT_TASK_LIST.md](AGENT_TASK_LIST.md) | Agent task list (vision-aligned); agents fetch first pending task. |
| [CYCLE_TASKLIST.md](CYCLE_TASKLIST.md), [CYCLE_STATE.md](CYCLE_STATE.md) | Legacy cycle reference (superseded by CURRENT_TASK_LIST and RunAutomationLoop). |
| [TASK_LIST_REPEATS_LOG.md](TASK_LIST_REPEATS_LOG.md) | Log of task list repeats. |
| [AUTOMATION_DEBUG_TASK_LIST.md](AUTOMATION_DEBUG_TASK_LIST.md) | Debug task list for automation. |
| [NEXT_SESSION_PROMPT.md](NEXT_SESSION_PROMPT.md) | Prompt for the next session (written by automation). |
| [30DAY_TO_10TASK_MAPPING.json](30DAY_TO_10TASK_MAPPING.json) | Mapping from 30-day schedule to 10-task list. |

---

## Task specs (TaskSpecs/)

The **TaskSpecs/** subfolder holds the **per-task specification docs**: day tasks (DAY3_, DAY4_, …), role tasks (DAY12_ROLE_PROTECTOR, DAY13_ROLE_HEALER, …), and feature specs (AGENTIC_BUILDING, CONVERSION_NOT_KILL, NIGHT_ENCOUNTER, PLANETOID_*, SIN_VIRTUE_SPECTRUM, etc.). These are the detailed docs that implement or scope vision sections.

**Vision → task docs:** See [workflow/README.md](../workflow/README.md) for the map from [VisionBoard/Core/VISION.md](../../VisionBoard/Core/VISION.md) sections to TaskSpecs.

---

## References

- **Vision and MVP:** [VisionBoard/](../../VisionBoard/) — VISION.md, PROTOTYPE_SCOPE, MVP_TUTORIAL_PLAN, VERTICAL_SLICE_CHECKLIST, planetoid design, STACK_PLAN.
- **Workflow index:** [workflow/README.md](../workflow/README.md)
- **Setup and conventions:** [SETUP.md](../SETUP.md), [KNOWN_ERRORS.md](../KNOWN_ERRORS.md)

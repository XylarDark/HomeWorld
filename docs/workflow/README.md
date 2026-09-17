# HomeWorld – Workflow index

This folder is the **entry point** for project workflow. Vision, MVP, and task-list content have been reorganized:

---

## Documentation layout

| Location | Contents |
|----------|----------|
| **[VisionBoard/](../../VisionBoard/)** | **MVP and vision:** Theme, campaign, moral system, scope. VISION.md, PROTOTYPE_SCOPE, MVP_* and tutorial plan, vertical slice, planetoid design/biomes, STACK_PLAN, CHARACTER_GENERATION_AND_CUSTOMIZATION, assets/Steam phased approach, Steam checklist. Plus vision-board prompt files (Aesthetics, Gameplay Mechanics, World Lore, etc.). See [VisionBoard/README.md](../../VisionBoard/README.md). |
| **[docs/TaskLists/](../TaskLists/)** | **Task generation and lists (quarantine / history):** 30-day schedule, daily state, accomplishments, project state. Pre-swarm agent loop **removed WAVE F**. See [TaskLists/README.md](../TaskLists/README.md). |
| **docs/** | Setup, conventions, content layout, PCG, automation, known errors, console commands, and other operational docs. |

---

## Active driver (post-audit)

**MVP lookdev swarm:** [swarm/SWARM_OPS.md](../../swarm/SWARM_OPS.md) + **Conductor** — [START_HERE.md](../../START_HERE.md). Live status: [swarm/PHASE_BOARD.md](../../swarm/PHASE_BOARD.md). Harness refine track: [Docs/11_SWARM_HARNESS_REFINE.md](../../Docs/11_SWARM_HARNESS_REFINE.md).

**Quarantine (do not start):** Pre-swarm agent-company loop — [docs/Automation/AGENT_COMPANY.md](../Automation/AGENT_COMPANY.md). Deleted WAVE F: `Start-AllAgents*`, `run_automation_cycle.py`, agent-loop Tools.

---

## Daily flow (yesterday / today / tomorrow)

**Swarm / Conductor sessions:** Read [docs/SESSION_SUMMARY.md](../SESSION_SUMMARY.md) and [swarm/PHASE_BOARD.md](../../swarm/PHASE_BOARD.md) at start; append SESSION_SUMMARY at end. Full [SESSION_LOG.md](../SESSION_LOG.md) only when investigating a specific past incident.

**Legacy task-list sessions:** Ask e.g. "What did we do yesterday and what do we need to do today?" — agent reads [TaskLists/DAILY_STATE.md](../TaskLists/DAILY_STATE.md) (quarantine/history). End of session: append SESSION_LOG if still using that track.

---

## Key links

- **Vision and scope:** [VisionBoard/Core/VISION.md](../../VisionBoard/Core/VISION.md), [VisionBoard/Core/STACK_PLAN.md](../../VisionBoard/Core/STACK_PLAN.md)
- **Swarm ops:** [swarm/SWARM_OPS.md](../../swarm/SWARM_OPS.md), [START_HERE.md](../../START_HERE.md)
- **Setup and conventions:** [SETUP.md](../SETUP.md), [CONVENTIONS.md](../CONVENTIONS.md), [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md), [KNOWN_ERRORS.md](../KNOWN_ERRORS.md)

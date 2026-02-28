# HomeWorld – Workflow

This folder is the **single place for project ideas and daily workflow**: consolidated vision, scope lock, and a 30-day schedule. Use it to know what to build and what "today" is.

---

## Daily flow (yesterday / today / tomorrow)

**Start a day:** Prompt the chat with e.g. "What did we do yesterday and what do we need to do today?" The agent reads [DAILY_STATE.md](DAILY_STATE.md) (and [SESSION_LOG.md](../SESSION_LOG.md)) and answers from **Yesterday** and **Today**.

**End a session:** The agent automatically (1) appends to [SESSION_LOG.md](../SESSION_LOG.md) and (2) updates [DAILY_STATE.md](DAILY_STATE.md): **Yesterday** = what was done this session; **Today** = next day's tasks; **Tomorrow** = preview of the day after; **Current day** = next day number. So the next time you start, "yesterday" and "today" are already correct.

**Stored and executed automatically:** No manual copy-paste. The agent reads DAILY_STATE at task start and updates it at task end (see `.cursor/rules/07-ai-agent-behavior.mdc`).

---

## Contents

| Document | Purpose |
|----------|---------|
| [DAILY_STATE.md](DAILY_STATE.md) | **Yesterday** (last session), **Today** (this day's tasks), **Tomorrow** (preview). Read at session start; updated at session end. |
| [VISION.md](VISION.md) | Theme, campaign summary, moral system (Seven Sins/Virtues), death/succession, tech summary, scope lock. |
| [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md) | Day-by-day schedule (Act 1 → Homestead → Family → Planetoid → Spirits → Dungeon → buffer). Check off items as you complete them. |

**Current day:** In [DAILY_STATE.md](DAILY_STATE.md) see **Current day** and **Today**. Or open [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md) and find the first **Day N** that still has unchecked items.

---

## Pre–Day 1 checklist (Phase 0 gate)

Complete before committing to Day 1 (or before Week 1 if using phase language):

- [ ] **Vision/Theme** approved
- [ ] **Pillars** locked
- [ ] **Campaign** flow good (mission count agreed)
- [ ] **Tech** feasible / budget (~$0–150)
- [ ] **Roadmap:** commit to the 30-day schedule
- [ ] **Next:** Art mocks + prototype vision (vision is in [VISION.md](VISION.md); mocks are art-side)

---

## Current status (task index)

| # | Task | Doc | Status |
|---|------|-----|--------|
| 1 | Fix character animation | [CHARACTER_ANIMATION.md](../tasks/CHARACTER_ANIMATION.md) | Completed |
| 2 | Fix character orientation | [CHARACTER_ORIENTATION.md](../tasks/CHARACTER_ORIENTATION.md) | Completed |
| 3 | Character on ground | [CHARACTER_GROUND.md](../tasks/CHARACTER_GROUND.md) | Completed |
| 4 | PCG forest on map | [PCG_FOREST_ON_MAP.md](../tasks/PCG_FOREST_ON_MAP.md) | In progress – manual graph + Generate; see [PCG_SETUP.md](../PCG_SETUP.md) |
| 5 | Family agents (Mass + State Tree) | [FAMILY_AGENTS_MASS_STATETREE.md](../tasks/FAMILY_AGENTS_MASS_STATETREE.md) | Not started |
| 6 | Agentic building (Mass + Smart Objects) | [AGENTIC_BUILDING.md](../tasks/AGENTIC_BUILDING.md) | Not started |
| 7 | Milady Character Import pipeline | [MILADY_IMPORT_ROADMAP.md](../tasks/MILADY_IMPORT_ROADMAP.md) | In progress – manual steps in roadmap |
| 8 | Homestead + planetoid + family + spirits + dungeon | 30-day schedule Days 6–25 | Not started |

Details and manual steps live in **docs/tasks/**; setup and references in [SETUP.md](../SETUP.md), [PCG_SETUP.md](../PCG_SETUP.md), [KNOWN_ERRORS.md](../KNOWN_ERRORS.md).

---

## References

- **Setup and conventions:** [SETUP.md](../SETUP.md), [CONVENTIONS.md](../CONVENTIONS.md), [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md), [MCP_SETUP.md](../MCP_SETUP.md)
- **Full tech stack:** [STACK_PLAN.md](../STACK_PLAN.md)
- **Planetoid design:** [PLANETOID_DESIGN.md](../PLANETOID_DESIGN.md)
- **Known errors and fixes:** [KNOWN_ERRORS.md](../KNOWN_ERRORS.md)

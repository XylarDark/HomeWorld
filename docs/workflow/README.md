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
| [30_DAY_IMPLEMENTATION_STATUS.md](30_DAY_IMPLEMENTATION_STATUS.md) | Which days are implementation-complete (done) vs pending/blocked. Used by the automation loop. |
| [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) | **Project overview and task list** — summary of work done, work not yet completed (T1–T10), and quick reference. Use this for "what to work on next." |
| [MVP_AND_ROADMAP_STRATEGY.md](MVP_AND_ROADMAP_STRATEGY.md) | How we balance MVP execution (validate loop fast) with long-term readiness (ship on same stack); what to implement for MVP; MVP-first vs release alignment. |

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
| 4 | PCG forest on map | [PCG_FOREST_ON_MAP.md](../tasks/PCG_FOREST_ON_MAP.md) | Completed – DemoMap + PCG; see [PCG_SETUP.md](../PCG_SETUP.md) |
| 4b | GAS 3 survivor skills | [GAS_SURVIVOR_SKILLS.md](../tasks/GAS_SURVIVOR_SKILLS.md) | Completed – run setup_gas_abilities.py; Day 2 |
| 4c | Day 3: Placement + playtest | [DAY3_PLACEMENT_AND_PLAYTEST.md](../tasks/DAY3_PLACEMENT_AND_PLAYTEST.md) | Completed – placement API verified; Week 1 playtest checklist in doc |
| 4d | Day 4: Polish + optional Milady | [DAY4_POLISH_AND_OPTIONAL_MILADY.md](../tasks/DAY4_POLISH_AND_OPTIONAL_MILADY.md) | Completed – polish checklist in doc; Milady scripts run via MCP |
| 4e | Day 5: Playtest sign-off | [DAY5_PLAYTEST_SIGNOFF.md](../tasks/DAY5_PLAYTEST_SIGNOFF.md) | Complete – four-beat playtest doc; Act 1 gate passed; Day 6 clear |
| 4f | Day 6 [1.1]: DemoMap layout | [DAY6_HOMESTEAD_LAYOUT.md](../tasks/DAY6_HOMESTEAD_LAYOUT.md) | Completed – bounds via create_demo_from_scratch.py + config; manual PCG per doc |
| 4g | Day 7 [1.2]: Resource nodes (trees) | [DAY7_RESOURCE_NODES.md](../tasks/DAY7_RESOURCE_NODES.md) | Ready – create BP_HarvestableTree (manual), run place_resource_nodes.py or place manually |
| 4h | Day 8 [1.3]: Resource collection loop | [DAY8_RESOURCE_COLLECTION.md](../tasks/DAY8_RESOURCE_COLLECTION.md) | Completed – C++ ability + reparent, PIE harvest validated |
| 4i | Day 9 [1.4]: Home asset placement | [DAY9_HOME_PLACEMENT.md](../tasks/DAY9_HOME_PLACEMENT.md) | Not started |
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

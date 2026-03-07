# HomeWorld – Workflow

This folder is the **single place for project ideas and daily workflow**: consolidated vision, scope lock, and a 30-day schedule. Use it to know what to build and what "today" is.

---

## Automation loop (current)

**Active driver:** [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md) (10 tasks T1–T10). Run `.\Tools\Start-AllAgents-InNewWindow.ps1` to start the loop. Generate new lists per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md). **Legacy (reference only):** [CYCLE_TASKLIST.md](CYCLE_TASKLIST.md), [CYCLE_STATE.md](CYCLE_STATE.md) — superseded by CURRENT_TASK_LIST and RunAutomationLoop.

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
| [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md) | **Master high-level record** of all work accomplished. Use with task list and vision to inform what work to do next and when generating the next task list. |
| [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md) | Day-by-day schedule (Act 1 → Homestead → Family → Planetoid → Spirits → Dungeon → buffer). Check off items as you complete them. |
| [30_DAY_IMPLEMENTATION_STATUS.md](30_DAY_IMPLEMENTATION_STATUS.md) | Which days are implementation-complete (done) vs pending/blocked. Used by the automation loop. |
| [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) | **Project overview and task list** — summary of work done, work not yet completed (T1–T10), and quick reference. Use this for "what to work on next." |
| [MVP_AND_ROADMAP_STRATEGY.md](MVP_AND_ROADMAP_STRATEGY.md) | How we balance MVP execution (validate loop fast) with long-term readiness (ship on same stack); what to implement for MVP; MVP-first vs release alignment. |
| [EDITOR_POLISH_TUTORIAL.md](../EDITOR_POLISH_TUTORIAL.md) | **Editor polish** — Step-by-step tutorial to get the slice to a polished MVP state: pre-demo verification, one-time manual steps (portal, State Tree Defend), and lighting/LOD/placement/animation/UX. Use when automation runs are complete and you are ready for in-Editor work. |

**Current day:** In [DAILY_STATE.md](DAILY_STATE.md) see **Current day** and **Today**. Or open [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md) and find the first **Day N** that still has unchecked items.

---

## Vision → task docs (cross-reference)

Map from [VISION.md](VISION.md) sections to the task docs that implement or scope them. Use this to trace "where do I work for X?"

| VISION section | Task / scope doc |
|----------------|-------------------|
| **Theme and prototype** (Love as Epic Quest, Act 1 focus) | [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md) |
| **Campaign summary** (7 levels, planetoid, homestead travels) | [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md), [PLANETOID_HOMESTEAD.md](../tasks/PLANETOID_HOMESTEAD.md), [PLANETOID_DESIGN.md](../PLANETOID_DESIGN.md) |
| **Day and night** (physical vs spiritual, love → night bonuses) | [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md) § Day/night, [DAY_RESTORATION_LOOP.md](../tasks/DAY_RESTORATION_LOOP.md), [DAY_LOVE_OR_BOND.md](../tasks/DAY_LOVE_OR_BOND.md), [NIGHT_ENCOUNTER.md](../tasks/NIGHT_ENCOUNTER.md) |
| **Conversion not kill** (strip sin → loved; vendors/helpers/quest/pets) | [CONVERSION_NOT_KILL.md](../tasks/CONVERSION_NOT_KILL.md) |
| **Combat variety** (defend = ranged/AOE; planetoid = combos/single-target) | [DEFEND_COMBAT.md](../tasks/DEFEND_COMBAT.md), [PLANETOID_COMBAT.md](../tasks/PLANETOID_COMBAT.md) |
| **Moral system (Seven Sins & Virtues)** | [SIN_VIRTUE_SPECTRUM.md](../tasks/SIN_VIRTUE_SPECTRUM.md), [PLANETOID_DESIGN.md](../PLANETOID_DESIGN.md) |
| **Planetoid complete → next** (homestead lifts, travel to next) | [PLANETOID_HOMESTEAD.md](../tasks/PLANETOID_HOMESTEAD.md) |
| **Week 1 playtest gate** (crash → scout → boss → claim home) | [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md) § Week 1 playtest, [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) |
| **Vertical slice** (one moment, one beautiful corner) | [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md), [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md) |

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

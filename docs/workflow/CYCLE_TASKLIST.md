# Cycle task list

Generated when the automatic development cycle starts. The agent reads and updates this file each iteration.

**Source:** [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) section 3 (T1–T10). Skip T10 (deferred). Status here is synced with that file.

**Format:** One task per section. Each task has:
- **id** — Ordinal (T1, T2, …)
- **goal** — One-line description
- **success criteria** — How we know it is done
- **doc** — Optional link to task doc
- **status** — `pending` | `in_progress` | `completed` | `blocked`

---

## T1. Run yield and dungeon scripts in Editor

- **goal:** Create BP_Cultivation_POI and BP_Mining_POI (Day 19) and optionally place Dungeon_POI (Day 24) in level.
- **success criteria:** With Editor open, run create_bp_yield_nodes.py and (optional) place_dungeon_entrance.py with target level open; Blueprints/actors exist; PIE shows yield log and inventory change for nodes.
- **doc:** [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md) Day 19/24.
- **status:** completed

---

## T2. PIE spot-check

- **goal:** Confirm character spawn, ground, animation, and PCG in PIE on DemoMap.
- **success criteria:** Run pie_test_runner.py via MCP with PIE active; read Saved/pie_test_results.json; key checks pass (or document any false negatives).
- **doc:** README-Automation.md.
- **status:** completed

---

## T3. Manual level/PCG steps (planetoid)

- **goal:** Planetoid level playable with PCG POI and portal streaming.
- **success criteria:** Planetoid level exists; Landscape has PCG_Landscape tag; PCG Volume assigned Planetoid_POI_PCG; Generate produces instances; DemoMap has Level Streaming or trigger to open/stream planetoid.
- **doc:** [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md) Day 16–17, [PCG_SETUP.md](../PCG_SETUP.md).
- **status:** completed

---

## T4. Manual family/State Tree steps (Day 11–12)

- **goal:** Mass Spawner on DemoMap; MEC representation mesh; State Tree Defend/Night branch.
- **success criteria:** Mass Spawner placed with MEC_FamilyGatherer config; N agents spawn in PIE; MEC has Static Mesh set; ST_FamilyGatherer has Night? branch and Defend behavior; PIE with hw.TimeOfDay.Phase 2 validates Defend.
- **doc:** [DAY11_FAMILY_SPAWN.md](../tasks/DAY11_FAMILY_SPAWN.md), [DAY12_ROLE_PROTECTOR.md](../tasks/DAY12_ROLE_PROTECTOR.md), [FAMILY_AGENTS_MASS_STATETREE.md](../tasks/FAMILY_AGENTS_MASS_STATETREE.md).
- **status:** completed

---

## T5. Dungeon level streaming / interior

- **goal:** Dungeon_POI actor in level triggers level streaming or opens dungeon interior.
- **success criteria:** In Blueprint or level, Dungeon_POI (or trigger volume) opens/streams dungeon sublevel; doc updated with steps.
- **doc:** [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md) Day 24.
- **status:** completed

---

## T6. Populate CYCLE_TASKLIST (this file)

- **goal:** CYCLE_TASKLIST.md has concrete tasks (id, goal, success criteria, doc, status) for the next cycle.
- **success criteria:** Agent or user can read CYCLE_TASKLIST and pick "next task"; status updated as tasks complete.
- **doc:** This file.
- **status:** completed

---

## T7. Buffer / polish (Days 26–30)

- **goal:** One moment + one beautiful corner for vertical slice; or Milady pipeline progress; or bug polish.
- **success criteria:** Chosen buffer item(s) advanced and documented (e.g. vertical slice checklist, Milady import steps, or KNOWN_ERRORS/SESSION_LOG entries).
- **doc:** [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md) Days 26–30, [MILADY_IMPORT_ROADMAP.md](../tasks/MILADY_IMPORT_ROADMAP.md), [VISION.md](VISION.md).
- **status:** completed

---

## T8. Plan next 30-day window

- **goal:** Define the next block of days (goals, scope, success criteria) after the current 30-day block.
- **success criteria:** New schedule or roadmap section (e.g. in 30_DAY_SCHEDULE or new doc) with next N days and links to task docs.
- **doc:** [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md), [VISION.md](VISION.md), [MVP_AND_ROADMAP_STRATEGY.md](MVP_AND_ROADMAP_STRATEGY.md).
- **status:** completed

---

## T9. Refiner run (rules/strategy from run history)

- **goal:** Use run history and errors to update .cursor/rules, KNOWN_ERRORS.md, or AGENTS.md so the same failures don't recur.
- **success criteria:** Run Run-RefinerAgent.ps1 (or refine-rules-from-runs); at least one doc updated from suggestions in agent_run_history.ndjson or automation_loop_breaker_report.md.
- **doc:** [AUTOMATION_REFINEMENT.md](../AUTOMATION_REFINEMENT.md).
- **status:** completed

---

## Next window (from NEXT_30_DAY_WINDOW)

Tasks for the next cycle after T1–T9. Source: [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md). Order: Harden & demo first, then Deferred / Act 2 / Steam EA by priority.

---

## N1. Harden & demo (vertical slice lock)

- **goal:** Lock chosen moment + corner; run pre-demo checklist; optional 1–3 min recording.
- **success criteria:** VERTICAL_SLICE_CHECKLIST pre-demo all checked; moment and corner locked in PROTOTYPE_SCOPE; demo clip or sign-off.
- **doc:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md), [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md).
- **status:** completed

---

## N2. Deferred features (one or more)

- **goal:** Implement one or more deferred items from T10: full agentic building, SaveGame/role persistence, death→spirit hook, boss GAS + reward.
- **success criteria:** At least one of: full agentic building flow, role persistence across sessions, spirit roster on death, boss GAS + reward.
- **doc:** [DAY10_AGENTIC_BUILDING.md](../tasks/DAY10_AGENTIC_BUILDING.md), [DAY15_ROLE_PERSISTENCE.md](../tasks/DAY15_ROLE_PERSISTENCE.md), [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md) Day 21/25.
- **status:** pending

---

## N3. Act 2 prep (day/night, defend at home)

- **goal:** TimeOfDay drives Defend; family at homestead; optional night encounter.
- **success criteria:** PIE: hw.TimeOfDay.Phase 2 → family Defend; doc or stub for night spawn.
- **doc:** [DAY12_ROLE_PROTECTOR.md](../tasks/DAY12_ROLE_PROTECTOR.md), [VISION.md](VISION.md) Act 2.
- **status:** pending

---

## N4. Steam EA prep (build, packaging, store)

- **goal:** Ship-ready build; optional Steam depots and store draft.
- **success criteria:** Packaged build runs; checklist for store page.
- **doc:** [SETUP.md](../SETUP.md), project scope lock.
- **status:** pending

---

*When all of T1–T9 are Done or Blocked, work from N1–N4. Optional: Refiner run, buffer/polish.*

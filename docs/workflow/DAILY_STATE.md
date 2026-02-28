# Daily State

**Purpose:** This file is read at session start and updated at session end so you can ask "what did we do yesterday and what do we need to do today?" and get a clear answer. The agent updates it automatically when a session ends.

**Current day:** 1

---

## Yesterday (last session)

What was completed or in progress in the previous session. Empty if this is the first day or no work was done yet.

- PCG debug: volume_extent_z_padding reduced to 1000 cm (volume no longer extends far below map); docs updated (PCG_SETUP, HOMESTEAD_MAP) with checklist for trees/rocks out of bottom or not upright. transform_offset_z remains 0; re-running create_homestead_from_scratch.py re-applies graph config.

---

## Today (Day 1)

What we need to do today. Matches [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md) for the current day.

- [ ] Complete PCG manual steps: set Get Landscape Data (By Tag + `PCG_Landscape`), set mesh list on Static Mesh Spawner(s), assign graph to PCG Volume, click Generate. See [PCG_SETUP.md](../PCG_SETUP.md).
- [ ] Verify trees/rocks generate on landscape. See [PCG_FOREST_ON_MAP.md](../tasks/PCG_FOREST_ON_MAP.md) if needed.

---

## Tomorrow (Day 2)

Preview of next day's focus so the next session knows what’s coming.

- Implement or verify GAS 3 survivor skills (Blueprint or C++; see STACK_PLAN Layer 3).
- Character and placement polish: movement, camera, any remaining AnimBP/ground checks. See CHARACTER_ANIMATION, CHARACTER_GROUND.

---

**How this is updated:** At the end of each task session, the agent (1) appends to [SESSION_LOG.md](../SESSION_LOG.md), (2) updates this file: **Yesterday** = what was done this session; **Today** = tomorrow’s tasks (from 30_DAY_SCHEDULE); **Tomorrow** = the day after; **Current day** = next day number.

# Day 6 [1.1]: DemoMap layout (PCG or authored)

**Goal:** Define DemoMap bounds (PCG Volume or level blockout) so Homestead Phase 1 has a clear playable region. This is the first Homestead Phase 1 task. See [30_DAY_SCHEDULE.md](../workflow/30_DAY_SCHEDULE.md) Day 6 and [DEMO_MAP.md](../DEMO_MAP.md).

**Status:** Complete. Day 6 [1.1] marked [x] in 30_DAY_SCHEDULE; DAILY_STATE and SESSION_LOG updated. Run create_demo_from_scratch.py in Editor and complete manual PCG steps per section 2 if not yet done.

---

## 1. Prerequisites

- [ ] Day 5 playtest signed off (four beats confirmable; see [DAY5_PLAYTEST_SIGNOFF.md](DAY5_PLAYTEST_SIGNOFF.md)).
- [ ] Editor open; C++ built if you changed code.

---

## 2. Define DemoMap bounds

**Option A: Use DemoMap + script (recommended)**

1. **Ensure DemoMap exists:** Run `Content/Python/create_demo_from_scratch.py` (Tools → Execute Python Script or MCP). It calls `ensure_demo_map` and opens DemoMap. If the map was created by duplicating Main, convert to World Partition: **Tools → Convert Level** (see [DEMO_MAP.md](../DEMO_MAP.md) “DemoMap setup”). Save the level after conversion.
2. **Set bounds in config:** Edit `Content/Python/demo_map_config.json`. Set **`volume_center_x/y/z`** and **`volume_extent_x/y/z`** (in cm) to match your DemoMap playable region. If you use **`use_landscape_bounds: true`**, the script can read landscape bounds once (ensure Landscape is loaded: **Window → World Partition → Load All** if needed). See [DEMO_MAP.md](../DEMO_MAP.md) “PCG summary” and “Config”.
3. **Create or reuse PCG volume:** With DemoMap open, run **`Content/Python/create_demo_from_scratch.py`** again. It creates or reuses the PCG volume and sizes it from config (and optional exclusion zone). Set **`recreate_volume_and_graph: true`** only if you need to force full recreation.
4. **Manual PCG steps:** Assign the graph to the PCG Volume, set Get Landscape Data (By Tag `PCG_Landscape`), set mesh list on Static Mesh Spawner(s), then **Generate**. See [PCG_SETUP.md](../PCG_SETUP.md) and [PCG_VARIABLES_NO_ACCESS.md](../PCG_VARIABLES_NO_ACCESS.md).
5. **No ground visible:** If placeholders or trees float, load all World Partition cells (Window → World Partition → Load All) so the Landscape cell loads. See [DEMO_MAP.md](../DEMO_MAP.md) “No ground visible”.

**Option B: Level blockout only (no PCG yet)**

1. Open or create DemoMap (`/Game/HomeWorld/Maps/DemoMap`). World Partition is enabled by default (Empty Open World).
2. Place blockout volumes or placeholder actors for the compound (house, outbuildings, walls) per [DEMO_MAP.md](../DEMO_MAP.md) “Layout summary”. Optional: add a minimal landscape (Mode → Landscape → Create New), tag **PCG_Landscape**, then run **create_demo_from_scratch.py** for PCG.
3. Document the playable bounds (e.g. extent in cm or a note in this doc) so Day 7 resource nodes can be placed in/around the area.

---

## 3. Validation

- [ ] DemoMap opens; no load errors.
- [ ] Bounds defined: either (A) PCG Volume exists and is sized from config (and optional exclusion zone), and Generate has been run, or (B) blockout defines the playable region.
- [ ] If PCG: ground visible (Landscape loaded); trees/rocks generate as desired.
- [ ] Optional: PIE on DemoMap to confirm spawn and movement.

---

## 4. After Day 6 [1.1]

- [ ] 30_DAY_SCHEDULE: Day 6 [1.1] item marked [x].
- [ ] DAILY_STATE: Yesterday = Day 6 layout; Today = Day 7 (1.2 Resource nodes); Current day = 7 (or in progress).
- [ ] SESSION_LOG: Short entry for Day 6 [1.1] (bounds defined, script used, any blockers).

---

## References

- [DEMO_MAP.md](../DEMO_MAP.md) — Primary demo map, config, scripts, PCG.
- [PCG_SETUP.md](../PCG_SETUP.md) — Manual PCG steps, volume size, Generate.
- [PCG_VARIABLES_NO_ACCESS.md](../PCG_VARIABLES_NO_ACCESS.md) — Settings automation cannot set.
- [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md) / [AGENTIC_BUILDING.md](AGENTIC_BUILDING.md) — Context for later Homestead Phase 1 tasks (not required for 1.1).

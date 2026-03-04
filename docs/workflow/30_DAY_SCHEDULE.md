# HomeWorld – 30-Day Schedule

Day-by-day schedule inspired by prototype vision and campaign vision. Complete "today's" list, check off items, then continue or stop. **Current day** = the first Day N below that still has unchecked items.

**Prototype gate:** Day 5 = sign-off for the core loop. Do not start Day 6 until explore → fight → build is playable (crash → scout → boss → claim home). Days 26–30: pick one moment + one beautiful corner for the vertical slice and/or record a short demo. See [VISION.md](VISION.md) (Demonstrable prototype and vertical slice).

---

## How to use

1. Open this file and find the first day with unchecked items.
2. Complete each task for that day. Items link to task docs or setup guides for steps.
3. When done, change `- [ ]` to `- [x]` for each item. Then either work ahead to the next day or stop.

Days are ordinal (Day 1, Day 2, …), not calendar dates. Start anytime and resume where you left off.

---

## Day-by-day overview

| Day | Focus | Task IDs / description |
|-----|--------|-------------------------|
| 1 | Act 1: PCG forest | Finish PCG manual steps; Generate |
| 2 | Act 1: GAS + character | GAS 3 skills; character/placement polish |
| 3 | Act 1: Placement + playtest | GetPlacementHit/placement; Week 1 playtest |
| 4 | Act 1: Polish + optional Milady | Polish explore→fight→build; optional ensure_milady_folders |
| 5 | Act 1: Buffer / playtest sign-off | Playtest crash→scout→boss→claim home |
| 6 | Homestead Phase 1 | 1.1 Homestead layout |
| 7 | Homestead Phase 1 | 1.2 Resource nodes |
| 8 | Homestead Phase 1 | 1.3 Resource collection loop |
| 9 | Homestead Phase 1 | 1.4 Home asset placement |
| 10 | Homestead Phase 1 | 1.5 Optional: agentic building |
| 11 | Family Phase 2 | 2.1 Family spawn |
| 12 | Family Phase 2 | 2.2 Role: Protector |
| 13 | Family Phase 2 | 2.3 Role: Healer |
| 14 | Family Phase 2 | 2.4 Role: Child |
| 15 | Family Phase 2 | 2.5 Role assignment and persistence |
| 16 | Planetoid Phase 3 | 3.1 Planetoid level / sublevel |
| 17 | Planetoid Phase 3 | 3.2 PCG POI placement |
| 18 | Planetoid Phase 3 | 3.3 Shrine POI, 3.4 Treasure POI |
| 19 | Planetoid Phase 3 | 3.5 Cultivation, 3.6 Mining |
| 20 | Planetoid Phase 3 | 3.7 Visit and interact |
| 21 | Spirits Phase 4 | 4.1 Death → spirit, 4.2 Spirit roster |
| 22 | Spirits Phase 4 | 4.3 Assign spirit to node, 4.4 Node progress/yield |
| 23 | Spirits Phase 4 | 4.5 Unassign / reclaim spirit |
| 24 | Dungeon Phase 5 | 5.1 Dungeon as POI, 5.2 Dungeon interior |
| 25 | Dungeon Phase 5 | 5.3 Boss actor, 5.4 Dungeon complete / reward |
| 26–30 | Buffer | Milady pipeline, 7-sins prep, polish, or catch-up |

---

## Day 1

**Act 1 — PCG forest**

- [x] Complete PCG manual steps: set Get Landscape Data (By Tag + `PCG_Landscape`), set mesh list on Static Mesh Spawner(s), assign graph to PCG Volume, click Generate. See [PCG_SETUP.md](../PCG_SETUP.md).
- [x] Verify trees/rocks generate on landscape. See [PCG_FOREST_ON_MAP.md](../tasks/PCG_FOREST_ON_MAP.md) if needed.

---

## Day 2

**Act 1 — GAS and character**

- [x] Implement or verify GAS 3 survivor skills (Blueprint or C++; see [STACK_PLAN.md](../STACK_PLAN.md) Layer 3). Run `Content/Python/setup_gas_abilities.py` in Editor to create GA_PrimaryAttack, GA_Dodge, GA_Interact and bind input; see [GAS_SURVIVOR_SKILLS.md](../tasks/GAS_SURVIVOR_SKILLS.md).
- [x] Character and placement polish: movement, camera, any remaining AnimBP/ground checks. See [CHARACTER_ANIMATION.md](../tasks/CHARACTER_ANIMATION.md), [CHARACTER_GROUND.md](../tasks/CHARACTER_GROUND.md). Verify in PIE on DemoMap.

---

## Day 3

**Act 1 — Placement and playtest**

- [x] Verify GetPlacementHit / GetPlacementTransform for placing build orders or props. See C++ [BuildPlacementSupport](../../Source/HomeWorld/BuildPlacementSupport.h), [AGENTIC_BUILDING.md](../tasks/AGENTIC_BUILDING.md), and [DAY3_PLACEMENT_AND_PLAYTEST.md](../tasks/DAY3_PLACEMENT_AND_PLAYTEST.md).
- [x] Run Week 1 playtest: explore → fight → build loop. See [VISION.md](VISION.md) (success criteria) and [DAY3_PLACEMENT_AND_PLAYTEST.md](../tasks/DAY3_PLACEMENT_AND_PLAYTEST.md).

---

## Day 4

**Act 1 — Polish and optional Milady**

- [x] Polish first playable loop (explore → fight → build). No family or co-op yet.
- [x] Optional: Run `ensure_milady_folders.py` and `create_milady_pastel_material.py` via MCP or Tools → Execute Python Script. See [MILADY_IMPORT_ROADMAP.md](../tasks/MILADY_IMPORT_ROADMAP.md), [MILADY_IMPORT_SETUP.md](../MILADY_IMPORT_SETUP.md).

---

## Day 5

**Act 1 — Playtest sign-off**

- [x] Playtest: survive 3 missions (crash → scout → boss → claim home). See [VISION.md](VISION.md) (Week 1 playtest goal).
- [x] Sign off Act 1 or note remaining items for buffer days.

---

## Day 6

**Homestead Phase 1 — Layout**

- [x] **[1.1] DemoMap layout (PCG or authored)** — Define DemoMap bounds (PCG Volume or level blockout). See [DAY6_HOMESTEAD_LAYOUT.md](../tasks/DAY6_HOMESTEAD_LAYOUT.md) and [DEMO_MAP.md](../DEMO_MAP.md). Context: [FAMILY_AGENTS_MASS_STATETREE.md](../tasks/FAMILY_AGENTS_MASS_STATETREE.md) / [AGENTIC_BUILDING.md](../tasks/AGENTIC_BUILDING.md).

---

## Day 7

**Homestead Phase 1 — Resource nodes**

- [x] **[1.2] Resource nodes (trees as resource object)** — Place harvestable tree nodes on DemoMap. Run create_bp_harvestable_tree.py then place_resource_nodes.py (or create BP manually and place). See [DAY7_RESOURCE_NODES.md](../tasks/DAY7_RESOURCE_NODES.md) and [AGENTIC_BUILDING.md](../tasks/AGENTIC_BUILDING.md) (BP_WoodPile, SO).

---

## Day 8

**Homestead Phase 1 — Resource collection**

- [x] **[1.3] Resource collection loop (player)** — C++ TryHarvestInFront + GA_Interact reparented to HomeWorldInteractAbility; PIE validated. See [DAY8_RESOURCE_COLLECTION.md](../tasks/DAY8_RESOURCE_COLLECTION.md).

---

## Day 9

**Homestead Phase 1 — Home placement**

- [x] **[1.4] Home asset placement (player)** — Place key P, GA_Place, TryPlaceAtCursor; PIE validated. See [DAY9_HOME_PLACEMENT.md](../tasks/DAY9_HOME_PLACEMENT.md).

---

## Day 10

**Homestead Phase 1 — Optional agentic building**

- [x] **[1.5] Optional: agentic building** — Prep done (BP_BuildOrder_Wall, create_so_wall_builder); full agentic building deferred to after Phase 2. See [DAY10_AGENTIC_BUILDING.md](../tasks/DAY10_AGENTIC_BUILDING.md), [AGENTIC_BUILDING.md](../tasks/AGENTIC_BUILDING.md).

---

## Day 11

**Family Phase 2 — Spawn**

- [x] **[2.1] Family spawn in homestead** — Run create_mec_family_gatherer.py, create ST_FamilyGatherer in Editor, link_state_tree_to_mec.py, place Mass Spawner on DemoMap. See [DAY11_FAMILY_SPAWN.md](../tasks/DAY11_FAMILY_SPAWN.md), [FAMILY_AGENTS_MASS_STATETREE.md](../tasks/FAMILY_AGENTS_MASS_STATETREE.md).

---

## Day 12

**Family Phase 2 — Protector**

- [x] **[2.2] Role: Attack/Defend (Protector)** — State Tree/combat behavior; GAS combat abilities. See [DAY12_ROLE_PROTECTOR.md](../tasks/DAY12_ROLE_PROTECTOR.md) and [FAMILY_AGENTS_MASS_STATETREE.md](../tasks/FAMILY_AGENTS_MASS_STATETREE.md).

---

## Day 13

**Family Phase 2 — Healer**

- [x] **[2.3] Role: Support/Healer** — C++ UHomeWorldHealAbility; run create_ga_heal.py for GA_Heal. See [DAY13_ROLE_HEALER.md](../tasks/DAY13_ROLE_HEALER.md), [FAMILY_AGENTS_MASS_STATETREE.md](../tasks/FAMILY_AGENTS_MASS_STATETREE.md).

---

## Day 14

**Family Phase 2 — Child**

- [x] **[2.4] Role: Child** — Non-combat; follow player, safe nodes. See [DAY14_ROLE_CHILD.md](../tasks/DAY14_ROLE_CHILD.md), [FAMILY_AGENTS_MASS_STATETREE.md](../tasks/FAMILY_AGENTS_MASS_STATETREE.md).

---

## Day 15

**Family Phase 2 — Persistence**

- [x] **[2.5] Role assignment and persistence** — Store role per family member (tag/fragment or subsystem). See [DAY15_ROLE_PERSISTENCE.md](../tasks/DAY15_ROLE_PERSISTENCE.md), [FAMILY_AGENTS_MASS_STATETREE.md](../tasks/FAMILY_AGENTS_MASS_STATETREE.md).

---

## Day 16

**Planetoid Phase 3 — Level**

- [x] **[3.1] Planetoid level / sublevel** — Create one planetoid level; travel via portal/sublevel. See [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md), [PLANETOID_DESIGN.md](../PLANETOID_DESIGN.md).

---

## Day 17

**Planetoid Phase 3 — POI placement**

- [x] **[3.2] PCG POI placement (high level)** — PCG graph places POI actors. See [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md).

---

## Day 18

**Planetoid Phase 3 — Shrine and Treasure**

- [x] **[3.3] Shrine POI** — Shrine actor with interaction/GAS. See [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md).
- [x] **[3.4] Treasure POI** — Treasure actor; loot on interact.

---

## Day 19

**Planetoid Phase 3 — Cultivation and Mining**

- [x] **[3.5] Cultivation section** — Cultivation node; spirits work it; yields over time. See [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md).
- [x] **[3.6] Mining section** — Mining node; spirits work it; yields ore/stone.

---

## Day 20

**Planetoid Phase 3 — Visit and interact**

- [ ] **[3.7] Visit and interact** — Player can travel to planetoid, reach POIs, interact (harvest treasure, activate shrine, etc.).

---

## Day 21

**Spirits Phase 4 — Conversion and roster**

- [x] **[4.1] Death → spirit conversion** — On death: mark as spirit, remove from roster. See [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md).
- [x] **[4.2] Spirit roster / list** — Subsystem or GameState: list of spirits.

---

## Day 22

**Spirits Phase 4 — Assign and yield**

- [x] **[4.3] Command: assign spirit to node** — Player assigns spirit to node. See [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md).
- [x] **[4.4] Node progress and yield** — Nodes produce resources when worked; player collects.

---

## Day 23

**Spirits Phase 4 — Unassign**

- [x] **[4.5] Unassign / reclaim spirit** — Player unassigns spirit; spirit idle for reassignment. See [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md).

---

## Day 24

**Dungeon Phase 5 — POI and interior**

- [ ] **[5.1] Dungeon as POI** — Dungeon entrance actor/trigger; on interact, load dungeon sublevel.
- [ ] **[5.2] Dungeon interior** — Interior layout (authored or PCG); boss arena at end.

---

## Day 25

**Dungeon Phase 5 — Boss and reward**

- [x] **[5.3] Boss actor and abilities** — Boss pawn with GAS; spawn in arena; drop loot. See [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md).
- [x] **[5.4] Dungeon complete / reward** — On boss death: grant reward.

---

## Day 26

**Buffer**

- [x] Catch-up, Milady pipeline, or 7-sins prep. See [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md), [MILADY_IMPORT_ROADMAP.md](../tasks/MILADY_IMPORT_ROADMAP.md), [VISION.md](VISION.md). Vertical slice: [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md).

---

## Day 27

**Buffer**

- [x] Continue buffer or polish: performance, LODs, onboarding. See [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md).

---

## Day 28

**Buffer**

- [ ] Continue buffer work or start post-alpha prep (Steam EA scope).

---

## Day 29

**Buffer**

- [x] Buffer or documentation updates. See [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md).

---

## Day 30

**Buffer**

- [x] Final catch-up, sign-off 30-day block, or plan next 30-day window. See [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md).

---

**See also:** [VISION.md](VISION.md), [README.md](README.md), [SETUP.md](../SETUP.md), [KNOWN_ERRORS.md](../KNOWN_ERRORS.md), [CONVENTIONS.md](../CONVENTIONS.md). **Next block:** [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md).

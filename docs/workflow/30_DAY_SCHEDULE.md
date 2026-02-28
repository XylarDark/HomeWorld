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

- [ ] Complete PCG manual steps: set Get Landscape Data (By Tag + `PCG_Landscape`), set mesh list on Static Mesh Spawner(s), assign graph to PCG Volume, click Generate. See [PCG_SETUP.md](../PCG_SETUP.md).
- [ ] Verify trees/rocks generate on landscape. See [PCG_FOREST_ON_MAP.md](../tasks/PCG_FOREST_ON_MAP.md) if needed.

---

## Day 2

**Act 1 — GAS and character**

- [ ] Implement or verify GAS 3 survivor skills (Blueprint or C++; see [STACK_PLAN.md](../STACK_PLAN.md) Layer 3).
- [ ] Character and placement polish: movement, camera, any remaining AnimBP/ground checks. See [CHARACTER_ANIMATION.md](../tasks/CHARACTER_ANIMATION.md), [CHARACTER_GROUND.md](../tasks/CHARACTER_GROUND.md).

---

## Day 3

**Act 1 — Placement and playtest**

- [ ] Verify GetPlacementHit / GetPlacementTransform for placing build orders or props. See C++ [BuildPlacementSupport](../../Source/HomeWorld/BuildPlacementSupport.h) and [AGENTIC_BUILDING.md](../tasks/AGENTIC_BUILDING.md).
- [ ] Run Week 1 playtest: explore → fight → build loop. See [VISION.md](VISION.md) (success criteria).

---

## Day 4

**Act 1 — Polish and optional Milady**

- [ ] Polish first playable loop (explore → fight → build). No family or co-op yet.
- [ ] Optional: Run `ensure_milady_folders.py` and `create_milady_pastel_material.py` via MCP or Tools → Execute Python Script. See [MILADY_IMPORT_ROADMAP.md](../tasks/MILADY_IMPORT_ROADMAP.md), [MILADY_IMPORT_SETUP.md](../MILADY_IMPORT_SETUP.md).

---

## Day 5

**Act 1 — Playtest sign-off**

- [ ] Playtest: survive 3 missions (crash → scout → boss → claim home). See [VISION.md](VISION.md) (Week 1 playtest goal).
- [ ] Sign off Act 1 or note remaining items for buffer days.

---

## Day 6

**Homestead Phase 1 — Layout**

- [ ] **[1.1] Homestead layout (PCG or authored)** — Define homestead bounds (PCG Volume or level blockout). Option: Use the Homestead map and [HOMESTEAD_MAP.md](../HOMESTEAD_MAP.md). See [FAMILY_AGENTS_MASS_STATETREE.md](../tasks/FAMILY_AGENTS_MASS_STATETREE.md) / [AGENTIC_BUILDING.md](../tasks/AGENTIC_BUILDING.md) for context.

---

## Day 7

**Homestead Phase 1 — Resource nodes**

- [ ] **[1.2] Resource nodes in/around homestead** — Place or spawn resource piles (e.g. BP_WoodPile). See [AGENTIC_BUILDING.md](../tasks/AGENTIC_BUILDING.md) (BP_WoodPile, SO).

---

## Day 8

**Homestead Phase 1 — Resource collection**

- [ ] **[1.3] Resource collection loop (player)** — Player can harvest resource piles; interaction/GAS grants resource (inventory or attribute). Stub: inventory subsystem or GAS attribute "Wood"; on harvest add amount.

---

## Day 9

**Homestead Phase 1 — Home placement**

- [ ] **[1.4] Home asset placement (player)** — Use GetPlacementHit/GetPlacementTransform to place build orders (e.g. BP_BuildOrder_Wall) or props. Input: place key → trace → spawn at hit.

---

## Day 10

**Homestead Phase 1 — Optional agentic building**

- [ ] **[1.5] Optional: agentic building** — Family agents fulfill build orders (SO_WallBuilder, State Tree BUILD). See [AGENTIC_BUILDING.md](../tasks/AGENTIC_BUILDING.md). Can be done after Phase 2.

---

## Day 11

**Family Phase 2 — Spawn**

- [ ] **[2.1] Family spawn in homestead** — Spawn N family members at start; tag or role ID per member. See [FAMILY_AGENTS_MASS_STATETREE.md](../tasks/FAMILY_AGENTS_MASS_STATETREE.md).

---

## Day 12

**Family Phase 2 — Protector**

- [ ] **[2.2] Role: Attack/Defend (Protector)** — State Tree/combat behavior; GAS combat abilities. See [FAMILY_AGENTS_MASS_STATETREE.md](../tasks/FAMILY_AGENTS_MASS_STATETREE.md).

---

## Day 13

**Family Phase 2 — Healer**

- [ ] **[2.3] Role: Support/Healer** — Behavior that prioritizes healing/buffing; GAS heal ability. See [FAMILY_AGENTS_MASS_STATETREE.md](../tasks/FAMILY_AGENTS_MASS_STATETREE.md).

---

## Day 14

**Family Phase 2 — Child**

- [ ] **[2.4] Role: Child** — Non-combat or limited combat; follow player, safe nodes. See [FAMILY_AGENTS_MASS_STATETREE.md](../tasks/FAMILY_AGENTS_MASS_STATETREE.md).

---

## Day 15

**Family Phase 2 — Persistence**

- [ ] **[2.5] Role assignment and persistence** — Store role per family member (GameState/SaveGame/subsystem). See [FAMILY_AGENTS_MASS_STATETREE.md](../tasks/FAMILY_AGENTS_MASS_STATETREE.md).

---

## Day 16

**Planetoid Phase 3 — Level**

- [ ] **[3.1] Planetoid level / sublevel** — Create one planetoid level; travel from homestead via portal or sublevel. See [PLANETOID_DESIGN.md](../PLANETOID_DESIGN.md).

---

## Day 17

**Planetoid Phase 3 — POI placement**

- [ ] **[3.2] PCG POI placement (high level)** — PCG graph that places POI actors (Shrine, Treasure, CultivationNode, MiningNode).

---

## Day 18

**Planetoid Phase 3 — Shrine and Treasure**

- [ ] **[3.3] Shrine POI** — Shrine actor with interaction/GAS.
- [ ] **[3.4] Treasure POI** — Treasure actor; loot on interact.

---

## Day 19

**Planetoid Phase 3 — Cultivation and Mining**

- [ ] **[3.5] Cultivation section** — Cultivation node/zone; workable by spirits (Phase 4); yields resources over time.
- [ ] **[3.6] Mining section** — Mining node/zone; workable by spirits; yields ore/stone.

---

## Day 20

**Planetoid Phase 3 — Visit and interact**

- [ ] **[3.7] Visit and interact** — Player can travel to planetoid, reach POIs, interact (harvest treasure, activate shrine, etc.).

---

## Day 21

**Spirits Phase 4 — Conversion and roster**

- [ ] **[4.1] Death → spirit conversion** — On character death: mark as spirit, remove from playable roster.
- [ ] **[4.2] Spirit roster / list** — Subsystem or GameState: list of spirits; UI or command interface can show available spirits.

---

## Day 22

**Spirits Phase 4 — Assign and yield**

- [ ] **[4.3] Command: assign spirit to node** — Player assigns spirit to CultivationNode/MiningNode; spirit contributes to node progress.
- [ ] **[4.4] Node progress and yield** — Cultivation/mining nodes produce resources when worked by N spirits; player can collect.

---

## Day 23

**Spirits Phase 4 — Unassign**

- [ ] **[4.5] Unassign / reclaim spirit** — Player can unassign spirit from a node (spirit becomes idle for reassignment).

---

## Day 24

**Dungeon Phase 5 — POI and interior**

- [ ] **[5.1] Dungeon as POI** — Dungeon entrance actor/trigger; on interact, load dungeon sublevel.
- [ ] **[5.2] Dungeon interior** — Interior layout (authored or PCG); boss arena at end.

---

## Day 25

**Dungeon Phase 5 — Boss and reward**

- [ ] **[5.3] Boss actor and abilities** — Boss pawn with GAS: health, abilities, phase; spawn in arena; on death drop loot.
- [ ] **[5.4] Dungeon complete / reward** — On boss death: grant reward (treasure, key, story flag); optional respawn or one-time.

---

## Day 26

**Buffer**

- [ ] Catch-up, Milady pipeline integration, or 7-sins/moral-system prep. See [MILADY_IMPORT_ROADMAP.md](../tasks/MILADY_IMPORT_ROADMAP.md), [VISION.md](VISION.md) (moral system).

---

## Day 27

**Buffer**

- [ ] Continue Day 26 focus or polish: performance, LODs, onboarding.

---

## Day 28

**Buffer**

- [ ] Continue buffer work or start post-alpha prep (Steam EA scope).

---

## Day 29

**Buffer**

- [ ] Continue buffer work or documentation updates.

---

## Day 30

**Buffer**

- [ ] Final catch-up, sign-off 30-day block, or plan next 30-day window.

---

**See also:** [VISION.md](VISION.md), [README.md](README.md), [SETUP.md](../SETUP.md), [KNOWN_ERRORS.md](../KNOWN_ERRORS.md), [CONVENTIONS.md](../CONVENTIONS.md).

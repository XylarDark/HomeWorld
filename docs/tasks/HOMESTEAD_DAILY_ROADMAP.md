# Homestead & Planetoid — Daily Task Roadmap

Day-by-day breakdown of the [Homestead & Planetoid Implementation Roadmap](HOMESTEAD_PLANETOID_ROADMAP.md). Use this to work in fixed daily chunks: open the doc, do "today's" list, then either continue to the next day or stop.

---

## How to use

1. **Current day** = the first **Day N** below that still has unchecked items. Open this file and scroll to that day.
2. **Today's list:** Complete each task for that day. Each item links to the main roadmap (phase/task ID) for full description and acceptance criteria.
3. **When done:** Check off the items (edit the file and change `- [ ]` to `- [x]`). Then either:
   - **Work ahead:** Move to the next day and continue, or
   - **Stop:** That’s all for the day.

Days are ordinal (Day 1, Day 2, …), not calendar dates, so you can start anytime and resume where you left off.

---

## Day-by-day overview

| Day | Phase | Task IDs | Focus |
|-----|-------|----------|--------|
| 1 | 1 | 1.1 | Homestead layout (PCG or authored) |
| 2 | 1 | 1.2 | Resource nodes in/around homestead |
| 3 | 1 | 1.3 | Resource collection loop (player) |
| 4 | 1 | 1.4 | Home asset placement (player) |
| 5 | 1 | 1.5 | Optional: agentic building |
| 6 | 2 | 2.1 | Family spawn in homestead |
| 7 | 2 | 2.2 | Role: Attack/Defend (Protector) |
| 8 | 2 | 2.3 | Role: Support/Healer |
| 9 | 2 | 2.4 | Role: Child |
| 10 | 2 | 2.5 | Role assignment and persistence |
| 11 | 3 | 3.1 | Planetoid level / sublevel |
| 12 | 3 | 3.2 | PCG POI placement |
| 13 | 3 | 3.3, 3.4 | Shrine POI + Treasure POI |
| 14 | 3 | 3.5 | Cultivation section |
| 15 | 3 | 3.6 | Mining section |
| 16 | 3 | 3.7 | Visit and interact |
| 17 | 4 | 4.1 | Death → spirit conversion |
| 18 | 4 | 4.2 | Spirit roster / list |
| 19 | 4 | 4.3 | Command: assign spirit to node |
| 20 | 4 | 4.4 | Node progress and yield |
| 21 | 4 | 4.5 | Unassign / reclaim spirit |
| 22 | 5 | 5.1 | Dungeon as POI |
| 23 | 5 | 5.2 | Dungeon interior |
| 24 | 5 | 5.3 | Boss actor and abilities |
| 25 | 5 | 5.4 | Dungeon complete / reward |

---

## Day 1

**Phase 1 — Homestead layout**

- [ ] **[1.1] Homestead layout (PCG or authored)** — Define homestead bounds (PCG Volume or level blockout). See [Phase 1](HOMESTEAD_PLANETOID_ROADMAP.md#phase-1-homestead-generation-resources-home-placement) in the main roadmap. **Option:** Use the Homestead map and [HOMESTEAD_MAP.md](../HOMESTEAD_MAP.md) (authored map + placeholders + PCG).

---

## Day 2

**Phase 1 — Resource nodes**

- [ ] **[1.2] Resource nodes in/around homestead** — Place or spawn resource piles (e.g. BP_WoodPile) in homestead or adjacent area. See [Phase 1](HOMESTEAD_PLANETOID_ROADMAP.md#phase-1-homestead-generation-resources-home-placement).

---

## Day 3

**Phase 1 — Resource collection**

- [ ] **[1.3] Resource collection loop (player)** — Player can harvest resource piles; interaction/GAS grants resource (inventory or attribute). See [Phase 1](HOMESTEAD_PLANETOID_ROADMAP.md#phase-1-homestead-generation-resources-home-placement).

---

## Day 4

**Phase 1 — Home placement**

- [ ] **[1.4] Home asset placement (player)** — Use GetPlacementHit/GetPlacementTransform to place build orders or props. See [Phase 1](HOMESTEAD_PLANETOID_ROADMAP.md#phase-1-homestead-generation-resources-home-placement).

---

## Day 5

**Phase 1 — Optional agentic building**

- [ ] **[1.5] Optional: agentic building** — Family agents fulfill build orders (SO_WallBuilder, State Tree BUILD). Can be done after Phase 2. See [Phase 1](HOMESTEAD_PLANETOID_ROADMAP.md#phase-1-homestead-generation-resources-home-placement) and [AGENTIC_BUILDING.md](AGENTIC_BUILDING.md).

---

## Day 6

**Phase 2 — Family spawn**

- [ ] **[2.1] Family spawn in homestead** — Spawn N family members at start; tag or role ID per member. See [Phase 2](HOMESTEAD_PLANETOID_ROADMAP.md#phase-2-family-roles-attackdefend-healer-child).

---

## Day 7

**Phase 2 — Protector role**

- [ ] **[2.2] Role: Attack/Defend (Protector)** — State Tree/combat behavior; GAS combat abilities. See [Phase 2](HOMESTEAD_PLANETOID_ROADMAP.md#phase-2-family-roles-attackdefend-healer-child).

---

## Day 8

**Phase 2 — Healer role**

- [ ] **[2.3] Role: Support/Healer** — Behavior that prioritizes healing/buffing; GAS heal ability. See [Phase 2](HOMESTEAD_PLANETOID_ROADMAP.md#phase-2-family-roles-attackdefend-healer-child).

---

## Day 9

**Phase 2 — Child role**

- [ ] **[2.4] Role: Child** — Non-combat or limited combat; follow player, safe nodes. See [Phase 2](HOMESTEAD_PLANETOID_ROADMAP.md#phase-2-family-roles-attackdefend-healer-child).

---

## Day 10

**Phase 2 — Role persistence**

- [ ] **[2.5] Role assignment and persistence** — Store role per family member (GameState/SaveGame/subsystem). See [Phase 2](HOMESTEAD_PLANETOID_ROADMAP.md#phase-2-family-roles-attackdefend-healer-child).

---

## Day 11

**Phase 3 — Planetoid level**

- [ ] **[3.1] Planetoid level / sublevel** — Create one planetoid level; travel from homestead via portal or sublevel. See [Phase 3](HOMESTEAD_PLANETOID_ROADMAP.md#phase-3-planetoid-generation-and-pois-shrines-treasure-cultivation-mining).

---

## Day 12

**Phase 3 — POI placement**

- [ ] **[3.2] PCG POI placement (high level)** — PCG graph that places POI actors (Shrine, Treasure, CultivationNode, MiningNode). See [Phase 3](HOMESTEAD_PLANETOID_ROADMAP.md#phase-3-planetoid-generation-and-pois-shrines-treasure-cultivation-mining).

---

## Day 13

**Phase 3 — Shrine and Treasure POIs**

- [ ] **[3.3] Shrine POI** — Shrine actor with interaction/GAS. See [Phase 3](HOMESTEAD_PLANETOID_ROADMAP.md#phase-3-planetoid-generation-and-pois-shrines-treasure-cultivation-mining).
- [ ] **[3.4] Treasure POI** — Treasure actor; loot on interact. See [Phase 3](HOMESTEAD_PLANETOID_ROADMAP.md#phase-3-planetoid-generation-and-pois-shrines-treasure-cultivation-mining).

---

## Day 14

**Phase 3 — Cultivation**

- [ ] **[3.5] Cultivation section** — Cultivation node/zone; workable by spirits (Phase 4); yields resources over time. See [Phase 3](HOMESTEAD_PLANETOID_ROADMAP.md#phase-3-planetoid-generation-and-pois-shrines-treasure-cultivation-mining).

---

## Day 15

**Phase 3 — Mining**

- [ ] **[3.6] Mining section** — Mining node/zone; workable by spirits; yields ore/stone. See [Phase 3](HOMESTEAD_PLANETOID_ROADMAP.md#phase-3-planetoid-generation-and-pois-shrines-treasure-cultivation-mining).

---

## Day 16

**Phase 3 — Visit and interact**

- [ ] **[3.7] Visit and interact** — Player can travel to planetoid, reach POIs, interact (harvest treasure, activate shrine, etc.). See [Phase 3](HOMESTEAD_PLANETOID_ROADMAP.md#phase-3-planetoid-generation-and-pois-shrines-treasure-cultivation-mining).

---

## Day 17

**Phase 4 — Spirit conversion**

- [ ] **[4.1] Death → spirit conversion** — On character death: mark as spirit, remove from playable roster. See [Phase 4](HOMESTEAD_PLANETOID_ROADMAP.md#phase-4-spirit-system-and-command-spirits-to-work-nodes).

---

## Day 18

**Phase 4 — Spirit roster**

- [ ] **[4.2] Spirit roster / list** — Subsystem or GameState: list of spirits; UI or command interface can show available spirits. See [Phase 4](HOMESTEAD_PLANETOID_ROADMAP.md#phase-4-spirit-system-and-command-spirits-to-work-nodes).

---

## Day 19

**Phase 4 — Assign spirit to node**

- [ ] **[4.3] Command: assign spirit to node** — Player assigns spirit to CultivationNode/MiningNode; spirit contributes to node progress. See [Phase 4](HOMESTEAD_PLANETOID_ROADMAP.md#phase-4-spirit-system-and-command-spirits-to-work-nodes).

---

## Day 20

**Phase 4 — Node progress and yield**

- [ ] **[4.4] Node progress and yield** — Cultivation/mining nodes produce resources when worked by N spirits; player can collect. See [Phase 4](HOMESTEAD_PLANETOID_ROADMAP.md#phase-4-spirit-system-and-command-spirits-to-work-nodes).

---

## Day 21

**Phase 4 — Unassign spirit**

- [ ] **[4.5] Unassign / reclaim spirit** — Player can unassign spirit from a node (spirit becomes idle for reassignment). See [Phase 4](HOMESTEAD_PLANETOID_ROADMAP.md#phase-4-spirit-system-and-command-spirits-to-work-nodes).

---

## Day 22

**Phase 5 — Dungeon POI**

- [ ] **[5.1] Dungeon as POI** — Dungeon entrance actor/trigger; on interact, load dungeon sublevel. See [Phase 5](HOMESTEAD_PLANETOID_ROADMAP.md#phase-5-dungeon-and-boss).

---

## Day 23

**Phase 5 — Dungeon interior**

- [ ] **[5.2] Dungeon interior** — Interior layout (authored or PCG); boss arena at end. See [Phase 5](HOMESTEAD_PLANETOID_ROADMAP.md#phase-5-dungeon-and-boss).

---

## Day 24

**Phase 5 — Boss**

- [ ] **[5.3] Boss actor and abilities** — Boss pawn with GAS: health, abilities, phase; spawn in arena; on death drop loot. See [Phase 5](HOMESTEAD_PLANETOID_ROADMAP.md#phase-5-dungeon-and-boss).

---

## Day 25

**Phase 5 — Dungeon complete**

- [ ] **[5.4] Dungeon complete / reward** — On boss death: grant reward (treasure, key, story flag); optional respawn or one-time. See [Phase 5](HOMESTEAD_PLANETOID_ROADMAP.md#phase-5-dungeon-and-boss).

---

**Full roadmap:** [HOMESTEAD_PLANETOID_ROADMAP.md](HOMESTEAD_PLANETOID_ROADMAP.md)

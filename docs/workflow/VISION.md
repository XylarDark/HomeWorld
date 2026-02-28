# HomeWorld – Vision (Consolidated)

Single source for project theme, campaign narrative, moral system, and scope. Informs the [30-day schedule](30_DAY_SCHEDULE.md) and all task work.

---

## Theme and prototype

**"Love as Epic Quest"** – Dopamine from intense combat + Oxytocin from nurturing bonds. Players build and protect a life worth fighting for. Roles for casual (healer/home) and hardcore (protector) players.

**Act 1 focus (Lone Wanderer):** Crash-land, scout biomes, fight bosses, claim home. Solo, 2–3h. Emotional beat: isolation → determination.

**Week 1 playtest goal:** Survive 3 missions: crash → scout → boss → claim home.

**Tech spine (Act 1):** PCG forest biome, GAS (3 skills), proc-gen realms, basic building. Free assets: FAB survival char, Quixel biomes.

**Success criteria:** First playable loop = explore → fight → build. No family or co-op yet.

---

## Demonstrable prototype and vertical slice

- **MVP (Minimum Viable Product):** Smallest playable version that validates the core promise (one compelling mechanic, minimal art/content). Goal: test fun and engagement early.
- **Vertical slice:** A short, complete section of the game at near-final quality: one clear gameplay loop, one memorable moment, and one polished "beautiful corner" to show capability. Used for stakeholders, playtesters, or funding.

**Campaign alignment:** The prototype is set in the **post–inciting incident** phase: the family has been taken; the player is the lone wanderer. Everything we build (explore, fight, build, claim home) is the first leg of the rescue — isolation → determination. "Claim home" = claiming a **new base of operations** (the homestead you build in the 30-day schedule), not the lost opening homestead. This is the foothold from which the player will go to Levels 1–7 to get the family back.

**Gate:** The **Week 1 playtest** (crash → scout → boss → claim home) is the prototype gate. Do not start Homestead/Family phases until explore → fight → build is playable and tested.

**By end of 30 days:** Choose **one moment** (e.g. claiming the homestead after the first boss, or first family member rescued) and **one beautiful corner** (e.g. homestead compound) to polish for a showable vertical slice and/or short demo video.

---

## Campaign summary

| Phase | Player state | Goal |
|-------|--------------|------|
| Opening | Homestead + family | Tutorial (resources, build, magic, combat) |
| Inciting incident | Family taken | Survive, set out to rescue |
| Levels 1–7 | Solo/party | Get family back; sin-themed planetoids |
| Level 7 climax | Family back | True villain revealed, absorbs sins, flies off |
| Act 2 | Ruined homestead | Repair; day = defend, night = vanquish |
| Final boss | Death, enemy slain | Child succeeds, returns, starts family |
| Endgame | Roster + homestead | Build all, style home, generations, trade |
| Death (no heirs) | Game over | Restart tutorial; optional spirit/ancestry retention |

**Opening:** Player starts in a homestead with a family; tutorial covers resource collection, home building, magic, combat. Then the homestead is attacked and the family is taken; the player sets out to get them back.

**The 7 levels:** Each level is a themed planetoid aligned with one of the Seven Deadly Sins (Pride, Greed, Wrath, Envy, Gluttony, Lust, Sloth). Levels, factions, and encounters are shaped by that sin and its virtue counterpart. Planetoid generation is distinct per level, surface + layers, per-level PCG; Astroneer-inspired, non-deformable. See [PLANETOID_DESIGN.md](../PLANETOID_DESIGN.md) for details.

**Level 7 climax:** Player gets the family back; the true villain reveals themselves, absorbs the power of the sins, and flies off. Campaign shifts from “rescue the family” to “repair the world and confront the villain.”

**Act 2:** Player returns to a ruined homestead; repair and rebuild; by day keep home and family safe, by night vanquish the enemy. Day/night loop drives mid- and endgame.

**Final boss:** Player is defeated and dies but the enemy is slain. The player’s child takes over, defeats or seals the villain, returns to the homestead, and starts their own family. Succession: the next generation carries on.

**Endgame:** Finish homestead, style home, raise generations, trade, build a roster of characters with different playstyles. Completion, expression, and dynasty — not a single “win” state.

---

## Moral system: Seven Sins & Virtues

Skills, passives, and abilities are tied to the Seven Deadly Sins and their positive counterparts. Each pair is a **spectrum** from **-1** (sin) to **0** (neutral) to **+1** (virtue). **0** is shared (e.g. Trade for Greed/Generosity); **-1** and **+1** are commitment.

| Sin (negative) | Virtue (positive) |
|----------------|-------------------|
| Greed | Generosity |
| Gluttony | Abstinence |
| Sloth | Productivity |
| Wrath | Grace |
| Pride | Humility |
| Envy | Fulfillment |
| Lust | Love |

**In play:** Environments and factions in the 7 levels are shaped by these aspects. Player choices influence the player’s level on each axis. **+1 (virtue)** tends to give more loot, experience, and life; **-1 (sin)** gives strong short-term passives/abilities that become detrimental over time. Virtue = sustainable; sin = tempting but costly long-term.

---

## Death and succession

- When a character dies, that character becomes a **spirit** and is no longer playable. The player continues as one of their children (or another heir).
- If the player dies with no children, the game restarts from the tutorial. Some progress may be kept (spirit or ancestry buff system). Lost: homestead progression, family progression, that run’s character progression.

---

## Tech and stack (summary)

- **Engine:** Unreal Engine 5.7. Open World, World Partition.
- **Platform:** PC, Steam Early Access. No console in MVP.
- **World:** PCG biomes (forest first, then sand/crystal); portals/sublevels for realm-hop.
- **Combat:** GAS (3 skills Act 1; extend for needs/buffs in Act 2).
- **Building:** Snap/placement; build orders + family agents (Mass + State Tree + Smart Objects) in Week 2+.
- **AI:** Mass Entity + Mass AI (UE 5.7 recommended) for family/swarm agents; AHomeWorldAIController for actor-based NPCs.
- **Day/Night:** DaySequence; TimeOfDay subsystem stub.
- **Multiplayer:** Steam Sockets; 2p Week 2, up to 8p later.
- **Leaderboards:** Steam API or SteamLead; Weeks 3–4.

**Full stack (layers, phases, implementation status):** [STACK_PLAN.md](../STACK_PLAN.md).

---

## Scope lock

- **Engine:** 5.7 only.
- **Platform:** PC + Steam Early Access. Do not add engine or platform variants without team decision.
- **Campaign:** 8–12h; Act 1 solo (2–3h) → Act 2 duo (3–4h) → Act 3 full co-op (3–5h+).

---

**See also:** [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md), [STACK_PLAN.md](../STACK_PLAN.md), [SETUP.md](../SETUP.md), [KNOWN_ERRORS.md](../KNOWN_ERRORS.md).

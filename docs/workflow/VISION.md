# HomeWorld – Vision (Consolidated)

Single source for project theme, campaign narrative, moral system, and scope. Informs the [30-day schedule](30_DAY_SCHEDULE.md) and all task work.

---

## Theme and prototype

**"Love as Epic Quest"** – Dopamine from intense combat + Oxytocin from nurturing bonds. Players build and protect a life worth fighting for. Roles for casual (healer/home) and hardcore (protector) players. By day we nurture and build (physical world, horses, tools); by night our astral selves defend the land (spiritual world, spirit abilities, flight, monsters). See **Day and night: physical and spiritual worlds** below.

**Act 1 focus (Lone Wanderer):** Crash-land, scout biomes, fight bosses, claim home. Solo, 2–3h. Emotional beat: isolation → determination.

**Week 1 playtest goal:** Survive 3 missions: crash → scout → boss → claim home.

**Tech spine (Act 1):** PCG forest biome, GAS (3 skills), proc-gen realms, basic building. Free assets: FAB survival char, Quixel biomes.

**Success criteria:** First playable loop = explore → fight → build. No family or co-op yet.

---

## Demonstrable prototype and vertical slice

- **MVP (Minimum Viable Product):** Smallest playable version that validates the core promise (one compelling mechanic, minimal art/content). Goal: test fun and engagement early.
- **Vertical slice:** A short, complete section of the game at near-final quality: one clear gameplay loop, one memorable moment, and one polished "beautiful corner" to show capability. Used for stakeholders, playtesters, or funding.

**Campaign alignment:** The prototype is set in the **post–inciting incident** phase: the family has been taken; the player is the lone wanderer. Everything we build (explore, fight, build, claim home) is the first leg of the rescue — isolation → determination. "Claim home" = claiming a **new base of operations** (the homestead you build in the 30-day schedule), not the lost opening homestead. This is the foothold from which the player will go to Levels 1–7 to get the family back.

**Gate:** The **Week 1 playtest** (crash → scout → boss → claim home) is the prototype gate. Do not start Homestead/Family phases until explore → fight → build is playable and tested. **MVP tutorial gate:** The **one-day tutorial loop** (wake → breakfast → love task → game with child → gather wood/ore/flowers → lunch → dinner → bed → spectral combat → boss → wake to family taken) is the target for the MVP tutorial; see **Campaign summary** § MVP tutorial loop and [MVP_TUTORIAL_PLAN.md](MVP_TUTORIAL_PLAN.md).

**By end of 30 days:** Choose **one moment** (e.g. claiming the homestead after the first boss, or first family member rescued) and **one beautiful corner** (e.g. homestead compound) to polish for a showable vertical slice and/or short demo video.

**MVP full scope (Vision-aligned):** Everything in this Vision that applies to the prototype and MVP is to be developed for the MVP. In addition to the MVP tutorial loop, Week 1 playtest gate, and vertical slice (one moment + one corner), the **MVP includes**:

- **Packaged build** — Ship-ready packaged build (run or smoke-test) for demo/distribution.
- **Main menu (WBP_MainMenu)** — Main menu with Play, Character, Options, Quit; first-launch flow into game.
- **Full agentic building** — Family agents fulfilling build orders (State Tree/Blueprint flow; not console-only).
- **Astral-by-day** — Ability to enter the astral during the day (progression unlock or stub) as part of MVP scope.
- **Bed actor** — Bed or wake-up trigger in-world (not console-only for go-to-bed / wake).
- **In-world meal, love, and game triggers** — Player-triggered breakfast/lunch/dinner, love task with partner, and game with child in-world (not console-only); nurtures bonds and supports the day loop.

All other systems and content described in this Vision that touch the opening, tutorial, day/night, combat, conversion, planetoids, moral system, and Act 1 are also in scope for MVP development. The next 10 task lists focus on this endeavor; see [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md).

---

## Campaign summary

| Phase | Player state | Goal |
|-------|--------------|------|
| Opening | Homestead + family | Tutorial (resources, build, magic, combat) |
| Inciting incident | Family taken | Survive, set out to rescue |
| Levels 1–7 | Solo/party | Get family back; sin-themed planetoids |
| Level 7 climax | Family back | True villain revealed, absorbs sins, flies off |
| Act 2 | Ruined homestead | Repair; day = defend, night = convert (strip sin → loved) |
| Final boss | Death, enemy slain | Child succeeds, returns, starts family |
| Endgame | Roster + homestead | Build all, style home, generations, trade |
| Death (no heirs) | Game over | Restart tutorial; optional spirit/ancestry retention |

**Opening:** Player **starts with a family** (partner and homestead). The tutorial covers resource collection, home building, magic, and combat. **Creating your child:** You do not start with a child; you **create your child** by playing a **mini-game**: press the same **sequence of keys in a song-like pattern** (e.g. a short rhythm or melody of key presses). When you complete the pattern, the **child spawns** and joins the household. Then the homestead is attacked and the family is taken; the player sets out to get them back.

**MVP tutorial loop (one day to inciting incident):** The smallest playable MVP is **one full day and one night** in the homestead, ending when the player wakes to find the family taken. You **start with a family** (partner); you **create your child** by playing the **child-creation mini-game** (press a sequence of keys in a song-like pattern; when you match the pattern, the child spawns). The sequence is: **(1)** Wake up in your homestead (with partner). **(2)** Optionally create your child via the key-sequence mini-game. **(3)** Have breakfast (with family). **(4)** Complete one love task with your partner. **(5)** Play one game with your child (if created). **(6)** Collect some wood, mine some ore, pick some flowers. **(7)** Have lunch. **(8)** Have dinner. **(9)** Go to bed. **(10)** Spectral self — you go out into the world. **(11)** Combat with an encampment. **(12)** Beat the boss. **(13)** Night ends. **(14)** You wake up — **the family is taken**. That moment is the **end of the tutorial** and the start of the main campaign (lone wanderer, set out to get them back). All mechanics in this loop are **simple versions** for the MVP. **Handoff to Act 1:** Immediately after the tutorial ends (family taken), the player enters **Act 1 (lone wanderer)** — the phase where they set out to rescue the family; see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § After tutorial and [MVP_TUTORIAL_PLAN.md](MVP_TUTORIAL_PLAN.md) List 10 scope for verification. This loop validates the core promise: nurture by day (meals, love task, child, gathering), fight by night (astral, encampment, boss), then the inciting incident. Implementation is broken into a **10-step task-list plan**; see [MVP_TUTORIAL_PLAN.md](MVP_TUTORIAL_PLAN.md).

**The 7 levels:** Each level is a themed planetoid aligned with one of the Seven Deadly Sins (Pride, Greed, Wrath, Envy, Gluttony, Lust, Sloth). Levels, factions, and encounters are shaped by that sin and its virtue counterpart. Planetoid generation is distinct per level, surface + layers, per-level PCG; Astroneer-inspired, non-deformable. See [PLANETOID_DESIGN.md](../PLANETOID_DESIGN.md) for details.

**Planetoid and homestead:** When you arrive on a planetoid, **your homestead lands and appears on the planetoid**; that becomes your base there. You **venture out** from the homestead to explore, defend, and convert. **When you complete a planetoid** (clear its challenges, convert its foes, meet the goal for that level), you **move on to another planetoid** — the homestead lifts and travels to the next.

**Planetoid biomes and resources:** Planetoids use **four biomes** at the start: **desert, forest, marsh, canyon**. Each biome has its own **harvestable** (trees, flowers/herbs, rocks, water, spirits), **monster type**, and **dungeon type**. Each biome can appear in three **alignments**: **corrupted** (where you fight), **neutral** (where you harvest), and **positive** (where you empower yourself). Resource nodes include trees, flowers/herbs, rocks, water, and spirits. See [PLANETOID_BIOMES.md](../PLANETOID_BIOMES.md) for the full design.

**Level 7 climax:** Player gets the family back; the true villain reveals themselves, absorbs the power of the sins, and flies off. Campaign shifts from “rescue the family” to “repair the world and confront the villain.”

**Act 2:** Player returns to a ruined homestead; repair and rebuild; by day keep home and family safe, by night **convert** the enemy (strip sin → loved form). Day/night loop drives mid- and endgame. See **Day and night: physical and spiritual worlds** below.

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

## Day and night: physical and spiritual worlds

**Day – physical world:** We love each other and spend time together: working on the home, building, cooking food, playing, collecting resources, and socializing. The day is the **physical** world we interact with (not the spiritual). We ride horses and use tools. We collect **physical goods** (materials, food, supplies).

**Daytime mechanics and roles:** By day you split time between distinct activities that support the night. **(1) Support / healer / caretaker** — **Cooking and having meals** with your family; this restores what was lost and nurtures bonds. **(2) Explorer / builder** — **Collecting resources**, **building**, and **exploring the planetoid**; you gather materials and expand your home and reach. **(3) Child** — You **create your child** via a **mini-game**: press a **sequence of keys in a song-like pattern**; when you match the pattern, the **child spawns** and joins the household. After that you **take care of them** (play with them, keep them safe). The **goal of the day** is to **build up love** — through meals, care, building together, and the child — which **gives you bonuses that you use during the night** (stronger astral combat, better restoration, or other benefits). Love is the bridge between day and night. **MVP:** Simple version of the child-creation mini-game (short key sequence, song-like timing).

**Day as restoration:** Part of your **day** is to **restore what was lost in the astral**. Eating food, taking care of yourself and your family, and generally living a wholesome and loving life will **restore** health and other losses from the previous night’s astral combat — and can **grant buffs** for when you fight in the astral again. There is **no automatic health restore at dawn**; restoration and preparation for the next night happen through how you spend your day (meals, care, bonds, wholesome choices). That loop makes the day meaningful: the way you live by day directly strengthens you for the night.

**Night – spiritual world:** We go to bed and our **astral bodies** defend our land from evil spirits and monsters. This is the **combat** part of the game. The night is the **spiritual** world we interact with. We use **spirit abilities**, fly around, and defeat monsters and spirits. We collect **spiritual artefacts and power** at night. How well you spent the day (food, care, family, virtue) carries into the night as restoration and buffs.

**Combat mechanics scope:** We **avoid going too in-depth with combat mechanics** until we do a **full vision board pass** on them. Until then, **placeholder abilities, UI, and stubs are fine** — enough to support the night loop and progression feel, without locking in deep systems (e.g. detailed hit reactions, combo trees, weapon variety). Implementation should stay minimal and replaceable.

**Vanquishing foes (conversion, not killing):** We **do not kill** enemies. Combat **strips them of their "sin"** and **converts them to their "loved" version**. Once converted, former monsters can become **vendors**, **helpers**, **quest givers**, or **join the homestead as pets or workers**. This aligns with the sin/virtue spectrum: the goal is to redeem, not destroy.

**Night encounters (two-part structure and goal):** Night combat is designed in two parts. **(1) Waves at home** — A set of **waves** that spawn **against your home**; you and your family defend and **convert** attackers. **(2) Packs on the planetoid** — **Monsters spawn throughout the planetoid**; you **explore to find and convert** these packs (strip sin → loved form). **(3) Key interest places** — At **key points** on the planetoid there are **bigger monsters and bosses** you must **convert**. **Goal:** You have a **limited amount of time** each night. You split it between **defending** (waves at home) and **exploring** (packs + bosses on the planetoid). Success depends on **damage/output and strategy**. As you **progress**, you become **powerful enough to clear an entire planetoid in one night** — converting all foes so they can join you as vendors, helpers, quest givers, or homestead pets/workers.

**Combat variety (defend vs planetoid):** To keep variety and let you progress without building everything at once: **(1) Defend (waves at home)** — You have **defenses around your homestead**. You can use **ranged attacks** from those defenses, or **go on the ground** and use **area-of-effect (AOE) attacks**. **(2) Planetoid (away from home)** — Combat there leans on **combos** and **single-target damage**. That way defend and planetoid play feel different and you can specialize. **End-game aspirational:** Over time you can use either AOE or single-target in either situation; that flexibility is late-game progression, not required from the start.

**Astral death:** If we die while fighting in our astral body, we simply return to our body and wake up in the morning. There is no permanent death from night combat. What was lost (e.g. health) is then restored **during the day** through the activities above, not instantly at dawn.

**Outside homestead at night (physical world):** If the player is **outside their homestead when it is night**, the physical world becomes deadly: an **ancient ghost** hunts them and will **kill the player quickly**. The homestead is the safe place at night; venturing out in the flesh is punished. This creates a clear risk/reward: stay home and go to bed (astral combat) or risk death by staying out. **Late game:** The player can grow **strong enough to kill the ancient ghost** and **survive the night** while **still exploring** — so night exploration becomes possible after progression, at a cost (see below).

**Death away from home and wife’s resurrection:** If the player **dies** in that situation (killed by the ancient ghost outside the homestead at night), they are **sent back home** and their **wife (partner) resurrects them**. So death outside at night is a setback (return home, resurrection by partner), not permanent death. The bond with the partner is what brings the player back.

**Staying up (negative traits):** The more **days and nights** the player **stays up** (e.g. exploring at night instead of sleeping, or pushing through without rest), the more they **accrue negative traits**. So surviving the night and exploring is possible late game, but choosing to do it repeatedly has a long-term cost — aligning with the sin/virtue spectrum (short-term gain, then detriment).

**Death during the day:** There are no mechanics to die during the day; the day is safe in that sense. Later in the game we gain the ability to **enter the astral during the day** (progression unlock).

**Design rule:** For each action we take on the world, we define how it affects the world — good, bad, or in-between. **Bad** choices can earn a trait or ability that is beneficial temporarily but then has **negative side effects**. **Good** choices take longer to come into effect but are **permanent** and get **stronger over time**. This aligns with the sin/virtue spectrum above: virtue = slow, permanent, compounding; sin = fast payoff, then cost.

**MVP scope summary:** [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md) § Day/night and astral.

---

## Death and succession

- **Death outside homestead at night:** If the player is killed by the **ancient ghost** while outside the homestead at night, they are **sent back home** and **resurrected by their wife (partner)**. This is a setback, not permanent death; see **Day and night** § Outside homestead at night and Wife’s resurrection. Late game, the player can kill the ghost and explore at night but accrues **negative traits** the more they stay up.
- When a character dies (in contexts where resurrection does not apply), that character becomes a **spirit** and is no longer playable. The player continues as one of their children (or another heir).
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

# HomeWorld – Campaign & Moral Vision

Narrative arc, level structure, and moral-compass system that shape the full game. Complements the [Prototype Vision](PROTOTYPE_VISION.md) and [Roadmap](ROADMAP.md).

---

## Opening: Homestead & Tutorial

The player **starts in a homestead with a family** and has access to **mid-campaign features** from the beginning:

- Resource collection  
- Home building  
- Magic  
- Combat  

The **tutorial** is conducted in this context: the player learns these systems while living with the family in the homestead. This establishes the life that will be lost and later reclaimed.

---

## Inciting Incident: Family Taken

The homestead is **attacked** and the **family is taken**. The player is left alone and must set out to get them back.

---

## The 7 Levels: Sins & Planetoids

The player spends the **first 7 levels** getting the family back. Each level is a **themed planetoid** (or set of planetoids/environments) aligned with one of the **Seven Deadly Sins**:

1. **Pride**  
2. **Greed**  
3. **Wrath**  
4. **Envy**  
5. **Gluttony**  
6. **Lust**  
7. **Sloth**  

Levels, factions, and encounters are shaped by that sin’s theme and its positive counterpart (see Moral System below). For how these planetoids are generated (distinct identity per level, surface + layers, per-level PCG; Astroneer-inspired, non-deformable), see [PLANETOID_DESIGN.md](PLANETOID_DESIGN.md).

---

## Level 7 Climax: Family Returned, True Villain Revealed

On the **seventh level** the player defeats the last sin and **gets the family back**. The **true villain** then reveals themselves, **absorbs the power of the sins**, and **flies off**. The campaign shifts from “rescue the family” to “repair the world and confront the villain.”

---

## Act 2: Ruined Homestead & Day/Night Loop

The player returns to a **ruined homestead** and must:

- **Repair and rebuild** the home  
- **Venture out by day** to keep the home and family safe  
- **Venture out by night** to vanquish the enemy  

This day/night loop drives the mid- and endgame: defend by day, strike by night.

---

## Final Boss: Defeat & Succession

In the **final boss fight** the player is **defeated** and dies, but the **enemy is slain**. The player’s **child** takes over, defeats or seals the villain, and **returns to the homestead** to **start their own family**. The story closes with succession: the next generation carries on the legacy.

---

## Moral System: Seven Sins & Virtues

Skills, passives, and abilities are tied to the **Seven Deadly Sins** and their **positive counterparts**. Together they form a **moral compass** that affects rewards, abilities, and world state.

### Pairs (Sin vs Virtue)

| Sin (negative) | Virtue (positive) |
|-----------------|--------------------|
| Greed           | Generosity        |
| Gluttony        | Abstinence        |
| Sloth           | Productivity      |
| Wrath           | Grace             |
| Pride           | Humility          |
| Envy            | Fulfillment       |
| Lust            | Love              |

### Spectrum: -1, 0, +1

Each pair is a **spectrum** from **-1** (sin) to **0** (neutral) to **+1** (virtue):

- **0** is a shared neutral state that either side can move through.  
  Example: for Greed and Generosity, **0 = Trade**; both paths have access to trade, but context and rewards differ.
- **-1** and **+1** represent commitment to the sin or the virtue.

### How It Shapes the Game

- **Environments and factions** in the 7 levels and beyond are shaped by these aspects (e.g. a Greed-themed realm vs a Generosity-themed faction).
- **Factions** interact with each other and with the player according to these alignments.
- **Player choices** (dialogue, actions, builds) **influence the player’s level** on each axis.
- **Positive aspects (+1)** tend to give: **more loot**, **more experience**, **more life** (health/survival).
- **Negative aspects (-1)** give **passives and abilities** that are **strong in the short term** but **become detrimental over time** and eventually hurt the player.

So: virtue is rewarded with sustainable power and resources; sin is tempting but costly long-term.

---

## Endgame

After the main story, the player continues by:

- **Finishing the homestead** – build every structure, unlock all build options  
- **Styling the home** – cosmetic and layout choices  
- **Raising generations** of children  
- **Trading** with NPCs or other players through a **trade system**  
- Building a **roster of characters** with **different playstyles and abilities** that the player can switch between  

Endgame is about **completion, expression, and dynasty**, not a single “win” state.

---

## Death & Succession Rules

- **When a character dies**, that character becomes a **spirit** and is **no longer playable**. The player must continue as **one of their children** (or another heir).
- **If the player dies and has no children**, the game **restarts from the tutorial**.  
  - Some progress may be kept (e.g. **spirit** or **ancestry buff** system).  
  - **Lost**: homestead progression, family progression, and that run’s character progression.

So: lineage and heirs are the safety net; losing everyone means a full reset with possible meta-progression (spirits/ancestry).

---

## Summary Table

| Phase              | Player state        | Goal                          |
|--------------------|---------------------|-------------------------------|
| Opening            | Homestead + family  | Tutorial (resources, build, magic, combat) |
| Inciting incident  | Family taken        | Survive, set out to rescue    |
| Levels 1–7         | Solo/party          | Get family back; sin-themed planetoids |
| Level 7 climax     | Family back         | True villain revealed, absorbs sins, flies off |
| Act 2              | Ruined homestead    | Repair; day = defend, night = vanquish |
| Final boss         | Death, enemy slain  | Child succeeds, returns, starts family |
| Endgame            | Roster + homestead  | Build all, style home, generations, trade |
| Death (no heirs)   | Game over           | Restart tutorial; optional spirit/ancestry retention |

---

**See also:** [PROTOTYPE_VISION.md](PROTOTYPE_VISION.md), [ROADMAP.md](../ROADMAP.md), [STACK_PLAN.md](STACK_PLAN.md).

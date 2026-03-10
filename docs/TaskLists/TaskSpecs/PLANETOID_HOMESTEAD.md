# Homestead on planetoid: design

**Purpose:** Design for how the homestead lands on a planetoid, the venture-out loop, completion condition, and transition to the next planetoid. Per [VISION.md](../../../VisionBoard/Core/VISION.md) § Planetoid and homestead: "When you arrive on a planetoid, **your homestead lands and appears on the planetoid**; that becomes your base there. You **venture out** from the homestead to explore, defend, and convert. **When you complete a planetoid** (clear its challenges, convert its foes, meet the goal for that level), you **move on to another planetoid** — the homestead lifts and travels to the next."

**Scope:** Design doc only; no implementation required. Implementation may reference this doc when building planetoid flow, level streaming, and homestead placement.

**See also:** [PLANETOID_DESIGN.md](../PLANETOID_DESIGN.md) (proc-gen, sin themes), [NIGHT_ENCOUNTER.md](NIGHT_ENCOUNTER.md) (waves at home, packs on planetoid, key-point bosses), [VISION.md](../../../VisionBoard/Core/VISION.md) (campaign, day/night, conversion not kill).

---

## 1. Homestead landing on planetoid

When the player **arrives** on a planetoid (e.g. via portal from previous level, or start of level 1), the **homestead lands and appears** on that planetoid. That location becomes the player’s base for that level.

**Design options (to be chosen at implementation):**

- **Homestead as actor/blueprint:** Spawn or stream a "homestead" actor or blueprint at a designated **landing position** on the planetoid. Landing position can be: (a) a fixed spawn point in the level, (b) a tagged volume or actor (e.g. `HomesteadLanding`), or (c) derived from level config (e.g. near portal, or at a safe distance from key encounters).
- **Homestead as sublevel:** The homestead is a separate sublevel (e.g. Homestead_Pride) that streams in and is placed/positioned when the planetoid level loads. Placement can be a fixed offset from a level anchor or from the portal entry point.
- **Shared homestead asset:** The same logical "homestead" (buildings, family, state) is reused across planetoids; only its **world position** (and possibly orientation) changes per planetoid. Persistence (SaveGame) stores homestead state; level load places it at the landing position for the current planetoid.

**Outcome:** On arrival, the player has a clear "home" on the planetoid from which to venture out. Defend-at-night and "waves at home" use this location as the home reference (see [NIGHT_ENCOUNTER.md](NIGHT_ENCOUNTER.md)).

---

## 2. Venture-out loop

From the homestead, the player **ventures out** to explore, defend, and convert. This is the core loop while on a planetoid.

- **Explore:** Move across the planetoid surface (and optional layers). Discover POIs, resources, packs, and key points. Day: physical world (resources, building, care). Night: spiritual world (waves at home, packs on planetoid, key-point bosses); see [NIGHT_ENCOUNTER.md](NIGHT_ENCOUNTER.md) and [VISION.md](../../../VisionBoard/Core/VISION.md) § Night encounters.
- **Defend:** By night, waves spawn **at the homestead**; the player (and family) defend and **convert** attackers (strip sin → loved form). Conversion not kill; converted foes can become vendors, helpers, quest givers, or homestead pets/workers.
- **Convert:** Clear packs across the planetoid and key-point bosses by converting them (strip sin → loved). Progress is measured by how much of the planetoid is "cleared" (converted) and whether level goals are met.

**Loop summary:** Each day/night cycle, the player may rest and prepare at the homestead, then venture out to explore and convert. Over time, the player clears the planetoid and meets the **complete planetoid** condition below.

---

## 3. Complete planetoid condition

A planetoid is **complete** when the level’s goal for that planetoid is met. Design options (per level or global):

- **Key points cleared:** All designated key points (e.g. dungeons, shrines, bosses) have been cleared — e.g. boss converted, POI objective met. A simple implementation: a counter or set of flags (e.g. `KeyPoint_Pride_Boss`, `KeyPoint_Pride_Shrine`) that are set when the player converts the boss or completes the POI.
- **Boss converted:** The level’s main boss (or sin avatar) has been **converted** (strip sin → loved form). Once converted, the boss may become a vendor, helper, or quest giver; the level marks "boss defeated" for completion.
- **Goal met:** A level-specific goal (e.g. "rescue the captive," "convert all wave spawners," "reach the summit") is satisfied. Can be a single flag or a combination of sub-goals.

**Outcome:** When the complete condition is true, the game can trigger the **transition to next planetoid** (below). Persistence (SaveGame) should record per-planetoid completion so the player can resume and move on correctly.

---

## 4. Transition to next planetoid

When the player **completes** a planetoid, the homestead **lifts** and **travels to the next** planetoid. The player then starts the cycle again: homestead lands → venture out → complete → next.

**Design options:**

- **Level load:** Unload current planetoid level (and optional homestead sublevel); load the next planetoid level (e.g. Level 2 = Greed). Homestead is placed on the new level via the same "homestead landing" rules (§1). Portal or level-entry actor in the new level can represent "arrival."
- **Streaming:** If using World Partition or level streaming, stream out the current planetoid (or its chunks) and stream in the next planetoid. Homestead actor or sublevel is moved or respawned at the landing position in the new streamed level.
- **Narrative beat:** Optionally play a short "homestead lifts / travels" moment (e.g. camera, VFX, or transition screen) before loading the next level, so the fiction of "homestead travels to next planetoid" is clear.

**Order of levels:** The 7 levels are sin-themed (Pride, Greed, Wrath, Envy, Gluttony, Lust, Sloth). Progression is typically linear (Level 1 → 2 → … → 7), but design may allow optional order or backtracking; completion state per planetoid should support that.

**Outcome:** After transition, the player is on the next planetoid with the homestead landed and the venture-out loop available again. SaveGame should record current planetoid index (or level name) and per-planetoid completion so save/load and re-entry behave correctly.

---

## 5. Testing planetoid complete (manual verification)

To test the "planetoid complete → travel to next" flow before a console command exists:

1. **Complete condition (stub):** In PIE, treat "boss converted" or "key points cleared" as the trigger. Optionally use an existing console (e.g. `hw.Conversion.Test` multiple times, or defeat key-point boss placeholder by overlap) to simulate clearing the planetoid.
2. **Transition:** When the complete condition is met (per level design), the game would load the next planetoid level (see §4). Manual verification: use **Portal** or **Open Level** (e.g. from DemoMap to Planetoid level, or level-to-level) to simulate "travel to next."
3. **Sign-off:** Confirm (a) completion state is observable (e.g. log, HUD, or SaveGame flag when implemented), and (b) level transition (portal or `OpenLevel`) works so "homestead travels to next" can be wired to it.

When a console command (e.g. `hw.Planetoid.Complete` or `hw.CompletePlanetoid`) is added, it will set a completion flag or log "planetoid complete" for automated PIE testing; see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md). **pie_test_runner** includes an optional check **Planetoid complete (hw.Planetoid.Complete)** that runs the command in PIE and verifies GameMode `bPlanetoidComplete` is true; results appear in `Saved/pie_test_results.json`. To add or extend this check, see `Content/Python/pie_test_runner.py` (`check_planetoid_complete`) and CONSOLE_COMMANDS.md (Check names table).

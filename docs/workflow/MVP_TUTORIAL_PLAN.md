# MVP tutorial plan (10 task-list phases)

**Purpose:** Break the **one-day MVP tutorial loop** (wake → breakfast → love task → game with child → gather → lunch → dinner → bed → spectral combat → boss → wake to family taken) into **10 task-list phases**. Each phase is one 10-task list (T1–T10). Generate lists per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); run agents with `.\Tools\Start-AllAgents-InNewWindow.ps1`.

**Source:** [VISION.md](VISION.md) § Campaign summary (MVP tutorial loop), § Demonstrable prototype (MVP tutorial gate).

**Vision alignment:** You **start with a family** (partner). You **create your child** by playing a **mini-game**: press the **same sequence of keys in a song-like pattern**; when you match the pattern, the **child spawns**. MVP uses **simple versions** of all mechanics (meals, love task, child creation, gathering, combat, etc.). Child-creation mini-game is a **simple** key-sequence / rhythm input for MVP.

---

## The 13-step loop (reference)

| Step | Beat | Notes |
|------|------|--------|
| 1 | Wake up in homestead | Morning state, spawn in bed/home |
| 2 | Have breakfast | Meal with family, restore/buff |
| 3 | Complete one love task with partner | One task type, completion trigger |
| 4 | Play one game with child | One game type, child NPC present |
| 5 | Collect wood, mine ore, pick flowers | Harvest loop, inventory |
| 6 | Have lunch | Meal, time-of-day |
| 7 | Have dinner | Meal, time-of-day |
| 8 | Go to bed | Sleep trigger, transition to night |
| 9 | Spectral self — go out into world | Astral form, leave homestead |
| 10 | Combat with encampment | Night combat, convert/clear |
| 11 | Beat the boss | Boss encounter, night goal |
| 12 | Night ends | Return to body, dawn |
| 13 | Wake up — family taken | **End of tutorial**; inciting incident |

---

## MVP tutorial checklist (what must be playable)

Single reference for "what must be playable" for the MVP tutorial. Use when verifying the tutorial gate or generating the next task list.

| # | Step | Playable? | Notes |
|---|------|----------|-------|
| 1 | Wake up in homestead | ☐ | List 2: morning state + spawn at homestead; see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 2) verification. Optional in-world wake at bed (List 56): interact (E) at bed or overlap after night → Dawn; see § Tutorial (List 8) and (List 10) verification. |
| 2 | Have breakfast | ☐ | List 3: verified by **hw.Meal.Breakfast** (or **hw.ConsumeMealRestore**) in morning, or **in-world** — face actor with tag **Breakfast** (e.g. **BP_MealTrigger_Breakfast**), press **E** (Interact) or overlap; see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 3) verification and List 3 scope above. |
| 3 | Complete one love task with partner | ☐ | List 4: verified by **hw.LoveTask.Complete** in PIE, or **in-world** — face actor with tag **Partner**, press **E** (Interact); see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 4) verification and List 4 scope above. |
| 4 | Play one game with child | ☐ | List 5: verified by **hw.GameWithChild.Complete** in PIE, or **in-world** — face actor with tag **Child**, press **E** (Interact); see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 5) verification and List 5 scope above. |
| 5 | Collect wood, mine ore, pick flowers | ☐ | List 6: verified by harvest in PIE (face tree, E; confirm "Harvest succeeded - Wood +N" in log and Physical on HUD) or **hw.Goods**; see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 6) verification and List 6 scope above. |
| 6 | Have lunch | ☐ | List 7: verified by **hw.Meal.Lunch** (or **hw.Meal.Breakfast** / **hw.ConsumeMealRestore** a second time during day), or **in-world** — face actor with tag **Lunch** (e.g. **BP_MealTrigger_Lunch**), press **E** (Interact) or overlap; see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 7) verification and List 7 scope above. |
| 7 | Have dinner | ☐ | List 7: verified by **hw.Meal.Dinner** (or run meal restore a third time during day), or **in-world** — face actor with tag **Dinner** (e.g. **BP_MealTrigger_Dinner**), press **E** (Interact) or overlap; see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 7) verification and List 7 scope above. |
| 8 | Go to bed | ☐ | List 8: verified by **hw.GoToBed** or **hw.TimeOfDay.Phase 2**, or **in-world** — face bed, press **E** (Interact) or overlap bed trigger → Phase: Night; see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 8) verification and List 8 scope above. |
| 9 | Spectral self — go out into world | ☐ | List 9: verified by **hw.GoToBed** or **hw.TimeOfDay.Phase 2** (night), then HUD "Phase: Night", **hw.SpiritBurst** / **hw.SpiritShield**, and night encounter Wave 1 in Log; see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 9) verification and List 9 scope above. |
| 10 | Combat with encampment | ☐ | List 9: verified by **hw.GoToBed** or **hw.TimeOfDay.Phase 2** (night), then HUD "Phase: Night" and "Wave 1", night encounter Wave 1 (and 2/3) in Output Log; see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 9) verification and List 9 scope above. |
| 11 | Beat the boss | ☐ | List 9: verified by night (Phase 2), key-point boss placeholder if present, then **hw.GrantBossReward** (Wood); see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 9) verification and List 9 scope above. |
| 12 | Night ends | ☐ | List 9: verified by **hw.AstralDeath** (night → dawn + respawn); see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 9) verification and List 9 scope above. |
| 13 | Wake up — family taken (end of tutorial) | ☐ | List 10: "wake up" = dawn phase + player at spawn (existing after **hw.AstralDeath**). Verified by running **hw.AstralDeath** after night, then confirming HUD "Phase: Dawn" and player at start; see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 10) verification and List 10 scope below. |
| — | **Agentic building (List 60, MVP full scope)** | ☐ | Family agent claims and completes one build order. Verified by **hw.PlaceWall**, **hw.CompleteBuildOrder**, **hw.SimulateBuildOrderActivation**; see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Agentic building (List 60) verification and [AGENTIC_BUILDING.md](../tasks/AGENTIC_BUILDING.md). |
| — | **Astral-by-day (List 61, MVP full scope)** | ☐ | Enter astral during the day (stub or progression unlock). Verified by **hw.EnterAstral** or **hw.AstralByDay** (day → Night), then **hw.AstralDeath** (or F8) → phase restores to Day; see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Astral-by-day (List 61) verification and [ASTRAL_DEATH_AND_DAY_SAFETY.md](../tasks/ASTRAL_DEATH_AND_DAY_SAFETY.md) §3. |
| — | **Defend-at-night (List 62, MVP full scope)** | ☐ | Family at Defend when night (Phase 2); return at dawn (Phase 0/3). Verified by **hw.TimeOfDay.Phase 2** (night → family move to DefendPosition), **hw.TimeOfDay.Phase 0** or **3** (return to GatherPosition), **hw.Defend.Status**; setup: place_defend_gather_positions.py, Family-tagged actors. See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Defend-at-night (List 62) verification and [DAY12_ROLE_PROTECTOR.md](../tasks/DAY12_ROLE_PROTECTOR.md). |

**Linked from:** [README.md](README.md) Vision → task row (MVP tutorial loop).

---

## List 63 integration verification

**Purpose:** For List 63 (tutorial loop + Week 1 playtest + pre-demo in one or two sessions), use a single entry point for run order and where to record pass/fail.

**Run order and where to document:** Use [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § [List 63 integration](../CONSOLE_COMMANDS.md#list-63-integration-run-order-and-outcome-locations) for the **run order** (1. Tutorial loop single-session → 2. Week 1 playtest single-session → 3. Pre-demo checklist) and the **"Where to document results"** column for each run. Runs (1) and (2) can be done in one PIE session or two; (3) can run before or after. Recommended: pre-demo §3 first (level + PIE + pie_test_runner), then tutorial loop, then Week 1 playtest.

**Which checklists and commands:**

| Run | Checklist / procedure | Commands |
|-----|------------------------|----------|
| Tutorial loop | This doc: **MVP tutorial checklist** (13 steps above) | [CONSOLE_COMMANDS](../CONSOLE_COMMANDS.md) § Pre-demo verification (Tutorial List 2–10) and § Commands (hw.*) |
| Week 1 playtest | [CONSOLE_COMMANDS](../CONSOLE_COMMANDS.md) § Pre-demo verification — Week 1 playtest checklist (crash → scout → boss → claim home) | Same doc § Commands |
| Pre-demo checklist | [VERTICAL_SLICE_CHECKLIST §3](VERTICAL_SLICE_CHECKLIST.md#3-pre-demo-checklist-before-recording-or-showing) (steps 1–8: open DemoMap, PCG, PIE, pie_test_runner, Saved/pie_test_results.json) | Same doc § Commands |

**Where to record pass/fail:** Tutorial outcome → [SESSION_LOG.md](../SESSION_LOG.md) or [VERTICAL_SLICE_CHECKLIST §3](VERTICAL_SLICE_CHECKLIST.md#3-pre-demo-checklist-before-recording-or-showing). Week 1 playtest → SESSION_LOG or [DAY5_PLAYTEST_SIGNOFF § T1 verification](../tasks/DAY5_PLAYTEST_SIGNOFF.md#t1-verification-current_task_list--week-1-playtest-loop). Pre-demo checklist → SESSION_LOG or VERTICAL_SLICE_CHECKLIST §3.

---

## 10 task-list phases (high-level focus)

| List | Focus (one-line) |
|------|-------------------|
| **1** | Vision + plan: Integrate MVP tutorial loop into VISION; create this plan doc; workflow README link; vertical slice §4 ref; tutorial loop checklist; verification + buffer. |
| **2** | Wake up + homestead start: Morning state, spawn in homestead, time-of-day “morning”; optional bed/trigger. |
| **3** | Breakfast: Meal system stub (breakfast), family present at table, restore/buff hook. |
| **4** | Love task with partner: One love task type, partner NPC, completion trigger (counts toward “one love task done”). |
| **5** | Play game with child: One game type with child NPC, completion trigger. |
| **6** | Gather loop: Collect wood, mine ore, pick flowers — harvest, inventory, placement (or stub). |
| **7** | Lunch + dinner: Meals at midday and evening, time-of-day triggers. |
| **8** | Go to bed: Sleep trigger, transition to night (astral ready). |
| **9** | Spectral + combat + boss: Astral out, combat encampment, beat boss, night ends. |
| **10** | Wake up + family taken: Tutorial end trigger (family taken), inciting incident, handoff to Act 1 (lone wanderer). |

---

## List 2 scope: wake up in homestead

**Purpose:** Give the next list generator a clear target for List 2 (wake up + homestead start).

**What "wake up in homestead" requires:**

- **Morning state:** When the player starts the tutorial day (or loads into the homestead), the game is in "morning" — e.g. time-of-day set to morning, lighting/ambience appropriate.
- **Spawn in homestead:** Player character spawns inside the homestead (or at a designated spawn point / bed location), not in the open world.
- **Time-of-day "morning":** A minimal time-of-day system (or stub) that can represent "morning" so later steps (breakfast, lunch, dinner, bed) can hook into time progression.
- **Optional:** A bed or "wake up" trigger that transitions from "sleeping" to "morning" state; if time-boxed, a simple "start in morning at homestead" is sufficient for List 2. **Forty-first list:** Bed/wake-up placeholder is **deferred**; List 3 (breakfast) may reference the same actor when added (wake at bed → go to breakfast).

**Out of scope for List 2:** Full meal system, family NPCs, love tasks, gathering, night sequence — those are later lists.

**Verification (List 2 — morning at homestead):** One doc entry point for pre-demo and List 2 checks: [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Pre-demo verification links (1) the step-by-step run sequence → [VERTICAL_SLICE_CHECKLIST §3](VERTICAL_SLICE_CHECKLIST.md) and (2) the `hw.*` command reference (same doc). To verify "wake up in homestead": (1) Start PIE on DemoMap (or Homestead); (2) confirm time-of-day is morning — HUD shows "Phase: Day" or run `hw.TimeOfDay.Phase` (no arg) and confirm 0 in Output Log; (3) confirm player spawns at homestead (viewport or log). **In-world wake at bed (List 56):** After night (Phase 2), interact (E) at bed or overlap bed trigger → Dawn; see CONSOLE_COMMANDS § Tutorial (List 8) (bed placement) and § Tutorial (List 10) verification (wake steps). For the full pre-demo run and all commands, use CONSOLE_COMMANDS § Pre-demo verification.

---

## List 3 scope: breakfast

**Purpose:** Define how "family present at table" is satisfied for List 3 (breakfast) so the step is verifiable.

**What "family at breakfast" means for List 3:**

- **Family present at table** is satisfied when there are **actors in the level with the tag `Family`**. When you run **`hw.Meal.Breakfast`** (or `hw.ConsumeMealRestore`) during the day, the game counts all actors that have the **Family** tag; if at least one exists, the meal counts as "with family" and **MealsWithFamilyToday** increments. The HUD shows **"Meals with family: N"** during the day.
- **No separate "breakfast table" actor is required** for List 3 scope. A designer may later add a table volume or tag for placement; for verification, Family-tagged actors in the level are sufficient.
- **Restore/buff hook:** Breakfast (hw.Meal.Breakfast or ConsumeMealRestore) restores Health, sets day buff, and contributes to love; HUD shows Restored today, Love, and at night "Day buff: active". No code change required — existing path is used.
- **Verification:** See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 3) verification: run `hw.Meal.Breakfast` in morning with one or more Family-tagged actors in the level; confirm HUD shows "Meals with family: 1" (or higher) and Restored today ≥ 1; set night phase and confirm "Day buff: active".

**How to verify step 2 (have breakfast):** (1) Start PIE on DemoMap (morning; phase Day). (2) Run **`hw.Meal.Breakfast`** (or `hw.ConsumeMealRestore`) or **in-world:** face actor with tag **Breakfast** (e.g. BP_MealTrigger_Breakfast), press **E** (Interact) or overlap trigger. (3) Confirm HUD shows Restored today ≥ 1 and Love increased if family present (place Family-tagged actors first for "meals with family"). (4) Set **`hw.TimeOfDay.Phase 2`** (night) and confirm HUD shows "Day buff: active". For full steps (Family tag setup, optional actors, in-world breakfast), see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 3) verification.

---

## List 4 scope: love task with partner

**Purpose:** Define how "complete one love task with partner" is satisfied for step 3 so the step is verifiable. Covers what the love task is, how the partner is identified, how completion is triggered, and how to verify.

**What "complete one love task with partner" means:**

- **One love task type** is defined for the MVP tutorial: e.g. "Interact with partner" (press Interact near partner) or a console command **`hw.LoveTask.Complete`** for PIE verification. Completing it adds **Love +1** (AddLovePoints) and increments **LoveTasksCompletedToday** on PlayerState; the HUD shows **"Love: N"**. The counter resets at dawn (GameMode dawn logic). "One love task done" is satisfied when Love increased from the task or LoveTasksCompletedToday ≥ 1.
- **Partner** is the actor the love task targets; see "How the partner is identified" below.

**How the partner is identified (at least one of):**

- **Family subsystem role:** Assign the **Partner** role to a family member via `UHomeWorldFamilySubsystem::SetRoleForIndex(SpawnIndex, EHomeWorldFamilyRole::Partner)`. For example, spawn index 0 can be designated as the partner (first family spawn). Code or Blueprint can call `GetRoleForIndex(0)` and compare to `Partner` to find the partner.
- **Actor tag "Partner":** Any actor in the level with the tag **Partner** is treated as the partner. Use `UGameplayStatics::GetAllActorsWithTag(World, FName("Partner"), OutArray)` (or level designation) to find the partner actor for overlap/interact checks.
- **First Family-tagged actor:** If no role or Partner tag is set, the level designer can treat the **first Family-tagged actor** (e.g. first in GetAllActorsWithTag order or first spawn) as the partner. Document in level or config which actor is the partner.

**How completion is triggered:**

- **Console (PIE verification):** Run **`hw.LoveTask.Complete`** in PIE. No arguments. This adds Love +1 and increments LoveTasksCompletedToday; HUD and Output Log confirm. Use for step 3 verification without placing a partner actor.
- **Interact with partner (in-world):** The player presses Interact (E) near the partner actor (tag **Partner** or family role Partner); the same completion path (AddLovePoints + IncrementLoveTasksCompletedToday) runs. Implemented List 58 T3; placement via place_partner.py and partner_position in demo_map_config.json.

**Verification (List 4 — one love task done):** See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 4) verification. **Console:** (1) Start PIE on DemoMap (phase Day). (2) Run **`hw.LoveTask.Complete`**. (3) Confirm HUD shows "Love: N" increased and Output Log shows "love tasks today: 1" (or run again for 2, etc.). (4) Optional: confirm at dawn the counter resets. **In-world (List 58):** Place an actor with tag **Partner** (e.g. via place_partner.py), start PIE on DemoMap (phase Day), face the partner, press **E** (Interact); confirm HUD "Love: N" increased and Output Log "Love task (interact with partner) — one love task done". For full steps and placement, use CONSOLE_COMMANDS § Tutorial (List 4) verification.

---

## List 5 scope: play game with child

**Purpose:** Define one "play game with child" type for MVP tutorial step 4 so the step is testable. Covers what the game type is, how the child is identified, how completion is triggered, and how to verify.

**One game type (defined for List 5):**

- **Console command stub:** Run **`hw.GameWithChild.Complete`** in PIE. No arguments. This adds Love +1 and increments **GamesWithChildToday** on PlayerState; the counter resets at dawn. "Played one game with child" is satisfied when the player has run this command (or, when implemented, interacted with a child actor). Same pattern as List 4 (hw.LoveTask.Complete).
- **Future:** Interact (E) near child actor will call the same completion path (AddLovePoints(1) + IncrementGamesWithChildToday). Completion trigger wiring is in T3.

**How the child is identified (at least one of):**

- **Family subsystem role:** Assign the **Child** role to a family member via `UHomeWorldFamilySubsystem::SetRoleForIndex(SpawnIndex, EHomeWorldFamilyRole::Child)`. For example, spawn index 1 can be designated as the child (second family spawn). Code or Blueprint can call `GetRoleForIndex(SpawnIndex)` and compare to `Child` to find the child. Existing: [HomeWorldFamilySubsystem.h](../../Source/HomeWorld/HomeWorldFamilySubsystem.h) (SetRoleForIndex, GetRoleForIndex, EHomeWorldFamilyRole::Child); [DAY14_ROLE_CHILD.md](../tasks/DAY14_ROLE_CHILD.md) (Child behavior).
- **Actor tag "Child" or "Role_Child":** Any actor in the level with the tag **Child** or **Role_Child** is treated as the child. Use `UGameplayStatics::GetAllActorsWithTag(World, FName("Child"), OutArray)` (or "Role_Child") to find the child actor for overlap/interact checks.
- **For DemoMap / List 5:** Place at least one family member (e.g. Mass Spawner with MEC_FamilyGatherer, or a Family-tagged actor) and assign Child role to one of them via `SetRoleForIndex(Index, Child)` at runtime or via level Blueprint; or place any actor and add the tag **Child** (or **Role_Child**) so "play game with child" can target it when interact is implemented.

**How completion is triggered:**

- **Console (PIE verification):** Run **`hw.GameWithChild.Complete`** in PIE. No arguments. This adds Love +1 and increments GamesWithChildToday; HUD and Output Log confirm. Use for step 4 verification without requiring a child actor in the level.
- **Interact with child (in-world):** Implemented List 59 T3. The player presses Interact (E) near the child actor (tag **Child**); the same completion path (AddLovePoints(1) + IncrementGamesWithChildToday) runs. See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 5) verification for in-world steps and placement (create_bp_child_placeholder.py, place_child.py, child_position in demo_map_config.json).

**Verification (List 5 — one game with child):** See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 5) verification. **Console:** (1) Start PIE on DemoMap (phase Day). (2) Run **`hw.GameWithChild.Complete`**. (3) Confirm HUD shows "Love: N" increased and Output Log shows "games with child today: 1". (4) Optional: at dawn the counter resets (GameMode OnAstralDeath). **In-world (List 59):** Place an actor with tag **Child** (e.g. via place_child.py), start PIE on DemoMap (phase Day), face the child, press **E** (Interact); confirm HUD "Games with child: N" increased and Output Log "Game with child (interact with child) — one game with child done". For full steps and placement, use CONSOLE_COMMANDS § Tutorial (List 5) verification.

---

## List 6 scope: gather loop (wood, ore, flowers)

**Purpose:** Define how "collect wood, mine ore, pick flowers" (MVP tutorial step 5) is satisfied so the step is verifiable. **Single entry point:** [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Pre-demo verification links (1) [VERTICAL_SLICE_CHECKLIST §3](VERTICAL_SLICE_CHECKLIST.md) (run sequence) and (2) this scope; **Tutorial (List 6) verification** in CONSOLE_COMMANDS gives the PIE steps and console stubs for wood, ore, and flowers.

**What "collect some wood" means (T1):**

- **Harvest path:** TryHarvestInFront (GA_Interact, key E) hits an **AHomeWorldResourcePile** (e.g. **BP_HarvestableTree**) with **ResourceType** Wood; the game adds Wood to UHomeWorldInventorySubsystem and the HUD shows **Physical** (total physical goods).
- **Verification:** In PIE on DemoMap: (1) Face a harvestable tree (ResourceType Wood). (2) Press **E** (Interact). (3) Confirm Output Log shows **"Harvest succeeded (Physical) - Wood +N"** and HUD **Physical** count increases. **pie_test_runner** includes a **Harvest flow (PIE)** check when PIE is running (TryHarvestInFront or face tree + E).
- **If DemoMap has no trees:** Run **place_resource_nodes.py** with DemoMap open (Tools → Execute Python Script or MCP); it reads **demo_map_config.json** `resource_node_positions` and spawns **BP_HarvestableTree** at each position. No new code required if harvest path already works.

**What "mine some ore" means (T2):**

- **Harvest path:** Same as wood: TryHarvestInFront (E) hits an **AHomeWorldResourcePile** with **ResourceType** Ore (e.g. **BP_HarvestableOre**); the game adds Ore to inventory and the HUD shows **Physical**.
- **Console stub:** Run **`hw.Gather.Ore`** [*amount*] in PIE to add Ore to inventory (default 10) without harvesting. Use for step 5 verification when no ore node is in the level.
- **Verification:** In PIE: (1) Face **BP_HarvestableOre**, press **E**, and confirm "Harvest succeeded - Ore +N" and Physical count; or (2) run **`hw.Gather.Ore`** and confirm **`hw.Goods`** or HUD shows Ore. Create ore Blueprint with **create_bp_harvestable_ore.py**; place via **place_resource_nodes.py** (uses **resource_node_ore_positions** in demo_map_config.json).
- **See:** [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 6) verification.

**What "pick some flowers" means (T3):**

- **Harvest path:** Same as wood/ore: TryHarvestInFront (E) hits an **AHomeWorldResourcePile** with **ResourceType** Flowers (e.g. **BP_HarvestableFlower**); the game adds Flowers to inventory and the HUD shows **Physical**.
- **Console stub:** Run **`hw.Gather.Flowers`** [*amount*] in PIE to add Flowers to inventory (default 5) without harvesting. Use for step 5 verification when no flower node is in the level.
- **Verification:** In PIE: (1) Face **BP_HarvestableFlower**, press **E**, and confirm "Harvest succeeded - Flowers +N" and Physical count; or (2) run **`hw.Gather.Flowers`** and confirm **`hw.Goods`** or HUD shows Flowers. Create flower Blueprint with **create_bp_harvestable_flower.py**; place via **place_resource_nodes.py** (uses **resource_node_flower_positions** in demo_map_config.json).
- **See:** [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 6) verification.

**Verification (List 6 — gather step 5):** One doc entry point: [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § **Tutorial (List 6) verification** gives the PIE steps for wood, ore, and flowers (harvest E or console stubs **hw.Gather.Ore**, **hw.Gather.Flowers**); **hw.Goods** logs physical total. CONSOLE_COMMANDS also links [VERTICAL_SLICE_CHECKLIST §3](VERTICAL_SLICE_CHECKLIST.md) for the full pre-demo run sequence.

---

## List 7 scope: lunch + dinner

**Purpose:** Document when lunch and dinner are available and how to verify MVP tutorial steps 6–7.

**When lunch and dinner are available:**

- Lunch and dinner use the same **day-only** path as breakfast (ConsumeMealRestore). Time-of-day phases are **0** = Day, **1** = Dusk, **2** = Night, **3** = Dawn. There is **no midday/evening subdivision** for List 7 — run **`hw.Meal.Lunch`** and **`hw.Meal.Dinner`** whenever the phase is Day (or Dawn). For verification, "run both meal commands during day" is sufficient.

**How to verify steps 6–7:** (1) Start PIE on DemoMap and ensure phase is Day (**`hw.TimeOfDay.Phase 0`** if needed). (2) **Console:** Run **`hw.Meal.Breakfast`**, then **`hw.Meal.Lunch`**, then **`hw.Meal.Dinner`**. Or **in-world:** Face actors with tags **Lunch** and **Dinner** (e.g. **BP_MealTrigger_Lunch**, **BP_MealTrigger_Dinner**), press **E** (Interact) or overlap trigger — same effect as the meal commands. (3) Confirm HUD **"Restored today"** ≥ 3 and **"Meals with family: N"** (if Family-tagged actors exist). All use the same ConsumeMealRestore logic (Health, day buff, love). **In-world placement (List 57):** Create lunch/dinner Blueprints with **create_bp_meal_trigger_lunch.py** and **create_bp_meal_trigger_dinner.py**; place on DemoMap with **place_meal_triggers.py** (reads **lunch_position**, **dinner_position** in `Content/Python/demo_map_config.json`). See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § **Tutorial (List 7) verification** for full steps and command reference.

---

## List 8 scope: go to bed

**Purpose:** Define how "go to bed" (MVP tutorial step 8) is satisfied and how to verify so List 9 (spectral, combat, boss) can run.

**What "go to bed" means:**

- **Sleep trigger:** The player (or tester) triggers "go to bed" — either by running **`hw.GoToBed`** or **`hw.Sleep`** in the console, or **`hw.TimeOfDay.Phase 2`** to set phase to Night, or (when implemented) by interacting with a bed actor. Any of these sets time-of-day to **Night (Phase 2)** so the player "wakes" in astral / night phase.
- **Transition to night:** After the sleep trigger, `GetCurrentPhase()` returns Night (Phase 2), the HUD shows **"Phase: Night"**, Defend phase is active, and astral abilities (SpiritBurst, SpiritShield) and the night encounter (e.g. Wave 1 placeholder spawn) are available. No separate "wake in astral" step is required for List 8 — the transition to night is the gate.

**Bed actor (List 56):** The in-world bed is **BP_Bed** (`/Game/HomeWorld/Building/`). Create with **create_bp_bed.py**; place one instance in DemoMap with **place_bed.py** (open DemoMap, run script or MCP `execute_python_script("place_bed.py")`). Position from `demo_map_config.json` **bed_position**. T2 (List 56) wires in-world go-to-bed (interact or overlap) to the same effect as **hw.GoToBed**. For List 8 verification, **hw.GoToBed** or **hw.TimeOfDay.Phase 2** remains sufficient; bed actor is optional for step 8 verification.

**Out of scope for List 8:** Full spectral combat, encampment clear, boss encounter, night ends — those are List 9.

**Verification (List 8 — go to bed):** See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § **Tutorial (List 8) verification**. To verify step 8: (1) Start PIE on DemoMap (any phase). (2) **Console:** Run **`hw.GoToBed`** or **`hw.Sleep`** (or **`hw.TimeOfDay.Phase 2`**). (3) **In-world (List 56):** Face **BP_Bed**, press **E** (Interact) or walk into bed trigger → HUD shows **"Phase: Night"** (same effect as hw.GoToBed). (4) Confirm HUD shows **"Phase: Night"**. (5) Optional: run **`hw.SpiritBurst`** or **`hw.SpiritShield`** (if abilities granted) and confirm Output Log "activated"; confirm night encounter Wave 1 spawn in Log. For full steps and command reference, use CONSOLE_COMMANDS § Tutorial (List 8) verification.

---

## List 9 scope: spectral self, combat, boss, night ends

**Purpose:** Define how MVP tutorial steps 9–12 (spectral self, combat with encampment, beat the boss, night ends) are satisfied so they are verifiable. **Single entry point:** [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Pre-demo verification links (1) [VERTICAL_SLICE_CHECKLIST §3](VERTICAL_SLICE_CHECKLIST.md) (run sequence) and (2) the command reference; **Tutorial (List 9) verification** in CONSOLE_COMMANDS gives the PIE steps for steps 9–12.

**Step 9 — Spectral self / astral out:**

- **What "spectral self — go out into the world" means:** The player at **night (Phase 2)** is the "spectral self" — same character, not a separate astral actor. At night the player has **astral abilities** (SpiritBurst, SpiritShield), **astral HP** on the HUD, and the **night encounter** spawns (waves). "Go out into the world" is satisfied when phase is Night and the player can use astral abilities and face the night encounter.
- **Verification (step 9):** (1) Start PIE on DemoMap. (2) Run **`hw.GoToBed`** or **`hw.TimeOfDay.Phase 2`**. (3) Confirm HUD shows **"Phase: Night"**. (4) Run **`hw.SpiritBurst`** or **`hw.SpiritShield`** and confirm Output Log shows ability activation. (5) Confirm night encounter Wave 1 spawn in Output Log ("Night encounter Wave 1 — spawned placeholder"). See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § **Tutorial (List 9) verification** for full steps; steps 10–12 (encampment, boss, night ends) are documented in the same section below.

**Step 10 — Combat with encampment:**

- **What "combat with an encampment" means:** For List 9, **"encampment"** is the **night encounter** — waves of placeholder foes spawned at night (Phase 2). Defend phase is active; the GameMode spawns Wave 1, then Wave 2, then Wave 3 placeholders (see [NIGHT_ENCOUNTER.md](../tasks/NIGHT_ENCOUNTER.md)). Family moves to DefendPosition when implemented. "Combat with encampment" is satisfied when phase is Night and the night encounter waves spawn; the player can use astral abilities and (when implemented) convert/clear foes.
- **Verification (step 10):** (1) Start PIE on DemoMap. (2) Run **`hw.GoToBed`** or **`hw.TimeOfDay.Phase 2`**. (3) Confirm HUD shows **"Phase: Night"** and **"Wave 1"** (or higher). (4) Confirm Output Log shows "Night encounter Wave 1 — spawned placeholder" (and Wave 2/3 when triggered). (5) Optional: run **`hw.SpiritBurst`** or **`hw.SpiritShield`** to confirm combat-ready; **`hw.CombatStubs`** to log Defend combat mode. See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § **Tutorial (List 9) verification** for step 10.

**Step 11 — Beat the boss:**

- **What "beat the boss" means:** For List 9, the **boss** is a **key-point boss placeholder** — the GameMode can spawn one at night when **KeyPointBossSpawnDistance** > 0 (see [NIGHT_ENCOUNTER.md](../tasks/NIGHT_ENCOUNTER.md)). "Beat the boss" is satisfied when the player has defeated or converted that placeholder (or, for PIE verification, triggered the reward). The console command **`hw.GrantBossReward`** [*amount*] grants the boss reward (Wood) and is the verification stub for "boss beaten".
- **Verification (step 11):** (1) Start PIE on DemoMap. (2) Run **`hw.GoToBed`** or **`hw.TimeOfDay.Phase 2`** (night). (3) If a key-point boss placeholder is present (spawned when KeyPointBossSpawnDistance > 0), defeat or convert it; or skip to (4). (4) Run **`hw.GrantBossReward`** (default Wood +100) in the console. (5) Confirm Output Log shows "hw.GrantBossReward granted Wood +N" and **`hw.Goods`** or HUD shows Wood. See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § **Tutorial (List 9) verification** for step 11.

**Step 12 — Night ends:**

- **What "night ends" means:** For List 9, **night ends** when the astral phase ends and the player returns to dawn — either by **astral death** (defeat in combat) or by running **`hw.AstralDeath`** in PIE. The command advances time to Dawn and respawns the player at the level start (see [ASTRAL_DEATH_AND_DAY_SAFETY.md](../tasks/ASTRAL_DEATH_AND_DAY_SAFETY.md)).
- **Verification (step 12):** (1) Start PIE on DemoMap. (2) Run **`hw.GoToBed`** or **`hw.TimeOfDay.Phase 2`** (night). (3) Confirm HUD shows **"Phase: Night"**. (4) Run **`hw.AstralDeath`**. (5) Confirm HUD shows **"Phase: Dawn"** (or Day) and the player has respawned at start. See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § **Tutorial (List 9) verification** for step 12.

---

## List 10 scope: wake up + family taken

**Purpose:** Define how "wake up" (MVP tutorial step 13) is satisfied so step 13 is verifiable. **Single entry point:** [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Pre-demo verification links (1) [VERTICAL_SLICE_CHECKLIST §3](VERTICAL_SLICE_CHECKLIST.md) (run sequence) and (2) the command reference; **Tutorial (List 10) verification** in CONSOLE_COMMANDS gives the PIE steps for step 13.

**List 10 scope and verification (summary):** Step 13 means **wake at dawn** (after night ends) and **family taken** = **end of tutorial** and **inciting incident** for Act 1 (player sets out to get them back); **handoff to Act 1** = lone wanderer phase. **How to verify:** (1) PIE: run **`hw.GoToBed`** or **`hw.TimeOfDay.Phase 2`** (night), then **`hw.AstralDeath`** → confirm HUD "Phase: Dawn" and player at start ("wake up"). (2) Run **`hw.TutorialEnd`** or **`hw.FamilyTaken`** → confirm Output Log "Family taken — tutorial complete; inciting incident" and PlayerState `GetTutorialComplete() == true`. Full steps and command reference: [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § **Tutorial (List 10) verification** and § After tutorial.

**Step 13 — Wake up (after night ends):**

- **What "wake up" means:** For List 10, **"wake up"** is the state **after night ends**: the game is in **Dawn (Phase 3)** and the player has **respawned at the level start** (homestead). This is the **existing behavior** after **`hw.AstralDeath`** (or after astral death in combat): AdvanceToDawn runs, time goes to Dawn, and the player is respawned at start. No new code is required — "wake up" = dawn phase + player at spawn.
- **Verification (step 13 — wake up):** (1) Start PIE on DemoMap. (2) Run **`hw.GoToBed`** or **`hw.TimeOfDay.Phase 2`** (night). (3) Run **`hw.AstralDeath`**. (4) Confirm HUD shows **"Phase: Dawn"** (or Day) and the player has respawned at start. That state is "wake up" for step 13. See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § **Tutorial (List 10) verification** for full steps. **Automated:** `pie_test_runner` has `check_astral_death` for night → dawn + respawn.

**Family taken (tutorial end):** "Family taken" on wake-up is the **end of the tutorial** and the **inciting incident** for Act 1 (player sets out to get them back). Verification (flag or **hw.TutorialEnd**) is covered in List 10 tasks T2–T5. See also [VISION.md](VISION.md) § Campaign summary (MVP tutorial loop).

**Handoff to Act 1 (lone wanderer):** After "family taken" (tutorial end), the **next phase** is **Act 1** — the player is the **lone wanderer** and sets out to get them back. In PIE, run **hw.TutorialEnd** or **hw.FamilyTaken** to mark tutorial complete; the local player's PlayerState then has `GetTutorialComplete() == true`, which Act 1 logic (e.g. load Act 1 map, show objective: find family) can use when implemented. See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Tutorial (List 10) verification and § After tutorial.

---

## List 60 (MVP full scope): agentic building

**Purpose:** Document verification for **full agentic building** (MVP full scope List 60): family agent claims and completes one build order. This is not part of the 13-step MVP tutorial loop; it is list 6 of 10 in the MVP full scope (Vision-aligned). See [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md) List 60.

**What "family agent completes one build order" means:**

- **Build-order path:** An incomplete build order (e.g. BP_BuildOrder_Wall) is placed in the level; a family agent (State Tree BUILD branch or Blueprint flow) finds it, moves to the Smart Object (SO_WallBuilder), claims the slot, and completes the build (CompleteBuildOrder / bBuildCompleted). If State Tree graph editing is not automatable, the flow is documented so it is playable in PIE (manual State Tree BUILD branch or commands). See [AGENTIC_BUILDING.md](../tasks/AGENTIC_BUILDING.md) and [DAY10_AGENTIC_BUILDING.md](../tasks/DAY10_AGENTIC_BUILDING.md).

**Verification (List 60 — agentic building):** Single entry point: [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § **Agentic building (List 60) verification**. Commands: **hw.PlaceWall** (place build order at cursor), **hw.CompleteBuildOrder** (complete nearest incomplete build order), **hw.SimulateBuildOrderActivation** (simulate SO_WallBuilder activation). To verify in PIE: (1) With family agents: observe agent move to build order and build complete, or (2) commands-only: run **hw.PlaceWall** then **hw.SimulateBuildOrderActivation** (or **hw.CompleteBuildOrder**) and confirm build completes. Run sequence → [VERTICAL_SLICE_CHECKLIST §3](VERTICAL_SLICE_CHECKLIST.md#3-pre-demo-checklist-before-recording-or-showing); commands → CONSOLE_COMMANDS.

---

## List 61 (MVP full scope): astral-by-day

**Purpose:** Document verification for **astral-by-day** (MVP full scope List 61): enter astral during the day (stub or progression unlock). This is not part of the 13-step MVP tutorial loop; it is list 7 of 10 in the MVP full scope (Vision-aligned). See [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md) List 61.

**What "enter astral during day" means:**

- **Stub (MVP):** From Day or Dusk, the player can trigger **hw.EnterAstral** or **hw.AstralByDay**; phase becomes Night (astral mode). Return via **hw.AstralDeath** (or F8) restores **Day** (not Dawn), so day/night flow is consistent. See [ASTRAL_DEATH_AND_DAY_SAFETY.md](../tasks/ASTRAL_DEATH_AND_DAY_SAFETY.md) §3 (Day/time integration).

**Verification (List 61 — astral-by-day):** Single entry point: [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § **Astral-by-day (List 61) verification**. Commands: **hw.EnterAstral**, **hw.AstralByDay** (alias). To verify in PIE: (1) Set day (**hw.TimeOfDay.Phase 0**). (2) Run **hw.EnterAstral** or **hw.AstralByDay**. (3) Confirm HUD "Phase: Night" and Output Log "Enter astral during day". (4) Run **hw.AstralDeath** (or F8). (5) Confirm HUD "Phase: Day" and Output Log "Return from astral-by-day — phase restored to Day." Run sequence → [VERTICAL_SLICE_CHECKLIST §3](VERTICAL_SLICE_CHECKLIST.md#3-pre-demo-checklist-before-recording-or-showing); commands → CONSOLE_COMMANDS.

---

## List 62 (MVP full scope): Defend-at-night

**Purpose:** Document verification for **Defend-at-night** (MVP full scope List 62): when it is night (Phase 2), family (Family-tagged actors) move to DefendPosition-tagged actors; at dawn (Phase 0 or 3) they return to GatherPosition. This is not part of the 13-step MVP tutorial loop; it is list 8 of 10 in the MVP full scope (Vision-aligned). See [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md) List 62.

**What "Defend-at-night" means:**

- **Night (Phase 2):** GameMode **TryMoveFamilyToDefendPositions** teleports Family-tagged actors to DefendPosition-tagged actors. Observable in PIE: run **hw.TimeOfDay.Phase 2**; Output Log shows "moved N family actor(s) to DefendPosition (teleport)."
- **Dawn (Phase 0 or 3):** **TryReturnFamilyFromDefendAtDawn** teleports family back to GatherPosition-tagged actors (or offset). Run **hw.TimeOfDay.Phase 0** or **hw.TimeOfDay.Phase 3**; Output Log shows "Defend phase end (dawn)" and "moved N family actor(s) to GatherPosition (teleport)."
- **Setup:** Run **place_defend_gather_positions.py** (DefendPosition + GatherPosition); **place_partner.py** or **place_child.py** for at least one Family-tagged actor. See [DAY12_ROLE_PROTECTOR.md](../tasks/DAY12_ROLE_PROTECTOR.md) §2.

**Verification (List 62 — Defend-at-night):** Single entry point: [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § **Defend-at-night (List 62) verification**. Commands: **hw.TimeOfDay.Phase 0/2/3**, **hw.Defend.Status**. To verify in PIE: (1) Start PIE on DemoMap (setup above). (2) Run **hw.TimeOfDay.Phase 2** (night) → family move to Defend; confirm Output Log and viewport. (3) Run **hw.Defend.Status** to log phase, DefendActive, counts. (4) Run **hw.TimeOfDay.Phase 0** or **3** → family return at dawn; confirm Output Log. Run sequence → [VERTICAL_SLICE_CHECKLIST §3](VERTICAL_SLICE_CHECKLIST.md#3-pre-demo-checklist-before-recording-or-showing); commands → CONSOLE_COMMANDS.

---

## How to use

- **Generate list N:** Read this doc for phase N focus; read [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md) and [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) §0; fill [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md) with 10 tasks (7–8 implementation, 2–3 verification + buffer).
- **After list N completes:** Generate list N+1 (or next phase); run `.\Tools\Start-AllAgents-InNewWindow.ps1`.
- **After list 10:** MVP tutorial loop is complete; next focus per VISION (e.g. Week 1 playtest, Act 1 lone wanderer).

---

**See also:** [VISION.md](VISION.md), [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md), [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md).

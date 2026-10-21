# 42 - Home loop design

**Status:** APPROVED by Lead (Luke Thompson), 2026-10-20 ET. Host tests exist for bites 1-8 and 10. Bite 9 (pan/oven) and bite 8A (water/signs) are design-only. The companion party design and its first build are on main; this loop follows that work.
**Origin:** Cursor plan `home_loop_design_0a6799a6` ("Home loop design"), scribed here as the one owner.
**Picks:** home loop interview, 2026-10-20: `1A 2A 3A 4A 5A 6A 7A 8A`.
**Follow-up:** same day: `1A 2A 3A`.
**Water picks:** 2026-10-20: seven existing poles on the home-pool wisp; the plot wisp infuses the water; the cooked meal is a marked consumable.
**When to use:** Before any work on cooking stations, meal buffs, house dust, garden plots that grow food, or the water/sign path.

Mode: solo. State: decide. Transition: Concept -> Greybox.

This doc is the owner of the repeating home loop: cooking, cleaning, and the garden. Do not copy it into the virtue bible, the vision board, or the schema. The canon map keeps one pointer row. The opening tutorial, the night rescue, cloud-wisp jobs, nurture, and the companion party stay in their own files.

## 1. Scope in one paragraph

At dawn and at dusk the player is home, in body form, and can cook, clean, and tend plots. Food cooked there arms one buff for the next Day phase. Wisps from the healed task pool run a station, a plot, or a cleaning job. Seeds the player already gathers become kitchen food when a wisp grows them. Nothing in the game is killed for food. The opening midday kettle stays the sprint gate it is today.

## 2. What the picks decide

- **1A.** Home play happens in home time at dawn and at dusk, around the day trip.
- **2A.** Food gives a buff that lasts for one Day phase (stamina, glide, or gather speed are the examples).
- **3A.** Mistimed food still serves. The bonus is smaller. The ingredients are spent as the recipe names, and the meal is not thrown out.
- **4A.** The player assigns wisps to stations, plants, or cleaning from one shared pool.
- **5A.** Dust only shrinks a bonus. The buildup is capped. Stats do not fall below the unbuffed baseline.
- **6A.** Ingredients come from gathered seeds grown with wisps.
- **7A.** Kettle (MUST #2) is the first recipe, and it is the tutorial on the hearth pot.
- **8A.** This file is the design. The build follows the companion party and Lead's ask. Bites 1-8 and 10 are on main; bite 9 and 8A wait.

## 3. What the follow-up decides

These three picks close the interview that the plan left open. They use the same letters as section 2 and are a second list.

- **1A.** The home wisp pool is the healed task wisps. Cloud wisps stay on the wound and on fertilizer.
- **2A.** A serve arms a buff for the next Day phase. One slot. A later serve replaces the armed buff. The opening midday kettle stays today's sprint gate.
- **3A.** Dust scales only the armed food buff. With no meal armed, dust changes no stat.

### 2026-10-20 water follow-up

Luke picked the water direction on 2026-10-20:

- **Sign.** One of the seven existing poles on the healed home-pool wisp. Cloud wisps keep their jobs.
- **Water.** The plot wisp infuses the plot water; there is no separate mixing or watering verb.
- **Food.** The harvest and cooked meal carry the pole; the meal is a marked consumable under the virtue bible.

## 4. What stays in the other owners

This design sits beside locks it does not rewrite.

- **Opening kettle.** `TryBrewNodeKettleTea` in [HomeWorldCharacter.cpp](../Source/HomeWorld/HomeWorldCharacter.cpp) requires Day and body form, spends opening herb chunks (at most 10) or `RES_HERB`, and sets the sprint gate for `TeaSprintHalfDaySeconds` (60). The gate clears when the phase leaves Day. The quest line stays `Brew the kettle.` via `bKettleBrewed`. Fast-forward stops `kettle` and `station` keep that success. Follow-up 2A keeps this path for the opening day. Section 2's 2A applies to serves after the tutorial day.
- **One recipe on the tutorial island.** [OPENING_TUTORIAL_INTERVIEW.md](context/OPENING_TUTORIAL_INTERVIEW.md) round 5: cooking on that day is the kettle brew. Home time (section 2's 1A) is the repeating dawn and dusk loop. The opening brew stays at midday. Kettle is one ingredient, so its sync factor is full on its own. The sync lesson is the second recipe, and that recipe stays off the tutorial island.
- **Cloud wisps.** Cap 2. One heals the homestead wound. One mixes fertilizer with a dung. [HOMEWORLD_ROUTE.md](context/HOMEWORLD_ROUTE.md) and `CarriedCloudWisps` keep those jobs. Follow-up 1A is the other population: the 2026-10-19 restatement in the opening interview, where a healed wisp can be assigned to a task.
- **Virtue poles and marked consumables.** [VIRTUE_ATTRIBUTE_BIBLE.md](VIRTUE_ATTRIBUTE_BIBLE.md) owns the seven axes, the runes, and the Give, Swap, Nullify, and Take verbs. Section 10.1 uses those rules for water, plant, harvest, and meal. It adds no axis and no verb.
- **Six resources and two nurture targets.** [DO_NOT.md](canon/DO_NOT.md) and [SCHEMA.md](canon/SCHEMA.md). Food outputs are kitchen-chest items. Plots are a home-loop list. `N1_Crop` and `N2_Stored` stay the night sow. Recipe costs enter the schema when a build bite is asked for. [GATHER_CRAFT_BIBLE.md](GATHER_CRAFT_BIBLE.md) already names cottage cooking as a later track; this file is that track's design. `RECIPE_CAMPFIRE`, `RECIPE_TENT`, `RECIPE_TORCH`, `RECIPE_TAME_BAIT`, `RECIPE_HEAL_SALVE`, and `RECIPE_FISH_GEAR` stay as they are.
- **Care replaces killing.** [PILLARS.md](canon/PILLARS.md). The locked one-fish beat stays a fishing beat. `RECIPE_FISH_GEAR` stays gear. Tame bait stays berry or herb.
- **Dawn and dusk.** The 4–8 s figures in the schema are the NightMix fade. [DAYNIGHT_BIBLE.md](DAYNIGHT_BIBLE.md): the bed grants spirit form. Home time is body form during Dawn and during Dusk. A glide still does not start at dusk.
- **Companions.** [41_COMPANION_PARTY_DESIGN.md](41_COMPANION_PARTY_DESIGN.md). At home they live here. Their assist is follow presence on the day trip. Nights stay solo. Station help is wisps.
- **Glide and gather plugs today.** `SetGlideSpeedScale` carries the spirit-sickness slow and clamps at 1. Gather grants one unit on the interact. `UHomeWorldAttributeSet` holds Stamina and MaxStamina, and traversal does not spend them. The GDD forbids a flight energy meter. Named buffs point at these systems. This doc does not raise the glide clamp.

## 5. Stations

Each recipe names the prep station for each ingredient and the vessel that cooks it. The player can run a station. A wisp assigned to that station can run it too.

- **Sink.** Wash. Prep.
- **Cutting board.** Chop. Prep.
- **Hearth pot.** Vessel for pot recipes. Kettle cooks here. The kitchen counter stays the consumable station the opening already uses. The pot is the vessel on that hearth.
- **Stovetop.** Pan vessel. Its cook time is its own.
- **Oven.** Bake vessel. Its cook time is its own.
- **Garbage.** The player may discard a prepped piece or scraps. A mistimed meal still serves (section 2's 3A). Discard spends the piece the player chose to drop. Scraps add no dust.

On the tutorial island only the sink and the hearth pot take part in Kettle. The board, the stovetop, the oven, and the garbage stay inert until the player is past that day.

## 6. Recipe and timing

A cook runs in home time. Prep that is unfinished when the window ends carries to the next dawn or dusk window. A vessel that is still cooking when the window ends serves at the mistime factor.

The cook starts once every ingredient on the recipe is prepped and in the vessel. A missing ingredient means the cook waits. A mistime is an early or late finish among ingredients that are all in the vessel.

One ingredient has one finish time, so Kettle's sync factor is the full value. Kettle's steps are wash at the sink, then cook in the hearth pot.

The second named food row is a pot of herb and greens, two grown ingredients, started so both finish inside the sync window. It is off the opening fast-forward list. It is one more named row beside Kettle. `RECIPE_KETTLE` is the first food row and does not replace the campfire craft rows.

One meal slot is armed at a time. A later serve replaces whatever that slot holds.

## 7. Buffs

Follow-up 2A. A serve after the tutorial day arms the buff for the next Day phase.

- A dawn serve covers the Day phase that follows that dawn, the trip about to start.
- A dusk serve covers the Day phase that follows the next dawn.
- The slot holds one buff. Cooking again replaces it, including a dawn serve that replaces last dusk's meal.
- The buff clears when that Day phase ends, at the same phase change that clears the tea sprint gate.
- The buff does not carry into a second day, and it does not change spirit sickness, a bonk, or a stroke.

The opening midday kettle writes the existing sprint gate for the rest of that Day. It does not write the armed-buff slot.

Buff ids:

- **BUFF_STAMINA.** The first build that needs a visible stamina meal lengthens the sprint window on the Day the meal covers, because MaxStamina is unread. When a system reads MaxStamina, the same id can raise that maximum for the Day. Magnitudes are taste-pass placeholders in section 14.
- **BUFF_GLIDE.** The row exists. The descent keeps its current steering. The buff logs. A faster glide waits on a taste pass, because the current scale clamps at 1 and is the sickness slow.
- **BUFF_GATHER.** The row exists. Gather stays one unit per interact. The buff logs. A shorter gather waits until a gather has a duration. Yield stays one unit.

Follow-up 3A. Cleanliness multiplies the armed food buff and nothing else.

`FoodBuff = RecipeMagnitude * SyncFactor * CleanFactor`

SyncFactor is the full value or the mistime value. CleanFactor moves from the filthy floor up to 1 as dust clears. The product shrinks the meal's bonus. The character with no meal armed is the baseline, and dust does not push any stat under that baseline.

## 8. Wisp allocation

Follow-up 1A. During home time the player assigns healed task wisps, one wisp to one target.

- A station wisp runs that station's current task during the home window, then waits.
- A cleaning wisp clears one surface per home window. The player's own clean is the same action.
- A plot wisp stays on that plant through the day trip and through the night. Taking the wisp off the plant pauses growth. The plant keeps what it has already grown.
- The first pole on a plot wisp is the water sign in section 10.1. The assignment still counts as the one wisp on that plot.
- Those assignments leave `CarriedCloudWisps`, the wound heal, and the fertilizer mix alone.
- The night loop stays the night loop. Assignment is a home-time verb.

The pool is the wisps the 2026-10-19 restatement already describes: a damaged wisp healed at the hot springs, then carried and set to a task. This doc adds station, plot, and cleaning to the tasks that restatement allows. It does not choose how many of those wisps exist. That count stays the open line in the opening interview.

## 9. Dust

Each dawn, the floor and a capped list of props gain dust, up to a per-surface cap. Cleaning a surface sets that surface's dust to 0. Dust has no movement, camera, or family effect.

The clean factor is the only consumer. Section 7's formula and follow-up 3A are the rule. Counts and the filthy floor are taste-pass placeholders in section 14.

## 10. Garden

The player gathers `RES_SEED` on the existing day gather. During home time, one seed goes into one plot. A wisp on that plot grows it across home windows. The harvest is a kitchen-chest item. Chest item ids are `ITEM_HERB` and `ITEM_GREENS` for the prototype pair. They are not `RES_*` ids.

Until a kitchen chest exists, Kettle keeps spending `RES_HERB` or the opening herb chunks. After the chest exists, a post-tutorial Kettle can spend `ITEM_HERB` from that chest.

`TryPickGardenHerb` stays the opening garden pickup. Later kettle herbs come from the plot.

"Grow anything" means each food ingredient has a plot row. The prototype list is herb and greens. Plot count and growth length are taste-pass placeholders in section 14.

Nurture stays two targets. These plots are the home loop's garden, and the night sow stays N1 and N2.

### 10.1 Water and wisp signs

Lead pick, 2026-10-20. This path is post-tutorial and uses the home pool only.

- **Sign.** A healed task wisp carries the seven-axis poles the virtue bible already gives a character. The pole comes from the existing character spawn row or a hand set on a placed wisp; this doc adds no new table. The water path reads the wisp's first pole. A paradox wisp is out of scope for this pass. The rune is visible on the wisp.
- **Water.** The plot has water. The wisp on the plot is the mix: it infuses the plot water with its first pole as it grows the plant. The water is part of the plot, not a `RES_*` resource and not a carried item. There is no fill, container, carry, or watering verb. A virtue pole reads as purified water; a sin pole reads as tainted water; a wisp with no pole leaves the water neutral.
- **Plant.** The plot seed is unmarked `RES_SEED` in this pass. The water is the only source of the plant's pole. The plant carries one pole and takes the water's pole. The plot, water, and plant show the same rune. If the wisp is removed, growth pauses and the plant keeps the pole it has. If the wisp is replaced, the plant takes the new wisp's first pole and keeps its growth. This is the plot's set, not the herb Swap verb.
- **Harvest.** The harvest is the same kitchen-chest item, `ITEM_HERB` or `ITEM_GREENS`, with the pole. A marked item is one instance and does not stack with an unmarked item. The six `RES_*` ids do not change.
- **Meal.** A recipe that spends a marked ingredient carries the pole into the meal. The meal is a marked consumable under the virtue bible. The serve still arms the normal home-loop buff for the Day; the armed slot also carries the meal's pole. The serve is the use; there is no separate eat verb. The mark follows Give: if the player's matching axis is empty, the player takes the pole for the Day. If the axis already holds a pole, the mark does nothing; the buff still arms. Swap, Nullify, and Take stay herb and bench verbs. An unmarked meal arms the buff with no pole.
- **Duration.** The mark clears with the armed buff when the Day phase ends. A pole from another source stays. The one-Day duration is a taste-pass placeholder.
- **Read.** The mark is visible as the same rune. It is not a hidden stat line. What a pole on the player changes in an encounter stays with the virtue bible and the later encounter pass. This section does not name a new encounter demand.
- **Scope.** The first pass uses one marked ingredient per recipe. How two marked ingredients combine is not decided. A marked seed, a paradox wisp, and a second marked ingredient are out of scope until a later pick.
- **Owners.** Cloud wisps keep their jobs. `CarriedCloudWisps`, the wound heal, and the fertilizer mix do not change. The opening kettle and the tutorial day do not change.

## 11. Kettle migration

The opening path stays `TryBrewNodeKettleTea`.

The migration bite keeps the log line `NODE_KETTLE: tea brew`, `bKettleBrewed`, the quest text `Brew the kettle.`, and the same-day sprint gate for the opening. After the tutorial day, the same recipe id serves into the armed-buff slot under follow-up 2A.

Kettle uses the sink and the hearth pot. The opening day still has one recipe.

## 12. Data shape

The owner is `UHomeWorldHomeLoopSubsystem`. Stations, dust, plots, and the armed buff live there, beside the character's tea gate rather than inside it. No new subsystem is added by this doc.

- **FHomeWorldRecipe.** Id, vessel, buff id, ingredient rows.
- **FHomeWorldRecipeIngredient.** Chest item id, prep station, prep seconds, cook seconds.
- **FHomeWorldChestItem.** Kitchen-chest item instance. It keeps the `ITEM_*` id and gains a pole. A marked item does not stack with an unmarked one.
- **FHomeWorldWispAssignment.** Wisp id, and one target: station, plot, or surface.
- **FHomeWorldDustSurface.** Surface id, dust count.
- **FHomeWorldPlot.** Index, growth, crop item id, and the plant's pole. The assigned wisp's first pole is the source.
- **FHomeWorldArmedBuff.** Buff id, sync factor, clean factor, the meal's pole, and the Day phase it covers.

`RECIPE_KETTLE` is the first food id. The second id is `RECIPE_GREENS_HERB` (placeholder name). Vessels are Pot, Pan, and Oven. Station ids are Sink, Board, Pot, Stove, Oven, and Garbage.

Chest item ids stay out of the six-resource enum. Schema gains a food cost row only in the build bite that spends it.

## 13. DO_NOT rows this design amends

**None.**

- The water path adds no seventh resource, no watering-as-survival, no new morality axis, and no new verb. It uses the plot wisp, the existing virtue poles, and the serve action.
- The resource list stays six. Chest items are a station chest, the same idea as the opening's crafting chests.
- Nurture stays two targets.
- Named recipes stay a list. Two food rows are the start of that list for meals. Campfire craft rows stay.
- The bed is still the form change. Home time does not grant spirit.
- Cloud-wisp cap and jobs stay.
- Companion rules stay in Doc 41. Wisps do the housework.
- The opening fast-forward list gains no stop in this doc.

## 14. Taste-pass placeholders

Lead has not locked a duration or a magnitude. Every number in this section is a placeholder for a taste pass. A build uses them as written until that pass replaces them.

- Sink prep 4 s. Cutting board prep 6 s.
- Pan cook 8 s. Pot cook 10 s. Oven cook 14 s.
- Sync window ±1.5 s. Full sync factor 1. Mistime factor 0.5.
- Home window 90 s at dawn and 90 s at dusk. This length is the play window. The NightMix fade stays the schema's 4–8 s.
- Clean action 3 s, and it clears one surface. A cleaning wisp clears one surface per home window.
- Dust +1 on the floor and on each tracked prop at dawn. Up to 6 props. Cap 3 per surface.
- Clean factor 0.5 when every surface is at cap, and 1 when every surface is clear. Linear in between.
- Garden cap 4 plots. A planted seed is ready after 2 home windows with a wisp on it.
- The water path reads the wisp's first pole; a paradox wisp is out of scope for this pass.
- The meal's mark lasts the Day the armed buff covers. This is a placeholder.
- One marked ingredient per recipe; two marked ingredients are out of scope.
- The rune display on water, plant, harvest, and meal is a look pass.
- Stamina meal, full sync and a clear house: +60 s on the sprint window, or +20 MaxStamina once something reads it. Mistime uses half that magnitude before the clean factor.
- Glide and gather meals: magnitude unset. They log, and the current glide and gather stay as they are.

Worked example, all placeholders: a mistimed stamina meal in a filthy house is `60 s * 0.5 * 0.5` = 15 s of extra sprint on the Day it covers, and the unbuffed sprint rules still apply underneath.

## 15. Build order

Each bite is one shot, after the companion party, and only when Lead asks. Bites 1-8 and 10 are on main; bite 9 and bite 8A wait. Tea, quest, cloud-wisp, fertilizer, and nurture tests stay green at every bite.

1. Tags and logs for the six stations. No timers.
2. `RECIPE_KETTLE` data that still calls the current brew.
3. Prep and cook timers and the sync factor, Kettle only, with the opening sprint exception.
4. The armed-buff slot for a post-tutorial serve. It expires when the phase leaves Day.
5. Assign one healed task wisp to one station. The player can still run that station.
6. Dust, the clean action, and the clean factor on the armed buff.
7. One plot: seed in, wisp on it, chest item out, and a post-tutorial Kettle can spend it.
8. `RECIPE_GREENS_HERB` on the pot. Off the opening fast-forward.
8A. Water and wisp signs: the plot wisp's first pole marks the plot water and plant; the harvest and meal carry it; the armed buff carries it. No new resource and no new verb.
9. Pan or oven as a second vessel, with one recipe.
10. A second quest chain, id `home_loop`. `BuildOpeningSteps` gains no step.

## 16. Test plan

For those bites. Host tests use the prefix `HomeWorld.HomeLoop`.

- The opening kettle still gates sprint and sets `bKettleBrewed`, and the tutorial day still has one recipe.
- A mistime serves at the smaller factor. The spend matches the recipe. The meal is served.
- Dust at cap leaves every unbuffed stat on the baseline. With no meal armed, dust changes nothing.
- Assigning a task wisp leaves `CarriedCloudWisps` and the fertilizer mix unchanged.
- A plot harvest is a chest item. The six `RES_*` ids are unchanged. N1 and N2 tests stay as they are.
- An armed buff clears when the phase leaves Day and is absent on the following day.
- A later serve replaces the slot's previous buff.
- A plot wisp with a pole marks the plot water and plant; the harvest chest item carries the pole; a meal carries it; the armed buff carries it.
- A neutral wisp leaves the plant unmarked.
- A marked chest item does not stack with an unmarked item.
- A served marked meal still arms the buff; the mark follows Give and does nothing when the axis is occupied.
- The water path leaves `CarriedCloudWisps`, the six `RES_*` ids, and the one-wisp-per-target rule unchanged.

Quest-suite stops: `hw.Playtest.FastForward` stops `kettle` and `station` keep their current success. This doc adds no stop to that list. The opening chain still completes the kettle step on `bKettleBrewed`. The `home_loop` chain is stored beside it, so a home-loop update does not replace the opening tracker. The water path adds no fast-forward stop.

## 17. Out of scope

- No code, no schema edit, and no level edit in the scribe that added this file.
- No flight energy meter, no seventh resource, no third nurture target, and no recipe web.
- No water container, no `RES_WATER` id, no fill, carry, or watering verb, and no watering-as-survival.
- No new sin/virtue axis. The water path uses the seven axes.
- No marked seed, no paradox wisp, and no recipe with two different marked ingredients.
- No named encounter demand and no new effect for a pole on the player.
- No change to the one-fish beat, tame bait, or the campfire craft list.
- Where damaged wisps stand on the tutorial night is locked 2026-10-21: the copse, the pond, and the hot springs. The warehouse is not on that night. Node quality and its fit with the virtue marks stay open in the 2026-10-21 interview. The count of healed task wisps stays open.
- River, marsh, and lair travel stay where Doc 41 left them.

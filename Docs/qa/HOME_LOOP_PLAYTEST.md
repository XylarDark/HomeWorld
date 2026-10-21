# Home loop play-confirm

Desk check for [`Docs/42_HOME_LOOP_DESIGN.md`](../42_HOME_LOOP_DESIGN.md) bites 1-8 and 10. The design stays in Doc 42. This file does not add rules.

Automation: `.\Tools\RunTests.ps1 -Filter HomeWorld.HomeLoop`. A green run is not the desk pass. Lead fills the result line after seeing the step.

**State:** host tests exist for bites 1-8 and 10. The in-editor pass is blocked because the repo has no committed home-loop station or plot placement in `L_SizeTest`. Do not fill the Lead table from a green host run. The water/sign chain is design-only in Doc 42 section 10.1; it has no playable pass.

The opening kettle still uses the existing brew. The opening day still has one recipe. The six resources and the cloud-wisp jobs do not change.

## 1. Stations and the opening exception

**Setup.** Host test. When the stations are placed, stand at home on the opening day.

**Action.** Query the station ids, then inspect the four stations that are not part of Kettle.

**Expected.** Six ids in design order: Sink, Board, Pot, Stove, Oven, Garbage. On the opening day only Sink and Pot take part. The Board, Stove, Oven, and Garbage stay inert.

**Covers.** `HomeWorld.HomeLoop.StationIds`, `HomeWorld.HomeLoop.TutorialStationsInert`. The placed-station check is human only and waits on placement.

## 2. Kettle unchanged

**Setup.** Opening day, body, herb chunks or `RES_HERB`, and the kettle. Then a post-tutorial chest with `ITEM_HERB`.

**Action.** Brew the opening kettle. Then serve a post-tutorial kettle from the chest.

**Expected.** The opening brew sets `bKettleBrewed` and the same sprint gate. The opening day still has one recipe. The post-tutorial kettle can spend `ITEM_HERB` from the chest. The opening brew does not write the armed-buff slot.

**Covers.** `HomeWorld.HomeLoop.KettleStillBrews`, `HomeWorld.HomeLoop.OpeningSprintUntouched`, `HomeWorld.HomeLoop.KettleSpendsChestHerb`, `HomeWorld.HomeLoop.OpeningBrewSkipsSlot`.

## 3. Prep, cook, sync, mistime

**Setup.** Kettle only, at the sink and the hearth pot. When placed, the same steps in the world.

**Action.** Wash the herb, cook it, and let one run finish outside the sync window.

**Expected.** Sink prep is 4 seconds and pot cook is 10 seconds. Unfinished prep carries to the next home window. A mistimed meal still serves at the smaller factor. The spend matches the recipe.

**Covers.** `HomeWorld.HomeLoop.KettlePrepCook`, `HomeWorld.HomeLoop.PrepCarries`, `HomeWorld.HomeLoop.MistimeServes`. The pour and timing feel are human only and wait on placement.

## 4. Armed buff

**Setup.** A post-tutorial serve at dawn and at dusk.

**Action.** Serve once at each window, then serve a second meal over the first.

**Expected.** One slot. A dawn serve covers the Day that follows that dawn. A dusk serve covers the Day after the next dawn. A later serve replaces the slot. The buff clears when that Day ends. The opening midday kettle is not in this slot.

**Covers.** `HomeWorld.HomeLoop.ArmedBuffDawn`, `HomeWorld.HomeLoop.ArmedBuffDusk`, `HomeWorld.HomeLoop.ArmedBuffReplaces`, `HomeWorld.HomeLoop.ArmedBuffClears`.

## 5. Wisp assignment

**Setup.** One healed task wisp, one station, and any carried cloud wisps.

**Action.** Assign the task wisp to the station. Then run the station yourself.

**Expected.** One task wisp is on one target. The player can still run the station. `CarriedCloudWisps`, the wound heal, and the fertilizer mix do not change.

**Covers.** `HomeWorld.HomeLoop.WispStationAssign`, `HomeWorld.HomeLoop.WispLeavesCloudWisps`.

## 6. Dust and clean

**Setup.** Dawn dust, an armed meal, and no armed meal.

**Action.** Let dust reach the cap on one surface. Clean one surface. Compare the armed buff with a filthy house and with no meal.

**Expected.** Dust adds up to the cap. Cleaning clears one surface. The clean factor scales only the armed food buff. With no meal armed, dust changes no stat. At the cap, every unbuffed stat stays on its baseline.

**Covers.** `HomeWorld.HomeLoop.CleanClearsOne`, `HomeWorld.HomeLoop.CleanFactorScalesBuff`, `HomeWorld.HomeLoop.DustCapBaseline`, `HomeWorld.HomeLoop.DustWithoutMeal`.

## 7. Plot harvest

**Setup.** `RES_SEED`, one plot, and one task wisp on that plot.

**Action.** Plant the seed, wait two home windows, and harvest.

**Expected.** The harvest is a kitchen-chest item, `ITEM_HERB` or `ITEM_GREENS`. The six `RES_*` ids do not change. The night sow stays N1 and N2.

**Covers.** `HomeWorld.HomeLoop.PlotHarvestChest`, `HomeWorld.HomeLoop.ResourcesStaySix`.

## 8. Greens and herb

**Setup.** A post-tutorial pot and the two grown ingredients.

**Action.** Cook `RECIPE_GREENS_HERB` with both ingredients inside the sync window.

**Expected.** The second food row serves. It is off the opening fast-forward list. The opening day still has one recipe.

**Covers.** `HomeWorld.HomeLoop.GreensHerbOffOpening`, `HomeWorld.HomeLoop.GreensHerbSync`.

## 9. Quest log: the home_loop chain

**Setup.** Finish the opening day by sleeping at the bed. This does not need the home-loop stations placed.

**Action.** Look at the top-left tracker and run the host test for the stored chains.

**Expected.** The `Opening` chain is still stored. The `home_loop` chain is stored beside it with its four lines: `Cook the kettle.`, `Assign a wisp.`, `Clear one surface.`, and `Plant one seed.` The HUD draws one chain at a time, most recently changed. Note which one you see; the storage test is the host test.

**Covers.** `HomeWorld.HomeLoop.QuestChainBesideOpening`, `HomeWorld.Systems.Opening.QuestLog`. Note which chain you see. If the display hides the Opening chain in a way that blocks the night pass, file a defect.

## 10. Water and wisp signs — design only

**Owner.** [`Docs/42_HOME_LOOP_DESIGN.md`](../42_HOME_LOOP_DESIGN.md) section 10.1.

**Not built.** Do not fill a result row. When the 8A bite lands, check:

- A plot wisp with a virtue pole shows the same rune on the water and the plant. A sin pole reads as tainted. A wisp with no pole leaves the water neutral.
- The harvest `ITEM_HERB` or `ITEM_GREENS` carries the pole. A marked item does not stack with an unmarked one.
- A recipe with one marked ingredient carries the pole into the meal.
- The serve arms the normal buff and carries the pole. The player takes the pole when the matching axis is empty. When the axis already holds a pole, the mark does nothing and the buff still arms.
- The mark clears when the armed buff's Day ends.
- `hw.Virtue.Read` shows the pole. There is no hidden stat line.
- `CarriedCloudWisps`, the six `RES_*` ids, and the one-wisp-per-target rule do not change.

There is no water container, no `RES_WATER` id, no fill or carry step, and no watering-as-survival.

## Blocked in-editor pass

The repo has no committed home-loop station or plot placement yet. Steps 1-8 are host-tested and wait on that placement. Step 9 can be seen now at the bed. Step 10 waits on the 8A build.

When the placement lands, play the steps in order on `L_SizeTest`. Do not replay the passed tutorial day; the home loop is post-tutorial. Do not add a seventh resource.

## Result

| Step | Host test | Lead | Date | Sentence |
|---|---|---|---|---|
| 1 | `HomeWorld.HomeLoop.StationIds`, `TutorialStationsInert` | | | |
| 2 | `KettleStillBrews`, `OpeningSprintUntouched`, `KettleSpendsChestHerb`, `OpeningBrewSkipsSlot` | | | |
| 3 | `KettlePrepCook`, `PrepCarries`, `MistimeServes` | | | |
| 4 | `ArmedBuffDawn`, `ArmedBuffDusk`, `ArmedBuffReplaces`, `ArmedBuffClears` | | | |
| 5 | `WispStationAssign`, `WispLeavesCloudWisps` | | | |
| 6 | `CleanClearsOne`, `CleanFactorScalesBuff`, `DustCapBaseline`, `DustWithoutMeal` | | | |
| 7 | `PlotHarvestChest`, `ResourcesStaySix` | | | |
| 8 | `GreensHerbOffOpening`, `GreensHerbSync` | | | |
| 9 | `QuestChainBesideOpening` | | | |
| 10 | design only | | | |

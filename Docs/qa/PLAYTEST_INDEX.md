# Playtest index

One entry point. Play one pass, fill that pass's result, stop.

**Now:** Night on the island in [`TUTORIAL_PLAYTEST_QUEUE.md`](TUTORIAL_PLAYTEST_QUEUE.md). The November 20 critical path in that file is the master list. Party, home loop, and the water/sign chain stay separate and are off that path.

## Passes

| Pass | File | State | What it covers |
|---|---|---|---|
| November 20 critical path | [`TUTORIAL_PLAYTEST_QUEUE.md`](TUTORIAL_PLAYTEST_QUEUE.md#critical-path) | Master list. Now: Night. | Opening through the dawn glide, three field nodes, camp rescue, then dress, audio, and VFX. Passed tutorial results stay in that file. |
| Companion party | [`PARTY_PLAYTEST.md`](PARTY_PLAYTEST.md) | Built in #319 and #325. Desk sign-off waits on Lead. | Eight in-editor steps for the partner and child. Design stays in [`Docs/41_COMPANION_PARTY_DESIGN.md`](../41_COMPANION_PARTY_DESIGN.md). |
| Home loop | [`HOME_LOOP_PLAYTEST.md`](HOME_LOOP_PLAYTEST.md) | Host tests for bites 1-8 and 10. In-editor pass blocked on station and plot placement. | Stations, kettle, prep and cook, armed buff, wisp assignment, dust, plot harvest, greens, and the `home_loop` quest chain. Design stays in [`Docs/42_HOME_LOOP_DESIGN.md`](../42_HOME_LOOP_DESIGN.md). |
| Water and wisp signs | [`Docs/42_HOME_LOOP_DESIGN.md`](../42_HOME_LOOP_DESIGN.md) section 10.1 | Design only. No build and no pass. | Seven existing poles on the home-pool wisp, plot-water infusion, harvest, and marked meal. Cloud wisps stay out. |
| Movement island | [`TUTORIAL_ISLAND_PLAYTEST.md`](TUTORIAL_ISLAND_PLAYTEST.md) | Separate movement pass. | The `L_SizeTest` walk pad and the 450 cm/s walk. Not the tutorial day. |
| Opening quest preflight | [`QUEST_TESTS.md`](QUEST_TESTS.md) | Developer check. | The host preflight and the in-editor opening sweep. It does not fill a human pass table. |

## What is built

| System | State | Evidence |
|---|---|---|
| Opening tutorial day | Passed through the bonk. Night and the wisp loop are built and waiting on replay. The glider, the delivery, and the day-camp arrival have host tests. The clearing is not placed. | [`TUTORIAL_PLAYTEST_QUEUE.md`](TUTORIAL_PLAYTEST_QUEUE.md) |
| Companion party | Built. | `HomeWorld.Party` |
| Home loop | Bites 1-8 and 10 have host tests. Bite 9 (pan/oven) and the water/sign bite are not built. | `HomeWorld.HomeLoop` |
| Quest log | The Opening chain and the `home_loop` chain are stored beside each other. The HUD draws the most recently changed chain. | `HomeWorld.HomeLoop.QuestChainBesideOpening`, `HomeWorld.Systems.Opening.QuestLog` |
| Water and wisp signs | Design only. | [`Docs/42_HOME_LOOP_DESIGN.md`](../42_HOME_LOOP_DESIGN.md) section 10.1 |
| Glider | Host test. The October 26 play has not started. | [`TUTORIAL_PLAYTEST_QUEUE.md`](TUTORIAL_PLAYTEST_QUEUE.md#the-glider) |
| Delivery | Host test. The November 2 play has not started. | [`TUTORIAL_PLAYTEST_QUEUE.md`](TUTORIAL_PLAYTEST_QUEUE.md#delivery) |
| Day camp | Host test. The clearing is not placed. | [`TUTORIAL_PLAYTEST_QUEUE.md`](TUTORIAL_PLAYTEST_QUEUE.md#day-camp) |
| Dawn glide, night glide, stealth, ease, shrine | Fast-forward stops. Not human passes. The meadow, the clearing, the guards, and the shrine are not saved into the map. | [`TUTORIAL_PLAYTEST_QUEUE.md`](TUTORIAL_PLAYTEST_QUEUE.md#dawn-glide) |

## Do not

- Do not replay or overwrite the passed midday, crafting, dog, backpack, fishing, wisp, or bonk results.
- Do not treat a green host test as the human pass.
- Do not move the home loop into the tutorial day. It is post-tutorial.
- Do not treat the glider or delivery host test as the human pass. Do not test the water/sign chain as if it were built.
- Do not add a seventh resource or a watering-as-survival rule.

## Commands

```powershell
.\Tools\RunTests.ps1 -Filter HomeWorld.HomeLoop
.\Tools\RunTests.ps1 -Filter HomeWorld.Party
.\Tools\RunTests.ps1 -QuestCheck
npm run docs:links
```

## Owners

- Opening tutorial: [`Docs/context/OPENING_TUTORIAL_INTERVIEW.md`](../context/OPENING_TUTORIAL_INTERVIEW.md) and [`Docs/VISION_BOARD.md`](../VISION_BOARD.md).
- Party: [`Docs/41_COMPANION_PARTY_DESIGN.md`](../41_COMPANION_PARTY_DESIGN.md).
- Home loop and water: [`Docs/42_HOME_LOOP_DESIGN.md`](../42_HOME_LOOP_DESIGN.md).
- Clouds and wisps: [`Docs/43_CLOUDS_WISPS_DESIGN.md`](../43_CLOUDS_WISPS_DESIGN.md).
- Virtue poles and runes: [`Docs/VIRTUE_ATTRIBUTE_BIBLE.md`](../VIRTUE_ATTRIBUTE_BIBLE.md).

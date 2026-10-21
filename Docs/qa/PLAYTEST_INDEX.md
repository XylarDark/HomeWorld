# Playtest index

One entry point. Play one pass, fill that pass's result, stop.

**Now:** Night on the island in [`TUTORIAL_PLAYTEST_QUEUE.md`](TUTORIAL_PLAYTEST_QUEUE.md). The party and home-loop passes wait on Lead. The water/sign chain is design-only.

## Passes

| Pass | File | State | What it covers |
|---|---|---|---|
| Opening tutorial day | [`TUTORIAL_PLAYTEST_QUEUE.md`](TUTORIAL_PLAYTEST_QUEUE.md) | Now: night and wisp replay. Glider blocked. | Midday through the bed, night wisps, and the wisp loop. The passed midday, crafting, dog, backpack, fishing, wisp, and bonk results stay in that file. |
| Companion party | [`PARTY_PLAYTEST.md`](PARTY_PLAYTEST.md) | Built in #319 and #325. Desk sign-off waits on Lead. | Eight in-editor steps for the partner and child. Design stays in [`Docs/41_COMPANION_PARTY_DESIGN.md`](../41_COMPANION_PARTY_DESIGN.md). |
| Home loop | [`HOME_LOOP_PLAYTEST.md`](HOME_LOOP_PLAYTEST.md) | Host tests for bites 1-8 and 10. In-editor pass blocked on station and plot placement. | Stations, kettle, prep and cook, armed buff, wisp assignment, dust, plot harvest, greens, and the `home_loop` quest chain. Design stays in [`Docs/42_HOME_LOOP_DESIGN.md`](../42_HOME_LOOP_DESIGN.md). |
| Water and wisp signs | [`Docs/42_HOME_LOOP_DESIGN.md`](../42_HOME_LOOP_DESIGN.md) section 10.1 | Design only. No build and no pass. | Seven existing poles on the home-pool wisp, plot-water infusion, harvest, and marked meal. Cloud wisps stay out. |
| Movement island | [`TUTORIAL_ISLAND_PLAYTEST.md`](TUTORIAL_ISLAND_PLAYTEST.md) | Separate movement pass. | The `L_SizeTest` walk pad and the 450 cm/s walk. Not the tutorial day. |
| Opening quest preflight | [`QUEST_TESTS.md`](QUEST_TESTS.md) | Developer check. | The host preflight and the in-editor opening sweep. It does not fill a human pass table. |

## What is built

| System | State | Evidence |
|---|---|---|
| Opening tutorial day | Passed through the bonk. Night and the wisp loop are built and waiting on replay. The glider is not built. | [`TUTORIAL_PLAYTEST_QUEUE.md`](TUTORIAL_PLAYTEST_QUEUE.md) |
| Companion party | Built. | `HomeWorld.Party` |
| Home loop | Bites 1-8 and 10 have host tests. Bite 9 (pan/oven) and the water/sign bite are not built. | `HomeWorld.HomeLoop` |
| Quest log | The Opening chain and the `home_loop` chain are stored beside each other. The HUD draws the most recently changed chain. | `HomeWorld.HomeLoop.QuestChainBesideOpening`, `HomeWorld.Systems.Opening.QuestLog` |
| Water and wisp signs | Design only. | [`Docs/42_HOME_LOOP_DESIGN.md`](../42_HOME_LOOP_DESIGN.md) section 10.1 |
| Glider | Not built. | [`TUTORIAL_PLAYTEST_QUEUE.md`](TUTORIAL_PLAYTEST_QUEUE.md) |

## Do not

- Do not replay or overwrite the passed midday, crafting, dog, backpack, fishing, wisp, or bonk results.
- Do not treat a green host test as the human pass.
- Do not move the home loop into the tutorial day. It is post-tutorial.
- Do not test the glider or the water/sign chain as if they were built.
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

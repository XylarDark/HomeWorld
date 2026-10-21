# Quest coverage matrix

One row per opening beat, in sweep order. Regenerate with
`python Content/Python/run_quest_tests_host.py --coverage`
(or `Tools/RunTests.ps1 -QuestCoverage`); this file is the static
snapshot. The volatile column - latest result, from
`Saved/quest_tests.json` - lives in `Saved/quest_coverage.json` only,
so a run never changes what is committed here. An absent result is
`inconclusive`, never a pass.

Coverage is **declared** in [`Content/Python/quest_test_coverage.py`](../../Content/Python/quest_test_coverage.py):
nothing is inferred from test names. The preflight warns when a declared
test name no longer exists. An empty cell is a real gap, not an
oversight - see `fish`, which no automation drives today. Human
judgement stays in [`TUTORIAL_PLAYTEST_QUEUE.md`](TUTORIAL_PLAYTEST_QUEUE.md).

| # | beat (stop) | manifest checks | Declared C++ automation coverage | Human-only |
|---:|---|---|---|---|
| 1 | **spirit** (`spirit`) | `beat.ready_for == spirit`<br>`quest.spirit_claimed == False`<br>`actors.reveal.spirit_visible == True`<br>`beat.ready_distance <= 300` | `HomeWorld.Systems.Opening.ChildArrivesFirst`<br>`HomeWorld.Systems.Opening.ChildRaceRoute`<br>`HomeWorld.Systems.Opening.QuestLog` | sightline of the spirit approach (can you not see it from over the hill?)<br>the E prompt wording at the spirit |
| 2 | **herbs** (`herbs`) | `beat.ready_for == herbs`<br>`quest.spirit_claimed == True`<br>`quest.herbs_gathered == 0`<br>`actors.reveal.spirit_visible == False`<br>`beat.ready_distance <= 300` | `HomeWorld.Systems.Opening.QuestLog`<br>`HomeWorld.T0.ZoneGenerator.HerbSpacingAndPineCap` | trace-heart draw feel on the herb bed<br>hover prompt while aiming at the bed |
| 3 | **backpack** (`backpack`) | `beat.ready_for == backpack`<br>`quest.herbs_gathered == 20`<br>`quest.herb_tenths == 20`<br>`quest.herb_west == True`<br>`quest.herb_east == True`<br>`actors.reveal.partner_waiting == False`<br>`beat.ready_distance <= 300` | `HomeWorld.T0.NodeGate.BackpackBeatFiresFromTaggedProp`<br>`HomeWorld.T0.M4.InventoryGatedByBackpack`<br>`HomeWorld.T0.DayGates.RefuseAtDuskAndNight`<br>`HomeWorld.Systems.Opening.QuestLog` | the gift beat wording when the partner hands it over |
| 4 | **kettle** (`kettle`) | `beat.ready_for == kettle`<br>`actors.reveal.partner_waiting == True`<br>`quest.armor_gift == True`<br>`quest.kettle_brewed == False`<br>`quest.station_open == False`<br>`beat.ready_distance <= 260`<br>`actors.counter.east_face in [980, 990]`<br>`2D(actors.partner.location, actors.reveal.partner_stand) <= 80 cm` | `HomeWorld.T0.M2.TeaGateOffWithoutBrew`<br>`HomeWorld.T0.FL2.GardenPickThenTea`<br>`HomeWorld.T0.DayGates.RefuseAtDuskAndNight`<br>`HomeWorld.Systems.Opening.QuestLog` | counter hover and pour feel at the kettle |
| 5 | **station** (`station`) | `beat.ready_for == station`<br>`quest.kettle_brewed == True`<br>`quest.station_open == False`<br>`quest.mixed_herbs == 0`<br>`beat.ready_distance <= 260`<br>`actors.counter.east_face in [980, 990]`<br>`2D(actors.partner.location, actors.reveal.partner_stand) <= 80 cm` | `HomeWorld.Systems.Opening.QuestLog` | open-then-mix rhythm at the counter |
| 6 | **dog** (`dog`) | `beat.ready_for == dog`<br>`quest.station_open == True`<br>`quest.mixed_herbs >= 1`<br>`actors.dog.tamed == False`<br>`beat.ready_distance <= 700`<br>`2D(actors.partner.location, actors.reveal.partner_stand) <= 80 cm` | `HomeWorld.Systems.Stroke.GraceMatchesItsShape`<br>`HomeWorld.Systems.Stroke.WrongShapeMisses`<br>`HomeWorld.Systems.Stroke.HerbSpendsOnMatch`<br>`HomeWorld.Systems.Stroke.PawnInputRunsTheHold`<br>`HomeWorld.Systems.Opening.QuestLog` | Grace trace draw feel (the click gesture itself)<br>slow-approach pacing while the dog watches |
| 7 | **fish** (`fish`) | `beat.ready_for == fish`<br>`actors.dog.tamed == True`<br>`quest.fish_caught == False`<br>`quest.mixed_herbs == 0`<br>`beat.ready_distance <= 1200`<br>`2D(actors.partner.location, actors.reveal.partner_stand) <= 80 cm` | `HomeWorld.Systems.Opening.QuestLog` | the catch itself at the pond edge (E, one fish - no test drives it) |
| 8 | **sleep** (`sleep`) | `beat.ready_for == sleep`<br>`quest.fish_caught == True`<br>`quest.night_spirit == False`<br>`beat.ready_distance <= 260`<br>`2D(actors.partner.location, actors.reveal.partner_stand) <= 80 cm` | `HomeWorld.T0.M11.BedAtNightGrantsSpirit`<br>`HomeWorld.T0.M11.DayBedStaysBody`<br>`HomeWorld.Systems.Opening.NightWisp.DepositStartsHeal`<br>`HomeWorld.Systems.Opening.QuestLog` | the form shift as the night starts (camera and breath) |
| 9 | **night** (`(no argument)`) | `beat.ready_for == night`<br>`quest.night_spirit == True`<br>`actors.reveal.partner_waiting == True`<br>`tag NODE_OPENING_WISP count == 3`<br>`beat.ready_distance <= 260`<br>`actors.counter.east_face in [980, 990]`<br>`2D(actors.partner.location, actors.reveal.partner_stand) <= 80 cm` | `HomeWorld.Systems.Opening.NightWisp.DepositStartsHeal`<br>`HomeWorld.Systems.Opening.ChildArrivesFirst` | wisp glow readability from the bed<br>the partner's night line wording |
| 10 | **collect** (`collect`) | `beat.ready_for == collect`<br>`quest.night_spirit == True`<br>`quest.wisps_collected == 0`<br>`quest.wisps_carried == 0`<br>`tag NODE_OPENING_WISP count == 3`<br>`beat.ready_distance <= 400`<br>`2D(actors.partner.location, actors.reveal.partner_stand) <= 80 cm` | `HomeWorld.Systems.Opening.NightWisp.DepositStartsHeal`<br>`HomeWorld.Systems.Opening.NightWisp.DepositNeedsWisp`<br>`HomeWorld.Systems.Opening.NightWisp.DepositNeedsHerb` | the click-heart gesture on the aimed wisp |
| 11 | **heal** (`heal`) | `beat.ready_for == heal`<br>`quest.night_spirit == True`<br>`quest.wisps_carried == 3`<br>`quest.wisps_healed == 0`<br>`beat.ready_distance <= 520`<br>`2D(actors.partner.location, actors.reveal.partner_stand) <= 80 cm` | `HomeWorld.Systems.Opening.NightWisp.DepositStartsHeal`<br>`HomeWorld.Systems.Opening.NightWisp.DepositNeedsHerb`<br>`HomeWorld.Systems.Opening.NightWisp.DepositNeedsWisp`<br>`HomeWorld.Systems.Opening.NightWisp.DepositNeedsSpringRange` | the 20s heal wait feel and the healed wisp's follow arc |

Library sources for the declared names: `Source/HomeWorld/*Tests.cpp`.

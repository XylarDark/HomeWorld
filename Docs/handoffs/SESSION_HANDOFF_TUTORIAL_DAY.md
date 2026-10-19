# SESSION_HANDOFF_TUTORIAL_DAY

Slice: playtest the opening day and the night wisp loop on `L_SizeTest`.
Canon checked: `Docs/VISION_BOARD.md` Opening tutorial. Do not restate it.
Job confirmed: build + test
Scenarios the human accepted: sleep grants spirit form. The claimed companion stays and hovers. A click heart collects a world wisp. Night does not start an encounter or spiritual power regen.
Changed paths: `Source/HomeWorld/HomeWorldCharacter.*` (wisp collect and carry, hot-spring deposit and heal timers, leg followers, night tracker steps, `DebugFastForwardOpening`), `Source/HomeWorld/HomeWorld.cpp` (`hw.Night.Wisp`, `hw.Night.Heal`, `hw.Playtest.FastForward`), `Source/HomeWorld/HomeWorldWispPlacement.*` (`HeartPoint`, `MeasureBounds`), `Source/HomeWorld/HomeWorldRuneShapeComponent.cpp` (heart beside the object, rune ribbon outer). `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md` holds the pass. `Docs/level/L_SizeTest_CONTEXT.md` owns the E chain and the wisp rules.
Evidence: build 2026-10-19 13:27, `UnrealEditor-HomeWorld.dll` 2.69 MB. Live PIE 17:30: `hw.Playtest.FastForward test herb collection` logged `playtest_ff: 1 spirit claimed`, then `playtest_ff: ready for herbs` at `SM_Size_HerbBed_B` (player X=-420, bed X=-680, 260 cm). No `playtest_ff: 2 herbs gathered`. PIE ended; editor left on `L_SizeTest`. Earlier same day: build 11:43, `.\Tools\RunTests.ps1` 81 passed / 0 failed; `hw.Playtest.FastForward` ran all nine day beats and the wisp loop. Heart centers: 227 cm (west bed) and 222 cm (east bed) from the mesh centers, 35 cm clear of the face.
Human play: bonk passed 2026-10-18. Night sleep granted spirit. The wisp loop, the leg followers, the new heart placement, and `hw.Playtest.FastForward` are not play-confirmed.
Disclosed / not verified: the 20 s heal, one herb chunk per wisp, the 600 cm spring range, and the leg-follower arc are placeholder tuning. The follower look is unconfirmed by eye. Warehouse and delivery-route assignment are the next slice, not built.
Do not redo: midday, stations, dog, backpack, fish, wisp hover, bonk.
Next action: fresh PIE on `L_SizeTest`. `hw.Playtest.FastForward test herb collection` claims the spirit and places you at the east bed to draw the heart. No argument still stops at night. `list` prints spirit, herbs, backpack, kettle, station, dog, fish, sleep, night, collect, heal. Then play the Night and Wisp loop sections in `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`. Fill their results. Stop.

Read only:

1. `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md` through the Wisp loop section.
2. `Docs/level/L_SizeTest_CONTEXT.md` for the wisp and the E chain.

Map: `/Game/HomeWorld/Maps/SizeTest/L_SizeTest`. One `.\Tools\Safe-Build.ps1 -LaunchEditorAfter` from the repo root if code changes. Do not commit unless asked.

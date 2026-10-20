# SESSION_HANDOFF_PLAYTEST

Slice: the next playtest on `L_SizeTest`. The open queue pass is Night on the island, then the wisp loop.
Canon checked: `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md` Now line. Do not restate the vision.
Job confirmed: test
Scenarios the human accepted: sleep grants spirit form. The claimed companion stays and hovers. A click heart collects a world wisp. Night does not start an encounter or spiritual power regen. The cottage is the two-floor shell in `Docs/level/L_SizeTest_ROOM_PLAN.md`.
Changed paths, uncommitted on `main` after `4a910e48`: `Content/Python/cabin_shell.py`, `Content/Python/scene_placement.py`, `Docs/level/L_SizeTest_ROOM_PLAN.md`, `Docs/level/L_SizeTest_ISLAND_PLAN.md`, `Docs/level/L_SizeTest_METRICS.md`, `Content/HomeWorld/Maps/SizeTest/L_SizeTest.umap`, `Source/HomeWorld/HomeWorldCharacter.cpp` (fast-forward bed stop uses the bed's own height). Seven `MI_Greybox_*.uasset` files are editor resaves. Do not commit them with the cottage. Do not commit unless asked.
Evidence: apply 2026-10-20 04:41 logged `cabin walk enter cross exit clear`, `armory walk enter cross exit clear`, `opening dog staged with a clear approach lane`, `cabin lights 7`, and `saved top 45000.0`. The bed-height change is not in a new DLL. The last editor module was 2026-10-19 13:27, `UnrealEditor-HomeWorld.dll` 2.69 MB.
Human play: bonk passed 2026-10-18. Night sleep granted spirit before this cottage. The Night and Wisp loop result tables are empty. The windows, lights, couches, kitchen counter, upper porch, play room, and yard spacing are not play-confirmed. A night fast-forward was run on the old cottage and then the shell changed, so that session does not fill the queue.
Disclosed / not verified: 20 s heal, one herb chunk, 600 cm spring range, leg-follower arc. Warehouse and delivery routes are not this pass. The glider is not built.
Do not redo: midday, stations, dog, backpack, fish, wisp hover, bonk. Do not move the dog. Do not retune the tame.
Next action: one `.\Tools\Safe-Build.ps1 -LaunchEditorAfter` so the bed stop uses the upstairs height. Fresh PIE on `L_SizeTest`. No-argument `hw.Playtest.FastForward` plays the day beats and stops at night. `list` prints the other stops. Luke plays the Night section, then the Wisp loop. Fill only the section he finishes. Stop.

Read only:

1. `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md` through the Wisp loop section.
2. `Docs/level/L_SizeTest_CONTEXT.md` for the E chain.
3. `Docs/level/L_SizeTest_ROOM_PLAN.md` and `Docs/level/L_SizeTest_ISLAND_PLAN.md` if the cottage or the yard is the thing he is judging.

Map: `/Game/HomeWorld/Maps/SizeTest/L_SizeTest`. A beat test is `hw.Playtest.FastForward` plus the words he used. Pass is `playtest_ff: ready for <name>`. End PIE only after he has played. Do not commit unless asked.

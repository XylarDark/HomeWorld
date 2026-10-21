# SESSION_HANDOFF_PLAYTEST

Slice: the next playtest on `L_SizeTest`. The open queue pass is Night on the island, then the wisp loop.
Canon checked: `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md` Now line. Do not restate the vision.
Job confirmed: test
Scenarios the human accepted: sleep grants spirit form. The claimed companion stays and hovers. A click heart collects a world wisp. Night does not start an encounter or spiritual power regen. The cottage is the two-floor shell in `Docs/level/L_SizeTest_ROOM_PLAN.md`.
On `main` as of `5948ac69` (2026-10-20): the two-floor cottage and `L_SizeTest.umap` (`4a910e48`, `ad33f549`); the seven `MI_Greybox_*.uasset` resaves and the bed fast-forward stop (#315); the quest suite, contract, preflight, and coverage matrix (#315, #318, #320, #321); night wisp tests (#317); the companion party build (#319, design `Docs/41_COMPANION_PARTY_DESIGN.md`). Party invite hookup is in progress on its own branch.
Evidence: apply 2026-10-20 04:41 logged `cabin walk enter cross exit clear`, `armory walk enter cross exit clear`, `opening dog staged with a clear approach lane`, `cabin lights 7`, and `saved top 45000.0`. No editor DLL has been built from `5948ac69` yet.
Human play: bonk passed 2026-10-18. Night sleep granted spirit before this cottage. The Night and Wisp loop result tables are empty. The windows, lights, couches, kitchen counter, upper porch, play room, yard spacing, and the companion party are not play-confirmed.
Disclosed / not verified: 20 s heal, one herb chunk, 600 cm spring range, leg-follower arc. Warehouse and delivery routes are not this pass. The glider is not built.
Do not redo: midday, stations, dog, backpack, fish, wisp hover, bonk. Do not move the dog. Do not retune the tame.
Next action: `.\Tools\RunTests.ps1 -QuestCheck` (host only; exit 0). With Luke's yes to close the editor, one `.\Tools\Safe-Build.ps1 -LaunchEditorAfter`. Then `.\Tools\RunTests.ps1 -Quest -QuestOnly night,collect,heal` as the developer check. Fresh PIE on `L_SizeTest`, no-argument `hw.Playtest.FastForward` plays the day beats and stops at night. Luke plays the Night section, then the Wisp loop. Fill only the section he finishes. Stop.

Read only:

1. `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md` through the Wisp loop section.
2. `Docs/level/L_SizeTest_CONTEXT.md` for the E chain.
3. `Docs/level/L_SizeTest_ROOM_PLAN.md` and `Docs/level/L_SizeTest_ISLAND_PLAN.md` if the cottage or the yard is the thing he is judging.
4. `Docs/41_COMPANION_PARTY_DESIGN.md` only if he judges partner or child company.

Map: `/Game/HomeWorld/Maps/SizeTest/L_SizeTest`. A beat test is `hw.Playtest.FastForward` plus the words he used. Pass is `playtest_ff: ready for <name>`. End PIE only after he has played. Docs and Source merge after the tests pass (`AGENTS.md` § Locks). A `.uasset` or `.umap` commit waits for Luke's yes. Leave his uncommitted desktop files alone.

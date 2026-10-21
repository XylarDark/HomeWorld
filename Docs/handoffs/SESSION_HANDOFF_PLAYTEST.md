# SESSION_HANDOFF_PLAYTEST

Slice: the November 20 critical path in `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`. One open row, Luke plays, scribe his sentence, then the next row.
Canon checked: `Docs/qa/PLAYTEST_INDEX.md` and the Now line in that queue. Locks from 2026-10-21 are in `Docs/context/OPENING_TUTORIAL_INTERVIEW.md` under `## Already locked`. Do not restate them. Do not restate the vision.
Job confirmed: test
Scenarios the human accepted: the 2026-10-21 locks in that interview, including the heart placement and the passed aim box. Sleep grants spirit form. The claimed companion stays and hovers. A click heart collects a world wisp. Night does not start an encounter or spiritual power regen. The cottage is the two-floor shell in `Docs/level/L_SizeTest_ROOM_PLAN.md`. The sky stays the day sky while the phase is night.
On `main` as of `af2d904b`, plus uncommitted Source and docs from the 2026-10-21 night replay. Leave them in the tree. Do not revert them. The untracked `.agents/skills/source-command-*` folders are not this pass.
Evidence: the 12:39 DLL has `bDrawOpeningAimBox` false, so the aim frame is off. The editor was closed by that build and was not relaunched. The heal is still a flat 20 seconds and the click heart still ends at 3 seconds.
Human play, 2026-10-21, do not redo: the click-heart cursor (6.0; traces stay 4.8). The heart beside the prop, turning with the view, head height above the local floor, raised only to clear the floor and the prop. The trace height passed. The child does not follow at night. The body camera stayed (arm 400, field of view 90). The day sky stayed bright (`NightMix` 0). The quest list is the only SizeTest indicator: Night, Quests, and Carrying are separate blocks. Three wisps were collected and one was set to heal. The aim box passed (half-extent 0.3, center 0.5 above the middle of the view) and its frame is off in source.
Disclosed / not verified: the locked heal formula is not in the binary. The Night table has no sentence. A bed press has not been played; the shortcut calls `BeginOpeningNight`. Warehouse, delivery routes, node mods, and the glider are not this row.
Do not redo: midday, stations, dog, backpack, fish, wisp hover, bonk, the movement-island walk, the passed aim box, the heart height, the day sky, or the quest-list split. Do not move the dog. Do not retune the tame. Do not re-interview. Do not turn the aim frame back on. Do not implement the heal formula until the Night table has his sentence.
Next action: the October 22 row. `hw.Playtest.FastForward sleep`. He presses E at the bed. Fill the Night table. Then the October 23 row: put the locked heal in the binary and fill the Wisp loop table. Party, home loop, and the water/sign chain stay off this path.

Blocked, not this row: the glider, the dawn glide, the water and wisp-sign chain, home-loop station and plot placement.

Setup: `.\Tools\RunTests.ps1 -QuestCheck` (host only; exit 0). The aim-frame compile already landed. Launch the editor, do not rebuild, unless a later source change needs it. Then `.\Tools\RunTests.ps1 -Quest -QuestOnly night,collect,heal` as the developer check, not the pass. Fresh PIE on `L_SizeTest`. `hw.Playtest.FastForward sleep` stops at the bed, still to press. He plays. End PIE only after he has played. Leave the editor on `L_SizeTest`.

On the wisp loop, the binary's flat 20 second heal and the heart ending at 3 seconds are the behavior to record until the October 23 row changes the formula. Say that in the sentence.

Read only:

1. This file.
2. `## Critical path` and the Night section in `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`.
3. `Docs/qa/PLAYTEST_INDEX.md` for the pass order and its Do not list.
4. `Docs/level/L_SizeTest_CONTEXT.md` for the E chain, when the pass is Night or the wisp loop.
5. `Docs/context/OPENING_TUTORIAL_INTERVIEW.md` section `## Already locked` if a result seems to contradict a lock. Do not open the rounds to change them.
6. `Docs/level/L_SizeTest_ROOM_PLAN.md` only if he is judging the cottage or the yard.

Map: `/Game/HomeWorld/Maps/SizeTest/L_SizeTest`. A beat test is `hw.Playtest.FastForward` plus the words he used. Pass is `playtest_ff: ready for <name>`, the actor named in that line, and the skipped beat's success line absent. A green host test does not fill a human table. Docs and Source merge after the tests pass (`AGENTS.md` § Locks). A `.uasset` or `.umap` commit waits for Luke's yes. Leave his uncommitted desktop files alone. One `.\Tools\Safe-Build.ps1 -LaunchEditorAfter` per reply, and only after his yes to close the editor.

# SESSION_HANDOFF_PLAYTEST

Slice: the November 20 critical path in `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`. October 23 is one sitting of the open rows, in the Now-line order. Luke plays. One sentence per table.
Canon checked: `Docs/qa/PLAYTEST_INDEX.md` and the Now line in that queue. Locks from 2026-10-21 are in `Docs/context/OPENING_TUTORIAL_INTERVIEW.md` under `## Already locked`. Do not restate them. Do not restate the vision.
Job confirmed: test
Scenarios the human accepted: the 2026-10-21 locks in that interview, including the heart placement and the passed aim box. Sleep grants spirit form. The claimed companion stays and hovers. A click heart collects a world wisp. Night does not start an encounter or spiritual power regen. The cottage is the two-floor shell in `Docs/level/L_SizeTest_ROOM_PLAN.md`. The sky stays the day sky while the phase is night.
On `main` as of `af2d904b`, plus uncommitted Source and docs from the 2026-10-21 night replay. Leave them in the tree. Do not revert them. The untracked `.agents/skills/source-command-*` folders are not this pass.
Evidence: the 12:39 DLL has `bDrawOpeningAimBox` false, so the aim frame is off. The editor was closed by that build and was not relaunched. The heal is still a flat 20 seconds and the click heart still ends at 3 seconds.
Human play, 2026-10-21, do not redo: the click-heart cursor (6.0; traces stay 4.8). The heart beside the prop, turning with the view, head height above the local floor, raised only to clear the floor and the prop. The trace height passed. The child does not follow at night. The body camera stayed (arm 400, field of view 90). The day sky stayed bright (`NightMix` 0). The quest list is the only SizeTest indicator: Night, Quests, and Carrying are separate blocks. Three wisps were collected and one was set to heal. The aim box passed (half-extent 0.3, center 0.5 above the middle of the view) and its frame is off in source.
Disclosed / not verified: the Night table has no sentence. A bed press has not been played; the shortcut calls `BeginOpeningNight`. The locked heal is in the binary. The meadow is not placed.
Do not redo: midday, stations, dog, backpack, fish, wisp hover, bonk, the movement-island walk, the passed aim box, the heart height, the day sky, or the quest-list split. Do not move the dog. Do not retune the tame. Do not re-interview. Do not turn the aim frame back on.
Next action: October 23, one sitting, the order in the Now line of `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`. Fresh PIE each row. He plays. One sentence per table. Do not fill a table before the sentence. The locked heal is in the binary. Party, home loop, and the water/sign chain stay off this path.

The field shell, the three nodes, and the runs that need them wait on the meadow site. No coordinate is written. Do not place that site.

Setup 2026-10-22: `HomeWorld.Opening.LookCursor` passed. The twelve stops `sleep` through `shrine` passed in the editor. PIE has ended. The editor is on `L_SizeTest`. Do not rebuild unless a later source change needs it. End PIE only after he has played.

Read only:

1. This file.
2. The Now line in `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`, then the table for the row he just played.
3. `Docs/qa/PLAYTEST_INDEX.md` for the pass order and its Do not list.
4. `Docs/level/L_SizeTest_CONTEXT.md` for the E chain, when the pass is Night or the wisp loop.
5. `Docs/context/OPENING_TUTORIAL_INTERVIEW.md` section `## Already locked` if a result seems to contradict a lock. Do not open the rounds to change them.
6. `Docs/level/L_SizeTest_ROOM_PLAN.md` only if he is judging the cottage or the yard.

Map: `/Game/HomeWorld/Maps/SizeTest/L_SizeTest`. A beat test is `hw.Playtest.FastForward` plus the words he used. Pass is `playtest_ff: ready for <name>`, the actor named in that line, and the skipped beat's success line absent. A green host test does not fill a human table. Docs and Source merge after the tests pass (`AGENTS.md` § Locks). A `.uasset` or `.umap` commit waits for Luke's yes. Leave his uncommitted desktop files alone. One `.\Tools\Safe-Build.ps1 -LaunchEditorAfter` per reply, and only after his yes to close the editor.

# SESSION_HANDOFF_PLAYTEST_PREP

Slice: the ahead-of-play list in `Docs/context/PLAY_TASKS.md`, section `## Ahead of the plays`. One task, then the next. The November 20 dates stay in `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`. This file does not restate them.
Canon checked: that task table and `## Critical path` in the queue. Locks from 2026-10-21 stay in `Docs/context/OPENING_TUTORIAL_INTERVIEW.md` under `## Already locked`. Do not restate them. Do not restate the vision.
Job confirmed: test
Scenarios the human accepted: the November 20 critical path locked 2026-10-21. Prep is the code and the placed actors that let a later row be played. The Night pass is a different chat.
On `main` as of `af2d904b`, plus uncommitted Source and docs from the 2026-10-21 night replay. Leave them in the tree. Do not revert them. The untracked `.agents/skills/source-command-*` folders are not this pass.
Evidence: `HomeWorld.Opening.GliderCraft`, `HomeWorld.Opening.Delivery`, and `HomeWorld.Opening.DayCamp` passed 2026-10-21. `.\Tools\RunTests.ps1 -QuestCheck` exited 0. The queue sections are built and their tables are blank. The day-camp clearing is not placed. The heal is still a flat 20 seconds and the click heart still ends at 3 seconds. Camp, guard, and shrine actors are not in the played map.
Human play: not this pass. The Night table has no sentence. Do not fill it.
Disclosed / not verified: the editor may be open on `L_SizeTest` for the Night pass. A build that launches the editor closes it. This pass has not asked for that.
Do not redo: the Night pass, the aim box, the heart height, the day sky, the quest-list split, midday, stations, dog, backpack, fish, wisp hover, bonk. Do not implement the heal formula before the Night table has a sentence. Do not place cloud wisps. Do not build the shelved rows. Do not edit `Docs/handoffs/SESSION_HANDOFF_PLAYTEST.md` or the Night section of the queue.

Next action: the Night pass in `Docs/handoffs/SESSION_HANDOFF_PLAYTEST.md`. Press E at the bed, then one sentence in the Night table. Place tasks stay until that pass releases `L_SizeTest`. Do not fill the glider or delivery tables from the host tests.

Owned here: `Docs/context/PLAY_TASKS.md` section `## Ahead of the plays`, the prep source, and `Content/Python/quest_test_manifest.py`. `glider`, `delivery`, and `daycamp` are in that manifest. Dawn glide, stealth, ease, and shrine are not. `Source/HomeWorld/HomeWorldCharacter.cpp` is shared with the Night pass. A change that must land in that file waits until the Night sentence is in, unless the edit is task 1 or task 2 and it does not touch the aim box, the heart placement, or the heal constants.

Read only:

1. This file.
2. `## Ahead of the plays` in `Docs/context/PLAY_TASKS.md`. One open task.
3. `Docs/qa/QUEST_TESTS.md` section `## Add a quest`, when the task adds a stop.
4. `Docs/context/OPENING_TUTORIAL_INTERVIEW.md` section `## Already locked`, when a craft or a heal number is in question. Do not open the rounds to change them.

Map for a later place task: `/Game/HomeWorld/Maps/SizeTest/L_SizeTest`. Place tasks wait until the Night pass releases that map. A `.uasset` or `.umap` commit waits for Luke's yes. Docs and Source merge after the tests pass. One compile, and only after his yes to close the editor.

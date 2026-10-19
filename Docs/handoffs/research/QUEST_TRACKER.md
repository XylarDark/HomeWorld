# Quest tracker

2026-10-18. A basic quest list for development, until dialogue bubbles and audio carry the same steps.

Ask: how other games show quest progression, and what HomeWorld should draw in the meantime.

## Already recorded

[UE_GAMEPLAY_SYSTEMS.md](UE_GAMEPLAY_SYSTEMS.md) already says a new mechanic is not another branch on the interact ability. This file does not repeat that. The tracker is a list the HUD draws. It does not press E.

## Sources

Retrieved 2026-10-18.

- UESP, Skyrim: Quests. https://en.uesp.net/wiki/Skyrim:Quests
- Warcraft Wiki, Quest. https://warcraft.wiki.gg/wiki/Quest
- Epic Games, AHUD DrawHUD, Unreal Engine 5.8. https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/GameFramework/AHUD

## Practice

Skyrim keeps a journal of stages. One quest is active. The compass points at the current stage. Completed stages stay in the journal. The player is not shown every later stage on day one.

World of Warcraft keeps a quest log of objectives. An objective checks off when its count is met. The tracker shows the current objectives of the watched quest, not a paragraph of dialogue.

Both are a list with a current line. Speech and audio are a later skin on the same list. Valheim does not use this list. Its hints are spoken. That is the skin this tracker is standing in for, not the list itself.

Unreal does not ship a quest log. `AHUD::DrawHUD` is the draw this project already uses for top-left text.

## Reuse

KEEP: One component, `UHomeWorldQuestLog`, holds the chains. Several chains can be stored. The HUD draws only the most recently changed chain, at the top left. A done line stays, marked `[x]`. The current line is `[ ]`. A later line stays off that chain until the one before it is done. An unchanged rewrite does not take the screen. The log writes `quest:` only when the current line changes.

CANDIDATE: The opening on `L_SizeTest` is the first list. Spirit, then both herb beds to 20 chunks, then the kettle, then the dog. The words are built in `BuildOpeningSteps`. A miss does not add a chunk and does not move the partner.

KEEP: The observatory and research are not a quest. The pick is round 5 in [`OPENING_TUTORIAL_INTERVIEW.md`](../../context/OPENING_TUTORIAL_INTERVIEW.md).

PARK: Dialogue widgets, voice, map markers, and a second copy of the lines in the output log.

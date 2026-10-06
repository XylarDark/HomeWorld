# Session start

The one start door for HomeWorld, for desktop IDE agents and for the room seats alike (Lead interview #9, 1A 2A, 2026-10-05). `DISCOVERY_START.md` and `ROUTE_START.md` now only point here.

This works in any IDE, chat surface, CLI, or agent runner. If a capability is missing, say so instead of inventing an equivalent.

## Read order

Read one file per step. Start the next read only after the previous one returns.

1. UserHarness/docs/human-use/route-context.md
2. Docs/context/HOMEWORLD_ROUTE.md
3. UserHarness/docs/context/menu.md
4. The pack path your task needs, from the table below. Skip a path that does not exist on main yet.

| Task | Read |
|------|------|
| Level work (actors, positions, bounds) | `Docs/level/L_VS_MVP_Markers_manifest.json` |
| Test or prove work (commands, log tags) | `Docs/COMMANDS_AND_LOG_TAGS.md` |
| Anything with a number in it | `Docs/WORLD_METRICS.md` |
| Fix work | `docs/KNOWN_ERRORS.md` first. If the fix depends on level data, also `Docs/level/L_VS_MVP_Markers_manifest.json`; if that is not on main yet, wait for Conductor's actor scan. |

The developer names any extra files. Only those get read. The agent does not pick files, name a bite, or open a new chat.

## Ending the reads

If the opening message already names the task, start it. Otherwise ask one question, in the current conversation, and carry on from the answer.

## Shared development and token rules

These hold for every agent, desktop or room. They live only here. `AGENTS.md` § Session (the ~60k handoff, one significant write at a time, stop on changes you did not make) still applies and is not repeated.

1. One unknown at a time: one named contract, one change, one run, one score, then stop.
2. Handoffs are 5 to 10 lines plus paths: goal, paths, pass bar, what blocks it. No transcripts or full gate JSON in chat. Name only the active bite.
3. Second fail on the same writer parks for Lead. Do not open another retry.
4. Build working mechanics first, managers and architecture after.
5. Before any level option, packet, or fix that touches the level, scan the level actors first. Never work from assumed positions.
6. A route line about movement or space names the axis, the distance, and what is past the edge, and matches the GDD.
7. A placeable actor needs a scene root and a keep-transform check.
8. Docs-only work merges after Test PASS. Source or level work (`.umap`, `.uasset`) waits for a Lead yes after Test PASS.
9. A route or GDD sentence changes only after Lead says yes to that exact sentence.

## Session close

Do not stop the moment the current task is done. Close in this order, and do not reach a later step while an earlier one still has work in it.

1. Finish every piece of work the agent can do itself.
2. Ask, with the question tool, any question whose answer would let the agent continue. Carry on from the answer rather than closing.
3. Only when no agent work is left and the next step needs the developer's hands, ask whether a tutorial is wanted. Never offer one for agent-owned work.

The tutorial on offer is `Docs/qa/HUMAN_TUTORIAL.md`.

This file is the HomeWorld copy of the start and close rules in `route-context.md`. There is one start door now; where the two differ, this one wins.

If an unrelated second task appears, alert and stop.

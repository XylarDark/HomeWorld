# Session start

The one start door for HomeWorld, for desktop IDE agents and for the room seats alike (Lead interview #9, 1A 2A, 2026-10-05). `DISCOVERY_START.md` and `ROUTE_START.md` now only point here.

This works in any IDE, chat surface, CLI, or agent runner. If a capability is missing, say so instead of inventing an equivalent.

## Mode

Lead interview #12, 12A (2026-10-05).

1. Every session starts in solo mode.
2. A message that starts with `HANDOFF from HomeWorld Co`, or says `mode: co`, switches the session to Co mode. This works at any point, including in a session that started solo.
3. The session goes back to solo only when Lead says `mode: solo`.
4. Each time the mode is set or changes, say so in one line, for example `mode: solo (default)` or `mode: co (handoff header)`.
5. Only the wording changes between modes. The rules below, the read order, and the checks before any fix (search `docs/KNOWN_ERRORS.md` for the symptom first; the manifest or an actor scan before any change that depends on level data) are the same in both.
6. In both modes, name the state (`agent`, `decide`, or `do`) before acting, as `route-context.md` says. These are not Co words.

In solo mode, the wording rule covers what the agent writes, not what it reads. Pack files may use Co words. Read them as written, and use the solo wording below when talking to Luke. Don't write room-style handoffs.

| Co wording | Solo wording |
|------------|--------------|
| Lead's yes | Ask Luke directly for a yes |
| Test PASS or a Test score | Luke reviews the PR |
| Conductor's actor scan | Scan the level actors in this session first |
| Report back to HomeWorld Co | Report to Luke in this chat |

## Read order

Read one file per step. Start the next read only after the previous one returns.

1. UserHarness/docs/human-use/route-context.md
2. Docs/context/HOMEWORLD_ROUTE.md
3. Docs/WORLD_METRICS.md

These pack files are named here, not read at start. Open one only when the task needs it: `Docs/level/L_VS_MVP_Markers_manifest.json` (103 actors, verdict complete) when the task touches level data, and `Docs/COMMANDS_AND_LOG_TAGS.md` (generated, do not hand-edit) when it touches a console command or log tag.

Extra reads by task, after the pack:

| Task | Also read |
|------|-----------|
| Fix work | Search `docs/KNOWN_ERRORS.md` for the symptom and read only the matching entries, before any other work. To add a new entry (cause, then how to avoid it), open only the format header and the matching `###` section. Never load the whole file to read or to write. If the fix depends on level data, open the manifest named above. If that file is missing, scan the level actors in this session first. |

Beyond the reads above, the agent opens only files the developer names, the pack file the task needs (named above), or a file `AGENTS.md` requires before an edit (steer-gate before setting feel, scope, or done). It does not name a bite or open a new chat.

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
8. Docs-only work merges after the review passes (Co: Test PASS; solo: Luke reviews the PR). Source or level work (`.umap`, `.uasset`) waits for Lead's yes (solo: Luke's yes) after that.
9. A route or GDD sentence changes only after Lead says yes to that exact sentence.

## Handing work back to the room

Lead interview #14, 1A (2026-10-05). To bring work from a desktop session back to HomeWorld Co, Lead says `mode: co — hand back`. The session switches to Co mode (if it isn't already), says `mode: co (hand back)`, and writes one message that starts with `HANDBACK to HomeWorld Co`. Lead pastes that message into the room. It holds, in this order:

1. Main SHA the session last pulled.
2. Each PR: number, head SHA, merged or open, and what it waits for (Test score or Lead's yes).
3. Each item from the handoff: expected vs found, one line each. An item not started says `not started`.
4. Desk checks, only if Lead ran them: expected vs found.
5. Open questions for Lead, one line each, with no answer guessed.
6. Anything left uncommitted or unpushed, by path.

No transcripts, full logs, or gate JSON. Paths and SHAs only.

## Session close

Do not stop the moment the current task is done. Close in this order, and do not reach a later step while an earlier one still has work in it.

1. Finish every piece of work the agent can do itself.
2. Ask, with the question tool, any question whose answer would let the agent continue. Carry on from the answer rather than closing.
3. Only when no agent work is left and the next step needs the developer's hands, ask whether a tutorial is wanted. Never offer one for agent-owned work.

No tutorial is on offer yet. Offer `Docs/qa/HUMAN_TUTORIAL.md` only once it is committed and `Content/Python/human_tutorial.py --check` exits 0. Until then, step 3 names the next manual step in one line.

This file is the HomeWorld copy of the start and close rules in `route-context.md`. There is one start door now; where the two differ, this one wins. The pinned `route-context.md` (`afdcb0f`) already has the close section. Do not wait on another UserHarness SHA for it.

If an unrelated second task appears, alert and stop.

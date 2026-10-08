# Door rules

Opened with the task. Not a start read. The mode switch and the close order stay in `Docs/context/SESSION_START.md`.

## Wording

In solo mode, the wording rule covers what the agent writes, not what it reads. Pack files may use Co words. Read them as written, and use the solo wording below when talking to Luke. Don't write room-style handoffs.

| Co wording | Solo wording |
|------------|--------------|
| Lead's yes | Ask Luke directly for a yes |
| Test PASS or a Test score | Luke reviews the PR |
| Conductor's actor scan | Open the manifest named in the door. It is the actor scan |
| Report back to HomeWorld Co | Report to Luke in this chat |

## Rules

Rules that used to be 6–9 live in `Docs/context/LEVEL_RULES.md`. `AGENTS.md` § Session still applies and is not repeated.

1. One unknown at a time: one named contract, one change, one run, one score, then stop. A recorded queue of agent-owned items runs until a decide, a do, or a second fail on the same writer. A missing tool blocks only that item. When Luke has said to run that queue, that is the yes for the level items it names (`Docs/context/SESSION_START.md`).
2. Handoffs are 5 to 10 lines plus paths: goal, paths, pass bar, what blocks it. No transcripts or full gate JSON in chat. Name only the active task (Co: the active bite).
3. Second fail on the same writer parks for Lead. Do not open another retry.
4. Build working mechanics first, managers and architecture after.
5. Before any level option, packet, or fix that touches the level, open the manifest named in the door. That file is the actor scan. If it is missing, scan the level actors in this session first. Never work from assumed positions. Do not copy `counts.actors` or `completeness.verdict` into the door.

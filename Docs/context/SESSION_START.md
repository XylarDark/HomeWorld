# Session start

The one start door. The old discovery and route start files are removed.

This works in any IDE, chat surface, CLI, or agent runner. If a capability is missing, say so instead of inventing an equivalent.

## Mode

1. Every session starts in solo mode.
2. `HANDOFF from HomeWorld Co` or `mode: co` switches to Co mode.
3. Back to solo only when Lead says `mode: solo`.
4. Say the mode in one line when it is set or changes.
5. Name the state (`agent`, `decide`, or `do`) before acting. These are not Co words.
6. Open `Docs/context/DOOR_RULES.md` with the task. It holds the wording table and rules 1–5.

## Read order

Read one file per step. Start the next read only after the previous one returns.

1. UserHarness/docs/human-use/route-context.md through `## How to detect the state` only. Stop before `## Session close`. The close order lives in this file.
2. Docs/context/ROUTE_INDEX.md

Open only when the task needs it: `Docs/WORLD_METRICS.md` when the task uses a number; `Docs/level/L_VS_MVP_Markers_manifest.json` when it touches level data (read `counts.actors` and `completeness.verdict` from the file; do not copy them here); `Docs/COMMANDS_AND_LOG_TAGS.md` when it touches a console command or log tag.

| Task | Also read |
|------|-----------|
| Fix work | Search `docs/KNOWN_ERRORS.md` for the symptom. Read only the matching entries. Never load the whole file. If the fix depends on level data, the manifest named above is the actor scan. If it is missing, scan the level actors in this session first. |
| Descent, gather, or fertilizer | `Docs/context/HOMEWORLD_ROUTE.md` |
| Route, placeable, merge, or level | `Docs/context/LEVEL_RULES.md` |
| Hand back | `Docs/context/HANDBACK.md` only when Lead says `mode: co — hand back` |

## Ending the reads

If the opening message already names the task, start it. Otherwise ask one question and carry on from the answer.

Other doors are not start reads. Open one only when the developer names it, or when the question shows it is needed.

| Need | Door |
|------|------|
| Swarm command | `START_HERE.md` |
| Steer, taste, or test | `Docs/handoffs/SLICE_SESSION.md` |
| Conductor session | `swarm/SWARM_OPS.md` |
| Acceptance check | `Docs/handoffs/DISCOVERY_CONTEXT_ACCEPTANCE.md` |
| Cloud and glider handoff | `Docs/handoffs/CLOUD_GLIDER_ROUTE_CONTINUE.md` |
| Polish asset board | `docs/qa/POLISH_ASSET_BOARD_HOW_TO.md` |

## Session close

1. Finish every piece of work the agent can do itself.
2. Ask any question whose answer would let the agent continue. Carry on from the answer.
3. Only when the next step needs the developer's hands, ask whether a tutorial is wanted. Never offer one for agent-owned work.

No tutorial is on offer yet. Offer `Docs/qa/HUMAN_TUTORIAL.md` only once it is committed and `Content/Python/human_tutorial.py --check` exits 0. Until then, step 3 names the next manual step in one line.

This file wins where it differs from `route-context.md`. The pinned route-context already has the close section. Do not wait on a UserHarness SHA for it.

If an unrelated second task appears, alert and stop.

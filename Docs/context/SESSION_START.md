# Session start

The one start door. The old discovery and route start files are removed.

This works in any IDE, chat surface, CLI, or agent runner. If a capability is missing, say so instead of inventing an equivalent.

## Mode

1. Every session starts in solo mode.
2. `HANDOFF from HomeWorld Co` or `mode: co` switches to Co mode.
3. Back to solo only when Lead says `mode: solo`.
4. Set the header once on the first message: `Mode: solo · State: agent`. Restate it only when the mode or state changes.
5. State is `agent`, `decide`, or `do`. These are not Co words. Name it before acting.
6. Open `Docs/context/DOOR_RULES.md` with the task. It holds the wording table and rules 1–5.

## Context loss

If the server restarts or the transcript is lost, re-read only this file, restate the mode/state header once, and do not re-run the start question.

## Read order

Read one file per step. Start the next read only after the previous one returns.

1. UserHarness/docs/human-use/route-context.md — the whole file. This file wins where it differs on the close order.
2. Docs/context/ROUTE_INDEX.md

Open only when the task needs it: `Docs/WORLD_METRICS.md` when the task uses a number; `Docs/level/L_VS_MVP_Markers_manifest.json` when it touches level data (read `counts.actors` and `completeness.verdict` from the file; do not copy them here); `Docs/COMMANDS_AND_LOG_TAGS.md` when it touches a console command or log tag.

| Task | Also read |
|------|-----------|
| Fix work | Search `docs/KNOWN_ERRORS.md` for the symptom. Read only the matching entries. Never load the whole file. If the fix depends on level data, the manifest named above is the actor scan. If it is missing, scan the level actors in this session first. |
| Descent, gather, fertilizer, or homestead | `Docs/context/HOMEWORLD_ROUTE.md` |
| Route, placeable, merge, or level | `Docs/context/LEVEL_RULES.md` |
| Hand back | `Docs/context/HANDBACK.md` only when Lead says `mode: co — hand back` |

## Ending the reads

If the opening message already names the task, start it. Otherwise size the input and say which track you picked in one line, so the user can override.

| Track | Signal | Action |
|-------|--------|--------|
| Named | Concrete verb + specific game thing + expected outcome | Say the plan in one line, skip to work. |
| Topic | A noun or area, no verb or no expected outcome | One typed clarifier, then proceed as Named. |
| Dream | No anchor to a specific system, or a pure idea statement | Run the intake below. |

Dream intake — three questions, one at a time, free text first, options only if they stall:

1. In one sentence, what is it?
2. What should the first minute feel like?
3. What is today's job — look at it, shape it, or build a piece of it?

Or skip the questions entirely: the agent drafts a short concept paragraph from whatever minimal input exists, and the user redlines it. That paragraph becomes the brief.

Then write a one-paragraph brief and get a yes before any agent work. On the Dream track, read `Docs/VISION_BOARD.md` before scoping.

Apply the same sizing to later messages: a topic-level or dream-level request mid-task drops to the clarify step, not straight into code.

Other doors are not start reads. Open one only when the developer names it, or when the question shows it is needed; route-context `## Curiosity` restates the same rule.

Before the first edit of the session, run `git status --short` once. Stop and report if it shows uncommitted changes you did not make.

## Session close

1. Finish every piece of work the agent can do itself.
2. Ask any question whose answer would let the agent continue. Carry on from the answer.
3. Only when the next step needs the developer's hands, ask whether a tutorial is wanted. Never offer one for agent-owned work.

No tutorial is on offer yet. Offer `Docs/qa/HUMAN_TUTORIAL.md` only once it is committed and `Content/Python/human_tutorial.py --check` exits 0. Until then, step 3 names the next manual step in one line.

This file wins where it differs from `route-context.md`. The pinned route-context already has the close section. Do not wait on a UserHarness SHA for it.

If an unrelated second task appears, alert and stop.

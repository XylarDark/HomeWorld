# Session start

The one start door. Any IDE, chat, CLI, or agent runner. If a capability is missing, say so. Do not invent a substitute.

## Mode

1. Start in solo mode. `HANDOFF from HomeWorld Co` or `mode: co` switches to Co. `mode: solo` switches back.
2. First message header, once: `Mode: <solo or co> · State: <agent, decide, or do>`. Name the real mode and the real state. Restate only when either changes.
3. State is `agent`, `decide`, or `do`. Name it before acting.
4. Open `Docs/context/DOOR_RULES.md` with the task.

## Context loss

Re-read only this file, restate the header once, and do not re-run the clarifier.

## Read order

One file per step. Wait for it before the next read.

1. `UserHarness/docs/human-use/route-context.md` — through `## How to detect the state` only. Stop before `## Session close`.
2. `Docs/context/ROUTE_INDEX.md`

Open only when the task needs it: `Docs/WORLD_METRICS.md` for a number; `Docs/level/L_VS_MVP_Markers_manifest.json` for level data (read `counts.actors` and `completeness.verdict` there; do not copy them here); `Docs/COMMANDS_AND_LOG_TAGS.md` for a console command or log tag.

| Task | Also read |
|------|-----------|
| Fix | Search `docs/KNOWN_ERRORS.md` for the symptom. Matching entries only, never the whole file. Level-data fixes use the manifest above as the actor scan. If it is missing, scan the level actors this session first. |
| Descent, gather, fertilizer, or homestead | `Docs/context/HOMEWORLD_ROUTE.md` |
| Route, placeable, merge, or level | `Docs/context/LEVEL_RULES.md` |
| T0 scope | `Docs/context/T0_INTERVIEW_LOCK.md` |
| First loop, or implement from the lock | `Docs/context/T0_INTERVIEW_LOCK.md`, `Docs/context/T0_SHAPE_PLAN.md`, and the active queue named in `Docs/CANON_MAP.md`. A later lock line wins over an older queue. |
| Interview, lock, or boss | `Docs/context/BOSS_LAIR_LOCK.md` and the vision-board line that points at it. A later lock wins. Do not open the GDD unless the lock names it. |
| Hand back | `Docs/context/HANDBACK.md` when the session is Co and the message says hand back |

## Ending the reads

A named task (verb + game thing + outcome) gets a one-line plan, then work. A recorded queue of agent-owned items runs until a decide, a do, or a second fail on the same writer. A missing tool blocks only that item: say so, do not invent a substitute, and continue the queue. When Luke has said to run that queue, that is the yes for the level items it names. One change, one run, then stop applies to a task that is still unknown. A topic (no verb or no outcome) gets one typed clarifier, then proceeds as named. A dream (no system, or a pure idea) asks, one at a time: what it is; what the first minute should feel like; whether today is look, shape, or build. Or draft a short concept paragraph for a redline — that paragraph is the brief. Dream work reads `Docs/VISION_BOARD.md` and waits for a yes. A topic or dream mid-task drops back to the clarifier.

An interview is one lock. Competing choices for that lock, then stop. Not a menu of different paths. Scribe the pick before the next lock. If the card fails, take a numbered reply in chat. Do not invent a substitute card.

Other doors are not start reads. Open one only when it is named, or when the question shows it is needed.

Before the first edit, run `git status --short` once. No checkout: say so. A remote write names the branch. Stop and report uncommitted changes you did not make.

## Session close

1. Finish every piece of work the agent can do itself.
2. Ask any question whose answer would let the agent continue, then carry on.
3. Only when the next step needs the developer's hands, ask whether a tutorial is wanted. Never offer one for agent-owned work.

No tutorial is on offer yet. Offer `Docs/qa/HUMAN_TUTORIAL.md` only once it is committed and `Content/Python/human_tutorial.py --check` exits 0. Until then, step 3 names the next manual step in one line.

This file wins on the close order. It also wins on mode, the read list, and the clarifier. Do not wait on a UserHarness SHA.

An unrelated second task: alert and stop. A second task Luke names is the yes.

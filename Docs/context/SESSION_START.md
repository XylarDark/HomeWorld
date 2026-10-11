# Session start

The one start door. Any IDE, chat, CLI, or agent runner. If a capability is missing, say so. Do not invent a substitute.

## Mode

1. Start in solo. `HANDOFF from HomeWorld Co` or `mode: co` switches to Co. `mode: solo` switches back.
2. First message, once: `Mode: <solo or co> · State: <agent, decide, or do> · Transition: <the Now line in Docs/art/PHASES.md>`. Read that line before the message. Name the real mode, the real state, and the open transition before acting. Restate when mode, state, or that line changes.
3. Open `Docs/context/DOOR_RULES.md` with the task.
4. Context loss: re-read only this file, restate the header once, and do not re-run the clarifier.

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
| What next, the project picture, the critical path, prototype assets, stills, Tripo, Meshy, Mixar, or art asset | `Docs/context/ART_ASSET_DOOR.md`. The room is Look. Do not offer rooms. |

## Pick the task

This is the production step. Vision says how the thing is shaped. The lists say what is next. The room says which files to open.

1. Read `Docs/VISION_BOARD.md` through `## Shape` only. Stop before the principles table.
2. Read the status line in `Docs/art/ASSET_CONTEXT_TASKS.md` (the sitting queue, through the lock lines). Read `## Critical path` in `Docs/context/PLAY_TASKS.md` and in `Docs/context/PROVE_TASKS.md`. Do not read the cards.
3. Start the first critical-path item that is not kept and whose co-fork blockers are done. Look’s status line wins while Play’s critical path says none.
4. Open that room and only the resources it names for that item. Look opens `Docs/context/ART_ASSET_DOOR.md`. Play opens the named lock. Prove opens the named prove.

## After the reads

- **Named task** (verb + game thing + outcome): one-line plan, then work.
- **Queue:** run until a decide, a do, or a second fail on the same writer. A missing tool blocks only that item: say so, do not invent a substitute, and continue the queue. When Luke has said to run that queue, that is the yes for the level items it names.
- **Unknown:** one change, one run, then stop.
- **Topic** (no verb or no outcome): one typed clarifier, then proceed as named. A topic or dream mid-task drops back to the clarifier.
- **Dream** (no system, or a pure idea): ask, one at a time, what it is; what the first minute should feel like; whether today is look, shape, or build. Or draft a short concept paragraph for a redline. That paragraph is the brief. Read `Docs/VISION_BOARD.md` and wait for a yes.

Other doors are not start reads. Open one only when it is named, or when the question shows it is needed.

Before the first edit, run `git status --short` once. No checkout: say so. A remote write names the branch. Stop and report uncommitted changes you did not make.

## Interview

One lock. Competing choices, then stop. Not a menu of paths. Scribe the pick before the next lock. If the card fails, take a numbered reply in chat. Do not invent a substitute card.

After the clarifier names the work, name one room and open that card. Look is `Docs/context/FORK_LOOK.md`. Play is `Docs/context/FORK_GAMEPLAY.md`. Prove is `Docs/context/FORK_TESTING.md`. Art and asset both open Look. You can correct the room. No pick stays in the clarifier. No fourth craft room. The art bible is the law inside Look. It is not a room. A card points at a settled lock. It does not reopen it. Shape is `Docs/context/SESSION_FORK_LOCK.md`.

Prototype assets, stills, and “what next” skip this choice. The task rows above already name the room.

## Session close

1. Finish every piece of work the agent can do itself.
2. Ask any question whose answer would let the agent continue, then carry on.
3. Only when the next step needs the developer's hands, ask whether a tutorial is wanted. Never offer one for agent-owned work.

No tutorial is on offer yet. Offer `Docs/qa/HUMAN_TUTORIAL.md` only once it is committed and `Content/Python/human_tutorial.py --check` exits 0. Until then, step 3 names the next manual step in one line.

This file wins on the close order. It also wins on mode, the read list, and the clarifier. Do not wait on a UserHarness SHA.

An unrelated second task: alert and stop. A second task Luke names is the yes.

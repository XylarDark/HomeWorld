# Session start

The one start door. Any IDE, chat, CLI, or agent runner. If a capability is missing, say so. Do not invent a substitute.

The newest block in [docs/SESSION_NOW.md](../../docs/SESSION_NOW.md) is the start. Read it, then the one file it names. Do not open `docs/history/SESSION_LOG.md` to start a chat.

## Build, worktrees, and git

1. Robocopy `Plugins/UnrealMCP` into every new git worktree before its first Build.bat. It is gitignored, so the worktree build fails without it.
2. Build.bat exit 6 has more than one cause: Live Coding in a running editor, a missing plugin, or a compile error. Read `Build-HomeWorld.log` before a retry. For Live Coding, build in a worktree or hand the editor close to Luke as a `do`.
3. Touch a copied-in source file before Build.bat. Copy-Item can keep an older mtime, and UBT then skips it as up to date.
4. A fail-before counts only after a green build in which the new test fails on its own assertion. A compile error is not a fail-before.
5. A headless `-ExecutePythonScript` entry script calls `unreal.set_keep_python_script_alive(True)`. UE 5.8 quits when the entry script returns.
6. An editor change is done only when a readback file written after the step started shows it. Say so before handing back.
7. Copy `Saved/` readbacks to the box, or to Drive with mtimes kept, before removing or switching any worktree.
8. Run `git branch -d` only after switching to main. From another HEAD it refuses branches merged into main.
9. Before the first edit, run `git status --short` once. `git add` uses the path that status prints. Do not retype `Docs/` when status shows `docs/`. No checkout: say so. A remote write names the branch. Stop and report uncommitted changes you did not make.

## Mode

1. Start in solo. `HANDOFF from HomeWorld Co` or `mode: co` switches to Co. `mode: solo` switches back.
2. First message, once: `Mode: <solo or co> · State: <agent, decide, or do>`. In the Look room only, add `· Transition: <the Now line in Docs/art/PHASES.md>` and read that one line first. Name the real mode and state before acting. Restate when either changes.
3. State, first match wins, for this task's next step: `decide` when it needs a judgment only Luke can make (vision, taste, priority, ship, which option) that is not recorded; ask with the real options, then stop. `do` when it needs hands the agent lacks (the editor, playing a build, hardware, an account); hand it over, then stop. Otherwise `agent`: say so in one owner sentence, then work.
4. A new shared utility, a new tool, or an always-on edit re-runs the state. Never a fourth state. The full rule is `UserHarness/docs/human-use/route-context.md`; open it only when the state is unclear.
5. Context loss: re-read only this file, restate the header once, and do not re-run the clarifier.

## Playtest reply

A log line, a screenshot, a lock to scribe, or a beat to test, reach, or fast-forward to uses this door and beats continuity. The mode line stays one sentence.

A beat reads the `hw.Playtest.FastForward` row in `Docs/COMMANDS_AND_LOG_TAGS.md` and the one section of `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md` that names that beat. The host preflight is `Docs/qa/QUEST_TESTS.md`. One compile after Luke's yes, and the handoff after a new lock, are `.agents/skills/token-efficient-context/SKILL.md`. Do not restate the pass line. A beat word that `list` does not print is not a new command. Say so and stop. The task is that line. Read only the active queue's Now line and the one owner file it points at. Do not read vision, the asset queue, or either critical path. The same on-screen fail twice stops the reply. Say what was not in the binary.

## Read order

A named handoff, queue section, or file: read that owner and stop. Skip the task table.

What next, the project picture, or an unnamed queue: read the newest block in `docs/SESSION_NOW.md` and the one file it names. If that file is a playtest handoff, the queue Now line is the pass. Do not open vision, `Docs/context/ART_ASSET_DOOR.md`, or either critical path. If that block names no file, read the status line in `Docs/art/ASSET_CONTEXT_TASKS.md` and `## Critical path` in `Docs/context/PLAY_TASKS.md` and `Docs/context/PROVE_TASKS.md`. Start the one open critical-path item. One room. Do not read the cards.

| Task | Also read |
|------|-----------|
| A number, level data, a console command, or a log tag | `Docs/WORLD_METRICS.md` for a number; `Docs/level/L_VS_MVP_Markers_manifest.json` for level data (read `counts.actors` and `completeness.verdict` there; do not copy them here); `Docs/COMMANDS_AND_LOG_TAGS.md` for a console command or log tag. |
| Fix | Search `docs/KNOWN_ERRORS.md` for the symptom. Matching entries only, never the whole file. Level-data fixes use the manifest above as the actor scan. If it is missing, scan the level actors this session first. |
| Descent, gather, fertilizer, or homestead | `Docs/context/ROUTE_INDEX.md`, then `Docs/context/HOMEWORLD_ROUTE.md` |
| Route, placeable, merge, or level | `Docs/context/LEVEL_RULES.md`. Add `Docs/context/DOOR_RULES.md` only for a level option, a packet, or a level fix. |
| T0 scope, or the named lock is T0 | `Docs/context/T0_INTERVIEW_LOCK.md` and `Docs/context/T0_SHAPE_PLAN.md`. A later lock line wins over an older queue. |
| Interview or lock | The interview file the message or the newest `docs/SESSION_NOW.md` block names. |
| Boss | `Docs/context/BOSS_LAIR_LOCK.md` and the vision-board line that points at it. Do not open the GDD unless the lock names it. |
| Hand back | `Docs/context/HANDBACK.md` when the session is Co and the message says hand back |
| Prototype assets, stills, Tripo, Meshy, Mixar, or art asset | `Docs/context/ART_ASSET_DOOR.md`. The room is Look. Do not offer rooms. |
| Movement test, greybox floor, blockout, sightline, or a prototype walk | `Docs/handoffs/research/UE_BLOCKOUT_PROTOCOL.md`. Engine cube and the material already on it. Player Start on that floor. Play In Editor, on foot. |
| Unreal API, the skills server, a new editor tool, Python placer, or import script | `Docs/tools/GAME_TOOL_CATALOG.md` before a new script or an engine call. That file names the `search` call. |
| Partner or child company, party flags, or night family teleports | `Docs/41_COMPANION_PARTY_DESIGN.md` |

## After the reads

- **Named task** (verb + game thing + outcome): one-line plan, then work.
- **Queue:** run until a decide, a do, or a second fail on the same writer. A missing tool blocks only that item: say so, do not invent a substitute, and continue the queue. When Luke has said to run that queue, that is the yes for the level items it names.
- **Unknown:** one change, one run, then stop.
- **Topic** (no verb or no outcome): one typed clarifier, then proceed as named. A topic or dream mid-task drops back to the clarifier.
- **Dream** (no system, or a pure idea): ask, one at a time, what it is; what the first minute should feel like; whether today is look, shape, or build. Or draft a short concept paragraph for a redline. That paragraph is the brief. Read `Docs/VISION_BOARD.md` and wait for a yes.

## Write a fact once

Vision stays in `Docs/VISION_BOARD.md`. A shared scene practice stays in `Docs/context/SCENE_SETUP.md`. A fact about one map stays in that map's context file under Docs/level. Coordinates stay in that map's metrics file. A room layout stays in that map's room plan. An opening-tutorial pick stays in `Docs/context/OPENING_TUTORIAL_INTERVIEW.md`. The playtest queue owns Now and the pass table. The task list owns build order. Another file points at the owner. It does not restate the fact.

## Interview

One lock. Scribe the pick in its owner file before the next lock, then write the handoff and stop. A lock does not start Play In Editor. The ask shape is `.agents/skills/steer-gate/SKILL.md`. Do not add a second prompt. A beat with no picked action gets one question: what the player does. Do not offer passes you invented.

After the clarifier names the work, name one room and open that card: Look `Docs/context/FORK_LOOK.md` (art and asset), Play `Docs/context/FORK_GAMEPLAY.md`, Prove `Docs/context/FORK_TESTING.md`. You can correct the room; no pick stays in the clarifier. No fourth room; the art bible is the law inside Look. A card points at a settled lock and does not reopen it. Shape is `Docs/context/SESSION_FORK_LOCK.md`. Prototype assets, stills, and what next skip this choice.

## Session close

The close order is `UserHarness/docs/human-use/route-context.md`. This file wins on the close order. It also wins on mode, the read list, and the clarifier. No tutorial is on offer yet. Offer `Docs/qa/HUMAN_TUTORIAL.md` only once it is committed and `Content/Python/human_tutorial.py --check` exits 0. Until then, step 3 names the next manual step in one line. Do not wait on a UserHarness SHA. An unrelated second task: alert and stop. A second task Luke names is the yes.

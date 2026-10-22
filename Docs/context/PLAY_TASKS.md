# Play tasks

Running list for the play room. Fed from `Docs/TaskLists/T0_NEXT_QUEUE.md`. A later lock wins. Do not copy route meters into chat.

Lanes: critical path, later, future. Session start walks critical path only. A task has one owner. Co-fork names the other room that must finish first.

## Critical path

The master list is [`Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`](../qa/TUTORIAL_PLAYTEST_QUEUE.md#critical-path). This file points there. It does not restate the days. The wake minute on `L_SizeTest` is kept. The cottage sheet is kept.

## Ahead of the plays

Prep so a later critical-path row can be played. The handoff is [`Docs/handoffs/SESSION_HANDOFF_PLAYTEST_PREP.md`](../handoffs/SESSION_HANDOFF_PLAYTEST_PREP.md). The Night pass stays [`Docs/handoffs/SESSION_HANDOFF_PLAYTEST.md`](../handoffs/SESSION_HANDOFF_PLAYTEST.md). A host check does not fill a human table.

Start now means source and a host test, with the editor left open. Place means the editor, after that Night pass releases `L_SizeTest`.

Tasks 1 and 2 passed their host tests on 2026-10-21 and are in Done. Task 3 added `glider`, `delivery`, `daycamp`, `dawnglide`, `nightglide`, `stealth`, `ease`, and `shrine`. The shrine stop runs the three ladders and stops before the E. Moss stays out of the six-slot carry. The heal formula is in the binary (`HomeWorld.Opening.HealTime`). The Night sentence is in. The one-press heal is in. The day-camp arrival passed `HomeWorld.Opening.DayCamp`; the clearing is still a place task. Dawn glide stops before the launch. No meadow, mist actor, or smoke actor is added.

| # | Task | Unblocks | Start | Done when |
|---|---|---|---|---|
| 3 | Quest stops | Oct 26 through Nov 10 | Done for the stops | `glider`, `delivery`, `daycamp`, `dawnglide`, `nightglide`, `stealth`, `ease`, and `shrine` are in `DebugFastForwardOpening` and `Content/Python/quest_test_manifest.py`. The shrine stop runs the three ladders and stops before the E. Moss stays out of the six-slot carry. The heal formula is in the binary. The Night sentence is in. `.\Tools\RunTests.ps1 -QuestCheck` exits 0. |
| 5 | Glide start and field landing | Oct 27 and Oct 29 | Place | `GP_GlideStart` is on the island. The landing is one authored meadow with a forest edge and three marked node sites. No path through the meadow. No seeded map. The site is chosen at the desk on `L_SizeTest` after the Night pass. No coordinate is written. |
| 6 | Three nodes and chests | Oct 30 and Nov 2 | Place, after 2 | One wood tree, one herb, one stone rock, on `M_WoodWild`, `M_GatherHerb`, and `M_CliffRock`. Three chests at home, one per material. |
| 7 | Day camp | Nov 4 | Place | The arrival passed `HomeWorld.Opening.DayCamp`. Still to place: a clearing and a `NODE_DAY_CAMP` actor on `L_SizeTest`. |
| 8 | Night glide markers | Nov 5 | Place, after 1 | A home glide start and a camp landing. No cloud wisp actors. |
| 9 | Guards and light | Nov 6 | Place | Three guard actors and their light volumes. A missing guard does not soft-latch an avoid. |
| 10 | Ease pads | Nov 9 | Place, after 9 | One ease pad on each guard. The wind-up, the spend, the wait, and the wrong shape are the existing verb. |
| 11 | Captive and shrine | Nov 10 | Place, after 9 | The captive actor and a shrine with `UHomeWorldShrinePortalComponent`. Freeing the partner requires the three sleeps. The shrine walks the partner home. |

## Later

| Item | Owner | Co-fork | State |
|---|---|---|---|
| Field greybox re-run on `L_Field` | Play | The zone contract in `Lib/02_Zones/gather/FIELD.json` | Off the November 20 path. Mass placed and verified 2026-10-14 (`field_greybox: CHECK PASS`, editor log 16:53Z). The sun pose and sky light fix landed after that run (`befdc171`), so a re-run of the placer and verifier is still owed. The path's field shell is the queue row for Oct 29. |
| Remap `M_FamilySilhouette` and `M_ValleyNight` onto the ten masters | Play | Engineering. Blocked: the Blender 4.4 install has no `blender.exe`. The cite and `Content/Python/remap_family_valley_materials.py` are ready. | Blocked |
| Camp art meshes from the filed camp images | Look | Play markers are already in the manifest. Do not start until the Look queue reaches camp. | Waiting on Look |

## Future

- Family-hint words past "toward the edge."
- Re-deriving `Docs/WORLD_METRICS.md` onto the scale pass.
- Shrine look past a standing stone at twice player height.

## Shared systems

Audit 2026-10-22 of the opening/beat code, not the whole repo. Each row is a patch that got copied instead of a system. A row is done when the copies are gone, not when a new call site is added. Evidence is the count at audit time.

| # | Task | Evidence | Done when | Lane |
|---|---|---|---|---|
| S1 | One interaction resolver | `HasOpeningLineOfSight` is called from five verbs; reach, look, and the wall test are re-ordered in each | Every opening verb resolves through one call that owns reach, look, wall, and hover. The verbs hold only what they do with the target. **Spec, gate, and cone in source, 2026-10-22; verb collapse pending.** | critical |
| S2 | Cached target registry | 26 `FindOpeningNamed`/`FindOpeningTaggedActor` calls, each a world scan; the prompt path runs them per frame | One registry, built on level load, invalidated on change. No per-frame world scan. **Cone's static tag list removed, 2026-10-22; registry pending.** | critical |
| S3 | Derived beat stop gaze | 16 hard-coded `Distance =` values; the 220 cm armory stop put a 0.9 m table under the look box and the hover never appeared | The stop derives its gaze from the target's bounds under one rule. Authored distance stays as intent only. **Gaze rule + centered frame in source, 2026-10-22; not built.** Distance still per beat. | critical |
| S4 | Shared return flight | The bonk had a teleport, then a launch, then a re-trigger loop, then a second copy of the same math. The rise-cross-land flight then launched straight up and landed on the rim. | `BeginBonkReturn(Target, PadOrigin, PadExtent)` is the only path. One shallow swoop, landing inset from the rim. A new bonk adds a call, not flight code. **Swoop is in source, 2026-10-22, waiting on the play.** | critical |
| S5 | One placement constants source | Counter height lived in `cabin_shell.BOXES`, a `90.0` in `seat_props`, and the reveal; raising the counter sank the kettle and blocked the save | Height, standoff, and tag names read from one module by the shell, the placer, and the reveal. | later |
| S6 | Named light presets | `scene_placement` writes intensity, radius, and temperature inline | Presets by name (candle, lamplight, night) in one table; a placer asks for a preset. | later |
| S7 | Debug probes behind a flag | `opening_los` logging sits in shipping code from today's table chase | The probe is behind a cvar or removed. | later |

S1 to S3 are the same defect seen three ways: each verb and each stop re-decides what "visible", "in reach", and "looked at" mean. S1 owns the answer.

## Done

- Glider craft. `HomeWorld.Opening.GliderCraft` passed, 2026-10-21.
- Delivery verb. `HomeWorld.Opening.Delivery` passed, 2026-10-21.
- Day-camp arrival. `HomeWorld.Opening.DayCamp` passed, 2026-10-21. The clearing is not placed.
- Heal formula. `HomeWorld.Opening.HealTime` covers 3.0, 3.1, 4.0, and 4.1. The Night sentence is in. One press at the hot springs starts one wisp. 2026-10-22.
- Wake-yard actors placed, 2026-10-08. No meshes. The rune is not placed.
- Night flight spreads the mixed fertilizer. `HomeWorld.T0.FL10.NightFlightSpreadsFertilizer` passed, 2026-10-08.

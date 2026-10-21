# Play tasks

Running list for the play room. Fed from `Docs/TaskLists/T0_NEXT_QUEUE.md`. A later lock wins. Do not copy route meters into chat.

Lanes: critical path, later, future. Session start walks critical path only. A task has one owner. Co-fork names the other room that must finish first.

## Critical path

The master list is [`Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`](../qa/TUTORIAL_PLAYTEST_QUEUE.md#critical-path). This file points there. It does not restate the days. The wake minute on `L_SizeTest` is kept. The cottage sheet is kept.

## Ahead of the plays

Prep so a later critical-path row can be played. The handoff is [`Docs/handoffs/SESSION_HANDOFF_PLAYTEST_PREP.md`](../handoffs/SESSION_HANDOFF_PLAYTEST_PREP.md). The Night pass stays [`Docs/handoffs/SESSION_HANDOFF_PLAYTEST.md`](../handoffs/SESSION_HANDOFF_PLAYTEST.md). A host check does not fill a human table.

Start now means source and a host test, with the editor left open. Place means the editor, after that Night pass releases `L_SizeTest`.

Tasks 1 and 2 passed their host tests on 2026-10-21 and are in Done. Task 3 added `glider`, `delivery`, `daycamp`, `dawnglide`, `nightglide`, `stealth`, and `ease`. The shrine stop is not in: the three strokes stay the player's. `.\Tools\RunTests.ps1 -QuestCheck` is the host check. The heal stop still waits on the Night sentence. The day-camp arrival passed `HomeWorld.Opening.DayCamp`; the clearing is still a place task. Dawn glide stops before the launch. No meadow, mist actor, or smoke actor is added.

| # | Task | Unblocks | Start | Done when |
|---|---|---|---|---|
| 3 | Quest stops | Oct 26 through Nov 10 | After the Night sentence for the heal stop | `glider`, `delivery`, `daycamp`, `dawnglide`, `nightglide`, `stealth`, and `ease` are in `DebugFastForwardOpening` and `Content/Python/quest_test_manifest.py`. The shrine stop waits on the player's three strokes. The heal stop waits on the Night sentence. `.\Tools\RunTests.ps1 -QuestCheck` exits 0. |
| 4 | Heal formula | Oct 23 | After the Night table has a sentence | The click heart sets the heal: 20 seconds at 3 seconds or under, plus 10 seconds per second over. A partial second counts. The heart may run past 3 seconds. A host test proves 3.0, 3.1, and 4.1. |
| 5 | Glide start and field landing | Oct 27 and Oct 29 | Place | `GP_GlideStart` is on the island. The landing is one authored meadow with a forest edge and three marked node sites. No path through the meadow. No seeded map. |
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

## Done

- Glider craft. `HomeWorld.Opening.GliderCraft` passed, 2026-10-21.
- Delivery verb. `HomeWorld.Opening.Delivery` passed, 2026-10-21.
- Day-camp arrival. `HomeWorld.Opening.DayCamp` passed, 2026-10-21. The clearing is not placed.
- Wake-yard actors placed, 2026-10-08. No meshes. The rune is not placed.
- Night flight spreads the mixed fertilizer. `HomeWorld.T0.FL10.NightFlightSpreadsFertilizer` passed, 2026-10-08.

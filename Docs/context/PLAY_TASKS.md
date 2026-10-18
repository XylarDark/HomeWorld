# Play tasks

Running list for the play room. Fed from `Docs/TaskLists/T0_NEXT_QUEUE.md`. A later lock wins. Do not copy route meters into chat.

Lanes: critical path, later, future. Session start walks critical path only. A task has one owner. Co-fork names the other room that must finish first.

## Critical path

The wake minute on `L_SizeTest` is kept. The cottage sheet is kept. The open play is the opening tutorial. The field greybox re-run is behind that queue.

| Item | Owner | Co-fork | State |
|---|---|---|---|
| Wake minute on `L_SizeTest` | Play | Look, for the cottage sheet and room plan | Kept 2026-10-14 |
| Opening tutorial on `L_SizeTest` | Play | Round 1 in `Docs/context/OPENING_TUTORIAL_INTERVIEW.md` | Open. Queue: `Docs/context/OPENING_TUTORIAL_TASKS.md`. The sequence is the Opening tutorial in `Docs/VISION_BOARD.md`. |
| Field greybox on `L_Field` | Play | The zone contract in `Lib/02_Zones/gather/FIELD.json` | Mass placed and verified 2026-10-14 (`field_greybox: CHECK PASS`, editor log 16:53Z). The sun pose and sky light fix landed after that run (`befdc171`), so a re-run of the placer and verifier in the editor is still owed before this is done. |

## Later

| Item | Owner | Co-fork | State |
|---|---|---|---|
| Remap `M_FamilySilhouette` and `M_ValleyNight` onto the ten masters | Play | Engineering. Blocked: the Blender 4.4 install has no `blender.exe`. The cite and `Content/Python/remap_family_valley_materials.py` are ready. | Blocked |
| Camp art meshes from the filed camp images | Look | Play markers are already in the manifest. Do not start until the Look queue reaches camp. | Waiting on Look |

## Future

- Family-hint words past "toward the edge."
- Re-deriving `Docs/WORLD_METRICS.md` onto the scale pass.
- Shrine look past a standing stone at twice player height.

## Done

- Wake-yard actors placed, 2026-10-08. No meshes. The rune is not placed.
- Night flight spreads the mixed fertilizer. `HomeWorld.T0.FL10.NightFlightSpreadsFertilizer` passed, 2026-10-08.

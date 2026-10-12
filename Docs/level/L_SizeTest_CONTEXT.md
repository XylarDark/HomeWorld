# L_SizeTest context

Open with `Docs/context/SCENE_SETUP.md` before moving this map. Placement numbers are in `Docs/level/L_SizeTest_METRICS.md`. `Content/Python/scene_placement.py` applies that file.

Map: `/Game/HomeWorld/Maps/SizeTest/L_SizeTest`.

## Measured floor

2026-10-11. The island actor is at z = 450 m. Five downward traces hit the pad at 45,000 cm. The cone hangs below that pad. The player start is on the path between the beds, yaw 90, facing the south opening. The snap rule is practice 12.

## Who is here

Homestead: cottage, rocks, pines, herb beds, lupines. The player start is on the south path, aimed at the entry. Plants do not block the capsule. The field mesh is scaled under the island so the pad reads as floating above the plain.

Not in this test: bear, guards, camp, clouds, bull, and the gatherables. The placer removes them and will not save if a solid shares the player’s clearance on the 1 m grid.

## Play

One directional light, `SizeTest_Sun`. Walk bounds are off on this map. Facing, the walk clip, the jump, and the shoulder sphere are practices 10, 11, and 16 in `Docs/context/SCENE_SETUP.md`. The cottage blocks, and the south opening is the way in. The layout is `Docs/level/L_SizeTest_ROOM_PLAN.md`.

Do not run `Content/Python/place_size_test.py` against this map. It builds a new level.

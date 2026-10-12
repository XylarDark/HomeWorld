# L_SizeTest context

Open with `Docs/context/SCENE_SETUP.md` before moving this map. Placement numbers are in `Docs/level/L_SizeTest_METRICS.md`. `Content/Python/apply_size_test_metrics.py` applies that file.

Map: `/Game/HomeWorld/Maps/SizeTest/L_SizeTest`.

## Measured floor

2026-10-11. The island actor is at z = 450 m. Five downward traces hit the pad at 45,000 cm. The cone hangs below that pad. Contact actors sit on 450 m. The placer snaps each mesh bottom to that top, measures again, and does not save if any bottom is more than 2 cm off. The player start is on the path between the beds, yaw 90, facing the south door.

## Who is here

Homestead: cottage, rocks, pines, herb beds, lupines. The player start is 6 m south of the cottage. Plants do not block the capsule. The field mesh is scaled under the island so the pad reads as floating above the plain.

Not in this test: bear, guards, camp, clouds, bull, and the gatherables. The placer removes them and will not save if a solid shares the player’s clearance on the 1 m grid.

## Play

One directional light, `SizeTest_Sun`. Walk bounds are off on this map. The pawn uses `SK_Size_Player` at a 2 m capsule. The mesh yaw offset is +90 because the coat faces mesh −Y. The walk clip plays only while moving, with root motion ignored. WASD moves the capsule. Space uses the existing 420 cm/s jump. A greybox sphere follows the right shoulder. The cottage walls block, and the south door is open onto the pad.

Do not run `Content/Python/place_size_test.py` against this map. It builds a new level.

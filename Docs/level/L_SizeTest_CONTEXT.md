# L_SizeTest context

Open with `Docs/context/SCENE_SETUP.md` before moving this map. Placement numbers are in `Docs/level/L_SizeTest_METRICS.md`. `Content/Python/scene_placement.py` applies that file.

Map: `/Game/HomeWorld/Maps/SizeTest/L_SizeTest`.

## Measured floor

2026-10-17. The island actor is at z = 450 m. The walk pad is a flat engine cube on that height, 70 m by 140 m. The player start is on the south of that pad, yaw 90, facing the cottage. Trees and rocks stand between the start and the door. The snap rule is practice 12.

## Who is here

Homestead: cottage, trees and rocks south of the door, herb beds, lupines, the partner at the south door, the child beside them, the two crafting stations — the kitchen counter is the consumable station with the kettle standing on it, and the armor table sits in the greybox armory in front of the cottage — and the opening dog on the east lawn at world (10.5 m, 1.5 m), a greybox body until a mesh exists. The player start is on the walk pad, south of those props, facing the cottage. Plants do not block the capsule. The partner and the child do not block it either. The dog does not block it either. The field mesh stays under the island and is not the floor you walk. The pad stays flat.

Not in this test: bear, guards, camp, clouds, bull, and the gatherables. The placer removes them and will not save if a solid shares the player’s clearance on the 1 m grid.

## Play

E on this map reaches the spirit, the partner, the garden, and the kettle, then returns. Anything else, including the bed and the dawn glide, has to be added to that chain in `UHomeWorldInteractAbility` or E will not reach it. Herb chunks live on `OpeningHerbTenths` on `AHomeWorldCharacter`. Wall meters stay in `Content/Python/cabin_shell.py` and `Docs/level/L_SizeTest_ROOM_PLAN.md`. Do not invent them.

One directional light, `SizeTest_Sun`. Walk bounds are off on this map. Facing, the walk clip, the jump, and the shoulder sphere are practices 10, 11, and 16 in `Docs/context/SCENE_SETUP.md`. The cottage blocks, and the south opening is the way in. The layout is `Docs/level/L_SizeTest_ROOM_PLAN.md`.

## First five seconds

2026-10-17. Luke kept the walk, stop, and hop. The body passes that initial pass. The opening to build on this homestead is the tutorial in [`Docs/VISION_BOARD.md`](../VISION_BOARD.md). The lock is [`Docs/context/PRINCIPLE_FIT_LOCK.md`](../context/PRINCIPLE_FIT_LOCK.md).

Do not run `Content/Python/place_size_test.py` against this map. It builds a new level.

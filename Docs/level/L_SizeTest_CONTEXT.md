# L_SizeTest context

Open with `Docs/context/SCENE_SETUP.md` before moving this map. Placement numbers are in `Docs/level/L_SizeTest_METRICS.md`. `Content/Python/scene_placement.py` applies that file.

Map: `/Game/HomeWorld/Maps/SizeTest/L_SizeTest`.

## Measured floor

2026-10-17. The island actor is at z = 450 m. The walk pad is a flat engine cube on that height, 70 m by 140 m. The player start is on the south of that pad, yaw 90, facing the cottage. Trees and rocks stand between the start and the door. The snap rule is practice 12.

## Who is here

Homestead: cottage, trees and rocks south of the door, herb beds, lupines, the partner at the south door, the child beside them, the two crafting stations — the kitchen counter is the consumable station with the kettle standing on it, and the armor table sits in the greybox armory in front of the cottage — and the opening dog in the north backyard, with a dog house beside it, a greybox body until a mesh exists. Crafting is the front yard. Research is the east hill. Fishing is the west pond. The player start is on the walk pad, south of those props, facing the cottage. Plants do not block the capsule. The partner and the child do not block it either. The dog does not block it either. The field mesh stays under the island and is not the floor you walk. The walk stays flat. Water, the farm plot, and the hill steps sit off that walk.

Not in this test: bear, guards, camp, clouds, bull, and the gatherables. The placer removes them and will not save if a solid shares the player’s clearance on the 1 m grid.

## Greybox color key

2026-10-18. Colors are a read, not a look. Cottage walls stay grey. This key does not add a master material, and it does not change the field stills. The lit cabin instances do not show a hue on these meshes. The read is `M_GreyboxRead`: a lit grey, roughness 0.85, with the key color mixed in at 0.55, then a 1 m checker drawn across each face. The axis the face sits on is left out, so a flat surface does not strobe. The dark square is 0.55 of that mix. It is not an unlit flat color, and it is not `M_SpiritUnlit`.

- Grey (`MI_Greybox_Stone`, click heart `MI_Greybox_Slate`): walls, floor, and anything with no verb. The dog house and the observatory block use stone.
- Green (`MI_Greybox_Olive`): done or safe. The tamed dog, an open station, the observatory path, the hill steps that are not glide-gated, and the steps up to the zipline perch.
- Yellow (`MI_Greybox_Tan`): in range, not finished. The dog while the Grace draw is available, and after Wrath eases until the herb tames it. A station until it opens. The farm plot.
- Red (`MI_Greybox_DangerRed`): refused or danger. The dog while Wrath is up and the Grace draw is not available.
- Blue (`MI_Greybox_Cyan`): water and the zipline. Spring, hot springs, river, pond, cable, both poles, and both perches.
- Purple (`MI_Greybox_Purple`): spirit and upgrade gates. The shoulder wisp, the dove (the Grace rune), the cave notch, the farm gate, and the glide-gated hill step when it is placed.

The dog and the stations swap those colors on the same mesh. On the homestead sheet, pines, rocks, and the bed are grey. Herb beds, lupines, and the kettle start tan. A gathered bed turns green until it returns. The kettle follows the station once that station opens. The unclaimed spirit is purple.

## Play

E on this map reaches, in order, the spirit, the partner, the garden, the kettle, the stations, the dog, the pond fish, a pine once you are spirit, the bed, and the zipline, then returns. A press on a tamed dog does not log. Sleep in the bed grants spirit and stays on the island. The dawn glide is not in that chain. Anything else has to be added in `UHomeWorldInteractAbility` or E will not reach it. Herb chunks live on `OpeningHerbTenths` on `AHomeWorldCharacter`. Each herb bed keeps its own return, 20 seconds. Gathering one bed does not replace the other's timer. Wall meters stay in `Content/Python/cabin_shell.py` and `Docs/level/L_SizeTest_ROOM_PLAN.md`. Do not invent them.

The shoulder wisp has three places. It sits on the player. If the mesh top reaches head height, it stays at head height, 40 cm to the viewer's right of the mesh center. If the top is below the head, it floats 40 cm above that top and 36 cm past the right face, and never more than 160 cm from the center. Rune ribbons are ignored, so a heart does not move the point. During a heart or the dove it follows the cursor. When the trace, the click, or a finished E ends, it returns to the shoulder, and that prop does not take it again until the player leaves its range.

The first verify after a level load can log `cottage is already in sight, hit CabinWall_01` while the map is still loading. Run `Content/Python/verify_homestead_scene.py` once more. That line is not a reason to move the cottage. A second `CHECK FAIL` is a real miss.

One directional light, `SizeTest_Sun`. Walk bounds are off on this map. Facing, the walk clip, the jump, and the shoulder sphere are practices 10, 11, and 16 in `Docs/context/SCENE_SETUP.md`. The cottage blocks, and the south opening is the way in. The layout is `Docs/level/L_SizeTest_ROOM_PLAN.md`.

## First five seconds

2026-10-17. Luke kept the walk, stop, and hop. The body passes that initial pass. The opening to build on this homestead is the tutorial in [`Docs/VISION_BOARD.md`](../VISION_BOARD.md). The lock is [`Docs/context/PRINCIPLE_FIT_LOCK.md`](../context/PRINCIPLE_FIT_LOCK.md).

Do not run `Content/Python/place_size_test.py` against this map. It builds a new level.

# Cabin room plan

Kept 2026-10-11 after a walk. Greybox blocks for the size-test home. `Content/Python/scene_placement.py` refuses to save unless a 42 cm body can enter, cross the rooms, and leave. The 9 by 11 m card in `Docs/art/SCALE.md` stays the art lock for a later mesh. This page is the layout you walk.

## What the comfortable plans have in common

Golden Eagle’s Farmhouse log plan (about 3,100 sq ft) is an open kitchen, dining, and living room under one tall volume, a covered porch, a mudroom and pantry, and a private main-floor suite with its own bath and closet. Their Country’s Best plan is the same idea at a more luxurious size. Archival’s Aspen (56 by 42 ft) puts the primary suite on the main floor beside an open great room and a covered porch. Architectural Designs 350011GH (51 by 60 ft, about 2,500 sq ft) opens the living space onto a deep covered deck and reaches the primary bedroom through a short hall, with the kitchen open to that room.

The shared comfort pattern is not a row of equal boxes. The public rooms are one volume. The porch is a room. The bedrooms are private, off that volume, each with a real door. A pantry closes the kitchen without walling the cook off from the room.

This body is 84 cm wide and 2 m tall, so a 91 cm door is the width of the body. Openings here are about twice the body. Rooms are larger than the human plans by roughly the same margin, which is what keeps a 2 m person from feeling shut inside a house rated for someone 1.7 m tall.

## Footprint

The cottage actor is at (−8 m, 0). Local +X is east and +Y is north. The shell is 17.5 m wide and 17 m deep, including a 4 m porch. It runs from local (−6.5, −6.8) to (11.0, 10.2). Walls are 5 m high and 30 cm thick. The pad is the floor. There is no door leaf. Posts mark the porch lip and stay off the entry.

| Room | Local X | Local Y |
|---|---|---|
| Porch | −6.5 to 11.0 | −6.8 to −2.8 |
| Great room | −6.5 to 3.5 | −2.8 to 5.6 |
| Kitchen | 3.5 to 11.0 | −2.8 to 3.4 |
| Pantry | 8.2 to 11.0 | 3.4 to 5.6 |
| Couple bedroom | −3.7 to 0.8 | 5.6 to 10.2 |
| Couple bath | −6.5 to −3.7 | 5.6 to 8.6 |
| Couple closet | −6.5 to −3.7 | 8.6 to 10.2 |
| Child bedroom | 0.8 to 7.4 | 5.6 to 10.2 |
| Child bath | 7.4 to 11.0 | 5.6 to 10.2 |

A hearth block sits on the west wall of the great room. It is a greybox marker, not a fireplace mesh.

## Openings

Clear width after the 30 cm wall:

- South entry, on the great room, 2.8 m wide and 3.2 m high.
- Porch crawl, east of the entry, 1.3 m clear. An 84 cm body fits. A 160 cm body does not. A filler blocks it until east-bed tea, or until night if the day woke the other face.
- Great room to kitchen, 4.4 m. The cook faces the room.
- Pantry door, 1.8 m.
- Couple suite and child room, 2.4 m and 2.8 m.
- Couple bath, child bath, and closet, 2.2 m, 2.2 m, and 1.8 m.

## Where the minute stands

The kettle is on the kitchen’s east wall, world (1.8 m, 0.0 m), yaw 180, facing into the room. At play the reveal grows the counter under it and it stands on top; the counter is the consumable station.

The player starts on the south of the pad at (−6 m, −58 m), yaw 90, facing the cottage. That is twice the earlier walk to the reveal. Trees and rocks stand between that start and the south door. The partner stands at the south door, world (−9.5 m, −8.2 m), on the player mesh, yaw 0, facing the player. Walking them inside is scheduled: stop, open the door the way the player does, then path to the kettle with collision on. They do not clip through the wall. The child starts beside the partner at world (−8.0 m, −8.6 m), on that same mesh at 0.6 scale, yaw 270, and runs to the spirit. The spirit is halfway between the player start and the cottage, at world (−7 m, −29 m).

Herb beds sit south of the porch, off the entry, yaw 0.

## The stations and the armory

Added 2026-10-18. Changed the same day after Luke's replay: the armory slid in front of the cottage, and the kitchen counter became the consumable station.

- The consumable station is the kitchen counter, against the east wall at world (2.15 m, 0). At play the reveal grows it 1.4 by 3.2 m, waist high at 0.9 m after the halving, and stands the kettle on top. Presses: the herb and the claimed spirit open it; the next press is its one output, the herb mixed with a spirit; after that the same counter brews at the kettle, one brew spending at most 10 chunks.
- The armory is the second building, in front of the cottage at world (−0.5 m, −13 m), south of the east wing across the courtyard. Seven by six metres outside, 4 m walls, 30 cm thick, one 2.4 m door on the west wall facing the courtyard. `Content/Python/armory_shell.py` grows the walls; the placer checks the door, a wall, the floor, and a 42 cm walk in and back out.
- The armor table stands against the armory's inside east wall: world (2.25 m, −13 m), 0.9 by 1.4 m, 0.9 m tall. The partner's gift opens it. No walk-speed or bonk-try change.

The cottage is the home: cooking and consumables. Four yards sit around it. Crafting is the front yard, south. Taming is the backyard, north. Research is the east hill. Fishing is the west pond. The numbers are in `Docs/level/L_SizeTest_METRICS.md`.

## The opening dog

Added 2026-10-18. Beat 4 of the tutorial day, after the armory.

- The north wall has a back door, 2.4 m wide, centered on the child room. It opens onto the backyard. The south door stays the front door.
- The dog stands in that backyard, north of the back door, facing the door. A dog house sits beside it, off the approach lane. The dog is a greybox body until a mesh exists. It is not a solid.
- The approach lane runs south from the dog to the back door. The placer still wants nine metres of clear pad back to the knock ring, and 2.8 m of clearance from every solid.
- Any press closer than 4 m knocks you back at once. A closing step faster than the slowest opening-wheel step (150 cm/s), inside 10 m, gets "Approach slowly." from the child, then the same shove about 1.25 s after that line is up. The armor gift clears the other proximity lines and leaves this one. Both knocks are a shove with a 250 cm/s lift and no damage. At the slow step, inside 9 m, the Grace symbol — the outline of a dove — appears; tracing it eases the Wrath. One mixed herb then tames the dog. The kept walk speed does not change.
- After the kettle brew grants the tea sprint, the child races from their room out the back door and waits beside the lane, 1.5 m east of it and 6.1 m short of the dog, facing the dog. The stop is outside the 4 m knock ring and inside the 9 m Grace ring.

## The zipline

One perch is the cottage's northwest corner, 4 m up, with a walkable slope down the west wall and another down the north wall. The cable hangs 2.3 m above that perch and slopes to a perch on the pond's near bank. A second cable runs from the research hill down to the northeast corner, with a walkable slope on the north wall and another on the east wall. E on a high perch rides that line. Neither line is the day glide.

## Frames and samples

Added 2026-10-18. The numbers are in `Docs/level/L_SizeTest_METRICS.md`. This page does not copy them.

The walk from the south start to the front door stays on the flat pad. South to north it is the copse gate, then the front yard.

The east hill is the research side. A winding path climbs it to the observatory. The spring is built into that hill. Hot springs sit at its foot. From there a river stays north of the cottage, then turns south only once it is far west of the walls, and meets the pond. The pond sits on the cottage's west line, further toward the pad edge, still in sight from the dog. The terrain sculpt of these shapes is a later pass. This sheet is the flat greybox of where they go.

The second pine grove stands beyond the hill. The farm plot stays east of the south path. A notch on the north face of the hill is the cave.

Armor opens the gap onto the farm plot. It does not change speed or bonk tries. The top step of the overlook is listed and not placed until a glide has happened. The cave notch overlaps only, and only in spirit form after sleep. The first day does not climb the hill.

## Pocket kit outside the porch

Added 2026-10-13. All positions are world, in meters. Z comes from each piece's bounds bottom, not from this page.

| Piece | Axis | From | To | Spacing | What's past the edge |
|---|---|---|---|---|---|
| Path stones (16 or 17) | +X, on the −Y side of the porch | (−9.5, −6.8) | (14.0, −6.0), at `SM_Size_Pine_S_B` | one every 1.5 m over about 23.5 m | the pine at +X; the porch lip at +Y |
| Fence run (6 pieces) | +X at Y −11.5 | X −15.0 | X −4.0 | evenly split over 11 m | open ground at −Y; the herb beds and path at +Y |

The last path stone (stone 16, or 17 if the run needs it) stops short of the pine's trunk. The shrine height (4 m at world (−16.2, −8.3)) is Lead's taste number and is not set here.

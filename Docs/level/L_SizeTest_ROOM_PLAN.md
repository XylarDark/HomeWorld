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

The kettle is on the kitchen’s east wall, world (1.8 m, 0.0 m), yaw 180, facing into the room.

The bed is in the couple bedroom against the north wall, world (−9.5 m, 9.0 m), yaw 0. It is not the sleep bed.

Herb beds sit south of the porch, off the entry, yaw 0. The player stands on that path at (−9.5 m, −9.5 m), yaw 90, aimed at the opening.

## Pocket kit outside the porch

Added 2026-10-13. All positions are world, in meters. Z comes from each piece's bounds bottom, not from this page.

| Piece | Axis | From | To | Spacing | What's past the edge |
|---|---|---|---|---|---|
| Path stones (16 or 17) | +X, on the −Y side of the porch | (−9.5, −6.8) | (14.0, −6.0), at `SM_Size_Pine_S_B` | one every 1.5 m over about 23.5 m | the pine at +X; the porch lip at +Y |
| Fence run (6 pieces) | +X at Y −11.5 | X −15.0 | X −4.0 | evenly split over 11 m | open ground at −Y; the herb beds and path at +Y |

The last path stone (stone 16, or 17 if the run needs it) stops short of the pine's trunk. The shrine height (4 m at world (−16.2, −8.3)) is Lead's taste number and is not set here.

# Size-test island plan

How the yard sits around the cottage. A resize edits this file, then the placer. Coordinates for the actors live in `Docs/level/L_SizeTest_METRICS.md`. The rooms live in `Docs/level/L_SizeTest_ROOM_PLAN.md`. This page does not copy either list.

## Origin

The cottage actor is the homestead origin: world (−8 m, 0). Local +X is east and +Y is north. The shell runs from local (−8, −8) to (18, 15), so the world box is x −16 to 10, y −8 to 15.

## Yards

| Yard | Side | What stays there |
|---|---|---|
| Craft | South, in front of the porch | Armory, herb beds, the family greeting |
| Tame | North of the back door | The dog and the 9 m approach |
| Research | East | The hill, the observatory, the hot springs |
| Fish | West | The pond |

## Clearances

These survive a resize.

- The dog stays at world (−3.9, 20). The north door stays on that x. Nine metres of pad stay north of the door, and the dog stays 2.8 m from any solid. Do not move the dog to make the house fit.
- The armory stays fully south of the porch lip. Its north edge is world y −10. The porch lip is world y −8. The gap is 2 m.
- Herb beds, lupines, the partner, and the child stand in the front yard, south of the porch lip. They do not stand on the porch.
- Zipline ends sit on the shell corners: northwest world (−16, 15), northeast world (10, 15).

## This pass

Herb beds and lupines stand at y −9.2, in the gap between the porch lip and the armory, west of the armory door. The partner is at (−9.5, −10.5) and the child at (−8, −11). The armory already clears the lip by 2 m, so it stays. The dog, the approach pines, and the player start stay.

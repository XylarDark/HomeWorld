# Scene setup

Open this before a test scene is created or moved. A measured failure is written once, in the file that owns it. Shared practice stays here. A fact about one map stays in `Docs/level/<Map>_CONTEXT.md`. Coordinates stay in that map's metrics file. A room layout stays in that map's room plan. Chat is not the record. Do not copy a paragraph into a second file.

Each played map gets `Docs/level/<Map>_CONTEXT.md`. That file names the map, the placement sheet, and the measured facts for that floor. The placer reads the metrics file. It does not invent a coordinate.

## Practices

Measured on `L_SizeTest`, 2026-10-11.

1. The walkable surface is whatever a downward trace hits, not the highest point of the mesh. Five traces land on the pad. Their middle value is the floor. If the highest hit is more than 50 cm above the lowest, the mesh has a hill and the save fails. The size-test cone was that hill: its tip was 3 m above the pad, and the bounds box reported the tip as the floor. In editor Python the hit is a struct: read `to_dict()`, because `location` is not an attribute. Reading it as an attribute logs a miss after a real hit. Measured 2026-10-11.

2. One placement sheet per map. `Content/Python/scene_placement.py` reads `Docs/level/L_SizeTest_METRICS.md` and is the placer for that map. `Content/Python/place_size_test.py` builds a new level. Do not run it to update a map that already exists.

3. The sheet names who is in the scene. On the size-test homestead that is the cottage, rocks, pines, flowerbeds, the partner by the bed, and the child in the garden. The bear and the guards are not on that island. Path stones, fence, moss, the stump, and the crystal stay off until the sheet adds them.

4. One directional light. A second one leaves the view black because forward shading uses a single sun. `L_SizeTest` keeps `SizeTest_Sun`, a sky light, a sky atmosphere, and an unbound exposure of 1.

5. The old walk bounds do not follow a high island. `UHomeWorldSoftBoundsComponent` defaults to center (−400, −50, 100) cm, radius 1050 cm, and MaxZ 600 cm. A pawn at 453 m is outside that cylinder, so the component pushes every tick. On `L_SizeTest` those bounds are off. A new scene turns them off or writes a center, a radius, and a Z range that match that scene’s floor.

6. The playable body is the developed mesh, and it does not start walking by itself. On `L_SizeTest`, BeginPlay assigns `SK_Size_Player`, sets the capsule half-height to 100 cm, and does not play the walk clip. WASD stays the existing move actions.

7. The player start is outside the cottage footprint and faces the door. The footprint is the room plan for that map. A start inside the box fails the walk.

8. Check the mesh bottom against the floor top after a place. Actor Z is not that check.

9. One editor. A commandlet and a build close it. Reopen one on the map under test.

10. Match the walk to the face before changing the offset. On `L_SizeTest` the right arm is mesh +X and the walk strides on Y, so the face is mesh −Y. `MeshForwardYawOffset` +90 turns that face onto actor +X. The mannequin default −90 points this coat backward. Offset 0 walks the body sideways to its face. The control rotation yaw is the PlayerStart yaw. Measured 2026-10-11.

11. Do not disable animation to stop a shove. `SetEnableAnimation(false)` freezes the bind pose, so WASD moves a body that never walks. On `SizeTest`, the imported walk plays only while horizontal speed is above a small threshold, and root motion is ignored. Standing stops the clip. There is no separate idle. The capsule is still the only thing WASD moves.

12. A snap that is not measured again does not count. After the move, every homestead mesh bottom is measured against the floor top. If it is more than 2 cm off, the placer moves it and measures once more. If it is still off, the map is not saved. Plants and solids both get this pin. The field stays at z = 0.

13. A long-lived editor keeps the old Python module. `apply_homestead_scene.py` reloads `scene_placement` before it runs. A headless `-nullrhi` trace does not hit meshes, and a miss is not a save.

14. The garden sits on the south apron of the cottage, long side parallel to the porch, with the path aimed at the door. Beds off to the east and west are not that garden. The placer refuses to save when a bed is north of the porch lip or turned away from the facade.

15. A solid cottage mesh is not an interior. On `L_SizeTest` the walkable cottage is the greybox in `Docs/level/L_SizeTest_ROOM_PLAN.md`. There is no door leaf. Herb beds stay off the entry. The old cottage mesh does not block. The island pad is the floor. A chest-high ray through the front opening and through the kitchen passage must miss, a ray into a side wall must hit, and the kettle and bed must sit in the kitchen and the couple room. A 42 cm body must enter, cross, and leave, or the save fails. Every actor's X, Y, and yaw must match the metrics sheet within 2 cm and 1 degree.

16. Space uses the jump already on the character, 420 cm/s. It does not add a second jump speed. In UE 5.8 the game reads `default_key_mappings` on the mapping context. `map_key` writes a deprecated list the game ignores, so Space does nothing until it is stored in `default_key_mappings`. Measured 2026-10-12 in play on `L_SizeTest`: that jump lifted the pawn 90 cm within one second, from 45102 to 45192. On the 2 m body the hop is visible. The speed stays 420 cm/s. On `SizeTest` a 25 cm sphere lags onto the right shoulder. It is a greybox follower, not a second character.

## Placement

Meters stay in the metrics file. That file is the approved layout. An image generator does not set distances. Models that emit numeric poses overlap and leave the floor; the layouts that hold use a written spec and then a constraint check. A 1 m grid is that check. It is not a tile the art must sit on. The approved coordinate can be any meter. The grid only rejects a solid footprint that shares a cell with another solid, or with the player capsule plus its clearance.

The placer in `Content/Python/scene_placement.py` reads the metrics file, snaps mesh bottoms to the measured floor top, measures them again, and refuses to save when any bottom is more than 2 cm off that top. It also refuses to save when the grid check or the capsule sweep fails. It sets yaw by name. Before that save it also overlaps a capsule of radius 42 cm and half-height 100 cm, expanded by 2 m of horizontal clearance, with its center 1 m above the floor. A hit on the island is the floor and is ignored. A hit on a cottage, pine, or rock fails the save. PCG and scatter brushes are for repeated dressing later. The homestead list is this metrics file. A Blender CSV export can feed that file later. It does not replace the check.

Solids block the pawn: island, cottage, pines, rocks. Plants do not: herb beds and lupines. A cone cluster used as blocking collision traps the capsule between the leaves. The floor under the island is one scaled field at the origin, so the homestead reads as floating above the plain. Camp, clouds, and the field gatherables are not part of this homestead test.


## A verified floor

A save is not a pass unless all six are true. A line that says the traces missed and then saved is not a pass. Run the check in the open editor. A headless `-nullrhi` run does not hit meshes.

1. `SM_Size_Island` has one box collision from the `pad` entry in `Docs/level/L_SizeTest_METRICS.md`, on the pad. The cone does not block. A hill is not this pad.
2. Five rays cast down onto that box all hit. Fewer than five hits fails the save. There is no fallback to the actor origin or the bounds max.
3. The highest hit is within 50 cm of the lowest. A larger gap is a hill.
4. The floor is the middle hit. Every homestead mesh bottom is within 2 cm of it.
5. The player capsule bottom is 10 cm above that floor, and the start is at least 5 m inside the pad.
6. A ray from the player start hits `SM_Size_Island` within 20 cm of that floor.

## Before you report

Do not tell the player a scene is done until the open editor has logged the pass. A description of the change is not that log. A material change is logged on the actors the player named. An imported mesh left on `WorldGridMaterial` is not painted, even when the cubes the placer spawned already wear the key. Headless `-nullrhi` does not hit meshes. A line through the middle of a gap is not a body: sweep the capsule radius. A hit read as an attribute is a miss. A position measured long after a one-second action is not that action.

For this map the pass is `scene_placement: CHECK PASS` and `scene_placement: cabin walk enter cross exit clear` from `Content/Python/verify_homestead_scene.py`, in the open editor, after the save. If either line is absent, the scene is not done. Fix it and run the script again before the reply. The same rule applies to the next map: name its verify script in `Docs/level/<Map>_CONTEXT.md` and do not report until that script logs its pass.

One change, then `Content/Python/verify_homestead_scene.py` in the open editor. That script measures and does not move or save. `apply_homestead_scene.py` is the writer: it places from the sheet and saves only when the same checks pass.

Do not start the next sitting on a failed check. The order for this homestead is the floor, then the face and the walk, then the placement sheet, then the door, then the hop and the shoulder sphere. The cottage sheet is kept. The wake minute on this map is the open play. This test does not replace the sheet.

## A new scene

1. Copy the practices above into `Docs/level/<Map>_CONTEXT.md`.
2. Measure the floor with five downward traces before the first place. Do not use the bounds max.
3. Write `Docs/level/<Map>_METRICS.md` with the player start, the actors that belong, and the ones that do not.
4. Point the placer at that metrics file.
5. After the first play, add any new measured failure to the practices list before the next scene.

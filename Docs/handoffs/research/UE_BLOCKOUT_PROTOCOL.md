# UE blockout protocol

Luke, 2026-10-17. Use this when the work is a prototype walk, a greybox floor, a sightline, or a first test of movement in a place. It is not the art transition, and it is not a hills pass.

## Ask

How Unreal tests basic movement and a blockout, and what HomeWorld uses while `Content/LevelPrototyping` is not in the project.

## Sources

- Epic, Designer 01: Project Setup and Level Blockout, Unreal Engine 5.8. https://dev.epicgames.com/documentation/unreal-engine/designer-01-project-setup-and-level-blockout-in-unreal-engine — retrieved 2026-10-17.
- Epic, Level Designer Quick Start, Unreal Engine 5.8. https://dev.epicgames.com/documentation/unreal-engine/level-designer-quick-start-in-unreal-engine — retrieved 2026-10-17.
- The walk-not-fly playtest is already in `EXIT_GAME_DESIGN_MOVEMENT_ENV_V1.md`. It was not fetched again.

## What Epic does

Blockout, also called graybox, is the layout before finished art. Simple shapes stand in for the floor, walls, and obstacles. The question is whether the space plays, not how it looks.

The 5.8 designer blockout uses `Content/LevelPrototyping/Meshes/SM_Cube`. That cube is 1 m on each side. Its grid material reads scale at a glance: dark lines are 1 m, the light floor lines are 0.1 m, and the light lines on a wall are 0.2 m. Ramps are `SM_Ramp` in the same folder. Test the scale as you resize.

The player starts at a Player Start. The blue arrow is the facing. Play is Play In Editor from that start, on the feet, with gravity and collision. Flying the editor camera is not the test.

## What this project uses

`Content/LevelPrototyping` is not in HomeWorld. Do not invent a second prototype material, and do not download a pack to fill that gap.

The cottage greybox is already `/Engine/BasicShapes/Cube`. A new floor, wall, or blocking prop in this kind of test uses that cube and the material already on that mesh. One mesh, one material, the pair the walls already show.

The field under the island is not the floor. The player stands on the blockout pad. A Player Start with nothing under it is a failed test.

Hills stay out of this test. `TERRAIN_HEIGHT_LATER.md`.

## Protocol

1. Name the walk. Where the feet start, which way they face, and what should come into sight.
2. Build that with the engine cube, plus props that are already in the map. No new material.
3. Put the Player Start on that floor, arrow aimed down the walk.
4. Play In Editor. Walk it. Do not judge it from the editor camera.
5. Change the block if the feet, the facing, or the sightline are wrong. Then walk it again.

## Keep, later, park

- KEEP. Engine cube and its current material for this prototype. Player Start on the pad. PIE walk.
- LATER. `SM_Cube` from LevelPrototyping, if that folder is added. It replaces the plain cube for the floor and walls. It does not add a second look beside it.
- PARK. A new greybox shader. Editor-camera approval. Treating the field under the island as the ground.

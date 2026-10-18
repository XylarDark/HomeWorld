# Terrain height, later

Luke, 2026-10-17. Hills and valleys are a later sightline modifier. They are not in the opening tutorial. Today's tutorial hides the cottage with a copse of pines and large stones.

## Ask

Catalog the work to add terrain height, and keep it off the tutorial that is being built now.

## Already in the repo

Not fetched again.

- The size-test floor is flat on purpose. `Docs/context/SCENE_SETUP.md` fails a save when the highest downward hit is more than 50 cm above the lowest. The cone under `SM_Size_Island` was that failure: its tip was read as the floor.
- The world island stays 660 m by 450 m, and the top stays 450 m above the plains. `Docs/WORLD_METRICS.md` and `Docs/context/HOMEWORLD_ROUTE.md`. A local hill does not move that drop.
- `L_VS_MVP_Markers` already has a Landscape. Replacing it with Mesh Terrain needs `APPROVE U58F-G`. The spike stays in the sandbox. `docs/UE/UE58_TECH.md` and `Docs/handoffs/U58F_G_MESH_TERRAIN.md`.
- PCG reads that Landscape by tag. The root Landscape can show no components while the streaming proxies hold them. `docs/KNOWN_ERRORS.md`.

## Later work

Do this after the opening tutorial has been played. Do not do it on `L_SizeTest` while that tutorial is the queue.

1. Choose the ground. A sculpt on the existing Landscape, or a few greybox ramps. Mesh Terrain stays in the sandbox until that approve.
2. Change the size-test floor check only for a map that is allowed to have relief. A hill there is a failed save until that check is rewritten on purpose.
3. Use the relief as a second way to hide a place, after the copse. The copse is the tutorial obscurer. The same pines and stones later become nodes a spirit can be set on, to gather over time. That gather is its own later system. It is not this file.
4. Replay the walk on a slope before any speed change. The kept walk is 450 cm/s on the flat pad.

## Not this tutorial

- No Landscape sculpt on `L_SizeTest`.
- No Mesh Terrain on the homestead.
- No change to the 50 cm floor rule until a later map asks for it.

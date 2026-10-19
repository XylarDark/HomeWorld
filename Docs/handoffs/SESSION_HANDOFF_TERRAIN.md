# SESSION_HANDOFF_TERRAIN

Slice: terrain height on the homestead island.
Job: the spec below is filled. Implement it only when a task asks. Do not sculpt from this file. Do not run the placer from this file. Do not add hills or heights the spec does not name.

## What you are looking at

The hills in play are the existing `SM_Size_Island` mesh on `/Game/HomeWorld/Maps/SizeTest/L_SizeTest`. It is the cone under the walk pad. The cone’s tip was already recorded as a false floor in [TERRAIN_HEIGHT_LATER.md](research/TERRAIN_HEIGHT_LATER.md). The pad is a separate flat cube. [Content/Python/scene_placement.py](../../Content/Python/scene_placement.py) writes a flat collision box from the pad size in [docs/level/L_SizeTest_METRICS.md](../../docs/level/L_SizeTest_METRICS.md). The grey cube steps in that sheet (`Hill_Step1`, `Hill_Step2`) are not this mesh. The placer has put those two on the map. `Hill_Step3` stays unplaced until glide.

The pawn walks the flat pad box. The spec says so. Do not change either surface until a task asks.

## Locks

- The opening walk stays flat: player start (−6, −58), spirit (−7, −29), cottage (−8, 0), copse gate, dog lane at x = 10.5. The 50 cm floor check still applies to traces on that walk. Water sheets and named hill steps are not that floor.
- The world drop stays 450 m. A local hill does not move it. [Docs/WORLD_METRICS.md](../WORLD_METRICS.md).
- No Landscape sculpt on `L_SizeTest` while the opening tutorial is the queue. The spec names a Landscape heightfield for later. No Mesh Terrain on the homestead. Mesh Terrain on `L_VS_MVP_Markers` still needs `APPROVE U58F-G`. [docs/UE/UE58_TECH.md](../../docs/UE/UE58_TECH.md), [U58F_G_MESH_TERRAIN.md](U58F_G_MESH_TERRAIN.md).
- The kept walk is 450 cm/s on the flat pad. A sloped replay happens before any speed change.
- The island samples already named in the metrics (farm plot, river, pond, overlook, cave notch) stay the places. Terrain follows those places. It does not invent new ones.

## Spec

Luke, 2026-10-18. Heights are not named. Do not invent them.

- Field look: `Field_hills_wide.jpg`, `Field_hills_pond.jpg`, and `Field_hills_crest.jpg` are kept. The rows are in [STILLS_LIBRARY.md](../art/STILLS_LIBRARY.md). They are the field biome. They are not homestead heights.
- Walked surface: the flat pad box. The opening walk stays on that pad.
- Ground system: one Landscape heightfield, when a map is allowed to have relief. Greybox along the graph edges is the blockout until that heightfield exists. `L_VS_MVP_Markers` keeps its Landscape. Mesh Terrain stays in the sandbox until `APPROVE U58F-G`.
- Hills: the east research hill, the spring in that hill, the hot springs at its foot, the river across the backyard, and the west fishing pond, plus `Hill_Step1` and `Hill_Step2`. `Hill_Step3` stays glide-gated and unplaced. No further hills. How tall is still unnamed.
- Graph: nodes peak, spring, hot spring, pond, and path sample. Edges river, ridge, and walk. The ridge is the east research hill. The river runs from the two springs to the west pond. Path samples on the walk stay at pad height. The names and the performance case are in [TERRAIN_TOPOLOGY.md](research/TERRAIN_TOPOLOGY.md).
- Cone: `SM_Size_Island` stays. Its collision stays the flat pad box until the heightfield replaces the visible cone.
- Later verb: a limited raise and level brush on that one heightfield, only after the opening walk has been played flat and the 50 cm floor check has passed. The opening has no brush. Caves and a fuller terraforming loop stay out.
- Placer contract: the metrics sheet lists those nodes and edges. [scene_placement.py](../../Content/Python/scene_placement.py) writes greybox along the relief edges, and writes height on the one heightfield only after the tutorial queue allows relief. The walk edge stays the flat pad. The 50 cm check stays on that spine.

## After the spec

1. Confirm the walked surface is the flat pad.
2. Keep the opening-walk traces on flat ground. Point the floor check at that walk.
3. The greybox stamp is in the metrics `graph` and tagged on the map. Verify logged `scene_placement: CHECK PASS top 45000.0` on 2026-10-18, with the river, ridge, and flat walk edges, and the heightfield skipped. The heightfield still waits until the opening tutorial has been played.
4. Replay the south approach before any other beat.

Compile with `.\Tools\Safe-Build.ps1` from the repo root only if C++ changes. Placement stays in the metrics file and `scene_placement.py`. One beat, then stop for a playtest. Do not commit unless asked.

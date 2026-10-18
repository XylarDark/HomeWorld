# UE pathing

One body. Walk surfaces, door gaps, and how an NPC follows a path without clipping. Collision rules live in `UE_COLLISION.md`.

## 2026-10-17 — Partner blocked by the island floor

Ask: path the partner through the south door to the kettle without turning collision off.

Already covered: nothing. This is the first entry.

Sources:

- Epic, Custom Navigation Areas and Query Filters in Unreal Engine 5.8, https://dev.epicgames.com/documentation/en-us/unreal-engine/custom-navigation-areas-and-query-filters-preparation-guide-in-unreal-engine , retrieved 2026-10-17. A Nav Mesh Bounds Volume is where the mesh is generated. An agent moves with Move to Actor. A query filter is a Filter Class on that move.
- Epic, Navigation System API, https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/NavigationSystem , retrieved 2026-10-17. `ANavMeshBoundsVolume` only blocks the path builder. It has no gameplay collision. `UNavigationSystemV1::FindPathToLocationSynchronously` is the synchronous query. `UNavigationQueryFilter` is the filter class.
- Epic forums, FindPathSync needs a query filter, https://forums.unrealengine.com/t/why-does-findpathsync-not-return-successful-path/1901983 , retrieved 2026-10-17. A null filter can fail the query. Pass `UNavigationQueryFilter`.

KEEP: If `UNavigationSystemV1::GetCurrent` has nav data, call `FindPathToLocationSynchronously` from the partner to the kettle and walk those points. If the path is missing or partial, use the doorway polyline. Do not invent a second path format.

KEEP: A walk surface is not an obstacle. `SM_Size_Island` and `SM_Size_WalkPad` are ignored by the partner sweep. The miss on 2026-10-17 was the capsule starting inside `SM_Size_Island`, so every step reported blocked and the partner never moved.

KEEP: The south door is already measured in `Content/Python/cabin_shell.py`. Cottage origin `(-800, 0)` cm. Entry local `x -290..-10` (center `-150`). Wall `y -280`. Porch lip `y -680`. World entry center `(-950, -280)`.

CANDIDATE: `RequestDirectMove` on a character-movement component, once the partner is a pawn. Not this pass. The partner is a skeletal mesh actor.

PARK: Turning collision off. Teleporting through `CabinWall_*`. A Nav Mesh Bounds Volume is not gameplay collision and does not replace the doorway.

## 2026-10-17 — Proximity mark is a key

Ask: the wisp should not orbit until the player asks.

Already covered: world confirm is E. Rune cursor is hold right mouse. See `.planning/research/INTERACT_INPUT_RESEARCH.md`.

New reuse, no new source file: Zelda puts the prompt up when you are near and one button confirms. Horizon and Ghost of Tsushima use a separate focus button before the mark. Okami uses one button to investigate and a different hold for the brush.

KEEP: Press Q to arm the mark. Press Q again to put it away. E still confirms. The orbit is in world space on the object, not parented to the player. Q is free. E, Shift, and right mouse are not.

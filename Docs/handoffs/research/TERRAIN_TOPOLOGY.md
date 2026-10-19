# Terrain topology

2026-10-18. How a topology graph can feed elevation when HomeWorld adds terrain height.

Ask: say what the placer would stamp, which ground system can hold it, and whether players should edit that ground. The spec is filled in the terrain handoff. This note leaves the placer unrun.

## Already recorded

[TERRAIN_HEIGHT_LATER.md](TERRAIN_HEIGHT_LATER.md) already holds the timing. Hills are a later sightline. The opening tutorial stays flat. The 50 cm floor check, the 450 m world drop, the `L_VS_MVP_Markers` Landscape, and the Mesh Terrain sandbox are in that file and in [SESSION_HANDOFF_TERRAIN.md](../SESSION_HANDOFF_TERRAIN.md). They were not fetched again. A local hill does not move the 450 m drop.

The terrain spec was filled on 2026-10-18. It lives in [SESSION_HANDOFF_TERRAIN.md](../SESSION_HANDOFF_TERRAIN.md). This file does not restate it. The three field stills are kept as the field biome, in [STILLS_LIBRARY.md](../../art/STILLS_LIBRARY.md). They are not homestead heights.

The decided layout this graph has to serve: a flat tutorial spine, and four yards. Front is crafting. North is the tame backyard. East is the research hill, with a spring in the hill and hot springs at the foot. A river crosses the backyard to a west fishing pond. Named samples already in the metrics (farm plot, river, pond, overlook, cave notch) stay the places.

## Sources

Retrieved 2026-10-18.

- The Level Design Book, Blockout. https://book.leveldesignbook.com/process/blockout
- Epic Games, Landscape Outdoor Terrain, Unreal Engine 5.8. https://dev.epicgames.com/documentation/en-us/unreal-engine/landscape-outdoor-terrain-in-unreal-engine?application_version=5.8
- Epic Games, Landscape Technical Guide, Unreal Engine 5.8. https://dev.epicgames.com/documentation/en-us/unreal-engine/landscape-technical-guide-in-unreal-engine?application_version=5.8
- Epic Games, Landscape Collision Guide, Unreal Engine 5.8. https://dev.epicgames.com/documentation/en-us/unreal-engine/landscape-collision-guide-in-unreal-engine?application_version=5.8
- Epic Games, Editing Landscapes, Unreal Engine 5.8. https://dev.epicgames.com/documentation/en-us/unreal-engine/editing-landscapes-in-unreal-engine?application_version=5.8
- Valheim Wiki (Weird Gloop), Map. https://valheim.weirdgloop.org/w/Map
- Valheim Wiki (Weird Gloop), Zones. https://valheim.weirdgloop.org/w/Zones
- Valheim Wiki (Weird Gloop), Building. https://valheim.weirdgloop.org/w/Building
- Valheim Wiki (Fandom), Hoe. https://valheim.fandom.com/wiki/Hoe

Repo facts, already recorded: `docs/UE/UE58_TECH.md`, `Docs/handoffs/U58F_G_MESH_TERRAIN.md`.

## 1. The graph

A topology graph here is nodes and edges the placer can stamp. The first artifact is that stamp.

KEEP: The parts are these.

- A ridge is a high edge. On this island that edge is the east research hill.
- A valley is a low edge. The river is that edge.
- A spring is a source node. One sits in the research hill. The hot springs at the foot are a second source node.
- An outlet is where that water arrives. The west fishing pond is the outlet.
- The walk spine is its own edge. Path samples are nodes on it. That edge stays flat until a spec says the walk may leave the pad.

CANDIDATE: When a spec accepts the names, the metrics list nodes `peak`, `spring`, `pond`, and `path sample`, and edges `river`, `ridge`, and `walk`. The hot spring is the second spring node, at the foot of the hill. The overlook stays a named sample the spec can bind to the peak. The cave notch stays a named sample. A heightfield stores one height per column, so the notch stays a placed volume on the hill.

PARK: Any hill formula, including one read off the field stills. This file has no heights.

## 2. UE 5.8 practice

KEEP: The performant ground, realistic or fantastical, is a Landscape heightfield. Epic's 5.8 Landscape system is the outdoor terrain tool. Each component stores its height in one texture. Sections are the LOD unit, and those LOD levels live in the texture mipmaps. Collision is that same heightfield. Collision Mip Level and Simple Collision Mip Level run from 0 (accurate, heavier) to 5 (cheaper, coarser). Epic's collision guide says most cases keep Collision Mip Level at 0 and Simple Collision Mip Level at 1 or 2.

KEEP: `L_VS_MVP_Markers` keeps its Landscape. Replacing it still needs `APPROVE U58F-G`. Mesh Terrain stays a sandbox spike on `/Game/HomeWorld/Maps/Sandbox/L_U58F_MeshTerrain`. The 5.8.2 tessellation guard stays in that sandbox note.

CANDIDATE: Greybox ramps are the blockout stamp of the graph, on a map the spec allows to have relief. The heightfield is the later ground, if the spec chooses Landscape. Once that heightfield exists, 5.8 Sculpt mode is Sculpt, Smooth, Flatten, Ramp, and Erosion. Paint mode blends material layers on that one surface, which is how the same ground can read as realistic or fantastical. The field stills are not that look yet.

CANDIDATE: A later river or ridge may be a Landscape Spline. 5.8 Manage mode adds splines. The walk spine stays a flat metric until the spec says it may leave the pad.

CANDIDATE: Landscape edit layers are the non-destructive path on the 5.8 Landscape page, so a later hill stamp can sit on its own layer. This note leaves them off.

PARK: Mesh Terrain as the homestead ground. A second surface under the walk, beside the pad the floor trace already reads.

## 3. Industry practice

The Level Design Book describes a blockout as a rough 3D draft of simple shapes, built and played before polished art, so the layout can still change cheaply.

KEEP: Block the graph first: the walk, the river, the pond basin, and the peak. Play that draft. Sculpt waits until the spec names the ground. The same page puts big shapes first, a ground plane set with Unreal's Flatten Target brush, and slopes as terraces before any smooth. One height authority answers the floor. On this project that lesson is already the cone under `SM_Size_Island`, whose tip was read as the floor. The walk spine is the readable corridor, the critical path the book asks a blockout to keep findable. Relief stays off that spine until the spec says otherwise. The copse remains the tutorial obscurer.

PARK: Erosion and auto-generators as the author of the hill. The same page says to skip them when the design needs control. The placer stamps the accepted graph.

## 4. Valheim, and whether players edit the ground

Valheim's explored map records biomes on a heightmap made at world generation. The world is zones of 64 m by 64 m. The game loads a 5 by 5 zone patch around the player, and it uses low-quality terrain after 180 m. That is a modest played distance.

The hoe elevates or levels the ground. Level ground pulls a patch toward the height under the player, or toward the aimed ground if shift is held. Raising ground spends 2 stone and needs a workbench nearby. The hoe lowers ground only a little. A pickaxe does the real dig. Pathen and paved road are paint. They leave the height alone. Building pieces snap. Shift turns snap off. Smooth is a Landscape sculpt brush. The hoe has no separate smooth mode.

The hoe page notes a cap of about 15–20 units from the generated mesh height. Other notes disagree on that exact cap. The number is Valheim's. It is not a HomeWorld height. The building page also warns that terrain edits add instances and can stutter.

KEEP: The comparable ground is one heightfield, loaded nearby, with coarser ground farther out, plus pieces that snap. A full voxel planet is the wrong cost for this island.

CANDIDATE: A limited raise and level brush on the homestead heightfield, after the opening walk has been played flat and the 50 cm floor check has passed. It is a later homestead verb. It edits that one heightfield.

PARK: Free voxel destruction, overhangs, and a cave dug out of the heightfield. PARK the rest of Valheim's terraforming loop (stone cost, workbench radius, earth-wall defense, path paint) until a spec asks for that verb. The opening tutorial has no terrain brush.

## 5. How the placer consumes the graph

KEEP: The opening walk spine stays flat until a spec says otherwise. The 50 cm floor check stays on traces along that spine. Water sheets and named hill steps are not that floor. The kept walk stays 450 cm/s on the flat pad. A sloped replay happens before any speed change, and only after the spec allows the walk to leave the pad.

CANDIDATE: Later, the metrics sheet lists the nodes and edges in section 1. `Content/Python/scene_placement.py` reads that list. Along a relief edge it writes greybox, the blockout stamp, or height on the one heightfield. Along the walk edge it keeps the flat pad. Path samples on that edge stay at pad height. The river edge runs from the hill springs across the backyard to the west pond. The ridge edge is the research hill. UE 5.8 also documents a Landscape Patch plugin that can change a heightmap procedurally. This contract does not choose that plugin. Heights come from the spec, when it exists.

PARK: Running the placer, or writing those metrics, from this note.

## 6. Performance

KEEP: One heightfield for the ground the spec allows to have relief. Material layers, painted in Landscape Paint mode, dress that surface. Collision comes from the heightfield, with a coarser collision mip only where a later pass needs the cost, inside Epic's 0-to-5 range. LOD comes from the Landscape section mipmaps. The tutorial does no runtime terrain-mesh rebuild. The raise and level brush is accepted in the spec. It waits until that walk has passed.

PARK: A unique mesh per hill. A runtime mesh rebuild during the tutorial. Mesh Terrain remesh on the homestead.

## Plan to proceed

Luke answered the interview on 2026-10-18. The five decisions are in [SESSION_HANDOFF_TERRAIN.md](../SESSION_HANDOFF_TERRAIN.md). This note still leaves the ground unsculpted, and it still leaves the placer unrun.

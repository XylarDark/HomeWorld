# Scale

One look. Two densities. Every transition from Concept on obeys this file. The build method in `Docs/02_ART_BIBLE.md` §5 is the law: cheap mass, a reusable detail kit, one living eye. This file says how that stays fast when the world is large and the lair holds a giant.

Play can change. The pictures cannot. A glide, a ram, a heal, and a night walk are the same pines, the same masters, and the same facet size.

## Three sizes

The player is 1.8 m and is not from this planet. The cottage is a normal home at the drawn plan. Ordinary creatures and plants are larger than the player. The bear and the bull match the cottage wall. The pines step up from that wall. The giant is the exception, many times the cottage. Locked 2026-10-10.

| Module | What uses it | Locked size |
|---|---|---|
| Player | The body and the camera | 1.8 m tall. Head about 0.3 m. |
| Cottage | The first home. Later building kits can be modular. This layout is the start. | 30 ft by 36 ft, walls 15 ft (4.57 m). Porch 30 ft by 8 ft. Living, kitchen, hall, child, bath, couple, as drawn. Door leaf 4 ft wide. Hall 8 ft deep. |
| Wild | Bear, bull, ordinary creatures, rocks | Bear shoulder and bull shoulder equal the cottage wall, 4.57 m. Other creatures may be smaller or larger than the cottage. Special animals and spirits may be otherwise. |
| Pines | One cone, three heights | Small 4.57 m. Medium 6.86 m. Largest 9.14 m. |
| Giant | The kneeling sleeper | Many times the cottage. The bull and the rider stay small on the back. The snake wraps the torso. |

These meters are the generation card. They were not measured off the pictures. A still can be kept for the relationship and still miss a number. When a prompt needs a size, paste the card. Do not ask the model to invent the meter from a scene. The file order is in `Docs/art/STILL_GENERATION_STANDARD.md`.

## Generation card

Paste the row you need. The figure in an asset shot is the 1.8 m player, standing next to the asset, not inside a scenic frame.

| Asset | Target | Picture that locks the look, not the meter |
|---|---|---|
| Player | 1.8 m tall. Head about 0.3 m. | The player mood stills. |
| Cottage | 9.14 m wide, 10.97 m deep, walls 4.57 m. Porch 9.14 m by 2.44 m. The drawn rooms. | `SM_Home_Cabin_doors.png` for the plan. The scenic stills do not lock the plan. |
| Door | 1.2 m clear width. Height is not locked. Hall behind it is 2.4 m deep. | The door plan. |
| Bear | Shoulder 4.57 m, the cottage wall. | The bear’s face and facets from the dusk picture. Not its height in that picture. |
| Bull | Shoulder 4.57 m. Player stands beside it. | `Field_bull_scale_v2.jpg` for the animal. The shoulder target is the cottage wall. |
| Pine, small | 4.57 m. | No kept sheet yet. |
| Pine, medium | 6.86 m. Same cone. | |
| Pine, largest | 9.14 m. Twice the cottage wall. | |
| Giant | Many times the cottage. No meter read off the picture. | `Lair_back_ride_v5.jpg` for the relationship only. |

The 14 m shell is retired. `HS_Shell_greybox.jpg` and `HS_Vista_bear_module_v9.jpg` show a cabin and a bear that do not match this card. They are not the greybox keep.

The 30 by 36 ft plan is the cottage, not a secret inside a larger shell. Door swings stay as drawn.

A scenic camera may lose the face. The play camera stays near the body, low, looking up, the way a small person sees a pallet they can walk under. The shoulder spirit is how that body stays readable up close.

## Vista

The wide shot is copies of a small kit. One pine. One rock. One lupine sprig. Turn them, scale them, and let the master material vary them. A thousand pines of one mesh is the forest. A thousand unique trees is not.

The player is small against the wild module. One warm eye sits far away: a cabin window, a fire, or the crystal. The moss-bear matches the cabin and the pines. The silhouette is the read. Moss, grain, and wear sit in the material, not in a mesh per clump.

Lights that cast shadows stay few. Windows are emissive on the wood master. Night is NightMix on the same mesh.

## Pocket

The close shot spends the unique meshes. The cabin, the player’s face, a beast’s head, the crystal, and the door are the hero exceptions already named in the bible. Onto that mass, snap the kit: moss clump, lupine sprig, fence, path stone, trim, one porch item, one bee or moth.

A piece that cannot be reused on three props is too unique. The pocket is denser because the camera is near, not because it uses a second style.

## The giant

The lair giant is one sleeper, and larger than the bear, the pines, the cabin, and the bull. The bull is wild-scale and still reads small on the back. The player rides that bull from the hip up to the head. Each coil comes off along that climb. The snake waits at the head. The cave is in the cliff. Ocean surrounds a small clearing at the mouth. The back is the place. The paid detail is the face and the snake’s eye. The mass stays faceted and cheap. When a mesh exists, the giant cap is 15,000 triangles. A vista may crop him. It does not get a second, heavier body.

The homestead moss-bear is the wild module made visible. Often cropped. One pose family, not a herd. The bull matches that module.

## Counts

These are the plan. They are not a captured frame.

| In one view | Plan |
|---|---|
| Animated characters | The slice needs the player, and then partner, child, three guards, or one bull. Stay under about twenty full characters before distant ones tick less often. |
| Unique meshes | Tens of kinds. Hundreds is the point to cut variety. |
| Pines, sprigs, rocks | Thousands of copies of one mesh. |
| Shadow-casting lights | A handful. |
| Spirit overlap | The shoulder mote, and one spirit body when someone is asleep. |

Nanite stays off the player, the flowers, the bugs, the moths, and any prop under a few thousand triangles. Hard edges fight Nanite simplification. Pines are solid facets. A masked leaf card still draws the trees behind it.

## What each transition checks

| Transition | The scale check |
|---|---|
| Concept | A vista shows the wild module: pines, lupines, and the cabin shell at the bear, the player small enough to stand under a bloom. The lair mouth shows a bull-length run and a giant whose back is a hill. |
| Concept → Greybox | Texture-off mass at the three modules. The cabin shell and the secret rooms are both blocked in. Copies, not a unique mesh per tree. No story lighting. |
| Greybox → Prototype | Faceted materials on the kit. Opaque pines. One front, side, and back for the mesh, then instances. |
| Prototype → Polish | The player’s face only. No new costume mesh. |
| Polish → Final | The poly caps. NightMix. Instances. No file in `Content/` until the pass bar is true. |

## Reject

A second tree species. A unique mesh per pine. A light in every window. A field of overlapping ghosts. A unique outfit on every guard. A second art style for a second way to play. A smoothed giant. A herd where the lock says one body. A human-sized cabin shell. A lair mouth the bull cannot charge. An ant-sized player.

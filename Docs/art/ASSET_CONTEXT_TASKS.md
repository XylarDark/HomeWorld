# Asset context tasks

Now: Concept → Greybox
Previous: Concept, kept 2026-10-10

The open transition is the work. The other four stay closed. Each transition is defined in [PHASES.md](PHASES.md). The open context is [transitions/CONCEPT.md](transitions/CONCEPT.md). Do not start the next one because a picture for it already exists.

One card per name in [PROTOTYPE_ASSET_BRIEFS.md](PROTOTYPE_ASSET_BRIEFS.md), plus the player. Order is homestead, descent and field, camp, barriers, lair last. One card’s stills per sitting. The next card waits until those pictures are kept or rejected.

## Sitting queue

Work these together, one at a time. A sitting ends when the stills are kept or rejected. Tripo and Meshy run only after that keep, from the front and the back of the same design. Mixar is the cleanup and the FBX export after the mesh exists. It does not invent the design.

Critical path, inside the open transition only. Items that belong to a later transition stay closed.

1. Player turnaround. Kept 2026-10-10. Identity sheet. It belongs to Greybox → Prototype. Closed while Concept is open.
2. Homestead wide, materials, night, and massing. Kept 2026-10-10. Wide and night are closer than 20 feet.
3. Cabin turnaround. Filed. Front, side, and back belong to Greybox → Prototype. Closed while Concept is open.
4. Partner still pack, then the child. The partner keeps one warm scarf. The player does not. Blocked until the cabin turnaround is kept or rejected.
5. Field and camp on the rescue loop. Clouds, wisp, landing, gathers, bull, clearing, three guards.

Later: bed, herb bed, kettle, edge, perch, shrine, barriers, and the lair after the mouth.

Future: dogs, cats, other animals and humanoids, and any second night mesh. Night stays NightMix on the same mesh.

## Stages

The five phases are states. The five transitions are the work. They are defined in `Docs/art/PHASES.md`.

| Asset | Pictures on file | Open transition |
|---|---|---|
| Player | Mood stills and a turnaround are filed. | Concept. The turnaround belongs to Greybox → Prototype. It stays closed. |
| Cabin | Mood stills, massing, the door plan, and a front elevation are filed. | Concept. Massing and the plan belong to Concept → Greybox. The front belongs to Greybox → Prototype. They stay closed. |
| Every other card | The card is written. | Concept. |

Status line: Transition is Concept → Greybox. The next file is the cottage asset sheet, alone, texture off. Open `Docs/art/transitions/CONCEPT_TO_GREYBOX.md` and `Docs/art/STILL_GENERATION_STANDARD.md`. Do not make another scene first.

Do not generate a mesh from text. Image-to-3D runs only after the stills on that card are kept. Do not check a box in [PROTOTYPE_ASSET_TRACK.md](PROTOTYPE_ASSET_TRACK.md) from this file. Do not copy a file into `Content/`.

Night is NightMix on the same mesh. A spirit still is a look, not a second model.

## Why the card looks like this

A hand modeler and a multi-view image-to-3D tool both fail the same way: one pretty view, and the unseen side gets invented. The back view is the usual invention. Front plus back, at the same height and the same light, is the pair that holds the design. Side and three-quarter complete it. Callouts name the material. A short don’t list stops the drift.

Tripo and Meshy multi-view take front (required), left, back, and right. Those views must be this design, not a second guess. Faces and limbs that bend stay a shape reference, then a hand mesh. A rigid prop may be decimated.

Hex swatches stay out until a still is accepted.

## Shared still pack

Check only what that card needs.

- Front, side, back, three-quarter. Same height. Plain background. Same light.
- Close material callout.
- Play camera near the body, about 20 feet, when the brief asks. Wild size is `Docs/art/SCALE.md`, not this distance.
- Texture off.
- Plan, only if the place has rooms.
- Spirit-form still, only if the subject is a sleeper. Same mesh later.

Tool, named only after the stills are kept:

- Rigid prop: Tripo, under 4,000 triangles.
- Bull or guard body: Meshy, under 8,000, and only if it must match the last accepted mesh.
- Giant: under 15,000 after decimate.
- Partner, child, guards, and the bull’s face and legs: hand mesh. Do not keep an AI retopo on a face or a bending limb.
- Rodin only for a close hero still, and only if the facets survive.

Status words: not started, context filed, stills for audit, kept.

## Player

Sleeper. Identity line, verbatim: dark coat, small spirit on the shoulder, faceted face, adult head about one sixth of height. The scarf in the expression sheet is not the signifier. The shoulder spirit is always spirit and is not its own mesh.

Reject: a scarf as the signifier, a weapon, a second body for night, text, a rune.

Stills filed, no mesh. Status: concept mood kept 2026-10-10. The turnaround stays closed until Greybox → Prototype.

- [x] Texture off, full body. [SM_Player_body_texture_off.jpg](player/SM_Player_body_texture_off.jpg)
- [x] Homestead, looking back. [SM_Player_homestead_lookback.jpg](player/SM_Player_homestead_lookback.jpg)
- [x] Field, standing. [SM_Player_field_stand.jpg](player/SM_Player_field_stand.jpg)
- [x] Camp approach. [SM_Player_camp_approach.jpg](player/SM_Player_camp_approach.jpg)
- [x] Spirit form. [SM_Player_spirit_form.jpg](player/SM_Player_spirit_form.jpg)
- [x] Front, side, back, three-quarter at one height. [SM_Player_turnaround.jpg](player/SM_Player_turnaround.jpg)

## Homestead

### SM_Home_Cabin

Wake read. A bear-sized shell with player-sized rooms inside. The shell matches the moss-bear. The rooms are 30 ft by 36 ft, porch 30 by 8, walls 15 ft. Living 17 by 14, kitchen 12 by 14, hall 8 ft with no door leaf, child 10 by 13, bath 8 by 9, couple 11 by 13. Leaf doors are 4 ft and park inside the room. A bear does not fit that door. Kitchen is an iron stove, a kettle, and one sink.

Reject: a modern appliance, a door leaf in the hall, a rune, text.

Status: stills for audit. Wide and night are closer than 20 feet.

- [x] Plan. [SM_Home_Cabin_doors.png](cabin/SM_Home_Cabin_doors.png)
- [x] Wide dusk. [HS_Wide.jpg](homestead/HS_Wide.jpg)
- [x] Close materials. [HS_Materials.jpg](homestead/HS_Materials.jpg)
- [x] Night. [HS_Night.jpg](homestead/HS_Night.jpg)
- [x] Texture-off massing. [HS_Massing.jpg](homestead/HS_Massing.jpg)
- [x] Front, side, back at one height. Filed for audit. [HS_Turnaround.jpg](homestead/HS_Turnaround.jpg)
- [ ] Tool: Tripo, under 4,000, only after the views are kept

### SM_Home_Bed

Sleep is the form change. Sleeper’s bed, not a creature. Low wooden bed, one quilt, faceted posts, readable from the couple’s door. No rune.

Reject: a rune, a second night bed.

Status: not started.

- [ ] Front, side, back, three-quarter
- [ ] Close quilt and posts
- [ ] About 20 feet, from the door
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SK_Partner

Stands by the bed. Sleeper. Same face planes as the player. Muted clothes. One warm scarf, so the loved one still reads when taken. Not a portrait render.

Reject: a different face, a cage, a weapon.

Status: mood still for audit. [SK_Partner_homestead_mood.jpg](player/SK_Partner_homestead_mood.jpg). Built from the kept north stars and the player mood set. One warm scarf. The child waits.

- [ ] Face planes
- [ ] Front, side, back, three-quarter, day
- [ ] Texture off
- [ ] Verb pose, standing by the bed
- [ ] Spirit-form still
- [ ] Tool: shape reference, then a hand mesh

### SK_Child

Garden, then the edge. Sleeper. Same face planes. Playing stance. The point reads with the whole body. Child head about four to five heads. Does not enter the lair.

Reject: text, a rune, an adult head size.

Status: not started. Same sitting as the partner.

- [ ] Face planes
- [ ] Front, side, back, three-quarter, day
- [ ] Texture off
- [ ] Verb pose, pointing with the body
- [ ] Spirit-form still
- [ ] Tool: shape reference, then a hand mesh

### SM_Home_HerbBed

First gather. Raised garden, herb clusters, faceted leaves, child-height, close camera. Distinct from the field herb.

Reject: a face in the leaves, photoreal plants.

Status: not started.

- [ ] Front, side, back, three-quarter
- [ ] Close leaves
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SM_Home_Kettle

Tea, day sprint. Kettle and two cups on a stump, herb steam, faceted metal, close camera.

Reject: a modern appliance, a second kettle for night.

Status: not started.

- [ ] Front, side, back, three-quarter
- [ ] Close metal
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SM_Home_Edge

Cliff the child plays at. Homestead rim, pines, a gap toward cloud, faceted stone lip, player for scale.

Reject: a HUD, a pancake edge.

Status: not started.

- [ ] Wide, player at about 20 feet
- [ ] Close stone lip
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SM_Glider_Perch

Day launch. Lookout pad, simple rail, faceted timber, open sky, player for scale. No flight HUD.

Reject: a HUD, a tech rail.

Status: not started.

- [ ] Front, side, back, three-quarter
- [ ] About 20 feet, player for scale
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SM_Shrine_Homestead

Night portal. Standing stone, about twice player height, faceted, no tech, no glow paint, dusk. The way home from the lair reuses this mesh.

Reject: a tech portal, a rune, glow paint.

Status: not started.

- [ ] Front, side, back, three-quarter
- [ ] About 20 feet, player beside it
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

## Descent and field

### SM_CloudLayer

The descent. Soft faceted cloud shelves, gaps a glider can steer through, warm above and cool below. No HUD.

Reject: a HUD, a solid wall of cloud.

Status: not started.

- [ ] Wide, player small against the shelves
- [ ] Side, so the gaps read
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SM_CloudWisp

One carried wisp. Always spirit. Small faceted light mote, readable at 20 feet, no face. No second body.

Reject: a face, a second night model.

Status: not started.

- [ ] Front, side, back, at 20 feet
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SM_Field_Landing

Walk returns. Open pine-edge clearing, faceted grass clumps, one worn circle, player for scale.

Reject: a HUD marker, a second circle.

Status: not started.

- [ ] Wide, player at about 20 feet
- [ ] Close worn circle
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SM_Gather_Herb

Day reap. Herb cluster on a faceted stump, close camera. Not the homestead bed.

Reject: the homestead herb-bed silhouette.

Status: not started.

- [ ] Front, side, back, three-quarter
- [ ] Close leaves
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SM_Gather_Wood

Day reap. Fallen faceted branch, readable at 20 feet.

Reject: a standing tree, photoreal bark.

Status: not started.

- [ ] Front, side, back
- [ ] About 20 feet
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SM_Gather_Berry

Day reap. Low berry bush, faceted fruit, close camera.

Reject: fruit that only reads as a color blob up close.

Status: not started.

- [ ] Front, side, back, three-quarter
- [ ] Close fruit
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SK_Bull

Field ride, later the lair ram. Sleeper. One mesh. Faceted barn bull, calm, saddle-free, player beside it. Do not make a second.

Reject: a boss read, a saddle, a second bull.

Status: not started.

- [ ] Front, side, back, three-quarter, day
- [ ] Texture off
- [ ] Player beside it
- [ ] Spirit-form still
- [ ] Tool: Meshy under 8,000 for the body if it must match. Face and legs are a hand mesh.

## Camp

### SM_Camp_Clearing

Sightline from outside. Pine camp, one fire, three posts, path in from the trees. No HUD marker.

Reject: a marker, a rune, armed-brute props.

Status: not started.

- [ ] Approach from outside, player small
- [ ] Wide of the clearing
- [ ] Close fire and one post
- [ ] Night, fire as the only warm
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SK_Guard_A

Ease, then a lair wound. Sleeper. Same face planes as the player. Tired, leaning, muted coat. The stick is not a weapon render.

Reject: a different species, a weapon render, a new face.

Status: not started.

- [ ] Face planes
- [ ] Front, side, back, three-quarter
- [ ] Texture off
- [ ] Verb pose, leaning
- [ ] Spirit-form still
- [ ] Tool: shape reference, then a hand mesh. Body cap 8,000 if a draft is kept only as reference.

### SK_Guard_B

Same family. Sitting, one arm held in.

Reject: a different species, a weapon render.

Status: not started.

- [ ] Face planes
- [ ] Front, side, back, three-quarter
- [ ] Texture off
- [ ] Verb pose, sitting
- [ ] Spirit-form still
- [ ] Tool: shape reference, then a hand mesh

### SK_Guard_C

Same family. Standing watch. The stick is a stick.

Reject: a club, a sword, a bow, a different species.

Status: not started.

- [ ] Face planes
- [ ] Front, side, back, three-quarter
- [ ] Texture off
- [ ] Verb pose, standing watch
- [ ] Spirit-form still
- [ ] Tool: shape reference, then a hand mesh

### SK_Partner_Taken

The stake. Reuse `SK_Partner`. Seated, unbound, same scarf, no cage. No new mesh and no new turnaround.

Reject: a cage, a new face, a new scarf.

Status: not started. One pose still after `SK_Partner` is kept.

- [ ] Seated pose of the same person
- [ ] Tool: none. Same hand mesh.

## Barriers

### SM_Forest_FogTree

Local eject, not a trip home. Thick faceted pine in fog. One trunk reads as a shove. No face in the bark.

Reject: a face, a second tree species, a portal home.

Status: not started.

- [ ] Front, side, back
- [ ] About 20 feet
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SK_River_Fish

Local eject to the bank. Sleeper animal. One leap, readable at 20 feet, not a boss.

Reject: a boss scale, a second fish.

Status: not started.

- [ ] Front, side, back of the leap
- [ ] About 20 feet
- [ ] Texture off
- [ ] Spirit-form still
- [ ] Tool: Tripo under 4,000 if the body stays rigid. A bending body is a hand mesh.

## Lair

Do this last. Day is coil one and coil two only. The eye is a light cone, not a mesh. The title card is UI.

### SM_Lair_Mouth

First minute of the cave. Dark faceted arch, kneeling silhouette inside, scary not grim, player for scale. Stop the lair if this fails as a thumbnail.

Reject: grimdark, text, a bright tech mouth.

Status: not started.

- [ ] Wide, player for scale
- [ ] Front of the arch
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SM_Lair_Giant

The place you ride. Sleeper. Both knees, back-to-head about 30 degrees, player on the calf. Face planes readable.

Reject: a slope you cannot walk in your head, a second giant.

Status: not started.

- [ ] Side, so the 30 degree back reads
- [ ] Front and back
- [ ] Player on the calf
- [ ] Texture off
- [ ] Spirit-form still
- [ ] Tool: under 15,000 after decimate. Face is a hand mesh.

### SM_Lair_Coil01

Full-speed ram. Snake coil on the giant’s back, snake mid-slide. The loose scale is a separate mesh.

Reject: the scale modeled into this coil.

Status: not started.

- [ ] Front, side, back
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SM_Lair_ScaleLoose

The ram tell. One bright plane, readable at 20 feet.

Reject: a scale that disappears into the coil.

Status: not started.

- [ ] Front and side
- [ ] About 20 feet
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SM_Lair_Coil02

Tickle drops it. Underside you can walk to. Lighter skin plane.

Reject: a coil with no walkable underside.

Status: not started.

- [ ] Underside view
- [ ] Side
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SM_Lair_SideRoom

Heal the guards. A pocket between coil two and coil three. Three bed rolls. Not a new zone.

Reject: a new zone, more than three rolls.

Status: not started.

- [ ] Wide of the pocket
- [ ] Close bed rolls
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SM_Lair_Coil03

Guards push. No loose scale. Opening toward the side room.

Reject: a loose scale on this coil.

Status: not started.

- [ ] Front, side, back
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SM_Lair_HeadBind

Head heal is the ask. Loop at the head. One dull eye plane. No line of text.

Reject: text, a bright gem eye, a rune.

Status: not started.

- [ ] Front of the head
- [ ] Side of the loop
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

### SM_Lair_Pool

A read, not a place. In frame below the chest. Rim only. No walkable bottom.

Reject: a pool you can enter.

Status: not started.

- [ ] Rim, from the side
- [ ] Texture off
- [ ] Tool: Tripo, under 4,000, after keep

## Not a mesh

- The giant’s eye is a light cone.
- The title card is UI.
- The way home reuses `SM_Shrine_Homestead`.
- Partner seated reuses `SK_Partner`.

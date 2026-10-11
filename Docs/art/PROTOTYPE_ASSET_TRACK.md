# Prototype asset track

| Field | Value |
|---|---|
| Status | OPEN. Human sitting. No Lead stamp. |
| Date | 2026-10-08 |
| Briefs | [PROTOTYPE_ASSET_BRIEFS.md](PROTOTYPE_ASSET_BRIEFS.md) |
| Notes | [VISUAL_NOTES_FOR_GENERATION.md](VISUAL_NOTES_FOR_GENERATION.md) |
| Lair shape | [../context/BOSS_LAIR_LOCK.md](../context/BOSS_LAIR_LOCK.md) |
| Policy | Do not promote a generated mesh into `Content/`. [../20_UASSET_AI_POLICY.md](../20_UASSET_AI_POLICY.md) |

Check a box only when that step's pass bar is true. Do not skip ahead. Stop the place if its first mesh fails.

## How to run one step

1. Paste the prompt from the briefs file. Append the paste block from the notes file. Every time.
2. Reject the image if the silhouette fails as a thumbnail, or if a priority note fails (size, planetoid, calm, no text). Generate again. Do not mesh a failed image.
3. Image to mesh. Tripo for a draft. Meshy if you want a budgeted stylized mesh. Rodin only for a close still.
4. Blender hand pass: texture off, silhouette holds, facet planes, pivot at the contact, scale applied, no baked light, box collision, name from the briefs.
5. Look from the play camera near the body, and from the scenic camera. Same mesh. Do not rescale. Wild size is `Docs/art/SCALE.md`.
6. Check the box. Next step.

Poly caps: prop under 4,000 triangles, bull or guard under 8,000, giant under 15,000 after decimate.

## PA-1 Homestead

- [ ] **PA-1.1 Cabin** `SM_Home_Cabin`. Pass: warm windows read at 20 feet, wood is faceted, player scale is obvious.
- [ ] **PA-1.2 Bed** `SM_Home_Bed`. Pass: readable from the door, one quilt, no rune.
- [ ] **PA-1.3 Partner** `SK_Partner`. Pass: brow, lid, and mouth are planes. One warm scarf. Not a portrait render.
- [ ] **PA-1.4 Child** `SK_Child`. Pass: same face planes, playing stance, the point reads with the whole body.
- [ ] **PA-1.5 Herb bed** `SM_Home_HerbBed`. Pass: herbs read at close camera, child-height.
- [ ] **PA-1.6 Kettle** `SM_Home_Kettle`. Pass: kettle and two cups read as the tea beat. Close camera.
- [ ] **PA-1.7 Edge** `SM_Home_Edge`. Pass: a stone lip and a gap toward cloud. This is where the child will show the fog later.
- [ ] **PA-1.8 Perch** `SM_Glider_Perch`. Pass: a launch pad, open sky, no flight HUD.
- [ ] **PA-1.9 Shrine** `SM_Shrine_Homestead`. Pass: standing stone, about twice player height, no tech glow.

Place pass: cabin, bed, partner, child, kettle, and edge can sit in one gray homestead. If the child does not read next to the bed, stop.

## PA-2 Descent and field

- [ ] **PA-2.1 Clouds** `SM_CloudLayer`. Pass: shelves with gaps a glider could steer through. Warm above, cool below.
- [ ] **PA-2.2 Wisp** `SM_CloudWisp`. Pass: readable at 20 feet, no face.
- [ ] **PA-2.3 Landing** `SM_Field_Landing`. Pass: open clearing, one worn circle, walkable read.
- [ ] **PA-2.4 Herb** `SM_Gather_Herb`. Pass: one cluster, close camera, distinct from the homestead bed.
- [ ] **PA-2.5 Wood** `SM_Gather_Wood`. Pass: a fallen branch, readable at 20 feet.
- [ ] **PA-2.6 Berry** `SM_Gather_Berry`. Pass: low bush, fruit reads close.
- [ ] **PA-2.7 Bull** `SK_Bull`. Pass: calm, saddle-free, player beside it. This mesh is the lair ram. Do not make a second.

Place pass: landing, three gathers, and the bull read as one field. If the bull reads as a boss, simplify it.

## PA-3 Camp

- [ ] **PA-3.1 Clearing** `SM_Camp_Clearing`. Pass: path in, one fire, three posts, sightline from outside, no marker.
- [ ] **PA-3.2 Guard A** `SK_Guard_A`. Pass: same face planes, tired, leaning.
- [ ] **PA-3.3 Guard B** `SK_Guard_B`. Pass: same family, sitting, one arm held in.
- [ ] **PA-3.4 Guard C** `SK_Guard_C`. Pass: same family, standing watch. The stick is not a weapon render.
- [ ] **PA-3.5 Partner seated** reuse `SK_Partner`. Pass: seated, same scarf, no cage.

Place pass: three guards and the partner read from outside the clearing. If a guard reads as a different species, redo that one.

## PA-4 Barriers

- [ ] **PA-4.1 Fog tree** `SM_Forest_FogTree`. Pass: one trunk reads as a shove. No face in the bark. Local eject, not a trip home.
- [ ] **PA-4.2 Fish** `SK_River_Fish`. Pass: one leap, readable at 20 feet, not a boss.

## PA-5 Lair

Do this last. Day is coil one and coil two only.

- [ ] **PA-5.1 Mouth** `SM_Lair_Mouth`. Pass: dark arch, kneeling silhouette inside, scary not grim. Stop the lair if this fails as a thumbnail.
- [ ] **PA-5.2 Giant** `SM_Lair_Giant`. Pass: both knees, back-to-head about 30 degrees, player on the calf. Stop if you cannot walk that slope in your head.
- [ ] **PA-5.3 Coil one** `SM_Lair_Coil01`. Pass: coil on the back, snake looks mid-slide.
- [ ] **PA-5.4 Loose scale** `SM_Lair_ScaleLoose`. Pass: a separate bright plane, readable at 20 feet. This is the ram tell.
- [ ] **PA-5.5 Coil two** `SM_Lair_Coil02`. Pass: underside you can walk to, lighter skin plane. The tickle drops this coil.
- [ ] **PA-5.6 Side room** `SM_Lair_SideRoom`. Pass: a pocket between coil two and three, three bed rolls, not a new zone.
- [ ] **PA-5.7 Coil three** `SM_Lair_Coil03`. Pass: no loose scale. Opening toward the side room.
- [ ] **PA-5.8 Head bind** `SM_Lair_HeadBind`. Pass: loop at the head, one dull eye plane. The head heal is the ask. No line of text.
- [ ] **PA-5.9 Pool** `SM_Lair_Pool`. Pass: in frame below the chest, rim only, no walkable bottom.

The eye is a light cone, not a mesh. The title card is UI. The way home reuses the homestead shrine.

## Not this track

A second bull. A rune. A mesh in `Content/`. A stealth minigame. A pool you can enter. A spoken title. LODs before a mesh survives the two-camera look.

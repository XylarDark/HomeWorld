# Visual notes for generation

Home sitting sheet. 2026-10-08. Law stays in `Docs/02_ART_BIBLE.md`. Product direction stays in `Docs/VISION_BOARD.md`. This file turns the priority notes into rules a generator will not drift from.

Paste the block at the bottom of every image prompt. Reject the image if any note fails.

## How studios do this

They do not generate volume and then look for the vision. They lock shape, proportion, color logic, lighting intent, and the out-of-style list on a few hero shots, then write those as rules. A mood board alone is not a brief. Out-of-style examples matter as much as the in-style ones. A color script is a production document: one palette frame per place, not one palette for the whole game.

For this sitting, the hero shots already exist in the art bible: dusk homestead, player face sheet, planetside camp test. Generate against those, not against a new style.

## The notes, as rules

| Note | It looks like | It fails if |
|---|---|---|
| Immersion | The place teaches itself. Path, fire, window, and the loose scale are the only signs. No HUD, no text, no markers. | A label, a quest arrow, a UI frame. |
| Size | The player is a ruler. The world is large. Beasts and the giant crop the frame. Default camera is about 20 feet. | A toy scale, a giant the size of a horse, assets rescaled per camera. |
| Beauty | Faceted masses with life on the planes: grain, moss, petals, crystal faces. Warm handmade. | Photoreal, smoothed clay, poster bands, scan wood. |
| Healing | Care is the verb. A wound is a thing you approach. A healed place is the same shape, warmer. | Gore, a kill pose, a boss health bar, a rebuilt mesh for night. |
| Calm | Quiet ground, one warm eye (window or fire), no clutter. Emotion is climate around the same silhouette. | Grimdark, mud gray, pitch black, a second tree species. |
| Planetoid | Close horizon, ground bending away, thin air, deep zenith, readable stars, a moon that is not a white speck. | A pancake island, a flat skybox, a sci-fi planet render. |
| Adventure | An edge you could step off, a path into pines, a bull you could ride, a cave mouth. | A free-flight sim, a locked door, a cutscene frame. |
| Spirit | Standing stone, cyan as a jewel not a lawn, a see-through gap, night is the same mesh with NightMix. No rune. | A tech portal, neon ring, a second night model, a rune stone. |
| Fantasy | Cartoon, not Disney. Zelda readability, Pixar sincerity. Not high fantasy. | Ornate armor, a chosen-one cape, a Disney princess, grim high fantasy. |

## Cousins, and what to take

| Game | Take | Leave |
|---|---|---|
| Breath of the Wild | Silhouette teaches the place. Warm vs cool. The world is large and the player is small. | The UI density. The combat. |
| Journey / Abzu | Scale makes wonder without making you powerless. One warm color against a cool field. Quiet. | The desert or the ocean as a biome. The anonymous hood. |
| Outer Wilds | Camping on a small world. Close horizon. Rustic, not NASA chrome. The look serves the place. | The time loop. The hard sci-fi instruments. |
| Spiritfarer | Care is the axis. A place should make you want to be there. Healing is comfort, not a spell effect. | The 2D boat. The death ferry. The animal cast. |
| Pixar | Face planes that act. One warm accent. Sincerity. | The toy smoothness. The big eyes past our lock. |

## Place scripts

One dominant temperature per place. Do not mix them in one image.

| Place | Temperature | The eye | Player job in the frame |
|---|---|---|---|
| Homestead | Warm dusk, cool forest right | One brighter window | Looking back, or the child at the edge |
| Descent | Warm above, cool below | One wisp | Small against the shelves |
| Field | Open day, quiet ground | The bull, planted | Beside the bull, not on it yet |
| Camp | Night, fire as the only warm | The fire | Approaching from outside the sightline |
| Lair | Cool cave, one warm wound or window-scale light | The loose scale, then the head | Small on the 30 degree back |

## Drift to ignore when generating

The art bible still has a planetside still of three armed brutes, and an appendix row for a rune. Product direction wins for this sitting. Guards are tired people with the player's face planes, not a new species and not a weapon render. The rune is removed. Night is the same meshes.

## Paste block

```
HomeWorld. Faceted semi-polygon, detail on the planes, not flat low poly, not photoreal, not a toy. Cartoon fantasy, warm handmade, Zelda readability, Pixar sincerity, not Disney, not high fantasy, not grim. Player small, world large, close horizon, thin air, deep zenith. One warm eye against cool. No text, no HUD, no rune, no gore, no tech portal. Plain background.
```

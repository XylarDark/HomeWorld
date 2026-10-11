# Prototype asset briefs

Home session kit. 2026-10-08. Shape only. Not a prove.

Follow [PROTOTYPE_ASSET_TRACK.md](PROTOTYPE_ASSET_TRACK.md). One step, pass bar, then the next. This file is the prompt list.

Build in play order. Homestead first, lair last. Paste one image prompt. Reject it if the silhouette fails as a thumbnail. Then image-to-mesh. Tripo for a draft, Meshy for a budgeted stylized mesh, Rodin only for a close still. Do not promote a generated mesh into `Content/`. See `Docs/20_UASSET_AI_POLICY.md`.

Style on every prompt: faceted semi-polygon, detail on the planes, cartoon fantasy, warm handmade, not photoreal, not a toy, not high fantasy, not grim. Small player in the corner for scale. Plain background. No text.

Hand pass on every mesh: silhouette with texture off, facet planes, pivot at the contact, scale applied, no baked light, simple collision, name from this file.

Two cameras, same mesh. The play camera stays near the 1.8 m body. The scenic camera shows the bear module. Do not rescale a mesh per camera. Modules: `Docs/art/SCALE.md`.

Poly caps: prop under 4,000 triangles, bull or guard under 8,000, giant under 15,000 after decimate.

## 1. Homestead

Wake, family, herb, tea, edge. Sleep at the bed is the form change. The child shows the fog lift from the edge later, and does not enter the lair.

| Name | Verb | Prompt |
|---|---|---|
| `SM_Home_Cabin` | Wake read | Small handmade cabin, warm windows, faceted wood, moss on the planes, night-safe glow in the glass, three-quarter, player for scale. Exterior 30 by 36 ft, porch 30 by 8, walls 15 ft. Living 17 by 14, kitchen 12 by 14 with stove, kettle, sink only. Hall 8 ft deep, no door leaf in it. Child 10 by 13, bath 8 by 9, couple 11 by 13. Every leaf door is 4 ft, swings into its own room, and parks flat on the nearest side wall. |
| `SM_Home_Bed` | Sleep is the form change | Low wooden bed, one quilt, faceted posts, readable from the door, no rune. |
| `SK_Partner` | Stands by the bed | Faceted young adult, muted clothes, one warm scarf, brow lid and mouth planes, neutral, three-quarter, not a portrait render. |
| `SK_Child` | Garden, then the edge | Small faceted child, same face planes, playing stance, points with the whole body, no text. |
| `SM_Home_HerbBed` | First gather | Raised garden, herb clusters, faceted leaves, child-height, close camera. |
| `SM_Home_Kettle` | Tea, day sprint | Kettle and two cups on a stump, herb steam, faceted metal, close camera. |
| `SM_Home_Edge` | Cliff the child plays at | Homestead rim, pines, a gap toward cloud, faceted stone lip, player for scale. |
| `SM_Glider_Perch` | Day launch | Lookout pad, simple rail, faceted timber, open sky, player for scale. |
| `SM_Shrine_Homestead` | Night portal | Standing stone, twice player height, faceted, no tech, no glow paint, dusk. |

## 2. Descent and field

Steered glide, one sign, no pickup. Land, gather, bull.

| Name | Verb | Prompt |
|---|---|---|
| `SM_CloudLayer` | The descent | Soft faceted cloud shelves, gaps a glider can steer through, warm above and cool below, no HUD. |
| `SM_CloudWisp` | One carried wisp | Small faceted light mote, readable at 20 feet, no face. |
| `SM_Field_Landing` | Walk returns | Open pine-edge clearing, faceted grass clumps, one worn circle, player for scale. |
| `SM_Gather_Herb` | Day reap | Herb cluster on a faceted stump, close camera. |
| `SM_Gather_Wood` | Day reap | Fallen faceted branch, readable at 20 feet. |
| `SM_Gather_Berry` | Day reap | Low berry bush, faceted fruit, close camera. |
| `SK_Bull` | Field ride, later the lair ram | Faceted barn bull, calm, saddle-free, player beside it, three-quarter. Reuse this mesh in the cave. Do not make a second. |

## 3. Camp

Day the loved one is taken. Night, ease three guards to sleep. Same three later in the lair.

| Name | Verb | Prompt |
|---|---|---|
| `SM_Camp_Clearing` | Sightline from outside | Pine camp, one fire, three posts, path in from the trees, faceted, no HUD marker. |
| `SK_Guard_A` | Ease, then lair wound | Faceted guard, same face planes as the player, tired, leaning, muted coat. |
| `SK_Guard_B` | Ease, then lair wound | Same family, sitting, one arm held close. |
| `SK_Guard_C` | Ease, then lair wound | Same family, standing watch, spear as a stick not a weapon render. |
| `SK_Partner_Taken` | The stake | Partner seated, unbound look, same scarf, faceted, no cage mesh. Reuse `SK_Partner`. |

## 4. Barriers

If you wander past the loop. Local eject. Not a trip home.

| Name | Verb | Prompt |
|---|---|---|
| `SM_Forest_FogTree` | Boots you to the forest edge | Thick faceted pine in fog, one trunk that reads as a shove, no face in the bark. |
| `SK_River_Fish` | Boots you to the bank | One large faceted fish mid-leap, readable at 20 feet, not a boss. |

## 5. Lair

After the camp rescue. Scary cliff mouth. Day is coil one and coil two only. Night is heals, the side room, their push, the eye, the head heal.

| Name | Verb | Prompt |
|---|---|---|
| `SM_Lair_Mouth` | First minute of the cave | Cliff cave mouth, dark faceted arch, kneeling silhouette inside, scary not grim, player for scale, no text. |
| `SM_Lair_Giant` | The place you ride | Atlas sleeper, both knees, back-to-head about 30 degrees, faceted stone-and-wood body, moss on the planes, face planes readable, player on the calf for scale. |
| `SM_Lair_Coil01` | Full-speed ram | Snake coil on the giant's back, one loose scale as a separate bright plane, snake sliding pose, faceted. |
| `SM_Lair_ScaleLoose` | The tell | Single loose scale, faceted, high contrast, readable at 20 feet. |
| `SM_Lair_Coil02` | Tickle drops it | Underside coil, sensitive skin as a lighter plane you can walk to, faceted. |
| `SM_Lair_SideRoom` | Heal the guards | Small cave pocket between coil two and coil three, three bed rolls, not a new zone. |
| `SM_Lair_Coil03` | Guards push, no scale | Third coil, no loose scale, side opening toward the room. |
| `SM_Lair_HeadBind` | Head heal is the ask | Snake loop at the giant's head, one eye as a dull plane, faceted. |
| `SM_Lair_Pool` | A read, not a place | Dark pool in the frame below the chest, no walkable bottom, faceted rim. |

The eye is a light cone in-engine, not a mesh. The title card is UI. The way home reuses `SM_Shrine_Homestead`.

## Sitting order

Follow the track. Prompts are above.

1. Cabin, bed, partner, child, herb bed, kettle, edge, perch, shrine.
2. Cloud layer, wisp, landing, herb, wood, berry, bull.
3. Camp clearing, three guards, partner seated.
4. Fog tree, river fish.
5. Cave mouth, giant, coil one, loose scale, coil two, side room, coil three, head bind, pool.

Stop a place if its first mesh fails the thumbnail. Do not skip ahead to the lair. Export names stay as in the tables. Pivot at the contact. Collision is a box. No second bull. No rune.

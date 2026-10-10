# Art bible context

Working packet for art-bible sittings: stills, the cabin, interiors, and generation. Open this with `Docs/context/FORK_ART.md` or `Docs/context/FORK_ASSET.md`. The law stays in `Docs/02_ART_BIBLE.md`. When a cabin fact changes, write it here and in the bible in the same edit.

Updated 2026-10-10, interview locks 1–4. `SM_Home_Cabin` is not kept yet. The plan below is the spec. Exploratory stills are not accepted pictures.

## Slogans

Three lines. Lighting, models, and places obey all three. The paste block stays.

- The place teaches itself.
- Safe home above a living world.
- One warm eye against the cool.

## Materials

A prop’s material must suggest its use. Wood reads as wood. Cloth reads as cloth. The iron stove reads as a cookstove. A modern appliance fails.

## Test figure

The expression-sheet person must belong in a homestead still, a field still, and a camp still. Dark coat, a small spirit on the shoulder, the six face planes. The scarf in the sheet is not the signifier. If that person looks wrong in the picture, the place fails. The shoulder spirit’s light takes five steps, one per stack. No number, no bar.

Some creatures are spirit by day and by night. Animals and humanoids have a day body and a spirit form, and they enter the spirit realm only while asleep. Dogs, cats, other animals, and other humanoids will follow that pair. The player is a sleeper. The shoulder spirit is always spirit.

Audit stills, 2026-10-10:

![Player, texture off](../art/player/SM_Player_body_texture_off.jpg)

![Player at the homestead](../art/player/SM_Player_homestead_lookback.jpg)

![Player in the field](../art/player/SM_Player_field_stand.jpg)

![Player approaching camp](../art/player/SM_Player_camp_approach.jpg)

![Player spirit form](../art/player/SM_Player_spirit_form.jpg)

## Pictures

These three files are the basis. The old `.b64` names were never files in the repo. `refs/keyart_homestead_night.jpg` and `refs/keyart_homestead_planetside_split.jpg` stay historical.

| File | Role |
|---|---|
| `VisionBoard/KeyArt/homestead_dusk_baseline.jpg` | Dusk homestead. Player looking back, warm cabin, lupines, crystal shrine, cropped moss-bear. |
| `VisionBoard/KeyArt/player_expression_sheet.jpg` | Face lock. Calm, smile, worry, awe, determination, startle. Dark coat. Shoulder spirit, not the scarf in the sheet. |
| `VisionBoard/KeyArt/homestead_close_assets.jpg` | Lupine and bee, porch, shrine crystal and moth. |

Paste block and place scripts stay in `Docs/art/VISUAL_NOTES_FOR_GENERATION.md`. Prompts stay in `Docs/art/PROTOTYPE_ASSET_BRIEFS.md`.

## Cousins

| Source | Take | Leave |
|---|---|---|
| Nintendo, Satoru Takizawa | One slogan set that lighting, models, and weather obey. Materials readable enough to suggest use. Large shapes mark, medium shapes hide, small shapes change the rhythm. | *Wind Waker*’s biggest cartoon lies. A style that reads as made for small children. |
| Blizzard, Samwise Didier | Silhouette and big color at the distance you play. Cut detail until the shape holds. | Bulk, broken armor, primary-color teams, metal album art. |
| Blizzard, Bill Petras and Arnold Tsang | A hopeful place. Readability before ornament. One familiar person used to test every new place. Paint the vision, then prove it. | Combat silhouette arms race, weapons, neon tech. |
| Pixar color scripts | A few tent-pole pictures, then one small color frame per beat. Ask what fails. | Toy-smooth surfaces and eyes past the face lock. |

## Generation

Paste the block whole. Change only the subject. Each attached picture has one job.

| Picture | Job |
|---|---|
| `homestead_dusk_baseline.jpg` | Place, light, and materials. |
| `player_expression_sheet.jpg` | The person. |
| `homestead_close_assets.jpg` | Close wood, flower, and crystal. |
| `Docs/art/cabin/SM_Home_Cabin_doors.png` | The plan and the door swings. |
| `Docs/art/homestead/HS_Wide.jpg` | Homestead wide. |
| `Docs/art/homestead/HS_Materials.jpg` | Close wood, stone, herb, stove, kettle. |
| `Docs/art/homestead/HS_Night.jpg` | Homestead at night. |
| `Docs/art/homestead/HS_Massing.jpg` | Texture-off cabin massing. |

Identity line, verbatim: dark coat, small spirit on the shoulder, faceted face, adult head about one sixth of height.

Reject at thumbnail size. Change one thing per new still. A generated floor plan does not replace the door drawing. The image tool swings doors into the hall. Do not accept that.

## Cabin

One lived-in house. Exterior body 30 ft wide by 36 ft deep (9.14 m by 10.97 m). Porch 30 ft by 8 ft on the front. Log walls 6 in. Interior 29 ft wide by 35 ft deep. Wall height 10 ft. Player about 1.8 m. Each bedroom is its own room: at least 70 sq ft and 7 ft on every side.

Front (south) to back (north):

- Living room, front left, 17 ft by 14 ft. Chimney and wood stove on the west wall. Seat and table north of the front-door swing.
- Kitchen, front right, 12 ft by 14 ft. One wood counter on the east wall: a simple iron cookstove, a kettle on the stove, one sink. No refrigerator, no second sink, no modern range.
- Hall, full width, 8 ft deep. No door leaf in the hall.
- Child’s room, back left, 10 ft by 13 ft. Twin bed on the west wall.
- Bathroom, back center, 8 ft by 9 ft, closet 8 ft by 4 ft behind it. Tub on the north wall. Toilet and basin on the east wall, clear of the swing.
- Couple’s room, back right, 11 ft by 13 ft. Queen bed, 5 ft by 6 ft 8 in, on the north wall, shifted east. The open doorway shows the bed from the hall.

Diagram: `Docs/art/cabin/SM_Home_Cabin_doors.png`. Redraw source: `Docs/art/cabin/draw_cabin_doors.py`.

## Doors

Every leaf is a 4 ft clear opening. It is hinged in a corner, swings 90 degrees into its own room, and parks flat against the side wall. The swing arc is empty. No leaf swings into the hall. The kitchen opening and the living-to-hall opening are 5 ft cased openings with no leaf.

- Front door: southeast corner of the living room. Leaf parks on the wall shared with the kitchen.
- Child: southeast corner. Leaf parks on the east wall.
- Bath: southwest corner. Leaf parks on the west wall.
- Couple: southwest corner. Leaf parks on the west wall. The west side of the room is the door pocket.

The image tool draws those swings into the hall. Do not accept that drawing. The PNG above is the plan.

Why these sizes, not a 4 ft house hall:

- Game doors are about 1.2–1.5 m. A real leaf is about 0.8–0.9 m. The capsule does not turn sideways. [Numivo scale cheat sheet](https://www.numivo.org/blog/level-design-scale-cheat-sheet)
- A third-person camera sits behind the player and clips in a corridor tighter than about 2 m. This hall is 8 ft (2.44 m). It is not a fight corridor. [Numivo scale reference](https://www.numivo.org/tools/scale-reference)
- A hinged door sweeps a quarter circle and traps anything in the arc. [The Level Design Book: Doors](https://book.leveldesignbook.com/process/scripting/doors)
- The camera needs air above a 1.8 m player, so the walls are 10 ft. [The player’s camera is everything](https://gellenor.medium.com/the-players-camera-is-everything-78749eccdf69)

## Stills library

Index: `Docs/art/STILLS_LIBRARY.md`. One card per asset: `Docs/art/ASSET_CONTEXT_TASKS.md`. One place, then stop for audit. Do not generate the next place in the same sitting. Nothing here is copied into `Content/`.

A place pack: wide with the player at about 20 feet, an approach or sightline, close materials, night only if the light changes, texture-off massing when the silhouette is the pass, and an interior plan only when the place has rooms.

A sleeper (player, partner, child, guards, bull, later dogs and cats): face or head planes, full body day texture off, the verb pose, and a spirit form entered only while asleep.

An always-spirit creature (the shoulder spirit, the cloud wisp, and later kin): one form for day and night, readable at 20 feet, no second body.

Each accepted still has one job. Paste the block whole. Attach only the pictures that job needs.

## Homestead sitting

Lock, 2026-10-10. First generate is the place, four angles: wide, close materials, night, texture-off massing. Partner and child are the next sitting. The cabin door plan and the player homestead look-back are inputs, not the finished pack.

## Sitting rules

One unchecked step, then stop. Do not promote a mesh into `Content/`. Do not check a track box until the pass bar is called true. Homestead, then field, then camp.

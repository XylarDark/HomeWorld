# Still generation standard

Kept 2026-10-10. Wired from `Docs/context/ART_ASSET_DOOR.md`.

A model sheet is a contract. Image tools are stateless. A new prompt without the kept picture invents a new design. Dimensions belong in the prompt. Numerals in the picture become garbage text, and the art bible already bans text.

## Catalog

Five kinds. The index is `Docs/art/STILLS_LIBRARY.md`. Every new file gets a row and a job before the next file is made. A scene does not replace a missing sheet.

| Kind | Job | Order |
|---|---|---|
| Mood scene | Light, place, and how the pieces sit. Not a meter. | A few. Already started. |
| Asset sheet | One subject. Flat light. Plain ground. The 1.8 m figure stands beside a prop. | Before another scene of that subject. |
| Turnaround | Front, then 90, 180, and 45 degrees. Each file attaches the kept front. | After that front is kept. |
| Callout | One hidden detail: door, face, horns, bark. | Only when the sheet hides it. |
| Scene again | Kept sheets placed together. | After the sheets. |

The open greybox sheets, in order, are the cottage, the pine, the bear, and the bull. The lair is already a scale keep and is not in this set. Meters are pasted from `Docs/art/SCALE.md`. The picture does not invent the meter.

An image model copies the attached picture and ignores a typed size. Do not attach a scene whose scale is wrong. One change per pass. Free local generation, when a card can hold a reference, is ComfyUI with an edit model such as FLUX.1 Kontext. That holds a face or a prop across views. It does not measure 4.57 m. Hosted free tiers are for a first mood, not for a sheet.

## Rules

1. Name the meters in the prompt. Player is 1.8 m. Head is one sixth of that height. A place uses the meters on its card. Do not print those numbers in the picture.
2. One kept picture is the design. Every later view attaches that picture. Do not attach a picture whose job is different.
3. Keep one front first. Camera at the subject’s mid-height. Orthographic. 0 degrees. Subject fills about 80 percent of the frame height. Equal margin. Flat light. No cast shadow. Plain light-gray background.
4. Side is 90 degrees. Back is 180 degrees. Three-quarter is 45 degrees. Each is its own file, attached to the kept front. Same frame fraction, same light, same ground line. A side that is another front is a failed side.
5. A prop sheet has no person in frame. Scale is the meters. The player stands in the mood still and the 20-foot still only.
6. A character sheet is an A-pose: arms slightly off the body, open hands, so the mesh does not fuse the arms to the coat. Head is one sixth of height.
7. Name the asymmetric side: chimney on the cabin’s right, spirit on the player’s left shoulder, scarf on the partner. The back view keeps that side. It does not mirror it.
8. One job per image. One change per reject. Name the view that failed. Do not rewrite the design in the retry.
9. Generate the set in one sitting. After a keep, Tripo or Meshy gets the separate files `Name_front`, `Name_side`, `Name_back`, `Name_threequarter`. Front is required. Front plus back stops the tool inventing the unseen side. Do not feed a back the image tool invented and then treat that guess as truth.

## Check before you show it

- Crown, shoulders, waist, and feet would sit on the same lines.
- Frame fraction matches the front.
- The named side did not flip.
- No person on a prop sheet.
- No text.

If one line fails, regenerate that view only.

## Prompt blocks

Paste the meters, then one of these, then the style block.

Prop:

```
Orthographic. Camera at mid-height. 0 degrees for front, 90 for side, 180 for back, 45 for three-quarter. Subject fills 80 percent of the frame height. Same ground line. Flat light. No cast shadow. Plain light-gray background. No person. No text. No extra props. Copy the attached front. Do not mirror the named side. Do not redesign the hidden side.
```

Character:

```
Orthographic. Camera at mid-height. 0 degrees for front, 90 for side, 180 for back, 45 for three-quarter. Full body fills 80 percent of the frame height. A-pose, arms slightly off the coat, open hands. Head one sixth of height. Same ground line. Flat light. No cast shadow. Plain light-gray background. No text. Copy the attached front. Do not mirror the named side. Do not redesign the hidden side.
```

## Reject

- A mood still used as the mesh input.
- A person standing in a prop sheet.
- A side view that is another front.
- Height, frame fraction, or ground line that does not match.
- Arms fused to the coat.
- A chimney, pouch, or spirit that flipped sides.
- A new prop, a new color, or a scarf on the player.
- Text, a HUD, or a rune.
- An unseen side that was not in the kept picture.

## Cabin, as a test

The cabin shell matches the bear. The room plan inside it is 30 ft by 36 ft, porch 30 by 8, walls 15 ft. Chimney on the cabin’s right. Modules: `Docs/art/SCALE.md`. A front elevation of the rooms is not a picture of the shell. Side and back attach the kept front of that same subject. They do not describe a new house.

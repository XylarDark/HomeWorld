# Opening tutorial tasks

The sequence is the Opening tutorial in [`Docs/VISION_BOARD.md`](../VISION_BOARD.md). This file is the work order. It does not copy that sequence.

Play is `L_SizeTest`. One beat at a time. A beat is done when its check has passed in the open editor and Luke has replayed that beat. The ease pad is not this queue.

The uncommitted edit already on [`Docs/level/L_SizeTest_ROOM_PLAN.md`](../level/L_SizeTest_ROOM_PLAN.md) stays. A beat that moves the player, the partner, or the child updates [`Docs/level/L_SizeTest_METRICS.md`](../level/L_SizeTest_METRICS.md) and only the position sentences in the room plan.

## Beat 1 — the copse, then the walk

The cottage is hidden by a copse of the existing pines and large stones, on the north side of the house. The player start is beyond that copse, facing the house. The partner and the child wait at the south door, out of that view. No hill. Terrain height is [`Docs/handoffs/research/TERRAIN_HEIGHT_LATER.md`](../handoffs/research/TERRAIN_HEIGHT_LATER.md).

`Content/Python/scene_placement.py` places from the metrics sheet.

Pass: `scene_placement: CHECK PASS` and `scene_placement: cabin walk enter cross exit clear` from `Content/Python/verify_homestead_scene.py` in the open editor. Luke replays only the approach.

Then the wheel, on this map only, from the picked slowest speed to 450 cm/s. A C++ test covers the steps. Luke replays the same walk and scrolls.

## Beat 2 — herb, spirit, child, shoulder

No new mesh. A greybox spirit and one herb sit halfway along the approach. Picking the herb uses the existing garden pick. The child runs from the door and offers a greybox wisp. Combining that wisp with the herb and giving it to the spirit heals it. The shoulder sphere already on `L_SizeTest` becomes that landing.

The wisp shows no pair yet. Night wisp rules in [`Docs/context/HOMEWORLD_ROUTE.md`](HOMEWORLD_ROUTE.md) stay. This offer is the tutorial pair, not a third night wisp.

Before the offer draws a rune, open the next interview round. The healing pair is not one of the seven names. Choices: Grace, Love, or leave the greybox unmarked. Recommend leave it unmarked until the handoff has been played.

The yard unveils while the player is still moving. There is no locked camera. The child starts toward the spirit at that crest. The crest is far enough that the child arrives at the same time or sooner, even if the player covers the gap at 585 cm/s.

Luke replays only this beat.

## Beat 3 — home and chores

Before anyone walks with you, open the next interview round.

| Id | Choice |
|----|--------|
| 1 | The partner stays at the door. You walk back. The welcome is there. |
| 2 | When the spirit is healed, the partner comes to you and walks back beside you. The welcome is at the door. |

Recommend 2. The opening says you walk home with the partner.

The kettle and the herb beds already exist (`TryNodeKettleInteractInFront`, `NODE_GARDEN`). This beat uses them. No new hint line. The place is the teacher.

Luke replays the return, one herb, and the kettle.

## Beat 4 — the two stations

Combining the herb and the wisp makes the consumable station usable. A greybox table is enough. No recipe beyond that unlock.

Before the armor gift changes a number, open the next interview round.

| Id | Choice |
|----|--------|
| 1 | The partner gives a visible piece. The armor table becomes usable. Speed and bonk tries stay as they are. |
| 2 | The piece also adds one bonk try. |
| 3 | Skip the gift until the mist beat. |

Recommend 1. The change, remove, and alter sentences in [`Docs/VIRTUE_ATTRIBUTE_BIBLE.md`](../VIRTUE_ATTRIBUTE_BIBLE.md) stay off this build list.

Luke replays the unlocks only.

## Beat 5 — mist, bonk, glide

A mist volume around the homestead. Jumping off while it is up launches you back onto the island. That launch is the bonk lesson. It does not turn on the stroke draw. `BeginStrokeFromInput` stays off on `L_SizeTest`.

Before the mist can clear, open the next interview round.

| Id | Choice |
|----|--------|
| 1 | The mist clears after the heal, one herb pick, and the kettle. The stations only have to be unlocked. |
| 2 | The mist clears only after you also use each station once. |
| 3 | The mist stays until you say the homestead is done. |

Recommend 1. The chores named in the opening are the herbs and the kettle. The stations are unlocks.

When it clears, the existing glide can start. Luke replays the jump-off, then the clear.

## Later

Not this queue.

- A random sin/virtue pair on cloud wisps that are not this offered one.
- Family lines past a single hint.
- The consumable recipe and the armor table’s alter loop.
- Camp, the field greybox re-run, and the ease pad.
- Hills and valleys. [`Docs/handoffs/research/TERRAIN_HEIGHT_LATER.md`](../handoffs/research/TERRAIN_HEIGHT_LATER.md).
- Setting a spirit on the copse to gather over time.

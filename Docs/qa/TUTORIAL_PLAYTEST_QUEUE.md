# Tutorial playtest queue

Play one pass. Fill its result. Stop. Bring the result back before the next pass.

Map for every pass that uses the opening: `/Game/HomeWorld/Maps/SizeTest/L_SizeTest`. Stand on the walk pad. The field under the island is not the floor. Do not sprint. The opening wheel is fine. Judge the walk at the top step, 450 cm/s.

`Docs/canon/PLAYTEST.md` has other uncommitted edits. Write results in this file.

**Now:** Pass 2b. Passes 3–8 stay blocked until those beats exist in the build.

---

## Pass 1 — The approach

**Ready.** Detail: `Docs/qa/TUTORIAL_ISLAND_PLAYTEST.md`.

Walk from the south start, through the trees and rocks, to the partner at the south door, at the top wheel step only (450 cm/s). Do not time the slower steps.

Pass when the cottage stays hidden until you are through the copse, the partner is standing outside the door facing you, and the pad still feels like one short approach.

Do not play the herb, the heal, the kettle, the mist, or the glide.

| Field | Result |
|---|---|
| Date | 2026-10-17 |
| Commit | |
| Speeds | Fine. Judge the top step only. |
| Cottage hidden by the copse | Yes. The copse needs more of the same trees and rocks. |
| Pad size | Good enough for this pass. |
| Partner | Fixed after the first look. Same model as the player, facing you. |
| Child and spirit | Child runs to the spirit, stays visible, and follows you back after the interact. Shoulder spirit starts off and appears on that interact. |
| Dialogue | Child and partner say nothing. Accepted for this pass. |
| Pass or fail | Pass. 2026-10-17. |

---

## Pass 2 — What this build already teaches

**Ready.** One walk at 450 cm/s. Dialogue is not part of this pass. Do not force a beat that is not there. Write what happens.

| Check | What happened |
|---|---|
| Does the yard come into view while you are still walking? | Not reported. |
| Does the child move toward a spirit? | Yes. The child followed you after the interact. |
| Spirit interact | Pass. The sphere disappeared and the shoulder spirit appeared. It was off at the start. |
| Can you pick a herb? | Pass. |
| Can you use the kettle? | Pass. Clicking it worked. |
| Shift to speed up | Pass. |
| If you jump off the pad, do you come back? | Not tried. |
| One sentence | Herb, kettle, and shift pass. 2026-10-17. |

A missing beat is a note, not a failure. Stop there.

---

## Pass 2b — Cursor, indicator, partner inside

**Ready.** Same map. Top step, 450 cm/s. Dialogue is still not this pass.

1. E confirms the object the wisp is marking. Hold the right mouse button for the rune cursor. Walking still works. Let go and the cursor leaves. A left click does not use the herb or the kettle.
2. Take the spirit. The shoulder wisp appears. Look at the kettle, a herb, or the partner. The wisp should float around the one you are locked onto.
3. Interact with the partner at the door. They should walk inside and stop beside the kettle. The child can follow you. That is not a fail if the child is still outside.

Pass when the cursor does not stop your walking, the wisp marks the locked target after the spirit is taken, and the partner ends beside the kettle.

| Check | Result |
|---|---|
| Hold E shows a cursor, and walking still works | Not reported. |
| Let go and the cursor leaves | Not reported. |
| After the spirit, the wisp floats around the locked target | Pass. Floated around the herbs and the partner. Kettle not checked; expected to work. |
| Partner walks inside to the kettle | Fail. Clipped through the wall. Collision-off is rejected. Real path is scheduled, not this pass. |
| Pass or fail | Indicator pass. Door path fail. 2026-10-17. |
| What felt wrong | Partner blocked at the door, stuttering. |

---

## Pass 3 — The heart on the wisp

**Blocked.** The wisp does not yet show Love as a heart.

When it does: one walk at 300 cm/s through the offer. Pass if you notice the heart without being told its name, and you are not asked to choose an axis.

| Field | Result |
|---|---|
| Date | |
| Noticed the heart without a name? | |
| One sentence | |

---

## Pass 4 — The bench, once

**Blocked.** The one commit is not built.

When it is: the partner says “Place it, turn it, commit.” Do that once. No second mark. Pass if the motion is clear and you are not choosing among axes.

| Field | Result |
|---|---|
| Date | |
| Finished the one commit? | |
| One sentence | |

---

## Pass 5 — The bonk

**Blocked.** Beat 5 is not the playable opening.

When it is playable: jump off while the mist is up. You come back onto the island. The first bonk does not slow the step and does not dim the shoulder light. Pass if you come back at once, you understand “not yet,” and you can continue the beat.

| Field | Result |
|---|---|
| Date | |
| Came back at once? | |
| Understood not yet? | |
| Tried again? | |
| One sentence | |

---

## Pass 6 — The marked herb

**Blocked.** The field herb is not placed.

When it is: after the glide, find the herb, pick it if you want, and bring it home to the bench. There is no second unused hook. Pass if the herb reads as the same kind of mark as the heart, and you can ignore it without getting stuck.

| Field | Result |
|---|---|
| Date | |
| Found it? | |
| Picked it? | |
| Connected it to the heart and the bench? | |
| One sentence | |

---

## Pass 7 — The whole opening

**Blocked.** Passes 3–6 have to exist in the build.

Play from the south start through the glide and the herb. Time the whole thing. Pass if you could say what the game is asking, the opening does not feel longer than a short visit, and you want to keep going. Do not look for a second unused object.

| Field | Result |
|---|---|
| Date | |
| Total time | |
| Could say what you were supposed to do? | |
| Wanted to continue? | |
| One sentence | |

---

## Pass 8 — Five new players

**Blocked.** Needs the opening those five people will actually play, and five people who have not played HomeWorld. Protocol: `.planning/research/ONBOARDING_PLAYTEST_PROTOCOL.md`.

Skip any beat in that protocol that is not in the build. Do not score a second unused hook. The bench is one commit. The herb is the hook.

Write a ranked list of the beats that failed, with a quote or a timestamp for each.

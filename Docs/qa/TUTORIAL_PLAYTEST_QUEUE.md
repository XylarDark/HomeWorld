# Tutorial playtest queue

Play one pass. Fill its result. Stop. Bring the result back before the next pass.

Map for every pass that uses the opening: `/Game/HomeWorld/Maps/SizeTest/L_SizeTest`. Stand on the walk pad. The field under the island is not the floor. Do not sprint. The opening wheel is fine. Judge the walk at the top step, 450 cm/s.

Write results in this file. The tutorial is one day on the island. The field is the first wild place, after the dawn glide. It is not a pass here.

Current pass entry: [`PLAYTEST_INDEX.md`](PLAYTEST_INDEX.md). This file owns the tutorial day only. The party and home-loop passes are separate.

**Now:** Night on the island, below. The bonk passed 2026-10-18. The glider is round 8 in [`Docs/context/OPENING_TUTORIAL_INTERVIEW.md`](../context/OPENING_TUTORIAL_INTERVIEW.md). It is not built. The water/sign chain is design-only.

**Built since the last pass:** the companion party (#319/#325) and the home-loop host bites 1-8/10. Neither is a tutorial beat. The `home_loop` quest chain is stored when the opening day ends.

The midday slice below is passed. 2026-10-18.

---

## Passed — Midday on the island

**Passed.** 2026-10-18. One walk at 450 cm/s. This is the start of the day. Do not replay it as the next pass.

- The approach, the copse, and the pad. The copse can take more of the same trees and rocks. That note is polish, not an open pass.
- The spirit claim and the shoulder wisp. The wisp starts off and appears when the spirit is claimed.
- The child runs to the spirit, follows, then goes to their room.
- Both herb hearts, the chunk bank, and the kettle. One brew spends at most 10. The partner line switches to the kettle once any chunks are banked.
- The partner walks inside and waits by the kettle. Tea sprint works.
- The counter and where the partner stands beside it are light polish, not a pass.

| Check | Result |
|---|---|
| Approach, copse, pad | Pass. 2026-10-17. Copse can take more of the same trees and rocks. |
| Spirit and shoulder wisp | Pass. 2026-10-17. |
| Herb hearts and kettle | Pass. 2026-10-18. Chunks bank with no cap. One brew spends at most 10. |
| Partner inside, child to their room | Pass. 2026-10-18. |
| Tea sprint | Pass. 2026-10-17. |
| One sentence | The played opening is the midday start. 2026-10-18. |

---

## Crafting stations

**Passed.** 2026-10-18. Replayed the unlocks, top step, 450 cm/s. Pass with the replay changes, now in the build: the kettle sits on the kitchen counter, the counter is the consumable station, and the armory slid in front of the cottage onto the courtyard.

| Field | Result |
|---|---|
| Date | 2026-10-18 |
| Consumable station opened? | Yes. The kitchen counter, opened with the herb and the claimed spirit. |
| Armor table opened? | Yes. "The partner gave the armor and when I went to the armory it was open." |
| One sentence | Pass with the replay changes: kettle on the counter, the counter is the station, the armory on the front courtyard. |

---

## The dog

**Passed.** 2026-10-18. Played on the island. The procedure stays in [`Docs/context/OPENING_TUTORIAL_INTERVIEW.md`](../context/OPENING_TUTORIAL_INTERVIEW.md).

| Field | Result |
|---|---|
| Date | 2026-10-18 |
| The child raced to the yard after the brew? | Pass. |
| Knocked away when too close or too fast? | Pass. |
| Grace eased the Wrath? | Pass. |
| Mixed herb tamed the dog? | Pass. |
| One sentence | Everything passed. Tweaks are left and not named. |

---

## The backpack

**Passed.** 2026-10-18. Round 6 in [`Docs/context/OPENING_TUTORIAL_INTERVIEW.md`](../context/OPENING_TUTORIAL_INTERVIEW.md). The kept walk stays 450 cm/s.

| Field | Result |
|---|---|
| Date | 2026-10-18 |
| The gift is a backpack you can see? | Pass, with the rest of this play. |
| Materials stay out of it? | Pass, with the rest of this play. |
| The armory table opens? | Pass, with the rest of this play. |
| Walk speed and bonk tries unchanged? | Pass, with the rest of this play. |
| One sentence | Playtest successful. Everything worked. |

---

## Fishing

**Passed.** 2026-10-18. After the dog. Round 5 in [`Docs/context/OPENING_TUTORIAL_INTERVIEW.md`](../context/OPENING_TUTORIAL_INTERVIEW.md). One fish. No minigame.

| Field | Result |
|---|---|
| Date | 2026-10-18 |
| At the pond, press E? | Pass, with the rest of this play. |
| One fish? | Pass, with the rest of this play. |
| No minigame? | Pass, with the rest of this play. |
| One sentence | Playtest successful. Everything worked. |

---

## The wisp

**Passed.** 2026-10-18. The placement for a short prop is in [`Docs/level/L_SizeTest_CONTEXT.md`](../level/L_SizeTest_CONTEXT.md).

| Field | Result |
|---|---|
| Date | 2026-10-18 |
| Tall prop at head height, on your right? | Pass. |
| Kettle and dog just above and to the right? | Pass. The kettle sat beside it. Short props now float above the top and past the right face. |
| Cursor during the heart and the dove, then home? | Pass. |
| Both beds back after 20 seconds? | Pass. The herb-bed wisp can sit a little further out. That gap is the same short-prop change. |
| One sentence | Everything passed. The short-prop spot was the only tweak. |

---

## The bonk

**Passed.** 2026-10-18. The mist is not part of it. The return lands further inland than the lip.

| Field | Result |
|---|---|
| Date | 2026-10-18 |
| Came back at once? | Pass. |
| Step stayed the same? | Pass. |
| Shoulder light stayed the same? | Pass. |
| Could continue? | Pass. |
| One sentence | It works. Send the landing further into the island. |

---

## Night on the island

**Built.** Waiting on this replay. Rounds 7 and 8 in [`Docs/context/OPENING_TUTORIAL_INTERVIEW.md`](../context/OPENING_TUTORIAL_INTERVIEW.md).

Press E at the bed. The coat hides and you are a wisp. The companion you claimed stays, and it hovers on the bed and on the other wisps the same way it hovers on everything else. Night does not start an encounter or spiritual power regen. The child says the bed-and-dawn line once. Purple wisps stand beside the south copse, at the pond, and at the hot springs. Press E on one and play the click heart. A kept heart collects it. You do not need the other quests first.

Quest log: sleeping ends the opening day, so the `Opening` chain and the `home_loop` chain are stored beside each other. The HUD draws only the most recently changed chain. Note which one you see; the storage test is `HomeWorld.HomeLoop.QuestChainBesideOpening`.

Developer shortcut for this replay: in a fresh PIE run `hw.Playtest.FastForward`. No argument plays the day beats in order (spirit, both herb beds, backpack, kettle, station mix, dog, fish, bed) and leaves you at the bed at night with every earlier step really executed. `test herb collection` claims the spirit, then places you at the east bed to draw the heart. `list` prints the other stops: spirit, herbs, backpack, kettle, station, dog, fish, sleep, night, collect, heal.

Developer check, not the pass: `.\Tools\RunTests.ps1 -Quest` runs all 11 stops in PIE and writes `Saved/quest_tests.json`. It loads `L_SizeTest`, ends PIE when done, and never fills the tables below. How to add a stop: [`QUEST_TESTS.md`](QUEST_TESTS.md).

| Field | Result |
|---|---|
| Date | |
| Slept and became spirit? | |
| Stayed on the island? | |
| Companion hovered, and a click heart collected a wisp? | |
| One sentence | |

---

## Wisp loop

**Built.** Waiting on this replay. Round 8 in [`Docs/context/OPENING_TUTORIAL_INTERVIEW.md`](../context/OPENING_TUTORIAL_INTERVIEW.md).

Night. Three damaged wisps stand at the copse, the pond, and the hot springs. Collect one with the click heart and it goes into the backpack. Carry it to the hot springs and press E: one herb chunk starts a 20 second heal. When the heal ends the wisp follows at the legs, not the shoulder. The claimed companion stays on the shoulder.

Placeholder tuning to judge: 20 second heal, one herb chunk per wisp, 600 cm spring range, three small purple followers in an arc at the feet.

| Field | Result |
|---|---|
| Date | |
| Three damaged wisps collected into the backpack? | |
| E at the hot springs started the heal and spent one herb chunk? | |
| Healed wisps follow at the legs, not the shoulder? | |
| One sentence | |

---

## The glider

**Not built.** At dawn, before the descent. Round 8 in [`Docs/context/OPENING_TUTORIAL_INTERVIEW.md`](../context/OPENING_TUTORIAL_INTERVIEW.md). It spends wood, silk, and metal from the armory chest. Those chests are not built. The day glide does not start before the craft.

| Field | Result |
|---|---|
| Date | |
| Crafted at the armory table? | |
| The descent does not start before the craft? | |
| One sentence | |

---

## Dawn glide

**Blocked.** Last mechanic of the tutorial. The mist clears at this dawn. The descent waits on the glider craft above.

You wake on the island. The bed returns you to the body. Dawn does not. The mist clears, and you glide down to the field. The glide is the day glide toward camp smoke, with no pickup. Pass if the glide is the last new mechanic, and the field reads as the first place past the tutorial.

| Field | Result |
|---|---|
| Date | |
| Woke on the island? | |
| Glided down to the field? | |
| One sentence | |

---

## Separate passes

These are post-tutorial or separate systems. They are not steps in this tutorial day.

- Companion party: [`PARTY_PLAYTEST.md`](PARTY_PLAYTEST.md). The design stays in [`Docs/41_COMPANION_PARTY_DESIGN.md`](../41_COMPANION_PARTY_DESIGN.md).
- Home loop: [`HOME_LOOP_PLAYTEST.md`](HOME_LOOP_PLAYTEST.md). The design stays in [`Docs/42_HOME_LOOP_DESIGN.md`](../42_HOME_LOOP_DESIGN.md).
- Water and wisp signs: design-only, [`Docs/42_HOME_LOOP_DESIGN.md`](../42_HOME_LOOP_DESIGN.md) section 10.1. Do not run it as a tutorial step.

---

## Retired

Not this queue. The herb heart is the rune already passed above. The field is not a tutorial beat.

- The heart drawn on the wisp.
- The bench commit, and the line "Place it, turn it, commit."
- The marked herb after the glide.
- One timed play of that old opening.
- Five new players. That waits until this day exists in the build.

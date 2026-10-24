# 45 - Future stress and virtue design

**Status:** FUTURE — Lead picks 2026-10-21, `SV 1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A 12A`. Not in the vertical slice. Does not change current build order, MVP scope, or any other design file until a build stage opens. Spec added 2026-10-23: the first bonus after the 20 November play is a Grace-moss meal that makes the next craft last longer. That bonus is not in the November slice. No code in that spec.
**Origin:** Lead chat, 2026-10-21. Picks scribed the same day from the interview at `C:\dev\stress-virtue-interview.md`.
**When to use:** Before any stress meter, virtue-juice item, moss resource, sin debuff, or all-seven reward. Read this file before proposing slice changes "for stress later."

Picks are closed. This file records the future direction only.

Do not copy this into the vision board, the GDD, `Docs/03_SYSTEMS_MVP.md`, `Docs/canon/DO_NOT.md`, `Docs/VIRTUE_ATTRIBUTE_BIBLE.md`, or `Docs/42_HOME_LOOP_DESIGN.md`. The canon map keeps one pointer row.

This round writes `Docs/45_STRESS_VIRTUE_FUTURE_DESIGN.md` and that pointer row only (12A). The files named above change when a build stage opens.

## 1. Status and slice boundary

The vertical slice and the home loop stay as they are. Nothing here authorizes a stress meter, a moss gather node, or a sin flip in the current queue. The chest of 6 and the pad spend are already in the slice. Section 8 records them and does not extend them.

The seven pairs already have names in [VisionBoard/Core/VISION.md](../VisionBoard/Core/VISION.md) and `EHomeWorldVirtuePole`: Greed/Generosity, Gluttony/Abstinence, Sloth/Productivity, Wrath/Grace, Pride/Humility, Envy/Fulfillment, Lust/Love. Each axis reads -1 sin, 0 neutral, +1 virtue. A paradox is both poles of one axis drawn as one mark. Canon has no separate names for the seven paradoxes.

When a build stage opens, the first build of this system is the Wrath/Grace axis only (8A). The other six axes, and every all-seven reward, stay direction (11A).

## 2. Lead idea and locked picks

Moss becomes a crafting ingredient that helps ease stress. Stress builds on the player. At a cap, a virtue flips to its sin. A healed wisp's pole flows into a material at home. That flow is called virtue juice. The player spends the marked material in a meal. All seven virtues, all seven sins, and all seven paradoxes are a later direction, including the special skills that holding every paradox would unlock. The first system is one axis.

### Locked 2026-10-21

1. **Infusion (1A).** A healed wisp infuses its first pole into a material at a home station. That is the water path in [Docs/42_HOME_LOOP_DESIGN.md](42_HOME_LOOP_DESIGN.md) §10.1, plus a herb mixed with a spirit. The material takes the wisp's first pole. This adds no new verb.
2. **Virtue juice (2A).** Virtue juice is the name for that infusion. It is not a carried item, not a bottle, and not a wisp charge. The six-slot carry stays empty of it.
3. **Moss (3A).** Moss is a kitchen-chest item, `ITEM_MOSS`. Wisps gather it from trees and rocks, the way silk and metal sit outside the six `RES_*` ids. There is no seventh resource.
4. **What raises stress (4A).** Stress rises from a hit or a bonk, and from a Day that ends without a home tend. A home tend is a meal served, or rest at home.
5. **What lowers stress (5A).** A served meal that contains Grace-marked moss lowers stress by a fixed amount. Sleeping in the bed lowers it a little.
6. **Who has stress (6A).** Only the player has stress in the first build. Creatures keep their existing hand-set or rolled poles.
7. **The flip (7A).** At the cap, Swap flips one of the player's virtue poles to its sin, then stress resets partway. Below the cap, nothing flips. On the first build the flip is Grace to Wrath. What Swap does when that axis is empty, or already Wrath, is not named.
8. **First build (8A).** The first build is the Wrath/Grace axis only. Grace moss eases stress. At the cap, Grace flips to Wrath.
9. **Where a sin lives (9A).** Stress and sin poles live on the player's virtue set, separate from the meal-buff slot. A sin shows its rune and changes an interaction. It never lowers a stat. The meal slot stays one slot.
10. **Ease pad and guards (10A).** The first build does not change the ease pad or the guards. Stress and sins are a home-loop read only.
11. **All seven (11A).** All 7 virtues, all 7 sins, and all 7 paradoxes are direction only. No build, and no skill tree.
12. **Where this is written (12A).** This file, plus one `CANON_MAP` pointer row. No other canon file in this commit.

## 3. What exists today, and where it conflicts

| Source | What it says |
|---|---|
| [Docs/03_SYSTEMS_MVP.md](03_SYSTEMS_MVP.md) | No seventh resource. Six `RES_*` ids. |
| [Docs/canon/DO_NOT.md](canon/DO_NOT.md) | No seventh resource. No crafting recipe webs. No generic skill trees. |
| [Docs/canon/SCHEMA.md](canon/SCHEMA.md) | Six slots. No equipment, weapon, or currency slot. |
| [Docs/42_HOME_LOOP_DESIGN.md](42_HOME_LOOP_DESIGN.md) §2 5A and §7 | Dust only shrinks a bonus. Stats do not fall below the unbuffed baseline. The meal buff is one slot, lasts one Day phase, and does not change spirit sickness, a bonk, or a stroke. |
| [Docs/42_HOME_LOOP_DESIGN.md](42_HOME_LOOP_DESIGN.md) §10.1 | A healed wisp's first pole infuses plot water. The water is not a `RES_*` resource and not a carried item. There is no fill, container, or carry. The harvest is `ITEM_HERB` or `ITEM_GREENS` with that pole. The serve Gives the pole to the player for the Day when that axis is empty. One marked ingredient per recipe. A paradox wisp is out of scope. |
| [Docs/VIRTUE_ATTRIBUTE_BIBLE.md](VIRTUE_ATTRIBUTE_BIBLE.md) | Swap flips a pole to the other pole of that axis. A mark shows a rune and changes an interaction. A mark does not add a hidden stat line, except node modifiers on 2026-10-21. The camp forest axis is Wrath/Grace. The ease runs Grace, then Wrath, then the paradox. |
| [Docs/context/OPENING_TUTORIAL_INTERVIEW.md](context/OPENING_TUTORIAL_INTERVIEW.md) | The player does not carry gathered materials. A healed wisp fills a wood, herb, or stone node into a chest. Silk, fiber, and metal nodes are refused. Silk and metal stay out of the six-slot carry. The dog is afflicted by Wrath; the ease draws Grace, then uses a herb mixed with a spirit. |
| [Docs/decisions/AGENT_DECISIONS.md](decisions/AGENT_DECISIONS.md) | Dawn wood, silk, and metal live on opening supply. They are not `RES_*` slots. |

**Plain conflicts, left in place until a build stage opens:**

- Canon has no stress meter, no virtue juice, and no moss ingredient. Moss in the art is a look, not an item.
- Six `RES_*` ids stay the carry. `ITEM_MOSS` follows silk and metal: a chest item, not a seventh resource. This commit does not add the id to `SCHEMA.md` or `03_SYSTEMS_MVP.md`.
- Today's wisps fill wood, herb, and stone, and they refuse silk, fiber, and metal nodes. Gather of `ITEM_MOSS` from trees and rocks waits for the build stage. This commit does not open those nodes.
- The meal-buff slot and the dust rule stay in Doc 42. A Grace-moss meal's stress change is a separate read on the virtue set. It does not lower a stat and it does not replace the armed buff.
- A stress number that the player cannot see would be a hidden stat line. The first build needs a visible read. The cap, the rates, and the reset amount are not named here, so this file does not invent them.
- Swap stays the herb verb the virtue bible already has. The cap uses that verb on the player's Wrath/Grace axis. It does not add a second flip verb.
- All-seven rewards, including paradox skills, would be a skill tree. They stay direction.

Amended 2026-10-23. The November slice does keep a kitchen chest of 6 `ITEM_MOSS`, and a finished pad spends 1 to sleep its guard. A miss does not spend. Gather nodes, the stress meter, the flip in play, and the craft-duration bonus stay off that slice. Section 8 is the correction. The bullets above stay as the 2026-10-21 reading.

## 4. Still unnamed

- The stress cap, the amount a hit or a bonk adds, the amount a missed home tend adds, the fixed amount a Grace-moss meal removes, the smaller amount bed sleep removes, and how far the cap resets after Swap.
- How a moss node looks, and which wisp gathers it.
- Names for the seven paradoxes. A paradox remains both poles of one axis on one mark.
- What Swap does when the player's Wrath/Grace axis is empty, or already Wrath.
- The multiplier that makes the next craft last longer. Lead names that one number when the build gate in section 8 opens. This file does not invent it. The test amounts already in the stress component (missed day, meal, bed, reset) are not locks and are not named here.

## 5. Staged path after the slice

No new calendar dates. The 20 November play is the queue's existing deadline, and it is the gate out of stage 0. Each stage needs the prior stage's proof plus a Lead gate. The gate is what may amend the GDD, `03_SYSTEMS_MVP.md`, `DO_NOT.md`, the virtue bible, and Doc 42.

| Stage | Goal | Must exist first |
|---|---|---|
| **0 — Slice** | The queue through 20 November. The kitchen chest starts with 6 `ITEM_MOSS`. A finished ease-pad ladder spends 1, and that spend is what puts the guard to sleep. A miss does not spend. No stress meter, no Grace-to-Wrath flip in play, no craft-duration bonus. No dated row is graded on stress. | The 20 November play. |
| **1a — Grace craft** | The first code after that play. A Grace-moss meal still lowers stress by the amount the component already subtracts. It also marks the next craft with the Grace rune and makes that craft's effect last longer than the same craft without the meal. The player sees the rune on the craft. They do not see a stress meter. | Stage 0 played. Lead names the multiplier in section 4. |
| **1 — Wrath/Grace at home** | Player stress only. A healed wisp infuses a material at a home station. Virtue juice is that infusion. `ITEM_MOSS` is chest stock gathered by a wisp. A hit, a bonk, or a Day without a home tend raises stress. A Grace-moss meal lowers it by the named fixed amount. Bed sleep lowers it a little. At the cap, Swap flips Grace to Wrath and stress resets partway. The sin shows a rune and changes an interaction. The ease pad, the guards, the meal-buff slot, and creature poles stay as they are. | Stage 1a. The remaining unnamed numbers in section 4 named by Lead. A visible stress read. |
| **2 — The rest of the set** | The other six axes, all-seven virtues, all-seven sins, and all-seven paradoxes. Direction only until a later gate. No skill tree in this file. | Stage 1 played. Paradox names if a gate asks for them. |

## 6. Lead answers

Answered 2026-10-21. All recommended.

1. **1A.** A healed wisp infuses its first pole at a home station.
2. **2A.** Virtue juice is that infusion, not an item.
3. **3A.** `ITEM_MOSS` in the kitchen chest. No seventh `RES_*`.
4. **4A.** A hit or a bonk, or a Day with no home tend.
5. **5A.** A Grace-moss meal lowers stress by a fixed amount. Bed sleep lowers it a little.
6. **6A.** The player only.
7. **7A.** At the cap, Swap flips one virtue to its sin, then a partial reset.
8. **8A.** Wrath/Grace only.
9. **9A.** Sins sit on the virtue set. They show a rune and change an interaction. They never lower a stat.
10. **10A.** No ease-pad change and no guard change.
11. **11A.** All seven virtues, sins, and paradoxes are direction only.
12. **12A.** This file and the canon-map pointer only.

## 7. Out of scope for this document

- A seventh `RES_*` id, a bottled virtue juice, or a wisp-charge counter.
- Stress on a creature, the partner, or the child.
- A stat that falls below the unbuffed baseline.
- An ease-pad change, a guard change, or a bonk-try change.
- A skill tree, or a build of the all-seven rewards.
- The numbers and names in section 4.
- Code for the Grace-craft bonus, until the 20 November play has been played.

## 8. Grace craft, after the slice

Lead, 2026-10-23. This section is the spec. It does not authorize code, a stress meter, or a change to any dated November row. The build gate is the 20 November play in [Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md](qa/TUTORIAL_PLAYTEST_QUEUE.md). The GDD, `03_SYSTEMS_MVP.md`, `DO_NOT.md`, the virtue bible, and Doc 42 stay as they are until that gate opens.

### What the slice already does

The kitchen chest starts with 6 `ITEM_MOSS`. A finished ease-pad ladder spends 1, and the guard sleeps only when that spend succeeds. A miss does not spend. Bed sleep, a late paradox miss, and a missed dawn already call the stress component. Nothing in play calls the hit amount or the Grace-to-Wrath flip. There is no meter. No November row is graded on a stress number.

A moss serve already lowers stress, then arms the one day buff. Those stay two reads. The duration bonus is a third read. It does not rewrite the buff slot. Doc 42 still holds: that buff does not change the stroke, the bonk, or spirit sickness.

### The first bonus

After the gate, a Grace-moss meal still lowers stress by whatever the component already subtracts. It also marks the next craft with the Grace rune and makes that craft's effect last longer than the same craft without the meal. The player sees the rune on the craft. They do not see a stress meter.

The opening kettle is not that craft. The first duration is the day sprint from the home-loop stamina meal. The rune is on that serve, not a new widget. The longer time is that sprint. One fixed multiplier, named by Lead at the gate. This section does not choose it.

The camp pad, the guards, the stroke, the bonk, and any downward stat stay unchanged. The meal slot stays one slot.

The later code sits beside the armed buff, not inside it. Serving the Grace-moss meal sets a one-shot flag. The next stamina serve reads it, scales the sprint, shows the Grace rune, and clears the flag. A host test keeps today's sprint when the flag is clear, expects the longer sprint and the rune when the flag was set, expects the stress drop, and expects an ease pad's result to stay the same. That bite does not hook the cap flip or the hit into play.

### Later, not in that bite

Written here so the chase has an owner. Not built with the first bonus.

1. The cottage and the family are the stress picture. An unmade bed, a cold table, a spirit that drifts. The number stays in the log until that picture exists.
2. A wisp finishing a home job counts as a day's tend, beside the meal and the bed. Skipping it shows on the spirit. It is not a third clock.
3. The second forest's stroke is the give. Generosity shortens the craft. Greed snatches a late one. The field shows both edges before either opens.
4. A paradox is both poles, stronger, and they interfere. The player meets Grace, then Wrath, then both.
5. The lair key is gathered in pieces from the field and the forests.

The house is the sheet: the rune on the meal, the coat, and the wisp. No skill tree. No second meter.

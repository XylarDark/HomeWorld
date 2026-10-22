# 45 - Future stress and virtue design

**Status:** FUTURE — Lead picks 2026-10-21, `SV 1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A 12A`. Not in the vertical slice. Does not change current build order, MVP scope, or any other design file until a build stage opens.
**Origin:** Lead chat, 2026-10-21. Picks scribed the same day from the interview at `C:\dev\stress-virtue-interview.md`.
**When to use:** Before any stress meter, virtue-juice item, moss resource, sin debuff, or all-seven reward. Read this file before proposing slice changes "for stress later."

Picks are closed. This file records the future direction only.

Do not copy this into the vision board, the GDD, `Docs/03_SYSTEMS_MVP.md`, `Docs/canon/DO_NOT.md`, `Docs/VIRTUE_ATTRIBUTE_BIBLE.md`, or `Docs/42_HOME_LOOP_DESIGN.md`. The canon map keeps one pointer row.

This round writes `Docs/45_STRESS_VIRTUE_FUTURE_DESIGN.md` and that pointer row only (12A). The files named above change when a build stage opens.

## 1. Status and slice boundary

The vertical slice and the home loop stay as they are. Nothing here authorizes a stress meter, a moss node, or a sin flip in the current queue.

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

## 4. Still unnamed

- The stress cap, the amount a hit or a bonk adds, the amount a missed home tend adds, the fixed amount a Grace-moss meal removes, the smaller amount bed sleep removes, and how far the cap resets after Swap.
- How a moss node looks, and which wisp gathers it.
- Names for the seven paradoxes. A paradox remains both poles of one axis on one mark.
- What Swap does when the player's Wrath/Grace axis is empty, or already Wrath.

## 5. Staged path after the slice

No calendar dates. Each stage needs the prior stage's proof plus a Lead gate. The gate is what may amend the GDD, `03_SYSTEMS_MVP.md`, `DO_NOT.md`, the virtue bible, and Doc 42.

| Stage | Goal | Must exist first |
|---|---|---|
| **0 — Slice** | The current queue. No stress meter, no `ITEM_MOSS`, no virtue-juice item. | MVP canon unchanged. |
| **1 — Wrath/Grace at home** | Player stress only. A healed wisp infuses a material at a home station. Virtue juice is that infusion. `ITEM_MOSS` is chest stock gathered by a wisp. A hit, a bonk, or a Day without a home tend raises stress. A Grace-moss meal lowers it by the named fixed amount. Bed sleep lowers it a little. At the cap, Swap flips Grace to Wrath and stress resets partway. The sin shows a rune and changes an interaction. The ease pad, the guards, the meal-buff slot, and creature poles stay as they are. | Stage 0. The unnamed numbers in section 4 named by Lead. A visible stress read. |
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

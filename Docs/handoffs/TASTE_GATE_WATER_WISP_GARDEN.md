# TASTE GATE — Water, wisp signs, garden, food

**Status:** RESOLVED 2026-10-20
**Gate id:** `TG-WATER-WISP-GARDEN`
**Heuristic:** 1 — would change game-mechanic canon.
**Created:** 2026-10-20
**Owner:** human — Luke
**Job:** taste

## Fork

The direction is: a wisp carries a sin/virtue sign; mixing it with water purifies or taints the water; the water goes on a garden plot; the plant takes the sign; the harvest carries it; the cooked food carries it.

The repo does not define whether that sign is one of the existing seven poles or a new single morality axis. It also does not define what the signed food does. Those are taste decisions, not agent flesh-out.

## Canon checked

- [`Docs/42_HOME_LOOP_DESIGN.md`](../42_HOME_LOOP_DESIGN.md): one healed task wisp per plot; cloud wisps stay on the wound and fertilizer; food arms one home-loop buff; six resources.
- [`Docs/43_CLOUDS_WISPS_DESIGN.md`](../43_CLOUDS_WISPS_DESIGN.md): cloud wisps cap two; the home pool is healed task wisps; a cloud wisp is not a home-pool wisp.
- [`Docs/VIRTUE_ATTRIBUTE_BIBLE.md`](../VIRTUE_ATTRIBUTE_BIBLE.md): seven axes; one pole per axis; marked herbs spend by Nullify, Swap, Give, or Take; marks are visible, not hidden stat lines; a mark changes the same stroke and does not add a verb.
- [`VisionBoard/Core/VISION.md`](../../VisionBoard/Core/VISION.md): the seven sin/virtue pairs.
- [`Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`](../qa/TUTORIAL_PLAYTEST_QUEUE.md): the tutorial queue stops at night; the home loop and party are outside it.
- [`Docs/qa/PARTY_PLAYTEST.md`](../qa/PARTY_PLAYTEST.md): a separate desk pass.

## Alert

```
Owner: human — the wisp-sign model and the water/food loop
Job: taste
You are here: Docs/42_HOME_LOOP_DESIGN.md, water/garden/food, shaping
Why now: the chain changes the home loop, the virtue chain, and the playtest shape. Guessing would create either a second morality axis or a new verb the virtue bible forbids.
I will not: invent the pole model, the wisp population, the water action, or the food payoff.
Recommend: keep the seven existing poles and the healed home-pool wisp; let the plot wisp infuse the water; make the cooked food a marked consumable under the existing virtue rules.
Need from you:
  1. Seven poles on the home-pool wisp (recommended)
  2. Seven poles on cloud wisps
  3. A new pure/tainted axis
  4. Wrath/Grace only for the first pass
  5. Skip for now
After you pick: scribe the pick in Doc 42, then rebuild the playtest queue and add the home-loop/party/quest-log passes.
```

## Round 1 questions

1. **Sign model and source.** Existing seven poles on the healed home-pool wisp is recommended. Cloud wisps, a new pure/tainted axis, or a Wrath/Grace-only sample are the alternatives.
2. **Loop shape.** Plot wisp infuses + marked meal is recommended. Manual basin + marked meal, plot wisp + buff-only, or sign-only/later are the alternatives.

## Resolution

Luke picked both recommended options on 2026-10-20:

- **Sign model:** seven existing poles on the healed home-pool wisp.
- **Loop shape:** the plot wisp infuses the water; the cooked meal is a marked consumable.
- **Kept:** cloud wisps on the wound and fertilizer; six resources; one wisp per target; no separate watering verb or water container.

## After the answer

1. Amend [`Docs/42_HOME_LOOP_DESIGN.md`](../42_HOME_LOOP_DESIGN.md) with the chosen sign model, water action, and food payoff. Keep cloud wisps, the six-resource lock, and the one-wisp-per-target rule intact unless the pick explicitly changes them.
2. Rebuild [`Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`](../qa/TUTORIAL_PLAYTEST_QUEUE.md) so the passed tutorial results stay untouched, the night/wisp replay is still the Now, and the post-tutorial home-loop/party/quest-log work is clearly separated.
3. Add a home-loop playtest pass for the built home-loop code and tests. Mark the water/sign chain design-only until its build bite exists.
4. Run the doc-link and consistency checks after editing.

## Do not

- Do not replay or overwrite the passed midday, crafting, dog, backpack, fishing, wisp, or bonk results.
- Do not add a seventh resource or a watering-as-survival rule.
- Do not treat the water chain as built until its code and tests exist.

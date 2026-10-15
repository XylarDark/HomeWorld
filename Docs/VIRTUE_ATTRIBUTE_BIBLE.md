# Virtue attributes

Prototype rules for the seven pairs. Lead lock, 2026-10-15. The pair names stay in [VisionBoard/Core/VISION.md](../VisionBoard/Core/VISION.md). This file does not copy the table.

## Set

A character, a collectible, or a piece of armor holds a set of poles. Each pair is one axis. The set never contains both poles of one axis. Seven is the maximum. Zero is allowed.

## Spawn

A placed actor may name its poles by hand. The hand set is checked for an opposite pair and for the cap. It does not roll.

Everyone else uses a spawn table. One row is characters. One row is herbs and other collectibles. Each row holds seven chances: the chance of the first pole through the chance of the seventh. The chances are non-increasing.

The roll stops on the first miss. On a hit it picks an axis that is not in the set, then one of that axis's two poles. Seven poles is the rare tail of that roll.

The placeholder chances, stored on the spawn table asset, are `1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/128`. Changing them is a later edit of that data.

## Herbs

A herb with no poles is a count of `RES_HERB`. Tea, planting, tame, and heal spend that count.

A herb with one or more poles is one instance. Two herbs with different poles are not one stack.

One marked herb is spent only when the verb changes the target:

- Nullify clears every pole on the target.
- Swap flips the target's pole on the axis named by the herb's first pole.
- Give adds that pole when the axis is empty.
- Take removes that pole when the target has it.

Give does nothing when the axis already holds either pole. Swap is the only move onto the other pole. A verb that does nothing does not spend the herb.

## Marks

Each pole has a rune. A paradox mark is the two poles of one axis combined into one symbol. It occupies that axis. The set still does not store both poles as two entries. The placeholder spawn table does not roll a paradox mark.

These marks are attributes. Sleep at the bed is still the form change. The bed rune stays removed.

## Encounters

On a creature, difficulty is the count of sin and virtue runes. A paradox mark is a wild behaviour, and it changes the drop. More runes means more yield. The yield comes from the encounter. A hit is still the launch, back to the homestead or away from the creature. There is no health bar and no kill.

A yielded item carries a pole, or a paradox mark of its own.

## Armor and consumables

Armor carries marks. It changes how you move, which places you can reach, how many bonk tries you have, and how spirit play goes. You equip the set for the objective you leave the homestead to do. A hit still launches you.

A marked consumable alters the character, or the world you then meet. Armor is how you meet what that alteration puts in front of you. Herbs stay on the verbs above. At the homestead you can change, remove, or alter marks. Those recipes are not named.

What a bonk try counts is not named.

## Planetside

The ground changes with how you treat it. As the days pass, mechanics arrive and mechanics leave. The schedule is not named. This layer is in the T0 slice. The rescue loop stays the first loop.

## Zones

Four zones carry the fourteen poles between them. Each zone has at least one paradox encounter. Which pole sits in which zone is not named. These four are places. They do not replace the seven mechanic families as the zone-type vocabulary.

The first forest is the camp forest, the edge you commit to from the field. When that camp is complete, the other forest edge opens. That forest has a different mechanic. The mechanic is not named. From inside the field the two edges stay identical until you commit.

Past the second forest is a river. The body crosses on stones, a jump. When the second forest is complete, spirit form can cross that river. This uses the spirit form you already have. On the far bank is marsh. Mountains close the way beyond it.

The field's own river edge stays the meadow view. The stone jump is the river after the second forest. Edge text: [Lib/02_Zones/gather/FIELD.json](../Lib/02_Zones/gather/FIELD.json).

The paradox item the lair requires is gathered on travels in the field and the forests. What it does in the hand is not named. The lair layer is [Docs/context/BOSS_LAIR_LOCK.md](context/BOSS_LAIR_LOCK.md).

## Authoring

Author the hardest form of a mechanic first. Then author the scaled-down steps that progression uses to reach it.

## Not named

- The drawing of each rune and of the paradox mark
- What a paradox behaviour does
- What a bonk try counts
- The second forest's mechanic
- Which of the fourteen poles sit in which zone
- Which mechanics arrive or leave on which day
- The homestead recipes that change, remove, or alter a mark
- The seven interactions in the lair
- What the lair's paradox item does

## Not in this pass

What a pole requires before a character will talk, sleep, be eased, be tamed, or be healed. The camp ease beat stays in [Docs/context/HOMEWORLD_ROUTE.md](context/HOMEWORLD_ROUTE.md) until those demands are named.

Which placed characters carry a hand set.

A widget that lists the poles. `hw.Virtue.Read` logs the poles on the named actor, or on the actor under the crosshair. It does not grant poles.

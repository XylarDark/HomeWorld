# Virtue attributes

Prototype rules for the seven pairs. The pair names stay in [VisionBoard/Core/VISION.md](../VisionBoard/Core/VISION.md). This file does not copy the table.

## Set

A character or a collectible holds a set of poles. Each pair is one axis. The set never contains both poles of one axis. Seven is the maximum. Zero is allowed.

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

## Not in this pass

What a pole requires before a character will talk, sleep, be eased, be tamed, or be healed. The camp ease beat stays in [Docs/context/HOMEWORLD_ROUTE.md](context/HOMEWORLD_ROUTE.md) until those demands are named.

Which placed characters carry a hand set.

A widget that lists the poles. `hw.Virtue.Read` logs the poles on the named actor, or on the actor under the crosshair. It does not grant poles.

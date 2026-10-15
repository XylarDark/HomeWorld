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

Each pole has a rune. At a glance the rune says which pole it is. A paradox mark is the two poles of one axis combined into one symbol, and at a glance it reads as both poles of that pair. Interview round 13, 2026-10-15. It occupies that axis. The set still does not store both poles as two entries. The placeholder spawn table does not roll a paradox mark. The art bible owns the drawing.

These marks are attributes. Sleep at the bed is still the form change. The bed rune stays removed.

A mark changes a visible interaction with a place or a creature. The yield follows from that interaction. A mark does not add a hidden stat line. Interview round 1, 2026-10-15.

## Encounters

On a creature, difficulty is the count of sin and virtue runes. A paradox mark runs both poles of its axis at once, and those two toys interfere. That interference is the wild behaviour, and it changes the drop. The encounter is one readable action. A miss launches you. A success yields. Interview rounds 3 and 5, 2026-10-15. More runes means more yield. The yield comes from the encounter. A hit is still the launch, back to the homestead or away from the creature. There is no health bar and no kill.

A yielded item carries a pole, or a paradox mark of its own.

## Armor and consumables

Armor carries marks. It changes how you move, which places you can reach, how many bonk tries you have, and how spirit play goes. You equip the set for one encounter. The set changes how that encounter behaves so you can finish it. Interview round 2, 2026-10-15. A hit still launches you.

A marked consumable alters the character, or the world you then meet. Armor is how you meet what that alteration puts in front of you. Herbs stay on the verbs above. At the homestead you change, remove, or alter a mark at a bench: place, turn, commit. A bad commit fails in the open. There is no menu. Interview round 4, 2026-10-15. Herbs still spend by the verbs above. The bench's recipes are not named.

What a bonk try counts is not named.

## Planetside

The ground changes with how you treat it. Using a paradox encounter retires that toy the next dawn and leaves a quieter version. A new toy arrives somewhere you have not used it. Interview round 10, 2026-10-15. This layer is in the T0 slice. The rescue loop stays the first loop.

## Zones

Four zones carry the fourteen poles between them. Each zone has at least one paradox encounter. Which pole sits in which zone is not named. These four are places. They do not replace the seven mechanic families as the zone-type vocabulary.

The first forest is the camp forest, the edge you commit to from the field. Its axis is Wrath / Grace. The one action is the ease. Grace finishes it. Wrath shoves it off. Paradox runs both, and they interfere. A miss launches you. A success yields. Interview round 6, 2026-10-15. When that camp is complete, the other forest edge opens. Its axis is Greed / Generosity. The one action is a give. Generosity completes it. Greed takes it back. Paradox runs both, and they interfere. The encounter shape stays: a miss launches you, a success yields. Interview round 7, 2026-10-15. That forest has a different mechanic from the ease. From inside the field the two edges stay identical until you commit.

Past the second forest is a river. The body crosses on stones, a jump. A mark changes a stone, and you can see that change before you jump. Interview round 8, 2026-10-15. When the second forest is complete, spirit form can cross that river. This uses the spirit form you already have. On the far bank is marsh. Mountains close the way beyond it. The marsh's paradox encounter is the last yield. You take that yield home. The lair's paradox item stays a find from the field and the forests. Interview round 9, 2026-10-15.

The field's own river edge stays the meadow view. The stone jump is the river after the second forest. Edge text: [Lib/02_Zones/gather/FIELD.json](../Lib/02_Zones/gather/FIELD.json).

The paradox item the lair requires is gathered on travels in the field and the forests. It is the key that lets the lair's last station happen. Interview round 12, 2026-10-15. The lair layer is [Docs/context/BOSS_LAIR_LOCK.md](context/BOSS_LAIR_LOCK.md).

## Authoring

Author the hardest form of a mechanic first. Then author the scaled-down steps that progression uses to reach it.

## Not named

- What a bonk try counts
- The second forest's give, beyond the axis and the take-back
- Which poles sit on the river and in the marsh
- Where the new dawn toy arrives
- The homestead bench's recipes
- Which lair pairs use an existing beat, and which get a new station

## Not in this pass

What a pole requires before a character will talk, sleep, be eased, be tamed, or be healed. The camp ease beat stays in [Docs/context/HOMEWORLD_ROUTE.md](context/HOMEWORLD_ROUTE.md) until those demands are named.

Which placed characters carry a hand set.

A widget that lists the poles. `hw.Virtue.Read` logs the poles on the named actor, or on the actor under the crosshair. It does not grant poles.

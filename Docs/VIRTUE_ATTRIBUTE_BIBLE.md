# Virtue attributes

Prototype rules for the seven pairs. Lead lock, 2026-10-15. The pair names stay in [VisionBoard/Core/VISION.md](../VisionBoard/Core/VISION.md). This file does not copy the table.

## Parked 2026-10-16

Do not build these. [`Docs/context/PRINCIPLE_FIT_LOCK.md`](context/PRINCIPLE_FIT_LOCK.md) wins.

- The armor bench. The change, remove, and alter sentences below are the old interview. They are not a build list.
- Pair toys other than the camp-forest ease stroke: a bite, a decoy, a shape that must be filled, a return to the start, and a grappling hook.
- Lair coils.

The zone-story, stroke-variety, and random-pair interviews do not authorize those toys. The ease stroke stays.

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

On a creature, difficulty is the count of sin and virtue runes. A paradox mark runs both poles of its axis at once, and those two toys interfere. That interference is the wild behaviour, and it changes the drop. The encounter is one readable action. A success yields. Interview rounds 3 and 5, 2026-10-15. More runes means more yield. The yield comes from the encounter. A hit uses the two punishments in Hits. There is no health bar and no kill.

A yielded item carries a pole, or a paradox mark of its own.

## Armor and consumables

Armor carries marks. It changes how you move, which places you can reach, how many bonk tries you have, and how spirit play goes. You equip the set for one encounter. The set changes how that encounter behaves so you can finish it. Interview round 2, 2026-10-15.

A marked consumable alters the character, or the world you then meet. Armor is how you meet what that alteration puts in front of you. Herbs stay on the verbs above. At the homestead you change, remove, or alter a mark at a bench: place, turn, commit. A bad commit fails in the open. There is no menu. Interview round 4, 2026-10-15. The ease's yield has one recipe. Place the mark on a piece of armor, turn it until the rune matches a pole you have drawn, and commit. A mismatch fails in the open and returns the mark. Interview, next beats round 5. Remove is the same bench. Turn the rune until it is blank, and commit. The mark comes off in your hand. A commit on the wrong rune fails in the open and leaves the mark. Interview, slice defaults round 4, 2026-10-15. Alter is the same bench. Turn the rune to the other pole of that axis, and only if you have drawn that pole. Otherwise the commit fails and the mark stays. Interview, bench and lair round 1, 2026-10-15. Herbs still spend by the verbs above.

## Planetside

The ground changes with how you treat it. Using a paradox encounter retires that toy the next dawn and leaves a quieter version. A new toy arrives in the next zone you have opened and not yet used. The first time, that is the second forest, after the camp is complete. Interview, next beats round 4. This layer is in the T0 slice. The rescue loop stays the first loop.

## Zones

Four zones carry the fourteen poles between them. Each zone has at least one paradox encounter. Which pole sits in which zone is not named. You meet the axes in a randomized order. The last encounter in that run is a paradox of the stroke. Every axis uses that stroke. The creature is the theme. A creature's normal mechanic stays the one already established for it. An axis or a paradox is a layer on that default. The default slightly changes the layer, and the encounter becomes unique and harder. Which axis appears can be random. Interview, creature themes round 1, 2026-10-15. The bull's tame waits on the paradox layer on that bull. On that layer you draw while standing still. A sudden move is the miss, and the bull charges. The herb approach stays the tame once that layer is done. Interview, creature themes round 2, 2026-10-15. The field roost is a climb in the open field, not a fourth place. The bull knocks out the lower blocker. The higher obstacle is the stroke, drawn while you climb. The nest is the rune. A miss drops you to the ledge below. It does not send you home. Interview, slice defaults rounds 1 and 2, 2026-10-15. A tree takes the same kind of layer. You draw a stroke on the trunk. The bark you can see is the rune. A miss is the creak and the few steps back. In spirit form that miss is still the glide to the bed. Interview, slice defaults round 3, 2026-10-15.

The first forest is the camp forest, the edge you commit to from the field. Its axis is Wrath / Grace. The one action is the ease. Grace finishes it. Wrath shoves it off. Paradox runs both, and they interfere. The misses and the player order are in Hardest form. A success yields. Interview round 6, 2026-10-15. When that camp is complete, the other forest edge opens. Its axis is Greed / Generosity. The one action is a give. You draw the rune while you move, inside a visible wind-up. Generosity completes the stroke. Greed snatches it if you are late or the stroke is wrong. That miss is the same miss as the ease. Interview, next beats round 3. The encounter shape stays. A success yields. Interview round 7, 2026-10-15. That forest has a different mechanic from the ease. From inside the field the two edges stay identical until you commit.

Past the second forest is a river. The body crosses on stones, a jump. A mark changes a stone, and you can see that change before you jump. Interview round 8, 2026-10-15. On the layer you draw across that marked stone, inside the jump. The stone is the rune. A miss is the fish, back to the bank. Interview, creature themes round 3, 2026-10-15. When the second forest is complete, spirit form can cross that river. This uses the spirit form you already have. On the far bank is marsh. Mountains close the way beyond it. The marsh's paradox encounter is the last yield. You take that yield home. On the layer you draw the yield's rune. One pole completes the take. The other snatches it. A miss knocks you away from the yield. Interview, creature themes, 2026-10-15. The lair's paradox item stays a find from the field and the forests. Interview round 9, 2026-10-15.

The field's own river edge stays the meadow view. The stone jump is the river after the second forest. Edge text: [Lib/02_Zones/gather/FIELD.json](../Lib/02_Zones/gather/FIELD.json).

The paradox item the lair requires is gathered on travels in the field and the forests. It is the key that lets the lair's last station happen. Interview round 12, 2026-10-15. The lair layer is [Docs/context/BOSS_LAIR_LOCK.md](context/BOSS_LAIR_LOCK.md).

## Hits

A hit has two punishments. The weak hit knocks you away from the mechanic. You stay, and the action is still there. The bonk sends you home. That is the biggest punishment, and it is this game's death. You do not die.

A bonk try is one hit that stays the weak knock-away. When no tries remain, the next hit bonks you home. A match leaves the extra point in hand, and the next stroke must pass through it. A weak hit keeps that point. A bonk drops it.

## Hardest form

The first atom to author is the camp-forest ease. One commit. Grace would finish it. Wrath shoves it off. At the ceiling both happen, and they interfere, so the finish and the shove are the same moment. You can see which pole is which before you commit.

Hardness is how the shove and the finish occupy that same action. Extra sin or virtue runes on that creature each change something you can see about that same ease: the approach, the shove, or what the success leaves. They raise the yield. They do not add a new verb.

On the ceiling, a failed ease bonks you home. On the quieter steps, a failed ease is only the weak hit. Armor for this encounter lets the finish win through the Wrath shove. Its bonk tries are the weak hits you get before the next hit bonks you home.

The success yields a marked thing whose job you could already see in the action. The drop is not a hidden roll.

The player meets the ease in this order, on the way to the placed paradox:

1. Grace alone. A miss is the weak hit.
2. Wrath alone. A miss is the weak hit.
3. The paradox. A miss is the bonk.
4. The same ease plus one visible rune.

The forest edge does not open onto the paradox. The placed hardest creature sits after a finished Grace ease and a Wrath shove. Author the paradox first, then cut the punishment to the weak hit for the two single-pole steps, then add one felt rune at a time. After the paradox is used, the next dawn leaves the quieter form: the weak hit.

This is the design target. The virtue component does not store a paradox mark, and this file does not claim the encounter is placed in a level. The camp ease in [Docs/context/HOMEWORLD_ROUTE.md](context/HOMEWORLD_ROUTE.md) stays the route beat.

## Challenge

The ease starts from four pillars: reaction time, preparedness, drawing a rune with movement and the cursor, and doing those at once. Lead, 2026-10-15.

Preparedness is before every commit. You choose the armor set at home. In the clearing you get one read of the rune, then the shove can start.

On a commit you draw the pole's rune with the cursor while you move. The stroke has to match the rune you can see. The shove has a visible wind-up. Finish inside it and spend the carried point or a bonk try, and that commit can match. Wait, and you keep the point and the try, while a shove after the window can bonk. A wrong shape still misses, and it does not spend either. Interview, next beats round 2. The lock is [`Docs/context/PRINCIPLE_FIT_LOCK.md`](context/PRINCIPLE_FIT_LOCK.md).

The steps:

1. Grace. Drawing only. No wind-up. A miss is the weak hit.
2. Wrath. The wind-up only. No drawing. A miss is the weak hit.
3. The paradox. One stroke that is both poles, started inside the wind-up. A late start bonks you home. A wrong shape misses and does not spend.
4. The same ease plus one visible rune. That rune is one more point the stroke must pass through. You can see the point before you start. Interview, next beats round 1.

The rounds are [`Docs/context/CHALLENGE_PILLARS_INTERVIEW.md`](context/CHALLENGE_PILLARS_INTERVIEW.md).

## Authoring

Author the hardest form of a mechanic first. Then author the scaled-down steps that progression uses to reach it. The player meets those steps first. The ease is the worked example above.

## Not named

- Further lair beats, beyond the snake's stroke and the tickle's stroke

## Not in this pass

What a pole requires before a character will talk, sleep, be eased, be tamed, or be healed. The camp ease beat stays in [Docs/context/HOMEWORLD_ROUTE.md](context/HOMEWORLD_ROUTE.md) until those demands are named.

Which placed characters carry a hand set.

A widget that lists the poles. `hw.Virtue.Read` logs the poles on the named actor, or on the actor under the crosshair. It does not grant poles.

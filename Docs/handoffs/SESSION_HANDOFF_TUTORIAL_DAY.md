# SESSION_HANDOFF_TUTORIAL_DAY

Slice: the rest of the one-day tutorial on `L_SizeTest`, after the passed midday opening.
Job: implement. Do not re-interview the dog. Do not change the passed midday slice.

Read, in order:

1. [Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md](../qa/TUTORIAL_PLAYTEST_QUEUE.md)
2. [Docs/context/OPENING_TUTORIAL_TASKS.md](../context/OPENING_TUTORIAL_TASKS.md)
3. [Docs/context/OPENING_TUTORIAL_INTERVIEW.md](../context/OPENING_TUTORIAL_INTERVIEW.md) rounds 2–4
4. The Opening tutorial section in [Docs/VISION_BOARD.md](../VISION_BOARD.md)
5. [docs/level/L_SizeTest_CONTEXT.md](../../docs/level/L_SizeTest_CONTEXT.md) for what is already on the map. The dog procedure is interview round 4. Do not copy it.

Play is `/Game/HomeWorld/Maps/SizeTest/L_SizeTest`. Compile with `.\Tools\Safe-Build.ps1` from the repo root. UE 5.8 only. One beat at a time. Stop after each beat so Luke can play it. Do not commit unless he asks.

## Already passed — do not redo

Approach, copse, pad, spirit claim, shoulder wisp, herb hearts, chunk bank, kettle (one brew spends at most 10), partner inside by the kettle, child to their room, tea sprint. The counter under the kettle is the consumable station; the armory sits in front of the cottage.

`OpeningHerbTenths` on `AHomeWorldCharacter` is the chunk bank. The SizeTest interact chain in `UHomeWorldInteractAbility::ActivateAbility` returns after spirit, partner, garden, and kettle. Anything new on this map has to be added to that chain or E will not reach it. `TryStartCloudDescent` is already below that early-out, so the dawn glide will not start until the chain allows it.

## Build in this order

### 1. Crafting stations

Built and passed, 2026-10-18. Use the stations already on the map. The kitchen counter is the consumable station, with the kettle on it. The armor table is the greybox table in the armory in front of the cottage. Do not spawn another pair of tables.

- The station opens once the player has the shoulder spirit and banked herb chunks. Its one output is an herb mixed with a spirit. That output is what the dog beat spends. After it, the same counter brews at the kettle on top.
- The partner's armor gift opens the armor table. No walk speed or bonk-tries change. The armor-number choice in the tasks file is still open. Stop before any number change.

Do not import the camp recipe list from `UHomeWorldCraftSubsystem`.

### 2. The dog

Built, verified 2026-10-18, awaiting the replay. After crafting. This is the first tame and the sin/virtue sample. The bull is unchanged. The procedure is interview round 4. Do not restate it here.

The knock is a shove back out of reach. It is not the mist bonk, and it does not deal damage. Reuse `UHomeWorldRuneShapeComponent` for the Grace draw. Do not retune the herb heart. The camp-forest ease in [Docs/VIRTUE_ATTRIBUTE_BIBLE.md](../VIRTUE_ATTRIBUTE_BIBLE.md) is the later encounter. Do not build it, the paradox, or its armor rules. `UHomeWorldBeastTameComponent` is the existing tame state machine. Use it if it can record this tame. Do not add a second tame schema.

The Grace draw is the outline of a dove (Luke, 2026-10-18), in `AHomeWorldOpeningDog::GraceUnitShape()`. Do not draw the herb heart and call it Grace.

The lead-in: when the brew grants the tea sprint while the child is in their room, they run the homecoming route reversed and stop on the lawn beside the dog's lane (1.5 m east of the lane line, 6.1 m short of the dog), facing the dog. Logs: `opening_reveal: the child races to the dog yard (N points)` and `opening_reveal: child waits at the dog yard`.

### 3. The bonk

A mist volume stays up around the homestead. Jumping off while it is up launches the player back onto the island. The launch does not slow the step and does not dim the shoulder light. `BeginStrokeFromInput` stays off on `L_SizeTest`. The mist does not clear after the kettle.

### 4. Night on the island

The child says the bed-and-dawn line once. Sleep in the bed grants spirit form. Night does not. The existing bed path is `GrantSpiritSleepGate` on `NODE_BED`. Phase-alone must stay body. The player remains on the island. The mist is still up, so a jump off is still the bonk.

Add the one line beside `ShowOpeningProximityLine`. Do not add a dialogue system.

### 5. Dawn glide

The player wakes on the island. The bed returns them to the body. Dawn does not. Then the mist clears. The last mechanic is the day glide down to the field: body, toward camp smoke, no pickup. Use `TryStartCloudDescent` and `GP_GlideStart`. Do not write a second glide. The field under the island is not the walk floor. The field is not a tutorial beat after the landing.

## Done when

Each beat logs its pass in the open editor, and Luke has replayed that beat. Fill the result table in the playtest queue. A clean compile is not the pass.

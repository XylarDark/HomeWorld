# Tutorial Design Ideas — HomeWorld

**Author:** Beam (OpenCode plan model), game designer perspective, 2026-10-17.  
**Status:** Ideas for discussion — not canon, not a task list. Add to wherever the team sees fit.  
**Context:** The opening tutorial is the next build (per PRINCIPLE_FIT_LOCK §1). The existing tutorial sequence is in `Docs/VISION_BOARD.md` (Opening tutorial) and the work order is in `docs/context/OPENING_TUTORIAL_TASKS.md`. This doc adds design ideas on top of that sequence.

---

## 1. The market hole this game fills

Zelda teaches complex systems through world, silhouette, and light — no tutorials, no UI density, no hand-holding. Path of Exile has enormous depth through modifiers and itemization — but its onboarding is hostile. No game does both. HomeWorld's bet: PoE-like depth (7 virtue axes, marks, armor bench, one stroke) taught like Zelda (diegetic, one thing at a time, through play). The tutorial must prove this works. If the tutorial is just "walk, pick herb, heal spirit, glide," it's a Zelda tutorial — not a HomeWorld tutorial. The HomeWorld tutorial must include at least one touch of the virtue system.

## 2. The next task I would identify

**Design the "first mark" bridge** — a short, low-stakes encounter in the field (after the glide lands) where the player finds a marked herb, picks it, and (optionally) places it on the armor bench at home. This is the bridge between the tutorial (which teaches movement, gather, heal, craft, armor unlock) and the first real challenge (camp ease with Grace/Wrath). Without this bridge, the player hits the camp ease with zero exposure to the mark system — the game's core depth mechanic appears for the first time in a high-stakes encounter. That's a design failure.

## 3. Zelda + PoE synthesis principles for the tutorial

### From Zelda (teaching)
- **Teach one thing at a time.** Each beat teaches one concept. No compound lessons.
- **Teach through failure.** Gentle, recoverable failure (bonk) teaches "not yet" without punishment.
- **No text until after the action.** The player acts, then the world confirms. UI names the action after the player does it.
- **Environment is the teacher.** Silhouette, material, light, and spatial layout announce purpose.
- **The player discovers, not is told.** Short contextual hints (one line, not dialogue trees).
- **Show, don't tell.** Visual cues precede verbal ones.

### From Path of Exile (depth)
- **Complexity through modifiers, not new verbs.** The player learns one stroke; marks change how it behaves.
- **Itemization that matters.** A marked herb is not a stack — it's an instance with identity.
- **"One more run" loop.** The player wants to try again with a different mark combination.
- **Deep but readable.** At a glance, a rune says which pole it is. No hidden stat lines.

### The synthesis (HomeWorld's innovation)
- **One verb, many modifiers.** The player learns "I do one thing" in the tutorial. Then the camp ease says: "do the same thing, but now there's a shove." The player already knows the stroke; the new element is the interference.
- **Teach the bench with one mark.** The partner shows the bench. The player places one mark, turns it, commits. One mark. One axis. One success. No choices, no complexity. Just the motion.
- **The wisp shows its mark.** When the child offers the wisp, it has a faint visual (a rune shape). The player can see it but not name it. Later, at the armor bench, the same rune appears. The player connects them. Zelda-style "show, don't tell."

## 4. Specific design ideas

### Idea 1: The tutorial wisp carries a visible (but unnamed) mark
In Beat 2 (herb, spirit, child, shoulder), the wisp the child offers has a faint rune shape visible on it. The player can see it but is not told what it is. The wisp is consumed in the heal. Later, at the armor bench (Beat 4), the same rune shape appears on a mark. The player connects: "oh, the wisp from the tutorial had a mark like this." This is the first hint that wisps and marks are related — taught without a single word.

**Why this works:** Zelda's "show, don't tell." The player sees a shape, files it, and later recognizes it. No tutorial popup. No "this is a mark." The discovery is the player's.

### Idea 2: The first armor bench interaction is a "guided commit"
In Beat 4 (the two stations), the partner says one line: "Place it, turn it, commit." The player does exactly one mark placement. No choices, no complexity. The mark is the one from the tutorial wisp (Idea 1). The player places it on a piece of armor, turns it until the rune matches, and commits. One mark. One axis. One success. Then the mist clears.

**Why this works:** Teaches the bench's three verbs (place, turn, commit) with a real but low-stakes action. The player learns the motion before they learn the system. When they later face the camp ease, they already know how to use the bench — they just need to choose which mark.

### Idea 3: The bonk teaches failure recoverability (Beat 5)
When the player jumps off the mist-covered island, the bonk launches them back. The shoulder spirit's light dims slightly (one stack). The player learns: "I failed, I'm back, I'm slower, but I'm not dead." This is essential before the camp ease, where failure bonks you home. The player needs to know failure is survivable before they face the first real challenge.

**Why this works:** Zelda teaches through gentle failure (falling off a cliff, getting hit by a bokoblin). The bonk is HomeWorld's version — but it also introduces spirit-sickness, teaching the player that failure has a cost (slower movement) without being terminal. This is the "one more thing" pattern: the bonk is not just a lesson in "not yet," it's a preview of the spirit-sickness system.

### Idea 4: The "first mark" moment (new beat, after the glide)
After the tutorial ends (glide lands in field), the player finds a marked herb on the field. This is the first real encounter with the virtue system. The herb has a visible mark (a rune shape). The player can pick it (gather) or leave it. If they pick it, they now have a marked item. At the armor bench (back home), they can place it.

**Why this works:** This is the bridge between tutorial and first real challenge. The player has:
1. Seen a mark (Idea 1, tutorial wisp)
2. Used the bench (Idea 2, guided commit)
3. Learned failure is recoverable (Idea 3, bonk)

Now they find a marked item in the wild and know what to do with it. The camp ease is no longer the first time they see the mark system — it's the first time they use it in a challenge context.

### Idea 5: Teaching through the "same stroke"
The tutorial should use the same stroke (the one action) in different low-stakes contexts:
- Heal = a stroke (draw the rune on the spirit)
- Gather = a stroke (draw the rune on the herb)
- Glide = a stroke (steer through the descent)
- Bonk recovery = a stroke (the player learns to re-attempt)

Then the camp ease says: "do the same thing, but now there's a shove." The player already knows the stroke; the new element is the interference (Wrath shoves the finish off). This is the "author the hard form first, then the scaled-down steps" principle applied to the tutorial.

**Why this works:** The player never learns a new verb. They learn one verb, in four contexts, then face a challenge that uses that same verb with one new element (the shove). The difficulty comes from interference, not from new mechanics.

### Idea 6: The "one more thing" pattern (end of tutorial)
Zelda's shrines end with: "you've learned one thing, now here's one more." HomeWorld's tutorial should end with a moment — after the glide lands in the field — where the player sees something new: a marked herb, or a faint rune on a pine, or a spirit wisp hovering near a stone. Not interactive. Just visible. The player thinks: "what was that?" And the answer is in the next beat (the field gather, the camp ease).

**Why this works:** The tutorial doesn't end with "you've learned everything." It ends with "there's more to discover." This is the hook that makes the player want to keep playing. It's also the transition from tutorial to game: the tutorial teaches the verbs; the field introduces the system.

## 5. What's missing from the current tutorial design

1. **No "first mark" moment.** The tutorial unlocks crafting and armor but doesn't use marks. The player hits the camp ease with zero mark exposure.
2. **No explicit connection between wisp and mark system.** The wisp is consumed in the heal. The mark system appears later (camp ease). The player has no reason to connect them.
3. **No teaching of "failure is not death" beyond the bonk.** The bonk is in Beat 5, but spirit-sickness (the real failure cost) is not introduced. The player learns "not yet" but not "you can fail and keep going."
4. **No preview of the camp ease.** The player doesn't know what they're preparing for. The tutorial should hint at the camp (a distant pine camp visible from the homestead? a sound? a mention from the partner?).
5. **The armor bench is unlocked but not used.** Beat 4 unlocks the table. But the player doesn't place a mark. The bench is a locked door the player walks past. This is a missed teaching opportunity.

## 6. What I would NOT change

- **The 5-beat structure.** It's clean, sequenced, and each beat teaches one thing. Don't add more beats.
- **The diegetic teaching approach.** No UI tutorials, no popups, no "press X to jump." The place is the teacher.
- **The bonk as failure.** It's the right gentle consequence.
- **The "unlock and discover later" pattern.** Unlocking crafting/armor in the tutorial and using them later is Zelda-like and correct.
- **The no-new-verbs rule.** The tutorial should not introduce new mechanics. It should introduce the system through existing verbs.

## 7. The next task I would identify

**Design the "first mark" bridge** — a short, low-stakes encounter in the field (after the glide lands) where the player finds a marked herb, picks it, and (optionally) places it on the armor bench at home. This is the bridge between tutorial and first real challenge.

Specifically:
1. **Author the wisp's visible mark** (Idea 1) — a faint rune shape on the tutorial wisp. Needs an art decision (which rune? Grace? Love? Unmarked greybox?).
2. **Author the guided commit** (Idea 2) — one line from the partner, one mark placement, one commit. Needs a design decision on which mark and which axis.
3. **Author the "first mark" herb** (Idea 4) — a marked herb on the field, visible from the landing. Needs a level design decision on placement and visibility.
4. **Author the "one more thing" moment** (Idea 6) — a visible-but-non-interactive mark or wisp at the end of the tutorial. Needs an art/level decision.

Items 1-4 are design decisions, not code. They can be made in an interview round (like the existing OPENING_TUTORIAL_INTERVIEW.md rounds). The existing interview rounds (1-5) are already locked. These would be rounds 6-9.

## 8. Open questions for the team

1. Should the tutorial wisp show a mark (Idea 1), or stay unmarked (current recommendation)? Showing a mark teaches the system earlier but risks overwhelming. Leaving it unmarked preserves the "discover later" pattern.
2. Should the armor bench be used in the tutorial (Idea 2), or just unlocked? Using it teaches the motion; unlocking it preserves mystery.
3. Should the "first mark" herb exist (Idea 4), or should the player's first mark encounter be the camp ease? The first option bridges tutorial→game; the second preserves the "author the hard form first" principle.
4. Should the tutorial end with a "one more thing" moment (Idea 6), or end cleanly with the glide? The first creates a hook; the second preserves simplicity.

These are taste questions. They cannot be answered by research alone. They need the Lead's judgment, informed by the Phase 1 playtest (which will reveal whether players are ready for the mark system at the end of the tutorial).
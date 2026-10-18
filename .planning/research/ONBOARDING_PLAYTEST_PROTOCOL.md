# Onboarding playtest protocol (research deliverable)

**Source:** Phase 1 research (R-1-1), 2026-10-17.  
**Status:** Draft — pending Lead scheduling.  
**Canon impact:** none yet. Findings may amend `Docs/VISION_BOARD.md` Opening tutorial.

## Purpose

Test whether the 5-minute opening tutorial teaches without tutorials, and where it breaks. The opening is hands-on/mixed (walk → reveal → herb+wisp → heal → chores → mist clears → glide) with diegetic teaching ("UI may name an action after the player acts").

## Participants

- 5 testers, first-time (no prior HomeWorld exposure).
- Mix: 2 experienced with 3D adventure games, 2 casual, 1 non-gamer.
- Think-aloud protocol: ask them to narrate what they're doing and why.

## Setup

- Build at a named commit (record sha).
- Map: `L_SizeTest`. The floor is the walk pad in `Docs/level/L_SizeTest_METRICS.md`. The first session, before the five-tester study, is `Docs/qa/TUTORIAL_ISLAND_PLAYTEST.md`.
- Observer (not the designer) runs the session; designer watches silently.
- Record screen + audio. No hints unless stuck >2 min.

## Beats to observe (per VISION_BOARD.md Opening tutorial)

| # | Beat | Observe | Pass criteria |
|---|------|---------|---------------|
| 1 | Walk to cottage (pines/stones hide it) | Do they find it? How long? | Reaches cottage without hint, <90s |
| 2 | Reveal: partner, child, wounded spirit | Do they understand the scene? | Can describe who/what without being told |
| 3 | Child runs to spirit; player picks herb | Do they understand the herb is for the spirit? | Picks herb and approaches spirit |
| 4 | Child offers cloud wisp; combine with herb | Do they figure out combining? | Successfully heals spirit |
| 5 | Spirit lands on shoulder | Does the shoulder spirit read as "companion"? | Player references it naturally |
| 6 | Walk home with partner | Navigation clear? | Reaches home without getting lost |
| 7 | Homestead chores (herbs, kettle) | Do they understand the tasks? | Completes both without hint |
| 8 | Combining herb+wisp unlocks crafting station | Do they notice the unlock? | Interacts with station |
| 9 | Partner gives armor → unlocks attribute table | Do they understand armor attributes? | Equips armor, reads table |
| 10 | Mist clears, glide starts | Do they understand the transition? | Attempts glide without being told |
| 11 | Jump while mist present → bonk | Does the bonk teach "not yet"? | Understands bonk = "go back" |
| 12 | Glide (steered cloud descent) | Can they steer and land? | Lands in field, walk control returns |

## Post-session questions

1. What was the game about? (fantasy comprehension)
2. What were you supposed to do? (goal clarity)
3. What was confusing? (pain points)
4. What did you enjoy? (positive signals)
5. Would you play more? (retention signal)

## Failure modes to watch for (from research)

- Information overload (too many new concepts at once)
- Misaligned difficulty (too much/little assumed)
- Pacing too slow (boring) or too fast (overwhelming)
- Forgetting mechanics not reinforced
- Treating all players the same (no skip for veterans)

## Deliverable

A ranked list of teaching beats that fail, with evidence (video timestamp + quote). Feeds: opening tutorial edits, armor bench onboarding, onboarding interview (Q3).
---
name: scope-refinement
description: Use when the agent would otherwise guess a product, scope, or architecture decision, or when a design change would move scope or a module boundary - ask with the Cursor question picker, two questions max, then stop.
---

# Scope refinement

When the next step would be a guess, or a design change would move scope or architecture, interview the Lead. Do not merge the texts and do not pick the winner.

**Protocol:** [scope-refinement.md](../../../docs/human-use/scope-refinement.md)  
**Profile first:** [taste-profile.md](../../../docs/human-use/taste-profile.md)  
**Queue:** Taste Gate handoff. Do not open a second queue.

## When to load

- The agent would have to invent a product, scope, or architecture choice to keep going.
- A design change would add, drop, or redraw scope or a module boundary.
- Two canon texts disagree about the slice.

Do not load for a typo, a locked decision, or a one-file edit inside a boundary the Lead already chose.

## Procedure

1. Read the profile. If the fork is locked or a do-not, follow it and do not ask.
2. Name the fork in one sentence, and the file or brief it comes from. For scope or quanta, use the Hard Parts brief. For a module inside a settled quantum, use the Ousterhout brief.
3. Drop options that break a lock. Each question is a real fork, with one recommended option grounded in those files.
4. Stage a candidate via [taste-profiler](../taste-profiler/SKILL.md) before asking. Do not promote yet.
5. Ask through Cursor’s structured question picker, max 2 questions, include Skip. Do not paste the options as a markdown menu.
6. Write `Docs/handoffs/TASTE_GATE_<ID>.md` and stop. Do not build.
7. After the Lead answers, promote that pick (or reject on Skip). Skip means do not start the next round.
8. If a question was too thin or already locked, add a dated row under Refinements and retire that wording. Do not delete it.

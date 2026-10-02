---
name: steer-gate
description: Use when a steer, taste, or test decision is missing, or before an edit that sets feel, scope, or what done means. Name the limitation, give numbered options, stop. Not for a typo in a path already named.
---

# Steer gate

You cannot take responsibility for a change you cannot explain, you cannot see the playtest, and you cannot decide taste. A clean log is not evidence. Past about 60k tokens you are in the dumb zone. When any of those limits is about to be crossed, prompt the human and stop.

Load [Docs/handoffs/SLICE_SESSION.md](../../../Docs/handoffs/SLICE_SESSION.md) and [docs/human-use/OWNERSHIP.md](../../../docs/human-use/OWNERSHIP.md).

## Prompt, then stop

Use the environment's question tool when it has one. Otherwise emit this block and wait. Do not edit, commit, or declare done in the same turn.

```
Owner: human — <decision>
Job: steer | taste | test
Limitation: <cannot take responsibility | cannot see the playtest | cannot decide taste | dumb zone | hallucinated API | clean log is not evidence>
Why now: <what goes wrong if I guess>
I will not: <the work I must not invent>
Recommend: <one option>
Need from you:
  1. <recommended>
  2. <edit>
  3. <dictate>
  4. Skip
After you pick: <next step>
```

## Ask when

- The slice, the scenario, or ship/no-ship is not confirmed this chat.
- The change would set feel, scope, isolation, or what "done" means.
- You would be grading your own output.
- The chat is long enough that a handoff file should exist before more edits.

## Do not ask when

- Typo or one-line fix in a path already named.
- The human already confirmed the scenarios this chat.
- The next step is agent-owned flesh-out of a decision they already made. Say `Owner: agent` and the limitation you are not taking.

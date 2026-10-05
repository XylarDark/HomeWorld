# Route start

Point a session at this file to hand over the route. This file is the start. It is not the facts, and it is not a state.

Open this file when the developer already knows what the work is. If they do not, and no bite is named, open `DISCOVERY_START` instead.

Read these two files, in this order, before any other work:

1. UserHarness/docs/human-use/route-context.md
2. Docs/context/HOMEWORLD_ROUTE.md

## Session close

Do not stop the moment the current task is done. Close in this order, and do
not reach a later step while an earlier one still has work in it.

1. Finish every piece of work the agent can perform itself.
2. Ask, with the question tool, any question whose answer would let the agent
   continue. Carry on from the answer rather than closing.
3. Only when no agent work is left and the next step needs the developer's
   hands, ask whether a tutorial is wanted. Never offer one for agent-owned
   work.

The tutorial on offer is `Docs/qa/HUMAN_TUTORIAL.md`. This section is the
HomeWorld copy of the agnostic rule in `route-context.md`; where the two
differ, this one wins.

The first file is the three states and how to detect them. The second file is the HomeWorld facts. Write a fact only into the second file, and only after a yes. Do not write HomeWorld facts into the first file.

Nothing else is part of this handover.

## Context handoff

Route work may offer `DISCOVERY_START` only when evidence from the route shows
that discovery context is necessary (for example, the requested work or next
question is not named). State the evidence and ask whether to switch. Wait for
the developer's answer; run the discovery-start sequence only after they
confirm. If they decline, continue route work or stop at its boundary. Do not
trigger a handoff from topic keywords alone.

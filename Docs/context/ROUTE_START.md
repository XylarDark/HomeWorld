# Route start

Point a session at this file to hand over the route. This file is the start. It is not the facts, and it is not a state.

Read these two files, in this order, before any other work:

1. UserHarness/docs/human-use/route-context.md
2. Docs/context/HOMEWORLD_ROUTE.md

The first file is the three states and how to detect them. The second file is the HomeWorld facts. Write a fact only into the second file, and only after a yes. Do not write HomeWorld facts into the first file.

Nothing else is part of this handover.

## Context handoff

Route work may offer `DISCOVERY_START` only when evidence from the route shows
that discovery context is necessary (for example, the requested work or next
question is not named). State the evidence and ask whether to switch. Wait for
the developer's answer; run the discovery-start sequence only after they
confirm. If they decline, continue route work or stop at its boundary. Do not
trigger a handoff from topic keywords alone.

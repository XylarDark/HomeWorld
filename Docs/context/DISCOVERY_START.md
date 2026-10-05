# Discovery start (provider agnostic)

Point a session at this file to start discovery. It is not the route start.
This protocol applies in any IDE, chat surface, CLI, or agent runner. It does
not depend on a named provider, model, plugin, or editor feature. Follow the
sequence using the tools available in the current environment; if a capability
is unavailable, state that limitation instead of inventing an equivalent.

Read, in this order, before asking. The state file is first.

One file per step. Start the next read only after the previous read has returned. Do not batch the reads into one step.

1. UserHarness/docs/human-use/route-context.md
2. Docs/context/HOMEWORLD_ROUTE.md
3. UserHarness/docs/context/menu.md

Then ask one question at a time, in the current conversation. Do not require a
new chat or a particular UI.

The developer names any extra files. Only those get read.

The agent does not pick the files.

The agent does not name a bite.

The agent does not open a new chat.

If a second task appears, alert and stop.

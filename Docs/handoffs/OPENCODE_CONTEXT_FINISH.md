# Finish the pre-built context, then stop

This session finishes the context start. It does not do the glider or the clouds. That test is a later chat, after this one stops.

## What failed

On 2026-10-04 a session titled "Discovery start test" was pointed at `Docs/context/DISCOVERY_START.md` and told to follow it. It did not.

It read, in one step:

1. `Docs/context/HOMEWORLD_ROUTE.md`
2. `UserHarness/docs/context/menu.md`
3. `UserHarness/docs/human-use/route-context.md`

Then it asked what the bite for the session is.

That session is a closed_fail. It is not a file score of `Docs/context/DISCOVERY_START.md`. The state file has to be first. The route facts are second. The menu is third. Each read is its own step, after the previous read has returned. The agent does not name a bite. The question is not "what is the bite".

A CLI run also does not show up in the OpenCode window Lead already has open. The window stayed on "Review hw-art-pipeline-handoff.txt". Do not treat a CLI run as the test Lead can see.

## The two start files

Both are on main at `878abd9`. Do not make them the same.

`Docs/context/DISCOVERY_START.md` is discovery. It is not the route start. It reads, one file per step:

1. `UserHarness/docs/human-use/route-context.md` (the three states)
2. `Docs/context/HOMEWORLD_ROUTE.md` (the HomeWorld facts)
3. `UserHarness/docs/context/menu.md`

Then one question. The developer names any extra files. The agent does not pick files, does not name a bite, and does not open a new chat. A second task means alert and stop. Discovery does not open `Docs/context/ROUTE_START.md`.

`Docs/context/ROUTE_START.md` is the route handover. It is not discovery. It stays:

1. `UserHarness/docs/human-use/route-context.md`
2. `Docs/context/HOMEWORLD_ROUTE.md`

No menu. No question. Do not write a question step into it. Do not add the menu. Do not add the six section names.

## The edit

Do not edit `Docs/context/ROUTE_START.md`.

`Docs/context/DISCOVERY_START.md` is not a file fail. If it is edited, the edit stays discovery only: state file, then route facts, then the menu, one file per step, then one question. It does not name a bite. It does not open the route start.

Do not put HomeWorld facts into `UserHarness/docs/human-use/route-context.md`. That file carries the three states and the detection rule only.

Do not shrink or pad HomeWorld `AGENTS.md`. Do not restore `UserHarness/python/`.

## Do not touch while you edit

- The dirty working copy of `Docs/context/HOMEWORLD_ROUTE.md`. Do not commit it.
- `docs/handoffs/research/EXIT_WISP_CLOUD_LOOK_V1.md`
- `docs/handoffs/research/EXIT_WISP_CLOUD_RING_V1.md`
- `docs/handoffs/research/PROMPT_WISP_CLOUD_RING_V1.md`
- `Docs/handoffs/OPENCODE_CLOUD_ROUTE_CONTINUE.md`
- Island spec, mesh, `.blend`, `.uasset`, `.umap`, fall reset, `HomeWorldGameInstance.cpp`.

Leave this edit uncommitted. Do not push.

## Stop

When discovery is one file per step and the route start is unchanged, stop. Do not open the glider. Do not record a route fact. Do not ask Lead to name a bite.

Lead tests it in a new chat they open themselves in the OpenCode window, pointed at `Docs/context/DISCOVERY_START.md`. The pass is the state file, then the facts, then the menu, each in its own step, then one question that is not "what is the bite".

The glider and cloud test is that later chat, not this one. Its facts handoff is `Docs/handoffs/OPENCODE_CLOUD_ROUTE_CONTINUE.md`, and only after this context pass.

# Architecture — agent-owned

**Owner: agent.** You decide and record it. As of 2026-10-01 this is no longer a
human taste gate — see [OWNERSHIP.md](OWNERSHIP.md#ownership-map) and
[AGENT_DECISIONS.md](../decisions/AGENT_DECISIONS.md).

Fill a section when a task actually touches it. Do not fill it to look thorough,
and do not stop a task to ask permission to draw a boundary. What still belongs to
the human is art design, game mechanic design, and the test bar — none of which
this file covers.

Every decision here that changes a boundary gets a row in the decision log. The
log is what makes agent-owned architecture auditable; a boundary changed without a
row is the failure mode this file now has to avoid.

Settled boundaries: [architecture/HOMEWORLD_TRADEOFFS.md](../architecture/HOMEWORLD_TRADEOFFS.md).
Standing prompt for a new boundary: [tradeoff-analyst-brief.md](../architecture/tradeoff-analyst-brief.md).

Module depth inside the game client: [HOMEWORLD_DESIGN.md](../architecture/HOMEWORLD_DESIGN.md).
Standing prompt: [design-complexity-brief.md](../architecture/design-complexity-brief.md).

Unreal-specific notes (engine version, render pipeline, Data Assets, plugins, Epic
C++) belong in [templates/unreal](../templates/unreal/README.md) and
[`.cursor/rules/21-unreal-engine.mdc`](../../.cursor/rules/21-unreal-engine.mdc).
Unity: [templates/unity](../templates/unity/README.md).

## How the agent fills this in

1. **Draft the boundary in the log, not in an alert.** One sentence of purpose, the
   files it touches, and the alternative you rejected.
2. **Then write it here** if the change is durable — a shape that future tasks will
   keep hitting belongs in the file, not only in the log.
3. **One-line change to existing code?** No entry, no file edit. Routine.

Three shapes of outcome, and what each owes you:

| Outcome | Log entry | This file |
|---|---|---|
| Boundary moved or created | **Required** | Update it |
| Existing boundary confirmed, nothing moved | Optional | Leave it |
| Typo, one-file fix, no boundary involved | None | Leave it |

The rule that used to require your confirmation is gone. What replaced it is the
requirement that the decision be written down.

## What is not on the public internet

Domain knowledge, private APIs, product constraints, and decisions that exist only
in this team or this repo.

```
(fill in)
```

## Purpose (one sentence)

```
(fill in)
```

## Stack

Language, runtime, frameworks, engine version, platforms, render pipeline, frontend
and backend integration.

```
(fill in)
```

## Architectural vision

How the pieces fit: GUI vs logic, content layout, singletons vs data-driven, where
web-provided data enters.

```
(fill in)
```

## Directory map

Where new code, content, tests, and docs go.

```
(fill in)
```

## Services, models, plugins

```
(fill in)
```

## Design patterns in force

```
(fill in)
```

## Post-implementation checklist

What “done” means for this cycle. **The agent must not tick these** — completion
is a **Test** job and stays human (see [OWNERSHIP.md](OWNERSHIP.md#ownership-map)).
The agent supplies the evidence; you decide whether it is satisfied.

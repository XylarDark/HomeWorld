# HomeWorld architecture trade-offs

Least-worst choices already fixed by the vision and the conventions. The standing prompt for a later review is [tradeoff-analyst-brief.md](tradeoff-analyst-brief.md). Harness copy: [DevEnvTemplate/docs/architecture/tradeoffs.md](../../DevEnvTemplate/docs/architecture/tradeoffs.md).

Code inside the game quantum: [HOMEWORLD_DESIGN.md](HOMEWORLD_DESIGN.md).

Do not look for a better shape. These are the accepted costs. Anything not in the table is **not decided**.

## Ranked characteristics (from vision, not a wishlist)

1. **Change cost of gameplay** — behavior stays in C++ so it can be reviewed and reused ([CONVENTIONS.md](../CONVENTIONS.md)).
2. **One playable client** — PC, one Unreal project, one Editor. Act 1 is a lone wanderer; co-op is later.
3. **Art and content cohesion** — one stylized world, one shot list, content in `Content/` and `Docs/` canon.
4. **Operability** — Python and MCP drive the Editor; the harness is a separate repo so game code does not own the doctor.

Scale-out, multi-region availability, and a dedicated backend are not drivers. Do not add them as reasons to split.

## Quanta

| Quantum | Deploys as | Static coupling kept inside |
|---------|------------|-----------------------------|
| **Game** | One UE client (`Source/HomeWorld`, `Content/`, `Config/`) | Gameplay types, GAS, maps, assets the client loads |
| **Harness** | DevHarness repo, pinned gitlink `DevEnvTemplate/` | Doctor, skills, sync. It does not compile into the game |

`Docs/` (product canon) and `docs/` (engineering notes) are two document trees in the same game repo. They are not two services. On Windows only one folder name is visible at a time. That cost stays.

## Data ownership

C++ gameplay types are the single writer of combat, movement, inventory, and abilities. Blueprints assign meshes, materials, and input assets. Two writers of the same behavior (a Blueprint graph plus a C++ ability) is one quantum pretending to be two. Do not add that split.

## What we are giving up

- Gameplay cannot ship as an independent service.
- Blueprint graphs are a poor place for new rules; designers get data, not control flow.
- The harness pin moves only when we choose to take an upstream commit.

**Reversal:** only if the vision requires a second deployable process (a real server quantum) with its own data owner. That is not the current Act 1 client.

## Skipped (no business driver yet)

Do not invent these:

- Microservices, event choreography, or a saga between game systems
- A consistency window for co-op or Steam sessions
- A second database or analytical store
- Filling the blank purpose fields in [human-use/architecture.md](../human-use/architecture.md)

## Fitness already in force

- New abilities are C++ classes; GA_* Blueprints stay data-only ([CONVENTIONS.md](../CONVENTIONS.md)).
- One UnrealMCP bridge. Do not add a second Editor MCP.
- Uasset commits follow the allowlist policy. Editor resaves are not an architecture change.

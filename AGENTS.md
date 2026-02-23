# HomeWorld – Agent context

**Project:** HomeWorld — Unreal Engine 5.7 game (Open World / World Partition). Targets UE 5.7 (compatible with 5.7.x, including 5.7.3). Theme: "Love as Epic Quest"; Act 1 focus is lone wanderer (explore → fight → build). See [docs/PROTOTYPE_VISION.md](docs/PROTOTYPE_VISION.md) and [docs/STACK_PLAN.md](docs/STACK_PLAN.md) for vision and stack.

**Programmatic by default:** As much work as possible is done in C++. New gameplay systems, movement, input, and core logic go in C++; Blueprint is for content, level design, and designer overrides. See [docs/CONVENTIONS.md](docs/CONVENTIONS.md) for the code-first checklist and C++ vs Blueprint split.

**Code:** C++ lives in `Source/HomeWorld/`. Default pawn: `AHomeWorldCharacter`; default game mode: `AHomeWorldGameMode`. Both use Enhanced Input for movement and look.

**Stack (enabled plugins):** Enhanced Input, PCG, Gameplay Abilities, Steam Sockets, Day Sequence. Mass/swarms plugin TBD when swarms are added (Mass Entity is deprecated). Config in `Config/`; project layout and rules in `.cursor/rules/` (Unreal C++, Blueprint, project).

**Setup and validation:** [docs/SETUP.md](docs/SETUP.md) (includes validation checklist). Cursor rules ship with the repo in `.cursor/rules/` — they are loaded automatically when the project is opened in Cursor. Key rules: `unreal-cpp.mdc` (C++ conventions + UE 5.7 API pitfalls), `08-project-context.mdc` (HomeWorld overview), `09-mcp-workflow.mdc` (MCP-first priorities). Always check `docs/KNOWN_ERRORS.md` before making changes in areas where errors have been recorded.

**MCP-first development:** When the Unreal Editor is running and MCP tools are connected (unrealMCP), prefer live Editor manipulation via MCP over writing scripts or giving manual instructions. See `.cursor/rules/09-mcp-workflow.mdc` and [docs/MCP_SETUP.md](docs/MCP_SETUP.md).

**Current tasks:** [docs/TASKLIST.md](docs/TASKLIST.md) — master task list; each task links to a detailed doc in `docs/tasks/`.

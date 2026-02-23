# HomeWorld – Agent context

**Project:** HomeWorld — Unreal Engine 5.7 game (Open World / World Partition). Targets UE 5.7 (compatible with 5.7.x, including 5.7.3). Theme: "Love as Epic Quest"; Act 1 focus is lone wanderer (explore → fight → build). See [docs/PROTOTYPE_VISION.md](docs/PROTOTYPE_VISION.md) and [docs/STACK_PLAN.md](docs/STACK_PLAN.md) for vision and stack.

**Programmatic by default:** As much work as possible is done in C++. New gameplay systems, movement, input, and core logic go in C++; Blueprint is for content, level design, and designer overrides. See [docs/CONVENTIONS.md](docs/CONVENTIONS.md) for the code-first checklist and C++ vs Blueprint split.

**Code:** C++ lives in `Source/HomeWorld/`. Default pawn: `AHomeWorldCharacter`; default game mode: `AHomeWorldGameMode`. Both use Enhanced Input for movement and look.

**Stack (enabled plugins):** Enhanced Input, PCG, Gameplay Abilities, Steam Sockets, Day Sequence. Mass/swarms plugin TBD when swarms are added (Mass Entity is deprecated). Config in `Config/`; project layout and rules in `.cursor/rules/` (Unreal C++, Blueprint, project).

**Setup and validation:** [docs/SETUP.md](docs/SETUP.md) (includes validation checklist). When editing C++, Blueprint, or project/config files, follow the corresponding `.cursor/rules/` conventions.

**Current tasks:** [docs/TASKLIST.md](docs/TASKLIST.md) — master task list; each task links to a detailed doc in `docs/tasks/`.

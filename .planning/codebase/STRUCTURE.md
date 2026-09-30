---
last_mapped_commit: 94158e9416cc44954f4fdb11e0de696e31836276
last_mapped_at: 2026-09-28
---
﻿# Structure

**Analysis Date:** 2026-09-28

## Directory Layout

```
HomeWorld/
├── Source/
│   ├── HomeWorld/           # Runtime C++ gameplay module
│   └── HomeWorldEditor/     # Editor module + commandlets
├── Content/                 # UE assets + Content/Python automation
├── Maps/                    # VS_MVP + Preview_* levels
├── Config/                  # UE ini
├── Config/                  # Harness JSON (preflight, DET pin)
├── Plugins/                 # UnrealMCP (gitignored install)
├── scripts/                 # Node doctor/preflight/evidence
├── docs/                    # UE engineering docs (lowercase)
├── Docs/                    # MVP swarm canon (capital D)
├── swarm/                   # PHASE_BOARD, SWARM_OPS, agents
├── UserHarness/          # DevHarness gitlink
├── AssetCreation/, blender/, Lib/, refs/, VisionBoard/
├── .opencode/               # GSD Core runtime (UNTRACKED — do not commit)
├── .planning/               # GSD host planning (this tree)
├── HomeWorld.uproject
├── package.json
├── AGENTS.md, START_HERE.md
└── .github/workflows/       # ci.yml, validate.yml
```

## Key Locations

| Path | Role |
|------|------|
| `Source/HomeWorld/*.h|.cpp` | Gameplay types (~70+ headers) |
| `Source/HomeWorld/HomeWorld.Build.cs` | Runtime module deps |
| `Maps/VS_MVP` | Vertical slice playable map |
| `Maps/Preview_Homestead_Night` | Homestead kit preview |
| `Maps/Preview_Lookout_To_Planet` | Transit / planet lookout |
| `Maps/Preview_Forest_Day` | Forest day preview |
| `Content/Python/` | Editor automation + `tests/` |
| `swarm/PHASE_BOARD.md` | **Only** live product phase authority |
| `Docs/` | Signed product canon |
| `docs/` | Engineering / setup / KNOWN_ERRORS |
| `.planning/codebase/` | GSD codebase map |

## Naming Conventions

- C++ types: `AHomeWorld*`, `UHomeWorld*`, `FHomeWorld*` / `E*` enums with HomeWorld prefix
- Abilities: C++ `UHomeWorld*Ability` + Blueprint `GA_*` reparented data-only
- Python: `snake_case.py` under `Content/Python/`
- Swarm handoffs: `Docs/handoffs/*.md`, phase docs `Docs/NN_*.md`

## Where Not to Put Things

- Do not invent product Acts under `.planning/phases/` unless Lead/PHASE_BOARD names them
- Do not commit `.opencode/` (currently untracked)
- Do not merge `Docs/` and `docs/` trees
- Do not treat `VisionBoard/MVP/` as live GDD (`AGENTS.md` quarantine)

---
*Structure analysis: 2026-09-28*

# HomeWorld – Agent context

**Project:** HomeWorld — Unreal Engine 5.7 game (Open World / World Partition). Targets UE 5.7 (compatible with 5.7.x, including 5.7.3). Theme: "Love as Epic Quest"; Act 1 focus is lone wanderer (explore → fight → build). See [docs/PROTOTYPE_VISION.md](docs/PROTOTYPE_VISION.md) and [docs/STACK_PLAN.md](docs/STACK_PLAN.md) for vision and stack. **Lock:** Engine 5.7 only; platform PC + Steam Early Access; do not add engine or platform variants without team decision.

**Programmatic by default:** As much work as possible is done in C++. New gameplay systems, movement, input, and core logic go in C++; Blueprint is for content, level design, and designer overrides. See [docs/CONVENTIONS.md](docs/CONVENTIONS.md) for the code-first checklist and C++ vs Blueprint split.

**Code:** C++ lives in `Source/HomeWorld/`. Default pawn: `AHomeWorldCharacter`; default game mode: `AHomeWorldGameMode`. Both use Enhanced Input for movement and look.

**Stack (enabled plugins):** Enhanced Input, PCG, Gameplay Abilities, Steam Sockets, Day Sequence. For Week 2 family agents, enable UE 5.7 recommended Mass Entity + Mass AI, StateTree, ZoneGraph, SmartObjects (see [SETUP.md](docs/SETUP.md)). Config in `Config/`; project layout and rules in `.cursor/rules/` (Unreal C++, Blueprint, project).

**MCP-first development:** When the Unreal Editor is running and MCP tools are connected (unrealMCP), prefer live Editor manipulation via MCP over writing scripts or giving manual instructions. See `.cursor/rules/09-mcp-workflow.mdc` and [docs/MCP_SETUP.md](docs/MCP_SETUP.md). For using external LLMs to generate Editor automation scripts, see [docs/EXTERNAL_AI_AUTOMATION.md](docs/EXTERNAL_AI_AUTOMATION.md).

**Current tasks:** [docs/TASKLIST.md](docs/TASKLIST.md) — master task list; each task links to a detailed doc in `docs/tasks/`.

## Dev environment setup

1. Install UE 5.7, clone this repo, open `HomeWorld.uproject`.
2. Run `Setup-MCP.bat` (one-time MCP bridge install).
3. Run `Build-HomeWorld.bat` to compile C++ (requires Editor closed or Live Coding off).
4. Open Editor, restart Cursor, verify MCP green dot in status bar.
5. See [docs/SETUP.md](docs/SETUP.md) for the full checklist.

**Enhanced Input** is applied automatically when the Editor loads (`Content/Python/init_unreal.py`). You do not need to run `setup_enhanced_input.py` unless movement still fails (troubleshooting).

## Testing

- **Automated (Python):** `PythonAutomationTest` plugin is enabled. Tests in `Content/Python/tests/` (named `test_*.py`) are auto-discovered. Run via Editor: Tools > Test Automation.
- **PIE tests:** `Content/Python/pie_test_runner.py` validates character spawn, ground contact, animation, and PCG. Run via MCP: `execute_python_script("pie_test_runner.py")`, then read `Saved/pie_test_results.json`.
- **CI:** GitHub Actions (`.github/workflows/validate.yml`) — Python lint, JSON schema checks, C++ header/source pairing, doc freshness.

## Code style

- **C++:** PascalCase types, camelCase locals; Unreal prefixes (`A`, `U`, `F`, `E`, `I`). Include own header first. See `.cursor/rules/unreal-cpp.mdc`.
- **Python:** PEP 8, type hints, 4-space indent. UE scripts must be idempotent (check-before-create). See `.cursor/rules/12-python.mdc`.
- **Commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`). See `.cursor/rules/04-git-workflow.mdc`.

## PR and commit guidelines

- Use Conventional Commits format for all commit messages.
- PowerShell shell: use `;` not `&&` for command chaining; use here-strings for multi-line commit messages.
- Pre-commit: lint, build check, no secrets, no `__pycache__` or temp JSON in tracked files.

## Security

- Never commit secrets, API keys, or `.env` files. Use `.env.example` for templates.
- `Saved/`, `Plugins/UnrealMCP/`, and `__pycache__/` are gitignored.
- Validate all external input at boundaries. See `.cursor/rules/02-security.mdc`.

## Setup and validation

[docs/SETUP.md](docs/SETUP.md) (includes validation checklist). Cursor rules ship with the repo in `.cursor/rules/` — they are loaded automatically when the project is opened in Cursor. Key rules: `unreal-cpp.mdc` (C++ conventions + UE 5.7 API pitfalls), `08-project-context.mdc` (HomeWorld overview), `09-mcp-workflow.mdc` (MCP-first priorities), `automation-standards.mdc` (variables-with-no-access procedure for Editor automation). Always check `docs/KNOWN_ERRORS.md` before making changes in areas where errors have been recorded. When adding automation for Editor/engine features, follow the "variables no access" procedure: identify required settings, verify automation access, document no-access items and manual steps (see `.cursor/rules/automation-standards.mdc` and e.g. `docs/PCG_VARIABLES_NO_ACCESS.md`).

- **Session continuity:** Read `docs/SESSION_LOG.md` at task start to load prior context. Append a summary at task end. See `.cursor/rules/07-ai-agent-behavior.mdc` (Session Continuity, AI Agent Checklist).

# Development with Cursor

HomeWorld is set up so that AI agents and humans follow the same conventions when working in Cursor.

- **Agent context:** [AGENTS.md](../AGENTS.md) at the repo root gives a short project summary, the **programmatic-by-default** policy, and where code and docs live. Use it to onboard agents and tools.
- **Cursor rules:** Under [.cursor/rules/](../.cursor/rules/), file-specific rules apply when you work with:
  - **Unreal C++** (`**/*.cpp`, `**/*.h`): naming, UPROPERTY/UFUNCTION, module boundaries, include order.
  - **Unreal Blueprint** (`**/*.uasset`): when to use Blueprint vs C++, naming, and that core movement/input/camera are in C++.
  - **Unreal project/config** (`**/*.uproject`, `**/Config/*.ini`): project layout, game module, plugins, default pawn and game mode.
  - **DevEnvTemplate rules** (00–20 series): core principles, code quality, security, testing, git workflow, error handling, documentation, AI-agent behavior, and tech-specific (TypeScript, Python, JSON, etc.). These are copied from [DevEnvTemplate](../DevEnvTemplate) and can be re-synced from there. Project context for HomeWorld is in AGENTS.md and docs/.
- **Building:** Generate Visual Studio project files from the `.uproject`, then build the **HomeWorld** and **HomeWorldEditor** targets. See the **Building (C++)** section in [SETUP.md](SETUP.md). To build from the command line, use MSBuild or the IDE after generating the solution once.
- **Compound Engineering plugin:** Recommending its commands when the use case fits is policy; the agent suggests plugin workflows (e.g. `/workflowsreview`, `/workflowsplan`) instead of doing that work inline. See [.cursor/rules/10-compound-engineering.mdc](../.cursor/rules/10-compound-engineering.mdc).

When asking Cursor to change C++ or Blueprint behavior, the rules ensure suggestions align with programmatic-by-default and the existing HomeWorld layout.

**Pinned environment (toolchain, MCP, Cursor plugins):** [DEV_ENV_MATRIX.md](DEV_ENV_MATRIX.md). Optional recommended VS Code/Cursor extensions: repo [`.vscode/extensions.json`](../../.vscode/extensions.json).

## DevEnvTemplate (environment doctor)

The project includes [DevEnvTemplate](../DevEnvTemplate) as a subfolder. It provides a **health check** for the development environment (diagnose, prescribe, auto-fix). To use it:

1. **One-time setup:** From the repo root, run `npm run doctor:build` to install and build the DevEnvTemplate tooling (requires Node.js 20+).
2. **Run health check:** `npm run doctor` — scans the project and reports on security, code quality, testing, CI/CD, and documentation gaps.
3. **Apply auto-fixes:** `npm run doctor:fix` — applies safe fixes (e.g. add `.env.example`, update `.gitignore`).

DevEnvTemplate is aimed at Node/TypeScript/Python projects; for an Unreal (C++/Blueprint) project its reports are partial but still useful for repo hygiene, secrets, and docs. For full DevEnvTemplate usage and LLM bootstrap instructions, see [DevEnvTemplate/BOOTSTRAP.md](../DevEnvTemplate/BOOTSTRAP.md).

# Development with Cursor

HomeWorld is set up so that AI agents and humans follow the same conventions when working in Cursor.

- **Agent context:** [AGENTS.md](../../AGENTS.md) at the repo root gives a short project summary, the **programmatic-by-default** policy, and where code and docs live. Use it to onboard agents and tools.
- **Agent skills:** Layer-synced from DevEnvTemplate into [`.agents/skills/`](../../.agents/skills/) (agent-workflow, plan-first, secure-coding, etc.). Skills load when relevant; they do not replace HomeWorld always-applied rules.
- **Cursor rules:** Under [.cursor/rules/](../../.cursor/rules/), file-specific rules apply when you work with:
  - **Unreal C++** (`**/*.cpp`, `**/*.h`): naming, UPROPERTY/UFUNCTION, module boundaries, include order.
  - **Unreal Blueprint** (`**/*.uasset`): when to use Blueprint vs C++, naming, and that core movement/input/camera are in C++.
  - **Unreal project/config** (`**/*.uproject`, `**/Config/*.ini`): project layout, game module, plugins, default pawn and game mode.
  - **UE stack (glob-scoped from template):** `21-unreal-engine.mdc`, `22-unreal-editor-ui.mdc` — general Unreal practices; HomeWorld keeps version-specific policy in `ue57-sources.mdc` / `ue57-editor-ui.mdc` and [UE57_TECH.md](../UE/UE57_TECH.md).
  - **HomeWorld / DevEnvTemplate always-applied rules** (00–20 series and project-specific): still in use. Newer DevEnvTemplate **retires** those always-on files for *new* adoptions (migrate into `AGENTS.md` + skills). HomeWorld **keeps** them until a dedicated migration; do not delete them during routine sync.
- **Building:** Generate Visual Studio project files from the `.uproject`, then build the **HomeWorld** and **HomeWorldEditor** targets. See the **Building (C++)** section in [SETUP.md](../SETUP.md). To build from the command line, use MSBuild or the IDE after generating the solution once.
- **Compound Engineering plugin:** Recommending its commands when the use case fits is policy; the agent suggests plugin workflows (e.g. `/workflowsreview`, `/workflowsplan`) instead of doing that work inline. See [.cursor/rules/10-compound-engineering.mdc](../../.cursor/rules/10-compound-engineering.mdc).

When asking Cursor to change C++ or Blueprint behavior, the rules ensure suggestions align with programmatic-by-default and the existing HomeWorld layout.

**Pinned environment (toolchain, MCP, Cursor plugins):** [DEV_ENV_MATRIX.md](DEV_ENV_MATRIX.md). Optional recommended VS Code/Cursor extensions: repo [`.vscode/extensions.json`](../../.vscode/extensions.json).

## DevEnvTemplate (doctor + layer sync)

Pinned checkout: [DevEnvTemplate/](../../DevEnvTemplate/) gitlink (refresh from the
template working tree when adopting Human Use steer/taste/test). Full template docs:
[DevEnvTemplate/docs/SYNC.md](../../DevEnvTemplate/docs/SYNC.md), [BOOTSTRAP.md](../../DevEnvTemplate/BOOTSTRAP.md).

### Doctor

1. **One-time setup:** From the repo root, run `npm run doctor:build` (install + build under `DevEnvTemplate/`). Template package prefers Node.js **24+**; host `package.json` still allows 20+ for older local installs.
2. **Run health check:** `npm run doctor`.
3. **Apply auto-fixes:** `npm run doctor:fix`.

Reports are partial for Unreal (C++/Blueprint) but useful for repo hygiene, secrets, and docs.

### Layer sync (refresh skills / entry shapes)

Sync copies **only allowlisted paths**; dry-run is the default. It never overwrites root `AGENTS.md`, never copies MCP configs, and never injects retired always-on rules.

```bash
# Preview (agent-context + operational-memory)
npm run sync

# Apply missing files only
npm run sync:apply
```

PowerShell: if npm mangles flags, call the CLI directly:

```powershell
node DevEnvTemplate/dist/scripts/sync/cli.js --layer agent-context,operational-memory --template ./DevEnvTemplate --project-root .
```

**Canonical automation gaps for HomeWorld:** [docs/Automation/AUTOMATION_GAPS.md](../Automation/AUTOMATION_GAPS.md). The template entry shape at `docs/operational/automation-gaps.md` is a pointer only.

**Human ownership:** [docs/human-use/OWNERSHIP.md](../human-use/OWNERSHIP.md) — you
steer, make taste, and test; the agent executes and stops when a job you own is
missing. Practices Cursor does not enforce: [cursor-cannot](../human-use/cursor-cannot/README.md).

**Opt-in extras:** Copy individual skills from [`.agents/skills-extras/`](../../.agents/skills-extras/) into `.agents/skills/` when needed (see [`.agents/README.md`](../../.agents/README.md)).

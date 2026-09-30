# Cursor Rules Directory

HomeWorld-specific Unreal rules plus technology-agnostic rules inherited from the
[UserHarness pin](../DevEnvTemplate). Rules are **opt-in by glob or
agent-requested**; `AGENTS.md` is the single always-on surface.

## Attach policy

### alwaysApply: 0

**No rule is `alwaysApply: true`.** `AGENTS.md` carries the always-on context.
Rules load when a glob matches the files being touched, or when the agent asks
for one by description. Adding an always-apply rule is a regression — see
`Docs/handoffs/PIN_SYNC_POLICY.md` (NEVER_AUTO for growth/shrink) and the
"Always-Applied Rule Budget Exceeded" row in
[docs/Setup/DOCTOR_POLICY.md](../../docs/Setup/DOCTOR_POLICY.md).

History: HR-B2 cut 15 → 3, and P4 cut 3 → 0 by retiring `07-ai-agent-behavior`
and `08-project-context` (both were near-duplicates of `AGENTS.md`) and
glob-scoping `20-full-automation-no-manual-steps` (whose invariant is already
stated in `AGENTS.md`). Those two files are kept as **tombstones** — retired, not
deleted — so a surviving reference resolves to a pointer instead of silently
loading stale guidance.

| Was always-apply | Now | Why |
|---|---|---|
| `07-ai-agent-behavior.mdc` | tombstone, `alwaysApply: false` | Duplicated `AGENTS.md`; its only unique section read `Saved/Logs/automation_*` files frozen since WAVE F deleted the loop that wrote them |
| `08-project-context.mdc` | tombstone, `alwaysApply: false` | A stale fork of `AGENTS.md`, with 3 references to files that do not exist |
| `20-full-automation-no-manual-steps.mdc` | `alwaysApply: false`, globs `Content/Python`, `Tools`, `.github/workflows`, `docs/Automation`, `.cursor/skills` | Invariant is in `AGENTS.md`; this file keeps the gap-log format and the host gate |

### Opt-in by glob

| Group | Files |
|---|---|
| Code | `00-core-principles`, `05-error-handling`, `16-feature-debug-instrumentation` |
| Tests | `03-testing` |
| Python | `12-python` |
| Shell | `15-shell-scripts` |
| JSON/YAML | `14-json-yaml` |
| MCP | `09-mcp-workflow` (transport, capability, crash rules); `09b-mcp-utility-scripts` (harness scripts + envelope) |
| Automation policy | `automation-standards` (tooling ladder, Lead gates); `19-automation-gaps` (gap procedure + log format pointer) |
| Lookdev evidence | `lookdev-evidence-standards` (PA-E, MRQ, capture preconditions) |
| Automation invariant | `20-full-automation-no-manual-steps` |
| Game content | `18-game-development-principles` (`.uasset`/`.umap`/`Maps/`/`Lib/`) |
| UE live | `21-unreal-engine`, `22-unreal-editor-ui`, `unreal-*`, `ue58-sources`, `ue58-editor-ui` |
| Docs layout | `19-docs-directory-structure` (`docs/**`, `Docs/**`) |
| Plugins | `10-compound-engineering`, `11-parallel-plugin` (`.cursor/**`) |
| PCG | `pcg-best-practices` |

### Description-only (agent-requested)

- `07-ai-agent-behavior.mdc`, `08-project-context.mdc` — **tombstones.** Say
  retired; do not restore.
- `19-automation-cycle.mdc` — WAVE F quarantine pointer; do **not** resurrect
  cycle bodies.

### Historical (narrow glob)

- `ue57-sources.mdc`, `ue57-editor-ui.mdc` — glob `docs/UE/UE57_*.md` only.
  Prefer `ue58-*` for active work. Both are marked HISTORICAL.

### Retired — stay deleted

`01`, `02`, `04`, `06`, `11-javascript`, `13-markdown`, `17` → migrated to
`.agents/skills/` or `AGENTS.md`.

Note `11-javascript` was retired for exactly the reason P4 finished: this is a
UE C++/Python host with no JavaScript product surface. P4 removed the surviving
TypeScript and JS examples from `05-error-handling.mdc` and rewrote
`03-testing.mdc`, which had carried Vitest/Jest/React Testing Library/`npm
install` instructions into a repo that has no `package.json` test setup.

## Canonical examples

Rules point to canonical examples in the repo rather than inlining long code.

- **C++:** `unreal-cpp.mdc` → pawn `HomeWorldCharacter.h/.cpp`; GAS:
  `HomeWorldGameplayAbility.h`, `HomeWorldAttributeSet.h`.
- **Python:** `12-python.mdc` → level/landscape `level_loader.py`; PCG
  automation `create_pcg_forest.py` (limits in
  [`docs/PCG/PCG_VARIABLES_NO_ACCESS.md`](../../docs/PCG/PCG_VARIABLES_NO_ACCESS.md)).

## Maintenance

- Refresh from the UserHarness pin by copying
  `DevEnvTemplate/.cursor/rules/*.mdc` → `.cursor/rules/`, **preserving** the
  HomeWorld `unreal-*` / `ue58-*` rules, the tombstones, and the zero
  `alwaysApply` count.
- Never introduce a reference to a retired rule. The retirement map is
  `DevEnvTemplate/scripts/tools/cursor-rules-adapter.ts`:
  `02-security.mdc` → `.agents/skills/secure-coding`;
  `04-git-workflow.mdc` → `AGENTS.md` (conventions).
- See [docs/Setup/CURSOR_DEV.md](../../docs/Setup/CURSOR_DEV.md) and
  [DevEnvTemplate/BOOTSTRAP.md](../DevEnvTemplate/BOOTSTRAP.md).

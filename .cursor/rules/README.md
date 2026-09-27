# Cursor Rules Directory

This directory contains Cursor rules for the HomeWorld project. It includes technology-agnostic rules from [DevEnvTemplate](../DevEnvTemplate) and HomeWorld-specific Unreal rules.

## Attach policy (ALWAYSAPPLY_AUDIT_V1)

### AlwaysApply — N=3 (session-wide trio)

Do **not** grow or shrink this set without a new Research EXIT.

| File | Role |
|------|------|
| `07-ai-agent-behavior.mdc` | Slim agent card (WAVE F refuse, MCP pointer, taste-gate) |
| `08-project-context.mdc` | Session project card (overlaps `AGENTS.md`; accepted tax) |
| `20-full-automation-no-manual-steps.mdc` | Autonomy invariant + host-gate cite to SWARM_OPS |

Host legality (DESKTOP parent-only, no cloud DESKTOP trials): [swarm/SWARM_OPS.md](../../swarm/SWARM_OPS.md) §14 / §16 — cite, do not fork into new alwaysApply rules.

### Opt-in by glob (not alwaysApply)

| Group | Files (typical) |
|-------|-----------------|
| Code | `00-core-principles`, `05-error-handling`, `16-feature-debug-instrumentation` |
| Python | `12-python` |
| Shell | `15-shell-scripts` |
| JSON/YAML | `14-json-yaml` |
| Tests | `03-testing` |
| MCP | `09-mcp-workflow` (Python/Tools/uproject — not Source) |
| Automation bible | `automation-standards` |
| Game content | `18-game-development-principles` (uasset/umap/Maps/Lib — not Content/**) |
| UE live | `21-unreal-engine`, `22-unreal-editor-ui`, `unreal-*`, `ue58-sources`, `ue58-editor-ui` (ue58: uproject/Source/Config/Plugins — not Content/**) |
| Docs layout | `19-docs-directory-structure` (`docs/**`, `Docs/**` only) |
| Gaps procedure | `19-automation-gaps` (`docs/Automation/AUTOMATION_GAPS.md`) |
| Plugins | `10-compound-engineering`, `11-parallel-plugin` (`.cursor/**`) |
| PCG | `pcg-best-practices` |

### Description-only

- `19-automation-cycle.mdc` — WAVE F quarantine pointer; do **not** resurrect cycle bodies.

### Historical (narrow)

- `ue57-sources.mdc`, `ue57-editor-ui.mdc` — glob only `docs/UE/UE57_*.md`; prefer ue58 for active work.

Retired (bite 6.2, stay deleted): `01`/`02`/`04`/`06`/`11-javascript`/`13-markdown`/`17` → skills.

## Canonical examples

Rules should point to **canonical examples** in the repo (e.g. `Source/HomeWorld/` or `Content/Python/`) instead of inlining long code.

- **C++:** `unreal-cpp.mdc` — pawn: `HomeWorldCharacter.h/.cpp`; GAS: `HomeWorldGameplayAbility.h`, `HomeWorldAttributeSet.h`.
- **Python:** `12-python.mdc` — level/landscape: `level_loader.py`; PCG automation: `create_pcg_forest.py` (see `docs/PCG/PCG_VARIABLES_NO_ACCESS.md` for limits).

Full list and links: [docs/UE/UE57_TECH.md](../../docs/UE/UE57_TECH.md).

## Maintenance

- To refresh rules from DevEnvTemplate: copy `DevEnvTemplate/.cursor/rules/*.mdc` to `.cursor/rules/` (**preserve** HW `unreal-*` / `ue58-*` / alwaysApply trio `07`/`08`/`20`).
- See [docs/Setup/CURSOR_DEV.md](../../docs/Setup/CURSOR_DEV.md) and [DevEnvTemplate/BOOTSTRAP.md](../DevEnvTemplate/BOOTSTRAP.md) for setup and usage.
- Sync must **not** inject retired always-on rules or grow alwaysApply without Research (PIN_SYNC NEVER_AUTO for growth/shrink).

# Cursor Rules Directory

This directory contains Cursor rules for the HomeWorld project. It includes technology-agnostic rules from [DevEnvTemplate](../DevEnvTemplate) and HomeWorld-specific Unreal rules.

## Structure

### Always-Applied Rules (HR-B2 session-wide trio)

- **07-ai-agent-behavior.mdc** - Meta-rules for AI agent tool usage and communication
- **08-project-context.mdc** - HomeWorld / DevEnvTemplate context; see also [AGENTS.md](../../AGENTS.md) and `docs/`
- **20-full-automation-no-manual-steps.mdc** - Autonomy invariant (AUTOMATION_GAPS; no “manual steps”)

### Globbed / legacy (00–06 and peers — not alwaysApply)

- **00-core-principles.mdc**, **03-testing.mdc**, **05-error-handling.mdc** — narrowed globs (bite 6.1). **01/02/04/06/17** deleted bite 6.2 → existing skills (`code-structure`, `secure-coding`, `documentation`, `plan-first`).
- **16-feature-debug-instrumentation.mdc** - Debug instrumentation policy for new features
- **19-docs-directory-structure.mdc** - Place new docs in correct docs/ subdir per [docs/DOCS_LAYOUT.md](../../docs/DOCS_LAYOUT.md)

### Stack-Specific Rules (Conditional, from DevEnvTemplate)

- **12-python.mdc**, **14-json-yaml.mdc**, **15-shell-scripts.mdc** - Apply when editing matching file types. (**11-javascript**, **13-markdown** retired bite 6.2; DET-generic **01/02/04/06/17** deleted — use `.agents/skills` equivalents.)

### HomeWorld-Specific Rules (Unreal)

- **unreal-project.mdc** - Project layout, .uproject, Config (`**/*.uproject`, `**/Config/*.ini`)
- **unreal-cpp.mdc** - C++ conventions (`**/*.cpp`, `**/*.h`)
- **unreal-blueprint.mdc** - Blueprint vs C++ (`**/*.uasset`)
- **unreal-gas.mdc** - Gameplay Ability System

## Canonical examples

Rules should point to **canonical examples** in the repo (e.g. `Source/HomeWorld/` or `Content/Python/`) instead of inlining long code.

- **C++:** `unreal-cpp.mdc` — pawn: `HomeWorldCharacter.h/.cpp`; GAS: `HomeWorldGameplayAbility.h`, `HomeWorldAttributeSet.h`.
- **Python:** `12-python.mdc` — level/landscape: `level_loader.py`; PCG automation: `create_pcg_forest.py` (see `docs/PCG/PCG_VARIABLES_NO_ACCESS.md` for limits).

Full list and links: [docs/UE/UE57_TECH.md](../../docs/UE/UE57_TECH.md).

## Maintenance

- To refresh rules from DevEnvTemplate: copy `DevEnvTemplate/.cursor/rules/*.mdc` to `.cursor/rules/` (preserve `unreal-*.mdc`).
- See [docs/Setup/CURSOR_DEV.md](../../docs/Setup/CURSOR_DEV.md) and [DevEnvTemplate/BOOTSTRAP.md](../DevEnvTemplate/BOOTSTRAP.md) for setup and usage.
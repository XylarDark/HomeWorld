# Cursor Rules Directory

This directory contains Cursor rules for the HomeWorld project. It includes technology-agnostic rules from [DevEnvTemplate](../DevEnvTemplate) and HomeWorld-specific Unreal rules.

## Structure

### Always-Applied Rules (Core, from DevEnvTemplate)

- **00-core-principles.mdc** - Reasoning transparency, professional communication, pre-flight checklist
- **01-code-quality.mdc** - Code organization, design principles, performance awareness
- **02-security.mdc** - OWASP Top 10, secrets management, security checklist
- **03-testing.mdc** - Testing philosophy, test pyramid, test structure
- **04-git-workflow.mdc** - Commit messages, branch naming, git best practices
- **05-error-handling.mdc** - Defensive programming, error patterns, edge cases
- **06-documentation.mdc** - Code comments, API docs, documentation standards
- **07-ai-agent-behavior.mdc** - Meta-rules for AI agent tool usage and communication
- **08-project-context.mdc** - DevEnvTemplate context (generic); for HomeWorld see [AGENTS.md](../../AGENTS.md) and `docs/`
- **16-feature-debug-instrumentation.mdc** - Debug instrumentation policy for new features
- **17-plan-first.mdc** - Plan before code for complex/multi-file work; see [docs/SPEC_AND_PLAN.md](../../docs/SPEC_AND_PLAN.md)
- **19-docs-directory-structure.mdc** - Place new docs in correct docs/ subdir per [docs/DOCS_LAYOUT.md](../../docs/DOCS_LAYOUT.md); keep docs organized.

### Stack-Specific Rules (Conditional, from DevEnvTemplate)

- **10-typescript.mdc**, **11-javascript.mdc**, **12-python.mdc**, **13-markdown.mdc**, **14-json-yaml.mdc**, **15-shell-scripts.mdc**, **20-frontend-frameworks.mdc** - Apply when editing matching file types.

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

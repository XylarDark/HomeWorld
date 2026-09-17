# Docs/11b — HR-B Harness Tighten Handoff

| Field | Value |
|-------|-------|
| **Status** | **COMPLETE — awaiting Lead `APPROVE HR-B`** |
| **Date** | 2026-09-17 |
| **Author** | Cloud Agent (HR-B) |
| **Baseline** | [11a_HR_MEASURES.md](11a_HR_MEASURES.md) |
| **Plan** | [11_SWARM_HARNESS_REFINE.md](11_SWARM_HARNESS_REFINE.md) § HR-B |

---

## Gate

Lead: type **`APPROVE HR-B`** to unlock HR-C (swarm ops refine).

---

## Checklist — what changed

| # | Deliverable | Status | Paths |
|---|-------------|--------|-------|
| 1 | DevEnvTemplate accepted pin + init runbook | Done | [docs/Setup/CURSOR_DEV.md](../docs/Setup/CURSOR_DEV.md) — SHA `213673f`, submodule init, Node 22 EBADENGINE accepted; bump deferred |
| 2 | Safe-Build → Editor → MCP single path | Done | [AGENTS.md](../AGENTS.md), [09-mcp-workflow.mdc](../.cursor/rules/09-mcp-workflow.mdc), [08-project-context.mdc](../.cursor/rules/08-project-context.mdc) |
| 3 | CI policy + SH-01 validate fix | Done | [validate.yml](../.github/workflows/validate.yml), [docs/Setup/CI_POLICY.md](../docs/Setup/CI_POLICY.md), [docs/DOCS_LAYOUT.md](../docs/DOCS_LAYOUT.md) |
| 4 | Rules slimming (non-destructive globs) | Done | 5 rules glob-scoped — see table below |
| 5 | Windows bridge runbook | Done | [docs/Setup/WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md) |
| 6 | HR-A measures + stamps | Done | [11a_HR_MEASURES.md](11a_HR_MEASURES.md), [11_SWARM_HARNESS_REFINE.md](11_SWARM_HARNESS_REFINE.md) |

**Not in scope (HR-B):** Submodule bump, gameplay C++, `.uasset` commits, mass rule delete, V3–V8.

---

## Rules count — before / after

| Metric | Before HR-B | After HR-B |
|--------|-------------|------------|
| Total `.cursor/rules/*.mdc` | 34 | 34 |
| `alwaysApply: true` | **20** | **15** |
| Glob-scoped (HR-B additions) | 12 | **17** |

### Glob-scoped in HR-B (was always-on)

| Rule | New globs |
|------|-----------|
| `ue57-editor-ui.mdc` | `**/*.uproject, **/Source/**, **/Content/**, **/Config/**, **/Plugins/**` |
| `ue57-sources.mdc` | same |
| `18-game-development-principles.mdc` | `**/Content/**, **/Maps/**, **/Lib/**, **/*.uasset, **/*.umap` |
| `09-mcp-workflow.mdc` | `**/Content/Python/**, **/Source/**, **/*.uproject, **/Tools/**` |
| `automation-standards.mdc` | `**/Content/Python/**, **/Tools/**, **/.github/workflows/**` |

### Deferred HR-B2 (left `alwaysApply: true`)

| Rule | Reason |
|------|--------|
| `07-ai-agent-behavior.mdc` | Session continuity, automation alerts — applies to all work |
| `08-project-context.mdc` | Project-wide onboarding context |
| `16-feature-debug-instrumentation.mdc` | All new features, any path |
| `20-full-automation-no-manual-steps.mdc` | Policy applies beyond UE paths |
| `19-docs-directory-structure.mdc` | All doc generation |
| `03-testing.mdc`, `01-code-quality.mdc`, etc. | General engineering standards |

---

## CI validate — path alignment (SH-01 fix)

| Before (stub / quarantine) | After (canonical) |
|----------------------------|-------------------|
| `docs/workflow/30_DAY_SCHEDULE.md` | `docs/TaskLists/30_DAY_SCHEDULE.md` |
| `docs/workflow/MVP_AND_ROADMAP_STRATEGY.md` | Removed from **required**; stub checked as warning only |
| `docs/tasks/*.md` (4 stubs) | Removed; `docs/TaskLists/README.md` + `DAILY_STATE.md` required |

---

## Verification

- [ ] `validate` job green on PR
- [ ] `python-lint` job green on PR
- [ ] Lead reviews Windows bridge + CI policy for DESKTOP-21CT3H0 workflow

---

## Next (after APPROVE HR-B)

**HR-C** — PHASE_BOARD post-audit section, handoff templates for cloud PRs, SESSION_LOG hygiene, dual-OS trim per [11_SWARM_HARNESS_REFINE.md](11_SWARM_HARNESS_REFINE.md).

---

*HR-B complete 2026-09-17 — awaiting Lead APPROVE HR-B.*

# Agent skills

Procedural knowledge for AI agents. Each skill's `description` is read on every turn to decide
relevance; the body loads only when that description matches the task.

**Skill load budget (EXIT SKILL_LOAD_BUDGET_V1):** keep the discoverable set small. Extras and A–E full are **cite / copy-in only** — never paste skill bodies into `AGENTS.md`. Do not copy `architecture-trade-offs-design-depth` onto a Cursor scan path (`.agents/skills/` or `.cursor/skills/`). Do not load lean A/B together with full A–E.

## Discoverable (Cursor scan paths)

### Core + HW-local (`.agents/skills/`)

Default DET adopters copy the **six** core skills. HomeWorld also keeps small HW-local skills in this tree (discoverable).

| Skill | Trigger |
| ----- | ------- |
| [agent-workflow](skills/agent-workflow/SKILL.md) | PowerShell or npm pattern, research-before-implement, KNOWN_ERRORS, or temp-file cleanup |
| [multi-agent-collaboration](skills/multi-agent-collaboration/SKILL.md) | More than one agent or person in the same tree |
| [plan-first](skills/plan-first/SKILL.md) | The user asked to save a plan |
| [secure-coding](skills/secure-coding/SKILL.md) | Input, secrets, auth, or dependencies |
| [token-efficient-context](skills/token-efficient-context/SKILL.md) | Tokens, credits, context cost, MCP, or editing rules/skills/AGENTS.md |
| [verification-evidence](skills/verification-evidence/SKILL.md) | Audits, health checks, guard tests, CI gates |
| [steer-gate](skills/steer-gate/SKILL.md) | HW-local: a steer, taste, or test call is missing before an edit that sets feel/scope/done |
| [swarm-mode-routing](skills/swarm-mode-routing/SKILL.md) | HW-local: first-hop swarm / NON-SWARM mode detect |
| [taste-gate](skills/taste-gate/SKILL.md) | HW-local: lookdev / “does this feel right” (single discoverable home) |
| [taste-profiler](skills/taste-profiler/SKILL.md) | HW-local: twin of taste-gate |

`integrateCursorRules` copies core skills into a host's `.agents/skills/` automatically.

### One catalog

Skill bodies live in `.agents/skills/` only. `.cursor/skills/` keeps a README and no `SKILL.md`, so Cursor does not advertise the same name twice. The `source-command-*` migrated skills and the retired `ue57-api-check` were dropped on 2026-10-20: the six commands live in `.cursor/commands/` and the opencode.json command templates, and the engine lock is UE 5.8. `ue58-api-check` stays callable. Do not add a second copy under `.cursor/skills/`.

## Extras live in the UserHarness template

> Lean extras `architecture-tradeoffs` and `design-complexity` are **subsets of** `architecture-trade-offs-design-depth` (A–E). Do not load a lean skill together with full A–E.

Optional skills for hosts that want deeper coverage have **one** copy, in the
template of record: `UserHarness/.agents/skills-extras/` (writer: `architecture-trade-offs-design-depth`,
see its `SYNC.md`). The project tree does not carry a second vendored copy —
`AGENTS.md` names `UserHarness/` as the doctor root and forbids vendoring a
second one. They are **not** copied by default and are **not** loaded until you opt
in, keeping the dormant-skill surface small. Path is `skills-extras` (not an official
Cursor skills scan dir).

| Skill | Trigger |
| ----- | ------- |
| [architecture-trade-offs-design-depth](../UserHarness/.agents/skills-extras/architecture-trade-offs-design-depth/SKILL.md) | Boundaries, module APIs, data/replication, team ownership, integration (Layers A–E). **Cite-only in seats. Never discoverable.** |
| [architecture-tradeoffs](../UserHarness/.agents/skills-extras/architecture-tradeoffs/SKILL.md) | Lean A-only subset of A–E — do not load with full A–E |
| [design-complexity](../UserHarness/.agents/skills-extras/design-complexity/SKILL.md) | Lean B-only subset of A–E — do not load with full A–E |
| [automation-standards](../UserHarness/.agents/skills-extras/automation-standards/SKILL.md) | Automation driving external tools, APIs, or CI |
| [code-structure](../UserHarness/.agents/skills-extras/code-structure/SKILL.md) | Modules, naming, file layout, performance budgets |
| [data-pipeline-safety](../UserHarness/.agents/skills-extras/data-pipeline-safety/SKILL.md) | Author-owned databases, CMS, infra state, binaries |
| [debug-instrumentation](../UserHarness/.agents/skills-extras/debug-instrumentation/SKILL.md) | New features, scripts, or APIs needing trace logs |
| [defensive-programming](../UserHarness/.agents/skills-extras/defensive-programming/SKILL.md) | External input, I/O, network, async concurrency |
| [documentation](../UserHarness/.agents/skills-extras/documentation/SKILL.md) | Comments, README, or anything under `docs/` |
| [exclusive-resource-access](../UserHarness/.agents/skills-extras/exclusive-resource-access/SKILL.md) | Browsers, ports, devices, or other single-user resources |
| [scope-refinement](../UserHarness/.agents/skills-extras/scope-refinement/SKILL.md) | Ask (2 questions max) before guessing a product, scope, or architecture call |
| [testing-standards](../UserHarness/.agents/skills-extras/testing-standards/SKILL.md) | Adding or updating tests or test frameworks |

### Opt in to extras

Copy the skills you need from the template into the host's active skills directory:

```bash
# From the repo root (UserHarness is the template of record)
cp -r UserHarness/.agents/skills-extras/testing-standards .agents/skills/
```

## Authoring

Keep `SKILL.md` short: only what the model does not already know. Extra files in the
skill folder load on demand.

- **`description`:** one sentence. Third-person *capability*, then this repo's
  `Use when …` trigger (Cursor matching). Do not lecture in the description; it is
  always-on.
- **Degrees of freedom:** high when the task is judgment (reviews); low when the
  agent must run exactly one script. Match shaping vs settled in `AGENTS.md`:
  shaping = higher freedom; settled work and migrations = lower.
- **Attach only what the task needs.** Core vs extras already splits the dormant
  surface; do not add a seventh core skill for a niche procedure.

Do not rewrite every existing description to match this. New skills follow it.

## Portability

Skills copied into host projects travel verbatim. Sections marked **Localize on copy** describe
this template's commands and layout — rewrite those for your project. `tests/unit/skill-portability.test.js`
enforces this rule on core skills (the default copied set).

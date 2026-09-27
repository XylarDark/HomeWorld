# Agent skills

Procedural knowledge for AI agents. Each skill's `description` is read on every turn to decide
relevance; the body loads only when that description matches the task.

**Skill load budget (EXIT SKILL_LOAD_BUDGET_V1):** keep the discoverable set small. Extras and A–E full are **cite / copy-in only** — never paste skill bodies into `AGENTS.md`. Do not copy `architecture-trade-offs-design-depth` onto a Cursor scan path (`.agents/skills/` or `.cursor/skills/`). Do not load lean A/B together with full A–E.

## Discoverable (Cursor scan paths)

### Core + HW-local (`.agents/skills/`)

Default DET adopters copy the **six** core skills. HomeWorld also keeps small HW-local skills in this tree (discoverable).

| Skill | Trigger |
| ----- | ------- |
| [agent-workflow](skills/agent-workflow/SKILL.md) | Any end-to-end coding task in the repo |
| [multi-agent-collaboration](skills/multi-agent-collaboration/SKILL.md) | More than one agent or person in the same tree |
| [plan-first](skills/plan-first/SKILL.md) | Multi-file or architectural work |
| [secure-coding](skills/secure-coding/SKILL.md) | Input, secrets, auth, or dependencies |
| [token-efficient-context](skills/token-efficient-context/SKILL.md) | Planning multi-file work, agent runs, tokens, MCP, or editing rules/skills/AGENTS.md |
| [verification-evidence](skills/verification-evidence/SKILL.md) | Audits, health checks, guard tests, CI gates |
| [swarm-mode-routing](skills/swarm-mode-routing/SKILL.md) | HW-local: first-hop swarm / NON-SWARM mode detect |
| [taste-gate](skills/taste-gate/SKILL.md) | HW-local: lookdev / “does this feel right” (single discoverable home) |
| [taste-profiler](skills/taste-profiler/SKILL.md) | HW-local: twin of taste-gate |

`integrateCursorRules` copies core skills into a host's `.agents/skills/` automatically.

### Live `.cursor/skills/` (see also that README)

Only these live project skills stay on the cursor scan path after the budget Do:

- `pcg-validate`
- `ue58-api-check`
- `automation-gap-solutions`
- Tombstones (if present): `ue57-api-check`, `demo-map-setup`, `homestead-setup` — WAVE F / historical; not live workflows

Lean A/B and taste twins are **not** duplicated under `.cursor/skills/` (retired).

## Extras (`.agents/skills-extras/`)

> Lean extras `architecture-tradeoffs` and `design-complexity` are **subsets of** `architecture-trade-offs-design-depth` (A–E). Do not load a lean skill together with full A–E.

Optional skills for hosts that want deeper coverage. They are **not** copied by default and are
**not** loaded until you opt in — keeping the dormant-skill surface small. Path is `skills-extras` (not an official Cursor skills scan dir).

| Skill | Trigger |
| ----- | ------- |
| [architecture-trade-offs-design-depth](skills-extras/architecture-trade-offs-design-depth/SKILL.md) | Boundaries, module APIs, data/replication, team ownership, integration (Layers A–E; sync [SYNC.md](skills-extras/architecture-trade-offs-design-depth/SYNC.md)). **Cite-only in seats. Never discoverable.** |
| [architecture-tradeoffs](skills-extras/architecture-tradeoffs/SKILL.md) | Lean A-only subset of A–E — do not load with full A–E |
| [design-complexity](skills-extras/design-complexity/SKILL.md) | Lean B-only subset of A–E — do not load with full A–E |
| [automation-standards](skills-extras/automation-standards/SKILL.md) | Automation driving external tools, APIs, or CI |
| [code-structure](skills-extras/code-structure/SKILL.md) | Modules, naming, file layout, performance budgets |
| [data-pipeline-safety](skills-extras/data-pipeline-safety/SKILL.md) | Author-owned databases, CMS, infra state, binaries |
| [debug-instrumentation](skills-extras/debug-instrumentation/SKILL.md) | New features, scripts, or APIs needing trace logs |
| [defensive-programming](skills-extras/defensive-programming/SKILL.md) | External input, I/O, network, async concurrency |
| [documentation](skills-extras/documentation/SKILL.md) | Comments, README, or anything under `docs/` |
| [exclusive-resource-access](skills-extras/exclusive-resource-access/SKILL.md) | Browsers, ports, devices, or other single-user resources |
| [testing-standards](skills-extras/testing-standards/SKILL.md) | Adding or updating tests or test frameworks |
| [taste-gate](skills-extras/taste-gate/SKILL.md) | Pointer → `.agents/skills/taste-gate` (no second body) |
| [taste-profiler](skills-extras/taste-profiler/SKILL.md) | Pointer → `.agents/skills/taste-profiler` |

### Opt in to extras

Copy the skills you need into the host's active skills directory:

```bash
# From the template root (or `.devenv/` when vendored)
cp -r .agents/skills-extras/testing-standards .agents/skills/
```

**Never** copy `architecture-trade-offs-design-depth` into `.agents/skills/` or `.cursor/skills/` on HomeWorld — seats cite; dual-source writer stays DET extras.

Or copy selected extras (avoid wholesale `cp -r .agents/skills-extras/*` on HomeWorld — that would put A–E on a scan path).

When running the doctor's agent-layer integration with extras:

```bash
npm run doctor:fix
# The integration API accepts includeSkillExtras: true when called programmatically.
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

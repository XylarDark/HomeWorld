# Taste Profiler

Durable Lead/process taste that **Taste Gates read first**, then stage and promote — never invent, never auto-consolidate.

**Track:** [Docs/29_TASTE_PROFILER.md](../../Docs/29_TASTE_PROFILER.md)  
**Durable store:** [taste-profile.md](taste-profile.md)  
**Skill:** [.cursor/skills/taste-profiler/SKILL.md](../../.cursor/skills/taste-profiler/SKILL.md)  
**Gates:** [taste-gates.md](taste-gates.md) · [OWNERSHIP.md](OWNERSHIP.md)

## How it fits

| Piece | Job |
|-------|-----|
| **taste-profile.md** | Versioned summary (canon pointers, prefs, locked decisions, gaps, do-not) |
| **Saved/taste_profile_session.json** | Staged candidates (gitignored) until Lead confirms |
| **taste-gate** | On limit: read profile → if covered, continue; else alert + queue + stage |
| **taste-profiler** | Bootstrap interview, stage, promote, refuse invent |

**Precedence:** latest Lead chat / `APPROVE *` > durable profile > never invent.

## What you do

1. Answer Taste Gate or profiler questions (max 2/turn).
2. Confirm promote (“promote”, pick option, or `APPROVE *`) so the agent updates `taste-profile.md`.
3. Reject staged candidates that should not become durable.

## Scope (since 2026-10-01)

This profile holds **art and mechanic taste, plus process prefs**. It does not hold
engineering decisions — architecture, module boundaries, code design and harness
refactoring are agent-owned and are recorded in
[AGENT_DECISIONS.md](../decisions/AGENT_DECISIONS.md) instead.

Promotion stays Lead-gated, but only because the *content* is taste. A harness or
architecture call must never be staged here as a way to get a human stamp on an
agent-owned decision; that is the route this reset closed.

## What the agent must not do

- Rewrite the durable profile without your confirm
- Stage an architecture, code-design or refactor decision here
- Treat Cursor Memories as team taste canon
- Duplicate the art bible palette into the profile
- Invent the next **product** track because the profile is thin

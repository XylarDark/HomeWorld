# Taste Gates

Continuous development: the agent is always either doing **executable work** or holding a **structured taste ask**—never inventing feel, never idle with no next question.

**Track:** [Docs/28_TASTE_GATES.md](../../Docs/28_TASTE_GATES.md)  
**Skill:** [.cursor/skills/taste-gate/SKILL.md](../../.cursor/skills/taste-gate/SKILL.md)  
**Profile (read first):** [taste-profile.md](taste-profile.md) · [taste-profiler.md](taste-profiler.md)  
**Alert shape:** [OWNERSHIP.md](OWNERSHIP.md) · detectors: [CYCLE.md](CYCLE.md)

## Scope: what is still a taste limit

As of **2026-10-01** a taste limit is **art design or game mechanic design**, and
nothing else:

| Still a Taste Gate (human) | No longer a Taste Gate (agent decides + logs) |
| -------------------------- | -------------------------------------------- |
| Art bible, palette, tone, "is this the product" | Architecture, module boundaries, directory map |
| Shot list, framing, still accept/reject | New shared util, new skill, `.cursor/mcp.json` entry |
| Beat, inventory, mechanic design | Which metric to optimize, which variant won |
| Product vision and feel targets | Harness refactoring — rules, skills, scripts, scorers |
| Reopening a **feel** target on a CLOSED track | Which harness Docs track comes next |

A harness or engineering fork is **not** a taste fork. It gets a decision-log
entry ([AGENT_DECISIONS.md](../decisions/AGENT_DECISIONS.md)), not a gate. The
failure mode to avoid is holding an architecture question open as "taste" because
it feels consequential.

## How this relates to steer / taste / test

| Job | Taste Gate role |
|-----|-----------------|
| **Taste** | Primary — art feel and mechanic design: art bible, palette, tone, shots, still verdicts, beat canon |
| **Steer** | Isolation, web reach, permissions only. Use the OWNERSHIP alert; it needs no Docs/28 queue |
| **Test** | Rubric / ship gates stay Test; do not launder Test as Taste |

Docs/26 Night Feel interview was a **manual** precursor. Taste Gates make that pattern reusable: detect → queue → ask (max 2 Q/turn) → scribe → resume.

## What you see

1. An OWNERSHIP alert with Job **taste** and numbered options.
2. A handoff under `Docs/handoffs/TASTE_GATE_*.md`.
3. Optional `Saved/taste_gates_pending.json` (gitignored) listing open gates.

Answer in chat (pick options), or use Lead phrases when the gate is a Docs track phase (`APPROVE *`). The agent scribes and continues.

## What the agent must not do

- Invent the decision to keep moving
- Open a new **product** track while PHASE_BOARD says next TBD without a gate — a *harness* track needs no gate
- Auto-approve taste or resurrect WAVE F agent loops
- Raise a Taste Gate for architecture, code design, or a refactor, to get a decision it could have made itself

## Docs tracks

Taste Gates can be their own Docs track phases (prefix **TG**) or fire mid-phase inside another track. Closing Docs/28 proves the harness; later tracks reuse the skill without reopening 28.

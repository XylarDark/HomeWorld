# Taste Gates

Continuous development: the agent is always either doing **executable work** or holding a **structured taste ask**—never inventing feel, never idle with no next question.

**Track:** [Docs/28_TASTE_GATES.md](../../Docs/28_TASTE_GATES.md)  
**Skill:** [.cursor/skills/taste-gate/SKILL.md](../../.cursor/skills/taste-gate/SKILL.md)  
**Profile (read first):** [taste-profile.md](taste-profile.md) · [taste-profiler.md](taste-profiler.md)  
**Alert shape:** [OWNERSHIP.md](OWNERSHIP.md) · detectors: [CYCLE.md](CYCLE.md)

## How this relates to steer / taste / test

| Job | Taste Gate role |
|-----|-----------------|
| **Taste** | Primary — purpose, vision, map, patterns, “is this the product,” AD feel |
| **Steer** | Only if the fork is harness/skill/MCP allowlist (still use OWNERSHIP alert; may not need Docs/28 queue) |
| **Test** | Rubric / ship gates stay Test; do not launder Test as Taste |

Docs/26 Night Feel interview was a **manual** precursor. Taste Gates make that pattern reusable: detect → queue → ask (max 2 Q/turn) → scribe → resume.

## What you see

1. An OWNERSHIP alert with Job **taste** and numbered options.
2. A handoff under `Docs/handoffs/TASTE_GATE_*.md`.
3. Optional `Saved/taste_gates_pending.json` (gitignored) listing open gates.

Answer in chat (pick options), or use Lead phrases when the gate is a Docs track phase (`APPROVE *`). The agent scribes and continues.

## What the agent must not do

- Invent the decision to keep moving
- Open a new product track while PHASE_BOARD says next TBD without a gate
- Auto-approve taste or resurrect WAVE F agent loops

## Docs tracks

Taste Gates can be their own Docs track phases (prefix **TG**) or fire mid-phase inside another track. Closing Docs/28 proves the harness; later tracks reuse the skill without reopening 28.

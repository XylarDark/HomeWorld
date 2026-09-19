# Swarm routing research (studio + model)

**Date:** 2026-09-19  
**Purpose:** Ground [SWARM_MODE_ROUTING.md](../human-use/SWARM_MODE_ROUTING.md) in major AI-dev-studio patterns and open-web model×task guidance. Re-check model matrix **quarterly** — benchmarks move.

**Related:** skill `swarm-mode-routing` · [token-efficient-context](../../.agents/skills/token-efficient-context/SKILL.md)

---

## Studio comparison → HomeWorld mapping

| Studio | Mechanism | Token lesson | HomeWorld mapping |
|--------|-----------|--------------|-------------------|
| [Cursor Skills](https://cursor.com/docs/skills.md) / [Rules](https://cursor.com/docs/rules) / [Subagents](https://cursor.com/docs/subagents.md) | Skills = on-demand body; rules = short always-on; subagents = isolated context + cheaper explore model | Do not put procedures in always-on AGENTS; isolate parallel work | `.agents/skills/*`; thin AGENTS; Task/subagents for explore |
| [Claude Code best practices](https://code.claude.com/docs/en/best-practices.md) / [skills](https://code.claude.com/docs/en/skills) | Short always-on facts; skills for workflows; description drives auto-invoke | Progressive disclosure (metadata always, body on trigger) | AGENTS facts only; `swarm-mode-routing` description triggers |
| [OpenAI Codex customization](https://developers.openai.com/codex/concepts/customization) / [subagents](https://developers.openai.com/codex/subagents) | AGENTS.md + skills + subagents + per-agent `model` | Same three-layer stack | Conductor parent + `.cursor/agents/*` role cards |
| [Copilot custom agents](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/custom-agents) / [Fleet](https://github.com/github/copilot-sdk/blob/main/docs/features/fleet-mode.md) | `infer` + `description` for auto-delegate; per-agent model; parallel fleet + shared todos | Parent keeps context clean; workers own one todo | Skill `infer`-like description; PHASE_BOARD fan-out |
| [Devin Desktop / Cascade rules](https://docs.devin.ai/desktop/cascade/memories) | `always_on` / `model_decision` / `glob` / `manual` | Prefer description-triggered over always-on | No new `alwaysApply` routing rule; skill = model_decision |
| [Aider architect/editor](https://aider.chat/docs/usage/modes.html) | Plan model ≠ edit model | Two-stage = better quality, more cost | Plan Mid/Frontier → implement Auto/Composer |
| [Continue model roles](https://docs.continue.dev/reference) | chat / edit / apply roles | Route by job, not one model for all | Task classes in SWARM_MODE_ROUTING |

---

## Model × task matrix (advice only — 2026-09)

Do **not** hard-pin vendor model IDs in CI. Cursor **Auto** remains the default for routine NON-SWARM work. Prefer **model class**: Auto | Mid | Frontier | Explore.

| Task class | Preferred class | Rationale (dated) |
|------------|-----------------|-------------------|
| Routine edits, boilerplate, Tab, bulk | **Auto** / Composer | Cheap high-volume; Flash-class workhorses |
| Mid planning, most C++/Python implement | **Mid** (Sonnet-class) | Default implement lane |
| Hard multi-file / architecture / subtle bugs | **Frontier** (Opus / GPT-5-class) | Stronger SWE / agentic benches; drop after turn |
| Terminal-heavy agent loops | **Mid–Frontier** (Sol-class when available) | Strong Terminal-Bench results in 2026 harnesses |
| Art Director taste / creative prose | **Frontier** | Nuanced judgment / writing quality |
| QA judge (independent verify) | **Mid–Frontier** | Independent of builder chat; accuracy over speed |
| Conductor orchestration | **Mid** (Frontier only for hard gate synthesis) | Coordination, not hero coding |
| Explore / parallel codebase search | **Explore** (fast/cheap subagent) | Cursor explore pattern — isolate tokens |

Sources (non-exhaustive): [Terminal-Bench 2.1](https://vals.ai/benchmarks/terminal-bench-2-1), [model routing roundups](https://andrew.ooo/answers/claude-opus-5-vs-gpt-5-6-sol-vs-gemini-3-6-flash-2026/), [Cursor subagents](https://cursor.com/docs/subagents.md) (cost isolation).

---

## Progressive disclosure (locked for HomeWorld)

1. **Always-on:** short facts in `AGENTS.md` + critical always-applied rules already in repo — do not add routing as `alwaysApply: true`.
2. **On invoke:** skill bodies (`swarm-mode-routing`, domain skills).
3. **On spawn:** one specialist role card + wave packet paths only ([SWARM_OPS](../../swarm/SWARM_OPS.md) thin context).
4. **Never:** dump full MVP brief or all `.cursor/agents/*` into a NON-SWARM engineering chat.

---

## Research gaps

- `parallel-cli` billing blocked deeper Parallel search on 2026-09-19; refresh with `/parallel-research` when credits available.
- Vendor model names change; update this file’s matrix, not hard-coded agent pins.

# Docs/28 — Taste Gates (TG)

| Field | Value |
|-------|-------|
| **Status** | **CLOSED / COMPLETE** — Lead **`APPROVE TG-E`**, 2026-09-19 ET |
| **Date** | 2026-09-19 |
| **Author** | Conductor (HomeWorld) |
| **Unlocked by** | Lead “start Taste Gates research” + implement-plan, 2026-09-19 ET |
| **Prefix** | **TG** |
| **Mode** | NON-SWARM (harness) |
| **Prior** | Docs/27 **CLOSED**; Docs/26 taste interview = manual precursor |

---

## Problem

Agents should stop on taste forks ([OWNERSHIP.md](../docs/human-use/OWNERSHIP.md)), but the harness did not **detect, queue, or resume** when they hit a limit. Continuous development needs: always either executable work **or** a structured human taste query—never silent invention, never idle with no next ask.

## Vision

**Taste Gates** — when the agent would invent feel/purpose/shape/product direction, it fires a gate: OWNERSHIP alert → durable handoff → pending queue → stop → human answers → scribe → resume agent work.

---

## TG-A — Research digest

### Repo map (HomeWorld)

| Surface | Role today | Gap |
|---------|------------|-----|
| [OWNERSHIP.md](../docs/human-use/OWNERSHIP.md) | Alert shape; taste job definition | No queue / resume / skill |
| [CYCLE.md](../docs/human-use/CYCLE.md) | Detectors (vision/map/patterns → human) | Soft agent judgment only |
| [architecture.md](../docs/human-use/architecture.md) | Taste options 1–5 | Not wired to track phases |
| [Docs/26_TASTE_NEXT.md](26_TASTE_NEXT.md) | Manual multi-round taste interview | One-off; not reusable gate template |
| [PHASE_BOARD.md](../swarm/PHASE_BOARD.md) | `APPROVE *` track gates | No “taste pending” row type |
| [SWARM_MODE_ROUTING.md](../docs/human-use/SWARM_MODE_ROUTING.md) | AD taste → separate chat | No machine pending file |
| Docs/27 Night Feel | Product phases after taste locked | Shows need for continuous next-ask |

### External patterns (2024–2026)

| Source | Finding for HomeWorld |
|--------|------------------------|
| [LangGraph `interrupt`](https://www.langchain.com/blog/making-it-easier-to-build-human-in-the-loop-agents-with-interrupt) | Pause mid-run; persist payload; resume later on another machine — maps to **queue + stop + scribe** |
| [OpenAI Agents SDK HITL](https://openai.github.io/openai-agents-python/human_in_the_loop/) | Interruptions list; serialize state; approve/reject then resume — maps to **pending JSON + Lead APPROVE** |
| [PAHF / personalized agents](https://personalized-ai.github.io/) | Pre-action clarification + memory + post-action feedback — maps to **max 2 Q/turn before inventing** |
| Pref-GUIDE / preference RL papers | Offline preference learning — **defer** (do not train policies from Lead chat) |
| ResearStudio (EMNLP 2025) | Pause/resume + human edit workspace — inspirational only; do not add new orchestration servers |

**Note:** `/parallel-research` not run this session (WebSearch digest used). Lead may paste a deeper report later into § Research addendum.

### Taste-limit heuristics (checkable)

Fire a Taste Gate when **any** is true and undecided **for this task**:

1. Would change product vision, GDD fantasy, art bible tone, or shot list (e.g. sixth shot).
2. Would pick next Docs track / surface feel without Lead or Docs/26-style interview.
3. Would invent architecture purpose / directory map ([architecture.md](../docs/human-use/architecture.md) still `(fill in)` for this task).
4. Would assign AD reject/approve on stills without AD or Lead waive.
5. Would reopen a CLOSED track’s feel targets.
6. PHASE_BOARD says next track TBD and agent would start product work anyway.

**Do not fire** for: typo/one-line; flesh-out of already-decided taste; implement after Lead `APPROVE` unlock.

---

## TG-B — Strategy matrix

| Item | Verdict | Notes |
|------|---------|-------|
| Taste Gate = first-class Docs track phase type | **Adopt** | Prefix **TG**; handoffs `TASTE_GATE_*` |
| Queue `Saved/taste_gates_pending.json` (gitignored) + durable `Docs/handoffs/TASTE_GATE_*.md` | **Adopt** | Saved/ already gitignored |
| Cursor skill `taste-gate` | **Adopt** | detect → alert → queue → stop → scribe after answer |
| Thin always-on rule pointer | **Adopt** | Point at skill + OWNERSHIP; no seventh cursor-cannot product |
| Docs/26-style gate template (max 2 Q/turn) | **Adopt** | In skill + taste-gates.md |
| Auto-run agent loop / Start-AllAgents | **Reject** | WAVE F quarantine |
| Preference-model / RL from Lead chat | **Reject** | Out of scope |
| DevHarness upstream PR same week | **Defer** | HomeWorld prove first; sync later |

**Strategy stamp:** Unlocked via Lead implement-plan 2026-09-19 ET (equivalent **`APPROVE TG STRATEGY`** for this track). Formal phrase still valid for future amendments: Lead **`APPROVE TG STRATEGY`**.

---

## Phases

| Phase | Focus | Status | Gate |
|-------|--------|--------|------|
| **TG-A** | Research digest | **DONE** | This doc |
| **TG-B** | Strategy matrix | **DONE** | Implement-plan unlock |
| **TG-C** | Skill + human-use page + rule pointer | **DONE** | See spike paths below |
| **TG-D** | Dry-run prove | **DONE** | Lead **`APPROVE TG-D`**, 2026-09-19 ET |
| **TG-E** | Close Docs/28 | **DONE** | Lead **`APPROVE TG-E`**, 2026-09-19 ET |

### Spike paths (TG-C)

- Skill: [.cursor/skills/taste-gate/SKILL.md](../.cursor/skills/taste-gate/SKILL.md)
- Human-use: [docs/human-use/taste-gates.md](../docs/human-use/taste-gates.md)
- Rule pointer: [.cursor/rules/07-ai-agent-behavior.mdc](../.cursor/rules/07-ai-agent-behavior.mdc) (Taste Gates checklist item)
- Prove handoff: [Docs/handoffs/TG_D_PROVE.md](handoffs/TG_D_PROVE.md)

---

## Non-goals

Auto-approve taste; invent feel; resurrect Start-AllAgents; dual MCP; UE lookdev in this track.

## Lead gates

| Phrase | Effect |
|--------|--------|
| **`APPROVE TG STRATEGY`** | Confirm/amend matrix (already unlocked via implement-plan) |
| **`APPROVE TG-D`** | Accept prove evidence — **DONE** 2026-09-19 ET |
| **`APPROVE TG-E`** | Close Docs/28 — **DONE** 2026-09-19 ET |

Harness remains in force after close: skill `taste-gate` (`.cursor/skills/` + `.agents/skills/`) + [taste-gates.md](../docs/human-use/taste-gates.md). Upstream: DevHarness (DevEnvTemplate) `.agents/skills-extras/taste-gate`. Next product Docs track is Lead-named or a fresh Taste Gate — do not invent.

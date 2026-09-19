# Docs/29 — Taste Profiler (TP)

| Field | Value |
|-------|-------|
| **Status** | **CLOSED / COMPLETE** — Lead **`APPROVE TP-E`**, 2026-09-19 ET |
| **Date** | 2026-09-19 |
| **Author** | Conductor (HomeWorld) |
| **Unlocked by** | Lead implement-plan for Taste Profiler, 2026-09-19 ET |
| **Prefix** | **TP** |
| **Mode** | NON-SWARM (harness) |
| **Prior** | Docs/28 Taste Gates **CLOSED**; Docs/26 interview = bootstrap seed |

---

## Problem

Taste Gates stop invention ([Docs/28](28_TASTE_GATES.md)) but agents lack a **durable, evolving** summary of Lead taste and locked decisions. Continuous development needs: read profile → work or gate → stage candidates → Lead promotes → resume.

## Vision

**Taste Profiler** — reviewed markdown profile + session candidates. Taste Gates **read the profile first**. Updates promote only after Lead/AD confirm or `APPROVE *`. Never invent; never auto-consolidate.

**Precedence:** latest Lead chat / `APPROVE *` > durable profile > never invent.

---

## TP-A — Research digest

### Repo map

| Surface | Role | Gap vs profiler |
|---------|------|-----------------|
| Docs/00–02 canon / art bible | Product taste | Locked; not rolling Lead prefs |
| Docs/26 interview | One-shot scope | Closed; not reusable profile |
| Docs/28 Taste Gates | Detect → queue → stop | No durable preference store |
| OWNERSHIP / CYCLE / architecture.md | Per-task taste jobs | Not cross-session profile |
| references/ | Golden snippets | Human-seeded exemplars only |
| PHASE_BOARD / SESSION_SUMMARY | Episodic decisions | Narrative, not structured profile |
| Cursor Memories / user rules | Personal editor prefs | Not team-reviewed product/process taste |

### External borrow (already collected)

| Source | Borrow |
|--------|--------|
| [LangMem user profiles](https://langchain-ai.github.io/langmem/guides/manage_user_profile/) | Small structured schema; update-in-place |
| [OpenAI context personalization](https://developers.openai.com/cookbook/examples/agents_sdk/context_personalization) | Session notes → promote → global; precedence |
| [LangGraph Store](https://docs.langchain.com/oss/python/langgraph/stores) | Cross-thread prefs (we use git markdown + Saved JSON) |
| [Cursor Rules docs](https://cursor.com/docs/rules) | Versioned team files over Memories for standards |

**Reject:** preference RL; auto-promote; Memories as canon.

---

## TP-B — Strategy matrix

| Item | Verdict |
|------|---------|
| Docs track prefix **TP** | **Adopt** |
| Durable `docs/human-use/taste-profile.md` | **Adopt** |
| Session `Saved/taste_profile_session.json` | **Adopt** |
| Skill `taste-profiler` + taste-gate read-first | **Adopt** |
| Thin rule checklist pointer | **Adopt** |
| Auto-promote / Memories as canon | **Reject** |
| DevHarness upstream same week | **Defer** until HomeWorld prove |

**Strategy stamp:** Unlocked via Lead implement-plan 2026-09-19 ET (≈ **`APPROVE TP STRATEGY`**).

---

## Phases

| Phase | Focus | Status | Gate |
|-------|--------|--------|------|
| **TP-A** | Research digest | **DONE** | This doc |
| **TP-B** | Strategy matrix | **DONE** | Implement-plan unlock |
| **TP-C** | Profile + skills + pages | **DONE** | Spike paths below |
| **TP-D** | Dry-run prove | **DONE** | Lead **`APPROVE TP-D`**, 2026-09-19 ET |
| **TP-E** | Close Docs/29 | **DONE** | Lead **`APPROVE TP-E`**, 2026-09-19 ET |

### Spike paths (TP-C)

- Profile: [docs/human-use/taste-profile.md](../docs/human-use/taste-profile.md)
- Skill: [.cursor/skills/taste-profiler/SKILL.md](../.cursor/skills/taste-profiler/SKILL.md)
- Gate patch: [.cursor/skills/taste-gate/SKILL.md](../.cursor/skills/taste-gate/SKILL.md)
- Human-use: [docs/human-use/taste-profiler.md](../docs/human-use/taste-profiler.md)
- Prove: [Docs/handoffs/TP_D_PROVE.md](handoffs/TP_D_PROVE.md)

---

## Non-goals

Auto-approve taste; replace art bible; Cursor Memories as truth; WAVE F loops; dual MCP; UE lookdev.

## Lead gates

| Phrase | Effect |
|--------|--------|
| **`APPROVE TP STRATEGY`** | Confirm/amend matrix (unlocked via implement-plan) |
| **`APPROVE TP-D`** | Accept prove evidence — **DONE** 2026-09-19 ET |
| **`APPROVE TP-E`** | Close Docs/29 — **DONE** 2026-09-19 ET |

Profile + skills stay live: [taste-profile.md](../docs/human-use/taste-profile.md), `taste-profiler` / `taste-gate`. DevHarness sync is a separate chore. Next product track: Lead-named or Taste Gate — do not invent.

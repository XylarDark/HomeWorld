# READING_CANON_V1

**Pointers only. Seats do not ingest this file. AGENTS does not copy this file.**

**Status:** ACTIVE (pointer canon)  
**Cite:** EXIT HARNESS_SOURCES_SCOUT_V1 · Lead 2026-09-27 · pin tip context DET `0a27306` / A–E blob `107a5118c95c1bf0b1b3d1755796632bff41b535`  
**Tip context:** HW `main` ≈ `5c9c08b` · ALWAYSAPPLY N=3 locked · no pin bump · no A–E body rewrite

Books and vendor essays join company canon **only as pointer rows**. Prefer this thin HW doc over skill-body or AGENTS growth.

---

## KEEP

A–E five primaries + named tight extracts. Full books stay out of seats. Each A–E row cites skill blob `107a5118c95c1bf0b1b3d1755796632bff41b535`.

| Layer | Source | Role (≤2 lines) | Blob |
|---|---|---|---|
| **A** | Ford et al., *Software Architecture: The Hard Parts* | System trade-offs, quanta, coupling, least-worst decisions. A-primary. | `107a5118c95c1bf0b1b3d1755796632bff41b535` |
| **B** | Ousterhout, *A Philosophy of Software Design* | Deep modules, information hiding, complexity budget for skills/files. B-primary. | `107a5118c95c1bf0b1b3d1755796632bff41b535` |
| **C** | Kleppmann, *Designing Data-Intensive Applications* | Logs, replication, derived state — checkpoint ≠ memory analog. C-primary. | `107a5118c95c1bf0b1b3d1755796632bff41b535` |
| **D** | Skelton/Pais, *Team Topologies* (+ tight DDD extract) | Stream/platform/enabling cuts; seat ownership. Do not expand D. | `107a5118c95c1bf0b1b3d1755796632bff41b535` |
| **E** | Nygard, *Release It!* | Stability patterns, backpressure, bulkheads, blast radius. E-primary. | `107a5118c95c1bf0b1b3d1755796632bff41b535` |
| Extract | Feathers *Working Effectively with Legacy Code* (WELC extract) | Tight extract only. Full book = PARK. | in A–E blob |
| Extract | Khorikov *Unit Testing Principles, Practices, and Patterns* (extract) | Tight extract only. Full book = PARK. | in A–E blob |
| Extract | DDD Evans / Vernon *Implementing DDD* (extract) | Tight extract inside D. Full books = PARK. | in A–E blob |
| Extract | Google *Site Reliability Engineering* (SRE extract) | Tight extract near E. Full SRE + Workbook = PARK. | in A–E blob |

---

## CANDIDATE

Pointer rows only. **Do not load in seats.** Abstracts ≤2 lines. No AGENTS dump.

| # | Source | URL | Abstract (≤2 lines) | Seat rule |
|---|---|---|---|---|
| 1 | Anthropic, “Building Effective Agents” (Schluntz/Zhang) | https://www.anthropic.com/engineering/building-effective-agents | Workflow vs agent; five composable patterns; start simple. Durable vendor pattern note, not a framework. | do not load in seats |
| 2 | Anthropic, “How we built our multi-agent research system” | https://www.anthropic.com/engineering/multi-agent-research-system | Orchestrator–worker case: parallel workers, compressed returns, cost math; not for tightly coupled codegen. **Cluster with #1**; do not seat both full texts. | do not load in seats |
| 3 | Anthropic cookbooks — orchestrator-workers / agent patterns | https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents | Pattern sketches for orchestrator-workers. Cite with #1/#2 cluster; no cookbook paste into skills. | do not load in seats |
| 4 | LangGraph persistence / checkpointer vs store (+ durable execution) | https://docs.langchain.com/oss/javascript/langgraph/persistence · https://docs.langchain.com/oss/javascript/langgraph/durable-execution | State = working set; history = audit/replay; store = cross-thread memory. Persistence ≠ memory. Maps onto C; does not replace C. | do not load in seats |
| 5 | SWE-bench family (Verified / Pro / Rebench / Live) — **measure-only** | https://www.swebench.com | Fitness instrument for harness changes. Do not derive architecture from leaderboards. | do not load in seats |
| 6 | Meadows, *Thinking in Systems* | book pointer (leverage points) | Leverage points / feedback / delays explain alwaysApply growth and AGENTS dump traps. Thin cite only. | do not load in seats |
| 7 | Dibia, *Designing Multi-Agent Systems* (2025) | book pointer | Framework-agnostic multi-agent patterns + eval chapter. Best book-shaped fill of the agent gap; pointer only. | do not load in seats |
| 8 | Cursor Rules + `AGENTS.md` vendor docs | https://cursor.com/docs/rules.md | Rules vs AGENTS vs skills; keep AGENTS thin. Vendor docs only — not tip blogs. | do not load in seats |
| 9 | Optional second-wave: *Software Engineering at Google*; *Observability Engineering* (Majors et al.) | book pointers | Pin discipline / “engineering ≠ programming”; wide events for “what did the worker do.” Still pointer-only; never a sixth layer. | do not load in seats |
| 10 | Game design — movement + env cluster (Swink *Game Feel*; Totten level architecture; Lynch nodes/paths; Level Design Book blockout) | [`GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md`](GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md) | Pointer cluster for T0 glide/weight/path/greybox prove language. Not a sixth A–E layer; seats cite path only. | do not load in seats |
| 11 | Game design — feel / juice cluster (Swink polish leg; Juice It or Lose It; Screenshake; MDA; Schell Feedback; Gabler juicy) | [`GAME_FEEL_CANON_V1.md`](GAME_FEEL_CANON_V1.md) | Pointer cluster for verb confirm / feedback dose / nurture-soothe juice language. Not a sixth A–E layer; weight/glide stay in movement-env canon. | do not load in seats |

---

## PARK / REJECT

- **PARK:** Larson *Staff Engineer*; Fournier *The Manager’s Path*; Forsgren/Humble/Kim *Accelerate*; Larson *An Elegant Puzzle* — career/org metrics, not harness mechanics. Team Topologies already covers the usable org slice.
- **REJECT:** Richards/Ford *Fundamentals of Software Architecture*; Ford et al. *Building Evolutionary Architectures* — **A-dup** / fork risk of locked A + existing Fitness. Do not add as peers.

---

## Surface rules

| Surface | Rule |
|---|---|
| This file | Primary KEEP + CANDIDATE pointers |
| Co skill / AGENTS | One path pointer at most; **no book lists** |
| alwaysApply / new seats / marketplace | Forbidden (N=3 locked) |
| A–E skill body | Unchanged; blob `107a5118c95c1bf0b1b3d1755796632bff41b535` |

*End READING_CANON_V1. Cite EXIT HARNESS_SOURCES_SCOUT_V1 · Lead 2026-09-27.*

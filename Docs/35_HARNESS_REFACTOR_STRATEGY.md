# Harness refactor strategy — bounded, deletion-first

| Field | Value |
|---|---|
| **Status** | **PROPOSED** — awaiting Lead go/no-go on Phase 1 |
| **Date** | 2026-10-01 |
| **Mandate** | Single human developer, multiple agents, **game design in C++ with Unreal Engine 5.8** |
| **Supersedes** | the harness's implicit purpose, as recorded in [DEC-0033](decisions/AGENT_DECISIONS.md) / [DEC-0034](decisions/AGENT_DECISIONS.md) |
| **Hard constraint from Lead** | *"I don't want to keep going on and on making this harness. I want something I can update once in a while as I get new information, not something that becomes a forever project."* |

---

## 0. The problem, stated precisely

The harness is not broken. It is **unbounded**. On the branch under review, **24 of 32 commits were harness work and the product did not move.** Seven defects were found in the evaluation harness in a single day, several producing *confidently wrong* numbers. Every fix was locally reasonable; the accumulation was not.

That is the signature of a project with no stopping condition. The remedy is not more discipline — it is a **termination criterion written down in advance**, plus a **kill rule** for anything that has not earned its place.

### The three findings that make the cut possible

1. **The only automated fact about the game is that it compiles.** `Source/` contains **zero** automation tests. All 11 npm test scripts test harness tooling. `ci.yml` proves compilation and stops.
2. **`AGENTS.md` is now a Linux Foundation standard** (Agentic AI Foundation, 2025-12-09; 24.7k stars, MIT, 60k+ projects, read by opencode/Cursor/Codex/Aider/goose). A 25-file always-on rules corpus is enterprise scaffolding applied to one person.
3. **The harness's own research question was already answered by others.** arXiv 2602.11988 (ICLR 2026 Workshop, ETH Zurich) and `eth-sri/agentbench` (MIT) measured context-file ablation at scale: **LLM-generated context files −3% success at +20% cost; developer-written +4%.** Instructions in context files *are followed* (tool use 1.6× vs <0.01× when unmentioned) — they cost more and do not reliably move a task-success metric.

---

## 1. The target: six things, and nothing else

A harness for one person with several agents has exactly six jobs. Everything that is not one of these is a candidate for deletion.

| # | Job | Why it earns its place | Cost |
|---|---|---|---|
| 1 | **Know what to do** | `AGENTS.md` (now a standard) + a small UE-specific rule set | ~1 file + 6 |
| 2 | **Not invent game design** | `docs/human-use/cursor-cannot/` + taste gates | existing |
| 3 | **Prove it compiles** | `Tools/Safe-Build.ps1` wired to `npm run verify` | ~20 LOC |
| 4 | **Prove it behaves** | First Catch2 **Low-Level Tests** in `Source/` | the real work |
| 5 | **Not collide on the Editor** | UE Editor ownership lock — a hazard with no web-dev equivalent | ~40 LOC |
| 6 | **Be cheap to review** | Assumption disclosure per change | ~0 LOC, template only |

Job 2 already exists and is the highest-value thing in the current harness. **It is the one part the audit did not touch.**

---

## 2. Phases, with exit criteria

Each phase ends on a **testable** condition. If a phase cannot state one, it is not a phase.

### Phase 1 — DELETE (no new code)

The six cuts from [DEC-0034](decisions/AGENT_DECISIONS.md). All pure deletion.

- `score-mdc-lift.js` (1,006 LOC) + `score-mdc-rules.js` (462 LOC) + their tests
- the `decisions:check` boundary gate (keep the log file as prose)
- the tombstone-retirement apparatus
- `task-lift.js` → reduced to McNemar + the three-arm design (~200 LOC), mechanism replaced by promptfoo

**Exit:** `git diff --stat` shows ≥2,500 LOC removed; `npm run test:all` green; nothing in `docs/` references a deleted file.

**Estimate:** half a day. Mostly deletions.

### Phase 2 — GROUND the harness on the game

- `npm run verify` = Safe-Build + RunTests + `npm run test:all`, one command, one place
- **UE Editor ownership lock** — a lockfile in `Saved/`; one agent may drive the Editor at a time
- assumption disclosure added to the commit template

**Exit:** one command proves the game builds; a second agent cannot open the Editor while one holds it.

**Estimate:** one day.

### Phase 3 — PROVE it behaves *(the only phase with real work)*

First **Catch2-based Low-Level Tests** in `Source/`. Epic's ATF documentation states ATF is *"not ideal for pure unit testing"* — LLT is the intended tool for C++ unit tests in UE5.

Start with what a solo dev would otherwise check by hand after every agent change. Candidates:

- the six-resource inventory-lite round trip
- tame-state transitions
- damage stripping sin → conversion (not death)
- save/load across a restart

**Exit:** at least three LLTs green under headless invocation; `ci.yml` runs them; **the harness can finally assert something about behaviour rather than about itself.**

**Estimate:** 1–2 days.

⚠️ **Verify locally before relying on it:** check `Engine/Source/Runtime/Core/Public/Misc/AutomationTest.h` for the exact `WITH_AUTOMATION_TESTS` spelling on 5.8. Research could not confirm `WITH_DEV_AUTOMATION_TESTS` on Epic's 5.8 pages.

### Phase 4 — LEAN the context corpus

`.cursor/rules/` 25 → 6–8. Keep only what is genuinely UE-5.8-and-HomeWorld-specific: `unreal-cpp` (incl. API pitfalls), `ue58-sources`, `ue58-editor-ui`, game-development-principles, docs-directory-structure, testing. The tech-agnostic ones fold into `AGENTS.md` or go.

**Exit:** ≤8 rule files; `AGENTS.md` unchanged in role; **the always-on surface is shorter than it is today.**

**Estimate:** half a day. Mostly deletion and folding.

### Phase 5 — STOP

Write the maintenance contract (§4). Delete the plan documents for the work just completed.

**Exit:** the harness is **six commands and one page**. Nothing about it is a project.

---

## 3. What is explicitly NOT happening

| | |
|---|---|
| No more arms, trials, or runs of the evaluation harness | R4 and R5 answered it; `eth-sri/agentbench` already measured it at scale |
| No R6, no cost accounting | Superseded |
| No new rule files | The failure mode was growth, not absence |
| No Gauntlet | Requires a **source build of the engine** — days and tens of GB. AAA-scale |
| No LangSmith / Braintrust | Self-hosting is Enterprise-tier only; closed-source; indefensible at team size 1–3 |
| No promptfoo Cloud | The local CLI is free, MIT, and sufficient |
| No new decision-log gate | It was red for 14 commits and caught nothing |

---

## 4. The maintenance contract — the part that makes this not a forever project

**The harness is touched when, and only when:**

1. **UE version changes** (5.8 → 5.9) — refresh the pitfall rules, re-run LLTs
2. **A gate produces a wrong answer** — a false positive costs you time, a false negative costs you a bug
3. **Quarterly, 30 minutes** — delete anything unused

**Target maintenance cost: under an hour per touch.**

### Kill rule — the anti-bloat mechanism

> **Any harness component that has not prevented or caught a real problem in 6 months is deleted.**

This is the clause that stops the next 24 commits. It is deliberately harsh, and it is asymmetric on purpose: a harness that has never caught anything is not insurance, it is tax.

### What "demonstrably useful" means, operationally

The harness is doing its job when **the product moves and agents are cheap to supervise**. Concretely:

| Signal | Target |
|---|---|
| Commits touching harness vs product | **Inverted from today** — product-dominant |
| Agent changes needing correction before merge | Declining over time |
| Bugs reaching you from an agent change | Near zero |
| Time you spend reviewing an agent's work | Minutes, not hours |
| `npm run verify` | Catches the failure before you see it |

**If after 3 months the ratio has not inverted, delete the harness entirely and rely on `AGENTS.md` plus the build gate.** That is a real option, not a rhetorical one.

---

### Phase 5 — STOP — **DONE**

Delivered: [36_HARNESS_MAINTENANCE_CONTRACT.md](36_HARNESS_MAINTENANCE_CONTRACT.md).

The maintenance contract is the phase. It states what the harness now is, the three
triggers that justify touching it, the six-month kill rule, the success signals, and
an explicit escape hatch: **if the harness-to-product commit ratio has not inverted
within three months, delete the harness** and rely on `AGENTS.md` plus the build gate.

### Phase 3 — PROVE it behaves — **OPEN, deliberately the last thing**

Revised per *Week 1 – Agentic Engineering*: **behaviour tests, not Catch2 unit
tests.** Unit-level TDD is *"impractical for most cases"* when the unit is a class;
BDD is *"a perfect fit for LLM-assisted engineering."*

Toolchain verified present 2026-10-01 (`dotnet`, `vswhere`, `UE_5.8`), so this is
feasible. It is left last deliberately: it is the only phase whose size is unknown,
and it needs a real build cycle rather than another context-starved pass.

---

## 5. Honest gaps in this strategy

1. **The PDFs you referenced are not in the repo.** I found no `.pdf` anywhere under `C:\dev\HomeWorld`. I have designed against the written material only — the taste interview, the art-pipeline research, and the harness research. If the loop-engineering design PDFs carry constraints I am missing, attach them and I will revise before Phase 1.
2. **The loops and GSD material in `.opencode/gsd-core/` was not audited.** It may be worth keeping, and I did not assess it.
3. **Phase 3 is the only phase whose size I do not know.** Writing LLTs may surface build or module issues that change the estimate.
4. **I have not verified that `Tools/RunTests.ps1` works headlessly**, only that it exists.

---

## 6. The one-paragraph version

Delete 2,500+ lines, replace the evaluation *mechanism* with promptfoo while keeping McNemar, wire the UE build into one command, add an Editor lock, write three Catch2 tests, collapse 25 rules to 7 — then **stop**, with a kill rule that deletes anything unused for six months. If the harness-to-product commit ratio has not inverted in three months, delete the harness.

*Strategy — [Docs/35_HARNESS_REFACTOR_STRATEGY.md](35_HARNESS_REFACTOR_STRATEGY.md) — awaiting Lead go/no-go.*
# The HomeWorld harness — maintenance contract

| Field | Value |
|---|---|
| **Status** | **IN FORCE** 2026-10-01 |
| **Mandate** | One human developer, several agents, **game design in C++ with Unreal Engine 5.8** |
| **Strategy** | [35_HARNESS_REFACTOR_STRATEGY.md](35_HARNESS_REFACTOR_STRATEGY.md) · **Decisions** [AGENT_DECISIONS.md](decisions/AGENT_DECISIONS.md) DEC-0033/0034 |
| **Origin** | Built with a prior AI from lab and forum research. That provenance explains the original shape and is recorded, not criticised — see §6 |

---

## 1. What the harness IS

**Six commands and one page.** That is the whole thing.

| Command | What it does |
|---|---|
| `npm run verify:fast` | JS suite. Seconds. Safe on every save. |
| `npm run verify` | + compile the C++. The default. Editor must be closed. |
| `npm run verify:ue` | + run UE automation tests. Needs `$env:UE_EDITOR`. |
| `npm run editor:lock <acquire\|release\|status>` | UE Editor ownership. One agent at a time. |
| `npm run scope:reconcile` | Declared scope vs the tree. Found real gaps. |
| `npm run decisions` | Decision log inspection. **Manual, non-gating.** |

Plus `AGENTS.md` (always-on, and now a Linux Foundation standard) and 25 glob-scoped rules in `.cursor/rules/`.

Everything else was deleted. See §4.

---

## 2. When you touch it — three triggers, nothing else

1. **UE version changes** (5.8 → 5.9). Refresh `unreal-cpp.mdc` pitfall rows, re-run `verify:ue`.
2. **A gate gives a wrong answer.** A false positive costs you time; a false negative costs you a bug. Both are worth ten minutes.
3. **Quarterly, 30 minutes.** Delete anything unused.

**Target cost: under an hour per touch.** If a touch is taking longer, that is the signal something new is being built, and the answer is no.

---

## 3. Kill rule — the anti-bloat mechanism

> **Any harness component that has not prevented or caught a real problem in six months is deleted.**

Deliberately harsh, deliberately asymmetric. A harness that has never caught anything is not insurance — it is tax charged against the scarcest resource in a one-person company.

---

## 4. What was deleted, and why that matters

| Removed | Reason |
|---|---|
| `score-mdc-lift.js` (1,006) + `score-mdc-rules.js` (462) + tests | Scored the **text** of rules. Our own header said they cannot answer the question that matters. |
| `harness-coverage.js` (369), `evidence-grep.js` (253), `preflight-scorer.js` (120) | Same layer. Watched the watchers. |
| `decisions:check` boundary gate | Enterprise compliance control on a team with no auditors. Red for 14 commits, caught nothing. Log kept as prose; script runnable by hand. |
| `task-lift.js` **features** — `--resume`, `--trials`, third arm | R4 and R5 answered the question. The three-arm design and McNemar are **kept**; the machinery around them was not earning its place. |
| 6 tombstone rules (31 → 25 files) | Retired pointers, not guidance. `ue57-sources.mdc` said of itself: *"HISTORICAL… Do not use for new Unreal lookups."* |

**Harness: 7,517 → ~4,250 LOC. Rules: 31 → 25 files. Tests: 236 → 115.**

---

## 5. What "working" looks like — and the escape hatch

The harness succeeds when **the product moves and agents are cheap to supervise.**

| Signal | Target |
|---|---|
| Harness commits vs product commits | **Inverted from 24:8.** Product-dominant. |
| Review time per agent change | Minutes |
| Bugs arriving from agent changes | Near zero |
| Gates that fire on their own | At least one, occasionally |

> **If in three months the ratio has not inverted, delete the harness entirely** and rely on `AGENTS.md` plus the build gate. That option is written down to be believed, not to look reasonable.

---

## 6. Provenance, recorded fairly

The original harness was built with a prior AI from lab and forum research. **That is not a mistake in the work — it is the natural output of the source material.** Research on harness engineering publishes *measurement tools*, because benchmark findings require measurement instruments. An agent building faithfully from that material produces scorers, coverage tools and ablation rigs.

The failure was in the transfer. The research answered *"do context files help coding agents?"* Your harness answered that question. Your question is *"does this help me ship a C++ UE game with several agents?"*

**What survives from that work and is worth keeping:** `cursor-cannot` + taste gates (the only thing between agent initiative and unrequested game design), `AGENTS.md` as the single always-on surface, the boundary-surface thinking, and explicit aborts when evidence was thin.

---

## 7. The one open obligation

**`Source/` contains zero automation tests.** Until it does, the only automated fact about HomeWorld is that it compiles.

Per *Week 1 – Agentic Engineering*: unit-level TDD is *"impractical for most cases"* when the unit is a class; **BDD is *"a perfect fit for LLM-assisted engineering."*** So the obligation is **behaviour tests, not Catch2 unit tests** — and the first ones should be the things you would otherwise check by hand after every agent change:

- the six-resource inventory round trip
- tame-state transitions
- combat stripping sin → conversion (never death)
- save/load across a restart

Build toolchain verified present 2026-10-01: `dotnet`, `vswhere`, `UE_5.8`.

---

## 8. What not to build next

| | |
|---|---|
| **Another measurement of the agent harness** | It has produced zero product decisions. `eth-sri/agentbench` (MIT) already ran the ablation at scale: LLM-generated context **−3%**, developer-written **+4%**, cost **+20%**. |
| **Gauntlet-style loops** | Unbounded agentic state, subjective stop condition. *Your own Week 1 slides* identify this as the failure mode — and 24 commits of harness work was exactly it. |
| **New rule files** | The failure mode was growth, not absence. |
| **More eval arms / trials / R6** | Superseded by DEC-0034. |
| **LangSmith / Braintrust** | Self-hosting is Enterprise-only. Closed-source. promptfoo is MIT and free. |
| **Gauntlet (UE)** | Needs a **source build of the engine**. Days, tens of GB. Gate behind real multiplayer. |

**Loop Engineering discipline applies to harness work itself:** deterministic stop condition, strict cost ceiling. Phase 1–5 of the refactor is the last unbounded project.

---

*Harness maintenance contract — IN FORCE 2026-10-01. Touch on trigger, not on mood.*
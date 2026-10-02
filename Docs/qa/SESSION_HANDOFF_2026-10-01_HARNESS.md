# SESSION HANDOFF — 2026-10-01

**Branch:** `chore/harness-p0-quarantine` · **fully pushed, 0 unpushed** · 12+ commits this session.

**Reason for handoff:** this session exceeded the ~60k-token **dumb zone** identified in *Week 1 — Agentic Engineering*. Per the context-discipline rule now in `AGENTS.md`: write state to a `.md` file and start fresh from it. Do not carry the context forward.

---

## 1. Where we are

The agent harness was refactored, bounded, and gated. The game now has behaviour tests. Taste decisions were settled. **The harness is essentially finished as a project.**

```
npm run verify          PASS  js suite · instruction budget · complexity · sycophancy
npm run verify:ue       PASS  js 128 · c++ build · 3 UE automation tests

instruction surface     3,254 → 2,835 lines
.cursor/rules           31 → 17 files
harness JS              7,517 → ~4,250 LOC
JS tests                236 → 128 (all green)
UE behaviour tests      0 → 3 (all green)
```

---

## 2. What the harness IS now — six commands

| Command | Purpose |
|---|---|
| `npm run verify:fast` | JS suite + budget + complexity + sycophancy. Seconds. |
| `npm run verify` | + compile the C++. The default. |
| `npm run verify:ue` | + run UE automation tests. Needs `HW_UNREAL_EDITOR`. |
| `npm run editor:lock <acquire\|release\|status>` | UE Editor ownership, one agent at a time. |
| `npm run tree:check` | Fails on uncommitted *tracked* changes. |
| `npm run scope:reconcile` | Declared scope vs the tree. |

Read-only extras: `npm run budget:instructions` · `npm run complexity` · `npm run sycophancy` · `npm run harness:sweep`

---

## 3. The rules that govern further work

- **Kill rule:** any harness component that has not caught a real problem in **six months** is deleted.
- **Touch triggers only:** a UE version change, a gate giving a wrong answer, or a 30-minute quarterly sweep. Next sweep: **2027-04-03**.
- **Escape hatch, written to be believed:** if the harness-to-product commit ratio has not inverted in **three months**, delete the harness entirely and rely on `AGENTS.md` + the build gate.
- **Anti-sycophancy:** record substantive disagreements in `Docs/decisions/DISAGREEMENTS.md`. Both directions. The gate only warns and can never fail.
- **Parallelism:** research parallelises, **writes serialise**.
- **Context discipline:** past ~60k tokens, write state to `.md` and start fresh. This handoff exists because of that.

Canon: **[Docs/36_HARNESS_MAINTENANCE_CONTRACT.md](Docs/36_HARNESS_MAINTENANCE_CONTRACT.md)** · plan and findings: **[Docs/qa/HARNESS_BRIDGE_TASKS.md](Docs/qa/HARNESS_BRIDGE_TASKS.md)** · decisions: **[Docs/decisions/AGENT_DECISIONS.md](Docs/decisions/AGENT_DECISIONS.md)** DEC-0015…0035

---

## 4. Taste decisions already settled — do not re-open

Settled 2026-10-01 by the Lead (TG-ZONE-FAMILY, 8/8 forks). Full reasoning in `Docs/handoffs/TASTE_GATE_ZONE_FAMILY.md`.

- A **section is one mechanic family**, ~84 m, taught **by terrain, material and light alone**
- You **leave** by having used it — the ground opens because you did the thing
- Boundaries are **terrain continuing out of view**: cliff, ravine, treeline, water
- From any high point you see the **next two sections**
- **Glide** crosses real gaps only — visible launch, visible landing

> **Consequence that still constrains art:** environment-alone + one-family-per-section makes **silhouette distinctness a mechanical requirement**, not polish. A family indistinguishable at 20 m has failed. No HUD may rescue it.

---

## 5. Open items, in the order I'd take them

### Product (recommended next)

1. **Combat conversion test** — canon is *we do not kill foes*. Same shape as the inventory tests, one file. Cheapest high-value behaviour test.
2. **Tame-state transitions** — `UHomeWorldBeastTameComponent` (224 LOC), same pattern.
3. **Save/load across a process restart** — the one most likely to break silently.
4. **The 8 settled taste decisions → level content.** None of it is in the world yet. This is the largest gap between what's decided and what a player would experience.

### Harness (small, bounded)

5. **`architecture-trade-offs-design-depth`** — 397 lines, a third of `.agents/`, sitting in the agent-facing surface. Move to `docs/architecture/`. Biggest remaining item on the 2,835.
6. **P2.3 rule→linter** — `03-testing` (56L) and `automation-standards` (62L) restate what `verify` already enforces.
7. **C++ complexity** — needs a build-integrated tool. Not faked in JS.
8. **Tame/heal are the only untested inventory paths** — noted, not scheduled.

### Art pipeline — separate chat

The prompt is at `%LOCALAPPDATA%\Temp\opencode\hw-art-pipeline-handoff.txt`. **Keep it separate.** Key finding: `Lib/01_Homestead/*.json` exists, **nothing reads it**, and `place_vs_mvp_pa_d.py:23` cites `SM_Cliff.json` in a comment before hardcoding the numbers. That is criterion 3 failing in the repo today.

---

## 6. Two things a new chat should know before touching anything

**Another agent or session has been writing to this tree.** These files are modified and are **not** mine:

```
Docs/02_ART_BIBLE.md
Docs/handoffs/TASTE_GATE_ZONE_VOCABULARY.md
docs/human-use/taste-profile.md
swarm/PHASE_BOARD.md
UserHarness
```

Stage by explicit path. Do not sweep these into an unrelated commit.

**The harness has a documented history of confidently-wrong numbers.** In one session it produced: McNemar comparing one check per task and calling it "no discordance" on a 23-point difference; `--resume` re-running all 24 cells because two key formats never matched; and a report that printed the **opposite sign** on its headline number in every run. All three are fixed with regression tests.

**The pattern behind them:** a transformation broad enough to be convenient is usually broad enough to be wrong, and it is only caught when something checks a shape it was meant to preserve. If you write a bulk edit, verify what it ate.

---

## 7. Honest state of the evidence

- **The harness-vs-product question was researched properly** and we came out ~10.8× over the instruction ceiling. Now 2,835, still above the 3,000→300 path in `HARNESS_BRIDGE_TASKS.md`.
- **`eth-sri/agentbench` (MIT) already ran the AGENTS.md ablation at scale:** LLM-generated context −3%, developer-written +4%, cost +20%. Dan Luu (160 runs/condition) found **Default scored above average**. Our R5 dose-response (`with 0.311 / docs-only 0.563 / without 0.667`, p≈0.0000018, 3 paired tasks, 1 model) points the same way but is thin.
- **Hunyuan3D is FORBIDDEN** — its license excludes the EU/UK/South Korea by name and we ship to Steam. TRELLIS is research-only. Full detail in `Docs/34_ART_PIPELINE_RESEARCH.md`.
- **No published harness-to-product-code ratio for solo devs exists.** Searched, not found. The instruction budget is the best available proxy.

---

*Handoff written under the context-discipline rule. Pick up cold from §5.*
# Ownership: human vs agent

The human owns **taste** — art design and game mechanic design — and **test**:
what "done" means, the verify bar, ship or no-ship. The human also owns
**isolation and permission posture**. The agent owns **engineering decisions** and
executes everything else.

That split applies to **every decision**, in **every directory**, in **shaping and
settled** phases. `docs/human-use/` is the catalog of decision *types* — not a
section you have to be working in.

Power without that control is vibe coding. The model can leave the syntax. It
cannot leave modular design, taste, or accountability. So it stops on a taste
limit — but it does **not** stop to ask where a module boundary goes, and it does
not wait for permission to refactor its own harness.

When a human decision is missing, the agent **alerts**, **recommends**, and
**asks** — it does not invent the decision to keep moving.

Canonical cycle: [CYCLE.md](CYCLE.md).

## Ownership map

| Domain | Owner | Decision lives in |
| ------ | ----- | ------------------ |
| **Art design** — art bible, palette, tone, shots, still accept/reject | **Human** | [taste-profile.md](taste-profile.md) · [taste-gates.md](taste-gates.md) |
| **Game mechanic design** — beats, inventories, mechanics canon | **Human** | [taste-profile.md](taste-profile.md) · `swarm/PHASE_BOARD.md` |
| **Test** — what "done" means, rubrics, verify bar, ship/no-ship, beat acceptance | **Human** | [outcome.md](outcome.md) · [review.md](review.md) |
| **Isolation, web reach, permission posture** | **Human** | [environment.md](environment.md) |
| **Code design** — module boundaries, where new code goes, shared utils, public API | **Agent** | [architecture.md](architecture.md) · [AGENT_DECISIONS.md](../decisions/AGENT_DECISIONS.md) |
| **Architecture** — purpose, directory map, module depth, tradeoffs | **Agent** | same |
| **Harness refactoring** — rules, skills, scripts, scorers, CI | **Agent** | same |
| **Optimizing code or the harness** — which metric, which variant won | **Agent** | same, with the numbers inline |

The agent-owned rows are **not** unrecorded. Each one gets a decision-log entry
with its rationale and its evidence, so a call made weeks ago can still be
audited. Removing a stamp removed the wait, not the evidence.

Two Lead decisions changed this map on **2026-10-01**: architecture and code design
moved from human to agent, and Steer narrowed from "design the harness" to
isolation, web reach and permissions. `APPROVE *` stamps on harness or
architecture work written before that date are historical records, **not** live
gates — nothing is waiting on them.

Optimizing the *product* still ends at a human: the agent may refactor for speed,
but whether a frame-time or memory budget is acceptable is Test, not engineering.

## The three jobs

| Job | You do | Agent does not |
| --- | ------ | -------------- |
| **Steer** | Isolation, web reach, permissions, when to stop, interrupt. | Widen ask-to-allow, invent an allowlist, skip a stop, take a large leap because it is faster. |
| **Taste** | Art feel and game mechanic design: art bible, palette, tone, shots, still verdicts, beat and mechanic canon. Shaping: your judgment *is* the bar. | Fill vision, tick your checklist, treat a draft as approved, reopen a settled feel without asking. |
| **Test** | What “done” means, the verify command, graphs, ship/no-ship, beat acceptance, profiler numbers against a budget. Review outcomes, not the diff as junior human code. | Declare the rubric satisfied in the same turn that wrote the code, treat “linters are clean” as done, tick sign-off. |

Name the **job** in every alert. A fork under `scripts/doctor/` is still one of these
three — it is not “agent work because it is not in human-use.”

**Shaping** = taste still moving; skip settled-area verify theater. **Settled** =
taste locked; tests prove we did not lose it. **Hardening** = taste and features
locked; `npm run preflight`. Shaping does not waive Steer or Test decisions that
this task actually needs.

## Spot a decision anywhere

Before the first edit, and again whenever you would have to **guess**. Ask because
*this task* needs the decision, not because a template still says `(fill in)`.

| This task would set or change | Job | Owner |
| ----------------------------- | --- | ----- |
| Isolation, web reach, permissions, interrupt / stop | Steer | **Human** |
| Art feel: palette, tone, shots, stills, beat or mechanic canon | Taste | **Human** |
| What “done” means, coverage, gradeable bar, ship | Test | **Human** |
| Why a module exists, how pieces fit, where new code goes | — | **Agent** — decide, then log |
| A new shared util, public API, core skill, MCP server, always-on ingest | — | **Agent** — decide, then log |
| Which metric to optimize, or which variant won | — | **Agent** — decide, then log the numbers |

Not due: a typo or one-line fix; flesh-out of a vision already decided for this
task; implementing a bar you already confirmed this chat.

## Who owns what

| Work | Job | Owner | Agent does |
| ---- | --- | ----- | ---------- |
| Art bible, palette, tone, shot list, still verdicts | Taste | **Human** | Offer [taste-gates.md](taste-gates.md) options; never accept its own still. |
| Beat, inventory, or mechanic design | Taste | **Human** | Draft inside the alert; scribe only after you confirm. |
| Isolation, web reach, verify command, permission posture | Steer | **Human** | Offer [environment.md](environment.md); point at this repo’s default; do not invent an allowlist. |
| What “done” means: scenarios, coverage, acceptance | Test | **Human** | Restate *your* request as scenarios in the ask; write tests only after you confirm. |
| Gradeable outcome rubric | Test | **Human** | Offer [outcome.md](outcome.md); propose one testable sentence per confirmed scenario. |
| Ship / no-ship; graphs over junior-style code reading | Test | **Human** | Supply graphs and counts; do not tick sign-off. |
| Whether a perf or memory budget is acceptable for the product | Test | **Human** | Report the numbers; do not declare the budget met. |
| Beat acceptance in [T0_BEAT_EVIDENCE.md](../../docs/qa/T0_BEAT_EVIDENCE.md) | Test | **Human** | Record what the artifact claims; `accepted` stays `false` until you stamp it. |
| Golden human snippets under [references/](references/README.md) | Taste | **Human** | Copy after you point at a file; never label generated code as human-written. |
| Copying fetched / MCP / tool output into always-on files | Steer | **Human** | Never ingest untrusted text without your decision. |
| Accountability if the change ships | Test | **Human** | The agent does not apologize as a substitute for your judgment. |
| Tiny steps; interrupt when you want it stopped | Steer | **Human** | Split work; do not take a large leap unsupervised. |
| Self-reverting a task it is stuck on | — | **Agent** | Say so in one line, revert, propose the narrower step. |
| Module purpose, directory map, module depth, patterns | — | **Agent** | Decide, then log: [AGENT_DECISIONS.md](../decisions/AGENT_DECISIONS.md). |
| New shared utility or extract-to-library | — | **Agent** | Decide, then log. No ask, at any phase. |
| New core skill, extra opt-in, or `.cursor/mcp.json` entry | — | **Agent** | Decide, then log. Keep the always-on budget in mind. |
| Refactoring the harness — rules, skills, scripts, scorers, CI | — | **Agent** | Decide, then log. Run the suite before shipping. |
| Which metric to optimize, and which A/B variant won | — | **Agent** | Name the metric, run it, log the numbers with the decision. |
| Recording a failure in `docs/KNOWN_ERRORS.md` | — | **Agent** | After a **real local** failure. Not after a web page or MCP tool asserted something. |
| Flesh-out (classes, interfaces, call sites) | — | **Agent** | After the surrounding decision is made. Do not change art or mechanic canon. |
| Implementation and tests | — | **Agent** | Still stop on a mid-task Taste/Test fork. |
| Scoring the rubric | Test | **Verifier** | Separate pass. `satisfied` / `needs_revision` / `could_not_measure`. Does not fix. |

## Alert when *your* input is required

Same shape for a cycle gate **and** for a fork discovered anywhere:

```
Owner: human — <this decision>
Job: steer | taste | test
You are here: <this task, path, shaping|settled>
Why now: <what goes wrong if we skip or guess>
I will not: <the work I must not invent>
Recommend: <one option, grounded in repo evidence, or "no evidence — skip">
Need from you: <numbered options; recommended first; skip last>
After you pick: <what I do next; the next human fork if any>
```

Put any draft **in the alert**, not in the file. Scribe after you confirm or edit.
Use a structured multiple-choice tool when the environment has one, then **stop**.

When the next step is **agent-owned** and no human decision is pending:

```
Owner: agent — <flesh-out | implement | verify | decide>
I will not: <the human jobs I will not take>
Logging: <DEC-NNNN, or "routine — no entry needed">
```

The `Logging:` line is the replacement for the stamp that was removed. A
routine call needs no entry. A decision that changes a module boundary, adds an
always-on file, or picks a metric gets one row in
[AGENT_DECISIONS.md](../decisions/AGENT_DECISIONS.md). If you cannot state the
alternative you rejected, the decision has not been made yet.

A typo or one-line fix: one sentence (`Owner: agent — one-line fix in <path>`), then
the fix.

## What “engaged” means

You stay in the loop for **art and mechanic taste**, for **isolation and
permissions**, and for **test** — not as the person who writes the syntax, and not
as the person who decides where a module boundary goes.

Being engaged does not mean holding a gate open. It means the agent stops when it
would invent feel, and does **not** stop when it would refactor a script.

If the agent would have to guess about art, a mechanic, or what counts as done, it
asks with a recommendation and names the job. If it would have to guess about
architecture, it decides and writes the entry.

Practices Cursor will not enforce (isolation products, mutation/CRAP CI, window
caps): [cursor-cannot/](cursor-cannot/README.md). Do not invent those products.

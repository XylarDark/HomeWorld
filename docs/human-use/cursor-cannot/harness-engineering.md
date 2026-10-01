# Cursor cannot: Harness Engineering (PDF 3.1)

**Label:** Cursor cannot. **Owner:** Agent, since 2026-10-01 (was: human Test).

The PDF’s harness is everything outside the model: instructions, tools, environment,
state, and verification. Most of that is this repo’s `AGENTS.md`, skills, and
Human Use. Two pieces are **not** Cursor products.

Nothing in this file is a gate you are asked to work. The agent now designs and
improves its own harness, and logs the decisions that matter
([AGENT_DECISIONS.md](../../decisions/AGENT_DECISIONS.md)). The limit below is
not "we need a human for this" — it is "this product does not exist, so do not
build it and call it closed."

## What the PDF asked

- Make runtime **observable and debuggable** as part of the harness.
- Verify with full-pipeline tests, self-reflection, and **adversarial reviews**
  (a competing LLM), not “I’m done.”
- Stop agents from declaring victory too early.

## What Cursor actually has

- A local agent, tools, and (if you start it) debug mode. There is no harness
  dashboard, no always-on trace of every tool call for you to audit, and no
  built-in second-model reviewer that runs on every change.
- We already require **counts** from a named verify command and a **separate
  verifier** pass for the outcome rubric. That is policy, not a Cursor feature.
- An adversarial pass is optional and is now the agent's to run: spawn the
  competing review as a subagent or a second session. It used to be a second chat
  you opened by hand.

## What the agent does

- **Early-victory defence is the agent's job.** Treat "I'm done" as a claim. Run
  the named verify command, and keep the separate verifier pass — the implementer
  does not grade itself. This is **Test** and still terminates at a human for
  ship/no-ship, but nothing waits on a human to *run* the check.
- **Harness design and refactoring are the agent's.** Rules, skills, scripts,
  scorers, CI. Decide, then log.
- Do not add a mutation-testing CI job, a CRAP action, or a custom observability
  product to "close" this slice. Those are other Cursor-cannot files.

## What the harness now does about early victory

The PDF's central warning is "stop agents declaring victory too early." Four
mechanisms exist, and each was added after the harness produced a confident wrong
number rather than because the PDF suggested it:

| Mechanism | Guards against | Command |
| --------- | -------------- | ------- |
| **Ablation verification** — the "without harness" arm is proven to have no harness left in it | Two arms that agree for the wrong reason, reported as "no effect" | `npm run tasklift` |
| **Void runs** — an agent that never ran is excluded from the denominator, not scored 0 | A crashed run read as a weak one | `npm run tasklift` |
| **Positive control** — each task's known-good answer must score 100% | An unsatisfiable check reporting a permanent 0% that reads as "the harness doesn't help" | `npm run tasklift:control` |
| **Decision-log enforcement** — a boundary change without a written reason fails | A decision made in the gap a removed human stamp used to fill | `npm run decisions:check` |

The common failure these share: an instrument that cannot fail, or cannot tell
success from absence, reports a number that looks like evidence. The first pilot
did all four at once and produced `lift: 0.25` from eight rejected agent sessions.

**Still absent:** a competing-model adversarial pass. The PDF asks for one; nothing
in `scripts/` implements it, and the agent now owns self-review — which is exactly
where a sycophantic model flatters its own work. A same-model adversarial pass is
weak; the PDF means a different provider. Not built; see
[AGENT_DECISIONS.md](../../decisions/AGENT_DECISIONS.md) for what would have to be
true to add it.

## Harness Test responsibilities (portable)

Stop **early victory** from metric proxies. The harness — scripts, reports, skills — must:

1. **Arrange before Act** — preflight gates that block capture/run when `ready: false`, or
   document **Harness exempt** where Arrange cannot apply.
2. **Three-state outcomes** — `pass` / `soft_fail` / `closed_fail`, defined once in
   [`scripts/outcome.js`](../../../../scripts/outcome.js) and shared. `void` is the
   *absence* of a state, not a fourth one: an unmeasured subject is excluded from
   the denominator rather than scored 0. A harness green is not a human visual or
   taste PASS.
3. **Metric ≠ visual** — luminance, checksums, screenshot size, and DOM snapshots prove the
   pipeline ran; framing, composition, and taste need a human stamp (see
   [taste-gates.md](../taste-gates.md) when taste limits apply).

Agents must record preconditions (content present, aim/focus, environment gates) in reports
before Act. Empty or black output without that evidence is not grounds for **closed_fail**.

Canonical checklist: [automation-harness.md](../../guides/automation-harness.md). Host UE
Editor policy: [.cursor/rules/automation-standards.mdc](../../../.cursor/rules/automation-standards.mdc).
Opt-in stack-agnostic mirror: `.agents/skills-extras/automation-standards` and
`testing-standards` (see [`.agents/README.md`](../../../.agents/README.md)).

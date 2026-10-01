# Cursor cannot: Optimization Refactor (PDF section 5)

**Label:** Cursor cannot. **Owner:** Agent, since 2026-10-01 (was: human Test).

The PDF splits refactor: the agent may chase duplication; **you** own performance.
That split is **reversed** as of 2026-10-01 — the agent now names the metric,
measures, and picks the A/B winner, then logs the numbers. See
[optimization.md](../optimization.md) and
[AGENT_DECISIONS.md](../../decisions/AGENT_DECISIONS.md).

What the human keeps is the **budget**, not the measurement: whether the resulting
frame-time or memory number is acceptable for the product. That is a Test
decision. The tooling gap below is unchanged and is still the reason a performance
claim in this repo is weakly evidenced.

## What the PDF asked

- Human **profiling** and A/B compilations.
- Feed the numbers back; do not optimize because the code “looks slow.”
- Do not review AI code as if it were human code — ask for graphs instead
  (see [code-quality-review.md](code-quality-review.md)).

## What Cursor actually has

- No built-in profiler, frame-time HUD, or A/B compilation runner for this
  template. Whoever measures, does it by hand with the engine's own tools.
- The agent can produce two variants and compare them itself. It **must** name the
  metric before it starts, and it must record a "before" number — a comparison with
  nothing on the left is not a result.

## What the agent does

Do not start a performance pass because the code "looks slow." Default is **skip**
unless a task actually needs speed.

When a performance pass *is* the task:

1. Name the metric and the hardware.
2. Measure before, change, measure after.
3. Record both numbers, the A/B outcome, and the alternative you rejected, in
   [optimization.md](../optimization.md) and the decision log.
4. Hand the budget to the human.

Do not invent a benchmarking product, and do not present "looks slow" as evidence.

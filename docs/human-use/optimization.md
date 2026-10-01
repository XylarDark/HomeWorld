# Optimization — agent-owned metrics, human-owned budget

**Owner: agent**, for choosing the metric, running it, and naming the A/B winner.
As of 2026-10-01 the "paste your numbers" gate is gone — the agent measures and
logs instead. See [OWNERSHIP.md](OWNERSHIP.md#ownership-map) and
[AGENT_DECISIONS.md](../decisions/AGENT_DECISIONS.md).

The one thing that stays human: whether the resulting frame-time, memory or build
budget is **acceptable for the product**. The agent may refactor for speed; it may
not declare the budget met. That is a **Test** decision.

Do not start a performance pass because the code "looks slow." Optimizing without a
named metric produces a number nobody can check.

## How the agent works this

1. **Name the metric first.** Frame time, p95, heap, build seconds. If you cannot
   name it, you have not decided to optimize.
2. **Measure before changing anything.** A "before" number is the only thing that
   makes the "after" mean anything.
3. **Log both numbers with the decision**, plus the alternative you rejected — for
   example, why you simplified instead of caching.
4. **Hand the budget to the human.** State the numbers; let Test decide.

## Measurements

What you ran, on what hardware, and the numbers that matter.

```
(fill in)
```

## A/B

What two compilations or implementations you compared, and which won.

```
A:
B:
Winner:
```

## Ask the agent

Previously you pasted a change request here. Now the agent writes the change and
the entry; this section is the request it is answering, kept for the case where you
want a specific optimization pursued.

```
(fill in)
```

Cursor has no profiler for this template:
[cursor-cannot/optimization-refactor.md](cursor-cannot/optimization-refactor.md).
Do not invent a benchmarking product to close that gap.

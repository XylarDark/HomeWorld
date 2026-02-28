# Spec-first and plan-first

When to use a spec or plan before implementation, and where plans live.

## When to plan first

For **complex or multi-file work**, the agent should propose a short implementation plan and get approval before editing. For **new features**, the plan should be informed by research (Epic/UE docs, best practices) and by following tutorials first, then expanding; see [.cursor/rules/07-ai-agent-behavior.mdc](../.cursor/rules/07-ai-agent-behavior.mdc) (Feature development: research and tutorials first). See [.cursor/rules/17-plan-first.mdc](../.cursor/rules/17-plan-first.mdc) for the rule and when to skip.

## Where plans live

- **Saved plans:** Plans can be saved under `.cursor/plans/` (e.g. `feature-name.md`) for resume and for future agents. Use when the user asks or when the task is large enough to benefit from a persistent reference.
- **Plan Mode:** In Cursor, use Plan Mode (Shift+Tab in the agent input) to get a reviewable plan before any code is written. You can save the result to `.cursor/plans/` via "Save to workspace."

## Spec-first (optional)

For very large features, a more formal flow is: agree on a short spec or requirements (what and why), then have the agent produce a technical plan (files, steps, constraints), then implement step by step. We do not require `plan.md` or `todo.md` for every task; the 17-plan-first rule is enough for most work.

## References

- Cursor: [Best practices for coding with agents](https://cursor.com/blog/agent-best-practices) (plan before code, save plans to `.cursor/plans/`).
- Project: [.cursor/rules/17-plan-first.mdc](../.cursor/rules/17-plan-first.mdc), [AGENTS.md](../AGENTS.md) (Commands, Boundaries).

# Spec-first and plan-first

When to use a spec or plan before implementation, and where plans live.

## When to plan first

For **complex or multi-file work**, the agent should propose a short implementation plan and get approval before editing. For **new features**, the plan should be informed by research (Epic/UE docs, best practices) and by following tutorials first, then expanding; see [.cursor/rules/07-ai-agent-behavior.mdc](../.cursor/rules/07-ai-agent-behavior.mdc) (Feature development: research and tutorials first). See [.cursor/rules/17-plan-first.mdc](../.cursor/rules/17-plan-first.mdc) for the rule and when to skip.

## Where plans and task lists live

- **Plans and task lists stay in the agent chat** by default. When the user asks for a plan or a task list, present it in the conversation (e.g. Cursor plan feature or a markdown list in the reply). Do not create or update files in `.cursor/plans/` or standalone task-list docs unless the user explicitly asks to save to a file or to the workspace.
- **"Make a plan" / "Create a plan":** Use the Cursor plan feature or write the plan in chat. Only create a file if the user explicitly asks to save the plan.
- **Plan Mode:** Use Plan Mode (Shift+Tab) to get a reviewable plan in-app before code is written. Keep the result in chat unless the user asks to save it to a file.

## Spec-first (optional)

For very large features, a more formal flow is: agree on a short spec or requirements (what and why), then have the agent produce a technical plan (files, steps, constraints), then implement step by step. We do not require `plan.md` or `todo.md` for every task; the 17-plan-first rule is enough for most work.

## References

- Cursor: [Best practices for coding with agents](https://cursor.com/blog/agent-best-practices) (plan before code; keep plans in chat unless the user asks to save).
- Project: [.cursor/rules/17-plan-first.mdc](../.cursor/rules/17-plan-first.mdc), [AGENTS.md](../AGENTS.md) (Commands, Boundaries).

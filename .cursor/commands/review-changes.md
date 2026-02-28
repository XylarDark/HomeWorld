# Review changes

Light review of current diffs for style, project patterns, and known pitfalls.

## Steps

1. **Inspect current changes**
   - Use Source Control / `git diff` to see staged and unstaged changes.
   - Focus on the files the user cares about (or all if small).

2. **Check against project rules**
   - **Style:** C++ (unreal-cpp.mdc), Python (12-python.mdc), commits (04-git-workflow.mdc).
   - **Boundaries:** No secrets, no edits to `Saved/` or `Plugins/UnrealMCP/`, no engine/platform change without team decision (AGENTS.md Boundaries).
   - **Known errors:** If touching areas mentioned in `docs/KNOWN_ERRORS.md`, ensure the fix or change doesn’t repeat a documented pitfall (e.g. MCP `blueprint_name` short name only, Python `get_actor_bounds` signature in UE 5.7).

3. **Summarize**
   - List what looks good.
   - Flag potential issues (style, missing error handling, idempotency for new scripts, or KNOWN_ERRORS relevance).
   - Suggest concrete edits only where helpful; avoid nitpicking.

## Scope

This is a light review. For exhaustive code/security/architecture review, recommend `/workflowsreview` (Compound Engineering) or a dedicated review pass.

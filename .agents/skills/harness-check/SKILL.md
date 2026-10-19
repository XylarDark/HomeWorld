---
name: harness-check
description: Use only when the user asks to check, update, or optimize the agent harness, its sources, or its context cost.
---

# Harness check

A general token question stays on [token-efficient-context](../token-efficient-context/SKILL.md). A playtest, a queue, or a named game file does not use this skill.

Check the sources when asked. Do not change a workflow door unless `Tools/Measure-AgentContext.ps1` shows the efficiency, or a host path is already broken. A URL correction in the source list is not a workflow change.

1. Read [docs/tools/HARNESS_SOURCES.md](../../../docs/tools/HARNESS_SOURCES.md) only. Do not open the playtest queue, vision, or `Source/`.
2. Fetch each source’s changelog or first page. Record the date and one sentence of what changed since that file’s last-checked line.
3. Update last-checked, and any moved URL, in that file. That edit does not need a token measurement.
4. Run `.\Tools\Measure-AgentContext.ps1` from the repo root. Record `standingTok`, the Cpp bucket, and `docs/SESSION_NOW.md` bytes.
5. Sort findings into three piles:
   - Host break: a path the launcher uses is gone, the MCP port the clients dial does not match the spec change, or `product-info.json` names a new Rider. Fix that one path. Evidence is the file or the log, not a blog.
   - Efficiency: a smaller standing catalog or a smaller start read. Edit only after a second script run shows the number moved the way claimed. Name both numbers in the reply.
   - Workflow: `Docs/context/SESSION_START.md`, the playtest queue, swarm, or who decides feel. Do not change these unless that second run shows a drop, or Luke says yes in this chat.
6. If a host break was real, add one Cause → Avoid line to `docs/KNOWN_ERRORS.md`. Do not add an `alwaysApply` rule. Stop.

---
name: token-efficient-context
description: Use when the user asks about tokens, credits, context cost, MCP bloat, or editing rules, skills, AGENTS.md, or .cursorignore.
---

# Token-efficient context

Past about 60k tokens, write a handoff and start a fresh chat. Do not carry the thread.

When a lock is scribed, write the handoff in that same reply and stop. Implementation is a new chat from that file. This kind of session interviews and writes the handoff. The implementer is the cheaper chat.

A playtest reply compiles once, with `.\Tools\Safe-Build.ps1 -LaunchEditorAfter` from the repo root. Do not close the editor again for a second fix in the same reply.

`git add` uses the path `git status` prints. `Docs/` and `docs/` are one directory.

Model class is in [docs/human-use/SWARM_MODE_ROUTING.md](../../../docs/human-use/SWARM_MODE_ROUTING.md). Plan with a stronger model, implement with a cheaper one, and verify separately.

---
name: token-efficient-context
description: Use when the user asks about tokens, credits, context cost, MCP bloat, or editing rules, skills, AGENTS.md, or .cursorignore.
---

# Token-efficient context

Use this when the task is context cost, a handoff, a playtest lock, or a long implementation chat. A one-line fix in a path already named does not use it.

Past about 60k tokens, write a handoff and start a fresh chat. Do not carry the thread.

When a lock is scribed, write the handoff in that same reply and stop. The handoff is the sentence just locked, the queue Now line, and the one owner file. Implementation is a new chat from that file. Do not build a mechanic in the chat that is still guessing the interaction. The implementer is the cheaper chat.

A stale handoff is not a start. If it disagrees with the queue Now line, the queue wins. Do not redo a passed beat from an old handoff.

One fact lives in one owner file. The queue names the pass and points at the owner. It does not restate the rule.

A playtest reply compiles once, with `.\Tools\Safe-Build.ps1 -LaunchEditorAfter` from the repo root. Do not close the editor again for a second fix in the same reply. Before that compile, search `docs/KNOWN_ERRORS.md` for the symptom. A material change stays in editor Python.

The check is the named log line. Do not pull the whole editor log, or a wall of screenshots, into the chat.

`git add` uses the path `git status` prints. `Docs/` and `docs/` are one directory.

Model class is in [docs/human-use/SWARM_MODE_ROUTING.md](../../../docs/human-use/SWARM_MODE_ROUTING.md). Plan with a stronger model, implement with a cheaper one, and verify separately. Do not grade your own playtest.

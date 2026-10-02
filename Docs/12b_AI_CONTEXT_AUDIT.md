# AI context audit — 2026-10-02

Same branch as the layout audit. This pass is what an agent pays every turn, not how a human browses the tree.

## Community bar

Vendors converged on the same shape in 2026: a short always-loaded root, skill bodies loaded only when the description matches, long docs pulled by path. Practical cuts people publish:

- Root `AGENTS.md` as a high-density summary, about 50–200 short lines. Past that, extra rules compete with the task. (PromptForge agents-md guide, 2026; Tabular Editor context guide.)
- One always-on rule under ~50 lines, or none. Four or five `alwaysApply: true` files prefix 3,000+ tokens every Composer turn. (Cursor forum, 2026-09-19.) A separate write-up caps all always-apply rules at ~2,000 tokens.
- Cursor’s own harness note (2026-09-23): moving MCP tool schemas out of the static prompt cut tokens 46.9% on sessions that called an MCP tool. Same move on built-in tools cut static tool-description tokens 60%. Load tools when needed.
- Instruction following falls as the window fills. This repo already calls ~60k tokens the dumb zone. Always-loaded text spends that budget before the task starts.

## What this repo already got right

- Accepted decline: always-on context lives in `AGENTS.md` only. The automation rule is `alwaysApply: false` with globs. The body still mentions the old `true` setting; the frontmatter does not.
- Skills exist. Descriptions are the always-loaded part. Bodies should stay deferred.
- `.cursorignore` already drops `Saved/`, `Binaries/`, `Intermediate/`, secrets.
- `token-efficient-context` already says new chat per task and no `@codebase` by default.

## What an agent still pays

| Always-loaded surface | Size | Problem |
| --- | ---: | --- |
| `AGENTS.md` | 190 lines, 26,161 chars, ~3,000 words | Loaded every session. Most of it restates commands and swarm ops that already live in linked docs. |
| Skill descriptions | ~1,900 chars across 10 skills | Cheap. Two descriptions say "any coding task" or "every task", so those bodies (~13k and ~1.8k) load on almost every edit. |
| `20-full-automation-no-manual-steps.mdc` | glob-scoped | Fine. Do not flip it back to always-on. |
| Indexable tree | 2,948 `Content/__ExternalActors__` files | Not in the prompt until search hits them. Then they flood `@codebase` and semantic search. |

Root prompts are worse if someone `@`s them: `HOMEWORLD_MASTER_PROMPT.md` is 11k chars, `HOMEWORLD_MVP_SWARM_BRIEF.md` is 20k. They are not always loaded. They are a footgun.

## Changes in this commit

`.cursorignore` now excludes `Content/__ExternalActors__/` and `Content/__ExternalObjects__/`. That is generated World Partition output. Indexing it cannot answer a gameplay question the map file does not already answer.

## Not done — needs a steer

Do not slim `AGENTS.md` in the same commit. It is the only always-on surface, and a bad cut drops the Safe-Build chain and the steer gate. The cut, when you confirm it, is: keep canon table, engine lock, Safe-Build command, steer-gate paragraph, dumb-zone line, ownership pointer. Move command encyclopedia and swarm ops back to the docs they already link. Target under 100 short lines.

Do not widen skill descriptions. `agent-workflow` ("any coding task") and `steer-gate` ("every task") defeat progressive disclosure. Narrow them to the miss they prevent, and keep the one-line pointer in `AGENTS.md`.

# Cursor cannot: Agent-specific Information (PDF last section)

**Label:** Cursor cannot. **Owner:** Agent, since 2026-10-01 (was: human Steer).

The PDF’s last page is about the model’s incentives and the context window.
Cursor does not enforce those limits from this repository.

Managing its own context and its own flattery is now the agent's job, not a
setting you have to remember to change. The one part that stays yours is the
**client-side** control, because it lives in your Cursor install and not in this
repository.

## What the PDF asked

- **Sycophancy:** agents answer first and flatter by design — disable that as
  soon as possible.
- **Smart zone** roughly below 60k tokens; **dumb zone** above. Stay in the
  smart zone by splitting agents, compacting markdown, new chats, or a HANDOFF
  packet.
- 1M-class windows for research (write out, leave); 200k-class for
  implementation with a tight harness.

## What Cursor actually has

- Model and “personality” / sycophancy controls live in **your Cursor settings**,
  not in `AGENTS.md`. Nothing this repo commits can turn flattery off for every
  user who clones it. The agent can decline to flatter in its own output; it
  cannot change the client default for you.
- Context size is a product limit. The agent can **prefer** a new chat and trim
  tool output ([token-efficient-context](../../../.agents/skills/token-efficient-context/SKILL.md));
  Cursor will not hard-stop a thread at 60k because we asked.
- HANDOFF is an IDE skill (`ce-handoff`) if you have that plugin. It is not
  bundled as a seventh core skill here.

## What the agent does

- Keep its own context in the smart zone: new chat per task, `@file` over
  `@codebase`, never paste folders. If the thread is noisy, summarize and start
  fresh, and write a handoff first.
- Do not flatter to close a thread. Agreement is not evidence.
- Do not add `alwaysApply: true` rules or a seventh skill to "keep the window
  small." That spends the always-on budget the PDF is warning about.

## What stays with the human

Turn down sycophancy / "always agree" in your own Cursor settings if the control
exists on your build. That is a client preference, not a repo decision.

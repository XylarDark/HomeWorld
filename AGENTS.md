# HomeWorld – Agent context

Always loaded. Detail lives in [docs/AGENTS_REFERENCE.md](docs/AGENTS_REFERENCE.md). Do not paste that file back here.

## Canon

| Path | Role |
|------|------|
| [Docs/VISION_BOARD.md](Docs/VISION_BOARD.md) | Product canon. Lone Wanderer; night is a form you become. Read before scoping. |
| [Docs/CANON_MAP.md](Docs/CANON_MAP.md) | Topic index. Start here to find an answer. |
| [START_HERE.md](START_HERE.md) | Swarm entry only. Default coding chats are not swarm. |

`Docs/` and `docs/` are one directory on Windows (DEC-0029). Do not sync them. Do not treat `VisionBoard/MVP/` or `docs/Automation/AGENT_COMPANY.md` as product canon.

## Lock

UE 5.8 only. PC + Steam Early Access. No engine or platform variant without a team decision. C++ for gameplay, movement, input, abilities. Blueprint for content and overrides. Pawn `AHomeWorldCharacter`, game mode `AHomeWorldGameMode`. UE facts from 5.8 docs only — [docs/UE/UE58_TECH.md](docs/UE/UE58_TECH.md), [docs/KNOWN_ERRORS.md](docs/KNOWN_ERRORS.md).

## Steer gate

You cannot take responsibility for a change you cannot explain, you cannot see the playtest, and you cannot decide taste. A clean log is not evidence. Before an edit that sets feel, scope, or done, load [steer-gate](.agents/skills/steer-gate/SKILL.md) and [Docs/handoffs/SLICE_SESSION.md](Docs/handoffs/SLICE_SESSION.md). Name the limitation, numbered options, then stop. Ownership map: [docs/human-use/OWNERSHIP.md](docs/human-use/OWNERSHIP.md).

## Session

Past ~60k tokens, write `Docs/handoffs/SESSION_HANDOFF_<slice>.md` and start a fresh chat from that file plus [docs/SESSION_SUMMARY.md](docs/SESSION_SUMMARY.md). Do not carry the transcript. One significant write at a time. Uncommitted changes you did not make: stop and report.

**End every session with a question.** Run `python Content/Python/session_close.py --notify` before you stop. It derives the critical path from the gate dependency chain, prints the one question to leave the Lead with - a judgment only they can make, labour only they can do, or a confirmation that the agent should keep working - and raises a desktop notification carrying that question. Do not end a session in silence; a session that simply stops leaves the Lead off the critical path.

The notification is harness-agnostic on purpose: it is a Windows toast plus the `grokbot://` protocol handler, neither of which knows which IDE the session ran in. `grokbot://` raises the Grok Bot window and **cannot carry text** - measured from Grok Bot 0.66.0's own bundle, every route parameter is an ID or a closed enum, and `open` takes none. The toast is the channel that carries the question. Use `--no-grokbot` to toast only.

## Build

Agents run `.\Tools\Safe-Build.ps1` only, from repo root. Never `Build-HomeWorld.bat` directly. Chain and MCP port: [docs/Setup/BUILD_POLICY.md](docs/Setup/BUILD_POLICY.md). Cloud agents have no UE.

## Do not re-litigate

- Always-on context is this file. No `alwaysApply: true` rule.
- Do not vendor a second doctor root. `UserHarness/` is the doctor root.
- Do not point `/loop-engineer` at a product decision or a continuity task.
- Index skips `Content/__ExternalActors__/` and `Content/__ExternalObjects__/`.
- Commands, swarm ops, testing, and style: [docs/AGENTS_REFERENCE.md](docs/AGENTS_REFERENCE.md).

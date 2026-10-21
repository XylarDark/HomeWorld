# HomeWorld – Agent context

Always loaded. Detail lives in [docs/AGENTS_REFERENCE.md](docs/AGENTS_REFERENCE.md). Do not paste that file back here.

## Canon

| Path | Role |
|------|------|
| [Docs/VISION_BOARD.md](Docs/VISION_BOARD.md) | Product canon. Read it before scoping. Do not restate it. |
| [Docs/CANON_MAP.md](Docs/CANON_MAP.md) | Topic index. Start here to find an answer. |
| [START_HERE.md](START_HERE.md) | Swarm entry only. Default coding chats are not swarm. |

`Docs/` and `docs/` are one directory (DEC-0029). There is no second tree. Do not sync the two spellings, and do not describe them as a split. Do not treat `VisionBoard/MVP/` or `docs/Automation/AGENT_COMPANY.md` as product canon.

## Lock

UE 5.8 only. PC + Steam Early Access. No engine or platform variant without a team decision. C++ for gameplay, movement, input, abilities. Blueprint for content and overrides. Pawn `AHomeWorldCharacter`, game mode `AHomeWorldGameMode`. UE facts from 5.8 docs only — [docs/UE/UE58_TECH.md](docs/UE/UE58_TECH.md), [docs/KNOWN_ERRORS.md](docs/KNOWN_ERRORS.md).

## Steer gate

You cannot take responsibility for a change you cannot explain, you cannot see the playtest, and you cannot decide taste. A clean log is not evidence. Before an edit that sets feel, scope, or done, load [steer-gate](.agents/skills/steer-gate/SKILL.md) and [Docs/handoffs/SLICE_SESSION.md](Docs/handoffs/SLICE_SESSION.md). Name the limitation, numbered options, then stop. Ownership map: [docs/human-use/OWNERSHIP.md](docs/human-use/OWNERSHIP.md).

## Session

Start every session from [Docs/context/SESSION_START.md](Docs/context/SESSION_START.md).

A request to test, reach, or fast-forward to a beat is `hw.Playtest.FastForward` plus the words used. The procedure is the playtest reply in that file.

Past ~60k tokens, write `Docs/handoffs/SESSION_HANDOFF_<slice>.md` and start a fresh chat from that file plus [docs/SESSION_NOW.md](docs/SESSION_NOW.md). Do not carry the transcript. Do not open `docs/history/SESSION_LOG.md` to start. One significant write at a time. Uncommitted changes you did not make: stop and report.

Do not report a scene done until its verify script has logged the pass in the open editor. The rule is in [Docs/context/SCENE_SETUP.md](Docs/context/SCENE_SETUP.md).

Legacy files in `Docs/handoffs/` are not a read list. Open a handoff only when this task names that file, or open the newest `SESSION_HANDOFF_*.md` when starting from a handoff. Do not search that folder for canon. Open a design or studio research file only when the task is explicitly that research, and then only the one topic file named in [Docs/handoffs/RESEARCH_PROMPT_CONTRACT.md](Docs/handoffs/RESEARCH_PROMPT_CONTRACT.md). Open [Docs/canon/DESIGN_ETHOS.md](Docs/canon/DESIGN_ETHOS.md) only when auditing a mechanic, an environment, or a progression step.

## Locks

Lead's locks. Never `git reset --hard`. Never commit a `.uasset` or `.umap` without Lead's yes. Never close or kill `UnrealEditor` without Lead's yes (`Safe-Build.ps1` taskkills it). Lead grants standing merge permission, docs and Source, after the tests pass. Leave Lead's uncommitted desktop files alone.

## Build

Agents run `.\Tools\Safe-Build.ps1` only, from repo root. Never `Build-HomeWorld.bat` directly. Chain and MCP port: [docs/Setup/BUILD_POLICY.md](docs/Setup/BUILD_POLICY.md). Cloud agents have no UE.

Editor work uses UnrealMCP on port 55557. A log line `editor_ui: NEED_SLATE` opens [.agents/skills/ue-editor-ui/SKILL.md](.agents/skills/ue-editor-ui/SKILL.md).

## Do not re-litigate

- Always-on context is this file. No `alwaysApply: true` rule.
- Do not vendor a second doctor root. `UserHarness/` is the doctor root.
- Do not point `/loop-engineer` at a product decision or a continuity task.
- Index skips `Content/__ExternalActors__/` and `Content/__ExternalObjects__/`.
- Commands, swarm ops, testing, and style: [docs/AGENTS_REFERENCE.md](docs/AGENTS_REFERENCE.md).

## Rider MCP

Open only for a C++ symbol, diagnostic, or refactor: [Docs/tools/Rider_MCP_for_UE_Games.md](Docs/tools/Rider_MCP_for_UE_Games.md) § Selective usage guidance. Never call `safe_delete` without `--preview true`; without it the tool deletes.

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

Past ~60k tokens, write `Docs/handoffs/SESSION_HANDOFF_<slice>.md` and start a fresh chat from that file plus [docs/SESSION_SUMMARY.md](docs/SESSION_SUMMARY.md). Do not carry the transcript. One significant write at a time. Uncommitted changes you did not make: stop and report.

Do not report a scene done until its verify script has logged the pass in the open editor. The rule is in [Docs/context/SCENE_SETUP.md](Docs/context/SCENE_SETUP.md).

Legacy files in `Docs/handoffs/` are not a read list. Open a handoff only when this task names that file, or open the newest `SESSION_HANDOFF_*.md` when starting from a handoff. Do not search that folder for canon.

## Build

Agents run `.\Tools\Safe-Build.ps1` only, from repo root. Never `Build-HomeWorld.bat` directly. Chain and MCP port: [docs/Setup/BUILD_POLICY.md](docs/Setup/BUILD_POLICY.md). Cloud agents have no UE.

Editor work uses UnrealMCP on port 55557. A log line `editor_ui: NEED_SLATE` opens [.cursor/skills/ue-editor-ui/SKILL.md](.cursor/skills/ue-editor-ui/SKILL.md).

## Do not re-litigate

- Always-on context is this file. No `alwaysApply: true` rule.
- Do not vendor a second doctor root. `UserHarness/` is the doctor root.
- Do not point `/loop-engineer` at a product decision or a continuity task.
- Index skips `Content/__ExternalActors__/` and `Content/__ExternalObjects__/`.
- Commands, swarm ops, testing, and style: [docs/AGENTS_REFERENCE.md](docs/AGENTS_REFERENCE.md).

## Rider MCP (selective use)
- Use native file/shell tools (read/edit/grep/git/shell) for routine reading, editing, searching, and Git operations in Cursor/OpenCode.
- Use Rider MCP selectively for semantic symbol search, Blueprint-inheritance lookup (`get_class_hierarchy --baseClass`), UE reflection/UHT diagnostics, and refactoring. It has **no usages search and no C++ call hierarchy**: `find_usages`/`find_implementations` do not exist in this build at all, and `analyze_calls` resolves nothing in C++. Use `rg` for callers.
- Do not use Rider MCP for operations native tools can do equally well.
- After C++ changes, check relevant Rider diagnostics. Run UBT when compilation validation is warranted (Safe-Build stays the compile).
- Avoid repeated full builds, redundant validation, and excessive tool calls for small changes.
- For substantial gameplay changes, verify observable behavior via focused tests or Unreal Editor execution.
- Rider MCP is Rider's own built-in server, reached at `http://127.0.0.1:64342/stream` (streamable) or `/sse` (legacy SSE). Start it with `.\Tools\Start-RiderMcp.ps1`; stop it with `-Stop`. Do **not** use `@jetbrains/mcp-proxy` — it probes `/api/mcp/list_tools`, which no Rider 2026.2 install contains. Every tool call needs `rootFolder=C:/dev/HomeWorld`; MCP roots do not substitute. File edits and shell stay on Cursor/OpenCode; UnrealMCP stays on 55557.
- Two environment prerequisites, or the server connects and every symbol query answers empty: UE 5.8 registered at `HKLM\SOFTWARE\EpicGames\Unreal Engine\5.8\InstalledDirectory`, and a .NET 10 runtime under `%USERPROFILE%\.dotnet` — UE 5.8's UnrealBuildTool is net10.0, and the machine-wide dotnet already having 10.x is *not* enough, because Rider prefers the user-local host. `Start-RiderMcp.ps1` preflights the .NET half and prints the install command.
- Trust the tools, not the connection: `search_symbol`/`search_text`/`search_file`/`get_file_problems` are the ones verified on HomeWorld C++. `search_file`'s `q` is a glob. `get_symbol_info` and `analyze_calls` resolve nothing in C++ yet, whatever the argument shape. The default whitelist exposes 32 tools; `-AllowedTools '*'` exposes 86 (including `rename_refactoring` and the debugger) but also shell and file-write tools, so it is opt-in. Rationale: [docs/tools/Rider_MCP_for_UE_Games.md](docs/tools/Rider_MCP_for_UE_Games.md).
- Reference: [docs/tools/Rider_MCP_for_UE_Games.md](docs/tools/Rider_MCP_for_UE_Games.md), [docs/handoffs/MARKETPLACE_POLICY_V1.md](docs/handoffs/MARKETPLACE_POLICY_V1.md).

Today's date: Thu Oct 15 2026

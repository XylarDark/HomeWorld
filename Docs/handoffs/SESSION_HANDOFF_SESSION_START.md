# SESSION_HANDOFF_SESSION_START

Slice: session-start tool calls and skills. Not a playtest beat.
Canon checked: `docs/tools/HARNESS_SOURCES.md` on 2026-10-21. Vision was not opened.
Job confirmed: test. This chat does not declare the pipeline done.
Scenarios the human accepted: optimize the start path for tool calls and skills, then let the next chat validate it.
Changed paths:
- `docs/tools/HARNESS_SOURCES.md` (last checked 2026-10-21)
- `docs/KNOWN_ERRORS.md` (Rider root URI row)
- `Tools/Measure-AgentContext.ps1` (2026-10-21 numbers in the comment)
- `docs/SESSION_NOW.md` (this block is the newest)
- this file
Evidence: see the table. Human play: not this slice.
Disclosed / not verified: `~/.agents/skills` is loaded again (26 skills, 1398 tok). It was parked on 2026-10-19. This chat did not move it. Mixar answered with an empty filepath, so no blend file was open. The working tree already had playtest and source edits; they were not touched.
Do not redo: the `ECONNREFUSED` restart. Quit Cursor only if a new log line is `ECONNREFUSED` and the port is not listening.
Next action: run the check below. Then the game task is the playtest prep block in `docs/SESSION_NOW.md`.

## Check

Editor, Rider, and Mixar stay up. Do not toggle MCP. Do not edit `Docs/context/SESSION_START.md` or `Content/Python/check_session_start.py` unless the checker fails. Both are already dirty.

1. `python Content/Python/check_session_start.py` prints `SESSION_START door check: pass`.
2. `.\Tools\Measure-AgentContext.ps1` from the repo root. Compare `standingTok` 4624, Cpp bucket 3804, and `docs/SESSION_NOW.md` bytes. A move needs a second run that shows the new number. Do not park `~/.agents/skills` unless Luke says those 26 skills leave standing context.
3. One read-only call on each server. Pass happens only when the result is the one named here.

| Server | Call | Pass |
|---|---|---|
| rider | `get_solution_projects` with `rootFolder` `C:/dev/HomeWorld` | a module list. The log line `Root URI must start with 'file://'` is the known handshake, not a failed call |
| unrealEditorUi | `list_toolsets` | `SlateInspectorToolset` |
| unreal-engine-skills | `unreal-engine-skills-manager` `search`, query `editor python`, limit 1 | id `ue-editor-scripting-and-python` |
| mixar | `get_blendfile_summary_path_info` | `status` ok. An empty filepath is an open server with no file |
| unrealMCP | `execute_console_command` `py print('hw-session-start-probe')` | `Saved/Logs/HomeWorld.log` contains `LogPython: hw-session-start-probe` |

## This chat, 2026-10-21 13:40

| Check | Result |
|---|---|
| Door checker | pass |
| Measure | standingTok 4624, Cpp 3804, SESSION_NOW 2612 bytes before this handoff |
| Rider connect 13:24:23 | stream connected, then `-32700` on root `c:\dev\HomeWorld`. `get_solution_projects` still returned modules |
| Slate `list_toolsets` | `SlateInspectorToolset` |
| Skills search `editor python` | `ue-editor-scripting-and-python` |
| Mixar path info | `status` ok, filepath empty |
| UnrealMCP probe | log line `[2026.10.21-17.40.00:382] LogPython: hw-session-start-probe` |

Harness sources since 2026-10-19: no URL moved. MCP `2026-07-28` deprecates Roots and says to pass the directory as a tool argument. Cursor still sends a Windows path. Rider rejects it. Claude Code v2.1.306 fixed a false "prompt is too long" when many MCP tools are loaded. That fix is not this editor.

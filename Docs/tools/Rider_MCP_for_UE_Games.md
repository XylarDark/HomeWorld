# Rider MCP + Cursor/OpenCode + Unreal Engine - Setup Guide

This document captures the specification from `C:\Users\User\Documents\Rider_MCP_for_UE_Games.pdf`, HomeWorld's policy alignment, and the **verified** state of the working setup as of 2026-10-15.

## Recommendation
Enable Rider MCP, but use it selectively rather than routing every operation through the IDE.

## Division of responsibilities
- **Cursor/OpenCode** — implementation, file editing, reasoning, and orchestration.
- **Rider MCP** — semantic code intelligence, Unreal-specific diagnostics, symbol navigation, and refactoring.
- **Unreal Build Tool (UBT)** — authoritative compilation results.
- **Unreal Editor** — runtime and gameplay verification.

## Where Rider MCP helps (Unreal C++)
- Semantic symbol search (declarations vs text matches)
- Find usages / call hierarchy (traces dependencies)
- Code inspections (C++ and Unreal-aware warnings)
- UHT diagnostics (reflection/metadata issues)
- Refactoring (safer symbol-aware changes)
- Build/run configurations (uses existing Rider configs)
- File read/edit/terminal mostly duplicate native Cursor/OpenCode tools (use native when possible)

## JetBrains rider-skills (reference)
Official: https://github.com/JetBrains/rider-skills

Key skills:
- `ue-code-authoring` — UE C++ with IDE intelligence/diagnostics (High)
- `navigating-code` — Semantic references/symbols (High)
- `refactoring-code` — Safer symbol-aware changes (High)
- `ue-live-debugging` — Runtime/crash investigation (High)
- `ue-test-authoring` — Unreal automation tests (Medium)

## Intended model
Use native tools for routine editing; use Rider MCP for semantic questions, diagnostics, and supported build actions. The two paths complement each other.

## Verified state (2026-10-15)

| Item | State |
|------|-------|
| Rider IDE | Installed via winget — **JetBrains Rider 2026.2.1** (spec needs >= 2025.2) |
| Transport | Rider's **own** MCP server, reached directly over HTTP. **Streamable: `http://127.0.0.1:64342/stream`** (POST, verified `initialize` -> 200). Legacy SSE also live at `/sse` (GET only; POST returns 405). |
| Proxy package | `@jetbrains/mcp-proxy@1.8.0` is **abandoned — it does not work with Rider 2026.2.** See "Why not the proxy" below. |
| Cursor wiring | `.cursor/mcp.json` -> `rider` entry `{ "url": "http://127.0.0.1:64342/stream" }` (live config is gitignored) |
| OpenCode wiring | `opencode.json` -> `mcp.servers.rider`, `type: remote`, `url: http://127.0.0.1:64342/stream` |
| Codex | Not used by this team; `.codex/config.toml` carries the same URL only so the file is not misleading |
| Skills | `ue-code-authoring`, `navigating-code`, `refactoring-code`, `ue-live-debugging`, `ue-test-authoring` vendored to `.agents/skills/` and `.cursor/skills/` |
| Launcher | `Tools\Start-RiderMcp.ps1` — starts the headless server, applies the tool whitelist, waits for the port, and supports `-Stop` / `-Status` |
| Rider MCP Server (GUI) | Enabled in `%APPDATA%\JetBrains\Rider2026.2\options\mcpServer.xml` (`enableMcpServer=true`, `mcpServerPort=64342`, `enableBraveMode=false`) |
| Confirmations | Command execution confirmation stays enabled (brave mode off) |
| Tool exposure | Whitelist enforced: **32 tools** exposed (31 semantic/diagnostic/refactoring/UE + router). Shell, build, and file-write tools are refused by the server. |

## How it actually works (verified, not from the spec)

### The proxy is dead; connect to Rider directly
- `@jetbrains/mcp-proxy@1.8.0` is the newest published version (2025-03-26) and predates Rider's native MCP server. It probes `http://<host>:<port>/api/mcp/list_tools` on ports 63342-63352.
- No file in `C:\Program Files\JetBrains\JetBrains Rider 2026.2.1` contains that route (verified by scanning every jar in the install), so the proxy always answers `failed: No working IDE endpoint available.`
- Do **not** set `IDE_PORT`; it only steers the dead probe.
- Rider 2026.2 serves MCP itself:
  - streamable HTTP: `POST http://127.0.0.1:64342/stream` -> `200`, full `initialize` result
  - legacy SSE: `GET http://127.0.0.1:64342/sse`, with client messages `POST`ed to `/message?sessionId=<uuid>`
  - `POST /sse` -> `405`, `POST /mcp` -> `404`, `POST /api/mcp` -> `404`
  - `63342` is the IDE's built-in web server (`/api/about` -> `200`), unrelated to MCP
- Client config is therefore a plain URL. No proxy, no bridge, no stdio.

### Starting it
`.\Tools\Start-RiderMcp.ps1` starts the headless server (`rider64.exe mcpServer --project=HomeWorld.uproject --port=64342 --allowed-tools=<list> --invocation-mode=direct`), waits until the port answers, and prints the URL. `-Stop` stops only the headless session and leaves a GUI Rider alone. Rider logs to `idea.log` and never to the console, so the script uses a real TCP connect as its success test.

A GUI Rider with `mcpServer.xml` enabled serves the same port, so GUI and headless cannot both run. The script prefers whichever already holds the port.

`-Project` overrides what is opened; the default is `HomeWorld.uproject`. The script also preflights the .NET 10 requirement described below and warns with the fix commands rather than letting the model come back empty.

### Every call needs `rootFolder`
The server refuses with *"Unable to determine the target project for the current MCP tool call"* unless the call carries `rootFolder=C:/dev/HomeWorld`. Declaring MCP **roots** does not help — the server asks for `roots/list`, then still demands the parameter (verified). The vendored skills do not mention this; agents must add it.

### Tool exposure (whitelist is real, and enforced)
`--allowed-tools` absent means a silent read-only default: `search_file, search_text, search_regex, search_symbol` only (logged as `MCP tools whitelist (default): ...`). `--allowed-tools=*` means *whitelist disabled* (all 86 tools registered by the plugins).

`Start-RiderMcp.ps1` passes an explicit 48-name whitelist. **32** of them are actually exposed; the whitelist removes the shell, build, run-config, raw file-write and DB/profiler tools, confirmed by asking the server for an unknown tool and reading its `Available tools:` reply.

- Exposed (32): the four `search_*` tools, `get_symbol_info`, `analyze_calls`, `get_class_hierarchy`, `find_default_value_overrides`, `findTests`, `get_solution_projects`, `get_project_dependencies`, `get_file_problems`, `get_project_problems`, `lint_files`, `safe_delete`, `extract_method`, `extract_interface`, `extract_base_class`, `change_api_signature`, `move_type_to_namespace`, `reorganize_namespaces`, `post_edit_quality_check`, `run_inspection_kts`, `generate_inspection_kts_examples`, `generate_inspection_kts_api`, `ue_health`, `ue_status`, `ue_get_logs`, `get_asset_properties`, `search_assets`, `search_tags`.
- Blocked and confirmed absent: `execute_terminal_command`, `execute_run_configuration`, `build_solution_start`, `build_solution_state`, `create_new_file`, `apply_patch`, `read_file`, `list_directory_tree`, `open_file_in_editor`, `reformat_file`, `ue_execute_python`, plus the SQL/Unity/dotTrace families.
- **Not available in this build, for any whitelist or invocation mode:** `rename_refactoring` and all sixteen `xdebug_*` tools. They appear in the all-tools list but never register as usable in a headless session. Rename has no `McpRenameHost` (the other refactorings have hosts); the debugger tools are likewise not hosted. Expose them via a GUI session if they are ever needed.
- `--invocation-mode=direct` is the default here: each tool is listed with its schema. Router mode lists only `execute_tool` and would break the vendored skills, which call tools by name. In router mode `rename_refactoring`/`xdebug_*` are additionally dropped from the routable set.

### Parameter names and call shapes (discovered, not documented)
Rider's own error messages carry the contract, so probe with a deliberately wrong call (e.g. `analyze_calls` without `analysisKind`) and read the reply. A call with no arguments answers with `Missing required parameters: <names>`.

| Tool | Verified shape |
|------|----------------|
| `search_symbol` | `{ q, paths?, include_external?, limit?, rootFolder }` — `include_external: true` reaches engine source (`UGameplayAbility` -> `Engine\Plugins\Runtime\GameplayAbilities\...`) |
| `search_text` / `search_regex` | `{ q, paths?, limit?, rootFolder }` |
| `search_file` | `{ q, ... }` where **`q` is a glob**, not a substring: `**/HomeWorldCharacter.h` -> 1 hit, a bare `HomeWorldCharacter` -> 0 hits |
| `get_file_problems` | `{ filePath (relative to solution root), errorsOnly?, timeout?, rootFolder }` |
| `get_class_hierarchy` | `{ baseClass, limit?, rootFolder }`, e.g. `ACharacter` |
| `get_symbol_info` | `{ filePath, line, column, rootFolder }` — 1-based |
| `analyze_calls` | `{ symbolFqn, analysisKind: "INCOMING_CALLS" \| "OUTGOING_CALLS", depth?, rootFolder }` |
| `get_project_dependencies` | `{ projectName, rootFolder }` — the name must match `get_solution_projects` exactly |

As verified on 2026-10-15, after the two prerequisites above: `search_symbol`, `search_text`, `search_regex`, `search_file`, `get_file_problems`, `get_project_problems` and `get_class_hierarchy` all returned real HomeWorld results. `get_symbol_info` and `analyze_calls` accepted well-formed calls but resolved **nothing in C++** — `get_symbol_info` -> `{"documentation":""}`, and `analyze_calls` -> `No callable symbol found` for `AHomeWorldCharacter`, `AHomeWorldCharacter::BeginPlay` and a class-declaration position alike. Treat those two as .NET/Java-shaped until an engine symbol proves otherwise.

### Prerequisite: two environment fixes, or every semantic call answers empty
An empty Unreal project model makes the MCP surface look broken while it is healthy: `search_symbol` -> `{"items":[],"more":true}`, `get_file_problems` -> `{"errors":[],"timedOut":true}`, `get_solution_projects` -> `Miscellaneous Files` and `&`. Both causes below had to be cleared.

**1. Register UE 5.8 (elevated).** The project sets `"EngineAssociation": "5.8"`, but `HKLM\SOFTWARE\EpicGames\Unreal Engine` held only `4.0`/`5.7` and `LauncherInstalled.dat` only `5.7`, so Rider could not resolve it even though `C:\Program Files\Epic Games\UE_5.8` exists (and `Build-HomeWorld.bat` reaches it by hard-coded path). Fix:

```powershell
# elevated
New-ItemProperty 'HKLM:\SOFTWARE\EpicGames\Unreal Engine\5.8' -Name InstalledDirectory `
    -Value 'C:\Program Files\Epic Games\UE_5.8' -PropertyType String -Force
```

The alternative — a `HKCU\SOFTWARE\Epic Games\Unreal Engine\Builds` key plus a new `EngineAssociation` — edits the tracked `.uproject`, so it needs a team decision. The registry route needs none.

**2. Give Rider's dotnet the .NET 10 runtime.** Rider builds the C++ model by running

`%USERPROFILE%\.dotnet\dotnet.exe "<UE_5.8>\Engine\Binaries\DotNET\UnrealBuildTool\UnrealBuildTool.dll" -Mode=QueryTargets -Output=<proj>\Intermediate\TargetInfo.<Target>.json`

and UE 5.8's `UnrealBuildTool.dll` is a **net10.0** app. `C:\Users\User\.dotnet` had only .NET 8.0.32, so the child exited `0x80008096` with *"You must install or update .NET to run this application"*, and `backend.*.log` recorded *"Generating UE4 project model failed. Will return empty project model"*. Note the machine-wide `C:\Program Files\dotnet` **already had** 10.0.12 — Rider prefers `%USERPROFILE%\.dotnet`, so a plain `dotnet --list-runtimes` looks fine while this is broken:

```powershell
Invoke-WebRequest https://dot.net/v1/dotnet-install.ps1 -OutFile "$env:TEMP\dotnet-install.ps1" -UseBasicParsing
& "$env:TEMP\dotnet-install.ps1" -Channel 10.0 -Runtime dotnet -InstallDir "$env:USERPROFILE\.dotnet"
```

`Tools\Start-RiderMcp.ps1` preflights this and warns with the same commands.

**What it was not.** Not the transport, not the whitelist, and not `.uproject` vs `.sln`. With the runtime present, opening the `.uproject` logs `UnrealHost - Unreal solution has been opened as .uproject`, Rider invokes UBT `-Mode=QueryTargets` for `Engine` and `HomeWorld` by itself, exit code 0, and no `-projectfiles` step is needed. A `.sln` also works but needs an explicit `Build.bat -projectfiles` run first and pulls ~2500 engine `.Build.cs` modules into the model.

## Exposed tool policy

Keep semantic and diagnostic tools. Turn off the ones that duplicate native Cursor/OpenCode tools or the UBT compile.

**Keep enabled:** `search_symbol`, `analyze_calls`, `get_symbol_info`, `get_file_problems`, `lint_files`, `search_file`, `search_regex`, `search_text`, `get_project_dependencies`, `get_solution_projects`, `get_class_hierarchy`, `find_default_value_overrides`, `findTests`, `safe_delete`, `extract_method`, `extract_interface`, `extract_base_class`, `change_api_signature`, `move_type_to_namespace`, `reorganize_namespaces`, `post_edit_quality_check`, `run_inspection_kts`, `ue_health`, `ue_status`, `ue_get_logs`, `get_asset_properties`, `search_assets`, `search_tags`

**Disable:** `execute_terminal_command` (shell stays on Cursor/OpenCode), `create_new_file`, `apply_patch`, `read_file`, `list_directory_tree` and `open_file_in_editor` (file reads/writes stay on Cursor/OpenCode), `build_solution_start` / `build_solution_state` and `execute_run_configuration` (compile stays on `Tools\Safe-Build.ps1`), `ue_execute_python`, `git_status`, `get_repositories`, `reformat_file`

All of this is applied by `Tools\Start-RiderMcp.ps1`; the GUI equivalent is Settings -> Tools -> MCP Server -> Exposed Tools.

## JetBrains skills installation (Cursor/OpenCode)
JetBrains' `rider-skills` ships Claude Code and Codex plugin manifests only. Cursor/OpenCode use the plain `SKILL.md` layout, so the five skills named in the spec were copied from a shallow clone of `https://github.com/JetBrains/rider-skills` into both skill roots this repo already uses:

- `.agents/skills/<skill>/` — read by OpenCode and other SKILL.md-aware agents
- `.cursor/skills/<skill>/` — referenced by `AGENTS.md` and listed in `opencode.json` (`skills: [".cursor/skills"]`)

Each skill folder carries `SKILL.md`, `metadata.json`, and a `reference/` directory with the tool contracts. Two gaps to remember when following them: add `rootFolder` to every call, and do not rely on `rename_refactoring` or `xdebug_*` until a GUI session provides them.

## Selective usage guidance (to add to AGENTS.md)
- Use native file/shell tools (read/edit/grep/git/shell) for routine reading, editing, searching, Git operations in Cursor/OpenCode.
- Use Rider MCP selectively for semantic symbol navigation, actual usages, call hierarchy, UE reflection/UHT diagnostics, and complex refactoring.
- Do not use Rider MCP for operations native tools can do equally well.
- After C++ changes, check relevant Rider diagnostics. Run UBT when compilation validation is warranted.
- Avoid repeated full builds, redundant validation, and excessive tool calls for small changes.
- For substantial gameplay changes, verify observable behavior via focused tests or Unreal Editor execution.

## Verification evidence (2026-10-15)
- `opencode mcp list` -> `✗ rider failed: No working IDE endpoint available.` (proxy), then after switching to the URL -> `✓ rider connected`.
- `POST http://127.0.0.1:64342/stream` with `initialize` -> `200`, `serverInfo {"name":"JetBrains Rider MCP Server","version":"2026.2.1"}`.
- Through OpenCode: `rider.get_solution_projects({rootFolder:"C:/dev/HomeWorld"})` -> `{"modules":[{"name":"Miscellaneous Files",...},{"name":"&",...}]}`; `rider.ue_health` -> `{"connected":false}`.
- Unknown-tool probe -> `Available tools:` lists exactly the 32 exposed names above.
- Failure signature before the .NET fix (`backend.*.log`): *"UnrealBuildTool: You must install or update .NET to run this application"*, exit `0x80008096`, *"Generating UE4 project model failed. Will return empty project model"*.
- Fix signature after (`backend.*.log`): `UnrealBuildTool: Written <proj>\Intermediate\TargetInfo.HomeWorld.json`, exit `ERRORLEVEL 00000000h`, `Finished generating target info`.
- Through OpenCode, headless, on this repo, after both prerequisites:
  - `search_symbol { q: "AHomeWorldCharacter" }` -> `HomeWorldCharacter.h`, `HomeWorldCharacter.cpp`
  - `search_symbol { q: "HomeWorldSpirit", limit: 5 }` -> wisp, lit volume, heal component, burst ability, stealth types headers
  - `search_file { q: "**/HomeWorldCharacter.h" }` -> 1 hit; `search_file { q: "Source/**/*.h" }` -> real hits
  - `search_regex { q: "UCLASS[\\s\\S]{0,80}class HOMEWORLD_API (A\\w+)" }` -> real hits per actor header
  - `search_symbol { q: "UGameplayAbility", include_external: true }` -> engine `GameplayAbility.h` etc.
  - `get_file_problems { filePath: "Source/HomeWorld/HomeWorldCharacter.h" }` -> `{"errors":[]}`, no timeout
  - `get_project_problems` -> `{"totalCount":0}`
  - `get_class_hierarchy { baseClass: "ACharacter" }` -> real entries
  - `get_solution_projects` -> full Unreal tree (`Miscellaneous Files`, `&`, `Engine`, `Plugins`, `Paper2D`, `AISupport`, ... `HomeWorld`)

## Verdict (qualitative)
- Unreal-specific code intelligence: High value
- Acceleration of straightforward implementations: Modest value

## References
- https://github.com/JetBrains/rider-skills
- https://www.jetbrains.com/help/rider/mcp-server.html
- Launcher: `Tools/Start-RiderMcp.ps1`
- HomeWorld policy: `docs/handoffs/MARKETPLACE_POLICY_V1.md`

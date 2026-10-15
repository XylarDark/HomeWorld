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
- Find usages / call hierarchy (traces dependencies) — **not for C++ in this build**: `find_usages` and `find_implementations` are absent, and `analyze_calls` resolves nothing. Use `rg`, or `rename_refactoring --preview` where a rename is admissible.
- Code inspections (C++ and Unreal-aware warnings)
- UHT diagnostics (reflection/metadata issues)
- Refactoring (safer symbol-aware changes)
- Build/run configurations (uses existing Rider configs) — **not exposed here**; the build stays `.\Tools\Safe-Build.ps1`.
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
`--allowed-tools` absent means a silent read-only default: `search_file, search_text, search_regex, search_symbol` only (logged as `MCP tools whitelist (default): ...`). `--allowed-tools=*` means *whitelist disabled* — **86** tools register.

`Start-RiderMcp.ps1` passes an explicit **31-name** whitelist, which exposes **32** tools: those 31 plus `execute_tool`, which is always present and *is* present in `direct` mode (correcting an earlier claim here). The whitelist removes the shell, build, run-config, raw file-write and DB/profiler/Unity families, confirmed by asking the server for an unknown tool and reading its `Available tools:` reply.

- Exposed (32): `search_symbol`, `search_file`, `search_text`, `search_regex`, `get_symbol_info`, `analyze_calls`, `get_class_hierarchy`, `find_default_value_overrides`, `findTests`, `get_solution_projects`, `get_project_dependencies`, `get_file_problems`, `get_project_problems`, `lint_files`, `safe_delete`, `extract_method`, `extract_interface`, `extract_base_class`, `change_api_signature`, `move_type_to_namespace`, `reorganize_namespaces`, `post_edit_quality_check`, `run_inspection_kts`, `generate_inspection_kts_examples`, `generate_inspection_kts_api`, `ue_health`, `ue_status`, `ue_get_logs`, `get_asset_properties`, `search_assets`, `search_tags`, `execute_tool`.
- **Absent in *both* modes — this build does not contain them at all.** The disabled-whitelist surface is 86 tools and neither `find_usages` nor `find_implementations` is among them. The vendored `navigating-code` skill is built on those two, so it cannot work as written; use `search_text`/`search_regex` for references and `get_class_hierarchy` for Blueprint inheritance.
- Blocked by the whitelist (in the build, deliberately kept out): `execute_terminal_command`, `execute_run_configuration`, `build_solution_start`, `build_solution_state`, `create_new_file`, `apply_patch`, `read_file`, `list_directory_tree`, `open_file_in_editor`, `reformat_file`, `git_status`, `get_repositories`, `ue_execute_python`, `spawn_actor`, `viewport_camera`, `take_screenshot`, `ue_import_blueprint_nodes`, `ue_export_blueprint_nodes`, plus the SQL/Unity/dotTrace families.

#### `rename_refactoring` and `xdebug_*`: reachable, but not by any whitelist
These seventeen tools **do work headless**. A preview `rename_refactoring` on `AHomeWorldCharacter` returned `{"ok":true,"applied":false,"touched":0,"affects":{"files":37,"callSites":327}}`, and `xdebug_get_debugger_status` returned `{"sessions":[]}`. An earlier revision of this document called them "not available in this build, for any whitelist or invocation mode" and blamed a missing `McpRenameHost`. That was wrong; the error came from reading only whitelisted sessions.

They are simply **not addressable by name**, because `--allowed-tools` is compiled into a glob mask with every CSV entry wrapped as `+*.<name>`:

```
--allowed-tools=search_symbol,rename_refactoring
  -> MCP tools whitelist: search_symbol, rename_refactoring
     (mask: -*,+*.search_symbol,+*.rename_refactoring)
```

`+*.search_symbol` matches; `+*.rename_refactoring` never does — not at +5s, +125s or +245s after the port opened, and not with a three-name list either (that run exposed only `search_symbol` and `execute_tool`). Raw mask syntax cannot help because the starter rewraps it: `-*,+*rename_refactoring` becomes `+*.+*rename_refactoring`. **No `--allowed-tools` value admits them.**

The only route is `-AllowedTools '*'`, which together with them exposes `execute_terminal_command`, `apply_patch`, `read_file`, `create_new_file`, `ue_execute_python` and `git_status` — exactly the shell and file-write surface this project keeps on Cursor/OpenCode. The default whitelist therefore knowingly gives up C++ rename and the live debugger; that trade-off is a policy call, not a technical limit.


### Parameter names and call shapes (discovered, not documented)
Rider's own error messages carry the contract, so probe with a deliberately wrong call (e.g. `analyze_calls` without `analysisKind`) and read the reply. A call with no arguments answers with `Missing required parameters: <names>`.

| Tool | Verified shape |
|------|----------------|
| `search_symbol` | `{ q, paths?, include_external?, limit?, rootFolder }` — `include_external: true` reaches engine source (`UGameplayAbility` -> `Engine\Plugins\Runtime\GameplayAbilities\...`) |
| `search_text` / `search_regex` | `{ q, paths?, limit?, rootFolder }` |
| `search_file` | `{ q, ... }` where **`q` is a glob**, not a substring: `**/HomeWorldCharacter.h` -> 1 hit, a bare `HomeWorldCharacter` -> 0 hits |
| `get_file_problems` | `{ filePath (relative to solution root), errorsOnly?, timeout?, rootFolder }` |
| `get_class_hierarchy` | `{ baseClass, limit?, rootFolder }` — returns **Blueprint assets that inherit the C++ class**, walking the whole chain; it is *not* a C++ subclass tree. `AHomeWorldCharacter` -> `BP_HomeWorldCharacter_C` at `Content/HomeWorld/Characters/BP_HomeWorldCharacter.uasset`. `search_assets { baseClass }` returns the same fact. |
| `get_symbol_info` | `{ filePath, line, column, rootFolder }` — 1-based |
| `analyze_calls` | `{ symbolFqn, analysisKind: "INCOMING_CALLS" \| "OUTGOING_CALLS", depth?, rootFolder }` |
| `get_project_dependencies` | `{ projectName, rootFolder }` — the name must match `get_solution_projects` exactly |

As verified on 2026-10-15, after the two prerequisites above: `search_symbol`, `search_text`, `search_regex`, `search_file`, `get_file_problems`, `get_project_problems` and `get_class_hierarchy` all returned real HomeWorld results. `get_symbol_info` and `analyze_calls` accepted well-formed calls but resolved **nothing in C++** — `get_symbol_info` -> `{"documentation":""}`, and `analyze_calls` -> `No callable symbol found` for `AHomeWorldCharacter`, `AHomeWorldCharacter::BeginPlay` and a class-declaration position alike. Treat those two as .NET/Java-shaped until an engine symbol proves otherwise.

### Verified behaviour of the rest of the exposed surface (2026-10-15)

| Tool | Verified behaviour on HomeWorld |
|---|---|
| `lint_files` | Real analysis, several files per call: one header -> 3.4 KB of warnings (`WEAK WARNING` items). **Slow: ~14 s for a single header**, so batch deliberately and expect a long call. |
| `search_assets` | UE asset search. `{ baseClass: "AHomeWorldCharacter" }` -> `BP_HomeWorldCharacter.uasset` with its `assetPath`. `{ query: "BP_" }` -> `{"assets":[]}`, so `query` is not an asset-name substring search; prefer `baseClass` or `packagePath`. |
| `search_tags` | `{ prefix, limit?, rootFolder }` -> GameplayTag definitions. `{ prefix: "Ability" }` -> `{"tags":[]}` here (the tags declared in `HomeWorldGameplayTags` are not exposed to it). |
| `get_asset_properties` | `{ assetPath, rootFolder }` -> reads UPROPERTY values / the CDO of a `.uasset` without opening the editor. Not yet exercised: it needs a real `Content/**` path. |
| `ue_status` | **`{"connected":false}`** — a one-stop editor + PIE + log read, but the bridge only answers when a UE editor with RiderLink is running. `ue_health` returns the same, and `ue_get_logs` then reads nothing. |
| `findTests` | `{ className?, classNamespace?, filePath?, ... }` — C#/NUnit test discovery. It cannot see UE automation tests, so it is dead weight on this project. |
| `post_edit_quality_check` | Built for the Claude Code hook loop: it takes a patch and reports the problems in the files it touched. Useful only when a patch exists; `lint_files` covers the same ground here. |
| `rename_refactoring` | C++ rename, confirmed working with the whitelist disabled: `--preview true` on `AHomeWorldCharacter` -> `affects.files: 37`, `affects.callSites: 327`, `applied: false`. Because a rename must resolve every reference, **the preview doubles as the "find usages" substitute** for the one capability `find_usages` cannot provide here. |

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

"Keep enabled" is a policy statement, not a claim that each one works: `analyze_calls` and `get_symbol_info` stay on only because turning them off buys nothing — both resolve **nothing in C++** here. `findTests` is C#-only, and `rename_refactoring` cannot be whitelisted at all (see above).

**Disable:** `execute_terminal_command` (shell stays on Cursor/OpenCode), `create_new_file`, `apply_patch`, `read_file`, `list_directory_tree` and `open_file_in_editor` (file reads/writes stay on Cursor/OpenCode), `build_solution_start` / `build_solution_state` and `execute_run_configuration` (compile stays on `Tools\Safe-Build.ps1`), `ue_execute_python`, `git_status`, `get_repositories`, `reformat_file`

All of this is applied by `Tools\Start-RiderMcp.ps1`; the GUI equivalent is Settings -> Tools -> MCP Server -> Exposed Tools.

## JetBrains skills installation (Cursor/OpenCode)
JetBrains' `rider-skills` ships Claude Code and Codex plugin manifests only. Cursor/OpenCode use the plain `SKILL.md` layout, so the five skills named in the spec were copied from a shallow clone of `https://github.com/JetBrains/rider-skills` into both skill roots this repo already uses:

- `.agents/skills/<skill>/` — read by OpenCode and other SKILL.md-aware agents
- `.cursor/skills/<skill>/` — referenced by `AGENTS.md` and listed in `opencode.json` (`skills: [".cursor/skills"]`)

Each skill folder carries `SKILL.md`, `metadata.json`, and a `reference/` directory with the tool contracts. Three corrections were applied to the vendored copies on 2026-10-15 — each was true of a normal IntelliJ-platform install and false here:

1. Add `rootFolder: "C:/dev/HomeWorld"` to every call, or the server answers `Unable to determine the target project for the current MCP tool call`.
2. `find_usages` and `find_implementations` **do not exist in this build** — absent from all 86 tools — so the whole `navigating-code` decision table was replaced. Use `search_text`/`search_regex` for references, or `rename_refactoring --preview` where a rename is admissible.
3. `analyze_calls` and `get_symbol_info` resolve nothing in C++, and the `xdebug_*`, `build_solution_*`, `reformat_file`, `ue_play` and `ue_execute_python` steps are unreachable under the default whitelist. `ue-live-debugging` now says so inline, and `refactoring-code` no longer tells the model to retry `rename_refactoring`, which no argument can reach. Both skill roots are kept byte-identical.

## Selective usage guidance (now in `AGENTS.md` and `.cursor/rules/unreal-cpp.mdc`)
- Use native file/shell tools (read/edit/grep/git/shell) for routine reading, editing, searching, Git operations in Cursor/OpenCode.
- Use Rider MCP selectively for semantic symbol search, Blueprint-inheritance lookup (`get_class_hierarchy --baseClass`), UE reflection/UHT diagnostics, and refactoring. It has **no usages search and no C++ call hierarchy**: `find_usages`/`find_implementations` do not exist in this build, and `analyze_calls` resolves nothing in C++. Use `rg` for callers.
- Do not use Rider MCP for operations native tools can do equally well.
- After C++ changes, check relevant Rider diagnostics. Run UBT when compilation validation is warranted.
- Avoid repeated full builds, redundant validation, and excessive tool calls for small changes.

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
- Whitelist mask, read from `idea.log` at launch: `MCP tools whitelist: search_symbol, rename_refactoring` followed by `(mask: -*,+*.search_symbol,+*.rename_refactoring)`. The CSV becomes a `+*.<name>` glob mask, which is why `rename_refactoring` never binds.
- `tools/list` with the whitelist disabled (`-AllowedTools '*'`) -> **86** tools, including `rename_refactoring` and all 16 `xdebug_*`. With the default whitelist -> **32**. Neither `find_usages` nor `find_implementations` appears in either list.
- `rename_refactoring { filePath: "Source/HomeWorld/HomeWorldCharacter.h", symbolName: "AHomeWorldCharacter", preview: true }` (whitelist disabled) -> `{"ok":true,"applied":false,"touched":0,"affects":{"files":37,"callSites":327},"files":[...]}` in 2.9 s.
- `xdebug_get_debugger_status` (whitelist disabled) -> `{"sessions":[]}`.
- `get_class_hierarchy { baseClass: "AHomeWorldCharacter" }` -> `{"classes":[{"name":"BP_HomeWorldCharacter_C","assetPath":"...\\BP_HomeWorldCharacter.uasset"}]}`.
- `search_assets { baseClass: "AHomeWorldCharacter" }` -> the same asset; `search_assets { query: "BP_" }` -> `{"assets":[]}`.
- `search_tags { prefix: "Ability" }` -> `{"tags":[]}`.
- `lint_files { files: ["Source/HomeWorld/HomeWorldCharacter.h"] }` -> 3.4 KB of warnings in ~14 s.
- `ue_status` / `ue_health` -> `{"connected":false}` — no editor is running, so there is no RiderLink session to read.
- Control run with the whitelist cut to `search_symbol,rename_refactoring,xdebug_get_debugger_status`: only `search_symbol` + `execute_tool` live, unchanged at t+5 s, t+125 s and t+245 s. The absence is a mask artefact, not startup timing.
- `Tools/Start-RiderMcp.ps1` preflight, 4/4 cases: registered project -> `C:\Program Files\Epic Games\UE_5.8`; bogus `9.9-nope` -> warns with the elevated fix command; non-`.uproject` -> skipped; registry read confirmed.

## Verdict (qualitative)
- Unreal-specific code intelligence: High value
- Acceleration of straightforward implementations: Modest value

## References
- https://github.com/JetBrains/rider-skills
- https://www.jetbrains.com/help/rider/mcp-server.html
- Launcher: `Tools/Start-RiderMcp.ps1`
- HomeWorld policy: `docs/handoffs/MARKETPLACE_POLICY_V1.md`

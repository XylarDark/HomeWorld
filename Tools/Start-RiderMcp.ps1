# Start-RiderMcp.ps1 - Start the JetBrains Rider MCP server headlessly and wait until it serves.
#
# Rider 2026.2 ships a native MCP server (the `mcpserver` plugin) that listens on its own port
# (default 64342) and serves two transports. Verified against a live install:
#   POST http://127.0.0.1:<Port>/stream -> 200 (streamable HTTP; what Cursor and OpenCode use)
#   GET  http://127.0.0.1:<Port>/sse    -> SSE stream, client messages to /message?sessionId=<uuid>
#   POST /sse -> 405, POST /mcp -> 404, POST /api/mcp -> 404, port 63342 is the IDE web server.
# It is NOT reached through @jetbrains/mcp-proxy: that proxy only probes
# http://127.0.0.1:<63342-63352>/api/mcp/list_tools, and a 2026.2 install contains no such route
# anywhere (verified by scanning every jar in the install). 1.8.0 is also the newest published
# proxy (2025-03-26), so no newer proxy fixes this. Clients dial the server's own URL instead.
#
# Headless mode is the `mcpServer` appStarter argument. Rider prints its own startup banner to
# idea.log (never to the console), so success is decided by an actual TCP connection, not by
# Start-Process having returned.
#
# Tool exposure: without --allowed-tools the headless starter silently applies a read-only
# default of search_file, search_text, search_regex, search_symbol, which hides the analysis,
# diagnostic and refactoring tools this project needs (confirmed in idea.log as
# "MCP tools whitelist (default): ..."). `-AllowedTools` widens that to the semantic set while
# keeping shell / build / raw-file-write tools off, so file edits and builds stay on the agent
# side (Safe-Build.ps1 remains the only compile path). Pass -AllowedTools '*' to expose all 86
# tools instead - that value means "whitelist disabled" to the starter, not a literal tool name.
#
# A GUI Rider with %APPDATA%\JetBrains\Rider2026.2\options\mcpServer.xml enabled serves the
# same port. Like Start-MixarMcp.ps1, this script only ever stops headless instances: the GUI
# may hold unsaved work.
#
# Usage: From project root, .\Tools\Start-RiderMcp.ps1 [-Port 64342] [-AllowedTools <csv>] [-Stop] [-Status]
#
#   -Port:         MCP port, must match what the MCP client dials (default 64342, which is also
#                  what options\mcpServer.xml records for GUI launches).
#   -AllowedTools: Comma-separated tool names to expose through the router. Default is the
#                  semantic set; '*' disables the whitelist and exposes everything.
#   -InvocationMode: 'direct' (default) exposes each allowed tool as its own MCP tool with a
#                  live input schema, which is what the vendored Rider skills call by name.
#                  'via-router' hides them behind execute_tool. Both modes expose the whitelist
#                  plus execute_tool, and execute_tool is present in direct mode as well, so
#                  either call style works without changing this default.
#   -Project:      File to open. Defaults to HomeWorld.uproject - the source of truth, and the
#                  model that works with no extra step. A .sln also works, but only after an
#                  explicit Build.bat -projectfiles run, and it drags ~2500 engine .Build.cs
#                  modules into the model. See the $ProjectDefault comment above.
#   -Stop:         Stop the headless server only; leave any GUI Rider running.
#   -Status:       Report whether the port is reachable and echo the last whitelist/SSE lines
#                  Rider logged, then exit.
#
# Exit code: 0 = reachable (or stopped/quiet as asked); 1 = not reachable / failed to start;
#            2 = Rider not found.

param(
    [int]$Port = 64342,
    [string]$AllowedTools = "",
    [string]$InvocationMode = "direct",
    [string]$Project = "",
    [switch]$Stop,
    [switch]$Status
)

$ErrorActionPreference = "Stop"

$RiderExe = "C:\Program Files\JetBrains\JetBrains Rider 2026.2.1\bin\rider64.exe"
$McpStarter = "mcpServer"
$IdeaLogDir = "$env:LOCALAPPDATA\JetBrains\Rider2026.2\log"

# The two prerequisites that decide whether any of this returns real C++ symbols. Both fail the
# same way - the server connects and answers everything with an empty result - so both are
# preflighted below rather than left to look like a broken MCP surface.
#
# Root cause, read off a frozen failure (idea.log + backend.<ts>.log):
#   For an Unreal project, Rider does not start a compiler. It runs
#       "<USER>\.dotnet\dotnet.exe" "<UE>\Engine\Binaries\DotNET\UnrealBuildTool\UnrealBuildTool.dll"
#           -Mode=QueryTargets -Output=<proj>\Intermediate\TargetInfo.<Target>.json
#   to build the target model, and the C++ feature set is fed from that JSON.
#   UnrealBuildTool in UE 5.8 is a net10.0 app. Where the dotnet Rider picks has no
#   Microsoft.NETCore.App 10.x, the child dies as
#       "You must install or update .NET to run this application"  (exit 0x80008096)
#   and the backend says
#       "Generating UE4 project model failed. Will return empty project model"
#   The MCP server then looks perfectly healthy while search_symbol answers
#   {"items":[],"more":true} and get_file_problems answers {"errors":[],"timedOut":true}.
#   That is the failure this script previously hit. It was not the transport, not the
#   whitelist, and not the choice of .uproject vs .sln.
#   Rider prefers %USERPROFILE%\.dotnet over the machine-wide C:\Program Files\dotnet, so a
#   box can fail here while `dotnet --list-runtimes` in a shell shows 10.x. Installed with:
#       & <dotnet-install.ps1> -Channel 10.0 -Runtime dotnet -InstallDir "$env:USERPROFILE\.dotnet"
#   Test-DotNetPrerequisite() below now warns loudly instead of letting the model come back empty.
#
# Which file: the .uproject is the source of truth and the whole model works from it -
# "UnrealHost - Unreal solution has been opened as .uproject", target info generated for Engine
# and HomeWorld, HomeWorld modules scoped in. A .sln also works but only after an explicit
#     "<UE>_5.8\Engine\Build\BatchFiles\Build.bat" -projectfiles -project=<uproject> -game -rocket
# run, and it drags ~2500 engine .Build.cs modules into the model. Default to the .uproject;
# pass -Project ...\HomeWorld.sln when engine sources are wanted.
$ProjectDefault = (Resolve-Path (Join-Path $PSScriptRoot "..\HomeWorld.uproject")).Path

if (-not $Project) { $Project = $ProjectDefault }

if (-not $AllowedTools) {
    # Semantic navigation, C++/UHT diagnostics, refactoring, UE asset reads. Deliberately absent:
    # execute_terminal_command, execute_run_configuration, build_solution_start/state,
    # create_new_file, apply_patch, read_file, list_directory_tree, open_file_in_editor,
    # reformat_file, git_status, get_repositories, ue_execute_python, ue_play, spawn_actor,
    # viewport_camera, take_screenshot, ue_import/export_blueprint_nodes, plus the SQL/Unity
    # tools this project does not use.
    #
    # `rename_refactoring` and the sixteen `xdebug_*` tools are deliberately NOT named below, and
    # the reason is NOT that this build lacks them - they are present and they work (a preview
    # rename of AHomeWorldCharacter resolved 37 files / 327 call sites; xdebug answered
    # {"sessions":[]}). The reason is that naming them cannot work.
    #
    # `--allowed-tools` is compiled into a glob mask, one `+*.<name>` per CSV entry:
    #     search_symbol,rename_refactoring  ->  -*,+*.search_symbol,+*.rename_refactoring
    # `+*.search_symbol` matches; `+*.rename_refactoring` never matches, at any point after
    # startup, whatever else is in the list. Verified 2026-10-15 with the whitelist cut down to
    # exactly `search_symbol,rename_refactoring,xdebug_get_debugger_status`: only search_symbol
    # registered, still absent 4 minutes later. Passing raw mask syntax does not help either -
    # the launcher rewraps every entry, so `-*,+*rename_refactoring` becomes `+*.+*rename_refactoring`.
    #
    # Those 17 tools are therefore reachable ONLY by disabling the whitelist outright
    # (`-AllowedTools '*'`), which exposes all 86 - including execute_terminal_command,
    # apply_patch, read_file, create_new_file, ue_execute_python and git_status, i.e. exactly the
    # shell and file-write surface this project keeps on Cursor/OpenCode. That is a policy call,
    # not a technical one, so the default stays the safe whitelist and knowingly gives up C++
    # rename and the live debugger. Rationale and the full evidence:
    # docs/tools/Rider_MCP_for_UE_Games.md.
    # Dropped after timing them on HomeWorld C++ (2026-10-15). Each one is still in the 86-tool
    # surface; none of them earns a schema on every turn, and two of them stall the server:
    #   findTests                  empty body at 90s, then the HTTP session is gone. C# tests only.
    #   post_edit_quality_check    empty body at 20s, then the session is gone.
    #   analyze_calls              "No callable symbol found" for AHomeWorldCharacter::BeginPlay.
    #   get_symbol_info            {"documentation":""}.
    #   extract_method, extract_interface, extract_base_class, change_api_signature,
    #   move_type_to_namespace, reorganize_namespaces
    #                              "not found" or a rejected line range on this C++.
    #   run_inspection_kts, generate_inspection_kts_examples, generate_inspection_kts_api
    #                              inspection authoring, not a query.
    #   find_default_value_overrides, get_asset_properties
    #                              {"overrides":[]} / {"properties":[]} with the editor down.
    $AllowedTools = (@(
        # search
        "search_symbol", "search_file", "search_text", "search_regex"
        # navigation that returns HomeWorld results
        "get_class_hierarchy"
        # project model
        "get_solution_projects", "get_project_dependencies"
        # diagnostics (incl. UHT / C++ problems). lint_files is real and slow (~14s per header).
        "get_file_problems", "get_project_problems", "lint_files"
        # refactoring. safe_delete --preview true lists C++ references. rename_refactoring
        # cannot be named in any whitelist; see the note above.
        "safe_delete"
        # UE asset / status reads. Empty and immediate when no editor has RiderLink.
        "ue_health", "ue_status", "ue_get_logs", "search_assets", "search_tags"
        # intentionally not listed: rename_refactoring and the sixteen xdebug_* debugger tools
        # (reachable only with -AllowedTools '*'), plus ue_play / execute_run_configuration /
        # ue_execute_python (UnrealMCP on port 55557, and Safe-Build.ps1 for the build).
    ) -join ",")
}

function Test-DotNetPrerequisite {
    # UnrealBuildTool 5.8 is a net10.0 app and Rider launches it through the user-local
    # $env:USERPROFILE\.dotnet when that host exists, otherwise the dotnet on PATH. A host
    # without a 10.x runtime yields an empty project model and empty symbol results, with no
    # error anywhere a caller would look. Warn here instead.
    $roots = @()
    if ($env:USERPROFILE -and (Test-Path (Join-Path $env:USERPROFILE ".dotnet\dotnet.exe"))) {
        $roots += (Join-Path $env:USERPROFILE ".dotnet")
    }
    $onPath = Get-Command dotnet -ErrorAction SilentlyContinue
    if ($onPath) { $roots += (Split-Path $onPath.Source -Parent) }

    foreach ($root in $roots) {
        $shared = Join-Path $root "shared\Microsoft.NETCore.App"
        if (-not (Test-Path $shared)) { continue }
        $majors = @(Get-ChildItem $shared -Directory -ErrorAction SilentlyContinue |
            ForEach-Object { ($_.Name -split '\.')[0] })
        if ($majors -contains "10") { return $root }
    }

    $tried = if ($roots.Count) { $roots -join ", " } else { "(no dotnet host found)" }
    Write-Warning "No .NET 10 runtime under: $tried"
    Write-Warning "Rider runs UnrealBuildTool (a net10.0 app) through one of those paths, so"
    Write-Warning "UnrealBuildTool will fail and every symbol/problem query will come back"
    Write-Warning "empty while the MCP server still looks connected. Install it user-locally:"
    Write-Warning '  Invoke-WebRequest https://dot.net/v1/dotnet-install.ps1 -OutFile "$env:TEMP\dotnet-install.ps1" -UseBasicParsing'
    Write-Warning '  & "$env:TEMP\dotnet-install.ps1" -Channel 10.0 -Runtime dotnet -InstallDir "$env:USERPROFILE\.dotnet"'
    return $null
}

function Test-UnrealEnginePrerequisite {
    # The other half of the same failure mode, and the half easiest to miss because it lives
    # outside the repo: where the engine version is not registered, Rider produces the exact
    # same empty model as a missing .NET runtime, and the two are indistinguishable from the
    # client (empty symbol results, healthy-looking server).
    #
    # HomeWorld.uproject sets "EngineAssociation": "5.8". Rider resolves a version to a real
    # install via LauncherInstalled.dat and
    #     HKLM\SOFTWARE\EpicGames\Unreal Engine\<version>\InstalledDirectory
    # On this machine the key was absent even though C:\Program Files\Epic Games\UE_5.8 exists,
    # because Build-HomeWorld.bat reaches the engine by hard-coded path and so never needed it.
    param([string]$UProjectPath)

    if (-not $UProjectPath -or $UProjectPath -notlike "*.uproject") { return $null }
    if (-not (Test-Path -LiteralPath $UProjectPath)) { return $null }

    $assoc = $null
    try {
        $assoc = (Get-Content -LiteralPath $UProjectPath -Raw | ConvertFrom-Json).EngineAssociation
    } catch {
        Write-Warning "Could not read EngineAssociation from $UProjectPath; skipping the engine check."
        return $null
    }
    if (-not $assoc) {
        Write-Warning "No EngineAssociation in $UProjectPath; Rider needs one to resolve the engine."
        return $null
    }

    $key = "HKLM\SOFTWARE\EpicGames\Unreal Engine\$assoc"
    $installed = $null
    if (Test-Path "HKLM:\SOFTWARE\EpicGames\Unreal Engine\$assoc") {
        $installed = (Get-ItemProperty -Path "HKLM:\SOFTWARE\EpicGames\Unreal Engine\$assoc" `
            -Name InstalledDirectory -ErrorAction SilentlyContinue).InstalledDirectory
    }

    if (-not $installed) {
        # The registry provider reads the same view as the shell's bitness, so a 32-bit shell can
        # miss a real key. reg.exe does not have that problem; fall back before warning loudly.
        # Native stderr becomes a terminating error under $ErrorActionPreference='Stop', which
        # this script sets, so relax it for this one call and always restore it.
        $prevEap = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        try {
            $out = @(& reg.exe query $key /v InstalledDirectory 2>$null)
        } finally {
            $ErrorActionPreference = $prevEap
        }
        $line = @($out | Where-Object { $_ -match 'InstalledDirectory' })
        if ($line.Count -gt 0 -and ($line[0] -match 'REG_SZ\s+(.+?)\s*$')) { $installed = $Matches[1] }
    }

    if ($installed -and (Test-Path -LiteralPath $installed)) { return $installed }

    Write-Warning "Unreal Engine $assoc is not registered where Rider looks for it."
    if ($installed) {
        Write-Warning "  $key names '$installed', but that path does not exist."
    } else {
        Write-Warning "  $key has no InstalledDirectory value (or the key is missing)."
    }
    Write-Warning "Rider resolves the project's EngineAssociation through that key. Without it the"
    Write-Warning "C++ model is empty: the MCP server connects, then every symbol query answers"
    Write-Warning "empty. Register it from an ELEVATED shell, then relaunch:"
    Write-Warning "  New-ItemProperty 'HKLM:\SOFTWARE\EpicGames\Unreal Engine\$assoc' ``"
    Write-Warning "      -Name InstalledDirectory -Value '<path to UE $assoc>' -PropertyType String -Force"
    return $null
}

function Test-McpPort {
    param([int]$TimeoutMs = 400)
    # A closed local port does not complete ConnectAsync: Wait burns the whole timeout
    # (measured 2051 ms for a 2000 ms wait). The poll loop used to sleep 2s and then wait
    # another 2s, so the "180s" budget was about 360s. An open port returns in milliseconds
    # either way, so the short timeout only changes the down case.
    $client = New-Object System.Net.Sockets.TCPClient
    try {
        $connect = $client.ConnectAsync("127.0.0.1", $Port)
        if (-not $connect.Wait($TimeoutMs)) { return $false }
        return $client.Connected
    } catch {
        return $false
    } finally {
        $client.Close()
    }
}

function Get-CommandLine([int]$ProcessId) {
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$ProcessId" -ErrorAction SilentlyContinue
    if ($proc) { return [string]$proc.CommandLine }
    return ""
}

function Get-McpListeners {
    # Tags each listener as headless vs GUI. Only the headless launcher carries the
    # `mcpServer` appStarter argument; its Rider.Backend child carries no marker of its own,
    # so it is identified by parentage instead.
    $pids = @(Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty OwningProcess -Unique)
    $out = @()
    foreach ($procId in $pids) {
        $cmd = Get-CommandLine $procId
        $isHeadless = ($cmd -like "*$McpStarter*")
        if (-not $isHeadless) {
            # A backend child of a headless launcher also counts as headless.
            $parent = (Get-CimInstance Win32_Process -Filter "ProcessId=$procId" -ErrorAction SilentlyContinue).ParentProcessId
            if ($parent -and ((Get-CommandLine $parent) -like "*$McpStarter*")) { $isHeadless = $true }
        }
        $out += [pscustomobject]@{ ProcessId = $procId; IsHeadless = $isHeadless; CommandLine = $cmd }
    }
    return $out
}

function Get-HeadlessTree([int]$RootPid) {
    # The launcher starts a Rider.Backend child; stopping only the launcher leaves the backend
    # alive and holding the port. Walk the parent/child graph to collect both.
    $all = @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue)
    $toVisit = @($RootPid)
    $seen = @{}
    $out = @()
    while ($toVisit.Count -gt 0) {
        $current = $toVisit[0]
        $toVisit = @($toVisit | Select-Object -Skip 1)
        if ($seen.ContainsKey($current)) { continue }
        $seen[$current] = $true
        $out += $current
        foreach ($child in ($all | Where-Object { $_.ParentProcessId -eq $current })) {
            $toVisit += $child.ProcessId
        }
    }
    return $out
}

function Show-StartupBanner {
    if (-not (Test-Path $IdeaLogDir)) { return }
    $log = Get-ChildItem $IdeaLogDir -Filter "idea.log" -File -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if (-not $log) { return }
    $hits = @(Select-String -Path $log.FullName -Pattern "MCP session invocation mode|MCP tools whitelist|SSE URL|MCP Server started on port|\* Project:" -ErrorAction SilentlyContinue)
    if ($hits.Count -eq 0) { return }
    Write-Host ("Last Rider startup lines ({0}):" -f $log.Name)
    $hits | Select-Object -Last 5 | ForEach-Object { Write-Host "  " $_.Line.Substring(0, [Math]::Min(240, $_.Line.Length)) }
}

if ($Status) {
    $listeners = @(Get-McpListeners)
    if (Test-McpPort) {
        if ($listeners.Count -eq 0) {
            Write-Host "Rider MCP reachable on 127.0.0.1:$Port (owner pid unknown)"
        }
        foreach ($l in $listeners) {
            $kind = if ($l.IsHeadless) { "headless mcpServer session" } else { "GUI Rider" }
            Write-Host "Rider MCP reachable on 127.0.0.1:$Port - $kind (pid $($l.ProcessId))"
        }
        Show-StartupBanner
        Write-Host "Dial it with: http://127.0.0.1:$Port/stream   (legacy SSE: http://127.0.0.1:$Port/sse)"
        exit 0
    }
    Write-Host "Nothing reachable on 127.0.0.1:$Port"
    exit 1
}

if ($Stop) {
    $headless = @(Get-McpListeners | Where-Object { $_.IsHeadless })
    if ($headless.Count -eq 0) {
        if (Test-McpPort) {
            Write-Host "Port $Port is held by a GUI Rider, not a headless session; leaving it alone. Close Rider yourself if you meant to."
            exit 0
        }
        Write-Host "Nothing reachable on 127.0.0.1:$Port; nothing to stop"
        exit 0
    }

    $kill = @()
    foreach ($l in $headless) { $kill += Get-HeadlessTree $l.ProcessId }
    $kill = @($kill | Sort-Object -Unique)
    foreach ($procId in $kill) {
        Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 3

    if (Test-McpPort) {
        Write-Host "Stopped pids $($kill -join ', ') but something still holds port $Port; inspect with -Status."
        exit 1
    }
    Write-Host "Stopped headless Rider MCP session (pids $($kill -join ', '))"
    exit 0
}

if (-not (Test-McpPort)) {
    if (-not (Test-Path -LiteralPath $RiderExe)) {
        Write-Error "Rider not found at $RiderExe. Install Rider or update `$RiderExe in this script."
        exit 2
    }

    $gui = @(Get-McpListeners | Where-Object { -not $_.IsHeadless })
    if ($gui.Count -gt 0) {
        # The GUI binds the port first, so a headless launch would fail to start its server.
        Write-Host "A GUI Rider already serves MCP on port $Port (pid $($gui[0].ProcessId)); using it instead of starting a headless session."
        Show-StartupBanner
        exit 0
    }

    $dotNetRoot = Test-DotNetPrerequisite
    if ($dotNetRoot) { Write-Host "dotnet with .NET 10: $dotNetRoot" }

    $engineRoot = Test-UnrealEnginePrerequisite -UProjectPath $Project
    if ($engineRoot) { Write-Host "Unreal Engine: $engineRoot" }

    $riderArgs = @($McpStarter, "--project=$Project", "--port=$Port",
        "--allowed-tools=$AllowedTools")
    if ($InvocationMode) { $riderArgs += "--invocation-mode=$InvocationMode" }
    Write-Host "Launching: $RiderExe $($riderArgs -join ' ')"

    $proc = Start-Process -FilePath $RiderExe -ArgumentList $riderArgs -WindowStyle Hidden -PassThru

    # Rider opens the port only after the project is loaded and indexes reach smart mode,
    # which took ~35-60s on a cold cache here. Poll the socket rather than trusting Start-Process.
    # 400 ms connect + 800 ms sleep, capped at 180 s of wall clock.
    $deadline = [Diagnostics.Stopwatch]::StartNew()
    while ($deadline.Elapsed.TotalSeconds -lt 180) {
        if (Test-McpPort -TimeoutMs 400) { break }
        Start-Sleep -Milliseconds 800
    }

    if (-not (Test-McpPort -TimeoutMs 400)) {
        Write-Error "Rider MCP did not become reachable on 127.0.0.1:$Port within 180s. Check idea.log in $IdeaLogDir."
        exit 1
    }
}

$listeners = @(Get-McpListeners)
if ($listeners.Count -eq 0) {
    Write-Host "Rider MCP reachable on 127.0.0.1:$Port (owner pid unknown)"
} else {
    foreach ($l in $listeners) {
        $kind = if ($l.IsHeadless) { "headless mcpServer session" } else { "GUI Rider" }
        Write-Host "Rider MCP reachable on 127.0.0.1:$Port - $kind (pid $($l.ProcessId))"
    }
}
Show-StartupBanner
Write-Host "URL (streamable): http://127.0.0.1:$Port/stream   (legacy SSE: http://127.0.0.1:$Port/sse)"
Write-Host "Stop the headless session with: .\Tools\Start-RiderMcp.ps1 -Stop  (leaves any GUI Rider alone)"
exit 0

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
#                  'via-router' hides them behind the single execute_tool, and in this build
#                  silently drops rename_refactoring and every xdebug_* tool from the
#                  routable set (observed: 32 of 48 named tools reached the router).
#   -Project:      File to open. Defaults to HomeWorld.sln when present, else HomeWorld.uproject.
#                  See the $ProjectDefault comment above for why .sln is the working default.
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

# The prerequisite that decides whether any of this returns real C++ symbols.
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
    # Semantic navigation, call hierarchy and UHT/C++ diagnostics, refactoring, UE asset reads and
    # the xdebug_* debugger surface the ue-live-debugging skill needs. Deliberately absent:
    # execute_terminal_command, execute_run_configuration, build_solution_start/state,
    # create_new_file, apply_patch, read_file, list_directory_tree, open_file_in_editor,
    # reformat_file, git_status, get_repositories, ue_execute_python, ue_play, spawn_actor,
    # viewport_camera, take_screenshot, ue_import/export_blueprint_nodes, plus the SQL/Unity
    # tools this project does not use.
    $AllowedTools = (@(
        # search
        "search_symbol", "search_file", "search_text", "search_regex"
        # semantic analysis and navigation
        "get_symbol_info", "analyze_calls", "get_class_hierarchy", "find_default_value_overrides", "findTests"
        # project model
        "get_solution_projects", "get_project_dependencies"
        # diagnostics (incl. UHT / C++ problems)
        "get_file_problems", "get_project_problems", "lint_files"
        # refactoring
        "rename_refactoring", "safe_delete", "extract_method", "extract_interface", "extract_base_class",
        "change_api_signature", "move_type_to_namespace", "reorganize_namespaces", "post_edit_quality_check"
        # inspections
        "run_inspection_kts", "generate_inspection_kts_examples", "generate_inspection_kts_api"
        # UE asset / status reads
        "ue_health", "ue_status", "ue_get_logs", "get_asset_properties", "search_assets", "search_tags"
        # debugger (ue-live-debugging skill)
        "xdebug_start_debugger_session", "xdebug_attach_to_process", "xdebug_control_session",
        "xdebug_get_stack", "xdebug_get_threads", "xdebug_get_frame_values", "xdebug_get_value_by_path",
        "xdebug_evaluate_expression", "xdebug_set_breakpoint", "xdebug_list_breakpoints",
        "xdebug_remove_breakpoint", "xdebug_run_to_line", "xdebug_set_variable",
        "xdebug_get_debugger_status", "xdebug_memory_dump", "xdebug_start_mixed_mode_debug"
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

function Test-McpPort {
    $client = New-Object System.Net.Sockets.TCPClient
    try {
        $connect = $client.ConnectAsync("127.0.0.1", $Port)
        if (-not $connect.Wait(2000)) { return $false }
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

    $riderArgs = @($McpStarter, "--project=$Project", "--port=$Port",
        "--allowed-tools=$AllowedTools")
    if ($InvocationMode) { $riderArgs += "--invocation-mode=$InvocationMode" }
    Write-Host "Launching: $RiderExe $($riderArgs -join ' ')"

    $proc = Start-Process -FilePath $RiderExe -ArgumentList $riderArgs -WindowStyle Hidden -PassThru

    # Rider opens the port only after the project is loaded and indexes reach smart mode,
    # which took ~35-60s on a cold cache here. Poll the socket rather than trusting Start-Process.
    for ($i = 0; $i -lt 90; $i++) {
        Start-Sleep -Seconds 2
        if (Test-McpPort) { break }
    }

    if (-not (Test-McpPort)) {
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

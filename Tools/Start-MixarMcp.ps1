# Start-MixarMcp.ps1 - Start the Mixar MCP server headlessly and wait until it is actually listening.
#
# Mixar is a Blender 4.2.2 fork (mixar.exe --version says so; bpy.app.version returns a
# spoofed (5, 2, 0) that exists only so extensions requiring >=5.1 install). It serves the
# official Blender Lab MCP add-on, installed at
# %APPDATA%\Mixar\Mixar\5.2\extensions\user_default\mcp (note the doubled Mixar).
#
# The add-on registers a headless CLI command named "blender_mcp" (NOT its module id,
# "bl_ext.user_default.mcp", which is rejected). That command blocks until interrupted,
# so it is launched as a detached background process here.
#
# Usage: From project root, .\Tools\Start-MixarMcp.ps1 [-BindHost 127.0.0.1] [-Port 9876] [-Stop] [-Status]
#
#   -BindHost: Bind address. Default 127.0.0.1 keeps the socket local. (Named to avoid
#              clashing with PowerShell's read-only $Host automatic variable.)
#   -Port:     MCP socket port. Must match what the MCP client dials (default 9876).
#   -Stop:     Stop the server listening on the port.
#   -Status:   Report whether the port is reachable, then exit.
#
# Exit code: 0 = reachable (or stopped/quiet as asked); 1 = not reachable / failed to start;
#            2 = Mixar not found.
#
# Liveness is decided by actually opening a TCP connection, not by Get-NetTCPConnection.
# That cmdlet was observed flapping between two different owning pids on consecutive
# samples when a stale server was present, which made an "already running" guard miss a
# live server and launch a duplicate.
#
# Online access note: the add-on refuses to start without network permission. It is
# already enabled persistently in Mixar (preferences.system.use_online_access), so
# --online-mode is not needed. If someone reverts that preference, add --online-mode to
# the argument list below and the add-on will work again.

param(
    [string]$BindHost = "127.0.0.1",
    [int]$Port = 9876,
    [switch]$Stop,
    [switch]$Status
)

$ErrorActionPreference = "Stop"

$MixarExe = "C:\Program Files\Mixar\mixar.exe"

function Test-McpPort {
    $client = New-Object System.Net.Sockets.TCPClient
    try {
        $connect = $client.ConnectAsync($BindHost, $Port)
        if (-not $connect.Wait(2000)) { return $false }
        return $client.Connected
    } catch {
        return $false
    } finally {
        $client.Close()
    }
}

function Get-McpListeners {
    # Returns every process holding the port, tagged headless vs GUI.
    # The GUI Mixar also serves MCP on this port (the add-on is enabled persistently and
    # starts its socket on launch), so "is anything listening" is not the same question
    # as "is the headless server up".
    $pids = @(Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty OwningProcess -Unique)
    $out = @()
    foreach ($procId in $pids) {
        $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$procId" -ErrorAction SilentlyContinue
        $isHeadless = $false
        $cmd = ""
        if ($proc) {
            $cmd = [string]$proc.CommandLine
            $isHeadless = ($cmd -like "*blender_mcp*")
        }
        $out += [pscustomobject]@{ ProcessId = $procId; IsHeadless = $isHeadless; CommandLine = $cmd }
    }
    return $out
}

if ($Status) {
    $listeners = @(Get-McpListeners)
    if (Test-McpPort) {
        if ($listeners.Count -eq 0) {
            Write-Host "MCP reachable on ${BindHost}:$Port (owner pid unknown)"
        }
        foreach ($l in $listeners) {
            $kind = if ($l.IsHeadless) { "headless server" } else { "GUI Mixar" }
            Write-Host "MCP reachable on ${BindHost}:$Port - $kind (pid $($l.ProcessId))"
        }
        exit 0
    }
    Write-Host "Nothing reachable on ${BindHost}:$Port"
    exit 1
}

if ($Stop) {
    # Kill ONLY headless servers. The GUI Mixar shares this port and must survive: it can
    # hold unsaved work, and a previous version of this script killed it because it read
    # the GUI as a socket owner. Command line is the only reliable discriminator.
    $headless = @(Get-McpListeners | Where-Object { $_.IsHeadless })
    if ($headless.Count -eq 0) {
        if (Test-McpPort) {
            Write-Host "Port $Port is held by a GUI Mixar, not a headless server; leaving it alone. Close Mixar yourself if you meant to."
            exit 0
        }
        Write-Host "Nothing reachable on ${BindHost}:$Port; nothing to stop"
        exit 0
    }

    foreach ($l in $headless) {
        Stop-Process -Id $l.ProcessId -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 2

    $stillHeadless = @(Get-McpListeners | Where-Object { $_.IsHeadless })
    if ($stillHeadless.Count -gt 0) {
        Write-Host "Stopped pids $($headless.ProcessId -join ', ') but headless server(s) $( $stillHeadless.ProcessId -join ', ') still hold port $Port; stop them manually."
        exit 1
    }
    Write-Host "Stopped headless MCP server(s) on port $Port (pid $($headless.ProcessId -join ', '))"
    $gui = @(Get-McpListeners)
    if ($gui.Count -gt 0) {
        Write-Host "GUI Mixar still serving port $Port (pid $($gui.ProcessId -join ', ')) - left running on purpose."
    }
    exit 0
}

if (-not (Test-McpPort)) {
    if (-not (Test-Path -LiteralPath $MixarExe)) {
        Write-Error "Mixar not found at $MixarExe. Install Mixar or update `$MixarExe in this script."
        exit 2
    }

    # Named to avoid clobbering PowerShell's automatic $args variable.
    $mixarArgs = @("--background", "--command", "blender_mcp", "--host", $BindHost, "--port", "$Port")
    Write-Host "Launching: $MixarExe $($mixarArgs -join ' ')"

    $proc = Start-Process -FilePath $MixarExe -ArgumentList $mixarArgs -WindowStyle Hidden -PassThru

    # Poll the socket rather than trusting Start-Process. The add-on exits with a printed
    # error (for example "Online access must be enabled") instead of listening, so a
    # successful start is only proven by an actual reachable port.
    for ($i = 0; $i -lt 30; $i++) {
        Start-Sleep -Seconds 2
        if (Test-McpPort) { break }
        if ($proc.HasExited) {
            Write-Error "Mixar exited (code $($proc.ExitCode)) without listening on port $Port. Check the Mixar add-on is enabled and online access is permitted."
            exit 1
        }
    }

    if (-not (Test-McpPort)) {
        Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
        Write-Error "Mixar did not become reachable on port $Port within 60s; stopped pid $($proc.Id)."
        exit 1
    }
}

$listeners = @(Get-McpListeners)
if ($listeners.Count -eq 0) {
    Write-Host "MCP reachable on ${BindHost}:$Port (owner pid unknown)"
} else {
    foreach ($l in $listeners) {
        $kind = if ($l.IsHeadless) { "headless server" } else { "GUI Mixar" }
        Write-Host "MCP reachable on ${BindHost}:$Port - $kind (pid $($l.ProcessId))"
    }
}
Write-Host "Stop the headless server with: .\Tools\Start-MixarMcp.ps1 -Stop  (leaves any GUI Mixar alone)"
exit 0
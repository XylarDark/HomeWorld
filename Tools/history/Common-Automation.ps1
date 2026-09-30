# Common-Automation.ps1 - Shared helpers for automation scripts.
# Dot-source from RunAutomationLoop.ps1, Safe-Build.ps1, Check-AutomationPrereqs.ps1, Watch, Guard, Refiner, GapSolver, Start-*.
# Use Test-UE_EDITORSet so we never pass null to Test-Path -LiteralPath $env:UE_EDITOR (causes ParameterBindingValidationException).

function Test-UE_EDITORSet {
    if (-not $env:UE_EDITOR -or [string]::IsNullOrWhiteSpace($env:UE_EDITOR)) {
        return $false
    }
    try {
        return (Test-Path -LiteralPath $env:UE_EDITOR)
    } catch {
        return $false
    }
}

# Returns project root: HOMEWORLD_PROJECT if set, else parent of Tools folder (caller's $PSScriptRoot).
function Resolve-ProjectRoot {
    param([string]$ScriptRoot = $PSScriptRoot)
    $root = $env:HOMEWORLD_PROJECT
    if (-not $root -or [string]::IsNullOrWhiteSpace($root)) {
        $root = (Resolve-Path (Join-Path $ScriptRoot "..")).Path
    }
    return $root.TrimEnd("\", "/")
}

# Returns path to Cursor Agent CLI (agent.exe, agent.cmd, or agent.ps1), or $null if not found.
# -AgentPath: if provided and file exists, return it; else search standard locations.
function Get-AgentExe {
    param([string]$AgentPath = "")
    if ($AgentPath -and (Test-Path -LiteralPath $AgentPath)) { return $AgentPath }
    $cmd = Get-Command agent -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $searchDirs = @(
        (Join-Path $env:LOCALAPPDATA "cursor-cli"),
        (Join-Path (Join-Path $env:LOCALAPPDATA "Cursor") "agent"),
        (Join-Path (Join-Path $env:USERPROFILE ".cursor") "bin"),
        (Join-Path $env:APPDATA "cursor-cli"),
        (Join-Path (Join-Path $env:LOCALAPPDATA "Programs") "cursor-cli"),
        (Join-Path $env:LOCALAPPDATA "cursor-agent")
    )
    foreach ($dir in $searchDirs) {
        if (-not $dir -or -not (Test-Path $dir)) { continue }
        $exe = Join-Path $dir "agent.exe"
        if (Test-Path -LiteralPath $exe) { return $exe }
        $c = Join-Path $dir "agent.cmd"
        if (Test-Path -LiteralPath $c) { return $c }
        $p = Join-Path $dir "agent.ps1"
        if (Test-Path -LiteralPath $p) { return $p }
    }
    return $null
}

# Single-instance guard: only one automation loop (RunAutomationLoop) should run per project.
# Lock file: Saved/Logs/automation_loop.lock contains the PID of the PowerShell process running the loop.
# If the lock exists and that process is still running, a second "start agents in new window" will refuse to start.
function Get-AutomationLoopLockPath {
    $root = Resolve-ProjectRoot
    return Join-Path (Join-Path (Join-Path $root "Saved") "Logs") "automation_loop.lock"
}
function Test-AutomationLoopRunning {
    $lockPath = Get-AutomationLoopLockPath
    if (-not (Test-Path -LiteralPath $lockPath)) { return $false }
    try {
        $content = Get-Content -Path $lockPath -Raw -ErrorAction Stop
        if (-not $content -or -not ($content.Trim() -match '^\d+$')) { return $false }
        $pidNum = [int]$Matches[0]
        $proc = Get-Process -Id $pidNum -ErrorAction SilentlyContinue
        return ($null -ne $proc)
    } catch {
        return $false
    }
}
function Set-AutomationLoopLock {
    $lockPath = Get-AutomationLoopLockPath
    $dir = Split-Path -Parent $lockPath
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    Set-Content -Path $lockPath -Value $PID -Encoding UTF8 -NoNewline -ErrorAction SilentlyContinue
}
function Remove-AutomationLoopLock {
    $lockPath = Get-AutomationLoopLockPath
    if (Test-Path -LiteralPath $lockPath) { Remove-Item -LiteralPath $lockPath -Force -ErrorAction SilentlyContinue }
}

# High-level event stream: one line to Saved/Logs/automation_events.log and terminal.
# Event types: round_completed, build_validated, build_failed, fixer_invoked, guardian_invoked, loop_exited_ok, loop_exited_fail, plus any custom (e.g. PIE validation).
# Callers that also want loop/watcher logs call Write-LoopLog/Write-WatcherLog separately.
function Write-AutomationEvent {
    param(
        [Parameter(Mandatory=$true)][string]$EventType,
        [Parameter(Mandatory=$true)][string]$Message
    )
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] [$EventType] $Message"
    $root = Resolve-ProjectRoot
    $logsDir = Join-Path (Join-Path $root "Saved") "Logs"
    $eventsPath = Join-Path $logsDir "automation_events.log"
    if (-not (Test-Path -LiteralPath $logsDir)) {
        New-Item -ItemType Directory -Path $logsDir -Force | Out-Null
    }
    try {
        Add-Content -Path $eventsPath -Value $line -Encoding UTF8 -ErrorAction SilentlyContinue
    } catch {}
    # Terminal: success=Green, failure=Red, info=Gray
    $isSuccess = $EventType -in "round_completed", "build_validated", "loop_exited_ok"
    $isFailure = $EventType -in "build_failed", "loop_exited_fail", "fixer_invoked", "guardian_invoked"
    if ($isSuccess) {
        Write-Host $line -ForegroundColor Green
    } elseif ($isFailure) {
        Write-Host $line -ForegroundColor Red
    } else {
        Write-Host $line -ForegroundColor Gray
    }
}

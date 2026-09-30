# Watch-HeartbeatStall.ps1 - Stall protection: kill the agent if the heartbeat has not updated for too long.
# Run automatically from RunAutomationLoop when -StallProtection is enabled, or manually in a second terminal.
# When the main loop is stuck (e.g. agent hung), the loop stops writing heartbeats; this script detects that
# and kills the agent process so the job completes and the loop can exit (then Fixer can run).
#
# Usage: .\Tools\Watch-HeartbeatStall.ps1 [-ParentPID <pid>] [-ProjectRoot <path>] [-StallThresholdMinutes <n>] [-CheckIntervalMinutes <n>]
#   -ParentPID: When given, exit when this process no longer exists (loop exited). RunAutomationLoop starts this with its own PID.
#   -ProjectRoot: Project root for Saved/Logs paths (default: resolve from script).
#   -StallThresholdMinutes: Consider stalled if heartbeat/last_activity not updated in this many minutes (default 15).
#   -CheckIntervalMinutes: How often to check (default 3).

param(
    [int]$ParentPID = 0,
    [string]$ProjectRoot = "",
    [int]$StallThresholdMinutes = 15,
    [int]$CheckIntervalMinutes = 3
)

$ErrorActionPreference = "SilentlyContinue"
$scriptRoot = $PSScriptRoot
$commonScript = Join-Path $scriptRoot "Common-Automation.ps1"
if (Test-Path -LiteralPath $commonScript) { . $commonScript }
if (-not $ProjectRoot) { $ProjectRoot = Resolve-ProjectRoot }
$ProjectRoot = $ProjectRoot.TrimEnd("\", "/")
$LogsDir = Join-Path $ProjectRoot "Saved\Logs"
$HeartbeatPath = Join-Path $LogsDir "automation_heartbeat.log"
$LastActivityPath = Join-Path $ProjectRoot "Saved\automation_last_activity.json"
$StallLogPath = Join-Path $LogsDir "stall_watcher.log"
$ErrorsLogPath = Join-Path $LogsDir "automation_errors.log"

function Write-StallLog {
    param([string]$Message)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] $Message"
    if ($StallLogPath) {
        try { Add-Content -Path $StallLogPath -Value $line -Encoding UTF8 -ErrorAction SilentlyContinue } catch {}
    }
}

# If parent PID given, exit when parent process is gone
if ($ParentPID -gt 0) {
    $parent = Get-Process -Id $ParentPID -ErrorAction SilentlyContinue
    if (-not $parent) {
        Write-StallLog "Watch-HeartbeatStall: parent PID $ParentPID not found; exiting."
        exit 0
    }
}

$stallThreshold = [TimeSpan]::FromMinutes($StallThresholdMinutes)
$checkIntervalSec = [math]::Max(60, $CheckIntervalMinutes * 60)

while ($true) {
    if ($ParentPID -gt 0) {
        $parent = Get-Process -Id $ParentPID -ErrorAction SilentlyContinue
        if (-not $parent) {
            Write-StallLog "Watch-HeartbeatStall: parent process $ParentPID ended; exiting."
            exit 0
        }
    }

    $agentProcs = Get-Process -Name "agent" -ErrorAction SilentlyContinue
    $agentRunning = ($agentProcs -and $agentProcs.Count -gt 0)

    if ($agentRunning) {
        $oldest = $null
        foreach ($path in @($HeartbeatPath, $LastActivityPath)) {
            if (Test-Path -LiteralPath $path) {
                $lastWrite = (Get-Item -LiteralPath $path -ErrorAction SilentlyContinue).LastWriteTime
                if (-not $oldest -or $lastWrite -lt $oldest) { $oldest = $lastWrite }
            }
        }
        if ($oldest) {
            $age = (Get-Date) - $oldest
            if ($age -ge $stallThreshold) {
                $stallMsg = "Watch-HeartbeatStall: STALL DETECTED. Heartbeat/last_activity not updated for $([math]::Round($age.TotalMinutes, 1)) min (threshold $StallThresholdMinutes min). Killing agent process(es)."
                Write-StallLog $stallMsg
                if ($ErrorsLogPath) { try { Add-Content -Path $ErrorsLogPath -Value "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $stallMsg" -Encoding UTF8 -ErrorAction SilentlyContinue } catch {} }
                foreach ($p in $agentProcs) {
                    try {
                        Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
                        Write-StallLog "Watch-HeartbeatStall: killed agent PID $($p.Id)."
                    } catch {}
                }
            }
        }
    }

    Start-Sleep -Seconds $checkIntervalSec
}

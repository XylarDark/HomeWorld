# Start-AllAgents.ps1 - One script to start the full agent company (Developer, Fixer, Guardian).
# Installs Cursor Agent CLI if missing, then runs the Watcher, which runs the Developer loop and
# invokes the Fixer on failure and the Guardian when the same failure recurs. Editor auto-launches
# before the first round when UE_EDITOR is set (use -NoLaunchEditor to skip).
#
# Usage: From project root, .\Tools\Start-AllAgents.ps1 [same params as Watch-AutomationAndFix.ps1]
#   -MaxFixRounds: Max fix-agent rounds before invoking Guardian and exiting (default 3).
#   -NoRetryAfterFix: After a fix round, exit instead of re-running the loop.
#   -NoPauseOnComplete: Do not pause at success (default is to pause and show status so you can confirm the loop finished normally).
#   -NoLaunchEditor: Do not auto-launch the Editor (default is to launch when UE_EDITOR set).
#   -SkipInstall: Do not install the CLI if missing; fail instead.
#   -Verbose: Pass through for prompt preview and elapsed time.
#
# See docs/AGENT_COMPANY.md for roles and accountability.

param(
    [int]$MaxFixRounds = 3,
    [switch]$NoRetryAfterFix,
    [switch]$NoPauseOnComplete,
    [string]$ProjectRoot = "",
    [string]$PromptFile = "",
    [switch]$NoLaunchEditor,
    [string]$Model = "auto",
    [string]$AgentPath = "",
    [switch]$SkipInstall,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$commonScript = Join-Path $PSScriptRoot "Common-Automation.ps1"
if (Test-Path -LiteralPath $commonScript) { . $commonScript }
if (-not $ProjectRoot) { $ProjectRoot = Resolve-ProjectRoot }
$ProjectRoot = $ProjectRoot.TrimEnd("\", "/")
if (-not (Test-Path $ProjectRoot)) {
    Write-Error "Project root not found: $ProjectRoot"
    if (-not $NoPauseOnComplete) { Read-Host "Press Enter to close this window" }
    exit 1
}

function Refresh-EnvPath {
    $userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
    $machinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    if ($userPath) { $env:Path = $userPath + ";" + $env:Path }
    if ($machinePath) { $env:Path = $machinePath + ";" + $env:Path }
}

# Ensure CLI is available (install if missing and not -SkipInstall)
$agentExe = Get-AgentExe -AgentPath $AgentPath
if (-not $agentExe) { Refresh-EnvPath; $agentExe = Get-AgentExe -AgentPath $AgentPath }

if (-not $agentExe -and -not $SkipInstall) {
    Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Start-AllAgents: Cursor Agent CLI not found. Installing..."
    try {
        irm 'https://cursor.com/install?win32=true' | iex
    } catch {
        Write-Error "Install failed: $_"
        if (-not $NoPauseOnComplete) { Read-Host "Press Enter to close this window" }
        exit 1
    }
    Refresh-EnvPath
    $agentExe = Find-AgentExe
}

if (-not $agentExe) {
    Write-Error "Cursor Agent CLI (agent) not found. Install manually or run without -SkipInstall."
    if (-not $NoPauseOnComplete) { Read-Host "Press Enter to close this window" }
    exit 1
}

Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Start-AllAgents: starting agent company (Developer + Fixer + Guardian via Watcher)..."
$watcherScript = Join-Path $PSScriptRoot "Watch-AutomationAndFix.ps1"
$watcherArgs = @{
    ProjectRoot    = $ProjectRoot
    AgentPath      = $agentExe
    MaxFixRounds   = $MaxFixRounds
}
if ($NoRetryAfterFix) { $watcherArgs["NoRetryAfterFix"] = $true }
if ($NoPauseOnComplete) { $watcherArgs["NoPauseOnComplete"] = $true }
if ($PromptFile) { $watcherArgs["PromptFile"] = $PromptFile }
if ($NoLaunchEditor) { $watcherArgs["NoLaunchEditor"] = $true }
if ($Model) { $watcherArgs["Model"] = $Model }
if ($SkipInstall) { $watcherArgs["SkipInstall"] = $true }
if ($Verbose) { $watcherArgs["Verbose"] = $true }

& $watcherScript @watcherArgs
$exitCode = $LASTEXITCODE

# Keep terminal open so you can see output and confirm how the run ended (success, failure, or stop)
if (-not $NoPauseOnComplete) {
    Write-Host ""
    Read-Host "Press Enter to close this window"
}
exit $exitCode

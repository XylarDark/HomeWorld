# Start-AllAgents.ps1 - One script to start the full agent company (Developer, Fixer, Guardian).
# Installs Cursor Agent CLI if missing, then runs the Watcher, which runs the Developer loop and
# invokes the Fixer on failure and the Guardian when the same failure recurs. Editor auto-launches
# before the first round when UE_EDITOR is set (use -NoLaunchEditor to skip).
#
# Usage: From project root, .\Tools\Start-AllAgents.ps1 [same params as Watch-AutomationAndFix.ps1]
#   -MaxFixRounds: Max fix-agent rounds before invoking Guardian and exiting (default 3).
#   -NoRetryAfterFix: After a fix round, exit instead of re-running the loop.
#   -NoLaunchEditor: Do not auto-launch the Editor (default is to launch when UE_EDITOR set).
#   -SkipInstall: Do not install the CLI if missing; fail instead.
#   -Verbose: Pass through for prompt preview and elapsed time.
#
# See docs/AGENT_COMPANY.md for roles and accountability.

param(
    [int]$MaxFixRounds = 3,
    [switch]$NoRetryAfterFix,
    [string]$ProjectRoot = "",
    [string]$PromptFile = "",
    [switch]$NoLaunchEditor,
    [string]$Model = "auto",
    [string]$AgentPath = "",
    [switch]$SkipInstall,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

# Resolve project root
if (-not $ProjectRoot) { $ProjectRoot = $env:HOMEWORLD_PROJECT }
if (-not $ProjectRoot) { $ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path }
$ProjectRoot = $ProjectRoot.TrimEnd("\", "/")
if (-not (Test-Path $ProjectRoot)) {
    Write-Error "Project root not found: $ProjectRoot"
    exit 1
}

function Refresh-EnvPath {
    $userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
    $machinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    if ($userPath) { $env:Path = $userPath + ";" + $env:Path }
    if ($machinePath) { $env:Path = $machinePath + ";" + $env:Path }
}

function Find-AgentExe {
    $cmd = Get-Command agent -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $searchDirs = @(
        (Join-Path $env:LOCALAPPDATA "cursor-cli"),
        (Join-Path (Join-Path $env:LOCALAPPDATA "Cursor") "agent"),
        (Join-Path (Join-Path $env:USERPROFILE ".cursor") "bin"),
        (Join-Path $env:APPDATA "cursor-cli"),
        (Join-Path (Join-Path $env:LOCALAPPDATA "Programs") "cursor-cli")
    )
    foreach ($dir in $searchDirs) {
        if (-not $dir -or -not (Test-Path $dir)) { continue }
        $exe = Join-Path $dir "agent.exe"
        if (Test-Path -LiteralPath $exe) { return $exe }
        $cmd = Join-Path $dir "agent.cmd"
        if (Test-Path -LiteralPath $cmd) { return $cmd }
    }
    return $null
}

# Ensure CLI is available (install if missing and not -SkipInstall)
$agentExe = $null
if ($AgentPath -and (Test-Path -LiteralPath $AgentPath)) {
    $agentExe = $AgentPath
}
if (-not $agentExe) { $agentExe = Find-AgentExe }
if (-not $agentExe) { Refresh-EnvPath; $agentExe = Find-AgentExe }

if (-not $agentExe -and -not $SkipInstall) {
    Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Start-AllAgents: Cursor Agent CLI not found. Installing..."
    try {
        irm 'https://cursor.com/install?win32=true' | iex
    } catch {
        Write-Error "Install failed: $_"
        exit 1
    }
    Refresh-EnvPath
    $agentExe = Find-AgentExe
}

if (-not $agentExe) {
    Write-Error "Cursor Agent CLI (agent) not found. Install manually or run without -SkipInstall."
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
if ($PromptFile) { $watcherArgs["PromptFile"] = $PromptFile }
if ($NoLaunchEditor) { $watcherArgs["NoLaunchEditor"] = $true }
if ($Model) { $watcherArgs["Model"] = $Model }
if ($SkipInstall) { $watcherArgs["SkipInstall"] = $true }
if ($Verbose) { $watcherArgs["Verbose"] = $true }

& $watcherScript @watcherArgs
exit $LASTEXITCODE

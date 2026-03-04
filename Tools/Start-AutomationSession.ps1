# Start-AutomationSession.ps1 - One-command start for the 30-day automation loop.
# Installs Cursor Agent CLI if missing, then runs RunAutomationLoop.ps1.
# Use this when you want to "start an automation session" without manually installing the CLI or restarting the terminal.
#
# Usage: From project root, .\Tools\Start-AutomationSession.ps1 [same params as RunAutomationLoop.ps1]
#   -SkipInstall: Do not run the CLI install; only start the loop (fail if agent not found).
#   -Verbose: Pass through to RunAutomationLoop for prompt preview and elapsed time per round (easier to see progress/stalls).
#   All other parameters are passed through to RunAutomationLoop.ps1.
#
# Prerequisites: After first run you may need to run "agent login" once to authenticate.

param(
    [string]$ProjectRoot = "",
    [string]$PromptFile = "",
    [switch]$NoLaunchEditor,  # pass through: run without auto-launching the Editor (default is to launch when UE_EDITOR set)
    [string]$Model = "auto",
    [string]$AgentPath = "",
    [switch]$SkipInstall,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

# Resolve project root (same as RunAutomationLoop)
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

# 1) Already on PATH or explicit path?
$agentExe = $null
function Write-SessionLog { param([string]$Msg) Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Msg" }
if ($AgentPath -and (Test-Path -LiteralPath $AgentPath)) {
    $agentExe = $AgentPath
    Write-SessionLog "Start-AutomationSession: using agent at $AgentPath"
}
if (-not $agentExe) {
    $agentExe = Find-AgentExe
    if ($agentExe) { Write-SessionLog "Start-AutomationSession: found agent at $agentExe" }
}

# 2) Refresh PATH and try again
if (-not $agentExe) {
    Refresh-EnvPath
    $agentExe = Find-AgentExe
}

# 3) Install if missing and not -SkipInstall
if (-not $agentExe -and -not $SkipInstall) {
    Write-SessionLog "Start-AutomationSession: Cursor Agent CLI not found. Installing..."
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
    Write-Error "Cursor Agent CLI (agent) not found. Install manually: irm 'https://cursor.com/install?win32=true' | iex ; then close and reopen your terminal and run this script again."
    exit 1
}

# Build args for RunAutomationLoop.ps1 (pass resolved path so loop does not depend on PATH)
$loopArgs = @{
    ProjectRoot = $ProjectRoot
    AgentPath   = $agentExe
}
if ($PromptFile) { $loopArgs["PromptFile"] = $PromptFile }
if ($NoLaunchEditor) { $loopArgs["NoLaunchEditor"] = $true }
if ($Model) { $loopArgs["Model"] = $Model }
if ($Verbose) { $loopArgs["Verbose"] = $true }

Write-SessionLog "Start-AutomationSession: launching loop script..."
$loopScript = Join-Path $PSScriptRoot "RunAutomationLoop.ps1"
& $loopScript @loopArgs
exit $LASTEXITCODE
